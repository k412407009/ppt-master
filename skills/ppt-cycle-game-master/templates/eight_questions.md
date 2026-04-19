# Eight Questions — 八问八答（电影组语言版）

> 在 Step 4 (Strategist) 之前必问完。用户回复支持紧凑格式（如 `B1 c1 D1 E1`），
> 详见 `${SKILL_DIR}/references/conversation-style.md` §1.2。
>
> 本模板**通用**（单循环 + 塔防 + 工厂 + 产业经营都可用）；
> 塔防/工厂可在此基础上**加 Q9 单局时长 + Q10 产业化深度**（见 vertical-tower-defense-pack.md §4）。

---

## 八问八答（推荐展示给用户的格式）

```markdown
## 📋 八问八答

请用紧凑格式回复（如 `1.B 2.c 3.A...` 或 `B c A C ...`）：

### 1. 📝 编剧 — 核心循环一句话怎么说？
- A) 经营 → 升级 → 扩张  ★（推荐：单循环经营）
- B) 防守 → 升级 → 扩张  ★（推荐：塔防）
- C) 采集 → 加工 → 销售  ★（推荐：工厂链）
- D) 探索 → 收集 → 收容  （动物收容/宠物题材）
- E) 自定义：<请描述>

### 2. 🎬 导演 — 头 30 秒玩家看到什么？
- A) 主角立绘 ×1 + Tap 反馈  ★（推荐：单循环）
- B) 已布置好的首关，自动开演  ★（推荐：塔防）
- C) 短动画 ×3 秒 + Skip 按钮
- D) 教学引导（强制 step-by-step）
- E) 自定义

### 3. 🎨 美术 — 风格基调？
- A) 暖 + 卡通  ★（推荐：单循环经营 / 治愈题材）
- B) 冷 + 写实  ★（推荐：塔防 / 生存题材）
- C) 暖冷对比 / 双调色板  ⚠️（**本 skill 不内置**双调色板支持，慎选）
- D) 单色高对比（黑白 + 1 主色）
- E) 像素 / 复古
- F) 自定义

### 4. 📷 摄影 — 抽帧覆盖几款？
- A) 3 款（最少）
- B) 5 款  ★（**推荐**，按 §VI 5 维度选）
- C) 7 款（重型立项）
- D) 自定义：<X 款>

### 5. ✂️ 剪辑 — SRD 节奏密度，哪几档必触发？
- A) 5.1-5.5 五档（短线立项）
- B) **5.1-5.7 全七档** ★（推荐，本 skill 默认强制 7 档）
- C) 自定义：<5.X 到 5.Y>

### 6. 🎟️ 制片 — 商业化点？
- A) IAP-only
- B) IAP + 广告  ★（行业默认）
- C) 订阅
- D) 抽卡 / 卡池
- E) 盒装 + DLC
- F) 自定义组合

### 7. 🎬 试映 — 留存目标 D1 / D7 / D30？
- A) 50 / 25 / 10（保守）
- B) 60 / 30 / 15  ★（中等品质）
- C) 70 / 40 / 20（高质量）
- D) 自定义：<D1/D7/D30>

### 8. 🎟️ 发行 — 目标市场？
- A) 国服 only
- B) 海外 only
- C) 双平台 同步  ★（推荐）
- D) 国服优先 + 海外跟进
- E) 自定义
```

---

## 紧凑回复解析示例

| 用户回复 | AI 解析 |
|---|---|
| `B C A B B B B C` | Q1=B, Q2=C, Q3=A, Q4=B, Q5=B, Q6=B, Q7=B, Q8=C |
| `1.B 2.C 3.A` | 只确认前 3 题，其余待回 |
| `1.B1 2.c1先全收吧` | Q1=B + 用户附带说明，Q2=C + 用户表态 |
| `B c A C E B B B` | 大小写不敏感，逐位匹配 |
| `全部默认` / `★ 全选` | 全部用 ★ 推荐项 |

---

## AI 应对 SOP

### 收到回复后

1. **解析全部 Q**（不要逐个 Q 二次确认）
2. **输出确认行**：

   ```markdown
   ✅ 八问已确认：B / C / A / B / B / B / B / C
   📋 → 进入 Step 4.5（Game Asset Collection），抽帧 5 款竞品。
   ```

3. **如果用户漏答**（比如只给了 5 个），列出**未答**的 Q，要求补：

   ```markdown
   ✅ 已收到 Q1-Q5（B / C / A / B / B）
   ⏳ 还需 Q6（商业化）/ Q7（留存目标）/ Q8（市场）
   ```

4. **如果用户写了 "自定义"**，立刻追问 1 行：

   ```markdown
   ✅ Q4 自定义已记
   ❓ 请告诉我具体抽帧款数：6 / 8 / 10 / ...
   ```

### 不允许的行为

❌ 逐个 Q 重复 "Q1 您选的是 B 对吗"
❌ 把所有选项再展示一遍要用户"确认"
❌ 加额外 Q（除非塔防/工厂 pack 加 Q9/Q10）
❌ 把 ★ 推荐项强加给用户（用户不选 ★ 也得尊重）

---

## 进入 design_spec 编写

八问全部确认后，AI **立刻**：

1. 切换角色为 📝 **编剧 Screenwriter** (Strategist)
2. 读 `${SKILL_DIR}/references/srd-density-checklist.md`
3. 读 `${PPT_MASTER}/templates/design_spec_reference.md`（母版）
4. 读 `${SKILL_DIR}/templates/design_spec_skeleton_cycle.md`（本 skill 骨架）
5. 输出完整 `design_spec.md`，**必含 §V SRD 表 7 档**
6. **等待用户确认 design_spec** （⛔ BLOCKING）
7. 进入 Step 4.5

---

## 与 ppt-master 八问的关系

| 项 | ppt-master 八问 | 本 skill 八问 |
|---|---|---|
| 1 | Canvas format | 不问（AGENT_PROMPT 第 0 节已定） |
| 2 | Page count range | 不问（AGENT_PROMPT 第 0 节已定） |
| 3 | Target audience | 不问（评委 / 老板 / 评审会，默认） |
| 4 | Style objective | Q3 风格基调 + Q1 核心循环 |
| 5 | Color scheme | Q3 风格基调 |
| 6 | Icon usage | 默认 tabler-outline，不问 |
| 7 | Typography | 默认 SourceHanSerif，不问 |
| 8 | Image usage | Q4 抽帧覆盖（默认 D + B） |
| - | - | + Q1/Q2/Q5/Q6/Q7/Q8（题材专属） |

> 本 skill 八问把 ppt-master 的"通用八问"**特化**为"游戏立项八问"。
> 通用项（画布 / 页数 / 字体）已经在 `AGENT_PROMPT_template.md` 第 0 节预填，不重复问。
