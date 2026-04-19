#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image remix toolbox for ppt-master game-asset pipeline.

Three orthogonal capabilities, all CLI-callable in one tool:

  1. COLLAGE     — multi-image PIL stitching (offline, no API).
                   Layouts: grid (auto), 2x1, 1x2, 2x2, 3x1, 1x3, hstrip, vstrip.

  2. I2I         — Seedream image-to-image. Sends a reference image (URL or
                   local file → base64) plus a text prompt to ARK Seedream.
                   If the live API rejects the i2i payload (older model /
                   unsupported field), automatically falls back to mode 4.

  3. DESCRIBE+T2I — Doubao Vision describes the reference (or collage), then
                    Seedream text-to-image generates a fresh variant. Pure
                    safety-net for when i2i is unavailable.

  4. REMIX       — combo: collage N reference frames into one composite, then
                   pipe that composite through I2I (or describe+t2i fallback).

Origin: distilled from `丁开心的游戏观察/sources/gen_images.py` plus new i2i +
collage logic. Reads the same `.env` as ppt-master `image_gen.py` so any key
that already works for `IMAGE_BACKEND=volcengine` works here too.

Usage examples:

  # 1) Stitch 4 reference frames into a 2x2 composite
  python image_remix.py collage \
      ref1.jpg ref2.jpg ref3.jpg ref4.jpg \
      --layout 2x2 --gap 12 --bg "#ffffff" -o composite.jpg

  # 2) Image-to-image: take a reference, restyle it
  python image_remix.py i2i ref.jpg \
      --prompt "Pixar-style cute fox shopkeeper running a TCG card store, soft pastel palette" \
      --aspect 16:9 -o variant.jpg

  # 3) Describe + text-to-image (no i2i support needed)
  python image_remix.py describe-then-t2i ref.jpg \
      --prompt "Re-imagine in Studio Ghibli watercolor style" \
      --aspect 16:9 -o variant.jpg

  # 4) Remix: collage 3 refs → i2i restyle in one call
  python image_remix.py remix \
      ref1.jpg ref2.jpg ref3.jpg \
      --layout hstrip --prompt "blend these into a cohesive PPT hero illustration" \
      --aspect 21:9 -o hero.jpg

Environment:
  ARK_API_KEY  or  VOLCENGINE_API_KEY   — required for i2i / t2i
  VOLCENGINE_BASE_URL                   — optional override
  VOLCENGINE_MODEL                      — optional, default doubao-seedream-4-5-251128
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Force UTF-8 stdout/stderr so emoji + Chinese print work on Windows GBK terminals.
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# .env bootstrap (mirrors fetch_game_assets.py)
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
PPT_MASTER_ROOT = SKILL_DIR.parent.parent


def _load_dotenv() -> None:
    env_path = PPT_MASTER_ROOT / ".env"
    if not env_path.exists():
        return
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v
    except Exception:
        pass


_load_dotenv()


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


ARK_API_KEY = _env("ARK_API_KEY") or _env("VOLCENGINE_API_KEY")
ARK_BASE = _env(
    "VOLCENGINE_BASE_URL",
    "https://ark.cn-beijing.volces.com/api/v3/images/generations",
)
ARK_MODEL = _env("VOLCENGINE_MODEL", "doubao-seedream-4-5-251128")
VISION_BASE = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
VISION_MODEL = "doubao-seed-1-6-vision-250815"


# ---------------------------------------------------------------------------
# PIL helpers
# ---------------------------------------------------------------------------

def _require_pil():
    try:
        from PIL import Image, ImageColor  # noqa: F401
    except ImportError as e:
        sys.exit(f"[fatal] Pillow required: pip install Pillow ({e})")


def _open(img_path: str):
    from PIL import Image
    img = Image.open(img_path)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    return img


