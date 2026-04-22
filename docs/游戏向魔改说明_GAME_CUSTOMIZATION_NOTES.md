# 游戏向魔改说明_GAME_CUSTOMIZATION_NOTES

## 这份文档是干什么的

这不是对上游 `ppt-master` 的否定，而是说明：为什么这个公开仓现在叫 **Game PPT Master**，以及它相对上游多改了哪些东西、又刻意保留了哪些兼容性。

---

## 一句话结论

`game-ppt-master` 是一个**面向游戏行业的公开定向改造版**：

- 底层仍然沿用 `hugohe3/ppt-master` 的原生可编辑 PPTX 引擎
- 上层增加了游戏行业所需的素材采集、评审闭环、三仓协同和交付说明

所以它不是“从零重写的新 PPT 引擎”，而是“把原始引擎产品化到游戏行业流程里”。

---

## 这次到底改了什么

### 1. 仓库定位改了

上游 `ppt-master` 的定位更通用，强调“任何文档 -> 可编辑 PPTX”。

这个仓库则明确聚焦：

- 游戏项目立项
- 竞品拆解
- 外部游戏评审
- 评审结果再回灌为汇报 PPT

也因此，GitHub repo 名称从 `ppt-master` 改成了 `game-ppt-master`。

### 2. 工作流从“单仓做 PPT”改成了“三仓闭环”

现在推荐的事实链路是：

1. `game-ppt-master`
2. `game-asset-collector`
3. `game-review`

对应关系：

- `game-ppt-master`：主流程、资料组织、PPT 产出
- `game-asset-collector`：商店抓图、视频抽帧、标签和描述
- `game-review`：结构化评审报告

### 3. 新增了游戏行业的中间层能力

相对纯 PPT 引擎，这个仓库重点增加了：

- Step 4.5 游戏素材采集衔接
- 外部游戏视觉证据链
- 评审报告回灌到 PPT 的闭环
- 与 `game-review` 的结构化产物对接
- 给同事用的三仓接入说明和元数据清单

### 4. 对外品牌改了，但内部兼容层没硬改

这是一个有意为之的兼容策略：

- GitHub repo 名叫 `game-ppt-master`
- 但内部目录仍保留 `skills/ppt-master/...`

原因很现实：

- 现有 skill 文档、脚本、项目提示词大量引用了 `skills/ppt-master/...`
- 如果连内部路径一起重命名，会打断现有项目、脚本和下游仓库桥接
- 现在先把“公开入口名”改对，把“内部兼容层”保住，是更稳妥的做法

---

## 哪些东西刻意没有改

这几个地方目前刻意保留上游兼容性：

- `skills/ppt-master/` 目录名
- 绝大多数底层 SVG -> PPTX 转换脚本路径
- 现有项目里已经写死的 `skills/ppt-master/...` 命令

换句话说：

- **对外**：这是 `game-ppt-master`
- **对内**：底层 engine path 仍然叫 `ppt-master`

---

## 对同事使用意味着什么

如果同事要直接下载使用，应该理解成：

1. 这是一个游戏行业专用入口仓
2. 但底层技术资产继承自上游 `ppt-master`
3. 本地推荐和 `game-asset-collector`、`game-review` 同级放置
4. 看到 `skills/ppt-master/...` 不要误以为没改名，这是兼容层

---

## 什么时候再考虑连内部路径一起改

只有在下面这些条件同时满足时，才值得做第二阶段重命名：

- `game-review`、`game-asset-collector`、个人项目提示词都已经切到新路径
- 不再需要兼容旧项目 prompt / wrapper / 自动脚本
- 有完整脚本去批量替换引用并验证

在那之前，**先改 GitHub repo 名和对外文档，保留内部路径兼容**，风险最低。
