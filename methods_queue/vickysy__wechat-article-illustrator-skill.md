---
name: wechat-article-illustrator-to-draft
description: Use when the user wants to turn a WeChat Official Account article draft into an illustrated, styled, WeChat-safe draft-box item with configurable visual styles.
---

# WeChat Article Illustrator To Draft

Create an illustrated WeChat Official Account draft directly from article text.

The core workflow is fixed, but the visual identity is controlled by a style profile. Do not assume the default profile is the user's brand.

## Non-Negotiables

- Never publish to followers. The only allowed write target is the WeChat draft box.
- Before calling any WeChat API that creates or updates a draft, get explicit user confirmation unless the user already approved the draft write in the current task.
- Never print or store `AppSecret` or `access_token` in article files, logs, manifests, or final messages.
- If credentials, IP whitelist, cover image, or draft permission are missing, stop at a local preview package and report the missing setup.

## Workflow

1. **Read the article**
   - Accept pasted text, local Markdown, DOCX, webpage text, or existing article HTML.
   - Preserve the writer's voice. Do not rewrite unless asked.
   - Infer title, author, digest, and source URL only when absent.

2. **Choose a style profile**
   - Read `templates/style-profiles.yaml`.
   - If the user has no style, start with `minimal_handdrawn`.
   - For creator-tool, Skill, workflow, or open-source process articles, prefer `bright_creator_infographic`.
   - If the user has brand colors or a logo, create a temporary custom profile before generating visuals.

3. **Plan images**
   - Use `references/article-to-draft-workflow.md`.
   - Pick cognitive anchors: concepts, contrasts, turning points, processes, or abstract sections.
   - Do not decorate every heading.
   - Do not add an AI robot, avatar, or mascot unless functionally needed by the idea.

4. **Generate and place images**
   - Final body illustrations should be generated with an image model, not manually drawn with PIL or programmatic shape code.
   - Use scripts only for local preview layout, image insertion, upload caching, and WeChat-safe HTML.
   - Information graphics must contain clear information structure and readable labels. Blank label boxes are not enough for final output.
   - If generated text is wrong, regenerate once or post-process exact labels locally; do not ship wrong labels.
   - Insert images after the paragraph they clarify.
   - Keep stable ASCII filenames, e.g. `fig01-question.png`.

5. **Build WeChat-safe HTML**
   - Follow `references/wechat-html-formatting.md`.
   - Apply `templates/wechat-theme.css`, then inline styles.
   - Do not put the article title/H1 into the uploaded body. The title belongs in the WeChat draft title field only.
   - Use the selected profile's section divider, emphasis color, and highlight rules.
   - Preserve the writer's paragraph rhythm. Do not split prose into many tiny step-like paragraphs unless the source was written that way.
   - Do not auto-highlight repeated keywords. Use bold only for explicit key paragraphs/sentences by default.
   - Remove scripts, unsafe attributes, CSS classes, IDs, and unsupported elements before upload.

6. **Upload assets**
   - Body images: upload via `/cgi-bin/media/uploadimg`, replace local `img src` with the returned WeChat image URL.
   - Cover image: upload via `/cgi-bin/material/add_material?type=image`, use returned `media_id` as `thumb_media_id`.
   - Cache upload mapping in a private manifest. Re-upload when assets change.

7. **Create or update draft**
   - If no local `draft_media_id`, call `/cgi-bin/draft/add`.
   - If a manifest has `draft_media_id`, call `/cgi-bin/draft/update` with `index: 0`.
   - Save returned draft metadata in the private manifest.

8. **QA before done**
   - Open or export local preview when possible.
   - Confirm title length, digest, cover, image count, body character count, and no local image paths.
   - Confirm no over-highlighting and no paragraph fragmentation.
   - Confirm images use the selected profile's own palette and motifs; do not copy a reference image's brand colors, scenery, logo, road, tree, mountain, or layout identity.
   - After a successful write, fetch the draft from WeChat and verify list-card fields: `title` and `digest` must be real readable text, not literal `\uXXXX` escapes or mojibake.
   - Report draft result without secrets.

## References

- `templates/style-profiles.yaml`: configurable visual profiles.
- `references/style-profiles.md`: how to adapt the skill to a user's own brand.
- `references/article-to-draft-workflow.md`: image planning and placement.
- `references/wechat-html-formatting.md`: WeChat-safe HTML rules.
- `references/wechat-draft-api.md`: draft API reference.
- `references/safety-and-credentials.md`: credential and write-safety rules.
