# Game PPT Master — AI generates natively editable PPTX for game-industry decks

[![Version](https://img.shields.io/badge/version-v2.3.0-blue.svg)](https://github.com/k412407009/game-ppt-master/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/k412407009/game-ppt-master.svg)](https://github.com/k412407009/game-ppt-master/stargazers)

English | [中文](./README_CN.md)

<p align="center">
  <a href="./docs/三仓协同架构_THREE_REPO_STACK.md"><strong>Three-Repo Stack</strong></a> ·
  <a href="./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md"><strong>Game Customization Notes</strong></a> ·
  <a href="./examples/"><strong>Examples</strong></a> ·
  <a href="./docs/faq.md"><strong>FAQ</strong></a> ·
  <a href="https://github.com/k412407009/game-ppt-master/issues"><strong>Issues</strong></a>
</p>

> **Repository positioning** — Game PPT Master is a public, game-focused derivative of upstream [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master). The base editable PPTX engine stays compatible with upstream, while this repo adds game-specific workflow, shared asset collection, and structured review handoff. See [Game Customization Notes](./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md).

---

Drop in a PDF, DOCX, URL, or Markdown — get back a **natively editable PowerPoint** with real shapes, real text boxes, and real charts. Then keep going into game-specific asset collection, review production, and final deck output.

> **How it works** — Game PPT Master is a workflow (a "skill") that works inside AI IDEs like Claude Code, Cursor, VS Code + Copilot, or Codebuddy. You chat with the AI — "make a game deck from this PDF" — and it follows the workflow to produce a real editable `.pptx` on your computer. No coding on your side; the IDE is just where the conversation happens.
>
> **What you'll do**: install Python, install an AI IDE, drop in your material. First-time setup is about 15 minutes. Each deck takes ~10–20 minutes of back-and-forth with the AI.

**[Why this engine?](./docs/why-ppt-master.md)**

There's no shortage of AI presentation tools — what's missing is one where the output is **actually usable as a real PowerPoint file**. I build presentations every day, but most tools export images or web screenshots: they look nice but you can't edit anything. Others produce bare-bones text boxes and bullet lists. And they all want a monthly subscription, upload your files to their servers, and lock you into their platform.

Game PPT Master is different:

- **Real PowerPoint** — if a file can't be opened and edited in PowerPoint, it shouldn't be called a PPT. Every element PPT Master outputs is directly clickable and editable
- **Game-industry workflow** — this repo adds collector handoff, game-review integration, and a repeatable game deck / review loop on top of the base PPT engine
- **Transparent, predictable cost** — the tool is free and open source; the only cost is your own AI editor, and you know exactly what you're paying. As low as **$0.08/deck** with VS Code Copilot
- **Data stays local** — your files shouldn't have to be uploaded to someone else's server just to make a presentation. Apart from AI model communication, the entire pipeline runs on your machine
- **No platform lock-in** — your workflow shouldn't be held hostage by any single company. Works with Claude Code, Cursor, VS Code Copilot, and more; supports Claude, GPT, Gemini, Kimi, and other models

**[See base-engine examples →](https://hugohe3.github.io/ppt-master/)** · [`examples/`](./examples/) — 15 projects, 229 pages

## Gallery

<table>
  <tr>
    <td align="center"><img src="docs/assets/screenshots/preview_magazine_garden.png" alt="Magazine style — Garden building guide" /><br/><sub><b>Magazine</b> — warm earthy tones, photo-rich layout</sub></td>
    <td align="center"><img src="docs/assets/screenshots/preview_academic_medical.png" alt="Academic style — Medical image segmentation research" /><br/><sub><b>Academic</b> — structured research format, data-driven</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/assets/screenshots/preview_dark_art_mv.png" alt="Dark art style — Music video analysis" /><br/><sub><b>Dark Art</b> — cinematic dark background, gallery aesthetic</sub></td>
    <td align="center"><img src="docs/assets/screenshots/preview_nature_wildlife.png" alt="Nature style — Wildlife wetland documentary" /><br/><sub><b>Nature Documentary</b> — immersive photography, minimal UI</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/assets/screenshots/preview_tech_claude_plans.png" alt="Tech style — Claude AI subscription plans" /><br/><sub><b>Tech / SaaS</b> — clean white cards, pricing table layout</sub></td>
    <td align="center"><img src="docs/assets/screenshots/preview_launch_xiaomi.png" alt="Product launch style — Xiaomi spring release" /><br/><sub><b>Product Launch</b> — high contrast, bold specs highlight</sub></td>
  </tr>
</table>

---

## Upstream Foundation

The native editable PPTX engine and the original `ppt-master` workflow were created by [Hugo He](https://github.com/hugohe3/ppt-master). That upstream work is still the technical foundation of this repository.

Game PPT Master is the game-industry adaptation layer on top of that foundation. This public repo focuses on:

- external game asset collection handoff
- structured game review production
- a three-repo local stack with `game-asset-collector` and `game-review`
- game-oriented project prompts and delivery flow

For the full delta from upstream, read [Game Customization Notes](./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md).

---

## Quick Start

### 1. Prerequisites

**You only need Python.** Everything else is installed via `pip install -r requirements.txt`.

| Dependency | Required? | What it does |
|------------|:---------:|--------------|
| [Python](https://www.python.org/downloads/) 3.10+ | ✅ **Yes** | Core runtime — the only thing you actually need to install |

> **TL;DR** — Install Python, run `pip install -r requirements.txt`, and you're ready to generate presentations.

<details open>
<summary><strong>Windows</strong> — see the dedicated step-by-step guide ⚠️</summary>

Windows requires a few extra steps (PATH setup, execution policy, etc.). We wrote a **step-by-step guide** specifically for Windows users:

**📖 [Windows Installation Guide](./docs/windows-installation.md)** — from zero to a working presentation in 10 minutes.

Quick version: download Python from [python.org](https://www.python.org/downloads/) → **check "Add to PATH"** during install → `pip install -r requirements.txt` → done.
</details>

<details>
<summary><strong>macOS / Linux</strong> — install and go</summary>

```bash
# macOS
brew install python
pip install -r requirements.txt

# Ubuntu / Debian
sudo apt install python3 python3-pip
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>Edge-case fallbacks</strong> — 99% of users don't need these</summary>

Two external tools exist as fallbacks for edge cases. **Most users will never need them** — install only if you hit one of the specific scenarios below.

| Fallback | Install only if… |
|----------|-----------------|
| [Node.js](https://nodejs.org/) 18+ | You need to import WeChat Official Account articles **and** `curl_cffi` (part of `requirements.txt`) has no prebuilt wheel for your Python + OS + CPU combination. In normal setups `web_to_md.py` handles WeChat directly through `curl_cffi`. |
| [Pandoc](https://pandoc.org/) | You need to convert legacy formats: `.doc`, `.odt`, `.rtf`, `.tex`, `.rst`, `.org`, or `.typ`. `.docx`, `.html`, `.epub`, `.ipynb` are handled natively by Python — no pandoc required. |

```bash
# macOS (only if the above conditions apply)
brew install node
brew install pandoc

# Ubuntu / Debian
sudo apt install nodejs npm
sudo apt install pandoc
```
</details>

### 2. Pick an AI Editor

| Tool | Rating | Notes |
|------|:------:|-------|
| **[Claude Code](https://claude.ai/)** | ⭐⭐⭐ | Best results — native Opus, largest context |
| [Cursor](https://cursor.sh/) / [VS Code + Copilot](https://code.visualstudio.com/) | ⭐⭐ | Good alternatives |
| Codebuddy IDE | ⭐⭐ | Best for Chinese models (Kimi 2.5, MiniMax 2.7) |

### 3. Set Up

**Option A — Download ZIP** (no Git required): click **Code → Download ZIP** on the [GitHub page](https://github.com/k412407009/game-ppt-master), then unzip.

**Option B — Git clone** (requires [Git](https://git-scm.com/downloads) installed):

```bash
git clone https://github.com/k412407009/game-ppt-master.git
cd game-ppt-master
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

To update later (Option B only): `python3 skills/ppt-master/scripts/update_repo.py`

### 4. Create

**Provide source materials (recommended):** Place your PDF, DOCX, images, or other files in the `projects/` directory, then tell the AI chat panel which files to use. The quickest way to get the path: right-click the file in your file manager or IDE sidebar → **Copy Path** (or **Copy Relative Path**) and paste it directly into the chat.

```
You: Please create a PPT from projects/q3-report/sources/report.pdf
```

**Paste content directly:** You can also paste text content straight into the chat window and the AI will generate a PPT from it.

```
You: Please turn the following into a PPT: [paste your content here...]
```

Either way, the AI will first confirm the design spec:

```
AI:  Sure. Let's confirm the design spec:
     [Template] B) Free design
     [Format]   PPT 16:9
     [Pages]    8-10 pages
     ...
```

The AI handles everything — content analysis, visual design, SVG generation, and PPTX export.

> **Output:** Two timestamped files are saved to `exports/` — a native-shapes `.pptx` (directly editable) and an `_svg.pptx` snapshot for visual reference. Requires Office 2016+.

> **AI lost context?** Ask it to read `skills/ppt-master/SKILL.md`.

> **Something went wrong?** Check the **[FAQ](./docs/faq.md)** — it covers model selection, layout issues, export problems, and more. Continuously updated from real user reports.

### 5. AI Image Generation (Optional)

```bash
cp .env.example .env    # then edit with your API key
```

```env
IMAGE_BACKEND=gemini                        # required — must be set explicitly
GEMINI_API_KEY=your-api-key
GEMINI_MODEL=gemini-3.1-flash-image-preview
```

Supported backends: `gemini` · `openai` · `qwen` · `zhipu` · `volcengine` · `stability` · `bfl` · `ideogram` · `siliconflow` · `fal` · `replicate`

Run `python3 skills/ppt-master/scripts/image_gen.py --list-backends` to see tiers. Environment variables override `.env`. Use provider-specific keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`, etc.) — global `IMAGE_API_KEY` is not supported.

> **Tip:** For best quality, generate images in [Gemini](https://gemini.google.com/) and select **Download full size**. Remove the watermark with `scripts/gemini_watermark_remover.py`.

### 6. Full Local Stack (3 Repos)

If you want the complete local workflow instead of the PPT-only path, clone these three sibling repositories under the same parent directory:

```text
<workspace>/
  game-ppt-master/        # main workflow + PPT generation
  game-asset-collector/   # store / video asset collection
  game-review/            # structured review report generation
```

Internal compatibility note:

- The public repo name is `game-ppt-master`
- The internal skill path remains `skills/ppt-master/...`
- Do not rename the internal `skills/ppt-master` directory unless you also update downstream scripts

Public repositories:

- [game-ppt-master](https://github.com/k412407009/game-ppt-master)
- [game-asset-collector](https://github.com/k412407009/game-asset-collector)
- [game-review](https://github.com/k412407009/game-review)

Recommended order:

1. Clone `game-ppt-master`
2. Clone `game-asset-collector`
3. Clone `game-review`

Then read the full stack guide:

- [Three-Repo Stack](./docs/三仓协同架构_THREE_REPO_STACK.md)
- [Ecosystem Manifest](./docs/生态清单_ECOSYSTEM_MANIFEST.json)

---

## Documentation

| | Document | Description |
|---|----------|-------------|
| 🆚 | [Why This Engine](./docs/why-ppt-master.md) | How the upstream PPT engine compares to Gamma, Copilot, and other AI tools |
| 🪟 | [Windows Installation](./docs/windows-installation.md) | Step-by-step setup guide for Windows users |
| 📖 | [SKILL.md](./skills/ppt-master/SKILL.md) | Core workflow and rules |
| 🎮 | [Game Customization Notes](./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md) | What changed from upstream `ppt-master`, what stayed compatible, and why this repo is named `game-ppt-master` |
| 🤝 | [Team Onboarding](./docs/同事接入指南_TEAM_ONBOARDING_GUIDE.md) | Shareable setup guide for colleagues: download links, API keys, local wiring, and first-run flow |
| 🧭 | [Three-Repo Stack](./docs/三仓协同架构_THREE_REPO_STACK.md) | End-to-end architecture, clone layout, model/API boundaries, and full workflow |
| 🧩 | [Ecosystem Manifest](./docs/生态清单_ECOSYSTEM_MANIFEST.json) | Machine-readable module manifest for `game-ppt-master` + `game-asset-collector` + `game-review` |
| 🎯 | [Game Review Closed Loop](./docs/游戏评审闭环_GAME_REVIEW_CLOSED_LOOP.md) | How `game-ppt-master` hands off assets and review JSON into `game-review` |
| 📐 | [Canvas Formats](./skills/ppt-master/references/canvas-formats.md) | PPT 16:9, Xiaohongshu, WeChat, and 10+ formats |
| 🛠️ | [Scripts & Tools](./skills/ppt-master/scripts/README.md) | All scripts and commands |
| 💼 | [Examples](./examples/README.md) | 15 projects, 229 pages |
| 🏗️ | [Technical Design](./docs/technical-design.md) | Architecture, design philosophy, why SVG |
| ❓ | [FAQ](./docs/faq.md) | Model selection, cost, layout troubleshooting, custom templates |

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to get involved.

## License

[MIT](LICENSE)

## Acknowledgments

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(author)) (CRAP principles) · McKinsey, BCG, Bain

## Contact & Collaboration

Looking to collaborate, integrate Game PPT Master into your workflow, or just have questions?

- 🐛 **Bug reports & feature requests** — [GitHub Issues](https://github.com/k412407009/game-ppt-master/issues)
- 📦 **Repository home** — [github.com/k412407009/game-ppt-master](https://github.com/k412407009/game-ppt-master)
- 🧱 **Upstream base engine** — [github.com/hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)

---

## Supported by DigitalOcean

<p>This project is supported by:</p>
<p>
  <a href="https://m.do.co/c/547f129aabe1">
    <img src="https://opensource.nyc3.cdn.digitaloceanspaces.com/attribution/assets/PoweredByDO/DO_Powered_by_Badge_blue.svg" alt="Powered by DigitalOcean" width="201" />
  </a>
</p>

Made with ❤️ on top of [Hugo He's upstream engine](https://github.com/hugohe3/ppt-master)

[⬆ Back to Top](#game-ppt-master--ai-generates-natively-editable-pptx-for-game-industry-decks)
