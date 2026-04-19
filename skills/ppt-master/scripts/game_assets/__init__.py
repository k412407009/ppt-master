"""Game asset collection pipeline for ppt-master.

Originated from `丁开心的游戏观察/sources/fetch_game_assets.py` and
`gen_images.py`, ported to ppt-master skill with project-aware paths and
unified .env reading.

Public modules:
- fetch_game_assets: store screenshots + video frame extraction + AI labeling
- image_remix: AI image-to-image + multi-image collage (Seedream + PIL)
"""
