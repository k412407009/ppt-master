# Design Spec Skeleton — 单循环游戏立项 PPT 骨架

> 在 Step 4 (Strategist) 编写 `design_spec.md` 时，**直接复制本骨架**填写。
> 本骨架基于 `${PPT_MASTER}/templates/design_spec_reference.md` 简化，
> **加强 §V (SRD) + §VI (Reference Game Matrix)**，**砍掉过度复杂的 brand assets / accessibility section**。
>
> Section 命名遵循 ppt-master 的 I-XI 结构（用户语言可中文，但 section 名保持英文）。

---

## I. Project Overview

```markdown
## I. Project Overview

| 字段 | 值 |
|---|---|
| 项目名 | <例：J_像素工坊> |
| 题材 | <单循环经营 / 竖屏塔防 / 工厂链 / 产业经营> |
| 核心循环（一句话） | <例：经营宠物店，养出稀有宠物再出售> |
| 立项阶段 | <S1 立项 / S2 Demo / S3 Pre-launch> |
| 评审日期 | <例：2026-04-25> |
| 目标页数 | <例：28 页> |
| 画布 | <ppt169 / xhs> |
| Decision Owner | <例：制作人 + 主美 + 数值> |
```

---

## II. Audience & Goal

```markdown
## II. Audience & Goal

| 字段 | 值 |
|---|---|
| 目标受众 | <评委 / 老板 / 评审会 / VC> |
| Top-1 信息 | <一句话：希望评审会记住的核心> |
| 立项决策 | <希望评审会做出什么决定> |
| 风险点 | <已知 1-3 条主要风险> |
```

---

## III. Style Spec

```markdown
## III. Style Spec

### III.1 配色（来自 Q3）
| 角色 | 色值 | 用途 |
|---|---|---|
| Primary | #XXXXXX | 章节标题 / CTA |
| Secondary | #XXXXXX | 次要强调 |
| Accent | #XXXXXX | 数据高亮 |
| Bg | #XXXXXX | 主背景 |
| Text | #XXXXXX | 主文本 |
| Subtext | #XXXXXX | 次文本 |

> ⚠️ 单循环 pack **不内置**双调色板。如果题材要求（如昼夜机制），见 ppt-master 主路径。

### III.2 字体
- 中文 H1-H3：Source Han Serif SC Bold
- 中文 Body：Source Han Serif SC Regular
- 英文/数字：Inter / Roboto

### III.3 Icon
- 默认 `tabler-outline/`
- 备选 `tabler-filled/`
- 不用 `chunk/`（除非有特殊需求）
```

---

## IV. Page Layout Plan

```markdown
## IV. Page Layout Plan

| 页 | 章节 | 标题 | 关键素材 | 镜头方向 |
|---|---|---|---|---|
| 01 | 封面 | <项目名>·立项汇报 | _remix/cover_v2.jpg | 全屏 hero |
| 02 | 引子 | 一句话项目介绍 | 主角立绘 | 中景 |
| 03 | I 概述 | 我们要做什么 | 核心循环图 | 远景 |
| 04 | V 循环 | 核心循环 | SRD 表 5.1-5.7 缩略 | 信息密度 |
| 05 | V 循环 | 5.1-5.3 早期钩子 | 时间线 | 特写 |
| 06 | V 循环 | 5.4-5.5 中期耦合 | 系统图 | 中景 |
| 07 | V 循环 | 5.6-5.7 长期粘性 | 高峰事件 | 全景 |
| 08 | VI 矩阵 | 5 款竞品总览 | 5×3 格子 | 远景 |
| 09 | VI 矩阵 | 核心循环参考：<游戏A> | 商店截图 ×4 | 中景 |
| 10 | VI 矩阵 | 美术风格参考：<游戏B> | UI 大图 | 特写 |
| 11 | VI 矩阵 | 商业化参考：<游戏C> | 商城页 | 信息密度 |
| 12 | VI 矩阵 | 元层参考：<游戏D> | 升级树 | 中景 |
| 13 | VII 美术 | 视觉锚点 | i2i 风格化 | 全景 |
| 14 | VII 美术 | NPC 立绘 | _gen/ × 5 | 中景 |
| ... | ... | ... | ... | ... |
| NN | XI 申请 | 立项申请 + 排期 | 时间轴 | 全景 |
```

