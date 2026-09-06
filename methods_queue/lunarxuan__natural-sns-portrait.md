---
name: natural-sns-portrait
description: Create or refine prompts for photorealistic, everyday SNS-style portraits of clearly adult women, especially natural smartphone snapshots with realistic skin, facial asymmetry, hair texture, casual composition, ambient light, and non-model-like poses. Use when the user asks for a realistic social-media portrait, candid phone photo, non-selfie portrait, selfie, reference-photo-based portrait prompt, or wants to reuse the bundled realism guidelines. If an image-generation tool is available, generate directly; otherwise return a production-ready prompt.
---

# Natural SNS Portrait

Create believable, everyday portrait photos that feel like ordinary smartphone images posted to social media rather than polished commercial photography.

## Workflow

1. Determine the requested shot type: selfie, mirror selfie, or photo taken by another person.
2. Determine setting, clothing, pose, gaze, framing, and mood from the user's request. If unspecified, choose an ordinary daily-life setting and a relaxed pose.
3. If reference photos are provided, preserve only visually observable, non-sensitive appearance cues relevant to likeness: face shape, hairstyle, approximate build, glasses/accessories, and general proportions. Do not infer identity or hidden personal attributes.
4. Load `references/realism-guidelines.md` and apply all relevant realism constraints.
5. Keep the subject clearly adult. Default to a woman in her 20s if age is not otherwise specified.
6. Prefer smartphone-photo realism over studio quality: ambient/natural light, slightly imperfect framing, restrained depth of field, small exposure inconsistencies, mild sensor noise, and ordinary environmental detail.
7. Avoid over-perfect AI aesthetics: plastic skin, extreme symmetry, enlarged anime-like eyes, hyper-clean hair strands, glossy CG highlights, impossible anatomy, overly staged poses, excessive bokeh, luxury-ad styling, and unnaturally pristine backgrounds.
8. For gaze requests, follow them exactly. For "目光与摄像头有交汇", make the eyes meet the camera naturally without a rigid passport-photo stare.
9. For non-selfie requests, make the camera position and body language consistent with another person holding the phone. Do not show the subject holding the capturing phone unless explicitly requested.
10. If an image-generation tool is available, generate the image without exposing raw tool arguments. Otherwise output one consolidated prompt ready for an image model.

## Prompt Construction

Build a single coherent prompt in this order:

- subject and clearly adult age range
- visible appearance / reference-photo likeness cues
- scene and everyday context
- shot type and camera relationship
- gaze and expression
- clothing/accessories if requested
- lighting
- smartphone texture and composition imperfections
- skin, hair, anatomy, and realism constraints
- negative constraints against CG/commercial/AI-looking results

Do not turn the result into a long numbered checklist unless the user asks. Prefer a compact but information-dense generation prompt.

## Provenance and Watermarks

Do not instruct systems to remove, disable, evade, or falsify provenance markers such as SynthID, C2PA, or invisible watermarks. It is fine to request that the visible scene itself contain no added text, logo, border, or decorative watermark, but do not promise that platform-level provenance metadata or invisible markers will be absent.
