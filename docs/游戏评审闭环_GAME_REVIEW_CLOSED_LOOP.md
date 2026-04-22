# 游戏评审闭环_GAME_REVIEW_CLOSED_LOOP

## 这份文档是干什么的

这不是一份单独的脚本说明，而是把 `game-ppt-master`、`game-asset-collector` 和 `game-review` 三个仓库之间的协作边界、输入输出和复现要求固化下来。

适用两类场景：

1. **内部立项 PPT 闭环**：从源材料生成 PPT，再做 Step 8 评委会评审，产出标准化报告。
2. **外部游戏评审闭环**：先抓商店页和 gameplay 证据，再生成结构化 `review.json`，最后落成 Word / Excel / Markdown 报告。

---

## 三个仓库各自负责什么

### `game-ppt-master`

负责上游制作和素材准备：

- 源材料转 Markdown
- 设计规格与大纲
- PPT 原生编辑页生成
- 调用共享采集器并消费素材结果

核心入口：

- [`skills/ppt-master/SKILL.md`](../skills/ppt-master/SKILL.md)
- [`docs/三仓协同架构_THREE_REPO_STACK.md`](./三仓协同架构_THREE_REPO_STACK.md)

### `game-asset-collector`

负责共享素材层：

- 商店截图抓取
- gameplay 视频下载与抽帧
- 标签与中文描述生成
- 统一 `raw_assets` 结构

核心入口：

- [../../game-asset-collector/README.md](../../game-asset-collector/README.md)
- [../../game-asset-collector/scripts/fetch_game_assets.py](../../game-asset-collector/scripts/fetch_game_assets.py)

### `game-review`

负责下游结构化评审和文档产出：

- 5 位评委 × 7 维度的 `review.json`
- `.docx` 评审报告
- `.xlsx` 执行清单 / 评分表 / 视觉索引
- `.md` 主观问题最优解

核心入口：

- [../../game-review/README.md](../../game-review/README.md)
- [../../game-review/skills/game-review/SKILL.md](../../game-review/skills/game-review/SKILL.md)

---

## 完整闭环

### 场景 A：内部立项 PPT 评审

```text
源材料
  -> game-ppt-master Step 1-7
  -> 导出 PPTX
  -> 评委会讨论并填写 review.json
  -> game-review 生成 docx/xlsx/md
```

关键文件：

- `<project>/design_spec.md`
- `<project>/exports/*.pptx`
- `<project>/review/<project>_review.json`

### 场景 B：外部游戏评审

```text
游戏名 / 商店包名 / 商店 URL / 视频 URL
  -> game-asset-collector fetch_game_assets
  -> raw_assets + labels.json + descriptions.json + metadata.json
  -> AI / 人工补全 review.json
  -> game-review --mode external-game --with-visuals
  -> docx/xlsx/md
```

关键目录：

- `<project>/raw_assets/<game>/store/...`
- `<project>/raw_assets/<game>/gameplay/frames/...`
- `<project>/raw_assets/<game>/gameplay/labels.json`
- `<project>/raw_assets/<game>/gameplay/descriptions.json`
- `<project>/raw_assets/<game>/metadata.json`

---

## 推荐执行方式

### 1. 先收素材

```bash
python3 ../game-asset-collector/scripts/fetch_game_assets.py "<game name>" \
  --project <project_path> \
  --gplay-id <google_play_package?> \
  --appstore-id <app_store_id?> \
  --steam-id <steam_app_id?> \
  --max-videos 2 \
  --label
```

如果自动视频搜索抓错，直接改用手动视频入口：

```bash
python3 ../game-asset-collector/scripts/fetch_game_assets.py "<game name>" \
  --project <project_path> \
  --video https://www.youtube.com/watch?v=<id> \
  --video <bilibili_BV_id> \
  --label
```

### 2. 再生成报告

```bash
game-review review <project_dir> --mode external-game --with-visuals
```

或旧接口：

```bash
python skills/game-review/scripts/review/generate_review.py <project_dir> \
  --mode external-game --with-visuals
```

---

## 当前已经沉淀下来的能力

### 文本与商店页

- Google Play 抓取支持官方包名路径，优先用 `--gplay-id`
- App Store 抓取支持 `--appstore-id`
- 当只有游戏名时，App Store 搜索现在走**严格候选筛选**
  - 命中不够确定时，**宁可跳过，不再误抓第一个结果**
  - 这能避免 `Last Beacon Survival -> Last Fortress: Underground` 这种误命中

### 视频与画面理解

- 支持 YouTube / Bilibili 手动视频入口 `--video`
- 支持 `ffmpeg` 抽帧 + pHash 去重
- 支持 ARK/Doubao Vision 统一输出：
  - `labels.json`
  - `descriptions.json`

### 报告与视觉索引

- `game-review` 的 Excel 视觉索引支持读取 `descriptions.json`
- 如果 `review.json` 里有 `V1/V2/...`，但原图丢失，表格会保留行并显示 `(图源缺失)`
- 这让“文字层可复现”和“视觉层是否完整”能被明确区分

---

## 复现一致性的关键前提

如果你要复现历史外部游戏评审，不要只保存最终产物：

- 只留 `docx/xlsx/md`：只能复现文字结论
- 保留完整 `raw_assets`：才能复现视觉索引和图片证据

最小保留集：

- `store/`
- `gameplay/frames/`
- `gameplay/labels.json`
- `gameplay/descriptions.json`
- `metadata.json`

---

## 交接给别人时最重要的三条

1. **素材收集和报告生成是两段式流程**，不要把它们混成一个黑箱。
2. **App Store / Google Play / 视频 URL 尽量给精确 ID 或精确 URL**，不要只给模糊游戏名。
3. **`raw_assets` 必须跟报告一起保存**，否则未来只能复现文字，复现不了视觉证据。
