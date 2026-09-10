---
name: game-cover-maker
description: Create high-attention Chinese game-sharing covers from screenshots/key art or newly generated backgrounds. Automatically infer game type, preserve recognizable game identity for known titles, switch genre-appropriate templates, support exact Chinese text, DLC/save/version/platform callouts, multiple sizes, strong same-game batch diversity, and varied typography/panel systems across multi-cover batches. Prefer image generation for artwork/background and deterministic Pillow rendering for final Chinese text.
---

# Game Cover Maker

Create bold Chinese game-sharing covers for discovery feeds and short-video platforms.

The most important rule is:

> **For an existing recognizable game, preserve game identity first; apply genre styling second.**

A cover can be more dramatic and more clickable than a raw screenshot, but it should still look like the requested game rather than a generic game from the same genre.

The user's explicit wording, target size, supplied references, genre/style override, platform claims, and requested cover count always take precedence.

## Core workflow

1. **Classify the game**
   - Separate genre from marketing/presentation tags.
   - Genre examples: `grand-strategy`, `strategy`, `roguelike`, `shooter`, `rpg`, `simulation`.
   - Descriptor examples: `大型单机`, `PC单机`, `Steam移植`, `手机直装`, `完全汉化`.
   - `大型单机` is not a genre.
   - If genre is clear, infer it automatically. If genuinely ambiguous, use `general`.

2. **Choose identity mode before designing**
   - Read `references/game_identity.md`.
   - Known existing game + no redesign request → default to `game-faithful` behavior.
   - User-supplied screenshot/image → use it as the highest-priority identity reference.
   - If no user image is supplied and tools allow, prefer official/publisher/store/gameplay references over inventing a generic replacement style.
   - Only use `genre-inspired` artwork when the game is unknown, references are unavailable, or the user explicitly requests a redesign.

3. **Plan batch diversity when count >= 2**
   - Read `references/batch_variation.md` and `references/typography_variation.md`.
   - Enable diversity mode automatically.
   - Build one distinct visual concept per requested image.
   - Vary scene, subject, camera, activity, composition, and visual anchor while keeping the same game's visual language locked.
   - Also vary the text system between batch members: title treatment, tag shape, feature-card arrangement, color-role assignment, version placement, and accent treatment.
   - Do not generate four near-identical faces, and do not paste the exact same text layer over four different backgrounds.
   - Do not create variety by changing the wording.

4. **Create or prepare artwork/background**
   - Use supplied screenshot/poster/key art when suitable.
   - For known games, preserve recognizable character proportions, rendering style, environment language, and major world motifs.
   - If generating a fresh scene, create a new composition rather than reproducing an official cover exactly.
   - When the deterministic text-render workflow is available, generated artwork should contain no title, no platform logo, no UI label, no watermark, and no promotional copy.
   - Leave usable negative space for title, feature blocks, version badge, and accent/CTA.

5. **Render exact copy inside the text-safe area**
   - Game names, DLC wording, version numbers, Chinese text, platform labels, and user-provided marketing wording must remain exact.
   - Apply the text-safe placement rules in `references/typography_variation.md` for **every cover**, including count = 1.
   - On `9:16`, reserve the top **9%** as an unsafe band for essential text; place the top tag around **9–11%** and keep the main title comfortably lower, normally beginning around **16–19%** of canvas height.
   - The title's first visible pixel should not rise above roughly **15%** on `9:16` unless the user explicitly requests a high title layout.
   - Never let a title, tag, badge, outline, shadow, sticker, or panel touch/cross the canvas edge.
   - If copy is long, wrap, slightly reduce font size, move lower, or simplify decoration before ever moving text upward into the unsafe top band.
   - Prefer deterministic rendering with `scripts/render_cover.py` when exact text is critical.
   - If text is rendered directly by image generation, explicitly require all lettering to be fully inside frame, **visibly lower than the top edge**, with generous top breathing room; inspect it closely and regenerate/fix any misspelling or clipping.
   - Do not normalize or rewrite user copy just because another phrase sounds more natural.

6. **Quality-check every size and every batch member independently**
   - Re-crop and reflow each ratio.
   - Never stretch a finished cover into another size.
   - Reject or regenerate near-duplicate batch members.
   - Reject visually attractive covers that no longer resemble the requested game.
   - Reject any cover where important text is partially outside frame, visually cramped against the top edge, or too high to survive feed/platform cropping.
   - Reject batches where the backgrounds vary but all typography, panel shapes, and color assignments are effectively identical unless the user explicitly requested a unified series template.

## Game identity preservation

For known games, game recognizability is a hard requirement.

Preserve, when supported by references:

- character proportions and silhouette language
- face/eye/mouth simplification level
- line-art and shading style
- costume/accessory language
- environment and prop design language
- gameplay-like scene scale and camera feeling
- recurring world/location motifs

Do **not** automatically transform a recognizable game into a generic anime/chibi/realistic/3D style just because that style fits the broad genre.

A useful test is:

> If the title text were hidden, would a player still plausibly recognize the game family?

