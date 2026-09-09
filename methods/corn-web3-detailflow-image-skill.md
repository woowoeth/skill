---
name: detail-flow
description: Build, redesign, polish, or review product detail pages for products, AI tools, models, SaaS features, developer products, plugins, ecommerce listings, and technical showcases. Use when the user provides a product image, reference image, screenshot, product concept, or existing page and asks for an independent 1:1 ecommerce image set, detail page, 10+-image product page, model page, product feature page, visual polish, responsive frontend implementation, screenshot-based QA, or reusable workflow derived from an existing product page project. Image-led ecommerce deliverables target the US market and require English-only visible copy.
---

# DetailFlow

## Overview

Use this skill to turn a product or feature idea into a useful, polished detail page. Prioritize clear product communication, real user workflows, implementation quality, responsive behavior, and visual assets that reveal the product rather than decorative filler. Keep the skill general-purpose: it may be used with different image-generation tools, frontend stacks, or local pipelines, but its core job is product detail-page planning, generation, review, and iteration. For image-led ecommerce delivery, default to independent square images rather than connected long-page slices.

## Execution Contract

For image-led ecommerce detail-page requests, follow the defined DetailFlow route strictly. Treat this contract as higher priority than convenience, improvisation, or tool preference.

- MUST follow this order: analyze inputs -> when a competitor page exists, extract its page-by-page product logic -> map that logic to the user's product -> produce the page content contracts -> wait for the first user approval -> write the complete master and per-image prompt pack from the approved contracts -> pass the pre-generation content-architecture audit -> establish the text visual master -> generate and internally inspect the first 2 final square images one at a time -> present the 2 individual images and audit together -> wait for the second user approval -> generate the remaining square images one at a time with contract-conformance checks -> run the final audit -> save and report the output folder.
- MUST use exactly two normal user approval gates for the standard workflow: approval 1 confirms the complete reference-to-product mapping and page contracts; approval 2 confirms the first 2 independently generated square images. Additional confirmation is needed only when a serious failure blocks safe continuation or the user requests a workflow change.
- MUST stop at both approval gates. Do not interpret silence, an approval from another stage, or a generic request to "continue" as approval for unreviewed page contracts or a visual sample package.
- MUST inspect every staged output before continuing. Do not proceed when the image is textless despite planned copy, ignores the reference style, changes the product, contains garbled text, invents claims absent from all supplied sources, or hides the provenance of reference-supplied claims.
- MUST treat every image-led ecommerce deliverable as US-market creative regardless of the user's conversation language or the language visible in source materials. Write every piece of visible image text in idiomatic American English, including product names rendered as copy, headlines, subtitles, labels, badges, annotations, specifications, units, comparison rows, disclaimers, and calls to action. Chinese text and Chinese/Han/CJK glyphs are forbidden in final images. If a source product, brand, logo, package, or reference contains Chinese text, use a user-supplied official Latin-script or English form; otherwise omit that text or use a grounded generic English descriptor instead of transliterating, inventing a translation, or reproducing the Chinese glyphs.
- MUST keep user-facing planning discussion in the user's preferred language when helpful, but every exact-copy field intended for rendering must contain English only. Author the text visual master, master reference prompt, and per-image generation prompts in English; source-language notes may remain in internal analysis only and must never be quoted or requested as visible text.
- MUST use the user's product images, reference images, confirmed facts, approved page contracts, and approved masters as the authoritative inputs. Do not replace them with a newly invented concept or a generic category template.
- MUST keep the task scoped to the requested ecommerce image set. Do not create a website, video, animation, presentation, application, workflow node, Python script, automation script, or other auxiliary artifact unless the user explicitly asks for that artifact.
- MUST NOT write code merely to simulate image generation, create placeholder deliverables, or bypass an unavailable image-generation/editing capability. If a required capability is unavailable or fails, state the limitation and stop at the current stage or offer the smallest relevant alternative.
- MUST keep the requested deliverable scope stable: do not add unrelated stages, output formats, image counts, or auxiliary deliverables without approval. When the user provides limited product information, infer suitable selling-point copy, scene ideas, visual motifs, labels, and supporting content from the product images, product category, reference images, and common buyer concerns. Clearly distinguish reasonable creative inference from confirmed facts. Do not invent exact technical parameters, certifications, awards, medical effects, discounts, or brand partnerships that are not supported by the user or source material.
- MUST NOT silently change the production route after a failed result. Revise only the smallest responsible layer described in the revision-routing rules, then request confirmation when the change affects approved page contracts or a master.
- MUST preserve approved outputs. Do not overwrite or discard accepted images while experimenting; save revisions as clearly identified replacements or versions.
- MAY use lightweight existing utilities only when they are necessary for deterministic operations such as reading image dimensions, checking files, or saving deliverables. Do not create new utility scripts for these operations unless the user explicitly requests automation.
- MUST treat image generation as the expensive operation. Finish and audit the complete page contracts and prompt pack before the first image-generation call. Fix a failed content or prompt audit with text-only planning work; it must not consume an image-generation attempt.
- MUST maintain one persistent page-content architecture map across the image set. For every reference page and planned slice, record the consumer question, page conclusion, evidence chain, ordered modules, information hierarchy, product-specific replacement, fact source, and claims absent from all supplied sources. Use `references/page-content-architecture.md` as the source of truth; do not rely on conversational memory.
- MUST stop before generation when a slice lacks a clear independent purpose, its modules do not support one conclusion, its evidence is missing or out of order, or its mapped competitor logic has been flattened into a generic headline plus product image. Repetition is a symptom to diagnose after these architecture checks, not the primary planning objective.
- MUST inspect each generated slice without making another image-generation call and compare the visible result with its approved page contract. Reject a slice when the intended conclusion is not immediately clear, the hierarchy or module order is lost, required evidence is absent, or decorative imagery replaces useful information. Revise the smallest responsible content, prompt, or slice layer before continuing.
- MUST plan at least 10 final detail-page slices for the standard image-led ecommerce workflow. Use more than 10 when the reference contains more distinct decision stages or dense sections that need room. Use fewer than 10 only when the user explicitly requests a smaller set. Do not pad toward 10 with repeated conclusions or evidence; if the available product and reference content cannot support 10 distinct pages, stop at the contract stage and request more facts or an explicit scope change.
- MUST allow claims visible in a user-supplied competitor reference to enter draft contracts, visible copy, and generation prompts as `reference_supplied` evidence, including performance numbers, materials, test or certification names such as SGS, and other product statements. Do not block or replace those claims merely because they are absent from the user's product photo. Mark them `reference_supplied_unverified` in the architecture map and first approval package so the user can decide whether to retain them. Do not invent claims absent from both the user's materials and the supplied reference, and continue replacing the competitor's brand and identity unless the user explicitly asks otherwise.
- MUST preserve the approved per-image content and prompt logic when applying the square format. Ratio, resolution, and independence are rendering constraints only; do not rewrite selling points, visible copy, modules, module order, evidence, competitor mapping, scenes, or information density merely to make the images square.
- MUST render each final ecommerce image as an independent `1:1` square. Target `1300 x 1300` pixels. When the image tool does not offer that exact size, use the closest supported square size, preferring the higher-resolution option; do not substitute a vertical or horizontal canvas.
- MUST NOT generate a `1:3` image master or `9:21` final slice for the standard ecommerce image workflow. Do not use previous/next edge continuation, outpainting between images, shared panoramic backgrounds, or prompts that say the image should continue from another image. Each square must be complete and independently uploadable.

