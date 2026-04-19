---
name: ppt-cycle-game-master
description: >
  Game-pitch PPT skill specialized for single-loop / cycle-based games (idle-management,
  vertical tower-defense, factory-chain, MPH-style). Wraps ppt-master's 7-step pipeline
  with a "film-crew" role metaphor and a Single-Run Density (SRD) checklist that quantifies
  hook cadence at sub-minute granularity. Use when the user asks to "做单机循环游戏立项 PPT",
  "circular game pitch", "塔防立项 PPT", "竖屏塔防 PPT", "idle game PPT", "电影组",
  or mentions "ppt-cycle-game-master".
---

# PPT Cycle-Game Master Skill

> 针对**单机循环 / 塔防 / 放置 / 工厂链**类游戏的"立项 PPT"专项 skill。
> 在 `ppt-master` 的 7 步流水线之上，套一层"电影组"角色比喻 + 节奏密度量化 + 简化的八问八答，
> 让对话更短、决策更快、节奏更可量化。

**Core Pipeline**（与 `ppt-master` 完全一致，本 skill 不重写脚本）:

```
Source → Project → Template → Strategist → [Game Asset Collection] → [Image_Generator] → Executor → Post → Export
   编剧前置        制片         美指          编剧（电影组核心）              摄影                美术          导演          剪辑       放映
```

> 本 skill 的"电影组"角色只是 **对话层别名**，底层执行链仍然是 `ppt-master` 的 6 角色 + 7 步骤。
> 所有脚本、validate、finalize、svg_to_pptx 一律调 `skills/ppt-master/scripts/*`，**绝不复制一份**。

---

## 何时触发本 skill（vs `ppt-master`）

| 场景 | 用 `ppt-master` | 用本 skill `ppt-cycle-game-master` |
|---|---|---|
| 通用咨询/年报/学术 PPT | ✅ | ❌ |
| 引用真实游戏的"立项汇报" | ✅（也可以） | ✅✅（更优，自带电影组对话 + SRD 表） |
| 单机循环游戏（MPH/Whiteout/放置）立项 | ✅（可） | ✅✅✅ |
| 竖屏塔防游戏立项（9:16） | ✅（可） | ✅✅✅（专属 vertical-tower-defense-pack） |
| 工厂链/产业化（Mindustry-like） | — | ✅✅（vertical-tower-defense-pack 包含此模式） |
| **玩法有"双线情绪反差/双调色板/复杂叙事弧"** | ✅✅ | ❌（本 skill **故意砍掉**双调色板模式，专为"单循环"优化） |

> **本 skill 的取舍**：用户已明确"玩法上不会有太多融合与过渡，更倾向单机循环制"。
> 因此本 skill **不内置**双调色板（DAY/NIGHT）、双玩法切换、Pixar 角色情感弧 等"叙事重型"工具——
> 那些保留在 `ppt-master` + `references/executor-consultant-top.md` 里。

---

## 🎬 Crew Roles（电影组角色映射）

| 电影组 | ppt-master 底层 | 主要产物 | 关键 reference |
|---|---|---|---|
| 📝 **编剧 Screenwriter** | Strategist | `design_spec.md` + 八问八答 + SRD 表 | `references/crew-roles.md` §1 / `${PPT_MASTER}/references/strategist.md` |
| 🎬 **导演 Director** | Executor | `svg_output/*.svg`（节奏 + 视觉锚点 + 转场） | `references/crew-roles.md` §2 / `${PPT_MASTER}/references/executor-base.md` |
| 🎨 **美术 Art Director** | Image_Generator | `images/_gen/`（立绘） + `images/_remix/`（i2i 风格化） | `references/crew-roles.md` §3 / `${PPT_MASTER}/references/image-generator.md` |
| 📷 **摄影 DOP** | Game_Asset_Collector | `images/_game_assets/<game>/`（商店截图 + 视频抽帧） | `references/crew-roles.md` §4 / `${PPT_MASTER}/references/game-asset-collector.md` |
| ✂️ **剪辑 Editor** | Post-processor | `svg_final/` + `notes/*.md` | `references/crew-roles.md` §5 / `${PPT_MASTER}/SKILL.md` Step 7 |
| 🎟️ **制片 Producer** | Project_Manager + Exporter | `exports/*.pptx`（双版本） | `references/crew-roles.md` §6 |

> `${PPT_MASTER}` = `skills/ppt-master/`

---

## 📐 Single-Run Density (SRD) — 核心独有概念

**SRD = Single-Run Density / 单循环节奏密度**：用 7 档时间锚点（5.1-5.7）量化"玩家头 30 秒到 D30"的钩子分布。
本 skill 强制要求 `design_spec.md` §V 必须包含一份完整的 SRD 表（模板见 `templates/srd_table.md`）。

| 阶段 | 时长 | 必触钩子 | 留存目标 |
|---|---|---|---|
| 5.1 | **0–30s** | 视觉钩子 ×1 | 95% |
| 5.2 | 30s–2min | 反馈循环 ① | 80% |
| 5.3 | 2–15min | 核心玩法首演 | 70% |
| 5.4 | 15–60min | 第二机制引入 | 60% |
| 5.5 | 1–4h | 元层耦合 | 50% |
| 5.6 | **Day 2–3** | 战斗/反派/高峰 | 40% |
| 5.7 | Day 5–30 | LTV / 长期目标 | 20% |

