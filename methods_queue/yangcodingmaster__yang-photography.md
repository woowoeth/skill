---
name: add-gallery-series
description: >-
  把一个新照片系列录入这个摄影作品集网站（往 Gallery 加一个系列）。当用户在
  assets/images/gallery/ 下新建了一个照片文件夹、希望把它加进网站时使用 —— 触发词如
  「加一个系列」「把 X 录入 gallery / 作品集」「新系列」「把这个文件夹加进去」「放在 XX 旁边，命名 XX」。
  会自动：探测真实图片格式、把 HEIC/HIF 等转成网页用 JPEG 并压缩（长边 2560 / 质量 90）、
  规范命名、写入 data.js 的 allSeries 与 allPhotos（每字段独占一行、文本字段留空待作者填）。
  即使用户只说「我又加了个文件夹，帮我弄进去」「把这批照片放到作品集里」，只要是往本作品集加照片系列，
  就应使用此 skill。不适用于 Archive 散片（那是 allArchive，只放 src/alt，结构不同）。
---

# 给 Gallery 添加一个新照片系列

## 这个 skill 做什么

作者会往 `assets/images/gallery/` 丢一个新文件夹（名字随意、照片可能是相机直出的 HEIC），
然后说一句「加进去，放在某某旁边，叫什么名字」。这个 skill 把后续工作流固化下来：
**把原始照片处理成网页规格，并正确写进 `data.js`，让它出现在 gallery 页。**

核心目标有两个，缺一不可：
1. **图片要变成网页能用、加载快的样子**（HEIC→JPEG、缩到合适尺寸、压缩）。
2. **`data.js` 要被正确改对**（位置、字段、格式都符合本仓库约定）。

## 动手前必读：本仓库的关键约定

- **`data.js` 是唯一数据源**，所有内容只改这里。完整数据结构见仓库根的 `CLAUDE.md`（"data.js 数据结构详解"一节）。
- **普通系列** = `allSeries` 里一个元数据对象 + `allPhotos[id]` 里一个照片数组。本 skill 主要处理普通系列。
- **命名规则**：文件夹名 / `id` 一律**连字符小写**（`Defocused UK` → `defocused-uk`），不能有空格/逗号/大写（部署到 GitHub Pages 会变 `%20`）。照片**零填充顺序命名** `01.jpeg`、`02.jpeg`…
- **封面靠 `cover` 字段显式指定**（不再默认取第一张）；省略会导致 gallery 缩略图空白，绝不能漏。
- **压缩标准固定**：HEIC→真 JPEG、**长边 2560px、质量 90**。这是网页展示的安全甜点（视觉无损、体积约降到 1/10）。**写死，不要问、不要改**——除非作者明确说要印刷级别或别的尺寸。
- **文本字段一律留空待作者自己填**（caption/date/location/desc/meta，以及没明确给的 titleZh/titleEn/year/location/descZh/descEn）。这是作者的明确偏好：他要逐张灵活打磨文案，skill 只搭好骨架。

## 先问清楚：这几件事 skill 决定不了，要和作者确认

| 需要确认 | 默认建议 |
|---|---|
| **id / 文件夹名** | 原文件夹名转连字符小写，跟作者复述一次确认 |
| **插入位置** | 作者会说（"放虚焦旁边" = 插在那个系列对象之后） |
| **titleZh / titleEn** | 作者给了就用；没给就留空。别自己猜中文标题 |
| **普通系列还是分章系列** | 默认普通系列。分章系列结构不同，见文末说明 |

作者已给的信息（如「命名虚焦之二」）直接用，不必再问。

## 工作流

### Step 0 — 探测真实情况（每次必做，别想当然）

为什么：踩过坑。相机直出的文件**扩展名经常说谎**——`.jpeg` 实际是 HEIC/HIF；
有的文件名还带**前导空格**（` 1.jpeg`），会让后续路径匹配失败。所以先看真身：

```bash
cd "assets/images/gallery/<原文件夹>"
for f in *; do printf '[%s] ' "$f"; file -b "$f" | sed 's/,.*//'; done
```

看三件事：① 真实格式（`ISO Media` / `HEIF` = HEIC，要转码）② 文件名有没有前导空格（`[` 紧贴文件名=没有）③ 数量和编号。

### Step 1 — 转码 + 压缩 + 规范命名

直接用脚本（这一步每次完全一样，已固化）。它会探测格式、转 JPEG、缩到长边 2560/质量 90、
自然排序后零填充命名，并自检。**它不删源文件夹**，过程中不丢东西：

```bash
bash .claude/skills/add-gallery-series/scripts/convert_photos.sh \
  "assets/images/gallery/<原文件夹>" \
  "assets/images/gallery/<hyphenated-id>"
```

脚本能处理：HEIC/HIF/heic 混合扩展名、带前导空格的文件名、横竖混排。

### Step 2 — 校验通过后，再删源文件夹

确认脚本输出"校验问题 0 处"、数量对得上，**然后才**删旧文件夹：

```bash
rm -rf "assets/images/gallery/<原文件夹>"
```

