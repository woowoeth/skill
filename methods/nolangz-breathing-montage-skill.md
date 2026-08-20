---
name: breathing-montage
description: Style-agnostic grammar for high-density editing with breathing room ("呼吸式高密度剪辑") — a frame-level rhythm skeleton for 15–120s short films, plus the AI-production discipline to execute it with image/video generation models. Use whenever the user wants: high-density or fast-cut editing that still breathes; a strobe/flash climax sequence; subliminal insert design (2–6 frame cuts); a two-worlds opposition montage; a rhythm skeleton or cut architecture for a short film, brand film, trailer, or vertical video; converting a storyboard into frame-exact edit structure; writing S4 multi-shot timestamped prompts with reference frames; or phrases like 高密度剪辑, 呼吸感节奏, 频闪段, 插帧, 剪辑骨架, 密度曲线, 卡点但不卡BPM, breathing montage, strobe climax, insert run. Trigger even if they only ask to "make the edit faster but keep it breathing" or "give my video an ANOMALY-style rhythm".
license: MIT
---

# Breathing Montage · 呼吸式高密度剪辑语法

高密度 ≠ 快。高密度 = **双峰分布**：≤12 帧的阈下插帧 × ≥2 秒的长呼吸，中间地带（~1 秒镜头）是无态度区，占比压到最低。密度的价值来自**起伏**——没有崩塌段的爆炸只是噪音。

本 skill 只提供语法，不携带任何视觉风格。所有色板、材质、年代、题材由项目自带。

## 五条铁律（违反任何一条，节奏即失效）

1. **双峰镜长法**：镜头要么是插帧（≤12f，帧数绝对，永不随片长缩放），要么是呼吸（≥2s）。1 秒级镜头 ≤ 总镜数 15%。
2. **一帧白闪法**：白闪永远恰好 1 帧纯白。全片大白闪 4 次（段界/波峰），小白闪 ≤3 次。
3. **贴词不贴拍**：切点贴 VO 名词与大音效，不贴 BPM 网格。VO 写成散文诗，每行一个"可翻译名词"，名词落地帧 = 切点。
4. **密度曲线形状**：低—中—中高—爆炸—崩塌。加速必须三段抬升（约 0.6s→0.2s）、顶点白闪、之后立刻给长呼吸——禁线性加速；频闪段之后禁渐慢，是崩塌不是减速带。
5. **溶解配额**：正片零溶解；全片仅彩蛋入口允许一次（它就是"反语法"的语法标记）。

## 工作流

1. 定二元命题与四维反义表 → 读 `references/worlds-and-color.md`
2. 定五锚点（情绪/母题/锚物/断裂/终帧）→ 同上文件末节
3. 按目标时长缩放九段骨架 → 读 `references/rhythm-skeleton.md`
4. 构建插帧母题银行与频闪谱 → 读 `references/inserts-and-strobe.md`
5. 写 VO 散文诗并做名词-切点对齐表 → `references/rhythm-skeleton.md` §VO
6. 排九段声音弧与镜头语权表 → 读 `references/sound-design.md`、`references/camera-grammar.md`
7. 生成与提示词（静帧优先、S4 形态）→ 读 `references/ai-production.md`
8. 发送/交付前跑 `assets/qc-checklist.md`；新项目起手用 `assets/skeleton-worksheet.md` 填空。

## 参考文件路由

| 需要 | 读 |
|---|---|
| 九段结构、时长缩放、加速/崩塌/真空规格、VO 名词落点法 | `references/rhythm-skeleton.md` |
| 插帧帧数语义、母题银行、信号元素渐进植入梯、频闪谱构造、负片规则 | `references/inserts-and-strobe.md` |
| 二元命题、色权分治、信号色配额、双帧率质感、缩略图可读、转场经济学、同框法、五锚点 | `references/worlds-and-color.md` |
| 静帧优先生产法、S4 提示词形态、参考帧角色纪律、端态法、排除项纪律、优先级声明 | `references/ai-production.md` |
| 声权分治、动机纪律、九段声音弧、采样层处理、混音优先级 | `references/sound-design.md` |
| 双峰机位法、镜头语权分治、运动语义预算、速度阶梯、结构性减速点、转场机位 | `references/camera-grammar.md` |

---
*戏剧学检查层（行为替换情绪、三细节、五锚点）改写自并致谢：smixs/visual-skills（Serge Shima，CC BY 4.0）、wuwangzhang1216/DirectorSKILL（MIT）。*
