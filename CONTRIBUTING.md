# 贡献说明

欢迎提交改进。

这个仓库当前面向中文用户维护，提交前请优先遵循下面几条：

## 可以贡献什么

- 新模板或版式
- 图表与 SVG 资产
- 脚本改进
- 文档补充与纠错
- Bug 反馈
- 新的工作流建议

## 提交前建议

1. 从 `main` 拉新分支。
2. 改动尽量聚焦，不要把无关修改混在一起。
3. 如果改了脚本或流程，请补最小验证说明。
4. 如果改了公开入口文档，请保持中文优先。

## SVG 相关约束

如果你的改动涉及 SVG，请先看：

- [CLAUDE.md](./CLAUDE.md)
- [skills/ppt-master/references/shared-standards.md](./skills/ppt-master/references/shared-standards.md)

尤其注意：

- 不要使用 `clipPath`、`mask`、`foreignObject`、外部 CSS、`<script>`
- 用 `fill-opacity` / `stroke-opacity`，不要直接依赖 `rgba()`
- 画布尺寸和 `viewBox` 必须正确

## Bug 反馈建议

提 issue 时请尽量带上：

- 问题现象
- 复现步骤
- 预期结果与实际结果
- 环境信息：系统、Python 版本、使用的 AI IDE

问题入口：

- [GitHub Issues](https://github.com/k412407009/game-ppt-master/issues)

## 行为约束

请遵循：

- [行为准则](./CODE_OF_CONDUCT.md)

## 开源协议

提交代码即表示你同意按：

- [MIT License](./LICENSE)

进行开源。
