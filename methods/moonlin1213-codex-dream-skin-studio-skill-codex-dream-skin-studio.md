---
name: codex-dream-skin-studio
description: Create and apply one-click Codex Dream Skin themes on macOS or Windows from a single reference image. Use when the user wants an image analyzed into a Codex UI skin, generated wallpaper and optional assets, a style-choice flow, a cross-platform theme pack, safe install/switch, or a double-click launcher that restores the latest saved skin after reopening Codex.
---

# Codex Dream Skin Studio

Turn one supplied image into a complete, installable Codex visual theme. Treat the image as a visual reference, never as a UI screenshot to clean up. Keep the workflow staged and reversible: analyze first, ask for the style direction, generate or prepare the artwork, validate it, package it, then apply it only through the installed Dream Skin engine.

## Current engine compatibility

- macOS official ChatGPT/Codex Desktop `26.727.51351` (build `6119`, Chromium `150.0.7871.182`) requires Dream Skin engine `VERSION` `1.2.2` or newer. Older `1.2.1` engines can save a theme but miss the CDP endpoint on the default profile or misplace the new home title/cards/composer because the host shell no longer exposes the old `main.main-surface` layout.
- The packaged macOS reopen launcher enforces that `1.2.2` floor and should tell the user to update the engine rather than retrying a mismatched live apply.
- That floor is not a performance guarantee. Before macOS application, run the read-only engine preflight described in [references/engine-health.md](references/engine-health.md). It recognizes the known unguarded root-refresh pattern and the guarded legacy variant without rejecting repaired copies merely because their version is still `1.2.2`. Unknown code is unverified, not safe. Installing this Skill does not patch or upgrade the engine.
- Use upstream `Fei-Away/Codex-Dream-Skin` `v1.5.11` or newer as the default engine source; it includes the `1.2.2` compatibility line and later Codex `26.727` fixes. Do not route users through a fork unless they explicitly ask for that fork and have verified it is synced.
- Windows remains supported through the separately installed Windows Dream Skin engine under `%LOCALAPPDATA%\CodexDreamSkin\engine`. After updating this Skill, tell Windows users to reinstall/update the Windows engine from upstream `Fei-Away/Codex-Dream-Skin` so `stage-theme-windows.ps1`, the `.lnk` safety wrapper, and `verify-dream-skin.ps1` all point at the matching managed runtime. Do not imply that installing the Skill alone updates the Windows engine.

## Interaction contract

1. Inspect the supplied image before asking broad questions. Record the visible subject, approximate age presentation, composition, dominant colors, contrast, materials, lighting, camera or illustration language, and likely focal point.
2. If the user has not specified a style, ask one focused question with a compact choice list. Offer at least: 可爱卡通, 简洁高级, Le Labo 极简, 赛博朋克科幻, 低饱和莫兰迪, 艺术感. Include `自定义` and allow a short free-form answer. Do not ask the user to understand theme schemas or image dimensions.
3. Ask only decisions that materially change the result: whether to preserve a real person's likeness, light/dark/auto shell preference, optional theme name, and whether optional sticker/avatar assets are wanted. Require explicit rights confirmation before preserving a real person's likeness. Default to an original fictional adult when rights are not confirmed.
4. Summarize the proposed visual direction in 5-8 concrete bullets and get one confirmation before paid or irreversible image generation. State what will be generated and what the current renderer can display.

## Workflow

### 1. Analyze and translate

Infer the following from the supplied image:

- subject placement, silhouette, pose, and identity-critical details;
- a palette of 4-6 colors, luminance range, accents, and overlay compatibility;
- materials, texture, depth of field, perspective, and light direction;
- a calm left-side continuation and a detailed right-side focal area.

Translate the chosen style into explicit scene objects, surfaces, medium, light, and palette. Prefer concrete nouns and physical light behavior over generic quality words. Read [references/background-method.md](references/background-method.md) before writing the generation prompt.

### 2. Generate a real background

Use the prompt structure in the background-method reference. The non-negotiable output contract is:

- opaque standalone `2560x1440` 16:9 artwork;
- one continuous physical or illustrated scene across the canvas;
- native-content safe zone at `x=0%-52%`, transition at `x=45%-62%`, focal subject at `x=62%-88%`;
- critical details within `y=16%-72%`, face around `y=20%-52%`, hands around `y=30%-70%`, with at least 8% edge padding;
- no UI, window chrome, sidebar, panel, card, button, input box, cursor, readable text, logo, signature, watermark, split panel, collage, duplicate person, or malformed anatomy.

Use Image 1 only for broad style and composition, Image 2 only for environment and materials, and Image 3 only for an explicitly authorized adult identity workflow. If a generator supports negative prompts, include the negative list from the reference.

### 3. Produce optional supporting assets

