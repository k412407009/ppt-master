# `scripts/game_assets/` — Game Asset Collection Toolbox

Auto-collects game prototype reference visuals for PPT projects.

> Distilled from `丁开心的游戏观察/sources/fetch_game_assets.py` and
> `gen_images.py`. Re-organized as a project-aware sub-pipeline of `ppt-master`,
> driven by **Step 4.5 Game Asset Collection** in `SKILL.md`.

## Why this exists

PPT Master runs in a strict no-image-reading sandbox: the agent never opens
`.jpg` / `.png` files directly. To put real game prototype visuals on slides
the agent needs an external "eye" that fetches images, classifies them, and
writes a paste-ready Image Resource List into `design_spec.md` §VIII.

Three sourcing strategies are supported, in priority order:

1. **Store screenshots** (App Store + Google Play + Steam, with Tavily
   Extract as fallback for screenshot-less iTunes responses).
2. **Gameplay video frame extraction** (yt-dlp pulls YouTube + Bilibili
   gameplay clips, ffmpeg extracts frames in 3 modes, pHash dedup).
3. **AI image-to-image / collage** (when no perfect prototype exists,
   take the closest reference + Seedream i2i, or stitch several refs and
   restyle the composite).

Steps 1 and 2 cover the user request "从商店或 DLC 抓取" and "寻找游戏视频
并进行抽帧"; step 3 covers "找最贴近的原型进行图生图，或者将几张图进行拼接".

## Files

| File | Purpose |
|------|---------|
| `fetch_game_assets.py` | P0 store screenshots + P1 video frame extraction + P1+ AI labeling + P2 emit Image Resource List |
| `image_remix.py` | `collage` (PIL stitching) + `i2i` (Seedream image-to-image) + `describe-then-t2i` fallback + `remix` combo |
| `__init__.py` | Marks the package |

## Dependencies

| Need | Install | When required |
|------|---------|---------------|
| Pillow | `pip install Pillow` | always (already in `requirements.txt`) |
| google-play-scraper | `pip install google-play-scraper` | for the Google Play branch (auto-falls back to Tavily Extract if missing) |
| yt-dlp | `pip install yt-dlp` or `winget install yt-dlp` | for gameplay video search/download |
| ffmpeg | `winget install ffmpeg` / `brew install ffmpeg` / `apt install ffmpeg` | for frame extraction |
| Tavily key | `TAVILY_API_KEY` env var or in `.env` | for store-page screenshot fallback (optional) |
| ARK key | `ARK_API_KEY` or `VOLCENGINE_API_KEY` env var or in `.env` | for AI labeling + i2i + describe |

## Quickstart — project-aware mode (recommended for PPT projects)

Inside an existing PPT Master project:

```bash
# 1) Pull store screenshots + 2 gameplay videos + AI labels for one game
python skills/ppt-master/scripts/game_assets/fetch_game_assets.py "DREDGE" \
    --project projects/H_深海守望者_xxx \
    --steam-id 1562430 --max-videos 2 --label

# 2) (optional) Re-run labeling only on already-collected frames
python skills/ppt-master/scripts/game_assets/fetch_game_assets.py "DREDGE" \
    --project projects/H_深海守望者_xxx --label-only

# 3) (optional) Just regenerate the Image Resource List md
python skills/ppt-master/scripts/game_assets/fetch_game_assets.py "DREDGE" \
    --project projects/H_深海守望者_xxx --emit-list-only
```

Output layout (relative to project):

```
images/
├── _game_assets/<game>/
│   ├── store/
│   │   ├── appstore/screenshot_*.jpg + icon.png
│   │   ├── googleplay/screenshot_*.jpg + icon.png
│   │   └── steam/screenshot_*.jpg + header.jpg + trailer_*.mp4 (+ optional)
│   ├── gameplay/
│   │   ├── frames/<video_slug>/frame_*.jpg
│   │   └── labels.json     (rel-path → label, 12-class taxonomy)
│   └── metadata.json
└── _game_assets_meta/
    └── <game>.image_resource_list.md   (paste into design_spec.md §VIII)
```