def _save(img, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fmt = "JPEG" if out_path.suffix.lower() in (".jpg", ".jpeg") else "PNG"
    if fmt == "JPEG" and img.mode == "RGBA":
        img = img.convert("RGB")
    img.save(out_path, format=fmt, quality=92)


# ---------------------------------------------------------------------------
# COLLAGE
# ---------------------------------------------------------------------------

LAYOUTS = {
    "grid": "auto-decide rows/cols by sqrt(N)",
    "2x1": "2 rows × 1 col (vertical pair)",
    "1x2": "1 row × 2 cols (side-by-side)",
    "2x2": "2 rows × 2 cols",
    "3x1": "3 rows × 1 col",
    "1x3": "1 row × 3 cols",
    "hstrip": "all images in a single horizontal strip",
    "vstrip": "all images in a single vertical strip",
}


def _layout_grid(n: int, layout: str) -> tuple[int, int]:
    if layout in ("hstrip", "1x" + str(n)):
        return 1, n
    if layout in ("vstrip", str(n) + "x1"):
        return n, 1
    if layout == "2x2":
        return 2, 2
    if layout == "2x1":
        return 2, 1
    if layout == "1x2":
        return 1, 2
    if layout == "3x1":
        return 3, 1
    if layout == "1x3":
        return 1, 3
    cols = max(1, int(math.ceil(math.sqrt(n))))
    rows = int(math.ceil(n / cols))
    return rows, cols


def collage(image_paths: list[str], out_path: Path, layout: str = "grid",
            gap: int = 8, bg: str = "#ffffff",
            cell_max: int = 1024) -> Path:
    """Stitch images into a composite."""
    _require_pil()
    from PIL import Image, ImageColor
    if not image_paths:
        sys.exit("[fatal] need at least 1 image to collage")

    rows, cols = _layout_grid(len(image_paths), layout)
    print(f"[collage] {len(image_paths)} images → {rows}x{cols}, gap={gap}, bg={bg}")

    imgs = [_open(p) for p in image_paths]

    # Resize each cell so longest edge ≤ cell_max
    sized = []
    for im in imgs:
        scale = cell_max / max(im.size)
        if scale < 1:
            new_size = (int(im.size[0] * scale), int(im.size[1] * scale))
            im = im.resize(new_size, Image.LANCZOS)
        sized.append(im)

    # Pad cells with black so each row has equal-height cells
    cell_w = max(im.size[0] for im in sized)
    cell_h = max(im.size[1] for im in sized)

    canvas_w = cols * cell_w + (cols + 1) * gap
    canvas_h = rows * cell_h + (rows + 1) * gap

    bg_color = ImageColor.getrgb(bg)
    canvas = Image.new("RGB", (canvas_w, canvas_h), bg_color)

    for idx, im in enumerate(sized):
        r, c = divmod(idx, cols)
        if r >= rows:
            break  # extras dropped (shouldn't happen with our layout calc)
        x = gap + c * (cell_w + gap) + (cell_w - im.size[0]) // 2
        y = gap + r * (cell_h + gap) + (cell_h - im.size[1]) // 2
        canvas.paste(im, (x, y))

    _save(canvas, out_path)
    print(f"[collage] ✓ saved {out_path}  ({canvas_w}x{canvas_h})")
    return out_path


# ---------------------------------------------------------------------------
# Image-to-base64 + URL detect
# ---------------------------------------------------------------------------

def _b64_data_uri(img_path: str, max_px: int = 2048) -> str:
    """Resize-and-encode a local image as a data: URI for ARK i2i payload."""
    from PIL import Image
    img = Image.open(img_path)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    # Down-scale to keep payload < ~5 MB (rough rule)
    if max(img.size) > max_px:
        scale = max_px / max(img.size)
        img = img.resize((int(img.size[0] * scale), int(img.size[1] * scale)),
                         Image.LANCZOS)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=88)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{b64}"


def _resolve_image_payload(ref: str) -> str:
    """If ref is http(s) URL, return as-is; else load local file as data URI."""
    if ref.startswith(("http://", "https://")):
        return ref
    p = Path(ref).expanduser().resolve()
    if not p.exists():
        sys.exit(f"[fatal] reference image not found: {p}")
    return _b64_data_uri(str(p))


