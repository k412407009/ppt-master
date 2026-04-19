# Palette Extraction

为 PPT Master 提供一个标准化的"配色输入"：从本地截图或 Figma 文件中抽出配色，统一写到 `palette.json`。设计阶段读这个文件代替凭感觉配色。

## 产出格式（两种脚本统一）

```json
{
  "source": {
    "type": "image | figma_styles | figma_thumbnails",
    "files": ["/abs/path/to/ref1.png"]
  },
  "swatches": [
    { "hex": "#0F172A", "rgb": [15, 23, 42], "role": "text",       "weight": 0.22 },
    { "hex": "#2563EB", "rgb": [37, 99, 235], "role": "primary",    "weight": 0.18 },
    { "hex": "#F97316", "rgb": [249, 115, 22], "role": "accent_1",  "weight": 0.09 },
    { "hex": "#F8FAFC", "rgb": [248, 250, 252], "role": "background","weight": 0.32 }
  ]
}
```

`role` 的含义：`primary` / `accent_N` / `background` / `text` / `neutral_N`。PPT Master 设计阶段按 role 就近取色。

---

## 1. 从本地截图取色 · `palette_from_image.py`

最推荐的起手式——在 Dribbble / 小红书 / Stitch 里看到好看的截图，下载到 `projects/<项目名>/sources/style_refs/`，然后：

```bash
python3 skills/ppt-master/scripts/palette/palette_from_image.py \
  projects/<项目名>/sources/style_refs/ \
  --k 6 \
  --out projects/<项目名>/palette.json
```

- 可以传多张图，也可以传一个目录（递归抓 `.png/.jpg/.webp`）
- `--k` 控制提取几种颜色，默认 6
- 脚本会自动滤掉几乎纯白和几乎纯黑的像素，防止被背景淹没

零依赖：只用了 `Pillow` + `numpy`（ppt-master 依赖已包含）。

---

## 2. 从 Figma 文件取色 · `palette_from_figma.py`

### 准备

把你的 Figma Personal Access Token 写到仓库根目录的 `.env`：

```env
FIGMA_TOKEN=figd_xxxxxxxxxxxxxxxx
```

`.env` 已经在 `.gitignore`，不会被 commit。脚本只从环境变量读 token，绝不落到产物或日志里。

Token 所需的 scope（在 Figma 生成时勾选）：
- `file_content:read`（必选）
- `file_metadata:read`（必选）
- `library_content:read`（可选，能读到已发布的样式/变量）
- `file_variables:read`（可选，新版 Variables 文件需要）

### 用法

```bash
python3 skills/ppt-master/scripts/palette/palette_from_figma.py \
  "https://www.figma.com/design/XXXXXXX/some-file?node-id=0-1" \
  --out projects/<项目名>/palette.json
```

脚本行为：

1. 先尝试读"已发布的 Color Styles"——如果这个 Figma 文件是规范的设计系统，这条路会直接拿到**带名字**的 swatch（如 `Brand/Primary`），role 会根据名字推断
2. 如果文件没发布样式（多数社区 pitch deck 都是这种），自动降级为：渲染前 12 个 frame 的缩略图 PNG → 复用本地取色逻辑 → 输出同样格式的 `palette.json`

想强制走第二种（比如就是想"按视觉"取而不是按命名）：加 `--force-pixels`。

---

## 在 PPT Master 里怎么用

在你项目的 `design_spec.md` 最前面加一段：

```markdown
## 配色
遵循 ./palette.json：
- 正文文字色 = role=text 的那个
- 强调/主色 = role=primary
- 辅助色依次取 role=accent_1 / accent_2
- 大面积背景 = role=background
除上述 6 色外不要自由发挥。
```

PPT Master 在生成时会读这个 spec，并把 `palette.json` 作为硬约束带入。
