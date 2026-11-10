# LaTeX 试卷

PDF 与同名源码目录放在一起。共 6 套试卷：计网 2023、2024、2025 年，计组 2018—2019 学年（2016 级）、2019 级、2021 级。源码仅保留题目，题图的 TikZ 源码一并提供。

`公共模板/` 保存编译时使用的 exam-zh v0.3.6 类文件、模块和中文字体配置，原许可证见其中的 `LICENSE`。

## 字体

自行准备有权使用的字体，放进本目录下的 `字体/`（不随仓库上传）：

- `STSong.ttf`、`STHeiti.ttf`、`STHeitiMedium.ttc`。最后一个文件须包含 SC Medium 字体，配置使用索引 1。
- New Computer Modern 的 `NewCM10-*.otf`、`NewCMSans10-*.otf`、`NewCMMono10-*.otf` 和 `NewCMMath-Book.otf`，包括 Book、Bold 及相应斜体版本。

不使用宋体、黑体或 Times 替换上述字体。

## 编译

使用 Tectonic。在某一套试卷的源码目录中运行，例如：

```powershell
tectonic -Z search-path="../../../公共模板" -Z search-path="../../../字体" paper.tex
```

各套试卷的主文件统一为 `paper.tex`，避免 Windows 下含空格的主文件名影响辅助文件读取。首次编译可能需要下载 TeX 依赖。

2018—2019 计组先编译两幅矢量题图，再编译主文件：

```powershell
tectonic -Z search-path="../../../公共模板" -Z search-path="../../../字体" instruction.tex
tectonic -Z search-path="../../../公共模板" -Z search-path="../../../字体" cpu.tex
tectonic -Z search-path="../../../公共模板" -Z search-path="../../../字体" paper.tex
```

这套源码由原构造记录恢复，原先误写的“期末”已更正为“期中”；两幅题图直接使用矢量版。其余 5 套来自对应 PDF 的原构造文件，仅调整共享字体路径。PDF 仍放在源码目录的上一级。
