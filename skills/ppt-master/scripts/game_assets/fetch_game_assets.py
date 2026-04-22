#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compatibility wrapper for the shared game-asset-collector repo."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _find_shared_repo() -> Path | None:
    override = os.environ.get("GAME_ASSET_COLLECTOR_SCRIPT", "").strip()
    if override:
        path = Path(override).expanduser().resolve()
        return path.parents[1] if path.exists() else None

    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "game-asset-collector"
        if (candidate / "game_asset_collector" / "fetch_game_assets.py").exists():
            return candidate
    return None


def main() -> None:
    repo = _find_shared_repo()
    if repo is None:
        raise SystemExit(
            "shared collector not found; clone sibling `game-asset-collector` or set GAME_ASSET_COLLECTOR_SCRIPT"
        )

    legacy_default = Path(__file__).resolve().parent / "game_assets_library"
    os.environ.setdefault("GAME_ASSET_COLLECTOR_DEFAULT_OUT", str(legacy_default))

    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))

    from game_asset_collector.fetch_game_assets import main as shared_main

    shared_main()


if __name__ == "__main__":
    main()
