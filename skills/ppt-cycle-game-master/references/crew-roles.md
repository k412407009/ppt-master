# Crew Roles — 电影组角色映射

> 6 个电影组角色 ↔ ppt-master 6 个底层角色的精确映射。
> AI 在切换角色时必须**先** read 本文件对应的 § + ppt-master 的对应 reference。
>
> `${PPT_MASTER}` = `skills/ppt-master/`

---

## 角色总表

| # | 电影组 | ppt-master 底层 | 主要产物 | ppt-master reference |
|---|---|---|---|---|
| 1 | 📝 编剧 Screenwriter | Strategist | `design_spec.md` | `${PPT_MASTER}/references/strategist.md` |
| 2 | 🎬 导演 Director | Executor | `svg_output/*.svg` | `${PPT_MASTER}/references/executor-base.md` + 风格 |
| 3 | 🎨 美术 Art Director | Image_Generator | `images/_gen/`, `images/_remix/` | `${PPT_MASTER}/references/image-generator.md` |
| 4 | 📷 摄影 DOP | Game_Asset_Collector | `images/_game_assets/` | `${PPT_MASTER}/references/game-asset-collector.md` |
| 5 | ✂️ 剪辑 Editor | Post-processor | `svg_final/`, `notes/*.md` | `${PPT_MASTER}/SKILL.md` Step 7 |
| 6 | 🎟️ 制片 Producer | Project_Manager + Exporter | 项目目录 + `exports/*.pptx` | `${PPT_MASTER}/SKILL.md` Step 2 + Step 7.3 |

---

## §1 📝 编剧 Screenwriter (Strategist)

### 职责
1. 读源材料（GDD / 竞品分析 / 微信对话）
2. 主导**八问八答**（电影组语言）
3. 主导 **SRD 表**（5.1-5.7 七档）
4. 输出 `design_spec.md`（11 节，I-XI）
5. 维护 §VIII Image Resource List（与摄影协作）

### 工作模式
- 用户决策 → 编剧落 design_spec → 摄影抽帧 → 美术生立绘 → 导演开拍
- **不直接写 SVG**（那是导演的事）
- **不直接抽帧**（那是摄影的事）

### 关键产物
```
projects/<项目名>/design_spec.md
├─ I.   Project Overview
├─ II.  Audience & Goal
├─ III. Style Spec (color/font/icon)
├─ IV.  Page Layout Plan
├─ V.   Core Loop + SRD Table  ← 本 skill 强化重点
├─ VI.  Reference Game Matrix  ← 本 skill 强化重点
├─ VII. AI Generation List
├─ VIII.Image Resource List   ← 摄影抽帧后回填
├─ IX.  Speaker Notes Skeleton
├─ X.   Risk & Open Questions
└─ XI.  Approval Sign-off
```

### 必读
- `${SKILL_DIR}/references/conversation-style.md`（**必读**）
- `${SKILL_DIR}/references/srd-density-checklist.md`
- `${PPT_MASTER}/references/strategist.md`
- `${PPT_MASTER}/templates/design_spec_reference.md`

---

## §2 🎬 导演 Director (Executor)

### 职责
1. 按 design_spec 顺序拍每一页（**page by page**，不分 batch）
2. 镜头语言 = SVG 视觉锚点 + 转场 + 节奏
3. 在 SVG 注释里加镜头编号（`<!-- 镜头 N -->`）
4. 每页生成立即 `validate_svg_output.py` 自检
5. 章节切换页用 hero 图（美术提供）

### 工作模式
- 上一页确认 PASS 才拍下一页
- **绝不**用 Cursor `Write` 工具写 SVG（含中文/`·`/中文标点）
- **必须**用 Python heredoc + `write_bytes(content.encode("utf-8"))`
- 每 4-5 页 batch 跑一次 `validate_svg_output.py`

### 关键产物
```
projects/<项目名>/svg_output/
├─ 01_封面.svg
├─ 02_<page-name>.svg
├─ ...
└─ NN_总结.svg
```

### 必读
- `${PPT_MASTER}/references/executor-base.md`（**必读**）
- 风格三选一：
  - `${PPT_MASTER}/references/executor-general.md`（活泼自由 ★ 推荐）
  - `${PPT_MASTER}/references/executor-consultant.md`（咨询）
  - `${PPT_MASTER}/references/executor-consultant-top.md`（MBB 顶级咨询）
- `${PPT_MASTER}/references/shared-standards.md` §0（encoding safety）
- `${PPT_MASTER}/docs/lessons/cursor-write-latin1-bug.md`（避免 Latin-1 bug）

---

## §3 🎨 美术 Art Director (Image_Generator)

### 职责
1. 看 design_spec §VII "AI Generation List"
2. 写 prompt 文档 → `images/image_prompts.md`
3. 用 `image_gen.py` 生成 t2i 立绘 → `images/_gen/`
4. 用 `image_remix.py` i2i 风格化竞品截图 → `images/_remix/`
5. （可选）`image_remix.py collage` 拼贴多图

### 工作模式
- 需要"原创视觉锚点"时用 t2i（NPC 立绘 / 章节背景 / hero）
- 需要"参考竞品"时用 i2i（把竞品截图风格化成本游戏调性）
- **每张图必须在 image_prompts.md 留下 prompt + 参数**（用于复盘）

