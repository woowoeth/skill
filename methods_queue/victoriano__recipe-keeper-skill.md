---
name: recipe-keeper
description: Extract and normalize cooking recipes from web and social URLs including Instagram, YouTube, TikTok, X/Twitter, blogs, and plain text; save them into a configurable Notion Recipes database; and optionally adapt them into Thermomix/TM6/TM7 and Cookidoo Created Recipe format. Use when asked to save a recipe link, ingest a social cooking video, normalize ingredients and instructions, keep source media, create Thermomix steps, or upload/patch Cookidoo custom recipes.
---

# Recipe Keeper

## Overview

Use this skill to turn messy recipe sources into a clean personal recipe system: normalized recipe data, a Notion page with media and ingredients, and an optional Thermomix/Cookidoo version with structured machine metadata.

The workflow is intentionally agent-led. The bundled scripts handle repeatable Notion and Cookidoo API calls, while the agent remains responsible for extraction, judgment, safety notes, and adaptation quality.

## Workflow

1. Capture the source.
   - Preserve the original URL.
   - For social videos, gather the caption, visible text, comments only when useful, transcript/subtitles when available, thumbnail, and direct media URL or local media file when legally and technically available.
   - If the source is image-only or incomplete, infer cautiously and mark uncertainty in notes.

2. Normalize the recipe.
   - Produce one JSON object using the shape in `examples/normalized-recipe.json`.
   - Prefer metric units.
   - Separate ingredients from equipment, garnish, serving notes, and optional substitutions.
   - Make instructions executable, ordered, and explicit.
   - Preserve the source media URL and best hero image.

3. Save to Notion.
   - Read `references/notion-recipe-schema.md` before creating or changing a Notion database mapping.
   - Use a Notion connector if available, or use `scripts/notion_recipe_cli.py`.
   - Never create duplicate pages without first searching by source URL and title.
   - Put video/media near the top of the page. Native file upload is best when the local environment supports it; external video/bookmark blocks are the portable fallback.

4. Adapt for Thermomix when requested or useful.
   - Read `references/thermomix-format.md`.
   - Keep unsafe or awkward operations as manual, oven, pan, fridge, or rest steps.
   - Use Thermomix settings only where they are technically meaningful.
   - Add food-safety notes for meat, eggs, fermentation, preservation, or low-temperature cooking.

5. Upload to Cookidoo only when explicitly requested.
   - Use `scripts/cookidoo_cli.py` with `COOKIDOO_EMAIL` and `COOKIDOO_PASSWORD`.
   - Convert the normalized recipe into the Cookidoo JSON shape documented in `references/thermomix-format.md`.
   - Every Thermomix machine action must have structured `ingredient`, `mode`, or `tts` metadata before upload.
   - Read the recipe back after upload when possible and report any dropped annotations.

## Normalized Recipe JSON

Use this shape before writing to Notion or Cookidoo:

```json
{
  "title": "Crispy salmon rice bowl",
  "source_url": "https://www.instagram.com/reel/example/",
  "media_url": "https://...",
  "image_url": "https://...",
  "platform": "Instagram",
  "author": "creator handle or name",
  "servings": 2,
  "prep_time_minutes": 15,
  "cook_time_minutes": 20,
  "total_time_minutes": 35,
  "ingredients": [
    "300 g salmon fillet",
    "200 g cooked rice"
  ],
  "instructions": [
    "Cut the salmon into bite-size pieces.",
    "Season and cook until browned."
  ],
  "notes": "Short adaptation notes and uncertainties.",
  "tags": ["dinner", "fish"]
}
```

## Scripts

Create a Notion page from normalized JSON:

```bash
NOTION_TOKEN="secret_..." \
NOTION_RECIPE_DATABASE_ID="..." \
python skills/recipe-keeper/scripts/notion_recipe_cli.py create \
  --file skills/recipe-keeper/examples/normalized-recipe.json \
  --dry-run
```

Create a Cookidoo custom recipe:

```bash
COOKIDOO_EMAIL="me@example.com" COOKIDOO_PASSWORD="..." \
python skills/recipe-keeper/scripts/cookidoo_cli.py create-custom \
  --file /tmp/thermomix-recipe.json \
  --image /tmp/recipe.jpg \
  --custom-coordinates auto
```

## Secrets And Safety

- Never store Notion tokens, Cookidoo credentials, cookies, or downloaded private media in this repo.
- Respect the source platform's terms and the user's rights to the media.
- Cookidoo Created Recipe endpoints used by the helper are private web endpoints, not an official public API. They can change without notice.
- Do not pretend Thermomix timing guarantees food safety. For risky foods, write explicit checks such as internal temperature or visual doneness.
