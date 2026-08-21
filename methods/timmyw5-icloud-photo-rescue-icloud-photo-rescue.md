---
name: icloud-photo-rescue
description: 把苹果官方 iCloud 照片导出（privacy.apple.com 的分部备份）整理成本地照片库：按拍摄年/月归档、还原相册、生成缩略图和离线相册界面。当用户要"整理 iCloud 导出照片""停用 iCloud 后整理备份""照片按日期归类""还原苹果相册"时使用。执行前必须 dry-run 并经用户确认。
---

# iCloud 照片导出 → 本地照片库

你要把苹果官方导出的照片备份整理成 `年/月` 结构的本地照片库，并还原相册、生成可浏览界面。以下是经过 3.8 万张照片实战验证的方法论。**红线：任何移动文件的步骤前，必须产出 dry-run 报告并获得用户明确确认。**

## 第 0 步：确认前提

- 用户数据必须是 privacy.apple.com「获取数据副本」的导出（特征：`iCloud Photos Part N of M` 或本地化命名的"第 N 部分"文件夹）。如果用户还没导出：提醒**先导出并验证完整、再取消订阅**（停付后苹果只保留有限宽限期）。
- 平台 macOS。检查工具：`python3`、`sips`（自带）；`exiftool`、`ffmpeg` 可用 brew 装（可选增强，装不上有回退）。
- 目标硬盘剩余空间：移动方式（同盘 rename）几乎不占额外空间；复制方式需要 ≥ 导出体积。问用户选哪种（复制保留原始导出，更稳妥；移动快且省空间）。

## 第 1 步：勘察导出结构（只读）

苹果导出的已知事实（先验证，格式可能有变体）：

```
Part N/
├── Photos/
│   ├── <几千个媒体文件平铺>          ← 文件系统时间=下载时间，不可用
│   ├── Photo Details-1.csv … -K.csv  ← 元数据表
│   └── Photo Details.csv             ← ⚠️ 每部分还有一个无编号的，glob 时别漏
├── Recently Deleted/                 ← 用户删过但仍导出的照片（含自己的 Photo Details）
├── Albums/<相册名>.csv               ← 仅第 1 部分有；内容是 imgName 文件名列表
├── Memories/                         ← 自动生成的回忆，可忽略
└── icloud-photos-iCloudUsageData*.zip ← 上传事件日志，仅覆盖导出前约 2 个月，一般用不上
```

`Photo Details*.csv` 列：`imgName, fileChecksum, favorite, hidden, deleted, originalCreationDate, viewCount, importDate`。日期格式 `"Sunday February 9,2025 1:36 AM GMT"`（**GMT！**）。

勘察时实测并报告给用户：各部分文件数、CSV 覆盖率（正常应 98%+）、总体积、有无 RAW/特殊格式。

## 第 2 步：构建索引 + dry-run（只读）

对每个媒体文件确定拍摄日期，优先级链：

1. **EXIF/内嵌时间**（exiftool 批量 `-fast2`，回退 sips `-g creation`；视频用 `CreationDate`(带时区,优先) → `CreateDate`）——这是拍摄地当地时间，最准
2. **CSV `originalCreationDate`**（GMT）→ 按用户主要生活时区折算（先问用户）。误差：旅行期截图可能 ±1 天，提前告知
3. 都没有 → `未知日期` 文件夹

已知的坑（都要处理）：

- **Live Photo 伴生视频**：`IMG_xxxx-1.MOV` 不在 CSV 里。剥 `-1` 后缀与同目录同名图片配对，**永远跟随图片的日期与去向**，不要独立判断（导出重打包可能把下载时间写进其内嵌元数据）
- **跨部分重复**：不同 Part 可能含相同 `fileChecksum` 的同名文件。保留一份（优先 Photos 里的，其次按部分序），其余移入 `重复文件/` 待用户复查，不要直接删
- **日期合法性**：EXIF 年份超出 [1995, 当前年+1] 视为无效，落到下一级
- **非常见扩展名**：RAW（.nef/.cr3/.cr2/.arw）、.heif、.pic 也是用户的照片，媒体扩展名清单必须包含；无扩展名文件跳过并报告
- **文件名冲突**：目标同名时加 `__pN` 后缀；Live 伴生跟随图片的改名规则

产出 dry-run 报告：各年月文件数、日期来源占比、重复数、无日期清单。**给用户看，确认后才进第 3 步。**

## 第 3 步：执行归档

- 目标结构：`照片库/YYYY/YYYY-MM/`；`Recently Deleted` → `已删除归档/YYYY-MM/`；重复 → `重复文件/`
- 每一次物理移动追加写 `moves_log.csv`（原路径,新路径,标签）——这是回滚的生命线
- 完成后对账：目标库文件计数 == 源清单计数；抽查数个跨年份文件验证 EXIF 与所在月份一致

## 第 4 步：相册 + 缩略图 + 界面

- **相册**：解析 `Albums/*.csv` 的 imgName → 映射到新路径。物化为 `相册/<名>/` 内的**相对符号链接**（一张照片可属多相册且不占空间；相对链接可在整个库改名/换盘后存活）
- **缩略图**：`sips -Z 400` 转 JPEG 到 `.thumbnails/<原相对路径>.jpg`（追加 .jpg 避免 a.heic/a.jpg 冲突；HEIC 借此变得浏览器可显示）；视频 ffmpeg 抽首帧；RAW 用 `exiftool -b -PreviewImage` 提取内嵌预览。脚本必须支持断点续跑（跳过已存在）
- **界面**：单文件 HTML + `<script src>` 加载 index.js（绕过 file:// 的 CORS）。视图：时间线（月分组+懒加载，勿一次渲染几万 DOM）、相册、收藏（CSV 的 favorite 列）、搜索、灯箱
- **本地服务**（若用户要"真实文件操作"的删除/归档/建相册）：Python 标准库 HTTP 服务，只绑定 127.0.0.1，POST /api/op 执行文件移动并原子重写 index.js（临时文件+rename）、更新相册符号链接。前端 file:// 打开时降级为只读模式

## 工程坑清单（实战踩过）

- 机械硬盘重 IO 下会短暂停滞：批处理脚本误报大量失败时，先查挂载状态再续跑；并行度 ≤2
- 端口探测 socket 要设 `SO_REUSEADDR`，否则 TIME_WAIT 会误判端口被占
- Finder 双击 `.command` 的 shell 无 UTF-8 locale：自动打开浏览器的 URL 里不要出现非 ASCII 字符（文件名用英文，或百分号编码）
- 沙盒化的辅助进程可能没有外接硬盘读权限：起服务用用户 shell 环境
- `ffmpeg -ss 0.5` 会让短视频抽帧失败：不带 `-ss` 取第一帧
- 服务端一切路径必须校验落在库目录内（防路径穿越）；相册名过滤 `/ : \` 等字符
- 用户可能在 Finder 手动删文件造成索引悬空：定期用"索引 vs 磁盘"对账脚本清理，注意相册按序号引用照片，删记录必须同步重映射相册索引

## 验证清单

- [ ] dry-run 报告经用户确认
- [ ] 移动后文件计数对账一致
- [ ] 抽查多个年份的文件：EXIF 日期与所在文件夹一致
- [ ] 相册链接 `ls -la` 可解析、Finder 双击能打开
- [ ] 界面三视图 + 搜索 + 灯箱实测
- [ ] （如有服务）curl 测每个 action + 非法路径拒绝 + kill -9 后索引完好
