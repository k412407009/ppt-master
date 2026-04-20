# ⚠️ Review scripts 正在迁移至独立 skill `game-review`

**日期**: 2026-04-21
**决策**: 把 review 功能从 `ppt-master` 拆出来, 变成独立的 [`game-review`](../../../../../game-review/README.md) skill。

## 当前状态

| 脚本 | 本目录 (旧) | `game-review/skills/game-review/scripts/review/` (新) |
| --- | --- | --- |
| `generate_review.py` | ✅ 仍工作 (E/H/I 依赖) | ✅ 增强版: `--mode` / `--with-visuals` |
| `build_summary.py` | ✅ 仍工作 | ✅ 镜像 (未改) |
| `add_visual_sheet.py` | ❌ 从未存在 (之前是 Last-Beacon-Survival 私有脚本) | ✅ 通用化后的正式入口 |
| `__init__.py` | ✅ | — |

## 为什么拆

- ppt-master 的本职是 "生成 PPT", review 只是它的收尾
- 外部游戏评审 (不生成 PPT) 用这套脚本时, 导入 ppt-master 全家桶过重
- 未来 CLI / Web 化需要独立的干净代码库 (见 `丁亮的个人助手/丁开心的游戏观察/external-game-reviews/website_roadmap.md`)

## 对 E / H / I 内部项目的影响

**短期 (本季度): 无影响**
- 旧脚本保留兼容, 继续用 `ppt-master/skills/ppt-master/scripts/review/generate_review.py <project>`
- 旧的 7 维度 charter (`../references/review-board.md`) 保持不变

**中期 (下次 D/E/F 项目立项时)**
- 建议直接用新 skill: `game-review/skills/game-review/scripts/review/generate_review.py <project> --mode internal-ppt`
- 行为一致, 仅路径不同

**长期**
- 本目录未来可能被删除 (当所有在产项目都迁移到 game-review skill 后)

## 如果你要改 review 逻辑

请改 **新 skill** (`f:/Git/game-review/skills/game-review/scripts/review/`), **不要** 改本目录, 避免两边分叉。本目录的 3 个脚本在 2026-04-21 之后应视为"只读归档"。

如果必须改本目录 (例如紧急修 E 项目的 review 生成 bug), 记得 **同步改到新 skill**, 或者直接删掉本目录里的脚本, 改为软引用到新 skill。

## 交叉索引

- 新 skill 门面: [`game-review/skills/game-review/SKILL.md`](../../../../../game-review/skills/game-review/SKILL.md)
- 新 skill charter: [`game-review/skills/game-review/references/review-board.md`](../../../../../game-review/skills/game-review/references/review-board.md)
- 产品化路线图: [`丁亮的个人助手/丁开心的游戏观察/external-game-reviews/website_roadmap.md`](../../../../../丁亮的个人助手/丁开心的游戏观察/external-game-reviews/website_roadmap.md)
