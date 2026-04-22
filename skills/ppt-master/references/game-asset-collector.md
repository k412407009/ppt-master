# Game Asset Collector — Step 4.5 specification

> Role definition for the new **Game Asset Collection** phase, inserted between
> Strategist (Step 4) and Image_Generator (Step 5) in `SKILL.md`. Triggered
> when Strategist's "Image Usage Confirmation" includes option **D) Game
> asset auto-collection**.

## Mission

Acquire **prototype reference visuals** for the games / DLC / source materials
discussed in the design spec, in priority order:

1. **Store screenshots** — App Store, Google Play, Steam (with Tavily Extract
   fallback for pages that hide screenshots from public APIs).
2. **Gameplay video frame extraction** — yt-dlp pulls YouTube + Bilibili
   clips, ffmpeg extracts frames, perceptual hashing dedups, Doubao Vision
   classifies frames into 12 scene categories.
3. **Closest-reference + AI image-to-image / collage** — when the design
   spec calls for an angle that none of the existing prototypes shows, pick
   the visually nearest references and either restyle one of them with
   Seedream i2i or stitch several together and restyle the composite.

The phase ends by writing an **Image Resource List** (Markdown table) that
the Strategist's `design_spec.md` §VIII can adopt verbatim.

## Inputs

- Confirmed `design_spec.md` (especially §VIII "Image Resource List" — drafts
  the slots that need filling).
- Game roster: extract from §I "Project Information" or §IX "Content Outline"
  the list of reference games / IPs / source documents to seed.
- For each game: optional Steam App ID, App Store ID, Google Play package
  name (sharply improves accuracy when known).

> App Store note: title search now uses a **strict candidate filter**. If the
> best hit is fuzzy, the collector skips App Store entirely instead of force-
> picking result #1. When you know the exact app, prefer `--appstore-id`.

## Decision tree (executed once per game)

```
                       ┌─────────────────────────────┐
   for each game →     │  Does design_spec list this │
                       │  game with specific scene   │  yes
                       │  needs (e.g. "shop-gacha    │  ──→  go to "Path A"
                       │  screen of game X")?        │
                       └─────────────────────────────┘
                                    │ no
                                    ▼
                       ┌─────────────────────────────┐
                       │  Are reusable assets        │
                       │  already cached locally?    │  yes
                       │  (check images/_game_assets │  ──→  skip P0+P1, only
                       │  /<game>/ from prior runs)  │       run P2 emit
                       └─────────────────────────────┘
                                    │ no
                                    ▼
                              run Path A
```

### Path A — store + gameplay collection

```bash
python ${SKILL_DIR}/scripts/game_assets/fetch_game_assets.py "<game name>" \
    --project <project_path> \
    --steam-id <id?>  --appstore-id <id?>  --gplay-id <pkg?> \
    --max-videos 2  --label
```

If auto-search finds the wrong clip, switch to manual video input:

```bash
python ${SKILL_DIR}/scripts/game_assets/fetch_game_assets.py "<game name>" \
    --project <project_path> \
    --video https://www.youtube.com/watch?v=<id> \
    --video <bilibili_BV_id?> \
    --label
```

This populates:

```
<project>/images/_game_assets/<sanitized_game>/
  ├── store/{appstore,googleplay,steam}/screenshot_*.jpg + icon.png
  ├── gameplay/frames/<video_slug>/frame_*.jpg  (≤ 15 after smart-quota)
  ├── gameplay/labels.json                       (12-class taxonomy)
  ├── gameplay/descriptions.json                 (Chinese one-line frame descriptions)
  └── metadata.json
<project>/images/_game_assets_meta/
  └── <sanitized_game>.image_resource_list.md   (paste-ready)
```

If a game has no recognizable presence on iTunes / Google Play / Steam (e.g.
mini-program titles, Chinese-only TapTap-only releases, internal R&D games),
Path A returns empty `stores` — fall through to Path B.

### Path B — gameplay video only (skip stores)

```bash
python ${SKILL_DIR}/scripts/game_assets/fetch_game_assets.py "<game name>" \
    --project <project_path> --gameplay-only --max-videos 3 --label
```

Useful for newer / regional / unreleased titles whose store APIs are
empty but YouTube / Bilibili gameplay walkthroughs exist.

