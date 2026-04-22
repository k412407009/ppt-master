# 同事接入指南_TEAM_ONBOARDING_GUIDE

这是一份可以直接转发给同事的入口页。目标只有一个：让别人拿到链接后，知道要下载哪三个仓、怎么摆目录、哪些 API Key 要准备、第一轮怎么跑通。

---

## 直接发这组链接

- 主入口：
  [https://github.com/k412407009/ppt-master/blob/main/docs/同事接入指南_TEAM_ONBOARDING_GUIDE.md](https://github.com/k412407009/ppt-master/blob/main/docs/%E5%90%8C%E4%BA%8B%E6%8E%A5%E5%85%A5%E6%8C%87%E5%8D%97_TEAM_ONBOARDING_GUIDE.md)
- 主仓 `ppt-master`：
  [https://github.com/k412407009/ppt-master](https://github.com/k412407009/ppt-master)
- 采集器 `game-asset-collector`：
  [https://github.com/k412407009/game-asset-collector](https://github.com/k412407009/game-asset-collector)
- 评审模块 `game-review`：
  [https://github.com/k412407009/game-review](https://github.com/k412407009/game-review)

如果只想发一个链接，就发上面的“主入口”。

---

## 三个仓分别干什么

| 仓库 | 作用 | 是否必需 |
| --- | --- | --- |
| `ppt-master` | 主工作流，负责资料整理、设计规格、页面生成、PPT 导出 | 必需 |
| `game-asset-collector` | 商店截图、视频抓取、抽帧、标签和描述 | 做游戏方向时必需 |
| `game-review` | 5 位评委 × 7 维度的结构化评审，输出 `docx` / `xlsx` / `md` | 做评审报告时必需 |

推荐目录结构：

```text
~/Desktop/Git/
  ppt-master/
  game-asset-collector/
  game-review/
```

三者要放在同级目录，不要嵌套。

---

## 怎么下载

### 方式 A：直接下载 ZIP

分别打开这三个仓库页面，点 `Code -> Download ZIP`。

### 方式 B：Git clone

```bash
cd ~/Desktop/Git
git clone https://github.com/k412407009/ppt-master.git
git clone https://github.com/k412407009/game-asset-collector.git
git clone https://github.com/k412407009/game-review.git
```

---

## 哪些 API / Key 需要准备

先分清两层：

1. IDE 主模型
2. 仓库脚本直接调用的 API

### A. IDE 主模型

这是你在 Cursor / Claude Code / Codex 里实际使用的主模型。它负责读 `SKILL.md`、决定调用哪个脚本、组织内容和输出。

常见选择：

- Claude
- ChatGPT / Codex
- 以后也可以接别的长上下文 coding model

这一层的账号和 Key，通常由 IDE 自己管理，不在这三个仓里硬编码。

### B. `ppt-master` 直接调用的 API

`ppt-master` 本身主要是工作流编排和 PPT 生成。它的直接外部调用主要分两类：

- 文档/网页转换：
  `curl_cffi`、`requests`、`pandoc`
- 图像生成：
  `skills/ppt-master/scripts/image_gen.py`

如果要开图像生成，需要配置：

- `IMAGE_BACKEND`
- 对应厂商的独立 Key，例如：
  - `OPENAI_API_KEY`
  - `GEMINI_API_KEY`
  - `VOLCENGINE_API_KEY` 或 `ARK_API_KEY`
  - `QWEN_API_KEY`
  - `ZHIPU_API_KEY`

火山引擎在这里的作用主要是图片生成后端之一。

### C. `game-asset-collector` 直接调用的 API

这是素材采集层，负责：

- App Store API
- `google_play_scraper`
- Steam API
- Tavily
- `yt-dlp`
- `ffmpeg`
- ARK / Volcengine Vision

最关键的环境变量：

| 变量 | 用途 | 是否建议 |
| --- | --- | --- |
| `TAVILY_API_KEY` | 商店页面兜底抓取、文本抽取 | 建议配置 |
| `ARK_API_KEY` | ARK / Doubao Vision 打标和中文描述 | 建议配置 |
| `VOLCENGINE_API_KEY` | `ARK_API_KEY` 的别名，也可直接用 | 二选一 |

火山引擎在这里的作用主要是视觉识别，不是主评审模型。

### D. `game-review` 直接调用的 API

当前公开版默认评审 provider 是：

- `COMPASS_API_KEY`

如果没配，会回退到本地 stub，流程能跑，但评审内容会退化成占位结果。

这层以后可以接：

- 火山引擎兼容 provider
- OpenAI 兼容 provider

但当前公开仓默认还是 Compass。

### E. DevTable API Key 现在处于什么位置

当前这三个公开仓里，**没有内建的 DevTable client**。也就是说：

- DevTable 不是三仓主链路的必需依赖
- 现在没有一个已经写死、必须照抄的 `DevTable` 环境变量名
- 如果你们内部要把项目单、素材索引、评审记录同步到 DevTable，那属于“协作数据层”，不是“PPT / 采集 / 评审”主链路

如果后面要统一给同事配置，我建议把命名固定成：

- `DEVTABLE_API_KEY`
- `DEVTABLE_BASE_URL`
- `DEVTABLE_APP_ID`
- `DEVTABLE_TABLE_ID`

注意：这四个名字是**推荐约定**，不是当前公开仓里已经强依赖的事实。

---

## 第一轮怎么跑通

### 只做 PPT

只需要 `ppt-master`。

典型流程：

1. 准备 PDF / DOCX / URL / Markdown
2. 在 IDE 里让模型按 `skills/ppt-master/SKILL.md` 跑
3. 输出 `exports/*.pptx`

### 做外部游戏素材

需要：

- `ppt-master`
- `game-asset-collector`

典型流程：

1. 在 `game-asset-collector` 跑商店抓取和视频抽帧
2. 得到 `raw_assets/<game>/...`
3. 把这些素材供 `ppt-master` 或 `game-review` 继续消费

### 做完整评审闭环

需要三个仓都在。

典型顺序：

1. `ppt-master` 组织问题、整理输入、确定项目结构
2. `game-asset-collector` 拉商店截图、关键帧、标签、描述
3. Agent / 人工补全 `review.json`
4. `game-review` 产出：
   - `*_review.docx`
   - `*_review.xlsx`
   - `*_subjective_responses.md`
5. 如需汇报，再把报告回灌到 `ppt-master` 做最终 PPT

---

## 推荐最小环境变量清单

如果是第一次给同事装机，先从这组最小变量开始：

```env
# game-asset-collector
TAVILY_API_KEY=...
ARK_API_KEY=...

# game-review
COMPASS_API_KEY=...

# ppt-master image generation (optional)
IMAGE_BACKEND=volcengine
VOLCENGINE_API_KEY=...
```

说明：

- 只做 PPT 而且不用 AI 出图时，不一定需要 `VOLCENGINE_API_KEY`
- 做素材识别时，`ARK_API_KEY` 很有价值
- 做正式评审时，`COMPASS_API_KEY` 很重要
- `DevTable` 不是当前公开三仓跑通所必需

---

## 更完整的说明去哪看

- 三仓架构总览：
  [三仓协同架构_THREE_REPO_STACK.md](./三仓协同架构_THREE_REPO_STACK.md)
- 机器可读元数据：
  [生态清单_ECOSYSTEM_MANIFEST.json](./生态清单_ECOSYSTEM_MANIFEST.json)
- 游戏评审闭环：
  [游戏评审闭环_GAME_REVIEW_CLOSED_LOOP.md](./游戏评审闭环_GAME_REVIEW_CLOSED_LOOP.md)

---

## 一句话介绍给同事

这套系统不是单仓工具，而是三仓协作：

- `ppt-master` 管主流程和 PPT
- `game-asset-collector` 管抓取和抽帧
- `game-review` 管结构化评审报告

当前公开版必需 API 主要是素材层和评审层；火山引擎主要用在视觉识别和可选图片生成；DevTable 目前属于可选的内部协作数据层，不是公开三仓的强依赖。