---

## V. Core Loop  ⭐ 本 skill 重点强化

```markdown
## V. Core Loop

### V.1 SRD 节奏密度表（7 档强制）

| 阶段 | 时长 | 玩家行为 | 必触钩子 | 留存目标 | 验收标准 |
|---|---|---|---|---|---|
| 5.1 | 0–30s    | <填> | <填> | 95% | <填> |
| 5.2 | 30s–2min | <填> | <填> | 80% | <填> |
| 5.3 | 2–15min  | <填> | <填> | 70% | <填> |
| 5.4 | 15–60min | <填> | <填> | 60% | <填> |
| 5.5 | 1–4h     | <填> | <填> | 50% | <填> |
| 5.6 | Day 2–3  | <填战斗/高峰/反派> | <填> | 40% | <填> |
| 5.7 | Day 5–30 | <填长期目标> | <填> | 20% | <填> |

> 详细模板见 `${SKILL_DIR}/templates/srd_table.md`。

### V.2 核心循环图解

[文字描述 + mermaid 图]

### V.3 单循环时长

- 标准单循环：~XX 秒/分
- 玩家在前 X 分钟内完成 N 次循环
- 循环间无强迫等待（如有，必须有元层补偿）
```

---

## VI. Reference Game Matrix  ⭐ 本 skill 重点强化

```markdown
## VI. Reference Game Matrix

### VI.1 5 款竞品（按维度分）

| # | 游戏名 | 维度 | 上游 | 我们要参考的具体点 |
|---|---|---|---|---|
| 1 | <游戏A> | **核心循环** | iOS / Android / Steam | 接客排队动画 / 升级路径 / ... |
| 2 | <游戏B> | **美术风格** | iOS / Android | UI 配色 / icon 风格 / 立绘姿态 / ... |
| 3 | <游戏C> | **商业化** | iOS / Android | IAP 礼包 / 广告位 / 推送时机 / ... |
| 4 | <游戏D> | **元层进阶** | iOS / Android | 赛季 / 公会 / 收集图鉴 / ... |
| 5 | <游戏E> | **UI / UX** | iOS / Android | 信息密度 / 单手操作 / 引导文案 / ... |

### VI.2 维度对比表

| 项 | 游戏A | 游戏B | 游戏C | 游戏D | 游戏E | **本游戏** |
|---|---|---|---|---|---|---|
| 单循环时长 | 5min | 8min | 10min | 6min | 12min | **7min** |
| 主玩法 | ... | ... | ... | ... | ... | **...** |
| 商业化 | IAP | IAP+ad | IAP | 抽卡 | IAP+ad | **IAP+ad** |
| 留存 D7 | 30% | 40% | 25% | 35% | 28% | **35%（目标）** |

### VI.3 不参考的游戏（划清边界）

- 不参考 <游戏X>：原因 ...
- 不参考 <游戏Y>：原因 ...
```

---

## VII. AI Generation List

```markdown
## VII. AI Generation List

### VII.1 t2i 立绘清单（送给美术 Image_Generator）

| # | 文件名 | Prompt 关键词 | 用途 | 尺寸 |
|---|---|---|---|---|
| 1 | _gen/main_character.jpg | "kawaii cat shop owner, ..." | 主角立绘 | 9:16 |
| 2 | _gen/villain.jpg | ... | 反派立绘 | 9:16 |
| ... | ... | ... | ... | ... |

### VII.2 i2i 风格化清单（送给美术）

| # | 源图 | 风格化 prompt | 用途 |
|---|---|---|---|
| 1 | _game_assets/<游戏A>/store/01.jpg | "Pixar style, warm colors, ..." | 封面 hero |
| ... | ... | ... | ... |

### VII.3 章节背景清单

| # | 章节 | 文件名 | Prompt | 尺寸 |
|---|---|---|---|---|
| 1 | III 概述 | _gen/ch1_bg.jpg | ... | 16:9 |
| ... | ... | ... | ... | ... |
```