If the user's request is ambiguous, choose the narrowest action that advances the current DetailFlow stage. Ask before expanding scope.

## Core Workflow

For image-to-ecommerce detail page requests, do not generate final images immediately. First produce structured page content contracts and ask the user to confirm or revise them. Generate images only after the user approves the content plan, unless the user explicitly asks to skip planning.

1. Clarify the product surface

   Identify the product name, audience, primary promise, concrete capabilities, constraints, proof points, and expected call to action. If the user provides a product image or reference image, infer visible materials, form, style, category, likely buyer concerns, and differentiators before writing page sections. If the user provides an existing page, inspect the current structure before proposing changes.

2. Shape the page architecture

   Build a scannable narrative: first-viewport identity, practical value, capability sections, examples or use cases, trust/proof, limits or requirements when relevant, and a clear next action. For ecommerce long pages, split the story into deliberate screens with one main job per screen, but vary the information weight across screens. Not every screen needs a campaign-style headline and subtitle; some screens should use smaller guide copy, explanatory paragraphs, labels, badges, callouts, ingredient/detail notes, comparisons, or scene captions. Avoid generic marketing copy that could describe any product.

   For image-led ecommerce long pages without a competitor detail-page reference, the first screen may establish 2-4 core claim seeds that later screens unpack or prove. When a competitor detail page is supplied, preserve its buyer journey and page responsibilities by default. Use only its visual DNA when the user explicitly says the reference is style-only or the input is a mood image rather than a detail page.

