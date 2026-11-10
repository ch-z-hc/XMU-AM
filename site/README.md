# 网页版

入口：https://ch-z-hc.github.io/XMU-AM/

`main` 分支更新后，GitHub Actions 自动生成课程目录并部署到 GitHub Pages。目录来自 Git 跟踪的各学期资料；`LaTeX 试卷/` 中重复的 PDF 不重复列出，源码保留仓库入口。

16 MiB 以内的 PDF 随站点部署，可直接预览。较大的教材与其他格式通过 GitHub 查看、下载，避免完整资料超过 Pages 的容量限制。文件链接固定到部署对应的提交。

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