### Step 3 — 写入 data.js（两处）

先备份，**先读最新的 `data.js`**（作者可能正同时在 IDE 改文案，读旧的会冲掉他的改动）：

```bash
cp data.js /tmp/data.js.bak
```

然后做两处插入（用脚本化的 Python 替换、或精准 Edit 都行，关键是锚点唯一、不破坏他人改动）：

1. **`allSeries`** —— 在作者指定的系列对象之后插入一个新对象（模板见下）。
2. **`allPhotos`** —— 加一个同名 key 的照片数组，**每张照片每个字段独占一行**（模板见下），文本字段留空。

> ⚠️ 若用脚本批量替换，务必"先读现盘文件、在内存里改、再写回"，并对锚点 `assert count==1`，
> 避免覆盖作者并发的手动编辑。

### Step 4 — 验证

```bash
node --check data.js        # 语法
```

再加载核对：系列顺序对不对、照片数对不对、**每个 `src` 都能对应磁盘上真实文件**。
（`var` 声明不暴露给 require，用 `new Function(code + ...)` 在上下文里取出 allSeries/allPhotos 来核对。）

预览验证封面能否加载时注意一个**缓存陷阱**：浏览器会缓存 `<script src="data.js">`，
普通刷新看到的还是旧数据。绕开办法：`fetch('/data.js?fresh='+Date.now())` 抓新鲜文件、
重跑 gallery 的渲染循环，再检查新封面 `img.complete && img.naturalWidth>0`。

### Step 5 — 报告 + 例行提醒

报告改了哪些文件、做了什么。并提醒作者：
- **HEIC 原片要另存备份**（网页版是缩小过的，不能用于印刷/二次修图）。
- 预览硬刷新用 **Cmd+Shift+R**。
- 若发现作者正在并发编辑 `data.js`，如实说明、确认他的改动已保留。
- 若系列是某个已有系列的"续集"，留意**中英文编号风格统一**（如第一卷英文是 `Defocused (i)`，
  第二卷宜 `Defocused (ii)` 而非 `Defocused II`）——但不要替他改这一行，提示他自己顺手调，避免和他的编辑器缓冲区撞车。

## 模板

### allSeries 条目（对齐现有写法，字段逐行对齐）

```javascript
  {
    id:       'defocused-uk',
    // 普通系列（无 type），封面用 cover 字段显式指定
    cover:    'assets/images/gallery/defocused-uk/01.jpeg',
    titleZh:  '虚焦之二',
    titleEn:  'Defocused II',
    year:     '',
    location: '',
    descZh:   '',
    descEn:   '',
  },
```

`titleZh/titleEn` 作者给了就填、没给留空；`year/location/descZh/descEn` 一律留空待填。`cover` 必填，指向 `01.jpeg`。

### allPhotos 照片对象（每字段独占一行 —— 作者要逐张手填，绝不能压成一行）

```javascript
  // ── <中文名> (<id>) 系列 ──────────────────────────────────
  // 文字字段先留空，想好了再逐张填；空字段不会显示
  '<id>': [
    {
      src:      'assets/images/gallery/<id>/01.jpeg',
      alt:      '',
      caption:  '',
      date:     '',
      location: '',
      desc:     '',
      meta:     '',
    },
    // ... 其余照片同样格式，01 02 03 ... 顺序排列
  ],
```

字段对齐：值都从 `location: ` 之后那一列开始（`location` 最长，其余补空格对齐），照搬 Defocused 系列的样子。

## 完整例子（一次真实运行）

> **作者**：「我又加了个 Defocused UK，放虚焦旁边，命名虚焦之二」
>
> 0. **探测** → 7 张，真身 HEIC/HIF，无前导空格
> 1. **脚本转换** → `defocused-uk/01–07.jpeg`，JPEG / 2560 长边 / 0.4–0.5MB
> 2. **校验 0 问题后删** 旧 `Defocused UK/`
> 3. **写 data.js** → allSeries 在 `Defocused` 后插入 `虚焦之二 / Defocused II`（cover=01.jpeg）；
>    allPhotos 加 7 张多行空字段对象
> 4. **验证** → `node --check` OK、顺序相邻、7 张 src 全部命中磁盘、封面 `loaded:true`
> 5. **报告** → 并发现作者已把原作改名 `虚焦之一 / Defocused (i)`，提示英文编号风格统一

## 边界情况：分章系列（sectioned）

本 skill 默认处理**普通系列**。如果作者要加的是**分章系列**（一个系列内分多个主题章节，
如年度合集 "Photos of 2025"），结构不同：

- `allSeries` 里要加 `type: 'sectioned'`，`cover` 仍必填。
- 照片不进 `allPhotos`，而进 `allChapters[id]`，按章节数组组织（每章有 titleZh/titleEn/descZh/descEn/photos）。
- 照片文件按子文件夹分章存放，编号可全局连续。

图片处理（Step 0–2）完全一样；只是 Step 3 写的是 `allChapters` 而非 `allPhotos`。
详见 `CLAUDE.md` 的 "allChapters — 分章系列结构" 和 "如何添加一个分章系列"。
