# Lessons from I_动物联盟 — 10 条复盘经验

> 本文档提炼自 **2026-04-19** 全程对话流（项目：`I_动物联盟_动物庇护所+Zootopia情感叙事+My-Perfect-Hotel`）。
> 启动新项目前**推荐回顾**，避免重复踩坑。
>
> 项目结果：28 页 SVG 100% PASS / 16,879 字讲稿（~600/页）/ 双版本 PPTX（13.67MB + 26.37MB）/ 0 WARN 0 FAIL。
> 全程用时（含 I/O + 等待）：约 4 小时。

---

## §1 选游戏要按维度分

❌ **错误做法**：随便选 5 款喜欢的游戏当竞品。
✅ **正确做法**：按 **核心循环 / 美术风格 / 商业化 / 元层 / UI** 5 个维度选，每个维度 1 款。

I_动物联盟 实际选了：
- 核心循环：**Animal Shelter Simulator**（管理 + 收容 + 升级）
- 美术风格：**Cat Cafe Manager**（暖卡通）
- 商业化：**My Perfect Hotel** (MPH)
- 元层：**Whiteout Survival**
- 战斗机制：**Hitman GO**（拖拽路径解密）+ **Thronefall**（轻塔防）

> 因为本项目玩法融合（治愈 + 战斗），所以多了"战斗机制"维度，比常规 5 款多了 1-2 款 = 7 款总。
> 单循环游戏建议**严格 5 款**，不要堆。

---

## §2 design_spec §VIII 的 Notes 字段必填"为什么用这张"

❌ **错误做法**：抽完帧直接放 §VIII 表格，Notes 字段空着 / 写"参考截图"。
✅ **正确做法**：每张图填一个**具体用途**：

```markdown
| 文件 | Notes |
|---|---|
| _game_assets/MPH/store/appstore/screenshot_02.jpg | §V.5 主循环图：左侧 NPC 排队 → 右侧服务台 → 上方收银 |
| _game_assets/Animal-Shelter/store/appstore/03.jpg | §VIII.1 收容所建造界面参考（玩家视角） |
| _remix/cover_zootopia_pixar_v2.jpg | §I 封面：Zootopia + Pixar 风格化主视觉 |
```

> 这样导演 (Executor) 在 Step 6 拍每页时 **知道每张图放在哪里**，不需要二次澄清。

---

## §3 双调色板项目要预留两套 NIGHT/DAY 资源

I_动物联盟 用了双调色板（暖白天 + 冷夜晚），结果：
- 单循环 5 款竞品截图都是"白天"调
- 美术 i2i 时还得为"夜晚"再生一套

**结论**：单循环 pack **故意不支持** 双调色板。
**例外**：如果游戏核心机制本身含昼夜（如 I_动物联盟 偷猎者只在夜里来），那才用双调色板。

---

## §4 SVG batch writer 必须用 Python heredoc

❌ **错误做法**：用 Cursor `Write` 工具直接写 SVG（含中文 / `·` / 中文标点）。
**结果**：90% 概率被 Cursor 编码为 Latin-1，silent corruption，finalize_svg 时挂掉。

✅ **正确做法**：写一个 `batchN_writer.py`，里面定义所有 SVG 内容字符串，最后用：

```python
out_path.write_bytes(content.encode("utf-8"))
```

I_动物联盟 用了 5 个 batch_writer：

```
notes/batch1_writer.py  ← SVG 01-08
notes/batch2_writer.py  ← SVG 08-12
notes/batch3_writer.py  ← SVG 13-18
notes/batch4_writer.py  ← SVG 19-23
notes/batch5_writer.py  ← SVG 24-28
notes/notes_writer.py   ← total.md
```

> 跑完后**必须**清理这些临时脚本（不入 git）。
> I_动物联盟 全部清理完成。

---

## §5 validate_svg_output.py 每个 batch 必跑

❌ **错误做法**：5 个 batch 全跑完才一次性 validate → 一旦发现错误，定位困难。
✅ **正确做法**：每个 batch 跑完立刻 validate：

```powershell
chcp 65001 | Out-Null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python projects/<项目名>/notes/batch1_writer.py
python ${PPT_MASTER}/scripts/validate_svg_output.py projects/<项目名>
# ↑ 此处必须 PASS 才能跑下一个 batch
```

I_动物联盟 在 batch2 / batch3 各发现一次 XML 错误（duplicate attribute / mismatched tag），
都靠 per-batch validate 立即定位并修复。

---

## §6 icon 用 placeholder `<use data-icon=...>` 让 finalize 嵌入

❌ **错误做法**：在 SVG 里直接写 `<path d="...">` 复杂 icon → SVG 又长又难维护。
✅ **正确做法**：写 placeholder：

```svg
<use data-icon="tabler-outline/star" x="100" y="200" width="32" height="32" />
```

`finalize_svg.py` 会自动从 `${PPT_MASTER}/templates/icons/` 找到对应文件，
inline 嵌入到 SVG 里。

> ⚠️ icon 名字要写对！I_动物联盟 早期写了 `star-filled` / `shell` 这俩不存在的，
> finalize 报 4 个 WARN。后来用 `fix_assets.py` find-replace 改成 `star` / `paw`。