3. Match the existing project

   Read the repository structure, framework, routing, component conventions, design tokens, asset strategy, and local styling patterns before editing. Reuse existing components and utilities when they fit.

4. Design for product comprehension

   Make the product itself a first-viewport signal. Use screenshots, generated visuals, product mockups, demos, or domain-relevant imagery when appropriate. Keep operational tools dense, restrained, and easy to scan; use more expressive visuals only when the product category supports it.

5. Implement the page

   Edit the smallest reasonable set of files. Keep content, layout, and interaction states complete enough that the page feels like a real product surface, not a placeholder. Respect existing frontend guidance for accessibility, responsiveness, and visual hierarchy.

6. Verify with real rendering

   Start the app when needed. Check desktop and mobile viewports with screenshots or browser inspection. Fix text overflow, overlapping elements, blank media, awkward crop/framing, one-note color palettes, missing states, and layout shifts before handing off.

## Image Generation Workflow

Use this workflow when the user provides a product image and asks for an ecommerce detail page, 10+-screen page, long sales image, or style-reference-based product page.

1. Analyze inputs

   Describe the product image and reference style separately. List observed product facts, reference-supplied claims, inferred selling points, and claims absent from all supplied sources.

   When the user provides a competitor detail page, use it as the default content-architecture skeleton rather than inventing an independent story first. If the page is extremely tall or unreadable when fitted to the viewer, split it into readable crops and inspect every crop. For each competitor page or meaningful region, extract its position in the buyer journey, internal page conclusion, evidence chain, ordered modules, information hierarchy, density, and transition to the next page. Map the reference sequence to at least 10 final slices for the standard workflow while replacing the competitor's product, brand, people, and imagery with the user's own. Reference-visible claims and specifications may transfer under the `reference_supplied` policy instead of being discarded solely because the product photo does not prove them.

   Use `one_to_one` when reference and target counts align. When they do not, use `merge_adjacent` to combine only neighboring reference regions that form one coherent decision task, or `split_dense` to divide one dense reference region across ordered target slices. Record `source_reference_slices`, `mapping_mode`, and `mapping_reason`; preserve source order and account for every meaningful reference module. Never drop or reorder content merely to hit the requested image count.

   Preserve the reference page order, page responsibilities, module relationships, evidence forms, and density by default. Transfer reference-visible claims directly as `reference_supplied` when they support those modules. Adapt only when neither the user's materials nor the reference provides usable content, or when the user rejects a transferred claim. In that case, keep the same buyer-decision role with the closest product-specific evidence, or mark the mapping `needs_fact` or `omit_with_reason`. Do not silently replace a missing proof module with a generic slogan or attractive product hero.

   Before writing the page contracts, give the user one concise opportunity to provide confirmed selling points, specifications, functions, audience, or prohibited claims when these are not already supplied. When competitor modules depend on claims visible in the supplied reference, transfer them as `reference_supplied_unverified` and include that provenance in the first approval package instead of blocking prompt generation. Reserve `needs_fact` for content absent from both the user's materials and the supplied reference. Do not make this a mandatory questionnaire. If the user chooses not to add information, continue using product-image evidence, reference-supplied claims, and reasonable category-level inference; clearly distinguish all three sources for review.

   When a reference image contains a strong character, model, mascot, hand, prop, or scene language, treat it as part of the reference style DNA if it supports the user's requested style. Preserve the visual language at an abstract level, such as 3D cartoon character presence, friendly brand host, hand-held product reveal, low-angle lifestyle shot, or macro annotation style. Do not copy the reference image's original brand, exact person identity, text, or product.

