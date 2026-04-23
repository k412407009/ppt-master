#!/usr/bin/env python3
"""三仓本地栈体检脚本.

目标:
1. 检查三仓是否按推荐方式放在同级目录
2. 检查 `.env` / API key / 视频依赖是否就绪
3. 给第一次上手的同事一个明确的下一步
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent


def _load_env(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            data[key] = value
    return data


def _merged_env() -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in (
        ROOT / ".env",
        WORKSPACE / "game-asset-collector" / ".env",
        WORKSPACE / "game-review" / ".env",
    ):
        merged.update(_load_env(path))
    merged.update(os.environ)
    return merged


def _find_env(env: dict[str, str], name: str) -> tuple[str, str | None]:
    direct = env.get(name, "").strip()
    if direct:
        return direct, name
    target = name.lower()
    for key, value in env.items():
        value = value.strip()
        if value and key.lower() == target:
            return value, key
    return "", None


def _status_line(status: str, label: str, detail: str) -> None:
    print(f"[{status}] {label}: {detail}")


def _repo_status(path: Path) -> tuple[str, str]:
    if path.exists():
        return "OK", str(path)
    return "WARN", f"未找到 {path.name}，三仓联动会缺模块"


def _find_recommended_python() -> tuple[str, str] | None:
    candidates = [
        "/opt/homebrew/bin/python3",
        "python3.14",
        "python3.13",
        "python3.12",
        "python3.11",
        "python3.10",
    ]
    for candidate in candidates:
        path = candidate if candidate.startswith("/") else shutil.which(candidate)
        if not path:
            continue
        try:
            out = subprocess.check_output(
                [path, "-c", "import sys; print(sys.version.split()[0])"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except Exception:
            continue
        parts = tuple(int(x) for x in out.split(".")[:2])
        if parts >= (3, 10):
            return path, out
    return None


def main() -> int:
    env = _merged_env()
    warnings: list[str] = []
    blockers: list[str] = []

    print("== game-ppt-master stack doctor ==")
    _status_line("OK", "repo", str(ROOT))
    _status_line("OK", "workspace", str(WORKSPACE))

    for name in ("game-asset-collector", "game-review"):
        status, detail = _repo_status(WORKSPACE / name)
        _status_line(status, name, detail)
        if status != "OK":
            warnings.append(f"未找到同级仓库：{name}")

    version = sys.version.split()[0]
    if sys.version_info >= (3, 10):
        _status_line("OK", "python", version)
    else:
        _status_line("MISS", "python", f"{version}（需要 >= 3.10）")
        blockers.append("Python 版本低于 3.10")

    env_path = ROOT / ".env"
    if env_path.exists():
        _status_line("OK", ".env", str(env_path))
    else:
        _status_line("WARN", ".env", "主仓未找到 .env，图片后端可能未配置")
        warnings.append("主仓未找到 .env")

    image_backend = env.get("IMAGE_BACKEND", "").strip()
    backend_keys = {
        "gemini": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "qwen": "QWEN_API_KEY",
        "zhipu": "ZHIPU_API_KEY",
        "volcengine": "VOLCENGINE_API_KEY",
        "stability": "STABILITY_API_KEY",
        "bfl": "BFL_API_KEY",
        "ideogram": "IDEOGRAM_API_KEY",
        "siliconflow": "SILICONFLOW_API_KEY",
        "fal": "FAL_API_KEY",
        "replicate": "REPLICATE_API_TOKEN",
    }
    if image_backend:
        _status_line("OK", "IMAGE_BACKEND", image_backend)
        key_name = backend_keys.get(image_backend)
        if key_name and env.get(key_name):
            _status_line("OK", key_name, "已配置")
        elif key_name:
            _status_line("WARN", key_name, f"IMAGE_BACKEND={image_backend}，但未找到对应 key")
            warnings.append(f"缺少图片后端 key：{key_name}")
    else:
        _status_line("WARN", "IMAGE_BACKEND", "未配置；做纯文稿 PPT 不影响，AI 生图会不可用")
        warnings.append("未配置 IMAGE_BACKEND")

    for key, label in (
        ("TAVILY_API_KEY", "网页抓取兜底"),
        ("ARK_API_KEY", "视觉标签/中文描述"),
        ("COMPASS_API_KEY", "评审模型"),
    ):
        value, source = _find_env(env, key)
        if value:
            detail = f"已配置（{label}）"
            if source and source != key:
                detail += f"；当前通过 `{source}` 读取，建议以后统一写成 `{key}`"
            _status_line("OK", key, detail)
        else:
            _status_line("WARN", key, f"未配置（{label}会降级或不可用）")
            warnings.append(f"未配置 {key}")

    for cmd, label in (("yt-dlp", "视频下载"), ("ffmpeg", "抽帧")):
        path = shutil.which(cmd)
        if path:
            _status_line("OK", cmd, f"{path}（{label}可用）")
        else:
            _status_line("WARN", cmd, f"未找到，素材采集里的 {label}会不可用")
            warnings.append(f"未找到 {cmd}")

    print("\n总结:")
    if blockers:
        print(f"- 阻塞项 {len(blockers)} 个：")
        for item in blockers:
            print(f"  - {item}")
    else:
        print("- 没有阻塞项。")

    if warnings:
        print(f"- 提醒 {len(warnings)} 个：")
        for item in warnings:
            print(f"  - {item}")
    else:
        print("- 三仓主链路已基本就绪。")

    print("\n推荐下一步:")
    print("- 主仓体检：python3 scripts/stack_doctor.py")
    print("- 采集器体检：python3 ../game-asset-collector/scripts/fetch_game_assets.py --doctor")
    print("- 评审项目体检：cd ../game-review && python3 -m game_review.cli doctor <project_dir>")
    if blockers:
        recommended = _find_recommended_python()
        if recommended is not None:
            path, version = recommended
            print(f"- 如果默认 python3 版本过低，建议改用：{path} （{version}）")
    return 0 if not blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
