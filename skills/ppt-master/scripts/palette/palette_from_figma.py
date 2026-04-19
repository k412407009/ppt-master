"""Extract a PPT-ready palette from a Figma file via the Figma REST API.

Auth: reads token from environment variable FIGMA_TOKEN (loaded from .env if present).
      Never hard-code the token.

Usage:
    python3 palette_from_figma.py <figma_url_or_file_key> [--out palette.json]

It tries two strategies in order:
  1) Read published Color Styles of the file (/v1/files/{key}/styles + node lookup).
  2) Fall back to rendering a thumbnail of each top-level frame and delegating to
     palette_from_image.build_palette so the output schema is identical.

Why two strategies:
  - Well-organized design files have named Color Styles → richer, labelled output.
  - Most community/pitch-deck files don't publish styles → we extract from pixels.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from palette_from_image import build_palette as build_palette_from_images  # noqa: E402


FIGMA_API = "https://api.figma.com/v1"


def load_env_file(env_path: Path) -> None:
    """Minimal .env loader; does not depend on python-dotenv."""
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def resolve_token() -> str:
    for candidate in [Path.cwd() / ".env", HERE.parents[3] / ".env"]:
        try:
            load_env_file(candidate)
        except Exception:
            pass
    token = os.environ.get("FIGMA_TOKEN") or os.environ.get("FIGMA_API_TOKEN")
    if not token:
        raise SystemExit(
            "FIGMA_TOKEN not found. Put `FIGMA_TOKEN=figd_...` into .env "
            "(in the ppt-master repo root) or export it as an env var."
        )
    return token


def parse_file_key(arg: str) -> str:
    if arg.startswith("http://") or arg.startswith("https://"):
        parsed = urlparse(arg)
        m = re.search(r"/(?:file|design|board)/([A-Za-z0-9]+)", parsed.path)
        if not m:
            raise SystemExit(f"cannot parse Figma file key from URL: {arg}")
        return m.group(1)
    return arg


def figma_get(path: str, token: str, params: dict | None = None) -> dict:
    r = requests.get(
        f"{FIGMA_API}{path}",
        headers={"X-Figma-Token": token},
        params=params,
        timeout=30,
    )
    if r.status_code == 403:
        raise SystemExit(
            "403 Forbidden from Figma. The token probably lacks the right scope. "
            "Minimum required: file_content:read + file_metadata:read. "
            "Regenerate the token with these scopes ticked."
        )
    r.raise_for_status()
    return r.json()


def extract_color_styles(file_key: str, token: str) -> list[dict] | None:
    """Returns a list of swatches from published FILL styles, or None if none found."""
    styles_resp = figma_get(f"/files/{file_key}/styles", token)
    meta = styles_resp.get("meta", {}).get("styles", [])
    fill_styles = [s for s in meta if s.get("style_type") == "FILL"]
    if not fill_styles:
        return None

    node_ids = [s["node_id"] for s in fill_styles]
    CHUNK = 50
    swatches: list[dict] = []
    for i in range(0, len(node_ids), CHUNK):
        chunk = node_ids[i : i + CHUNK]
        nodes_resp = figma_get(
            f"/files/{file_key}/nodes",
            token,
            params={"ids": ",".join(chunk)},
        )
        nodes = nodes_resp.get("nodes", {})
        for style in fill_styles:
            nid = style["node_id"]
            entry = nodes.get(nid)
            if not entry:
                continue
            doc = entry.get("document", {})
            fills = doc.get("fills", [])
            color_fills = [f for f in fills if f.get("type") == "SOLID" and f.get("color")]
            if not color_fills:
                continue
            c = color_fills[0]["color"]
            opacity = color_fills[0].get("opacity", 1.0) * c.get("a", 1.0)
            r = int(round(c.get("r", 0) * 255))
            g = int(round(c.get("g", 0) * 255))
            b = int(round(c.get("b", 0) * 255))
            swatches.append(
                {
                    "hex": f"#{r:02X}{g:02X}{b:02X}",
                    "rgb": [r, g, b],
                    "opacity": round(opacity, 3),
                    "name": style.get("name", ""),
                    "description": style.get("description", ""),
                    "role": _role_from_name(style.get("name", "")),
                }
            )
    return swatches or None


def _role_from_name(name: str) -> str:
    low = name.lower()
    if any(w in low for w in ("primary", "brand", "main")):
        return "primary"
    if "accent" in low:
        return "accent"
    if any(w in low for w in ("bg", "background", "surface")):
        return "background"
    if any(w in low for w in ("text", "ink", "foreground")):
        return "text"
    if any(w in low for w in ("neutral", "gray", "grey", "border", "muted")):
        return "neutral"
    return "misc"


def render_thumbnails(file_key: str, token: str, out_dir: Path) -> list[Path]:
    """Render top-level FRAME thumbnails as PNG to disk and return their paths."""
    file_resp = figma_get(f"/files/{file_key}", token, params={"depth": 2})
    canvases = file_resp.get("document", {}).get("children", [])
    frame_ids: list[str] = []
    for canvas in canvases:
        for child in canvas.get("children", []):
            if child.get("type") in ("FRAME", "COMPONENT", "COMPONENT_SET"):
                frame_ids.append(child["id"])
    if not frame_ids:
        raise SystemExit("no top-level frames found to render")

    frame_ids = frame_ids[:12]
    images_resp = figma_get(
        f"/images/{file_key}",
        token,
        params={"ids": ",".join(frame_ids), "format": "png", "scale": 1},
    )
    urls = images_resp.get("images", {}) or {}

    out_dir.mkdir(parents=True, exist_ok=True)
    saved: list[Path] = []
    for fid, url in urls.items():
        if not url:
            continue
        try:
            img_bytes = requests.get(url, timeout=30).content
        except Exception as e:
            print(f"[warn] download failed for {fid}: {e}", file=sys.stderr)
            continue
        safe = fid.replace(":", "_")
        p = out_dir / f"frame_{safe}.png"
        p.write_bytes(img_bytes)
        saved.append(p)
    return saved


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", help="Figma file URL or file key")
    ap.add_argument("--out", default="palette.json")
    ap.add_argument(
        "--force-pixels",
        action="store_true",
        help="skip published-styles path; always render thumbnails and extract pixels",
    )
    args = ap.parse_args()

    token = resolve_token()
    file_key = parse_file_key(args.file)

    swatches = None if args.force_pixels else extract_color_styles(file_key, token)

    if swatches:
        palette = {
            "source": {"type": "figma_styles", "file_key": file_key},
            "swatches": swatches,
        }
    else:
        print("no published color styles; falling back to thumbnail pixel extraction")
        tmp_dir = Path(args.out).expanduser().resolve().parent / "_figma_thumbs"
        images = render_thumbnails(file_key, token, tmp_dir)
        if not images:
            raise SystemExit("no thumbnails rendered; cannot extract palette")
        palette = build_palette_from_images(
            images, k=6, near_white=0.95, near_black=0.08
        )
        palette["source"] = {
            "type": "figma_thumbnails",
            "file_key": file_key,
            "thumbnail_dir": str(tmp_dir),
            "thumbnail_count": len(images),
        }

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(palette, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out_path} ({len(palette['swatches'])} swatches)")
    for s in palette["swatches"][:10]:
        label = s.get("name") or s.get("role", "?")
        print(f"  {label:<20} {s['hex']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
