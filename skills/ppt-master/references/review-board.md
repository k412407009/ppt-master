# Review Board — Step 8 二次确认评审 (PPT 完工后专用)

> ⚠️ **迁移提示 (2026-04-21)**: 本 charter 已独立成 `game-review` skill, 源头版本是
> [`game-review/skills/game-review/references/review-board.md`](../../../../../game-review/skills/game-review/references/review-board.md),
> 本文件仅作 ppt-master 内部 Step 8 引用的历史副本, 修改请改 game-review 那份并同步回来。
> 外部游戏评审新项目直接用 [`game-review` skill](../../../../../game-review/README.md)。

> 此 spec 定义 PPT 导出完成后的"评委会评审"阶段, 是 ppt-master skill 的 Step 8 (Post-export review)。
> 触发条件: 用户在 PPTX 导出后明确要"找评委会评一遍"或"二次确认评审"。
> 输出: 每个项目 3 件套 (`.docx` + `.xlsx` + `subjective_responses.md`) + 1 份跨项目汇总 `review-summary.md`。

---

## I. 评委会人物卡 (5 人, 固定)

| 代号 | 角色 | 工龄 | 背景 | 评审视角 |
|---|---|---|---|---|
| **P** | 资深制作人 | 15 年 | 主导过 3 款放置/SLG 上线 (其中 1 款全球流水 8 位数), 现任研发负责人 | **立项可行性** + **整体节奏** + **商业终局** |
| **S1** | 战略专家 · 题材策略 | 12 年 | 用户研究 + 题材立项咨询出身, 服务过腾讯/网易/米哈游 | **题材匹配度** + **用户画像** + **题材风险/合规** + **赛道竞品** |
| **S2** | 战略专家 · 玩法系统 | 10 年 | 系统策划 + 核心循环设计, 主刀过 2 款月活千万级放置游戏 | **核心循环可行性** + **数值边界** + **玩法粘性** + **长留存设计** |
| **O1** | 运营 · 用户运营 / LTV | 6 年 | 大 R 玩家维护 + 留存优化 | **留存钩子密度** + **付费节点合理性** + **情感链接** + **新手 7 日转化** |
| **O2** | 运营 · 投放 / CPM | 8 年 | TA / Tencent Ads / FB Ads 跨平台投放 | **投放素材兼容度** + **CPM 预算可承担性** + **题材变现天花板** + **品类用户重叠** |

> 历史 (2026-04-20 前) 评委 P 视角含 "团队/排期/预算", 并设有 D8 (团队/排期/预算) 与 D9 (PPT 表达力) 两个维度。因为这两维对外部上线产品结构性失效 (见 external-game-reviews/MVP_A_reflection.md §2.1), 也对内部立项评审意义不大 (预算和 PPT 表达力是流程问题不是产品问题), 2026-04-20 T3 正式从评委会 charter 移除。

---

## II. 评审维度 (7 项 · 每项 1–5 分)

| 维度 ID | 名称 | 主问 |
|---|---|---|
| **D1** | 战略 - 题材匹配度 | S1 主, P 副 |
| **D2** | 玩法 - 核心循环 | S2 主, P 副 |
| **D3** | 玩法 - 时间节点 (5min/15min/30min/1h/2h/4h/Day1→Day2) | S2 主, O1 副 |
| **D4** | 玩法 - 阶段过渡 (放置→沉浸→指挥→外扩) | S2 + P 主 |
| **D5** | 商业化 - 付费/留存 | O1 主, P 副 |
| **D6** | 风险 - 题材/合规 | S1 主, P 副 |
| **D7** | 美术/配色/素材 | P 主, S1 副 |

**打分规则**: 1=灾难 / 2=严重不足 / 3=可接受需补 / 4=优秀 / 5=拔尖

---

## III. 问题分类与处理

每个评委问 **3–6 个问题**, 共 **15–30 个问题/项目**。每个问题有两个属性:

### 属性 1: 客观/主观