2. Produce the page contracts first

   Output one `page_content_contract` per requested image, with at least 10 contracts in the standard workflow, before generating images. Keep the existing contract fields and prompt-building logic unchanged. For independent square delivery, set `top_edge_anchor` and `bottom_edge_anchor` to `none` instead of planning cross-image continuation. Every module must still have a stable `module_id`, source-module mapping or product-specific origin, relationship to the conclusion, information units with fact provenance, evidence form, hierarchy level, exact visible copy, and target assets with roles and availability. Reference-derived modules must also bind readable reference-crop ids. Record whether transferred claims are `reference_supplied_unverified`. When a competitor reference exists, include `source_reference_slices`, `mapping_mode`, and `mapping_reason`. Ask the user to confirm or revise the complete mapping and contracts before generating images.

   When no competitor detail-page architecture exists, derive the contracts from the buyer decision journey and optionally use 2-4 first-screen claim seeds to keep the story coherent. When a competitor detail page exists, its page sequence and information logic take priority over the fallback claim-seed framework unless the user explicitly requests an original structure or style-only use.

   Treat these fields as planning controls, not visible labels. Do not write internal labels such as `module_type`, `detail`, `parameter_trust`, `FAQ`, or `screen_job` into visible page copy. Convert them into natural, concise buyer-facing American English. All exact text in `visible_copy` and any page-level `text_exact` field must use English only and must contain no Chinese/Han/CJK glyphs, even when the user, product image, or competitor reference is Chinese.

   Do not force every screen into the same `headline + subtitle` structure. Reserve the strongest headline/subtitle treatment for the first screen or other true section openers. Later screens should choose copy modules based on the section's job: explanatory text, small guide title, label clusters, icon notes, proof callouts, ingredient/detail annotations, scenario captions, comparison rows, trust bullets, or closing CTA. The copy structure should drive layout variation and hierarchy.

   Set `conclusion_expression` from the reference module behavior or the page's evidence needs, such as `headline`, `annotation_map`, `comparison`, `step_sequence`, `diagram`, `scene_caption_cluster`, `trust_checklist`, or `quiet_closing`. `page_conclusion` is an internal semantic target, not automatically visible copy. Require an explicit headline only when `explicit_headline_required` is true; annotations, comparisons, steps, diagrams, or captions may communicate the conclusion without another poster headline.

   Before asking for approval, run a product-manager review. The full sequence must follow a comprehensible buyer journey. Each page must have one clear reason to exist, one sentence-level conclusion, evidence that directly supports it, and an intentional module order. A viewer should understand the intended takeaway in about three seconds. Reject a contract when its modules are merely a list, when the largest visual does not carry the main conclusion, when decorative content replaces proof, or when adjacent pages compete for the same decision task.

   When a competitor map exists, the first approval package must show a concise side-by-side mapping from every competitor region and module to its target slice and module: mapping mode, page job, internal conclusion, module sequence, information units, evidence form, target assets, factual gaps, and adaptation reasons. No meaningful reference module may disappear silently. Judge similarity by preserved decision logic, hierarchy, evidence richness, and density—not by copied wording or pixels. Repetition is a failure when two pages have the same purpose, conclusion, and evidence role; a recurring product, person, camera type, or visual device is acceptable when it serves a clear new page responsibility.

   Preserve the reference's useful information density when a competitor page exists. Otherwise, use enough evidence to make the page conclusion clear without padding toward a fixed module count. A sparse page still needs an explicit decision, transition, atmosphere, trust, identity, or closing role.

3. Build and audit the complete prompt pack before image generation

   Read `references/page-content-architecture.md`. Save the approved reference mapping and page contracts as persistent campaign state before generating any final image.

   Compile the master prompt and all final-slice prompt specifications from the approved contracts as one complete prompt pack. Do not let prompt writing re-plan the page. Every slice prompt must identify the contract's module ids and state its page purpose, expected takeaway, conclusion expression, ordered modules, hierarchy, required evidence, exact copy, target assets, mapped readable reference crops, and out-of-scope content.

   Run one whole-pack pre-generation audit. It must verify:

   - the page sequence preserves the approved buyer journey and, when present, the competitor's page-by-page logic;
   - every slice has one clear conclusion and an evidence chain whose modules appear in the approved order and hierarchy;
   - every reference module has a recorded target module or explicit disposition, and all `adopt` and `adapt` information units have fact provenance (`user_confirmed`, `visible_in_product`, `reference_supplied`, or `safe_inference`), target assets, and corresponding readable reference crops;
   - information density comes from useful claims, labels, steps, comparisons, annotations, or proof rather than unrelated decorative elements;
   - no slice has collapsed into a generic headline plus product hero, and no two slices perform the same decision task with the same conclusion and evidence;
   - every renderable string is idiomatic American English, contains no Chinese/Han/CJK glyphs, and is bound verbatim into an English-language master or per-image prompt that explicitly forbids Chinese or other CJK text in the rendered image.

   Treat any failure as a hard stop before image generation. Revise the prompt pack and page-content architecture map until the audit passes. Record the audit result and only then permit the first image-generation call.

