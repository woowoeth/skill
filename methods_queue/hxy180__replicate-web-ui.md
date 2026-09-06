---
name: replicate-web-ui
description: Analyze and rebuild the visual design, responsive layout, components, interaction states, and motion of a reference URL, screenshot, or video inside the user's existing frontend project. Use when the user asks to recreate, clone, replicate, migrate, reverse engineer, or take inspiration from a website, page, component, animation, or design language. Inspect the reference, document evidence when useful, implement with the target project's current framework, and verify the result in a real browser. Do not use to copy private source code, protected brand assets, deceptive authentication or payment pages, or material the user is not authorized to reproduce exactly.
---

# Replicate Web UI

Rebuild how a reference interface looks and behaves using original, project-native code. Treat the reference as visual and behavioral evidence, not as source code to copy.

## Inputs and defaults

Discover from the request and workspace:

- Reference URL, screenshot, video, or combination
- Target repository and route or component
- Existing framework, styling system, design tokens, and commands
- Fidelity: `inspired`, `close`, or `exact-authorized`
- Important viewports, states, and motion

Ask only when the reference or target cannot be discovered. Default to `close`, the target project's current stack, and desktop, tablet, and mobile verification.

Require a clear ownership or permission statement before using `exact-authorized`. Otherwise use `close` and replace identity-bearing material.

## Workflow

### 1. Preflight

- Inspect the target repository before choosing an implementation.
- Identify its framework, router, package manager, component library, tokens, fonts, asset conventions, and test commands.
- Check the worktree and preserve unrelated changes.
- Confirm that the reference is accessible and that browser or media-inspection tools are available.
- Read [references/compliance-boundaries.md](references/compliance-boundaries.md) for sensitive, brand-heavy, proprietary, login, payment, financial, medical, or government interfaces.
- For a full page or multi-component task, create `docs/replicate-ui/`; skip research files for a small component unless they reduce ambiguity.

If no target project exists, ask before scaffolding one. Do not assume Next.js, React, Tailwind, or any component library.

### 2. Reconnaissance

Read [references/visual-analysis.md](references/visual-analysis.md), then collect evidence appropriate to the input.

#### Live URL

1. Capture the top and full page at `1440px`, `768px`, and `390px`, plus any visible breakpoint.
2. Scroll from top to bottom before clicking. Record sticky navigation, reveals, parallax, scroll snapping, and layout transitions.
3. Exercise meaningful hover, focus, active, selected, expanded, loading, error, menu, drawer, modal, carousel, and accordion states.
4. Use computed styles on representative elements to measure geometry, typography, color, borders, shadows, positioning, transitions, and animation. Do not estimate values that can be inspected.
5. Inventory images, video, SVG, icons, and fonts, but download or reuse only material the user may lawfully use.

Do not click irreversible controls, submit forms, authenticate, purchase, delete, or mutate external data merely to observe a state.

#### Screenshot

- Measure geometry, hierarchy, alignment, aspect ratios, typography, spacing, and visual tokens from visible evidence.
- Distinguish observed facts from inferred responsive or interactive behavior.
- Request additional states only when an unsupported inference would materially affect the implementation.

#### Video or GIF

- Review the sequence at normal speed and frame by frame around transitions.
- Record trigger, initial state, final state, duration, delay, easing, direction, stagger, and interruption behavior.
- Map each visible moment to a component state; do not treat the video as a single static screenshot.

If access is blocked, continue from available screenshots or video and report which states could not be observed.

### 3. Build a reference specification

For a complex page, write only the artifacts that will guide implementation:

- `docs/replicate-ui/REFERENCE.md`: capture matrix, design tokens, asset decisions, and breakpoint summary
- `docs/replicate-ui/BEHAVIORS.md`: scroll and interaction state table
- `docs/replicate-ui/components/<name>.md`: component geometry, layering, states, content, and responsive behavior

Use [references/research-templates.md](references/research-templates.md) for concise templates. Record evidence, not copied production markup. Outer HTML may be inspected to understand layering, but do not paste it into the implementation as a shortcut.

### 4. Define the adaptation

- Separate reusable design principles from the reference's identity.
- Map reference sections to the user's content, product goals, and information architecture.
- Reuse target-project tokens and components where close enough; add a small token layer only when needed.
- Replace logos, trademarks, proprietary copy, copyrighted illustrations, photography, paid fonts, and tracking identifiers unless the user supplies them or confirms rights.
- Prefer local, licensed assets. Never hotlink production assets as a permanent implementation.
- Preserve the fidelity contract: `inspired` may change composition, `close` matches experience while changing identity, and `exact-authorized` pursues pixel-level similarity for authorized material.

### 5. Implement incrementally

- Match page shell and large geometry first, then responsive flow, typography, spacing, visual detail, interaction, and motion.
- Follow the repository's component boundaries and naming conventions. Do not force one file per visual block when the codebase uses another pattern.
- Keep each meaningful component runnable before moving on. Run the cheapest relevant typecheck, unit test, or build check at useful milestones.
- Use semantic HTML, keyboard-accessible controls, visible focus, readable contrast, and `prefers-reduced-motion` fallbacks.
- Use precise values when the reference depends on them, but avoid brittle absolute positioning when normal layout can reproduce the behavior.
- Avoid new dependencies when the existing stack can implement the effect.
- Do not copy minified bundles, hidden APIs, analytics, credentials, or private source.

### 6. Assemble and verify

1. Start the target application and open the implemented route in a real browser.
2. Capture the same viewports and states used during reconnaissance.
3. Compare reference and implementation section by section, not only above the fold.
4. Fix overflow, wrapping, stacking, font metrics, spacing, crop, breakpoint, state, and animation discrepancies.
5. Verify keyboard interaction, focus, reduced motion, and basic contrast where relevant.
6. Run repository tests, lint, typecheck, and build commands appropriate to the change.

For same-size PNGs, use:

```powershell
python scripts/compare_screenshots.py reference.png implementation.png --diff diff.png
```

Treat the score as diagnostic evidence, not the objective. Intentional changes in branding and content should remain different.

## Failure handling

- Browser blocked: use supplied media, document unavailable states, and avoid pretending hidden behavior was verified.
- Cross-origin styles inaccessible: inspect representative elements through computed styles instead of scraping stylesheets.
- Font or asset unavailable: use a licensed metric-compatible substitute and record the difference.
- Network or download failure: retry a bounded number of times, then use a local substitute without blocking unrelated implementation.
- Reference changes during work: preserve timestamped captures and implement against the captured state.
- Existing tests fail before edits: distinguish baseline failures from regressions and report both.

## Completion standard

Do not stop at a style audit, screenshots, specifications, or a plan when implementation was requested. Finish when the requested code runs, relevant states are visually checked, and verification results and intentional differences are reported, unless an external blocker makes that impossible.

Report:

- What was implemented
- Which reference traits were preserved
- Which assets or behaviors were intentionally changed
- Viewports and states verified
- Commands run and remaining limitations