- **O (Objective)** — 有明确的改动建议, 在 PPT/文档/数值上可执行
  → 必须给出: 改动位置 (页号/章节) + 改动建议 + 优先级
- **S (Subjective)** — 主观, 业内无统一答案
  → 必须给出: 评委倾向回答 + **当前 PPT 方案的最优解辩护理由** (帮策划/制作人在评委面前 hold 住)

### 属性 2: 优先级

| 优先级 | 含义 | 修订动作 |
|---|---|---|
| **P0** | 立项被否或评委一票否决高风险 | **PPT 终稿前必改** |
| **P1** | 不改会被严重 challenge, 但不至于否决 | **下一次评审前补** |
| **P2** | nice-to-have / 加分项 | **下版迭代再说** |

---

## IV. 输出物规范

每个项目的 `review/` 目录下产出 3 件套:

### 1. `<project>_review.docx` (评审报告 · 给评委 + 制作人)

```
封面: 项目名 / 评委会 5 人 / 评审日期 / 整体打分 / 一句话裁决
执行摘要: 7 维度雷达图描述 + 高低分维度 + 3 大风险 + 3 大亮点
逐评委意见: 每位评委一节, 含评分表 + 3-6 个问题 + 改动建议
修订总览 (Action Items): 按 P0/P1/P2 分组, 列出具体修订条目
最终裁决: 通过 / 有条件通过 / 不通过 + 复审节点
```

### 2. `<project>_review.xlsx` (问题清单 · 给执行)

3 个 sheet:

- **`Issues`** — 每行 1 个问题, 共 **12 列**: 前 9 列是评审产出 (只读), 后 3 列是**用户决策 (可填)**:

  | 列 | 字段 | 说明 |
  |---|---|---|
  | A | ID | Q01-Q18 |
  | B | 评委 | 全名 + 工龄 (如 "资深制作人 (15年)") |
  | C | 维度 | D1-D7 全名 |
  | D | 类型 | 客观 / 主观 |
  | E | 优先级 | P0/P1/P2 (彩色单元格) |
  | F | 页号/影响 | Slide 号 |
  | G | 问题 | 评委原话 |
  | H | 改动建议/最优解 | O 类含 suggestion; S 类含 [评委倾向] + [最优解] |
  | I | 答辩话术 | S 类 talking_points |
  | **J** | **要不要改** | **三选一下拉: 改 / 待定 / 不改. 默认待定 (黄)** |
  | **K** | **我要做什么** | **行动目标 (What). 留空=按评委原方案; 填=覆盖评委目标** |
  | **L** | **怎么做** | **具体步骤 (How). 留空=AI 按 K 自动推导; 填=严格按此实施** |

  J 列带**数据验证**(强制下拉)+ **条件格式**(改=绿/待定=黄/不改=灰)+ 表头批注。
  K/L 两列用于驱动 skill 自动化改 PPT, 见 §VIII。

- **`Scores`** — 5 评委 × 7 维度 打分矩阵 + 每维均分 + 每评委均分 + 整体加权总分
- **`Action_Items`** — O 类 issue 按 P0/P1/P2 分组, 含 owner / 预估工时

### 3. `<project>_subjective_responses.md` (主观问题最优解 · 给制作人)

仅含 S 类问题, 每条:
```
## Q-NN: <问题原文>
**评委**: <代号> · **维度**: <Dx> · **优先级**: <P0/P1/P2>
**评委倾向**: <评委自己的看法>
**最优解辩护**: <PPT 当前方案为什么也合理>
**口径建议**: <制作人答辩话术 1-3 句>
```

---

## V. 跨项目汇总: `review-summary.md` + `projects_comparison.xlsx`

放在 `<projects_root>/` 根目录 (即 `ppt-master/projects/` 或 `ppt-master-projects/` 根), 两个产物:

### V.1 `review-summary.md` (人看)
- 总体裁决对照表 (项目 × 加权总分 × verdict × 复审节点)
- 7 维度评分纵向对比 (7 行 × N 项目列)
- 共性问题 (≥2 项目都中招的低分维度) → 提到 skill 层迭代
- 各项目 P0 必改清单
- 推荐推进顺序 (按 verdict rank + 分数排)
- ppt-master skill 层改进建议

