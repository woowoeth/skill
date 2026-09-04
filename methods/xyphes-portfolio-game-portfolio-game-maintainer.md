---
name: portfolio-game-maintainer
description: Design, implement, or audit the bilingual React classic portfolio, Phaser adventure, shared content, quests, assets, accessibility, and PWA behavior in portfolio-game. Do not use for generic TypeScript work unrelated to this product.
---

# Portfolio game maintainer

Classify the change as shared content, classic React UI, Phaser adventure, asset/audio, or PWA/offline work. Read `AGENTS.md`, then inspect the canonical content and contracts for the affected area.

## Shared content

Change the canonical entity first. Reference its stable ID from zones, quests, and dialogues. Do not place editorial prose in Phaser scenes or map files. Reject invented facts and incomplete FR/EN pairs.

For a cross-mode change, verify that one entity is rendered by the classic UI and exposed by a Phaser interaction without duplicated prose.

## Gameplay

Keep the world open and screen-based. Professional discovery must remain completable in 5-10 minutes; optional hobbies may add at most 5 minutes. Combat is brief and non-punitive. Classic mode, CV, and contact remain reachable without completing a challenge.

## Assets

Verify license and provenance before integration, update `docs/asset-licenses.md`, copy only used files, and preserve crisp pixel-art scaling. Never use Zelda or Nintendo assets, identifiers, layouts, or audio.

## Validation

Select checks by impact. At minimum run typecheck, lint, unit tests, and build. For affected behavior also verify direct routes, React/Phaser mount cleanup, saved-state recovery, FR/EN parity, keyboard/touch access, no audio autoplay, PWA offline behavior, and the absence of Phaser from the classic bundle.