**反模式禁忌**（提炼自 I_动物联盟 复盘，详见 `references/lessons-from-i-zoo.md`）:
- ❌ 5.1 起步在"30 分钟"而非 30 秒 → 头 30 分流失 48%+
- ❌ 5.5 → 5.6 跳过 Day 2-3 → 玩家"第一次"新鲜感断点
- ❌ 战斗/反派 Day 7 才出 → 玩家不知道游戏有"战斗"概念
- ❌ "思考头 30s vs 30min" 单位歧义不区分 → 编剧/导演沟通错位

完整 SRD 检查表见 `references/srd-density-checklist.md`。

---

## 🗣️ 对话风格（必读）

本 skill **必须** 在 Step 4 八问八答前先读 `references/conversation-style.md`：
- **简短指令承接**："都ok的" / "剩余的直接跑完" / "B1 c1 D1 E1" 等快速决策键的处理 SOP
- **修正模式识别**："我挺喜欢... 唯一的问题是 X" 不是否定，是**局部修正**
- **颗粒度敏感**：任何时间单位（s/min/h/Day）必须 explicit，AI 主动澄清"30s 还是 30min"
- **类比驱动澄清**：用户给 2-3 个类比时（"俯视角射击 vs 怪物横扫"），AI 必须给具体方案
- **背景前置**：用户提到"S2"等阶段语境，AI 不要追问，直接采纳
- **速通模式**：用户说"剩余的直接跑完"后，AI 不再二次确认，但**完成后必须发完整报告**

---

## 🚀 启动流程（用户开新项目时）

1. **复制项目级模板**到新项目：
   ```powershell
   Copy-Item skills/ppt-cycle-game-master/AGENT_PROMPT_template.md `
             projects/<项目名>/AGENT_PROMPT.md
   ```

2. **AI 读取触发链**（按顺序）:
   ```
   skills/ppt-cycle-game-master/SKILL.md         ← 你正在读
   skills/ppt-cycle-game-master/references/conversation-style.md   ← 必读
   skills/ppt-cycle-game-master/references/workflow.md
   skills/ppt-cycle-game-master/references/crew-roles.md
   skills/ppt-cycle-game-master/references/srd-density-checklist.md
   ```

3. **按题材二选一**（任选其一）:
   - 单机循环 / 经营 / 放置 → `references/cycle-game-pitch-pack.md`
   - 竖屏塔防 / 工厂链 / 产业化 → `references/vertical-tower-defense-pack.md`

4. **进入 ppt-master 7 步**：从 Step 1 (source_to_md) 开始；Step 4 用本 skill 的"电影组" + SRD；
   Step 4.5 必触发；Step 6/7 完全复用 `ppt-master/scripts/*`。

---

## 🚨 强制纪律（继承自 ppt-master + 本 skill 加强）

> 本 skill **完全继承** `${PPT_MASTER}/SKILL.md` 的 8 条 Global Execution Discipline。
> 在此基础上 **额外加 3 条**：

9. **SRD 表强制** — `design_spec.md` §V 必须包含 7 档 SRD 表（5.1–5.7），缺任何一档视为执行失败
10. **抽帧覆盖率 ≥3 款** — 单机循环立项至少抽 3 款竞品截图/视频帧（建议 5 款），覆盖"核心循环 / 美术 / 商业化"3 个维度
11. **速通报告强制** — 用户说"直接跑完"后，AI 完成所有 SVG/notes/finalize/export 后，**必须输出一份完成报告**（页数 / SVG PASS / 讲稿字数 / PPTX 大小 / 反思 1-3 条）

---

## References Index

| 文件 | 作用 | 必读时机 |
|---|---|---|
| `references/conversation-style.md` | 用户对话风格 SOP（快速决策 / 修正模式 / 颗粒度 / 速通） | **本 skill 触发后立即** |
| `references/workflow.md` | 7 步工作流（电影组 + ppt-master 映射） | Step 1 之前 |
| `references/crew-roles.md` | 6 角色 × 产物 × 底层映射 | Step 4 之前 |
| `references/srd-density-checklist.md` | 7 档 SRD 节奏密度量化清单 + 反模式 | Step 4 编写 design_spec §V 时 |
| `references/cycle-game-pitch-pack.md` | 单机循环游戏立项专题包（轻量化） | 题材为"循环"时 |
| `references/vertical-tower-defense-pack.md` | 竖屏塔防 + 产业化专题包 | 题材为"塔防/工厂"时 |
| `references/lessons-from-i-zoo.md` | I_动物联盟 项目 10 条经验复盘 | 启动新项目前推荐回顾 |

## Templates Index

| 文件 | 作用 |
|---|---|
| `AGENT_PROMPT_template.md` | 项目级 AI 提示词模板（每个新项目复制一份） |
| `templates/design_spec_skeleton_cycle.md` | 单机循环游戏 design_spec.md 骨架（含 SRD §V） |
| `templates/eight_questions.md` | 八问八答（电影组语言版） |
| `templates/srd_table.md` | SRD 节奏密度表 markdown 模板 |

---

## Notes

- 本 skill **不复制** `ppt-master/scripts/*`；所有脚本路径写为 `${PPT_MASTER}/scripts/<name>.py`
- 本 skill 对**双调色板 / 双玩法切换 / Pixar 情感弧**等"叙事重型"工具**故意不支持**，需要时回 `ppt-master` 用 `executor-consultant-top.md`
- 触发条件：源材料含"游戏立项 / 同类竞品分析 / Demo 设计 / GDD 草案"+ 目标输出"立项 PPT"
- 与 `ppt-master/scripts/game_assets/fetch_game_assets.py` **强耦合**：本 skill 默认 Step 4.5 触发率 = 100%
