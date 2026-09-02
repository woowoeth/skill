---
name: douban-movie-weekly
description: Create or update a Chinese weekly movie-recommendation HTML report from Douban Movie Calendar daily entries, using the bundled reusable HTML and email templates, public poster URLs, and verified movie metadata. Use when generating the weekly report, refreshing its data, or maintaining the recurring movie-calendar task.
---

# 豆瓣电影周报

使用本 skill 生成或刷新每周电影日历周报。`assets/weekly-template.html` 和 `assets/email-template.html` 是唯一的视觉与版式来源；只替换数据和占位符，不在运行时重写 CSS、布局或邮件结构。

## 数据获取

1. 使用用户配置的时区；未配置时使用运行环境的本地时区，计算最近 7 个自然日。
2. 优先读取公开的 2026 电影日历镜像：<https://yes1am.github.io/douban-movie-calendar/>。
3. 按 `MM.DD` 找到每日条目，记录日期、片名、豆瓣评分、豆瓣链接、日历文案和推荐依据。
4. 不要使用豆瓣一周口碑榜、热门榜或个性化推荐替代电影日历。
5. 为每部电影补充能够可靠核实的年份、导演、类型、主演和简短不剧透简介；详情页受限或字段无法核实时不要编造。
6. 镜像不可访问或缺少日期时，在周报中记录缺失原因，不要用其他电影补位。

## 海报

- 不抓取豆瓣图片；优先使用 Wikimedia Commons/Wikipedia 或其他能确认片名对应关系的公开图片直链。
- 只使用已确认属于该片的图片 URL，不把搜索结果页当作图片 URL。
- 按模板的海报区域填入中文 `alt`、`loading="lazy"` 和失败时的渐变 fallback。

## 配置

个人设置只能放在自动化任务或运行时配置中，不要写入 skill 或模板：

- `recipient_email`：收件地址；
- `sender_account`：已连接的 Gmail 发件账户；
- `greeting`：邮件称呼，默认“你好”；
- `send_email`：是否发送，默认关闭，只有用户明确授权后启用；
- `send_day`、`send_time`、`timezone`：发送日、时间和时区，默认周日、本地时间；
- `report_output_dir`：本地 HTML 周报目录，默认当前项目的 `outputs/`；
- `report_filename_pattern`：默认 `week{iso_week} {start_month}.{start_day}-{end_month}.{end_day} 电影推荐.html`，其中 `{iso_week}` 为周一所属日期的 ISO 周序号，月日不补零。

分享 skill 时只分享 skill 文件和模板，不分享包含邮箱、令牌、任务 ID 或本地路径的自动化配置。

首次运行或配置缺失时，先确认：是否发邮件、发件账户、收件地址、称呼、发送日/时间/时区和本地保存目录。未确认发送前只生成 HTML，不发邮件。

## 模板与邮件

- HTML 周报从 `assets/weekly-template.html` 开始生成。
- 邮件正文从 `assets/email-template.html` 开始生成，并沿用同一批电影数据和海报。
- 只替换模板占位符，不改变模板结构；模板需要改变时先修改 skill 资源。
- HTML 必须自包含；邮件使用内联样式、公开海报直链，并同时提供可读的纯文字 fallback。
- 邮件正文应完整呈现周报，不发送 HTML 附件，也不添加附件提示。
- 周报至少包含每日片目、全部可获取的电影卡片、3 部本周候选及理由、来源和数据日期。

## 运行流程

1. 按本地时区计算周报范围并读取 7 个日历条目。
2. 补齐可靠元数据和海报 URL，标记无法核实的字段。
3. 填充模板占位符，保持模板结构。
4. 将文件保存到 `report_output_dir`，按 `report_filename_pattern` 命名；目录不存在时创建，不能覆盖未授权的已有文件。
5. 周一至周六只记录数据；进入本地时区的周日后才发送完整周报。用户要求预览时立即生成当前范围的 HTML。
6. 邮件发送成功后只做简短确认；失败时说明原因，不要声称已发送。

## 模板占位符

生成文件时不得残留以下占位符：

- `{{WEEK_RANGE}}`、`{{CARDS}}`、`{{PICKS}}`、`{{SOURCE_NOTE}}`
- `{{ITEM_COUNT}}`、`{{GREETING}}`、`{{EMAIL_CARDS}}`、`{{EMAIL_PICKS}}`

最终检查：占位符已全部替换，卡片数量与条目一致，图片失败时版式仍完整，邮件 HTML 和纯文字 fallback 均可读，正文没有附件提示。
