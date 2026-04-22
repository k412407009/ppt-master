# Game PPT Master

面向游戏行业的本地 PPT 工作流。

输入 PDF、DOCX、网页或 Markdown，输出真正可编辑的 `.pptx`。如果需要完整链路，还可以和 `game-asset-collector`、`game-review` 组合，完成素材抓取、结构化评审和最终汇报。

## 这是什么

这个仓库解决 3 件事：

- 把原始资料整理成可编辑 PPT，而不是图片或网页截图
- 把游戏行业常见场景串起来：立项、竞品、拆解、评审、汇报
- 作为三仓体系的主入口，衔接采集器和评审模块

## 仓库定位

- GitHub 公开仓名：`game-ppt-master`
- 本地推荐目录名：`game-ppt-master/`
- 内部兼容路径仍保留：`skills/ppt-master/...`
- 底层可编辑 PPTX 引擎来自上游 [hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)

为什么保留内部 `skills/ppt-master/...` 路径：

- 现有脚本、项目提示词和下游桥接大量依赖这条路径
- 先把公开入口统一成 `game-ppt-master`，风险更低
- 兼容策略详见 [游戏向魔改说明](./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md)

## 适合什么场景

- 游戏立项汇报
- 竞品分析和拆解
- 外部游戏评审结果回灌成 PPT
- 把 PDF、DOCX、网页快速整理成结构化 deck

## 最小安装

只需要先装 Python 3.10+。

```bash
git clone https://github.com/k412407009/game-ppt-master.git
cd game-ppt-master
pip install -r requirements.txt
```

Windows 用户建议直接看：

- [Windows 安装指南](./docs/zh/windows-installation.md)

## 最快使用方式

1. 把源文件放进 `projects/` 目录。
2. 在你使用的 AI IDE 里打开本仓库。
3. 让 AI 先读取 `skills/ppt-master/SKILL.md`。
4. 告诉它使用哪份资料生成 PPT。

示例：

```text
请先阅读 skills/ppt-master/SKILL.md。
然后用 projects/q3-report/sources/report.pdf 生成一份 10 页左右的游戏行业汇报 PPT。
```

输出文件会落在 `exports/`。

## 推荐编辑器

- `Claude Code`：效果最好
- `Cursor`
- `VS Code + Copilot`
- `Codebuddy`

核心原则不是绑定某个 IDE，而是让模型按 `SKILL.md` 跑完整流程。

## 可选：AI 生图

如果你要在 PPT 里补图，可以配置 `.env`：

```bash
cp .env.example .env
```

```env
IMAGE_BACKEND=gemini
GEMINI_API_KEY=your-api-key
GEMINI_MODEL=gemini-3.1-flash-image-preview
```

支持的后端包括：

- `gemini`
- `openai`
- `qwen`
- `zhipu`
- `volcengine`
- `stability`
- `bfl`
- `ideogram`
- `siliconflow`
- `fal`
- `replicate`

查看后端说明：

```bash
python3 skills/ppt-master/scripts/image_gen.py --list-backends
```

## 完整链路：三仓协同

如果你不仅要做 PPT，还要做素材抓取和结构化评审，推荐把 3 个仓库放在同级目录：

```text
<workspace>/
  game-ppt-master/
  game-asset-collector/
  game-review/
```

三者分工：

- `game-ppt-master`：主工作流、PPT 生成、最终汇报
- `game-asset-collector`：商店截图、视频抽帧、标签、描述
- `game-review`：5 位评委 × 7 维度评审，输出 `docx` / `xlsx` / `md`

对应仓库：

- [game-ppt-master](https://github.com/k412407009/game-ppt-master)
- [game-asset-collector](https://github.com/k412407009/game-asset-collector)
- [game-review](https://github.com/k412407009/game-review)

链路说明见：

- [三仓协同架构](./docs/三仓协同架构_THREE_REPO_STACK.md)
- [同事接入指南](./docs/同事接入指南_TEAM_ONBOARDING_GUIDE.md)
- [生态清单](./docs/生态清单_ECOSYSTEM_MANIFEST.json)

## 文档入口

| 文档 | 说明 |
|---|---|
| [游戏向魔改说明](./docs/游戏向魔改说明_GAME_CUSTOMIZATION_NOTES.md) | 说明这个仓库相对上游改了什么、保留了什么 |
| [Windows 安装指南](./docs/zh/windows-installation.md) | Windows 用户安装步骤 |
| [为什么选这套引擎](./docs/zh/why-ppt-master.md) | 和其他 AI PPT 工具的区别 |
| [SKILL.md](./skills/ppt-master/SKILL.md) | 核心流程与规则 |
| [三仓协同架构](./docs/三仓协同架构_THREE_REPO_STACK.md) | 三仓完整链路 |
| [同事接入指南](./docs/同事接入指南_TEAM_ONBOARDING_GUIDE.md) | 给同事看的下载、目录、API Key 说明 |
| [游戏评审闭环](./docs/游戏评审闭环_GAME_REVIEW_CLOSED_LOOP.md) | 从素材到评审报告再到 PPT 的闭环 |
| [脚本与工具](./skills/ppt-master/scripts/README.md) | 所有脚本入口 |
| [常见问题](./docs/zh/faq.md) | 模型选择、导出、排版等问题 |

## 当前建议的使用顺序

### 只做 PPT

1. 安装依赖
2. 打开仓库
3. 让 AI 阅读 `skills/ppt-master/SKILL.md`
4. 指定源文件
5. 在 `exports/` 里查看结果

### 做游戏素材和评审

1. 在 `game-asset-collector` 抓商店图和视频帧
2. 在 `game-review` 生成结构化评审报告
3. 再回到 `game-ppt-master` 做最终汇报 PPT

## 反馈

- 问题反馈：[/issues](https://github.com/k412407009/game-ppt-master/issues)
- 仓库主页：[github.com/k412407009/game-ppt-master](https://github.com/k412407009/game-ppt-master)
- 上游引擎：[github.com/hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)

## 开源协议

[MIT](./LICENSE)