### V.2 `projects_comparison.xlsx` (机器看 · 可排序筛选)
4 个 sheet:
- **Overview**: 每项目 1 行, 列 = 项目 / 加权总分 / verdict / P0/P1/P2 数 / Run 排级 / 下一步
- **Scores_Matrix**: 7 维度 × N 项目 打分矩阵 + 低分/高分标记
- **All_Issues**: 所有项目的全部 issue 摊平成一张大表 (N×18 行), 带项目列, 可按优先级/维度/评委筛选
- **P0_Cross_Project**: 仅 P0 issue 的跨项目聚合视图 (方便一眼看到"本轮必改的全部项")

---

## VI. 工具链

| 工具 | 用途 |
|---|---|
| `python skills/ppt-master/scripts/review/generate_review.py <project_dir>` | 读 `review/<project>_review.json` → 生成 docx + xlsx (12 列) + subjective_responses.md |
| `python skills/ppt-master/scripts/review/build_summary.py <projects_root>` | 读多个项目的 `<project>_review.json` → 生成 review-summary.md + projects_comparison.xlsx |

### `<project>_review.json` Schema

```json
{
  "project": "E_TCG卡店帝国",
  "verdict": "conditional_pass",
  "weighted_score": 4.05,
  "review_date": "2026-04-20",
  "reviewers": [
    {"id": "P", "name": "资深制作人", "years": 15, "background": "...", "perspective": "..."},
    {"id": "S1", "name": "战略专家·题材", ...}
  ],
  "scores": {
    "P":  {"D1":4, "D2":4, "D3":5, "D4":4, "D5":3, "D6":4, "D7":4},
    "S1": {...}, "S2": {...}, "O1": {...}, "O2": {...}
  },
  "highlights": [
    "封面闪卡金 + Pokemart 暖色配色高级",
    "Slide 11 头 30min 8 钩子密集, 抗早期流失设计扎实"
  ],
  "risks": [
    "Slide 22 节奏曲线峰值过密, 第 2 周可能审美疲劳",
    "L5 PVE-SLG 三阶段商业进阶 ROI 模型缺乏一手数据支撑"
  ],
  "issues": [
    {
      "id": "Q01",
      "reviewer": "P",
      "dimension": "D2",
      "type": "O",
      "priority": "P1",
      "page": "Slide 13",
      "question": "升级店面图 45° 俯视角好看, 但实际 mobile 玩家在小屏看清楚吗?",
      "suggestion": "加一张同视角的 mobile 全屏截图对照, 证明 UI 可读"
    },
    {
      "id": "Q07",
      "reviewer": "S1",
      "dimension": "D6",
      "type": "S",
      "priority": "P1",
      "page": "Slide 27",
      "question": "TCG 题材在国内审批合规上有没有未抽到稀有卡 = 赌博的争议?",
      "subjective_position": "我个人认为这是潜在 P0 风险, 应在 Slide 27 单开半页讨论",
      "best_answer": "TCG Card Shop Sim 的'抽包'是模拟经营, 玩家本人不是 gambler 而是店主, 法律定性更接近放置经营, 不触发 G 类版号。但需准备版号沟通文档作为附件",
      "talking_points": [
        "对标 Steam 上 TCG Card Shop Sim 已上架 PRC 版无问题",
        "我们的玩家身份是店主, 卖卡 ≠ 抽卡赌博",
        "已咨询合规团队, 准备好版号沟通材料"
      ]
    }
  ]
}
```

---

## VII. 评审流程 (走完 1 个项目)

