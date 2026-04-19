# AGENT_PROMPT — `<项目名>` 立项 PPT

> **使用方法**：把本文件**复制**到新项目目录 `projects/<项目名>/AGENT_PROMPT.md`，
> 替换 `<...>` 占位符，然后在 Cursor 里贴 `@AGENT_PROMPT.md` 启动。
>
> 本模板配套 SKILL：`skills/ppt-cycle-game-master/`（电影组 / 单循环 / SRD 7 档）。

---

## 0. 项目元信息（必填）

| 字段 | 值 |
|---|---|
| 项目名 | `<例：J_像素工坊_Mindustry+Whiteout-Survival>` |
| 题材类型 | `<二选一> 单机循环经营 / 竖屏塔防+产业化` |
| 画布 | `<二选一> ppt169（横屏 1920×1080）/ xhs（竖屏 1080×1920）` |
| 参考游戏 | `<3-5 款>` |
| 目标页数 | `<例：24-32 页>` |
| 当前阶段 | `<例：S1 立项 / S2 Demo / S3 Pre-launch>` |
| 截止时间 | `<例：明天 9:00 评审会前>` |

---

## 1. SKILL 触发链（AI 必读，按顺序）

```
1. skills/ppt-cycle-game-master/SKILL.md                              ← 入口
2. skills/ppt-cycle-game-master/references/conversation-style.md      ← 对话风格 SOP（必读）
3. skills/ppt-cycle-game-master/references/workflow.md                ← 7 步工作流
4. skills/ppt-cycle-game-master/references/crew-roles.md              ← 6 角色映射
5. skills/ppt-cycle-game-master/references/srd-density-checklist.md   ← SRD 7 档清单
6. 按题材二选一：
   ├─ 单机循环经营 → skills/ppt-cycle-game-master/references/cycle-game-pitch-pack.md
   └─ 竖屏塔防     → skills/ppt-cycle-game-master/references/vertical-tower-defense-pack.md
7. skills/ppt-master/SKILL.md                                         ← 底层 7 步流水线
```

---

## 2. 八问八答（电影组语言版）

> 见 `skills/ppt-cycle-game-master/templates/eight_questions.md` 完整问题集。
> AI 在 Step 4 必须**先问完这 8 题**才能进入 design_spec 编写。
> 用户回复支持 `B1 c1 D1 E1` 这种紧凑格式（详见 `conversation-style.md` §1）。

```markdown
| # | 角色 | 问题 | 选项（默认值用 ★ 标） |
|---|---|---|---|
| 1 | 📝 编剧 | 核心循环一句话怎么说？ | A) 经营→升级→扩张 ★  B) 战斗→收集→进化  C) 自定义 |
| 2 | 🎬 导演 | 头 30 秒玩家看到什么？ | A) 立绘×1 + Tap 反馈 ★  B) 短动画 + Skip  C) 教学引导  D) 自定义 |
| 3 | 🎨 美术 | 风格基调？ | A) 暖+卡通  B) 冷+写实 ★  C) 暖冷对比  D) 单色高对比 |
| 4 | 📷 摄影 | 抽帧覆盖几款？ | A) 3 款  B) 5 款 ★  C) 7 款  D) 自定义 |
| 5 | ✂️ 剪辑 | SRD 哪几档必触发？ | A) 5.1-5.5 五档  B) 5.1-5.7 全七档 ★  C) 自定义 |
| 6 | 🎟️ 制片 | 商业化点？ | A) IAP-only  B) IAP+广告 ★  C) 订阅  D) 盒装+DLC |
| 7 | 🎬 试映 | 留存目标 D1/D7/D30？ | A) 50/25/10  B) 60/30/15 ★  C) 自定义 |
| 8 | 🎟️ 发行 | 目标市场？ | A) 国服  B) 海外  C) 双平台 ★  D) 国服优先海外跟进 |
```

---

## 3. SRD 节奏密度表（必填，design_spec §V）

> AI 必须在 Step 4 输出 design_spec 时**完整填出 7 档**。
> 模板见 `skills/ppt-cycle-game-master/templates/srd_table.md`。