If not, the artwork needs a better identity reference or a new generation.

### Example: 米加小镇 / dollhouse life-sim

Do not turn `米加小镇` into generic anime chibi art.

Treat it as a `simulation` game with a **cozy-life-sim / dollhouse subtype**. Preserve the game's recognizable flat/lightly shaded 2D cartoon language, simple rounded character proportions, compact facial features, dollhouse/cutaway rooms, and dense interactive everyday props.

Good scene variation:

- town street / outdoor social scene
- home / bedroom / kitchen
- mall / clothing / supermarket
- school + hospital + restaurant multi-location collage

The four covers may show different characters and locations, but all should look like they belong to the same game world.

## Same-game batch diversity

This is a hard requirement when the user requests multiple images of the same game.

### Do not anchor to previous generated faces

When the same game was already generated earlier in the conversation, do not automatically reuse those AI-generated covers as positive image references. This can lock the model onto the same face, costume, pose, or composition.

Use prior generated covers as concept history to avoid, not as the primary identity source.

Only reuse an earlier AI-generated cover as a positive reference when the user explicitly asks for:

- same character / same face
- same visual identity
- editing that exact cover
- a close variant of that exact design

For known commercial games, use the real game's visual references for identity and previous AI outputs only to avoid repeating concepts.

### Mandatory visual variation dimensions

For each cover in a batch, vary at least 4 of:

- primary subject
- character identity/archetype
- character count
- camera distance and angle
- environment/scene category
- subject position and title composition
- secondary visual anchor
- activity/action
- lighting/time/weather
- palette emphasis within the selected game/genre family

Tiny prop swaps do not count.

For a batch of 4, do not use the same dominant human archetype more than once unless the title has one fixed iconic protagonist and the user wants protagonist consistency. For games that support it, strongly prefer at least one environment/map/multi-scene cover without a dominant close-up face.

## Typography and panel diversity

Text content is fixed; text presentation is not.

When count >= 2, default to visible text-style variation unless the user explicitly asks for a uniform series template.

Read `references/typography_variation.md` and vary at least 3 text-design dimensions between neighboring covers:

- title fill/treatment
- outline/shadow treatment
- top-tag shape and position
- feature-card shape and arrangement
- version-badge position/style
- color-role assignment
- title alignment/placement
- accent/CTA treatment

Text-position variation must always stay inside the ratio-specific safe area. A composition is not considered diverse if its only difference is pushing the title dangerously close to the top edge.

Do not use the exact same combination of red top tag + same title fill + yellow feature strip + same green badge + same bottom banner on every cover.

Keep the design coherent with the real game palette. Diversity does not mean random colors.

If the user did not supply `accent`, do not invent a large bottom CTA just to fill the layout. A cleaner cover with more visible artwork is allowed and often desirable.

Exact-copy examples:

- `无广版` must not silently become `无广告版`
- `自带菜单` must not silently become `内置菜单`
- version numbers must remain unchanged

## Automatic genre routing

Detailed design guidance lives in `references/genre_templates.md`; taxonomy guidance lives in `references/game_taxonomy.md`; identity guidance lives in `references/game_identity.md`; batch guidance lives in `references/batch_variation.md`; typography guidance lives in `references/typography_variation.md`.

| Genre | Renderer value | Template behavior |
| --- | --- | --- |
| 动作 | `action` | 红黑冲击、粗笔刷、强攻击感 |
| Roguelike / 肉鸽 | `roguelike` | 深红黑、地牢/危险氛围 |
| 射击 | `shooter` | 橙黑战术、斜切面板、速度/火力感 |
| RPG / ARPG | `rpg` | 深蓝紫 + 金色、史诗框体 |
| 普通策略 / RTS / SLG / 塔防 / 4X | `strategy` | 海军蓝 + 金色、指挥/战役/版图感 |
| 大战略 / Grand Strategy | `grand-strategy` | 帝国蓝 + 羊皮纸金、地图/外交/国家经营感 |
| 休闲 / 益智 / 卡牌 | `casual` | 高亮蓝橙、圆角卡片、轻松清晰 |
| 恐怖 / 惊悚 | `horror` | 低饱和黑红、压迫感 |
| 赛车 / 竞速 | `racing` | 青橙霓虹、斜切面板、极速感 |
| 模拟 / 经营 / 建造 / 生活模拟 | `simulation` | 青绿或原作主色、圆角、清晰生活/经营场景 |
| 生存 / 末日 | `survival` | 橄榄/土黄、粗粝荒野感 |
| 二次元 / 动漫 | `anime` | 粉紫 + 青色霓虹、高饱和 |
| 像素 / 复古 | `retro` | 紫粉/青色、像素块面板 |
| 未识别 | `general` | 通用高冲击模板 |

### Grand Strategy routing

`grand-strategy` is distinct from generic `strategy`.

Typical examples:

- `欧陆风云4` / Europa Universalis
- `钢铁雄心4` / Hearts of Iron
- `十字军之王3` / Crusader Kings
- `维多利亚3` / Victoria
- `群星` / Stellaris

