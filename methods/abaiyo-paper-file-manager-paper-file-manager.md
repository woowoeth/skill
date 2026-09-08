---
name: paper-file-manager
description: 创建和管理科研论文的初稿、回稿目录，按格式归档图片、数据、正文、参考文献和审稿材料，并切换当前写作阶段。用于整理本地论文项目文件；不负责撰写或评审论文本身。
---

# 科研论文文件管理

使用 `scripts/paper_manager.py` 创建并整理一篇论文的本地工作目录。所有命令都显式传入论文目录，不假定固定磁盘或用户目录。

## 工作原则

- 新论文先执行 `init`。默认阶段为“初稿”，同时创建初稿和回稿的标准目录。
- 用户说明初稿已完成、进入修改或回稿阶段时，执行 `switch <论文目录> 回稿`。切换只影响后续归档，不迁移已有文件。
- 用户要求切回初稿时，执行 `switch <论文目录> 初稿`。
- 整理论文目录内的文件时，先让文件进入 `待整理`，再执行 `sort`。该操作会移动其中可识别的文件。
- 从论文目录外导入时使用 `ingest`，默认复制以保留来源；只有用户明确要求移动源文件时才加 `--move`。
- 不凭猜测归类含义不清的 PDF。无法识别的文件保留或复制到 `待整理`，并把结果告诉用户。
- 不覆盖同名文件。脚本会自动追加序号。
- 操作前确认论文目录和输入文件正是用户指定的对象。不要扫描或整理无关目录。

## 标准目录

每篇论文包含：

```text
论文目录/
├── 待整理/
├── 初稿/
│   ├── 图片/
│   ├── 数据/
│   ├── 正文/
│   └── 参考文献/
├── 回稿/
│   ├── 图片/
│   ├── 数据/
│   ├── 正文/
│   ├── 参考文献/
│   └── 审稿意见与回复/
└── .paper-manager.json
```

## 常用命令

从 skill 目录运行：

```bash
python scripts/paper_manager.py init "<论文目录>"
python scripts/paper_manager.py sort "<论文目录>"
python scripts/paper_manager.py ingest "<论文目录>" "<文件1>" "<文件2>"
python scripts/paper_manager.py switch "<论文目录>" 回稿
python scripts/paper_manager.py status "<论文目录>"
```

添加自定义目录，可同时登记扩展名或文件名关键词规则：

```bash
python scripts/paper_manager.py add-folder "<论文目录>" "补充实验" --stage 回稿
python scripts/paper_manager.py add-folder "<论文目录>" "代码" --stage both --extension .py --extension .ipynb --keyword script
```

`--stage` 可用 `初稿`、`回稿`、`active` 或 `both`。自定义规则优先于内置格式分类；用户明确指定目标目录时，直接尊重其选择。

## 归档判断

- 常见位图、矢量图和绘图文件进入“图片”。
- Origin、Excel、CSV、MAT、HDF5、NumPy 等进入“数据”。
- Word、LaTeX、Markdown、RTF 和 OpenDocument 正文进入“正文”。
- BibTeX、RIS、EndNote、PubMed 等文献管理格式进入“参考文献”。
- PDF 根据文件名关键词判断为参考文献、正文或审稿材料；无法判断时进入“待整理”。
- 审稿意见、回复信和决定信只在回稿阶段进入“审稿意见与回复”。

完成操作后，报告当前阶段、实际移动或复制的文件、仍在待整理中的文件及任何同名重命名。