4. Lock the visual master and structure before final image generation

   Create or confirm the text visual master and structure before generating final images:

   - Text master: `visual_master_spec`, `master_reference_prompt`, and `visual_style_dna`. Use it to lock palette, lighting, space, materials, typography, recurring visual motifs, reference-style DNA, product identity rules, section rhythm, information density, and page structure.
   - Structure source: the approved page contracts with each image's decision stage, buyer question, conclusion, evidence chain, ordered modules, hierarchy, and exact copy. Use it as the highest priority source for final prompts.

   Do not generate a `1:3` image master for the standard square-image workflow. This format change must not alter the approved content, copy, evidence, or visual direction of the individual-image prompts.

5. Generate final page sections

   Generate final screens as independent `1:1` square US ecommerce images, targeting `1300 x 1300` pixels. When that exact size is unavailable, request the closest supported high-resolution square size and prefer the higher-resolution option. Each image must follow the approved page contract exactly: do not change its decision stage, buyer question, conclusion, evidence, module sequence, hierarchy, expected takeaway, exact copy, scene logic, or information density during prompt writing. Request the image tool's highest available native detail and quality for the selected square size; do not generate a smaller image and enlarge it as the normal route. In every image prompt, state that all visible typography must reproduce the approved American English copy only and that Chinese/Han/CJK glyphs, untranslated source text, and invented non-English lettering are prohibited.

   When competitor crops exist, give each image the crop named by its page contract; do not rely on one unreadably tall reference. Use the competitor crop for page logic, module behavior, hierarchy, density, and any claims marked `reference_supplied`; use the product images for product identity. Do not pass a previous image's edge as continuation context. Each prompt must preserve the approved conclusion, evidence chain, and module sequence instead of falling back to a generic product hero.

   After each slice is generated, perform a read-only contract-conformance audit before continuing. Identify the visible conclusion, reading order, primary and secondary modules, evidence, labels, and takeaway from the actual image rather than the prompt. Compare them with the approved page contract and all mapped competitor pages. Passing the prompt audit does not waive this check because an image model may flatten structured content during generation.

   Reject the output when the page conclusion is unclear, evidence is missing, module hierarchy is inverted, labels are detached from their subjects, the reference page's useful logic and density have been reduced to decoration, or any visible Chinese/Han/CJK glyph appears. Treat Chinese text as a hard language failure even when it came from the supplied product, packaging, logo, or competitor reference. Revise only the smallest responsible prompt or image and do not continue until the current page contract passes. Use contact sheets after images 04 and 06 to verify the decision flow, hierarchy rhythm, and page responsibilities; these are internal checks, not additional user approval gates or connected final outputs.

   Use staged generation checks. Generate the first 2 square images separately, inspect them individually, and present both individual files with a concise audit as the second confirmation package. Generate the remaining images only after the user confirms this package. If an early image fails internally, revise only the affected rendering constraint or image prompt before presenting the package; return to the page contracts only when the approved content logic itself is responsible.

6. Prepare independent square-image delivery

   Deliver the final images as separate `1:1` files. Every image must have a complete composition and be uploadable on its own. Keep the approved lighting, product identity, recurring visual motifs, typography system, spacing rhythm, content, and visual direction consistent. Do not connect backgrounds or elements across image boundaries. Keep visible product color, shape, brand marks, and distinctive components consistent across the set.

