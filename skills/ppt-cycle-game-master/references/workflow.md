# Workflow — 7 步工作流（电影组叙事 + ppt-master 底层映射）

> 本 workflow **完全继承** `${PPT_MASTER}/SKILL.md` 的 7 步流水线 + 8 条 Global Execution Discipline。
> 本文件**只列差异**，相同的部分用 → 链回 ppt-master。
>
> `${PPT_MASTER}` = `skills/ppt-master/`
> `${SKILL_DIR}`  = `skills/ppt-cycle-game-master/`

---

## 总览

```
Source → Project → Template → Strategist → [Game Asset Collection] → [Image_Gen] → Executor → Post → Export
  📚       🎟️         🎬          📝             📷                          🎨           🎬       ✂️       🎟️
   编剧前置  制片        美指        编剧                 摄影                            美术        导演      剪辑      放映
```

| Step | ppt-master 名 | 本 skill 别名 | 强化点 |
|---|---|---|---|
| 1 | Source Processing | 📚 编剧前置 | 同 ppt-master，无差异 |
| 2 | Project Init | 🎟️ 制片立项 | 自动 cp `AGENT_PROMPT_template.md` 到项目目录 |
| 3 | Template | 🎬 美指选模板 | **默认走 free design**（循环游戏 PPT 不适合套老模板） |
| 4 | Strategist | 📝 编剧（**核心**） | 八问八答用电影组语言 + **强制产出 SRD §V** |
| 4.5 | Game Asset Collection | 📷 摄影抽帧 | **触发率 100%**（本 skill 必走） |
| 5 | Image Generator | 🎨 美术生立绘 | i2i 风格化 + 章节背景 |
| 6 | Executor | 🎬 导演拍摄 | SVG 节奏 + 视觉锚点 + 转场 |
| 7 | Post + Export | ✂️ 剪辑 + 🎟️ 放映 | finalize + 双版本 PPTX + 速通报告 |

---

## Step 1: Source Processing 📚 编剧前置

**100% 复用** `${PPT_MASTER}/SKILL.md` Step 1。

> 单机循环游戏立项的源材料通常是：
> - 早期 GDD 草案 (`.docx`)
> - 同类竞品分析（飞书 / 腾讯文档 url）
> - 老板的微信对话截图（贴文字到对话）
> - 自己脑子里的想法（直接说，不需要文件）

→ 见 `${PPT_MASTER}/SKILL.md` Step 1 表格。

---

## Step 2: Project Init 🎟️ 制片立项

**100% 复用** `${PPT_MASTER}/SKILL.md` Step 2 + **本 skill 加 1 步**：

```bash
python3 ${PPT_MASTER}/scripts/project_manager.py init <项目名> --format ppt169
# 或竖屏：--format xhs

# 本 skill 额外步骤：复制 AGENT_PROMPT 模板
cp ${SKILL_DIR}/AGENT_PROMPT_template.md \
   projects/<项目名>/AGENT_PROMPT.md
```

> ⚠️ **画布选择**：
> - 单机循环经营 → `ppt169`（横屏，适合评审会投影）
> - 竖屏塔防 → 评审会用 `ppt169`，但 design_spec §VIII 必须含 9:16 截图

---

## Step 3: Template 🎬 美指选模板

⛔ **BLOCKING**: 与 ppt-master 一致，但本 skill **默认推荐 B (Free Design)**：

```markdown
💡 AI Recommendation：单机循环游戏立项 PPT 内容高度自定义（SRD 表 / 抽帧拼贴 / 立绘），
现成模板（McKinsey / Telecom）会限制视觉自由度，**强烈建议选 B Free Design**。

A) Use existing template
B) Free Design ★（推荐）
```

→ 详见 `${PPT_MASTER}/SKILL.md` Step 3。

---

## Step 4: Strategist 📝 编剧（**核心 + 强化**）

🚧 **GATE**: Step 3 complete.

⛔ **BLOCKING**: 八问八答 + SRD 表 必须完成且用户确认才能进 Step 4.5。

### 4.1 必读链（按顺序）

```
1. ${SKILL_DIR}/references/conversation-style.md  ← 对话风格 SOP
2. ${SKILL_DIR}/references/crew-roles.md §1       ← 编剧角色定义
3. ${SKILL_DIR}/references/srd-density-checklist.md  ← SRD 7 档清单
4. 按题材二选一：
   ├─ 单循环 → ${SKILL_DIR}/references/cycle-game-pitch-pack.md
   └─ 塔防   → ${SKILL_DIR}/references/vertical-tower-defense-pack.md
5. ${PPT_MASTER}/references/strategist.md          ← 底层 Strategist gate（必走）
6. ${PPT_MASTER}/templates/design_spec_reference.md  ← design_spec 母版
```

### 4.2 八问八答（电影组语言）

→ 见 `${SKILL_DIR}/templates/eight_questions.md`

### 4.3 SRD §V 必填

design_spec.md §V "Core Loop" 必须包含 7 档完整 SRD 表。
→ 见 `${SKILL_DIR}/templates/srd_table.md`

**反模式自检**（写完后 AI 必须 self-check）：
- [ ] 5.1 起步 ≤30s（不是 30min）
- [ ] 5.2-5.7 没有断点（每档时长连续）
- [ ] 5.6 含战斗 / 反派 / 第一次 PvE（Day 2-3 内）
- [ ] 所有时间字段含单位（s / min / h / Day）

---

## Step 4.5: Game Asset Collection 📷 摄影抽帧（**强制**）

🚧 **GATE**: Step 4 complete + 用户确认 design_spec。