```markdown
| 阶段 | 时长 | 玩家行为 | 必触钩子 | 留存目标 | 验收标准 |
|---|---|---|---|---|---|
| 5.1 | 0–30s    | <填> | <填> | 95% | <填> |
| 5.2 | 30s–2min | <填> | <填> | 80% | <填> |
| 5.3 | 2–15min  | <填> | <填> | 70% | <填> |
| 5.4 | 15–60min | <填> | <填> | 60% | <填> |
| 5.5 | 1–4h     | <填> | <填> | 50% | <填> |
| 5.6 | Day 2–3  | <填战斗/反派/高峰> | <填> | 40% | <填> |
| 5.7 | Day 5–30 | <填长期目标> | <填> | 20% | <填> |
```

> ⚠️ 反模式提醒（详见 `conversation-style.md` §3）：
> - 5.1 起步必须 ≤30s，**不能从 30min 起步**
> - 5.5 → 5.6 之间**不能跳过 Day 2-3**
> - 战斗/反派**不能晚于 Day 3**
> - 时间字段必须**显式带单位**

---

## 4. Step 4.5 抽帧清单（强制触发）

本 skill 默认 Step 4.5 触发率 = 100%。AI 必须按下表跑：

```markdown
| 游戏 | 维度 | Steam ID | AppStore ID | GooglePlay Pkg | 抽帧 max-videos |
|---|---|---|---|---|---|
| <参考1> | 核心循环 | <id> | <id> | <pkg> | 2 |
| <参考2> | 美术风格 | <id> | <id> | <pkg> | 2 |
| <参考3> | 商业化 | <id> | <id> | <pkg> | 2 |
| <参考4> | 系统耦合（可选） | <id> | <id> | <pkg> | 1 |
| <参考5> | 元层（可选） | <id> | <id> | <pkg> | 1 |
```

**执行命令**（每款游戏跑一次，AI 自己生成参数）:

```bash
python3 ${PPT_MASTER}/scripts/game_assets/fetch_game_assets.py "<game name>" \
    --project projects/<项目名> \
    --steam-id <id?> --appstore-id <id?> --gplay-id <pkg?> \
    --max-videos 2 --label
```

---

## 5. 完成判定（速通完成报告必含）

| 项 | 验收 | 检查方式 |
|---|---|---|
| SVG 100% PASS | `validate_svg_output.py` 0 ENCODING / 0 XML | 自动 |
| finalize 0 WARN | `finalize_svg.py` 0 missing icon / 0 missing image | 自动 |
| 讲稿字数 200-400/页 | `total_md_split.py` 切分后逐页统计 | 自动 |
| 双版本 PPTX | `<name>_<ts>.pptx`（Native）+ `<name>_<ts>_svg.pptx` | 自动 |
| SRD 表完整 | design_spec §V 含 5.1-5.7 七档 | 人工 |
| 抽帧覆盖 ≥3 款 | images/_game_assets/ 子目录 ≥3 | 自动 |

---

## 6. 速通触发词（用户可用任意一个）

- `剩余的直接跑完`
- `跑完`
- `做完`
- `继续到底`
- `直接出 PPT`

触发后 AI 行为：
1. 不再二次确认任何非 BLOCKING 步骤
2. 跑完 Step 4.5 + Step 6 + Step 7 全部
3. 用户**说话时间 = AI 干活时间**（用户可以离开屏幕）
4. **完成后必出报告**（见上一节）

---

## 7. 项目专属说明（可选填）

> 这一段是给本项目特殊约束用的。常见场景：
> - 美术风格特殊要求（如"必须 pixel-art 32×32"）
> - 商业化禁忌（如"不能有抽卡"）
> - 评审约束（如"评委是 SLG 老炮，不要写新手向的解释"）
> - 时间紧张（如"今晚 11 点前必须出 PPTX"）

```
<在此填写本项目特殊要求；没有就保持空>
```

---

## 8. 启动命令

用户在 Cursor 里贴的启动语：

```
@AGENT_PROMPT.md  按这个启动 ppt-cycle-game-master skill
```

或更简短：

```
@AGENT_PROMPT.md  开干
```

---

> **环境变量约定**：
> - `${PPT_MASTER}` = `skills/ppt-master/`
> - `${SKILL_DIR}`  = `skills/ppt-cycle-game-master/`
> - `${PROJECT}`    = `projects/<项目名>/`
