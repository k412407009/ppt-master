"""Extract a PPT-ready color palette from one or more reference images.

Usage:
    python3 palette_from_image.py <image_or_dir> [<image_or_dir> ...] \
        [--k 6] [--out palette.json] [--ignore-near-white 0.95] [--ignore-near-black 0.08]

Output: palette.json with primary / accents / neutrals slotted by role,
suitable to be read by PPT Master during design spec generation.

Design notes:
- Pure Pillow + numpy; no scikit-learn dependency to keep install footprint small.
- k-means initialized with k-means++ for stable results across runs (fixed seed).
- We operate in Lab-ish space (just L* derived from RGB luma) only for role sorting,
  clustering itself runs in RGB which is good enough for palette extraction from
  already-curated reference images.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image

SUPPORTED_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
RNG_SEED = 42


@dataclass
class Swatch:
    hex: str
    rgb: tuple[int, int, int]
    weight: float
    role: str


def iter_image_paths(inputs: Iterable[str]) -> list[Path]:
    out: list[Path] = []
    for raw in inputs:
        p = Path(raw).expanduser().resolve()
        if p.is_dir():
            out.extend(
                sorted(c for c in p.rglob("*") if c.suffix.lower() in SUPPORTED_EXT)
            )
        elif p.is_file() and p.suffix.lower() in SUPPORTED_EXT:
            out.append(p)
    return out


def load_pixels(paths: list[Path], max_side: int = 400) -> np.ndarray:
    """Load pixels from all images, downscale each to max_side for speed."""
    buckets: list[np.ndarray] = []
    for p in paths:
        try:
            img = Image.open(p).convert("RGB")
        except Exception as e:
            print(f"[warn] skip {p.name}: {e}", file=sys.stderr)
            continue
        img.thumbnail((max_side, max_side))
        buckets.append(np.asarray(img, dtype=np.float32).reshape(-1, 3))
    if not buckets:
        raise SystemExit("no readable images")
    return np.concatenate(buckets, axis=0)


def filter_extremes(
    pixels: np.ndarray, near_white: float, near_black: float
) -> np.ndarray:
    """Drop near-white and near-black pixels — they drown out real brand colors."""
    luma = (0.2126 * pixels[:, 0] + 0.7152 * pixels[:, 1] + 0.0722 * pixels[:, 2]) / 255.0
    keep = (luma > near_black) & (luma < near_white)
    return pixels[keep]


def kmeans_pp(pixels: np.ndarray, k: int, iters: int = 20) -> tuple[np.ndarray, np.ndarray]:
    """Minimal k-means with k-means++ init. Returns (centers, labels)."""
    rng = np.random.default_rng(RNG_SEED)
    n = pixels.shape[0]

    first = rng.integers(0, n)
    centers = [pixels[first]]
    closest_sq = np.sum((pixels - centers[0]) ** 2, axis=1)
    for _ in range(k - 1):
        probs = closest_sq / closest_sq.sum()
        idx = rng.choice(n, p=probs)
        centers.append(pixels[idx])
        new_sq = np.sum((pixels - centers[-1]) ** 2, axis=1)
        closest_sq = np.minimum(closest_sq, new_sq)
    centers_arr = np.stack(centers)

    for _ in range(iters):
        d2 = ((pixels[:, None, :] - centers_arr[None, :, :]) ** 2).sum(axis=2)
        labels = d2.argmin(axis=1)
        new_centers = np.stack(
            [
                pixels[labels == i].mean(axis=0) if np.any(labels == i) else centers_arr[i]
                for i in range(k)
            ]
        )
        if np.allclose(new_centers, centers_arr, atol=0.5):
            centers_arr = new_centers
            break
        centers_arr = new_centers

    d2 = ((pixels[:, None, :] - centers_arr[None, :, :]) ** 2).sum(axis=2)
    labels = d2.argmin(axis=1)
    return centers_arr, labels


def rgb_to_hex(rgb: np.ndarray) -> str:
    r, g, b = [int(round(max(0, min(255, v)))) for v in rgb]
    return f"#{r:02X}{g:02X}{b:02X}"


def assign_roles(centers: np.ndarray, weights: np.ndarray) -> list[Swatch]:
    """Slot cluster centers into PPT-friendly roles:

    - background: lightest, reasonably desaturated (or the single lightest)
    - text: darkest
    - primary: highest-weight colorful cluster
    - accent_1 / accent_2: next two colorful clusters by weight
    - neutrals: remaining
    """
    luma = (0.2126 * centers[:, 0] + 0.7152 * centers[:, 1] + 0.0722 * centers[:, 2])
    maxc = centers.max(axis=1)
    minc = centers.min(axis=1)
    saturation = np.where(maxc > 0, (maxc - minc) / np.maximum(maxc, 1e-6), 0.0)

    order = np.argsort(-weights)

    background_idx = int(np.argmax(luma))
    text_idx = int(np.argmin(luma))

    colorful_order = [
        i for i in order if i not in (background_idx, text_idx) and saturation[i] > 0.15
    ]
    neutral_order = [
        i for i in order if i not in (background_idx, text_idx) and i not in colorful_order
    ]

    roles: dict[int, str] = {background_idx: "background", text_idx: "text"}
    if colorful_order:
        roles[colorful_order[0]] = "primary"
    for rank, i in enumerate(colorful_order[1:], start=1):
        roles[i] = f"accent_{rank}"
    for rank, i in enumerate(neutral_order, start=1):
        roles[i] = f"neutral_{rank}"

    swatches: list[Swatch] = []
    for i in range(len(centers)):
        swatches.append(
            Swatch(
                hex=rgb_to_hex(centers[i]),
                rgb=tuple(int(round(v)) for v in centers[i]),
                weight=float(weights[i]),
                role=roles.get(i, f"misc_{i}"),
            )
        )
    swatches.sort(key=lambda s: (-s.weight,))
    return swatches


def build_palette(
    image_paths: list[Path],
    k: int,
    near_white: float,
    near_black: float,
) -> dict:
    pixels = load_pixels(image_paths)
    pixels = filter_extremes(pixels, near_white=near_white, near_black=near_black)
    if pixels.shape[0] < k:
        raise SystemExit(f"too few informative pixels ({pixels.shape[0]}) for k={k}")

    if pixels.shape[0] > 80_000:
        rng = np.random.default_rng(RNG_SEED)
        pixels = pixels[rng.choice(pixels.shape[0], 80_000, replace=False)]

    centers, labels = kmeans_pp(pixels, k=k)
    counts = np.bincount(labels, minlength=k).astype(np.float64)
    weights = counts / counts.sum()

    swatches = assign_roles(centers, weights)
    return {
        "source": {
            "type": "image",
            "files": [str(p) for p in image_paths],
            "pixel_count_sampled": int(pixels.shape[0]),
        },
        "swatches": [asdict(s) for s in swatches],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inputs", nargs="+", help="image files or directories")
    ap.add_argument("--k", type=int, default=6, help="number of colors (default 6)")
    ap.add_argument(
        "--out",
        default="palette.json",
        help="output path (default ./palette.json)",
    )
    ap.add_argument(
        "--ignore-near-white",
        type=float,
        default=0.95,
        help="drop pixels brighter than this (0-1 luma); default 0.95",
    )
    ap.add_argument(
        "--ignore-near-black",
        type=float,
        default=0.08,
        help="drop pixels darker than this (0-1 luma); default 0.08",
    )
    args = ap.parse_args()

    paths = iter_image_paths(args.inputs)
    if not paths:
        print("no images found in inputs", file=sys.stderr)
        return 2

    palette = build_palette(
        paths,
        k=args.k,
        near_white=args.ignore_near_white,
        near_black=args.ignore_near_black,
    )
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(palette, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote {out_path}")
    for s in palette["swatches"]:
        print(f"  {s['role']:<12} {s['hex']}  weight={s['weight']:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