### 关键产物
```
projects/<项目名>/images/
├─ _gen/                  ← t2i 原创立绘
├─ _remix/                ← i2i 风格化（竞品 → 本游戏调性）
├─ _game_assets/<game>/   ← 摄影组采集（不是美术）
└─ image_prompts.md       ← 所有 prompt 留底
```

### 必读
- `${PPT_MASTER}/references/image-generator.md`（**必读**）
- `${PPT_MASTER}/scripts/game_assets/README.md`（image_remix 用法）

---

## §4 📷 摄影 DOP (Game_Asset_Collector)

### 职责
1. 按 design_spec §VI "Reference Game Matrix" 跑 `fetch_game_assets.py`
2. 抽商店截图（App / Google / Steam，Tavily fallback）
3. 抽视频帧（yt-dlp + ffmpeg + pHash dedup）
4. 智能打标（豆包 Vision 12 类场景 + smart-quota 提前停）
5. 输出 `image_resource_list.md` → 回填给编剧拼到 §VIII

### 工作模式
- **本 skill 触发率 100%**（单循环/塔防立项必抽帧）
- 每款游戏跑 1 次 `fetch_game_assets.py`
- 抽完后用 `analyze_images.py` 检查比例分布
- **AI 永远不直接打开图片**，只看 `labels.json` / `image_resource_list.md`

### 关键产物
```
projects/<项目名>/images/_game_assets/<game>/
├─ frames/                ← 视频抽帧
├─ store/appstore/        ← App Store 截图
├─ store/googleplay/      ← Google Play 截图
├─ store/steam/           ← Steam 截图
├─ labels.json            ← Doubao Vision 12 类标注
└─ metadata.json          ← 游戏元信息

projects/<项目名>/images/_game_assets_meta/
└─ <game>.image_resource_list.md  ← 粘贴到 design_spec §VIII
```

### 必读
- `${PPT_MASTER}/references/game-asset-collector.md`（**必读**）
- `${PPT_MASTER}/scripts/game_assets/README.md`

### 工具速查
```bash
# 单款游戏完整采集
python3 ${PPT_MASTER}/scripts/game_assets/fetch_game_assets.py "<game>" \
    --project projects/<项目名> \
    --steam-id <id?> --appstore-id <id?> --gplay-id <pkg?> \
    --max-videos 2 --label

# 仅商店截图（不抽视频）
python3 ${PPT_MASTER}/scripts/game_assets/fetch_game_assets.py "<game>" \
    --project projects/<项目名> --store-only
```

---

## §5 ✂️ 剪辑 Editor (Post-processor)

### 职责
1. 跑 `validate_svg_output.py`（最后一道闸）
2. 跑 `total_md_split.py`（讲稿切分）
3. 跑 `finalize_svg.py`（icon 嵌入 / 图片 base64 / 文字 flatten / 圆角 path）
4. 跑 `svg_to_pptx.py -s final`（双版本 PPTX）
5. 出**速通完成报告**（强制）

### 工作模式
- 4 个子步骤**必须分开跑**，绝不能合并到一个 shell 命令
- 每步 PASS 才进下一步
- 完成后立即给报告

### 关键产物
```
projects/<项目名>/
├─ svg_final/             ← finalize 后的 SVG（即将出 PPTX）
├─ notes/                 ← 切分后的讲稿
│   ├─ total.md
│   ├─ 01_封面.md
│   └─ ...
└─ exports/
    ├─ <项目名>_<ts>.pptx       ← Native DrawingML
    └─ <项目名>_<ts>_svg.pptx   ← SVG 嵌入版（Office 2019+）
```

### 必读
- `${PPT_MASTER}/SKILL.md` Step 7（**必读**）

---

## §6 🎟️ 制片 Producer (Project_Manager + Exporter)

### 职责
1. **项目立项**：跑 `project_manager.py init`，建目录结构
2. **依赖管理**：检查 requirements.txt 是否齐全
3. **AGENT_PROMPT 复制**：把本 skill 模板 cp 到项目目录
4. **导出双版本 PPTX**（实际命令由剪辑跑，制片确认验收）
5. **git 同步**：项目产物按 `.gitignore` 走云盘同步，**不入仓库**

### 工作模式
- 项目立项后**不参与具体创作**，只在每个里程碑确认验收
- 验收 checklist 见本 skill 的 SKILL.md "完成判定"

### 关键产物
```
projects/<项目名>/
├─ AGENT_PROMPT.md            ← 制片立项时复制
├─ sources/                   ← 源材料归档
├─ design_spec.md             ← 编剧产出（验收）
├─ images/                    ← 摄影 + 美术产出（验收）
├─ svg_output/                ← 导演产出（验收）
├─ svg_final/                 ← 剪辑产出
├─ notes/                     ← 剪辑产出
├─ exports/                   ← 剪辑 + 制片产出（验收）
└─ <gitignored, 走云盘同步>
```

### 必读
- `${PPT_MASTER}/SKILL.md` Step 2 + Step 7.3
- 本 skill 的 `AGENT_PROMPT_template.md`

---

## 角色切换协议

每次切换角色，AI 必须输出：

```markdown
## [Crew Switch: 🎬 导演 Director (Executor)]
📖 Reading: ${SKILL_DIR}/references/crew-roles.md §2
📖 Reading: ${PPT_MASTER}/references/executor-base.md
📖 Reading: ${PPT_MASTER}/references/executor-general.md
📋 当前任务：开始拍 SLIDE 02-05
```

> 与 ppt-master 的 "Role Switching Protocol" 完全一致，只是角色名换了别名。