1. **读源材料**: `design_spec.md` (Part 5 重点), `<project>.md` (源文档), exports 下的 PPTX 文件名
2. **写 JSON**: 按 §VI Schema 填 `<project_root>/review/<project>_review.json`
3. **跑脚本**: `python skills/ppt-master/scripts/review/generate_review.py <project_root>` → 自动产 3 件套
4. **可选 verify**: 用 PowerPoint / WPS 打开 `<project>_review.docx` 看排版
5. **汇总**: 所有项目都跑完后, `python skills/ppt-master/scripts/review/build_summary.py projects/` → `review-summary.md` + `projects_comparison.xlsx`

---

## VIII. 决策驱动改 PPT 闭环

Step 8 评审结束后, 策划/制作人在 `review/<project>_review.xlsx` Issues sheet 的 J/K/L 三列填决策, 触发后续 skill 自动化改 PPT:

### VIII.1 三列决策的语义

| 列 | 字段 | 语义 | 留空行为 |
|---|---|---|---|
| J | 要不要改 | **是否本轮执行** (改 / 待定 / 不改) | 默认 "待定", 不改 PPT |
| K | 我要做什么 | **行动目标** (What), 一句话的结果描述 | 沿用评委 `suggestion` / `best_answer` |
| L | 怎么做 | **具体步骤** (How), 拆到可执行粒度 | AI 按 K 推导具体步骤 |

### VIII.2 三列的组合处理规则

| J | K | L | skill 行为 |
|---|---|---|---|
| 待定/不改 | * | * | **跳过** |
| 改 | 空 | 空 | 按评委原 `suggestion`/`best_answer` 自动改 SVG |
| 改 | 填 | 空 | 用 K 覆盖目标, AI 自动推导步骤改 SVG |
| 改 | 填 | 填 | 严格按 L 的步骤改 SVG, 不再推导 |
| 改 | 空 | 填 | 警告 (缺目标只有步骤通常是不一致的) + 按 L 执行 |

### VIII.3 执行工具链 (主 agent)

1. 读 xlsx Issues sheet, 过滤 J="改" 的行
2. 按上表规则, 把每条 issue 翻译成一份 **改动单 markdown** (issue ID → 目标 → 步骤 → 影响 svg 列表)
3. 按改动单逐项修改 `svg_final/*.svg` (主 agent 做, **不能委派 sub-agent**, 见 AGENTS.md)
4. 改完重跑 `scripts/svg_to_pptx.py` 重新打包 pptx
5. 在 `review/` 下追加一份 `<project>_revision_log_<timestamp>.md`, 记录本轮改了哪些 issue / 哪些 svg / 产出哪个 pptx

### VIII.4 自检

每次执行前必须:
- 读一遍 xlsx (不要用缓存的 json), 因为用户可能在 Excel 里手改了打分或加了自己的文字
- 核对 issue ID 在 json 里还存在(避免 Excel 里手删了 ID 后续脚本崩)
- 备份当前 pptx 到 `exports/.backup_<timestamp>/`

---

## IX. 红线 / 注意

1. **不要凭空捏造数据**: 评委的所有"基准对比" (类如"对标某游戏 D1 留存 35%") 必须用 design_spec / 源文档里出现过的数据, 不能臆造
2. **主观问题必须有 best_answer**: 不能只列问题不给答案, 那是甩锅
3. **每个评委 3-6 问, 不少于 15 / 不超过 30**: 太少就不严肃, 太多评审会变成走过场
4. **打分要有差异**: 5 个评委 × 7 维度 = 35 个格子, 全 4 分或全 5 分等于没评; 应该有 1-2 个 2 分或 3 分体现真实争议
5. **verdict 三选一**: `pass` / `conditional_pass` / `not_pass`, 没有"通过但需要重做"这种含糊词
6. **维度历史变更**: 2026-04-20 T3 将 D8 (团队/排期/预算) 与 D9 (PPT 表达力) 从 charter 移除, 现仅评 D1-D7。历史 review.json 里保留的 D8/D9 分数和 issue 不再被脚本读取, 但向后兼容; 如需保留团队/预算讨论, 建议挪到 `design_spec.md` 的 Part 6 (交付计划) 或单独做 `delivery_plan.md`, 不再走评委会。
