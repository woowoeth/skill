---
name: create-80s-chinese-art
description: Analyze, generate, or transform images using specific visual lineages from 1970s–1980s Chinese picture books, children's magazines, animation art, folk-tale illustration, lianhuanhua, and poetic landscape painting. Use when the user mentions 80年代中式美学、老绘本、上美影、儿童刊物、连环画、老插画、胶版印刷，or supplies period Chinese illustration references and wants prompts, covers, posters, story images, or style transfer. Treat this as reference-led art direction, never as a generic retro, guofeng, anime, or texture filter.
---

# Create 80s Chinese Art

Reconstruct a concrete visual lineage from evidence. Do not render “80 年代中式美学” as one universal style label.

## Required references

- Read [references/visual-grammar.md](references/visual-grammar.md) for every task.
- Read [references/generation-protocol.md](references/generation-protocol.md) before writing prompts or generating/editing images.
- Read [references/source-analysis.md](references/source-analysis.md) when working from the Xiaohongshu reference set or explaining the diagnosis.
- Inspect supplied visual references directly. Post titles and captions are metadata, not visual evidence.

## Workflow

1. Identify the exact target: analysis, prompt, new image, image edit, cover, poster, or sequence.
2. Inspect the full reference set, including carousel pages when available. Analyze shape language before texture or mood.
3. Select exactly one visual lineage from `visual-grammar.md`. Do not blend unrelated sources by default.
4. Select 2–4 coherent reference images from that lineage for image generation. Label them as style-only references; do not copy their characters or compositions.
   - When the user provides no local references, use the matching files under `assets/style-references/`.
5. Define the target scene in the same narrative register as the references. Prefer children, animals, folk characters, daily collective life, or small figures in nature when validating this aesthetic. A contemporary adult lifestyle scene is a poor first test because it strongly activates current editorial/anime priors.
6. Write the prompt in this order: scene relationship → silhouette and proportion → face/hair/hands → spatial construction → color masses → physical medium → restrained print behavior.
7. Generate. Inspect the result at face, hand, silhouette, and whole-frame levels. Reject on the first lineage failure; do not try to rescue a wrong drawing system with more paper grain.
8. Iterate by correcting one structural axis. If the figure system is wrong, regenerate from the references instead of editing only the eyes.

## Hard rules

- Default to **中国儿童刊物水粉** only when the user invokes the broad trend without pointing to a specific reference.
- Keep **动画赛璐珞、装饰性民间故事、线描连环画、抒情山水** as separate lineages.
- Exclude public mosaic murals from the default. They belong to a different public-art tradition and must be explicitly requested.
- Never mix “公共马赛克＋儿童杂志＋现代日漫” to make a new hybrid.
- Do not describe a realistic modern person and then ask the model to “make it retro.” Redesign the person through the chosen period shape grammar.
- Do not use `cinematic`, `anime`, `Ghibli`, `concept art`, `highly detailed`, `beautiful young woman`, or `editorial illustration` in positive prompts.
- Do not use aging artifacts as primary style controls: yellow paper, scratches, film grain, dust, faded photo, or sepia.

## Lineage gate

Reject the image when any of these appear:

- Current anime face: V-shaped jaw, glossy iris, eyelash emphasis, tiny nose, beauty-ad skin, strand-by-strand hair, melancholy profile pose.
- Contemporary digital concept art: rim light, atmospheric perspective, photographic rain, reflections, depth of field, volumetric light, detailed architecture.
- Texture substitution: one noise layer or scratch overlay applied equally to sky, skin, clothes, and ground.
- Modern anatomy wearing an old palette: fashion-illustration proportions, narrow shoulders, long limbs, elegant hands, model-like posture.
- Current “retro children’s book” prettification: two matching round faces, identical circular blush, neat bowl-cut hair, symmetric smiles, centered cozy staging, decorative flowers/animals, and polished collectible-book charm.
- Generic “Chinese” signaling: lanterns, clouds, dragons, seals, hanfu, red-and-gold palette without narrative need.
- Mixed lineage: cel-animation face inside painterly magazine scenery, or ink-line characters inside cinematic digital backgrounds.

Accept only when the image passes all four checks:

1. **Silhouette**：the subject reads as a designed period shape at thumbnail size.
2. **Figure grammar**：head, face, hair, limbs, hands, clothes, and pose follow the selected lineage consistently.
3. **Spatial grammar**：the world is built with overlapping color masses, stage-like planes, or deliberate emptiness—not photographic perspective by default.
4. **Material grammar**：brush and print behavior vary by object and come from a plausible original medium.

## Output

For analysis, return:

- `谱系`：one lineage, with evidence.
- `造型系统`：silhouette, proportions, face, hair, hands, clothing.
- `画面系统`：space, color, medium, print.
- `禁区`：specific drift risks.

For prompts, return one main prompt plus a compact negative block. Name the selected reference images and their roles when generating with image tools.

For image edits, list invariants first. If preserving a photographic adult identity conflicts with the chosen drawing system, state that the result can preserve pose and clothing cues but not literal facial realism.