## Quickstart — image_remix.py

```bash
# COLLAGE: stitch 4 refs into a 2x2 composite (no API)
python skills/ppt-master/scripts/game_assets/image_remix.py collage \
    a.jpg b.jpg c.jpg d.jpg --layout 2x2 --gap 12 -o composite.jpg

# I2I: take a single reference + restyle with Seedream
python skills/ppt-master/scripts/game_assets/image_remix.py i2i \
    ref.jpg \
    --prompt "Pixar cute fox shopkeeper running TCG card store, soft pastel" \
    --aspect 16:9 -o variant.jpg

# DESCRIBE+T2I: when i2i model isn't available
python skills/ppt-master/scripts/game_assets/image_remix.py describe-then-t2i \
    ref.jpg \
    --prompt "Studio Ghibli watercolor, oceanic mood" \
    --aspect 21:9 -o variant.jpg

# REMIX combo: collage + i2i in one call
python skills/ppt-master/scripts/game_assets/image_remix.py remix \
    ref1.jpg ref2.jpg ref3.jpg \
    --prompt "blend into a cohesive PPT hero illustration" \
    --layout hstrip --aspect 21:9 -o hero.jpg
```

## Frame extraction modes (`fetch_game_assets.py` gameplay)

| Mode | Trigger | Behaviour | When to use |
|------|---------|-----------|-------------|
| sparse + dedup (default) | (no flag) | 1 frame / N seconds, then pHash dedup (Hamming < 8) | most balanced |
| scene-detect + dedup | `--scene` | ffmpeg `select=gt(scene,0.3)` + pHash dedup | content-driven, good for cutscene-rich videos |
| scene-detect (legacy) | `--no-smart` | scene-detect, no dedup | drop-in legacy mode |

`--frame-interval N` controls sparse-mode interval (default 5).
`--scene-threshold F` controls scene-detect sensitivity (default 0.3).

## AI labeling (`--label`)

12-class taxonomy:
`ui-menu / battle / shop-gacha / main-city / cutscene / loading /
character / map-world / tutorial / social / ad-creative / other`

Default smart-quota stops as soon as enough variety is collected:
`battle 3 + main-city 2 + character 2 + shop-gacha 2 + ui-menu 2 +
map-world 1 + cutscene 1 + tutorial 1 + other 1 = 15 frames total.`

Override per-class with e.g. `--battle 5 --main-city 4 --shop-gacha 3`.

Vision model: `doubao-seed-1-6-vision-250815` via ARK Beijing endpoint.
Each call uses a 256×256 thumbnail with `detail: low` to minimize tokens.

## I2I fallback chain

`image_remix.py i2i` is built defensively:

1. Try Seedream API with `image` field (true image-to-image).
2. If HTTP 400 (model rejects the field), automatically:
   - Send the reference to Doubao Vision → get a 4-6 sentence description.
   - Merge description + user prompt → call plain text-to-image.
3. If 429 (rate-limit), exponential backoff up to 3 retries.

Pass `--no-fallback` to disable step 2 and hard-fail instead.

## Failure modes

- `ffmpeg not on PATH` → install via `winget install ffmpeg` (Windows) or
  `brew install ffmpeg` (mac) / `apt install ffmpeg` (linux).
- `yt-dlp not installed` → `pip install yt-dlp` (Python pkg) or
  `winget install yt-dlp` (binary).
- `ARK_API_KEY not set` → labeling silently degrades to heuristic-only;
  i2i / t2i / describe will hard-fail with a clear message.
- `google_play_scraper timeout` → automatically falls back to Tavily Extract.
- `Tavily 401/429` → silently skips that fallback path.

## See also

- `references/game-asset-collector.md` — full skill specification.
- `references/strategist.md` §VIII — Image Usage Confirmation now includes
  option **D) Game asset auto-collection** that triggers this pipeline.
- `references/image-generator.md` — separate AI text-to-image pipeline used
  for purely synthetic illustrations (cover art, conceptual diagrams).