---

## §7 image href 一定写真实路径

❌ **错误做法**：在 SVG 里写不存在的图片路径（特别是 `_game_assets/` 子目录写错）。
✅ **正确做法**：写之前**先 ls 一下**确认真实路径。

I_动物联盟 早期写了 9 个不存在的 image href（misreference），
finalize 报 9 个 WARN。后来用 `fix_assets.py` find-replace 修复：

```python
REPLACEMENTS = [
    ("_game_assets/Animal-Shelter-Simulator/store/steam/",
     "_game_assets/Animal-Shelter-Simulator/store/appstore/"),
    ("_game_assets/Whiteout-Survival/store/appstore/",
     "_game_assets/Whiteout-Survival/store/googleplay/"),
    # ...
]
```

> **预防**：导演 (Executor) 在写 SVG 之前，应该 `ls projects/<项目名>/images/_game_assets/<game>/` 确认路径。

---

## §8 八问八答一次给清，AI 不要二次确认

I_动物联盟 用户回复格式：

```
1.B1 接受双调色板（暖白天 + 冷夜晚）
2.c1先全收吧
```
+
```
D1 E1
```

= 4 个 Q 一次性给完。

❌ **AI 错误反应**：逐个回 "Q1 您选的是 B1 对吗 ✅ ... Q2 您选的是 C1 对吗 ✅"
✅ **AI 正确反应**：一次性确认所有，进入下一步：

```markdown
✅ 八问已全部确认（B1 / C1 / D1 / E1 / ...），进入 design_spec 编写
```

---

## §9 SRD 节奏表必有 7 档（5.1-5.7）

I_动物联盟 早期写到 5.6 就停了（5.6 = Day 3-Day 7），被用户立刻 challenge：
> "中间 Day 2、Day 3 的钩子在哪里？你没有给玩家体现出'第一次'的新鲜感。"

**修复**：
- 5.6 改为 Day 2-3（不是 Day 3-7）
- 5.7 接管 Day 5-30
- 5.6 必须含战斗 / 反派 / 第一次 PvE

> 这就是为什么本 skill 在 SKILL.md "强制纪律 §9" 写：**SRD 表强制 7 档**。
> 缺一档视为执行失败。

---

## §10 速通模式必出报告

用户说"剩余的直接跑完"+"都ok的"两条短指令后，AI **必须**：

1. 不再二次确认任何非 BLOCKING 步骤
2. 跑完 Step 4.5 + Step 6 + Step 7 全部
3. **完成后必出完成报告**（含数字 + 反思）

I_动物联盟 完成报告含：
- 总页数 28 / 28
- validate_svg_output 100% PASS
- finalize_svg 0 WARN / 0 FAIL（修了 fix_assets 之后）
- 讲稿字数 16,879 字（平均 ~603 字/页）
- 双版本 PPTX（13.67 MB + 26.37 MB）
- 用时 ~4 小时

> 报告模板见 `${SKILL_DIR}/references/conversation-style.md` §1.3。
> 不出报告 = 用户不知道做完了 = 任务事实上没完成。

---

## §11 (Bonus) 题材误导自检

I_动物联盟 早期 AI 一度写成了《卡店帝国》（E_TCG）的 TCG 卡牌内容，被用户立刻指正：
> "哎，不对，你不应该写《动物联盟》的 PPT 报告吗？为什么你突然写了《卡店帝国》的 TCG 卡牌内容？"

**预防 SOP**（详见 `conversation-style.md` §6）：
- 每次回复前 self-check 项目名、当前 Step、当前角色
- 项目名以 `${PROJECT}/AGENT_PROMPT.md` 第一行为准
- 不要凭记忆开工，先读 `AGENT_PROMPT.md`

---

## §12 (Bonus) 时间单位永远显式

I_动物联盟 早期 SRD 表写 "思考头 30，挂机回报 45"，用户立刻 challenge：
> "你那个思考头是 30秒还是 30分钟？挂机回报是 45秒还是 45分钟？"

**修复**：所有时间字段必须带单位（s / min / h / Day），不允许裸数字。
这条已经写进 `conversation-style.md` §3 + `srd-density-checklist.md` §2。

---

## 总结：一句话教训

| # | 教训 | 一句话 |
|---|---|---|
| 1 | 选游戏 | 按 5 维度选 5 款 |
| 2 | §VIII Notes | 每张图填用途 |
| 3 | 双调色板 | 单循环 pack 故意不支持 |
| 4 | SVG 写法 | Python heredoc + `write_bytes(encode("utf-8"))` |
| 5 | validate | 每 batch 跑一次 |
| 6 | icon | placeholder + 名字写对 |
| 7 | image href | 写之前先 ls 验证 |
| 8 | 八问八答 | 一次给清不二次问 |
| 9 | SRD 表 | 7 档强制（5.1-5.7） |
| 10 | 速通报告 | 完成后必出 |
| 11 | 题材自检 | 每次回复前 check 项目名 |
| 12 | 时间单位 | 永远带单位 |
