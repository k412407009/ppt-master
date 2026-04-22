# Game PPT Master — 面向游戏行业的原生可编辑 PPTX 工作流

[![Version](https://img.shields.io/badge/version-v2.3.0-blue.svg)](https://github.com/k412407009/game-ppt-master/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/k412407009/game-ppt-master.svg)](https://github.com/k412407009/game-ppt-master/stargazers)

[English](./README.md) | 中文

<p align="center">
  <a href="./docs/三仓协同架构_THREE_REPO_STACK.md"><strong>三仓架构</strong></a> ·
  <a href="./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md"><strong>游戏向魔改说明</strong></a> ·
  <a href="./examples/"><strong>示例</strong></a> ·
  <a href="./docs/zh/faq.md"><strong>常见问题</strong></a> ·
  <a href="https://github.com/k412407009/game-ppt-master/issues"><strong>Issues</strong></a>
</p>

> **仓库定位** — Game PPT Master 是基于上游 [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) 做的公开游戏行业定向改造版。底层可编辑 PPTX 引擎保持兼容，这个仓库额外补了游戏向工作流、共享采集器衔接和结构化评审闭环。详见 [游戏向魔改说明](./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md)。

---

丢进一份 PDF、DOCX、网址或 Markdown，拿回一份**原生可编辑的 PowerPoint**——真正的形状、真正的文本框、真正的图表，不是图片。然后继续衔接游戏素材抓取、评审产出和最终汇报。

> **运作方式** —— Game PPT Master 是一套在 AI IDE（Claude Code / Cursor / VS Code + Copilot / Codebuddy 等）里运行的工作流（一个 "skill"）。你在 IDE 的对话框里跟 AI 说"用这份资料做一份游戏行业 PPT"，AI 按这套工作流在你本机生成一个真正可编辑的 `.pptx`。你不写任何代码——IDE 只是你和 AI 对话的地方。
>
> **你要做的**：装 Python、装一个 AI IDE、把资料放进来。第一次配置约 15 分钟；之后每做一份 PPT 大约 10–20 分钟的聊天。

**[为什么选这套底层引擎？](./docs/zh/why-ppt-master.md)**

市面上不缺 AI PPT 工具——缺的是一个**生成出来的 PPT 能真正拿去用**的工具。我每天都在做 PPT，但大部分产品输出的是图片或网页截图，好看但改不了；要么就是基础到只有文本框和列表。你还得按月充会员，把文件传到别人的服务器上，被锁在某个平台里。

Game PPT Master 不一样：

- **真正的 PPT** — 如果一个文件在 PowerPoint 里打不开、不能编辑，它就不应该被叫做 PPT。Game PPT Master 输出的每个元素都能直接点击修改
- **游戏行业闭环** — 在底层 PPT 能力之上，这个仓库补了素材抓取衔接、评审报告联动和游戏向工作流
- **成本透明可控** — 工具免费开源，唯一成本是你自己的 AI 编辑器，花了多少钱你清清楚楚。VS Code Copilot 下最低 **$0.08/份**
- **数据不出本地** — 你的文件不应该为了做一份 PPT 就被上传到别人的服务器。除与 AI 模型的对话外，全流程在你的电脑上完成
- **不锁定平台** — 你的工作流不应该被任何一家公司绑架。Claude Code、Cursor、VS Code Copilot 等均可驱动；Claude、GPT、Gemini、Kimi 等模型均可使用

**[查看底层引擎示例 →](https://hugohe3.github.io/ppt-master/)** · [`examples/`](./examples/) — 15 个项目，229 页

## 效果展示

<table>
  <tr>
    <td align="center"><img src="docs/assets/screenshots/preview_magazine_garden.png" alt="杂志风 — 打造小院指南" /><br/><sub><b>杂志风</b> — 暖色调，大图排版，生活方式感</sub></td>
    <td align="center"><img src="docs/assets/screenshots/preview_academic_medical.png" alt="学术风 — 医学图像分割研究" /><br/><sub><b>学术风</b> — 严谨结构，数据图表，论文答辩场景</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/assets/screenshots/preview_dark_art_mv.png" alt="暗色艺术风 — MV 深度解析" /><br/><sub><b>暗色艺术风</b> — 电影感深色背景，美术馆陈列感</sub></td>
    <td align="center"><img src="docs/assets/screenshots/preview_nature_wildlife.png" alt="自然风 — 湿地野生动物纪录" /><br/><sub><b>自然纪录风</b> — 沉浸式摄影，简洁信息层级</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/assets/screenshots/preview_tech_claude_plans.png" alt="科技风 — Claude AI 订阅方案" /><br/><sub><b>科技 / SaaS 风</b> — 白底卡片，定价表格，产品说明书</sub></td>
    <td align="center"><img src="docs/assets/screenshots/preview_launch_xiaomi.png" alt="发布会风 — 小米春季新品" /><br/><sub><b>发布会风</b> — 高对比度，参数突出，苹果/小米发布会感</sub></td>
  </tr>
</table>

---

## 上游基础与游戏向改造

原始的 `ppt-master` 引擎与可编辑 PPTX 工作流由 [Hugo He](https://github.com/hugohe3/ppt-master) 创建，这部分仍然是本仓库的底层技术基础。

Game PPT Master 在这个基础上，专门面向游戏行业补了几层能力：

- 三仓协同：`game-ppt-master` + `game-asset-collector` + `game-review`
- 外部游戏素材抓取与抽帧衔接
- 结构化评审报告闭环
- 游戏项目用的 skill / prompt / 交付流程

具体差异见 [游戏向魔改说明](./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md)。

---

## 快速开始

### 1. 前置条件

**只需装 Python 即可。** 其余依赖通过 `pip install -r requirements.txt` 一次装齐。

| 依赖 | 是否必须 | 用途 |
|------|:--------:|------|
| [Python](https://www.python.org/downloads/) 3.10+ | ✅ **必需** | 核心运行时——唯一真正需要安装的东西 |

> **一句话总结** — 装好 Python，跑一行 `pip install -r requirements.txt`，就可以开始生成 PPT 了。

<details open>
<summary><strong>Windows</strong> — 请看专门的手把手安装指南 ⚠️</summary>

Windows 需要一些额外步骤（PATH 设置、执行策略等）。我们为 Windows 用户写了一份**手把手安装指南**：

**📖 [Windows 安装指南](./docs/zh/windows-installation.md)** — 从零到跑通第一份 PPT，10 分钟搞定。

简要流程：从 [python.org](https://www.python.org/downloads/) 下载 Python → **安装时勾选 "Add to PATH"** → `pip install -r requirements.txt` → 完成。
</details>

<details>
<summary><strong>macOS / Linux</strong> — 安装即用</summary>

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
<summary><strong>边缘场景备用方案</strong> — 99% 的用户用不到</summary>

下面两个外部程序只作为极端场景的兜底。**绝大多数用户根本不需要装**，只有遇到以下具体场景才装：

| 备用方案 | 只在以下情况才装 |
|---------|-----------------|
| [Node.js](https://nodejs.org/) 18+ | 你需要抓取微信公众号文章，**且**你的 Python + 系统 + CPU 组合下 `curl_cffi`（`requirements.txt` 里已默认安装）没有预编译 wheel。正常安装下 `web_to_md.py` 已能通过 `curl_cffi` 直接抓微信。 |
| [Pandoc](https://pandoc.org/) | 你需要转 `.doc`、`.odt`、`.rtf`、`.tex`、`.rst`、`.org`、`.typ` 这些小众格式。`.docx`、`.html`、`.epub`、`.ipynb` 已由 Python 原生处理，不需要 pandoc。 |

```bash
# macOS（仅在上述条件成立时才装）
brew install node
brew install pandoc

# Ubuntu / Debian
sudo apt install nodejs npm
sudo apt install pandoc
```
</details>

### 2. 选择 AI 编辑器

| 工具 | 推荐度 | 说明 |
|------|:------:|------|
| **[Claude Code](https://claude.ai/)** | ⭐⭐⭐ | 效果最佳——原生 Opus，上下文最充裕 |
| [Cursor](https://cursor.sh/) / [VS Code + Copilot](https://code.visualstudio.com/) | ⭐⭐ | 不错的替代方案 |
| Codebuddy IDE | ⭐⭐ | 国产模型最佳选择（Kimi 2.5、MiniMax 2.7） |

### 3. 配置项目

**方式 A — 下载 ZIP**（无需安装 Git）：
[GitHub](https://github.com/k412407009/game-ppt-master) → **Code → Download ZIP**

**方式 B — Git clone**（需先安装 [Git](https://git-scm.com/downloads)）：

```bash
git clone https://github.com/k412407009/game-ppt-master.git
cd game-ppt-master
```

然后安装依赖：

```bash
pip install -r requirements.txt
```

日常更新（仅方式 B）：`python3 skills/ppt-master/scripts/update_repo.py`

### 4. 开始创作

**提供原始材料（推荐）：** 将 PDF、DOCX、图片等文件放入 `projects/` 目录下，在 AI 聊天面板中告诉它使用哪些文件。获取路径的最快方式：在文件管理器或 IDE 侧边栏中右键文件 → **复制路径**（Copy Path / Copy Relative Path），直接粘贴进聊天框。

```
你：请用 projects/q3-report/sources/report.pdf 这份文件生成一份 PPT
```

**直接输入内容：** 也可以把文字内容直接粘贴进聊天窗口，AI 会根据这些内容生成 PPT。

```
你：请根据以下内容制作成 PPT：[粘贴你的文字内容...]
```

两种方式下 AI 都会先确认设计规范：

```
AI：好的，先确认设计规范：
   [模板] B) 自由设计
   [格式] PPT 16:9
   [页数] 8-10 页
   ...
```

AI 全程处理——内容分析、视觉设计、SVG 生成、PPTX 导出。

> **输出说明：** 两个带时间戳的文件保存至 `exports/` — 原生形状版 `.pptx`（可直接编辑）和 `_svg.pptx` 快照版（视觉参考备份）。需要 Office 2016+。

> **AI 迷失上下文？** 让它先读 `skills/ppt-master/SKILL.md`。

> **遇到问题？** 查看 **[常见问题](./docs/zh/faq.md)** — 涵盖模型选择、排版问题、导出异常等，基于真实用户反馈持续更新。

### 5. AI 生图配置（可选）

```bash
cp .env.example .env    # 然后填入你的 API Key
```

```env
IMAGE_BACKEND=gemini                        # 必填——必须显式指定
GEMINI_API_KEY=your-api-key
GEMINI_MODEL=gemini-3.1-flash-image-preview
```

支持的后端：`gemini` · `openai` · `qwen` · `zhipu` · `volcengine` · `stability` · `bfl` · `ideogram` · `siliconflow` · `fal` · `replicate`

运行 `python3 skills/ppt-master/scripts/image_gen.py --list-backends` 查看分级。环境变量优先于 `.env`。使用各家独立的 Key（`GEMINI_API_KEY`、`OPENAI_API_KEY` 等）——不支持全局 `IMAGE_API_KEY`。

> **建议：** 高质量图片推荐在 [Gemini](https://gemini.google.com/) 中生成并选择 **Download full size**。去水印可用 `scripts/gemini_watermark_remover.py`。

---

## 文档导航

| | 文档 | 说明 |
|---|------|------|
| 🆚 | [为什么选这套引擎](./docs/zh/why-ppt-master.md) | 上游 PPT 引擎与 Gamma、Copilot 等工具的对比 |
| 🪟 | [Windows 安装指南](./docs/zh/windows-installation.md) | Windows 用户手把手安装教程 |
| 📖 | [SKILL.md](./skills/ppt-master/SKILL.md) | 核心流程与规则 |
| 🎮 | [游戏向魔改说明](./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md) | 说明和上游 `ppt-master` 相比，这个仓库改了什么、保留了什么、为什么 GitHub repo 改名为 `game-ppt-master` |
| 🤝 | [同事接入指南](./docs/同事接入指南_TEAM_ONBOARDING_GUIDE.md) | 可直接转发给同事的下载、API Key、串联说明 |
| 🧭 | [三仓协同架构](./docs/三仓协同架构_THREE_REPO_STACK.md) | `game-ppt-master`、`game-asset-collector`、`game-review` 的完整链路 |
| 📐 | [画布格式](./skills/ppt-master/references/canvas-formats.md) | PPT 16:9、小红书、朋友圈等 10+ 种格式 |
| 🛠️ | [脚本与工具](./skills/ppt-master/scripts/README.md) | 所有脚本和命令 |
| 💼 | [示例](./examples/README.md) | 15 个项目，229 页 |
| 🏗️ | [技术路线](./docs/zh/technical-design.md) | 架构、设计哲学、为什么选 SVG |
| ❓ | [常见问题](./docs/zh/faq.md) | 模型选择、费用、排版问题排查、自定义模板 |

---

## 贡献

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 开源协议

[MIT](LICENSE)

## 致谢

[SVG Repo](https://www.svgrepo.com/) · [Tabler Icons](https://github.com/tabler/tabler-icons) · [Robin Williams](https://en.wikipedia.org/wiki/Robin_Williams_(author))（CRAP 设计原则）· 麦肯锡、BCG、贝恩

## 联系与合作

欢迎讨论 Game PPT Master 这个游戏行业改造版，或者查看上游底层引擎：

- 🐛 **Bug 反馈与功能建议** — [GitHub Issues](https://github.com/k412407009/game-ppt-master/issues)
- 📦 **当前仓库** — [github.com/k412407009/game-ppt-master](https://github.com/k412407009/game-ppt-master)
- 🧱 **上游底层引擎** — [github.com/hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)

---

## DigitalOcean Support

<p>本项目获得 DigitalOcean Open Source Credits Program 支持：</p>
<p>
  <a href="https://m.do.co/c/547f129aabe1">
    <img src="https://opensource.nyc3.cdn.digitaloceanspaces.com/attribution/assets/PoweredByDO/DO_Powered_by_Badge_blue.svg" alt="Powered by DigitalOcean" width="201" />
  </a>
</p>

Made with ❤️ on top of [Hugo He 的上游引擎](https://github.com/hugohe3/ppt-master)

[⬆ 回到顶部](#game-ppt-master--面向游戏行业的原生可编辑-pptx-工作流)
