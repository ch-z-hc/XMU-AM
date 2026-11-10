# 网页版

入口：https://chzhc.cn/xmu-am/

备用入口：https://ch-z-hc.github.io/XMU-AM/

`main` 分支更新后，GitHub Actions 自动生成课程目录并部署到 GitHub Pages。自托管入口使用同一份构建产物，需单独同步发布。每门课程按试卷、教材、笔记三栏展示，手机端纵向排列。试卷同时有期中、期末时按上下两组展示，只有一种时不重复分组。试卷、教材和笔记统一采用紧凑列表，每栏默认显示 3 份，其余可展开查看；试卷按期中、期末分别计数，带年份的试卷按年份降序排列，字母归档编号按 A、B、C 顺序排列。输入搜索关键词时，各栏直接显示全部匹配项。只展示各学期课程目录中的 PDF；空分类不显示，其余栏靠左排列。Markdown、LaTeX 等源文件与配套图片统一存放在 `源文件/`，可通过网页侧栏进入，不纳入资料列表。

16 MiB 以内的 PDF 随站点部署，可直接预览。较大的 PDF 通过 GitHub 查看、下载，避免完整资料超过 Pages 的容量限制。文件链接固定到部署对应的提交。

完整检出仓库后运行：

```sh
python3 site/build.py
python3 -m http.server 8080 --directory site/dist
```

稀疏检出本地预览可提供 GitHub recursive tree API 的 JSON 快照：

```sh
python3 site/build.py --tree /path/to/tree.json --preview
```

预览模式仅链接本地已有 PDF；正式部署缺少文件时会报错，不会发布不完整文件包。

分类以核对内容后的归档目录为准，不按文件扩展名或标题关键词推断：真题、回忆卷及其配套文件归入期中或期末；知识点整理、复习提纲与解题笔记归入笔记；教材及配套阅读材料归入教材。源文件保留原有学期、课程和分类层级；LaTeX 工程整体位于 `源文件/LaTeX 试卷/`，其模板、字体和题图的相对路径保持不变。

## 自托管发布

从对应提交的成功构建中下载名为 `github-pages` 的 artifact，解包其中的 `artifact.tar`，将 HTML、CSS、JavaScript、`catalog.json` 和 `files/` 一并同步到独立静态目录。站点使用相对路径，可以部署在 `/xmu-am/` 等子路径下；静态服务器应将不带末尾斜杠的入口重定向到带斜杠版本，并支持 PDF Range 请求。

只部署构建产物，不复制整个仓库；不要使用 `--preview` 生成的软链接目录。大于 16 MiB 的 PDF 继续通过 GitHub 获取，不占用自托管站点空间。独立部署目录应位于博客发布目录之外，避免博客更新时被清理。
