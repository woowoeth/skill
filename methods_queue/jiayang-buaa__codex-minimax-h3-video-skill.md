---
name: codex-minimax-h3-video
description: 使用 Z-Image、MiniMax H3 Director、MiniMax H3 与 HyperFrames 生成、剪辑并闭环验收连续视频。适用于从创意或参考视频出发制作首帧/首尾帧可控的本地 AI 短片；不用于单张图片生成或与视频无关的普通剪辑。
---

# Codex × MiniMax H3 自动成片与验收

把 Codex 作为总编排器：拆分分镜、编写提示词、选择帧约束模式、顺序调用 ComfyUI、组织 HyperFrames 剪辑，并依据可观察证据决定接受或局部返工。

## 开始前

1. 读取 [references/environment.md](references/environment.md)，检查 ComfyUI、模型、Director、Node.js、HyperFrames 与 FFmpeg。
2. 先运行只读检查：`./scripts/check_environment.ps1 -ComfyUIRoot $env:COMFYUI_ROOT`。
3. 不要把模型、API Key、个人绝对路径或生成缓存提交到仓库。
4. 缺少环境时，先报告下载体积、磁盘位置和显存卸载影响；只有用户授权后才安装或下载。

## 生成流程

### 1. 形成镜头计划

将目标视频拆成每段 4–15 秒的因果动作。为每段写明时间范围、画幅、人物与场景锁定项、对白、环境声、动作微时间线、起始状态和结束状态。相邻镜头的下一段起始状态必须等于上一段锁定的结束状态。长对白宁可拆段，不要压缩成不自然语速。

### 2. 选择帧约束模式

字段和示例见 [references/job-modes.md](references/job-modes.md)。

- `first_frame`：Z-Image 生成首帧，适合开放式动作。
- `first_last_frame`：Z-Image 同时生成首尾帧，适合必须到达指定结尾的动作。
- `existing_first_frame`：使用上一段真实末帧续拍，是默认连续分镜方式。
- `existing_first_last_frame`：固定已有首尾帧，只重做中间内容，适合局部修复。

首尾帧提示词必须锁定人物身份、服装、场景、光线、镜头侧和关键道具。仅需要首帧时不要凭空生成尾帧。

### 3. 顺序生成

使用 `scripts/invoke_pipeline.ps1`。先 `-ValidateOnly`，确认模式、节点、模型和帧数，再提交真实任务。

```powershell
./scripts/invoke_pipeline.ps1 -JobFile ./templates/job-first-frame.example.json -ComfyUIRoot $env:COMFYUI_ROOT -ValidateOnly
```

- 默认拒绝向非空队列追加任务；不要因为等待中断而重复提交。
- 每段完成后核对 ComfyUI history 与实际输出文件。
- 用 `extract_last_frame.ps1` 提取真实末帧，再作为下一段输入。
- 若画面出现大字、漏词、换脸或跳变，只重做受影响镜头；未经用户确认最多自动重试一次。

### 4. HyperFrames 剪辑

使用 HyperFrames 保存正式、可编辑的剪辑工程：

1. `npx hyperframes init <project> --video <clip> --non-interactive`
2. 建立时间线、字幕和必要的直接切换；不要用转场掩盖不连续。
3. 依次运行 `lint`、`inspect`，再运行高质量 `render`。
4. 可用 `scripts/render_hyperframes.ps1` 执行标准验证与渲染。

FFmpeg 只作为格式统一、末帧提取、技术检测和局部修复工具；正式时间线优先保存在 HyperFrames 中。

### 5. 验收闭环

读取 [references/qa.md](references/qa.md)，至少检查：输出规格和音轨；ASR 是否覆盖指定对白；切点前后人物、构图、道具和动作状态；黑帧、生成大字、水印、换脸和闪烁；HyperFrames 字幕是否越界、遮脸或重复。

验收结论应区分通过、可接受偏差、必须局部返工。不要因为渲染命令成功就宣称成片合格。

## 交付

交付最终 MP4、HyperFrames 工程、镜头清单和简短 QA 报告。说明各镜头使用的帧约束模式，以及仍存在的可见限制。