> ⚡ **本 skill 触发率 100%**：单机循环 / 塔防立项 PPT 没有不抽帧的。

### 4.5.1 必读

```
${PPT_MASTER}/references/game-asset-collector.md
```

### 4.5.2 抽帧覆盖率

| 题材 | 最少款数 | 推荐款数 | 必覆盖维度 |
|---|---|---|---|
| 单机循环经营 | 3 款 | **5 款** | 核心循环 / 美术 / 商业化 |
| 竖屏塔防 | 3 款 | **5 款** | 单波次 / 兵种树 / 升级路径 |
| 工厂链 | 4 款 | 6 款 | 资源链 / UI 密度 / 自动化 / 末期复杂度 |

### 4.5.3 命令

```bash
# 每款游戏跑一次（AI 按 §VIII 表自动生成）
python3 ${PPT_MASTER}/scripts/game_assets/fetch_game_assets.py "<game>" \
    --project projects/<项目名> \
    --steam-id <id?> --appstore-id <id?> --gplay-id <pkg?> \
    --max-videos 2 --label
```

### 4.5.4 i2i 风格化（可选 + 强力推荐）

```bash
# 把竞品截图风格化成本游戏的视觉基调
python3 ${PPT_MASTER}/scripts/game_assets/image_remix.py i2i ref.jpg \
    --prompt "..." --aspect 16:9 -o variant.jpg

# 多图 collage + 风格化
python3 ${PPT_MASTER}/scripts/game_assets/image_remix.py remix r1.jpg r2.jpg r3.jpg \
    --prompt "..." --layout hstrip --aspect 21:9 -o hero.jpg
```

### 4.5.5 输出契约

抽完后 AI **必须**把每款游戏的 `image_resource_list.md` 拼到 `design_spec.md §VIII`，
并填 **"为什么用这张"** 的 Notes 字段。

---

## Step 5: Image_Generator 🎨 美术生立绘（条件触发）

🚧 **GATE**: Step 4.5 complete; design_spec §VII "AI generation list" 不为空。

→ 100% 复用 `${PPT_MASTER}/SKILL.md` Step 5。

> 本 skill 推荐用法：
> - 5 张以内：NPC 立绘（核心循环主角 + 反派 + 商人 + 玩家化身 + 引导）
> - 3-5 张：章节背景（Strategist / 玩法循环 / 商业化 / 节奏 / 总结）
> - 2-3 张：主视觉 hero 图（Step 6 封面 / 章节切换页用）

---

## Step 6: Executor 🎬 导演拍摄

🚧 **GATE**: Step 4 (+ 4.5 + 5 if 触发) complete.

→ 100% 复用 `${PPT_MASTER}/SKILL.md` Step 6 + 8 条 Global Execution Discipline。

### 本 skill 强化点

1. **风格选择**：默认 `executor-general.md`（循环游戏适合活泼自由风），
   除非用户明确指定咨询风。
2. **Page-by-page 节律**：严格遵循 ppt-master 的 "SEQUENTIAL PAGE GENERATION ONLY"，
   不分 batch（除非用户明确说"分批跑"）。
3. **encoding safety**：**必须**用 Python heredoc + `write_bytes(content.encode("utf-8"))`，
   绝不能用 Cursor `Write` 工具写 SVG（含中文 / `·` / 中文标点）。
4. **每页生成后立即** `validate_svg_output.py <project_path>`，0 失败才继续。

### 章节标记（电影组术语）

在 SVG 注释里加 `<!-- 镜头 N -->` 标记：

```svg
<!-- 镜头 12 / 章节 III "玩法循环" / 镜头方向：从主循环→分支系统 -->
<svg ...>
```

---

## Step 7: Post + Export ✂️ 剪辑 + 🎟️ 放映

🚧 **GATE**: Step 6 complete; svg_output 全 PASS validate.

→ 100% 复用 `${PPT_MASTER}/SKILL.md` Step 7（4 个子步骤一个一个跑）。

### 本 skill 加：速通完成报告（强制）

跑完 Step 7.3 后，AI **必须** 立即输出报告（模板见 `${SKILL_DIR}/references/conversation-style.md` §1.3）：

```markdown
## ✅ 速通完成报告

| 项目 | 数据 |
|---|---|
| 总页数 | XX / XX |
| validate_svg_output | 100% PASS |
| finalize_svg | 0 WARN / 0 FAIL |
| 讲稿字数 | XX,XXX 字（平均 ~XXX 字/页） |
| PPTX 双版本 | Native XX MB + SVG XX MB |
| 用时 | ~XX 分钟 |

### 反思
1. ……（1-3 条，可选）
```

---

## 速查：每步触发条件总表

| Step | 触发 | 跳过 |
|---|---|---|
| 1 | 源材料非 markdown | 已是 md / 用户口述 |
| 2 | 永远触发 | 永不跳过 |
| 3 | 永远触发（默认 B） | 永不跳过 |
| 4 | 永远触发 | 永不跳过 |
| **4.5** | **本 skill 100% 触发** | **本 skill 不允许跳过** |
| 5 | design_spec §VII 非空 | §VII 全部用 _game_assets/ |
| 6 | 永远触发 | 永不跳过 |
| 7 | 永远触发 | 永不跳过 |

---

## 与 ppt-master Discipline 的关系

本 workflow **额外执行** SKILL.md 中的 11 条纪律：
- 1-8 条：100% 继承 ppt-master
- 9 条：SRD 表强制
- 10 条：抽帧覆盖率 ≥3 款
- 11 条：速通报告强制

详见 `${SKILL_DIR}/SKILL.md` § 强制纪律。