7. Audit the result

   After generation, check whether every result is a separate square US ecommerce image that can be understood and uploaded independently. Also check whether the product drifted, text became garbled, any Chinese/Han/CJK glyph or untranslated source text is visible, layout hierarchy failed, claims absent from all supplied sources appeared, or reference-supplied claims lost their provenance. Give specific revision advice before proposing another generation pass. A language failure can never pass because the remaining content is otherwise correct or visually polished.

   When a competitor reference exists, the final audit must compare every actual slice with all competitor pages and modules mapped into its contract. Fail the result if the page purpose, conclusion, module sequence, evidence relationship, hierarchy, or transferable information density was lost. Repeated imagery is a failure when it makes page responsibilities indistinguishable, but it is not a substitute for this content-architecture review.

   The final audit must read the approved page contracts and inspect all final images individually; a contact sheet may be used only as an internal overview. For each image, state the visible takeaway in one sentence and verify that it matches the contract. Do not pass a set merely because it is visually polished when the information story is unclear.

   Route revisions to the smallest responsible layer instead of regenerating the full set by default:

   - Copy or wording failure: revise the affected module's `visible_copy` and regenerate only the affected slice or repair its text area.
   - Product identity, orientation, color, shape, logo, or component failure: strengthen the product-reference constraint and regenerate only the affected slice.
   - Single-screen hierarchy or clutter failure: revise that screen's evidence allocation, module sequence, visual hierarchy, or exact copy while preserving its approved page responsibility.
   - Repeated visual grammar across several screens after content contracts pass: revise those screens' composition while keeping their approved conclusions, evidence, and unaffected screens.
   - Whole-set style consistency failure: revise the text visual master, then regenerate only the images influenced by the change when possible.
   - Whole-page buyer-journey or reference-mapping failure: return to the page contracts. Use full regeneration only when the approved content architecture changes substantially.

8. Deliver the image set

   After generation, revision, and final audit are complete, save the approved image set without adding a separate destination-confirmation step. If the user has already provided a destination, use it. Otherwise, create a clearly named delivery folder under the current workspace, such as `outputs/product-detail-page/<product-name>-<timestamp>/`. If there is no usable workspace, create the delivery folder beside the working source assets or in the active working directory. Preserve the original generated files.

   Deliver the complete set of approved individual square images with clear sequential filenames. Do not include a `1:3` master, `9:21` slices, an early concat preview, or a final long-image concat unless the user explicitly requests those separate artifacts. Do not include rejected or superseded variants unless the user explicitly asks for all iterations.

   Verify that every requested file exists in the delivery folder, is square, and contains English-only visible text with no Chinese/Han/CJK glyphs. Do not deliver a file that fails this language check. At the end, report the delivery folder path and a short completion status so the user can open the folder and review the images. Do not ask the user to choose a save path after generation is already complete. Use clear names such as `product_image_01.png` through at least `product_image_10.png`.

## Page Principles

- Make the first screen answer: what is this, who is it for, and why does it matter now?
- Prefer concrete capability language over vague adjectives.
- Let examples, parameters, screenshots, comparisons, and workflows carry credibility.
- Avoid nested cards, decorative blobs, generic gradients, and hero sections that hide the actual product.
- Keep headings proportional to their containers; do not use hero-scale type inside compact panels.
- Use stable dimensions for fixed-format UI such as tabs, toolbars, media frames, grids, counters, and feature tiles.
- Treat mobile as a first-class page, not a compressed desktop afterthought.

## Content Checklist

- Product name and category are visible immediately.
- Primary CTA matches the user's intended business or workflow goal.
- Capabilities are specific enough to be testable or recognizable.
- Sections are ordered by user decision flow, not by internal feature inventory.
- Technical claims include constraints, assumptions, or usage context when needed.
- The page includes enough concrete examples for a new visitor to understand the product.
- For image-led ecommerce pages, specifications, materials, certifications, awards, and measured parameters may come from the user's materials or a supplied competitor reference. Record competitor-derived items as `reference_supplied_unverified` in the approval package; invent nothing absent from all supplied sources.

## Implementation Checklist

- Inspect existing components, routes, and styles before adding new abstractions.
- Use assets that show the product, output, workflow, or real subject matter.
- Confirm images, videos, canvases, or generated visuals render correctly.
- Check at least one desktop and one mobile viewport for overflow and overlap.
- Run available build, lint, or tests when the project provides them and the change scope warrants it.
- Report the local URL or file path the user can open.

## References

Read `references/detail-page-patterns.md` when choosing section patterns, adapting the skill to a specific product category, or reviewing whether a page structure is complete.

For every multi-image ecommerce workflow, also read `references/page-content-architecture.md` before writing prompts or generating images.