---

## VIII. Image Resource List  ⭐ 本 skill 重点强化（摄影抽帧后回填）

```markdown
## VIII. Image Resource List

### VIII.1 _game_assets（摄影组采集）

| 文件 | 来源 | 内容 | Notes（"为什么用这张"） |
|---|---|---|---|
| _game_assets/<游戏A>/store/appstore/01.jpg | App Store 官方 | 主界面截图 | §V.5 主循环图：左侧排队→右侧服务台 |
| _game_assets/<游戏A>/frames/00045.jpg | YouTube gameplay | 升级动画 | §V.4 升级解锁视觉参考 |
| ... | ... | ... | ... |

### VIII.2 _gen / _remix（美术产出）

| 文件 | Prompt 简版 | Notes |
|---|---|---|
| _gen/main_character.jpg | kawaii cat shop owner | §I 封面 + §VII 立绘页 |
| _remix/cover_v2.jpg | 5-img collage + Pixar restyle | §I 封面 hero |

### VIII.3 总计

- 商店截图 ×<XX> 张 / 视频抽帧 ×<XX> 张 / i2i ×<XX> 张 / t2i ×<XX> 张
- 总大小 ~<XX> MB
- 覆盖游戏 <X> 款
```

---

## IX. Speaker Notes Skeleton

```markdown
## IX. Speaker Notes Skeleton

每页讲稿 200-400 字。结构：

[Pause]
开场 1 句

主体 3-5 段：
- [Data] 数据点
- [Benchmark] 行业对比
- [Transition] 转场到下一点

[Pause]
收尾 1 句 → 引下一页
```

---

## X. Risk & Open Questions

```markdown
## X. Risk & Open Questions

### X.1 已知风险

| # | 风险 | 影响 | 缓解 |
|---|---|---|---|
| 1 | <例：5.6 偷猎者夜袭机制可能让"治愈"用户流失> | D2-D3 留存 -10% | A/B 测试是否做"硬核难度"版 |
| 2 | ... | ... | ... |

### X.2 开放问题（需要评审拍板）

| # | 问题 | 备选 | Owner |
|---|---|---|---|
| 1 | 是否做双调色板（DAY/NIGHT）？ | A) 做 B) 不做 ★ | 主美 |
| 2 | ... | ... | ... |
```

---

## XI. Approval Sign-off

```markdown
## XI. Approval Sign-off

- [ ] 编剧 (Strategist): __________
- [ ] 导演 (Executor): __________
- [ ] 美术 (Image_Generator): __________
- [ ] 数值 (Designer): __________
- [ ] 制片人 (Producer): __________

立项决策：__________
评审日期：__________
```

---

## 与 ppt-master design_spec_reference.md 的差异

| Section | ppt-master 母版 | 本骨架 |
|---|---|---|
| I. Project Overview | 通用 | **加 题材 / 立项阶段 / 评审日期** |
| II. Audience & Goal | 通用 | 不变 |
| III. Style Spec | 含 brand assets / accessibility | **砍 brand assets / accessibility** |
| IV. Page Layout Plan | 表格 | **加 镜头方向**（电影组语言） |
| **V. Core Loop** | 简单 | **强制 SRD 表 7 档** |
| **VI. Reference Game Matrix** | 通用引用 | **强制 5 款竞品 5 维度** |
| VII. AI Generation List | 通用 | **加 i2i 子节** |
| **VIII. Image Resource List** | 通用 | **强制填 Notes "为什么用这张"** |
| IX. Speaker Notes | 通用 | 不变 |
| X. Risk | 通用 | **加 开放问题表** |
| XI. Sign-off | 通用 | **加 电影组角色** |