# ---------------------------------------------------------------------------
# Aspect ratio → size (matches backend_volcengine)
# ---------------------------------------------------------------------------

ASPECT_TO_SIZE_1K = {
    "1:1": "2048x2048", "2:3": "1664x2496", "3:2": "2496x1664",
    "3:4": "1728x2304", "4:3": "2304x1728", "4:5": "1728x2160",
    "5:4": "2160x1728", "9:16": "1440x2560", "16:9": "2560x1440",
    "21:9": "3024x1296",
}


def _resolve_size(aspect: str) -> str:
    if "x" in aspect:  # already resolved like "1920x1080"
        return aspect
    s = ASPECT_TO_SIZE_1K.get(aspect)
    if not s:
        sys.exit(f"[fatal] unsupported aspect '{aspect}'. "
                 f"Use one of {list(ASPECT_TO_SIZE_1K)} or W x H.")
    return s


# ---------------------------------------------------------------------------
# I2I via Seedream
# ---------------------------------------------------------------------------

def _post_json(url: str, body: dict, headers: dict, timeout: int = 300):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return -1, str(e)


def i2i(ref: str, prompt: str, out_path: Path,
        aspect: str = "16:9", strength: float = 0.55,
        retries: int = 3, allow_fallback: bool = True) -> Path:
    """Seedream image-to-image. ref can be URL or local file path."""
    if not ARK_API_KEY:
        sys.exit("[fatal] ARK_API_KEY (or VOLCENGINE_API_KEY) not set in env or .env")

    image_field = _resolve_image_payload(ref)
    size = _resolve_size(aspect)

    payload = {
        "model": ARK_MODEL,
        "prompt": prompt,
        "image": image_field,
        "size": size,
        "response_format": "url",
        "watermark": False,
    }
    if strength is not None:
        payload["strength"] = float(strength)

    headers = {
        "Authorization": f"Bearer {ARK_API_KEY}",
        "Content-Type": "application/json",
    }

    print(f"[i2i] model={ARK_MODEL}  size={size}  strength={strength}")
    print(f"[i2i] ref={ref if ref.startswith('http') else Path(ref).name}")
    print(f"[i2i] prompt={prompt[:120]}{'...' if len(prompt) > 120 else ''}")

    last_err = None
    for attempt in range(1, retries + 1):
        print(f"  [..] attempt {attempt}/{retries}", end="", flush=True)
        start = time.time()
        status, body = _post_json(ARK_BASE, payload, headers, timeout=300)
        elapsed = time.time() - start
        print(f"  ({elapsed:.1f}s, status={status})")

        if status == 200:
            try:
                data = json.loads(body)
                items = data.get("data") or []
                image_url = items[0].get("url") if items else None
                if image_url:
                    return _download_to(image_url, out_path)
            except Exception as e:
                last_err = f"parse error: {e}"
                print(f"  [WARN] {last_err}")
        elif status == 400 and allow_fallback:
            # Likely "image" field unsupported → fall back to describe+t2i
            print("  [WARN] i2i payload rejected (HTTP 400). Falling back to describe-then-t2i.")
            print(f"        body: {body[:200]}")
            return describe_then_t2i(ref, prompt, out_path, aspect=aspect, retries=retries)
        elif status == 429:
            wait = 60 * attempt
            print(f"  [RATELIMIT] sleep {wait}s")
            time.sleep(wait)
            continue
        else:
            last_err = f"HTTP {status}: {body[:200]}"
            print(f"  [WARN] {last_err}")
            time.sleep(5 * attempt)

    if allow_fallback:
        print("[i2i] all attempts failed → describe-then-t2i fallback")
        return describe_then_t2i(ref, prompt, out_path, aspect=aspect, retries=retries)
    sys.exit(f"[fatal] i2i failed: {last_err}")