When requested, generate an avatar portrait, decorative sticker, small badge, or theme preview from the same approved art direction. Keep these as separate files with transparent or opaque backgrounds as appropriate. Do not bake text or stickers into `background.jpg`.

The stable cross-platform renderer contract is `theme.json + background.jpg`; it does not automatically render arbitrary sticker fields. Package optional files under `assets/` with a short manifest and describe them as delivered assets until a supported renderer field exists. Never add unsupported JSON fields and claim they are visible.

### 4. Validate before packaging

Resolve the installed skill directory and run the dependency-free validator. It reads PNG, JPEG, and WebP dimensions directly in Node.js and does not depend on macOS `sips` or a Windows image utility.

macOS or Linux shell:

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/codex-dream-skin-studio"
node "$SKILL_ROOT/scripts/validate-wallpaper.mjs" --file "/path/to/background.png"
```

Windows PowerShell 5.1+:

```powershell
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$SkillRoot = Join-Path $CodexHome 'skills\codex-dream-skin-studio'
node "$SkillRoot\scripts\validate-wallpaper.mjs" --file "C:\path\to\background.png"
```

Reject output that is not exactly `2560x1440`, is larger than 16 MB, or is not PNG, JPEG, or WebP. Preview CSS `cover` crops at 16:9, 16:10, 4:3, and ultrawide ratios. Check light and dark translucent overlays. Regenerate or crop deliberately; never stretch a non-16:9 image.

### 5. Create the one-click theme pack

Detect the host platform before choosing commands. Use the installed engine and keep theme creation separate from application.

On macOS:

```bash
ENGINE="$HOME/.codex/codex-dream-skin-studio"
"$ENGINE/scripts/customize-theme-macos.sh" \
  --image "/path/to/background.png" \
  --name "Theme name" \
  --tagline "Optional short line" \
  --accent "#RRGGBB" \
  --secondary "#RRGGBB" \
  --highlight "#RRGGBB" \
  --no-apply
```

The command converts and stages a JPEG plus `theme.json` in the live theme directory. For a distributable preset, copy those two files to `macos/presets/preset-<slug>/` and keep optional supporting assets beside them. Use `switch-theme-macos.sh --id <theme-id> --no-apply` to stage a saved theme without touching Codex.

On Windows, the official Store-installed `OpenAI.Codex` app, Windows PowerShell 5.1+, Node.js 22+, and the separately installed Windows Dream Skin engine are required. Stage and save a theme without applying it:

```powershell
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$SkillRoot = Join-Path $CodexHome 'skills\codex-dream-skin-studio'
& "$SkillRoot\scripts\stage-theme-windows.ps1" `
  -Image "C:\path\to\background.png" `
  -Name "Theme name" `
  -ThemeJson "C:\path\to\theme.json"
```

The Windows staging script validates the image through the installed engine, copies it into `%LOCALAPPDATA%\CodexDreamSkin`, updates `active-theme`, and saves a self-contained copy under `themes`. It does not touch Codex unless `-Apply` is explicitly passed. Use `switch-theme-windows.ps1 -List`, then `switch-theme-windows.ps1 -Id <theme-id>` to stage a saved theme; add `-Apply` only after the restart policy below has been considered.

### 6. Apply without restart loops

On macOS, require engine `VERSION` 1.2.2 or newer, then read `status-dream-skin-macos.sh --json --deep` first. Engine 1.2.0 has a known LaunchServices/process-locale race that can lose CDP and remain stuck on Applying; engine 1.2.1 can still mismatch official ChatGPT/Codex Desktop `26.727.51351` because it lacks the dedicated profile/CDP and new home-layout compatibility fixes. Do not invoke mismatched engines through the reopen launcher.

- If `session` is `active` and `cdpOk` is true, apply through the hot path or saved-theme switcher.
- If `session` is `off` and Codex is not running, one controlled start is allowed.
- If Codex is running but `cdpOk` is false, do not call `start-dream-skin-macos.sh --prompt-restart` repeatedly. Explain that the existing process has no verified CDP endpoint and ask for one explicit controlled restart, or hand the user the packaged reopen launcher. Never silently kill or restart the app more than once per request.
- After an apply attempt, verify `session`, `injectorAlive`, `cdpOk`, `themeName`, and `appliedThemeName`. If verification fails, say that the theme remains saved but live injection is inactive, leave it staged, and report the exact state; do not keep retrying restarts.
- After a successful macOS apply, offer one short idle sample on a settled visible page using [engine-health.md](references/engine-health.md); use it when investigating heat or validating a renderer fix. Do not claim performance verification from session status alone. A hidden/busy page or unavailable endpoint is inconclusive, not permission to restart or install monitoring.

