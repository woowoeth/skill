name: upscale
description: "Turn low-quality images into cleaner, sharper, detail-rich HD images while preserving composition and subject identity. 将低质量图片处理成更干净、更锐利、细节更完整的高清图，并默认保留原构图和主体身份。"
---

# Upscale

Shortcut trigger:

- `/upscale`

快捷指令：

- `/upscale`

This skill is for turning one image into a cleaner, sharper, high-definition result with fuller detail and better usability.

这个 skill 用来把单张图片处理成更清晰、更锐利、细节更完整、可用性更高的高清结果。

The core rule is not “make it bigger.”

核心不是“单纯放大”。

The core rule is:

> preserve the image logic, then make it look materially cleaner and more detailed.

核心规则是：

> 先保住画面逻辑，再把清晰度和细节真正做上去。

## When to use it

Use this skill when the user wants any of these:

用户有下面这些需求时，就该用这个 skill：

- upscale
- HD redraw
- cleaner image with preserved composition
- sharper image without redesign
- detail recovery
- low-quality image repair

## What success means

Success requires:

成功标准：

1. the image looks cleaner, sharper, and more usable
2. the important details are materially improved without changing the image logic

If the user explicitly needs high-resolution delivery, success also requires:

如果用户明确要求高分辨率交付，还需要满足：

3. the delivered file has a real long edge of `3840px` or another requested export size

## Default behavior

- ask as little as possible
- infer the safest route from the image
- preserve composition by default
- preserve subject identity by default
- export a real high-resolution file when the requested delivery standard requires it

默认行为：

- 尽量少问
- 从图片本身推断最稳妥的路线
- 默认保构图
- 默认保主体身份
- 如果交付标准需要，就导出真实高分辨率文件

## Step 1: Classify the image

First decide whether the image is:

先判断图片属于哪一类：

### A. Good for redraw-style enhancement

Usually includes:

- illustrations
- stylized 3D renders
- toys and model objects
- product images with clear outlines
- macro images with a clear focal subject
- simple posters or graphics with manageable text

### B. Risky for redraw-style enhancement

Usually includes:

- photoreal close-up portraits
- dense text
- UI with lots of tiny details
- infographics
- images whose realism depends on subtle skin or lighting transitions

If the image is risky, use a conservative route.

如果图片风险高，就走保守路线。

## Step 2: Choose the route

### Route 1: Structure-preserving redraw

Use when the image is good for redraw-style enhancement.

适合那些本身就适合高清转绘增强的图。

Goal:

- keep composition
- keep subject relationships
- improve edge quality
- restore cleaner detail

If the tool supports multi-image or multi-step image editing, use this logic:

1. lock structure
2. lock major color relationships
3. recover visual logic and finish

If the tool only supports one-pass editing, still instruct it to:

- preserve exact framing
- preserve subject placement
- improve clarity without redesign

### Route 2: Conservative realistic cleanup

Use for portraits, text-heavy images, and realism-sensitive photos.

适合人像、文字密集图、以及对写实质感敏感的照片。

Goal:

- reduce softness
- improve clarity carefully
- avoid identity drift
- avoid plastic skin
- avoid warped text

Do not push style changes or reconstruction too aggressively.

## Step 3: Prompting rules

Regardless of route:

不管走哪条路线，都要明确写清：

- explicitly say to preserve composition
- explicitly say to preserve proportions
- explicitly say not to add or remove objects
- explicitly say not to change identity when a person is present
- explicitly say what should become clearer

### Good prompt pattern

Describe:

好的 prompt 应该写清：

- what the subject is
- what must stay unchanged
- which details should become cleaner
- which risks must be avoided

### Bad prompt pattern

Do not:

不要这样写：

- simply say “make it HD”
- simply say “enhance quality”
- ask for stronger style if the goal is preservation

## Step 4: Export final resolution

After the enhancement result is created, export the final file to the delivery standard the task requires.

生成增强结果后，要按任务需要导出成最终交付分辨率。

Default high-resolution export rule:

默认高分辨率导出规则：

- set the long edge to `3840px`
- keep original aspect ratio
- do not crop unless the user explicitly asks

Use the bundled script:

```bash
python3 scripts/export_high_res.py INPUT OUTPUT
```

Example:

```bash
python3 scripts/export_high_res.py result.png result_4k.png
```

Use this as the default when the user says things like:

用户说这些话时，默认就该走这个导出标准：

- `4K`
- `高清成品`
- `最终导出要能直接用`

If the user does not specify output dimensions, the skill should still improve the image first, then decide whether a real 4K export meaningfully helps the delivery.

如果用户没指定尺寸，也应该先把图做好，再判断是否有必要导出成真实 4K 文件。

## Step 5: Verify the result

Do not assume the enhancement or export succeeded.

不要默认增强或导出已经成功。

Always check the output and report the result to the user.

一定要检查结果，并把结果明确告诉用户。

If a high-resolution export was part of the task, explicitly mention:

如果这次任务包含高分辨率导出，要明确回报：

- output path
- final width
- final height

## Failure modes

### 1. The image looks cleaner but the file is still too small for delivery

Fix:

修正方式：

- export again with long edge `3840px`
- verify the output size before delivery

### 2. Identity drift on portraits

Fix:

- switch to conservative realistic cleanup
- reduce reconstruction pressure
- strengthen “preserve real face identity” in the prompt

### 3. Text becomes warped or unreadable

Fix:

- reduce redraw aggressiveness
- prioritize cleanup over reinterpretation
- warn the user if the source text is too small for safe regeneration

### 4. Composition changes

Fix:

- restate exact preservation of framing and subject placement
- avoid prompts that imply redesign

## What to tell the user

Keep the user-facing response short and concrete:

面向用户的回复要短、具体：

- whether the image is suitable for this route
- what the main enhancement focus is
- where the final 4K file is
- what the final dimensions are

## Hard constraints

- do not confuse “looks sharper” with “finished delivery”
- do not redesign the subject unless the user explicitly asks
- do not silently crop to a different composition
- do not over-ask when the image already implies a safe route

硬约束：

- 不要把“看起来更清楚”当成“已经交付完成”
- 除非用户明确要求，不要重设计主体
- 不要偷偷裁成另一种构图
- 图片已经足够明确时，不要过度追问
