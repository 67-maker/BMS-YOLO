# BMS-YOLO IEEE Access 论文 — 项目记忆

## 编译环境
- 本机已装 **TeX Live 2026**，二进制在 `/d/texlive/2026/bin/windows/`（pdflatex/xelatex/bibtex 均可用）。
- 探测技巧：`which` 可能漏检，用 `command -v pdflatex` 或检查该目录。
- 论文源目录：`D:\Claude program\IEEE ACCESS_latex\`（主文件 `access_final.tex`，类 `ieeeaccess.cls`）。
- 标准编译流程（在该目录、PATH 含 tex 二进制）：
  `pdflatex -interaction=nonstopmode access_final.tex` → `bibtex access_final` → `pdflatex` ×2。
- 文末用 `\bibliographystyle{IEEEtran}` + `\bibliography{references}`，BibTeX 数据库 `references.bib`。
- 产物 `access_final.pdf` 约 85 MB（因 qualitative_fig_*.pdf 等大图嵌入），属正常。

## 易错点
- `access_final.tex` 的 `\author{...}` 必须闭合花括号，否则 `\address` 被吞入参数导致编译失败。
- Fig. 1 整体架构图由 `generate_architecture.py`（matplotlib）生成 `figure1_architecture.pdf`，在 tex 中 `\includegraphics[width=\linewidth]{figure1_architecture.pdf}`。
