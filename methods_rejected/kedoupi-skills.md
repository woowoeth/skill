---
name: skill-incubator
description: >
  Use when working inside the Skills incubator (kedoupi/skills): create a new
  installable agent skill as a <name>-skill GitHub submodule, scaffold with
  new-skill.sh, register-submodule.sh, edit or fix an existing skill, bump
  versions, run offline tests, or prepare publish/release. Triggers: 新建 skill,
  创建 skill, scaffold, new-skill, 改 skill, 修改 skill, edit skill, bump version,
  release skill, publish skill, 孵化器, incubator, submodule, /skill-incubator.
  Not for end-user Feishu/Lark messaging (lark-push) and not for generic Grok-only
  ~/.grok skills.
metadata:
  version: "0.4.0"
---

# Skill Incubator

Project-local meta skill for the **parent** repo `kedoupi/skills`. Guides agents
that **author** product skills. **Not** published via `npx skills add`.

## Always

1. Resolve **incubator root**: contains `schema/`, `_template/`, `scripts/new-skill.sh`.
2. Contract SoT: [`schema/skill-repo.md`](../../../schema/skill-repo.md); product registry SoT: `products.json`.
3. **Naming**
   - Package (`SKILL.md` name): `<name>` (e.g. `lark-push`)
   - GitHub + submodule dir: `<name>-skill` (e.g. `lark-push-skill`)
   - Install: `npx skills add kedoupi/<name>-skill`
   - Path: `<name>-skill/skills/<name>/`
4. Parent is git + **submodules**; each product repo is its own GitHub and is type `single` or `family`.
5. Scaffold creates a `single` product via `bash scripts/new-skill.sh …` (do not hand-copy `_template`).
6. Never ship this meta skill inside a product package.

Example product: package `lark-push` in submodule dir `lark-push-skill` (`kedoupi/lark-push-skill`).

Checklists: [references/checklist.md](./references/checklist.md).

## Route

| User intent | Section |
| --- | --- |
| 新建 / create / scaffold | [New skill](#new-skill) |
| 修改 / edit / bump | [Edit skill](#edit-skill) |
| 发布 / tag / publish | [Release skill](#release-skill) |
| 列表 / 健康检查 | [List & doctor](#list--doctor) |

## New skill

### 1. Align

- Triggers, side effects, deps, durable config, publish vs private
- Package `name` (kebab-case) + author (default `kedoupi`)

### 2. Validate

- Package name legal; reserved: `_template`, `schema`, `scripts`, `agents`, `docs`
- Neither `<name>` nor `<name>-skill` top-level dir should already exist

### 3. Scaffold

```bash
bash scripts/new-skill.sh <name> [--author kedoupi]
# → ./<name>-skill/ with skills/<name>/
```

### 4. Implement (inside `<name>-skill/`)

1. `skills/<name>/SKILL.md` — triggers + `metadata.version`
2. Scripts with `pwd -P`; offline dry-run if side effects
3. README EN + zh-CN; repo `AGENTS.md`; thin `CLAUDE.md`
4. `bash tests/run.sh` and `npx skills add ./ --list`

### 5. Publish child + register submodule

```bash
# create empty GitHub kedoupi/<name>-skill, then in child:
git remote add origin git@github.com:kedoupi/<name>-skill.git
git push -u origin main

# from incubator root:
bash scripts/register-submodule.sh <name>-skill
git push origin main   # parent, after user approves
```

### 6. Registry + catalog (**mandatory**)

Parent root **`products.json`** is the product directory; README/AGENTS tables are
generated views. Incomplete if a product or entrypoint ships but is missing/stale.

```bash
# after submodule register / first public release:
# 1) add products.json object: type, primary, entrypoints, purpose, repo, install
# 2) add a short install blurb if non-trivial
# 3) generate and verify:
bash scripts/render-catalog
bash scripts/check-catalog
bash scripts/doctor
```

Schema SoT: `schema/skill-repo.md` § **Product registry and generated catalog**.

## Edit skill

### 1. Locate

- Submodule path: `<name>-skill/` (e.g. `lark-push-skill/`)
- Read child `AGENTS.md` + `skills/<name>/SKILL.md`

### 2. Classify

| Kind | Action |
| --- | --- |
| Behavior | Code + bump primary `metadata.version`; sync lockstep family entrypoints; render catalog |
| Docs only | No version bump; registry/catalog optional unless product facts changed |
| Incubator-wide | `schema/` + `_template/` on **parent** |

### 3. Git (two repos)

```bash
# inside child submodule
git add … && git commit && git push

# parent: bump pointer; update products.json if purpose/entrypoints changed
cd <incubator-root>
bash scripts/render-catalog
git add <name>-skill products.json README.md AGENTS.md
git commit -m "chore: bump <name>-skill (+ generated catalog if needed)"
bash scripts/check-catalog
```

Confirm before any push.

## Release skill

1. Child: `bash tests/run.sh` green  
2. Version = tag `vX.Y.Z`; push tag on **child** remote  
3. `npx skills add kedoupi/<name>-skill --list`  
4. Parent: submodule pointer + optional registry changes + `bash scripts/render-catalog`
5. `bash scripts/check-catalog` green, then parent commit/push

**Do not** ship a release with only a submodule SHA bump and stale registry/generated views.

## List & doctor

Prefer scripts (deterministic):

```bash
bash scripts/list-skills
bash scripts/render-catalog --check
bash scripts/check-catalog        # registry ↔ packages ↔ generated views
bash scripts/check-skill-layout   # docs / tests / artifacts separation
bash scripts/doctor               # includes catalog + layout
bash scripts/link-agent-skills    # optional Claude/Grok vendor symlinks
```

| Check | Expect |
| --- | --- |
| Parent git | `kedoupi/skills` |
| Schema / template / scripts | present + executable |
| Meta skill | `.agents/skills/skill-incubator/SKILL.md` |
| Product | registered `single` or `family`; all `skills/*/SKILL.md` entrypoints declared |
| Catalog | products.json matches packages/submodules; generated tables current |
| Layout | `docs/` · `tests/` · `artifacts/` separation (`schema/skill-repo.md`) |

## Safety

- Confirm before `git push`, tag, or GitHub create on parent or child
- No secrets in packages; no `rm -rf` product dirs without explicit ask
- Do not publish this meta skill

## Out of scope

| Need | Instead |
| --- | --- |
| Feishu push | product `lark-push` |
| Generic Grok skill | Grok create-skill |

## References

- `schema/skill-repo.md`
- `scripts/new-skill.sh`, `scripts/register-submodule.sh`
- `scripts/list-skills`, `scripts/doctor`, `scripts/link-agent-skills`
- `references/checklist.md`
- root `AGENTS.md`