Use map + nation/leader + army/navy + diplomatic/imperial symbols + navy/gold/parchment rather than an explosive action poster.

### Auto-routing rules

- Explicit user genre wins.
- If the title/context makes the genre clear, infer it explicitly.
- Otherwise use `--genre auto`.
- More-specific families win over broad ones.
- User style overrides the genre default.
- Identity rules override generic genre styling for known games.

Examples:

- `重生细胞` → `roguelike`
- `欧陆风云4` → `grand-strategy`
- `文明6` → `strategy` / civilization-4X subtype
- `米加小镇` → `simulation` / cozy-life-sim subtype

## Genre vs marketing copy

The Skill should distinguish what the game **is** from what the cover **says**.

For example, `欧陆风云4` can be classified internally as:

- genre: `grand-strategy`
- platform: `PC`
- presentation descriptor: `大型单机` or `PC单机` when appropriate
- feature claims: only those supplied by the user

For mainstream audiences, a broad descriptor may be clearer than a technical genre label, but the internal genre still controls the template.

## Default copy hierarchy

Unless the user asks for another arrangement:

1. Top tag: user-supplied `tag`, placed around the upper safe zone rather than near the canvas edge
2. Giant game title, fully visible and noticeably below the top tag
3. Up to 3 user-supplied feature callouts
4. Optional version/menu badge using the exact supplied value
5. Giant bottom emphasis only when the user supplied an `accent`

Use only claims provided by the user or clearly supported by supplied context. Do not invent DLC status, unlocked content, save status, MOD functions, version numbers, platform availability, ratings, download counts, slogans, or offline-only claims.

## Output sizes

| Preset | Pixels | Ratio | Typical use |
| --- | ---: | ---: | --- |
| `feed-4x5` | 1080×1350 | 4:5 | Default feed/game-share cover |
| `portrait-3x4` | 1080×1440 | 3:4 | Portrait poster/card |
| `vertical-9x16` | 1080×1920 | 9:16 | Full-screen vertical cover |
| `square-1x1` | 1080×1080 | 1:1 | Square card |
| `landscape-16x9` | 1920×1080 | 16:9 | Standard horizontal thumbnail |
| `landscape-16x10` | 1600×1000 | 16:10 | Wide game card |

Custom exact size:

```bash
--size WIDTHxHEIGHT
```

Example: `--size 1242x1660`.

## Background-generation guidance

When no usable art is supplied, generate or retrieve a background aligned with both **game identity** and **genre**.

General requirements:

- recognizable game visual language for known titles
- one clear primary subject or visual anchor unless using a multi-scene layout
- genre-appropriate environment and palette without overwriting the game's own palette
- calmer area for title and feature callouts
- enough contrast for supplied text
- no accidental promotional copy/logos/watermarks when exact overlay rendering is used
- for multiple covers, change the concept substantially while keeping art-direction identity stable
- reserve clean negative space inside the safe title zone rather than relying on the extreme top edge
- on `9:16`, preserve visible artwork/sky/background above the top tag so the typography stack feels intentionally lowered rather than top-heavy

For `grand-strategy`, prioritize maps, borders, flags, monarchs/generals/diplomats, fleets, armies, capitals, parliament/court/war-room objects, parchment, seals, compass/globe elements.

For cozy-life-sim/dollhouse games, prioritize recognizable everyday locations, flat/light 2D character language, rooms, furniture, shops, school, hospital, restaurant, street scenes, and playful props. Avoid generic anime-chibi substitution.

## Font behavior

The renderer searches common Chinese fonts on Windows/macOS/Linux, including Microsoft YaHei, SimHei, DengXian, PingFang, and Noto CJK. Never bundle or redistribute font files. If automatic detection fails, pass a local font path with `--font`.

## Quality gate

Before returning a cover or batch, verify:

- the genre/template is sensible
- known-game identity is preserved
- a player could plausibly recognize the game family without reading the title
- characters look like they belong to that game rather than a generic substitute
- background props/environments match the game's visual world
- exact Chinese wording matches the user's copy
- game name, version/menu text, feature text, tag, and accent are unchanged
- marketing descriptors do not create unsupported factual claims
- no text is clipped
- no text, outline, shadow, badge, or panel touches the canvas edge
- on `9:16`, essential text remains below the top **9%** unsafe band, the tag sits around **9–11%**, and the main title begins around **16–19%** rather than crowding the top
- the upper edge has visible breathing room before the first important text element
- no important subject is hidden unnecessarily
- title remains readable at about 250 px preview width
- every output size was reflowed rather than stretched
- multi-image batches are meaningfully different in scene/concept
- multi-image batches still look like the same game
- multi-image batches do not reuse the exact same typography/panel/color system by default
- previous AI-generated same-game outputs were not accidentally used as the main identity reference
- no bottom accent/CTA or extra slogan was invented when the user did not provide one

Return the generated image file(s) directly. Keep commentary short unless the user asks for design analysis.