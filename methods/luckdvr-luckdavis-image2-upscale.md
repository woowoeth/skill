---
name: luckdavis-image2-upscale
description: "Use when the user provides an image and asks for a faithful redraw-upscale. The model redraw is produced at its native resolution (typically about 1.4K); the 3840-pixel file is a proportional delivery upscale, not a native 4K redraw."
---

# Luckdavis Image2 Upscale

Use English for model-facing prompts. Use Chinese for user questions and delivery notes.

## Scope gate

Accept only PNG and JPG inputs (`.png`, `.jpg`, `.jpeg`). Do not accept GIF, SVG, HEIC, AVIF, or any other format; ask the user to provide a PNG or JPG instead.

Use this skill for an existing image whose content should stay the same while becoming larger and clearer. Its positioning is **faithful redraw-upscale**: the model redraw is produced at its native resolution (typically about 1.4K), then proportionally resized to a 3840-pixel long-edge delivery file. The delivery file is not a native 4K redraw; never describe it as “4K超清重绘” or imply that new native 4K detail was generated. Route content replacement, background replacement, multi-image compositing, and new-scene generation out of this skill with:

> 这个需求涉及换内容、合成或生成新画面，不属于保真放大范围。

## Version rule

Treat every generated or normalized image as immutable. Give each output a new `_vNNN` or timestamped path; the script assigns the next unused `_vNNN` automatically. Keep older versions available for rollback and never overwrite them.

## 1. Choose the reference route

Always ask before processing:

> 这次放大请选择参照方式：
> 1. 快速：不加参照，直接保真重绘；主体锚定会稍弱。
> 2. 搜索：我搜索主体或产品的官方图，并把它作为参照图。
> 3. 给图：你提供一张清晰参照图。

For search, find an official image of the same subject or product. If none is available, say so and let the user choose quick mode or provide an image. For a supplied or found candidate, confirm that the subject or model matches and that the view is compatible with the source; otherwise explain the mismatch and request another reference.

This step is complete only when the user has chosen a route and, for a reference route, one usable matching image has been selected. The reference's role in the edit request is defined only in [prompt-architecture.md](references/prompt-architecture.md).

## 2. Preflight the source

Inspect dimensions and format without writing an image. Apply the output geometry and acceptance rules from [dimension-guide.md](references/dimension-guide.md):

```bash
python3 scripts/upscale_4k.py "/absolute/path/input.png" --inspect
```

If `low_resolution_gate` is `true`, pause before using Image Gen:

> 这张图的长边小于约 1200 像素。继续处理会更接近重新创作，而不是单纯放大。你要继续，还是换一张更大的原图？

Ask rather than infer when the image does not resolve whether softness is intentional or damaged, whether text should remain, or whether the aspect ratio should change. Apply the geometry decision from `dimension-guide.md`.

After confirmation, create the sole editing target. The script applies EXIF orientation, converts to RGB, and performs the required proportional LANCZOS resize to a 3840-pixel delivery working size under the version rule. This resize prepares the edit and delivery geometry; it does not make the later model redraw native 4K:

```bash
python3 scripts/upscale_4k.py "/absolute/path/input.png" \
  --output "/absolute/path/input_working.png"
```

Read the JSON to obtain the actual versioned output path. This step is complete when the source passed the format and low-resolution gates, all unresolved intent questions are answered, and the working image exists at the reported path.

## 3. Read the image and build the prompt

Inspect the working image itself. Read [prompt-architecture.md](references/prompt-architecture.md) before every redraw; it is the single authority for image roles, full-dimension analysis, prompt assembly, and reference constraints.

After inspecting the image, consult [text-lock.md](references/text-lock.md) to decide whether its branch activates; that file alone defines the condition, prompt wording, verification, and delivery disclosure.

This step is complete only when every prompt-assembly check in `prompt-architecture.md` passes and every included observation is supported by the image, the selected reference, or an explicit user correction.

## 4. Redraw once with built-in Image Gen

Use Codex's built-in gpt-image-2/Image Gen image-editing capability. Put the selected inputs and the assembled English prompt into one edit request, using the roles defined in `prompt-architecture.md`. Perform one full-frame redraw.

Save the raw redraw under the version rule. This step is complete when the request matches the prompt-architecture checklist and the raw result exists as a separately addressable version.

## 5. Normalize and verify

Normalize the raw redraw against the untouched original under the version rule:

```bash
python3 scripts/upscale_4k.py "/absolute/path/redraw_v001.png" \
  --aspect-reference "/absolute/path/input.png" \
  --output "/absolute/path/final.png"
```

Read the emitted JSON and apply every acceptance check in `dimension-guide.md`. Treat the measured ratio fields as boundary evidence; do not infer crop, padding, or canvas extension from a fixed boolean. Reject a version that fails the geometry guard even though its file remains available for audit.

Visually check that the subject and composition remain intact, the original colour and medium continue, text has not mutated, and no conspicuous fake texture or duplicated structure has appeared. This step is complete only when both the geometry checks and visual checks pass.

## 6. Deliver and correct

Return the accepted version with a short Chinese note that identifies the reference route, what was constrained, the regions that remain uncertain, and the measured geometry result. State that the model redraw was generated at native resolution (typically about 1.4K) and proportionally enlarged for 3840-pixel delivery; do not call the result a native 4K redraw:

> 参照方式：……  
> 已锁定：……  
> 我没完全把握、请重点看：……  
> 尺寸与边界核验：按脚本 JSON 如实填写。

When the text branch activated, include the exact disclosure required by `text-lock.md`.

This delivery is complete when the user can identify the exact accepted file, the reference route, the uncertain regions, the text warning when applicable, and whether geometry verification passed.

If the user requests a correction after the first result, then and only then read [correction-loop.md](references/correction-loop.md). Do not load correction instructions during the first redraw.
