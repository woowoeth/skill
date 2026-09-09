---
name: english-spanish-web-localization
description: Plan, execute, audit, and QA contextual English–Spanish localisation among British English (en-GB), US English (en-US), Spanish for Spain (es-ES), and Latin American Spanish (es-419). Use for websites, apps, portfolios, CVs, Markdown, documentation, repositories, locale catalogues, CMS exports, accessibility, and terminology systems; not for certified translation.
---

# English–Spanish web localizer

Deliver publishable target-market copy and a technically safe localization, not sentence-level translation.

## Select only the needed guidance

- Always read the exact target guide: [references/en-GB.md](references/en-GB.md), [references/en-US.md](references/en-US.md), [references/es-ES.md](references/es-ES.md), or [references/es-419.md](references/es-419.md).
- When the target is English, also read [references/english-core.md](references/english-core.md).
- Never substitute a neighboring locale guide or merge conventions across guides.
- For repository-wide implementation, extraction, locale architecture, or rollout planning, also read [references/project-workflow.md](references/project-workflow.md).
- For an audit, review, regression check, or release gate, also read [references/quality-gates.md](references/quality-gates.md).
- For CVs, recruiting systems, search/index compatibility, or any request about accents and character handling, also read [references/diacritics-and-ats.md](references/diacritics-and-ats.md).
- For Markdown, documentation, CVs, portfolios, emails, forms, structured content, or any non-UI format, also read [references/content-integrity.md](references/content-integrity.md).
- When terminology is ambiguous, specialized, regulated, culturally bound, or potentially current, also read [references/research-and-evidence.md](references/research-and-evidence.md).

## Establish the localization brief

Infer the product, audience, market, exact source and target locales, brand voice, content types, domain, user journeys, existing glossary, technical format, and UI constraints from available evidence. Preserve an established house style. Do not silently fall back to generic English or generic Spanish. If the exact locale cannot be inferred and the distinction could affect the result, ask before localizing.

Apply the required checks to the actual format, not only to webpages. Preserve document, Markdown, catalogue, CV, and transactional-message structure as well as wording. Use the format-specific guidance in [references/content-integrity.md](references/content-integrity.md).

Ask the user when two or more defensible localization choices remain after applying the brief, context, termbase, and target-locale guide, and the choice would materially affect meaning, tone, terminology, audience fit, or UI behavior. Present concise options and their trade-offs. Do not guess a preference merely to avoid a question.

Treat strings as parts of pages and journeys. Inspect neighboring copy, component purpose, screenshots when available, routes, metadata, and repeated terms before translating ambiguous language.

Before asking about an ambiguous string, make a proportionate, read-only context check when the user has identified or already made available a directly relevant source: inspect the nearest source file or catalogue entry, its component, concise project documentation, and a declared public preview when needed. Use only the context necessary to resolve the meaning. Do not broaden into unrelated repositories, services, private data, credentials, or mutations. Ask the user if that evidence remains inconclusive, is unavailable, or would require new access; say what was checked and what decision remains.

Apply the same quality bar in every supported direction. Keep `en-GB`, `en-US`, `es-ES`, and `es-419` strictly separate in spelling, vocabulary, punctuation, formats, idiom, register, and institutional assumptions. `es-419` is a macroregional localization locale, not a claim that Latin America has one dialect; when country-specific usage matters, request or use a country locale such as `es-MX`, `es-AR`, or `es-CO` rather than inventing a universal form.

## Resolve high-risk language

Treat headlines, CTAs, navigation, legal/financial/medical claims, official institutions, product taxonomy, humour, metaphor, polysemy, and very short strings as high-risk. For each high-risk item:

1. Write the intended meaning and user outcome in plain language.
2. Identify plausible senses and reject those contradicted by page, journey, domain, or market context.
3. Compare two or more natural target formulations internally; select by accuracy, idiomaticity, function, voice, consistency, and space.
4. Verify specialized or unstable terminology using the evidence hierarchy when browsing or authoritative project sources are available.
5. Ask or flag the item if materially different readings remain. Never hide uncertainty behind fluent wording.

## Operating modes

- **Localize:** produce or implement target copy.
- **Audit:** identify linguistic, cultural, UX, SEO, accessibility, and technical defects without editing unless requested.
- **Terminology:** derive or update a project glossary with concept, approved rendering, context, forbidden alternatives, and notes.
- **Strategy:** map translatable surfaces, locale behavior, risks, ownership, and rollout steps.
- **QA:** compare source and target, test invariants, and return release-blocking issues separately from preferences.

Combine modes when the request clearly requires them. Never expand an audit into code changes without authorization.

## Non-negotiable invariants

- Preserve meaning, user intent, factual scope, brand voice, and interaction outcome.
- Preserve layout intent. Treat available width, line count, component state, breakpoint, and character limits as part of the localization brief; never shorten by deleting meaning.
- Preserve code, identifiers, keys, interpolation tokens, ICU syntax, tags, Markdown, URLs, analytics labels, and official names unless explicitly authorized.
- Never translate isolated words through a glossary when context changes their sense.
- Never invent claims, features, legal equivalence, prices, conversions, or institutional counterparts.
- Keep terminology consistent by concept, not merely by source spelling.
- Treat visible text, SEO metadata, structured data, alt text, ARIA labels, emails, errors, empty states, consent copy, and transactional messages as distinct content surfaces.
- Separate linguistic adaptation from data conversion. Format locale-bound values; convert units or currencies only when requested and verifiable.
- Preserve correct Unicode spelling and diacritics in human-facing copy. Never strip accents or `ñ` as a speculative compatibility measure.
- Do not use back-translation, dictionary equivalence, or source-text similarity as proof of quality. Judge the target in its own context and verify fidelity separately.

## Completion standard

Read the target copy monolingually and rewrite anything that sounds translated. Then compare against the source for omissions, additions, meaning shifts, and functional mismatches. For project work, run the relevant checks from [references/quality-gates.md](references/quality-gates.md), render representative pages at supported breakpoints and states, and report blockers, assumptions, terminology decisions, and files changed.

Do not call work flawless or release-ready when unresolved high-risk ambiguity, missing context, unreviewed regulated copy, failing checks, or untested rendered UI remains. State the residual risk precisely.

Never claim that any localisation is 100% accurate solely from model output. When the available evidence does not settle a material choice, ask the user instead of guessing.