def _download_to(url: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "ppt-master/image_remix"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        out_path.write_bytes(resp.read())
    print(f"  [DONE] saved {out_path}  ({out_path.stat().st_size // 1024} KB)")
    return out_path


# ---------------------------------------------------------------------------
# DESCRIBE + T2I  (the universal fallback)
# ---------------------------------------------------------------------------

def vision_describe(ref: str, hint: str = "") -> str:
    """Use Doubao Vision to produce a detailed description of the reference."""
    if not ARK_API_KEY:
        sys.exit("[fatal] ARK_API_KEY not set")

    image_field = _resolve_image_payload(ref)
    sys_prompt = (
        "You are an art director writing a precise illustration prompt. "
        "Describe the supplied reference in 4-6 sentences, focusing on: "
        "(a) overall composition + camera angle, (b) art style / palette / lighting, "
        "(c) main subjects + their poses/actions, (d) background environment. "
        "End with one sentence that distills the visual mood in keywords."
    )
    user_text = "Describe the visual of this image."
    if hint:
        user_text += f" Pay extra attention to: {hint}"

    body = json.dumps({
        "model": VISION_MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": image_field, "detail": "low"}},
            {"type": "text", "text": f"{sys_prompt}\n\n{user_text}"},
        ]}],
        "max_tokens": 320,
    }).encode()
    req = urllib.request.Request(
        VISION_BASE, data=body, method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {ARK_API_KEY}"},
    )
    print("[describe] calling vision...")
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[describe] WARN: {e}")
        return ""


def t2i(prompt: str, out_path: Path, aspect: str = "16:9", retries: int = 3) -> Path:
    """Plain text-to-image fallback."""
    if not ARK_API_KEY:
        sys.exit("[fatal] ARK_API_KEY not set")
    size = _resolve_size(aspect)
    payload = {
        "model": ARK_MODEL,
        "prompt": prompt,
        "size": size,
        "response_format": "url",
        "watermark": False,
    }
    headers = {"Authorization": f"Bearer {ARK_API_KEY}",
               "Content-Type": "application/json"}
    print(f"[t2i] model={ARK_MODEL}  size={size}")
    print(f"[t2i] prompt={prompt[:120]}{'...' if len(prompt) > 120 else ''}")

    last_err = None
    for attempt in range(1, retries + 1):
        print(f"  [..] attempt {attempt}/{retries}", end="", flush=True)
        start = time.time()
        status, body = _post_json(ARK_BASE, payload, headers, timeout=300)
        elapsed = time.time() - start
        print(f"  ({elapsed:.1f}s, status={status})")
        if status == 200:
            try:
                data = json.loads(body)
                items = data.get("data") or []
                image_url = items[0].get("url") if items else None
                if image_url:
                    return _download_to(image_url, out_path)
            except Exception as e:
                last_err = f"parse error: {e}"
        elif status == 429:
            wait = 60 * attempt
            print(f"  [RATELIMIT] sleep {wait}s"); time.sleep(wait); continue
        last_err = f"HTTP {status}: {body[:200]}"
        time.sleep(5 * attempt)

    sys.exit(f"[fatal] t2i failed: {last_err}")


def describe_then_t2i(ref: str, prompt: str, out_path: Path,
                      aspect: str = "16:9", retries: int = 3) -> Path:
    """Vision describes ref → describe + user prompt are merged → t2i."""
    desc = vision_describe(ref, hint=prompt[:80])
    if desc:
        print(f"[describe] got {len(desc)} chars")
        merged = (
            f"Reference visual described as: {desc}\n\n"
            f"Now create a NEW illustration that follows the user's intent: {prompt}\n"
            f"Keep the reference's overall composition, palette, and mood, "
            f"but apply the new instruction faithfully."
        )
    else:
        merged = prompt
    return t2i(merged, out_path, aspect=aspect, retries=retries)


# ---------------------------------------------------------------------------
# REMIX combo
# ---------------------------------------------------------------------------