### Path C — closest-reference i2i / collage

Triggered when:

- Path A and Path B return zero usable frames for a required scene, OR
- Strategist explicitly asks for a stylized hero illustration (e.g. "Pixar
  fox running a TCG store") that no real game ships.

The agent picks 1–4 closest existing references (from
`images/_game_assets/<game>/`, `_examples/`, or any user-supplied folder)
and chooses one of three sub-strategies:

| Sub-strategy | Tool | When |
|--------------|------|------|
| Single ref → restyle | `image_remix.py i2i ref.jpg --prompt ...` | one prototype is already 80% right, just need a re-skin |
| Multi-ref → composite then restyle | `image_remix.py remix r1.jpg r2.jpg ... --prompt ...` | want to fuse multiple games' aesthetics into one slide |
| Multi-ref → composite only | `image_remix.py collage r1.jpg r2.jpg ... --layout 2x2 -o out.jpg` | need a literal "competitor comparison" panel |

All three forms write a **single PNG/JPG** to wherever you point `-o`. They
do NOT update `image_resource_list.md` automatically — the agent must add
the new entry manually after Path C runs (treat it as user-provided).

## Outputs

1. Per-game asset directory under `<project>/images/_game_assets/<game>/`.
2. Per-game Image Resource List Markdown under
   `<project>/images/_game_assets_meta/<game>.image_resource_list.md`.
3. (Optional) `image_remix.py` outputs in `<project>/images/_remix/`
   (chosen by the agent, no required convention).

## Integration with `design_spec.md`

After all per-game runs finish, the agent merges all
`_game_assets_meta/*.image_resource_list.md` files into `design_spec.md`
§VIII, fills the **Purpose** column per slide, and confirms total slot
coverage matches §IX Content Outline.

If the design spec was already finalized, append the new resource list as a
sub-section "VIII.b Auto-collected references" rather than rewriting in
place.

## Quality gates

Before declaring the phase complete:

- [ ] Each game listed in §VIII or §IX has at least 1 reference frame OR a
      conscious "skip — no public material" note in the resource list.
- [ ] `labels.json` for each game contains at least the scene categories
      that the slides actually need (re-run with `--battle 5 --shop-gacha 4`
      etc. if defaults underfill).
- [ ] Any Path-C `image_remix.py` output is under 4 MB and aspect-matched
      to its slide's layout container (use `analyze_images.py` to verify
      after you finish — see `scripts/analyze_images.py`).

## Failure handling

| Symptom | Cause | Action |
|---------|-------|--------|
| `ffmpeg not found` | not on PATH | install via `winget install ffmpeg` (Win) / `brew install ffmpeg` (mac) |
| `yt-dlp returned 0 videos` | game has no English/Chinese gameplay on YouTube/B站 | retry with `--max-videos 5`; if still empty, fall through to Path C |
| `Tavily 429` | rate-limited | wait 60s, re-run with `--store-only` to retry just stores |
| `ARK_API_KEY missing` | env not loaded | put it in `${PPT_MASTER_ROOT}/.env`; this script auto-loads on startup |
| HTTP 400 on i2i | older Seedream model rejects `image` field | the script auto-falls back to describe-then-t2i; no action needed |
| HTTP 429 on Seedream | rate limit | exponential backoff 60s/120s/180s built-in |

## Permissions / etiquette

This pipeline only fetches **publicly accessible** materials:

- iTunes / Google Play / Steam Store APIs are official, public, no auth.
- yt-dlp only downloads videos the public can stream; downloads are deleted
  after frame extraction unless `--keep-video` is passed.
- Tavily Extract only crawls publicly indexed pages.
- All outputs are intended for **internal PPT use** (research-planner /
  development-producer audiences); do NOT redistribute frames or covers
  externally without rights clearance.

## Why we do not delegate this phase to a sub-agent

Same constraint that governs Step 6 SVG generation: the choice of which
games to seed, which scenes to prioritize, and which closest-reference to
restyle depends on the **full upstream conversation context** (source
document, design spec, slide outline). Hand-off to a sub-agent loses that
context. The phase is therefore executed by the main agent issuing
`fetch_game_assets.py` / `image_remix.py` calls in sequence.