On Windows, stage first, then run the installed engine's `verify-dream-skin.ps1` if a Dream Skin session is already expected to be live. If verification reports no verified endpoint, do not force a process restart. Ask for one explicit controlled restart or use the packaged Windows launcher, which runs `apply-last-theme-windows.ps1`; that wrapper delegates exactly once to `start-dream-skin.ps1 -PromptRestart`. After launch, run `verify-dream-skin.ps1` once; on failure, preserve `%LOCALAPPDATA%\CodexDreamSkin\active-theme`, say that the theme remains saved but live injection is inactive, and report the relevant `state.json`, `verify.log`, and injector-log paths. When users update this Skill, remind them to update the Windows engine from the same current Dream Skin source because the `.lnk` and staging helpers call that separate managed runtime. Never loop `-RestartExisting` or bypass the engine's Store-package identity checks.

#### Relaunch and persistence boundary

Theme-file persistence is not the same as live-injection persistence. The installed engine saves the theme pack, but its external injector and loopback debug endpoint belong to the current Codex process. A standard Codex launch does not automatically restore them.

- When delivering or applying a theme on either platform, proactively tell the user that opening Codex through its standard icon may show the official appearance even though the saved theme still exists.
- Offer to create the packaged double-click launcher in a user-chosen location. Default to `Downloads` when the user has no preference.
- On macOS:

  ```bash
  SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/codex-dream-skin-studio"
  "$SKILL_ROOT/scripts/install-reopen-launcher-macos.sh" \
    --output-dir "$HOME/Downloads"
  ```

- On Windows PowerShell 5.1+:

  ```powershell
  $CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
  $SkillRoot = Join-Path $CodexHome 'skills\codex-dream-skin-studio'
  & "$SkillRoot\scripts\install-reopen-launcher-windows.ps1" `
    -OutputDirectory (Join-Path $HOME 'Downloads')
  ```

- Explain that the launcher reads the engine's current live theme, which is the most recently saved or selected theme. It does not hard-code one preset.
- Existing macOS launchers are script copies. After updating this Skill, offer a backed-up replacement to pick up preflight, with explicit permission for `--force`. Custom combined launchers calling the engine directly need their own integration; do not overwrite them with the plain skin launcher.
- After a standard Codex restart shows the default appearance, the user can double-click the launcher. If Codex is already running without CDP, the launcher requests one controlled restart confirmation and then applies that theme. It never registers a background agent or silently restarts Codex.
- If the user wants another location or localized filename, pass `--output-dir` / `--name` on macOS or `-OutputDirectory` / `-Name` on Windows. Use `--force` or `-Force` only with explicit permission when replacing an existing launcher.
- On macOS, if `themeName` is present while `session=stale`, `injectorAlive=false`, or `cdpOk=false`, explain that the theme is saved but not live. On Windows, the equivalent evidence is a valid `active-theme\theme.json` with a missing or unverifiable live endpoint. Ask the user to double-click the platform launcher once. Do not describe this as theme loss.
- If the user requires the standard Codex icon to restore the skin automatically, explain that this needs an engine-level relaunch or persistence feature. Do not claim the Skill implements autostart, create an unsupported `LaunchAgent`, or modify the Codex application bundle.

Use the installed restore launcher or restore script to return to the official appearance. The project is an external loopback injector and must not modify the Codex application bundle, `app.asar`, code signatures, API settings, or provider configuration.

### 7. Preserve home-card placement

When renderer CSS is part of the task, keep the native home suggestion-card group (`.group/home-suggestions`) immediately above the composer with a responsive gap rather than a fixed position directly below the hero. Use a viewport-height-aware offset and a compact-height override. Verify in a full home screenshot that card bottoms sit roughly 48-120px above the composer top, with no overlap and a readable title above them.

## Style translation defaults

- **可爱卡通**: rounded original shapes, soft cel shading, playful props, clear silhouette, controlled high-key accents.
- **简洁高级**: restrained objects, matte/gloss material contrast, generous midtone space, one refined focal detail.
- **Le Labo 极简**: warm paper, raw glass, muted ink and earth colors, tactile labels represented only as abstract marks, no readable text or brand marks.
- **赛博朋克科幻**: coherent neon light sources, dark lifted shadows, reflective materials, holographic atmosphere, no UI panels or fake screens.
- **低饱和莫兰迪**: dusty sage, parchment, clay, smoke blue, soft contrast, natural texture that survives both shells.
- **艺术感**: choose one bounded medium such as editorial collage, gouache, ink wash, oil, or analog film; keep perspective, texture, and light coherent.

## References

- [background-method.md](references/background-method.md): generation prompt, safe-zone geometry, reference-image roles, and acceptance checklist.
- [runtime-contract.md](references/runtime-contract.md): supported theme metadata, macOS and Windows commands, status interpretation, and restart guards.
- [engine-health.md](references/engine-health.md): macOS preflight, short idle sampling, result limits, and data-preserving recovery.