def remix(image_paths: list[str], prompt: str, out_path: Path,
          layout: str = "grid", aspect: str = "16:9",
          strength: float = 0.55) -> Path:
    """Collage refs → I2I (with describe-then-t2i fallback)."""
    tmp = out_path.with_name(out_path.stem + "_collage.jpg")
    collage(image_paths, tmp, layout=layout, gap=10)
    return i2i(str(tmp), prompt, out_path, aspect=aspect, strength=strength)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Image remix toolbox — collage + i2i + describe-then-t2i + remix combo")
    sub = p.add_subparsers(dest="cmd", required=True)

    # collage
    pc = sub.add_parser("collage", help="PIL multi-image stitching, no API")
    pc.add_argument("images", nargs="+", help="2+ image paths")
    pc.add_argument("--layout", default="grid",
                    choices=list(LAYOUTS.keys()), help="layout name")
    pc.add_argument("--gap", type=int, default=8, help="gap pixels between cells")
    pc.add_argument("--bg", default="#ffffff", help="background color")
    pc.add_argument("--cell-max", type=int, default=1024,
                    help="max longest edge per cell (default 1024)")
    pc.add_argument("-o", "--out", required=True, help="output image path")

    # i2i
    pi = sub.add_parser("i2i", help="Seedream image-to-image")
    pi.add_argument("ref", help="reference image path or URL")
    pi.add_argument("--prompt", required=True, help="text guidance")
    pi.add_argument("--aspect", default="16:9",
                    choices=list(ASPECT_TO_SIZE_1K.keys()) + ["WxH"],
                    help="output aspect (or WxH like 1920x1080)")
    pi.add_argument("--strength", type=float, default=0.55,
                    help="how much to deviate from ref (0..1, default 0.55)")
    pi.add_argument("--no-fallback", action="store_true",
                    help="disable describe-then-t2i auto fallback on i2i failure")
    pi.add_argument("-o", "--out", required=True)

    # describe-then-t2i
    pd = sub.add_parser("describe-then-t2i",
                        help="Vision-describe ref + apply user prompt + Seedream t2i")
    pd.add_argument("ref")
    pd.add_argument("--prompt", required=True)
    pd.add_argument("--aspect", default="16:9")
    pd.add_argument("-o", "--out", required=True)

    # plain t2i (handy for one-offs)
    pt = sub.add_parser("t2i", help="plain Seedream text-to-image (handy one-off)")
    pt.add_argument("--prompt", required=True)
    pt.add_argument("--aspect", default="16:9")
    pt.add_argument("-o", "--out", required=True)

    # remix combo
    pr = sub.add_parser("remix",
                        help="collage N references → i2i restyle (with t2i fallback)")
    pr.add_argument("images", nargs="+")
    pr.add_argument("--prompt", required=True)
    pr.add_argument("--layout", default="grid", choices=list(LAYOUTS.keys()))
    pr.add_argument("--aspect", default="21:9")
    pr.add_argument("--strength", type=float, default=0.55)
    pr.add_argument("-o", "--out", required=True)

    return p


def main():
    parser = _build_parser()
    args = parser.parse_args()
    out_path = Path(args.out).expanduser().resolve()

    if args.cmd == "collage":
        collage(args.images, out_path, layout=args.layout, gap=args.gap,
                bg=args.bg, cell_max=args.cell_max)
    elif args.cmd == "i2i":
        i2i(args.ref, args.prompt, out_path, aspect=args.aspect,
            strength=args.strength, allow_fallback=not args.no_fallback)
    elif args.cmd == "describe-then-t2i":
        describe_then_t2i(args.ref, args.prompt, out_path, aspect=args.aspect)
    elif args.cmd == "t2i":
        t2i(args.prompt, out_path, aspect=args.aspect)
    elif args.cmd == "remix":
        remix(args.images, args.prompt, out_path, layout=args.layout,
              aspect=args.aspect, strength=args.strength)


if __name__ == "__main__":
    main()
