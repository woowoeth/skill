---
name: cti-expert
description: "Cyber threat intelligence and OSINT analysis toolkit. Runs structured investigations and delivers analyst-grade intelligence products with sourced, trust-scored findings. Use for OSINT and CTI cases, digital-footprint and exposure review, domain/subdomain/DNS/certificate recon, web-infrastructure pivoting (favicon hashes, tracker IDs, TLS certs, phishing-kit fingerprinting, campaign clustering), username/email/phone enumeration, breach and infostealer-log triage, image forensics, geolocation, crypto-wallet and IBAN/bank-account tracing, darknet search, M365/Azure and SaaS tenant recon, China/Sinophone recon (ICP filings, PRC corporate registries, Baidu/FOFA/Quake/ZoomEye), vulnerability and ransomware lookup, threat modeling, PII redaction, and structured reporting. Commands include /case, /sweep, /query, /webpivot, /username, /phone, /email-deep, /breach-deep, /icp, /cn-corp, /iban, /stealer-log, /exposure, /threat-model, /report, /brief, /redact, /apikeys."
version: "2.8"
author: "Hieu Ngo - chongluadao.vn"
---

# CTI Expert

Cyber threat intelligence and open-source intelligence skill. Turns Claude into a trained CTI/OSINT analyst. Generates precision search queries, interprets public data, builds case timelines, and delivers structured intelligence products — no API keys, no paid subscriptions.

> **Runs anywhere.** Works in **Claude Code** (Desktop & CLI) and in **OpenAI Codex / ChatGPT** and other `AGENTS.md`-aware agents — see [`AGENTS.md`](AGENTS.md) for the cross-agent runtime contract. Throughout this file, **`$SKILL_DIR`** = the directory containing this `SKILL.md` (Claude Code: `~/.claude/skills/cti-expert`; Codex/manual clone: the repo you are working in). Resolve it by locating `SKILL.md` — never hard-assume `~/.claude`. Detect the OS once (Windows/macOS/Linux) and prefer **uv** for all Python — see §13 Tool Auto-Install Policy.

Collection method: `agent-browser` when available (JavaScript-heavy sites, infinite-scroll, screenshot evidence), with automatic fallback to web search / web fetch / direct URL fetch. Tool limitations are logged as collection gaps — never as case blockers.

---

## 1. Quick Start

```bash
# Full autonomous case — runs every applicable technique
/case target.com

# Guided flow for first-time investigators
/flow person

# Summary of what's been found so far
/brief
```

Append `--yolo` to any command to skip all interactive prompts and confirmations. The analyst makes every decision autonomously.

---

## 2. AEAD Case Lifecycle

Every investigation follows four phases:

| Phase | What Happens |
|-------|-------------|
| **Acquire** | Collect raw data — `/sweep`, `/query`, `/username`, `/phone`, `/email-deep`, `/subdomain`, `/webpivot` + `/icp` (domain/URL targets), `/cn-corp` · `/iban` · `/hash-id` on discovery |
| **Enrich** | **Recursive pivot loop** — the [pivot orchestration engine](engine/pivot-orchestration.md) treats every discovered identifier as a new seed and expands the graph hop-by-hop (`/branch`, `/crossref`, `/link-subjects`, `/signatures`) **automatically until the frontier is exhausted**, no approval prompts (`autonomy=auto`). Acquire↔Enrich iterate, not run once. |
| **Assess** | Score and verify — `/exposure`, `/threat-model`, `/validate`, `/coverage`, `/verify-finding`. Judgments carry **likelihood terms**, coverage gets the **5W1H pass**, attributions get an **ACH matrix** ([`handbook/analytic-standards.md`](handbook/analytic-standards.md)) |
| **Deliver** | Package output — `/report`, `/brief`, `/render`, `/workspace save` — **auto-saves .md + .html + .json + .csv + IOC bundle** |

Run `/progress` at any point to see which phase you're in and what's pending.

> **`/case` and web-infra pivoting.** For a **domain or URL** target, `/case` includes
> web-infrastructure pivoting (`/webpivot`) in the Acquire phase. It runs **keyless by default**
> (crt.sh + passive DNS + anonymous urlscan) and **upgrades automatically when premium keys are
> set** via `/apikeys` (Shodan/Censys/FOFA/DNSLytics/SecurityTrails/urlscan-PRO/WhoisXML). Because
> `/webpivot` can fetch the target directly, for hostile infrastructure it prefers passive capture
> (urlscan/Wayback) — see [`techniques/web-pivot.md`](techniques/web-pivot.md). It is **not** run for
> username/phone/person targets.
>
> **Archive IOC harvest runs by default too.** For domain/URL targets the Acquire phase also runs
> `wayback_harvest.py <domain> --indicators` (add `--urlscan` when `URLSCAN_API_KEY` is set),
> harvesting **emails, phones, crypto wallets, tracking/verification IDs, SaaS-operator IDs, and
> socials from the *entire* Wayback history** — not just the live page — with first-seen/last-seen
> per selector. It writes case-schema `indicators[]` to `<case>/raw/harvest.indicators.json`, which
> merge into the case and flow into the **auto-saved IOC bundle** at Deliver. This is the step that
> recovers selectors a network later scrubbed — across the whole snapshot corpus, not just the live page.
> Passive by construction — only web.archive.org (+ urlscan.io if keyed), never the target.
>
> **The five v2.6 commands are in the pipeline too — no flags.** `/icp` runs for every
> domain/URL/org target (and an IP's resolved hostname); `/cn-corp`, `/iban` and `/hash-id`
> fire the moment a company name/USCC, payment detail, or hash appears — and all three feed
> their yields **back into the recursive pivot loop** as new seeds, so an ICP licence serial or
> a reused bank account expands the graph like any other node. `/redact` is the exception: it
> is **opt-in** (`--redact`), because a redacted report is a weaker artifact and that should
> always be a deliberate choice. Full trigger table: §Technique Activation Matrix.
> Narrow with `--no-cn`.

> **Two layers, one skill: broad collector → deep pipeline.** cti-expert is the **broad
> collector** — the wide net of Acquire/Enrich commands (`/webpivot`, `/sweep`, `/subdomain`,
> `/icp`, `/username`, `/email-deep`, `/breach-deep`, …) that pull artifacts from anywhere. The
> **`intel_engine` engine is now vendored in-repo under `intel_engine/`** (`intel_engine/harness/`,
> `intel_engine/tools/`, `intel_engine/WebPivot/`, `intel_engine/IntelGraph|IntelReport|BinaryPivot|IntelAnalysis/`)
> and supplies the **pipeline chains + deeper pivoting logic**: a persistent knowledge base (`intel_engine/knowledge/`), versioned cases
> (`cases/`), cross-case correlation, calibrated assessment, and rendering.
>
> **The chain:** broad collection (cti-expert) → the pipeline (`/pipeline`, `/harness`) ingests it,
> then applies the deep logic — *"seen this operator before?"* (`/recall`), whole-KB clustering
> (`/kb --cluster`, `/cert-overlap`), false-positive control (`/reference`), risk scoring
> (`/risk`), hypothesis generation, confidence calibration, and a versioned `Assessment`. The
> pipeline drives cti-expert's own `scripts/webpivot/pivot_extract.py` collector, so the broad and
> deep layers share one artifact shape end-to-end.
>
> **Self-contained & self-resolving.** `/backend` resolves to **SELF** (in-repo) — no external
> setup. Deps: `uv venv && uv pip install -r requirements.txt` (harness SDK/MCP + IntelGraph
> renderers; the collector + KB + deterministic pipeline are stdlib and need none). An explicit
> `$INTEL_HOME` still overrides for a shared external KB. Full architecture, the op map, and the
> evidence-envelope schema: [`connectors/intel-backend.md`](connectors/intel-backend.md).

---

## 2.5. Pivot Priority & False-Positive Control (CRITICAL)

Two failure modes ruin a cluster: asserting a link that isn't there, and missing one that is.
This section governs both. Apply it in Enrich, before anything reaches a report.

### Pivot priority ladder

Work **down** this ladder. Never assert same-operator on a lower rung when a higher rung is
available or contradicts it. Tag every asserted link in the report with the rung it rests on.

| Rung | Indicator | Strength |
|---|---|---|
| 1 | Registrant email / phone / org — **including historic WHOIS** | decisive |
| 2 | One domain carrying **two identities across its own WHOIS history** | decisive — proves an alias |
| 3 | Site-verification token (Google Search Console, etc.) | decisive — proves account control |
| 4 | Shared TLS certificate / SAN cross-cover | strong |
| 5 | Nameserver delegation to a host the operator **runs themselves** | strong — proves zone control |
| 6 | APK signing certificate | strong |
| 7 | Distinctive favicon / analytics / tracker / backend tenant ID | moderate — verify below |
| 8 | Co-tenancy on a **dedicated** host (few tenants) | moderate |
| 9 | Site template / framework / kit | **weak — kit-level, never operator-level** |
| 10 | Co-tenancy on **shared/reseller** hosting; managed-provider nameservers | information, not a link |

**Reverse-WHOIS is the highest-yield pivot here.** Always `mode=preview` first — the count is
free. A term returning hundreds is shared boilerplate; do not purchase it.

### Mandatory false-positive control

Before any indicator becomes a cluster edge, run `/reference check <value>`. If it returns
UNKNOWN, **decide and record it** with `/reference add` so the next case inherits the judgement.

Six traps, all of which have produced real false clusters:

| Trap | Why it fools you | Test |
|---|---|---|
| **Commodity site kit** | A template sold to hundreds of unrelated fraud operators | Search the template path in urlscan/FOFA — a large population means kit-level |
| **Privacy-proxy contacts** | The registrar's boilerplate phone/email, shared by every customer of that service | Reverse-WHOIS it; a spread of unrelated domains means noise |
| **Shared/reseller hosting IP** | A 20+-tenant cPanel box links nothing | Count tenants before clustering |
| **Managed-provider nameservers** | Cloudflare/GoDaddy/Gandi/Wix NS are shared by millions | Self-hosted NS is rung 5; provider NS is rung 10 |
| **Org-name collision** | A registrant org string that also matches a real, unrelated company | Reverse-WHOIS the org; inspect what comes back before attributing |
| **Shared analytics / tag container** | Often one web developer reusing a container across unrelated clients | **Check domain creation dates** — a decade-old business sharing a tag with a new fraud domain is a third party |

> **Never put an unvalidated indicator into a report that recommends abuse reporting.** Naming an
> uninvolved business is the most damaging error this skill can produce. When a cluster rests on a
> single rung-7-or-below indicator, label it *candidate, single-indicator* — not a cluster member.

### Never submit the case's own sample to a public sandbox (CRITICAL)

`/anyrun` is **lookup-only**. It reads detonations that already happened; it has no submit path,
and the submission endpoint is deliberately absent from `BinaryPivot/references/anyrun.json`.
`tests/test_no_sample_submission.py` enforces that as a gate, so it cannot regress quietly.

**Do not work around it.** Uploading the case's own APK / installer / archive to ANY.RUN —
or VirusTotal, or any public sandbox — is an **outbound, irreversible** act:

- A public task is **world-readable**: the file, its hash, screenshots and full network log.
- **Operators watch for their own samples.** The standard response is to rotate the backend,
  revoke the signing key and re-skin the front — destroying the infrastructure the case is built
  on, often days before a takedown or referral can land.
- **It cannot be recalled.** Unlike a query from the wrong egress, there is no cleanup.

If detonation is genuinely necessary, **stop and put it to the analyst in plain terms** — what
becomes public, and that it is permanent — and let them do it themselves in the sandbox UI on a
**private** plan. Never as a side effect of a pivot, and never on standing permission inferred
from an earlier approval. The same reasoning governs `--submit` (urlscan/Wayback): a public
urlscan scan of a live scam funnel is visible to the operator too.

### A permuted email is a hypothesis, never a finding (CRITICAL)

When a case yields a **real person's name** or a **username**, and you already hold a domain that
matters to the case, run **`/email-permute`**. An operator's mailbox is almost never published, but
it is usually *derivable* — mail hosts use a small set of local-part conventions, and the operator's
own domain is the highest-yield thing to permute against.

That value comes with a matching hazard, so this rule is absolute:

- **Permute against the case's own domains.** Name × the operator's domain is a narrow, high-prior
  question. Name × `gmail.com` is volume with no prior behind it — `--free` exists, is capped, and
  should be a deliberate choice, not a reflex.
- **Never ingest a candidate into the KB, cite one in a report, or contact one.** A fabricated
  address that reaches `kb_ingest` becomes a shared indicator, and a shared indicator merges two
  operator clusters. A permutator wired straight into correlation does not enrich a case — it
  silently names an innocent party. This is the same failure RULE 5 exists to prevent.
- **Candidates are not seeds.** They never enter the spider-map frontier. Only an address in the
  tool's `promote` list — corroborated by *independent* evidence (Gravatar registration, breach
  corpus, a GitHub commit, a page/DOM hit, a dork) — may be treated as a real email seed, and that
  promotion is an analyst decision.
- **Never validate over SMTP.** `RCPT TO` probing connects to the *target's* mail server, which the
  egress posture exists to prevent on a hostile case; and a catch-all domain answers `250` for
  every address ever tried, so it manufactures confidence instead of measuring it. Use `--verify`,
  which gates on MX (RFC 7505 null MX included) and checks Gravatar — both keyless, neither
  touching the target.

State the status in the turn. *"12 candidates, 0 corroborated"* is an honest result; presenting
those 12 as discovered addresses is not.

### Dead seed? Do not stop

Zero pivots, a parked page, or NXDOMAIN is not an answer. Run **`/fallback <domain>`** — crt.sh,
the full Wayback timeline, archive.today, and the local KB. A parked apex frequently has live
subdomains: enumerate CT and the Wayback CDX host histogram before writing a seed off. Report an
empty result as empty; a collector that returned nothing is a finding, not something to omit.

---

## 3. Command Reference

> **How to read this table — check the marker before you announce a command.**
>
> | Marker | Meaning | What you may say |
> |---|---|---|
> | **T2:** / **T1:** shown | Backed by a real CLI op and/or MCP tool. | Call it, then report what it returned. |
> | **[model]** | No code behind it, and none is needed — it names a way for *you* to work (a summary style, a checklist, a KB read-back). | Do the thing. Never claim a tool ran. |
> | **[unimplemented]** | The tradecraft is documented but nothing executes it yet. | Say so, then follow the linked technique by hand. Do NOT narrate it as a tool call. |
>
> A command with no marker and no **T2:**/**T1:** line has not been triaged yet — treat it as
> **[unimplemented]**. Announcing a tool call that cannot happen is the failure this table exists
> to prevent: the output looks identical to real collection and is not.

### 3.0 Entry point & registered commands

**`/cti <target>` is the single entry to this skill.** It routes any target type — domain, IP,
email, username, phone, wallet, hash, APK — through recall → collect → cluster → assess. Plain
English works identically ("analyze example.com and pivot the infrastructure"); the command form
just removes ambiguity.

Eight commands are **registered with Claude Code** by `bash scripts/register.sh` and work from a
cold prompt in any project:

| Command | Does | Equivalent T2 op | Equivalent T1 tool |
|---|---|---|---|
| **`/cti <target>`** | **entry point — routes by target type** | *(whole chain)* | *(whole chain)* |
| `/cti-recall <seed>` | seen before? **run first, always** | `recall` | `domain_verdict`, `which_cases` |
| `/cti-case <ID> <seeds>` | full deterministic pipeline | `pipeline open` | *(none — CLI only)* |
| `/cti-pivot <url\|ip>` | collect one target | `pivot-extract` | `pivot_extract` |
| `/cti-cluster <domain>` | correlate & expand | `kb`, `cert-overlap` | `kb_cluster`, `cert_overlap` |
| `/cti-check <indicator>` | false-positive control | `reference check` | `reference_check`, `reference_add` |
| `/cti-report <ID>` | render graph + PDF/DOCX | `graph`, `report` | `render_diagram`, `render_report` |
| `/cti-status` | backend / MCP / credits health | `backend.py status` | `api_usage` |

> **Every other `/command` in §3 is a convention read from this file, not a registered command.**
> Once the skill is loaded they are unambiguous instructions; typed at a cold prompt they do
> nothing. When in doubt use `/cti` and describe the goal.

**Three layers, one operation.** The same capability is reachable three ways and the names differ
by layer — T0 uses `kebab-case` after a slash, T2 uses `kebab-case` ops, T1 uses `snake_case`
tools. The table above is the canonical mapping; when you add a capability, add a row here in the
same commit or the layers drift apart again.

Capabilities that are *not* registered commands still carry their layer mapping inline in the §3
tables. The engine's WebPivot/BinaryPivot collectors add these: `/capabilities` (T2 `capabilities`,
T1 `capability_check`), `/impersonate` (T2 `impersonate`, T1 `impersonation_hunt`), `/search-pivot`
(T2 `search-pivot`, T1 `search_pivot`), `/censys` (T2 `censys`, T1 `censys`), `/intelx`
(T2 `intelx`, T1 `intelx_search`) and `/anyrun` (T2 `anyrun`, T1 `anyrun_lookup`).

---

Commands grouped by AEAD phase.

### Acquire

| Command | What It Does | Example |
|---------|-------------|---------|
| `/case [target]` | Full pipeline — runs every applicable technique **T2:** `intel.py case <seed>` (= `pipeline`) | `/case example.com` |
| `/sweep [target]` | Multi-vector recon on any target type **T2:** `intel.py sweep <target>` (= `pipeline`) | `/sweep @username` |
| `/query [subject]` | Builds 12–15 advanced search operator queries **T2:** `intel.py query <indicator>` | `/query example.com` |
| `/username [handle]` | Enumerate handle across 3000+ platforms **T2:** `intel.py username <handle>`. **T1:** `username_enum` — HYPOTHESES, not findings | `/username johndoe` |
| `/phone [number]` | Carrier, line type, reputation, public associations **T2:** `intel.py phone +<E164>`. **T1:** `phone_osint` — carrier/line-type NOT determined | `/phone +84901234567` |
| `/email-deep [email]` | Accounts, breach history, infrastructure **T2:** `intel.py email-deep <email>`. **T1:** `deep_profile` — metered steps planned, not fired | `/email-deep u@domain.com` |
| `/subdomain [domain]` | CT logs, brute-force, passive enumeration; flags admin/sensitive subdomains (`admin`,`adm`,`kef`,`ador`,`panel`…) per `handbook/admin-endpoint-indicators.md` **T2:** `intel.py subdomain <domain>`. **T1:** `subdomain_enum` — multi-source; names any source that was down | `/subdomain example.com` |
| `/breach-deep [email]` | Multi-source breach lookup with context **T2:** `intel.py breach-deep <email>`. **T1:** `deep_profile` (mode=breach) | `/breach-deep u@domain.com` |
| `/traffic [domain]` | Traffic estimation, ranking, audience data **T2:** `intel.py traffic <domain>`. **T1:** `traffic_rank` — Tranco only; no paid-panel estimates | `/traffic example.com` |
| `/visitors [domain]` | Full visitor intelligence: tech, geo, sources, analytics **T2:** `intel.py visitors <url>`. **T1:** `pivot_extract` (trackers) | `/visitors example.com` |
| `/techstack [domain]` | Technology fingerprint (CMS, analytics, CDN, server) **T2:** `intel.py techstack <url>`. **T1:** `pivot_extract` (tech_fingerprint) | `/techstack example.com` |
| `/competitors [domain]` | Competitor & related site discovery **[unimplemented]** | `/competitors example.com` |
| `/secrets [target]` | Exposed credentials in repos and paste sites **T2:** `intel.py secrets <target>`. **T1:** `github_osint` (secrets=true) — code search needs auth, so queries are EMITTED | `/secrets github.com/org` |
| `/github-osint [target]` | GitHub user/org/repo recon: profiles, repos, code search, commits, forks **T2:** `intel.py github-osint <target>`. **T1:** `github_osint` | `/github-osint github.com/org/repo` |
| `/threat-check [target]` | IP/domain/URL/hash threat intelligence **T2:** `intel.py threat-check <indicator>`. **T1:** `threat_check` | `/threat-check 185.1.1.1` |
| `/scam-check [domain]` | Phishing/scam/malicious domain check **T2:** `intel.py scam-check <domain>`. **T1:** `threat_check` (mode=scam) | `/scam-check susp-site.xyz` |
| `/webpivot [url]` | Web-infra pivoting — extract favicon mmh3 / GA-GTM-AdSense / wallet / SaaS-operator artifacts from a page's DOM → ranked pivot queries (Shodan/PublicWWW/urlscan/FOFA). Flags: `--render`, `--crawl`, `--history` (Wayback GA), `--fetch` (pull archived page content — WebFetch can't reach Wayback), `--harvest` (full-IOC harvest across whole archive history → emails/phones/wallets/IDs/socials), `--whois`, `--graph` (cluster), `--rank` (score same-operator relations), `--cert` (cert-fingerprint pivot), `--suggest`, `--wallets`, `--paths`. See `techniques/web-pivot.md` (reverse-lookup engines per artifact → `handbook/pivot-services.md`) **T2:** `intel.py webpivot <url>`. **T1:** `pivot_extract` | `/webpivot https://scam-site.top` |
| *(automatic — no flag)* | Four layers now run on **every** collection and need no command. **Asset layer:** fetches the page's own JS bundles and re-runs every extractor over the source — the fix for SPA/white-label kits where the shell HTML is empty; yields off-apex `api_endpoint`/`websocket_endpoint` (the backend survives a front-end re-skin), `build_env:<KEY>` tenant tokens, `js_bundle_sha256`, and via `sourceMappingURL` the operator's own `dev_username`/`dev_project`. **SPA route table:** reads the app's router literals — `spa_route:admin`, `spa_route:funnel`, and a `spa_route_signature` that survives a re-skin. Zero extra requests, routes are leads only and are never fetched. **Well-known/policy files:** a fixed standards list (never a wordlist, no path brute-forcing) → `adstxt_publisher`, `apple_team_id`, `security_contact`. **JARM:** TLS-stack fingerprint of the server. Suppress with `--no-assets` / `--no-well-known`; cap fetches with `--assets-max N` | *(runs inside `/cti-pivot`)* |
| `/capabilities` | **Run this first, and again before reporting any "nothing found".** Which optional API keys are configured, and for each absent one the *evidence class that went unqueried* plus the free path that substitutes. A keyless run extracts every artifact but cannot **reverse** most of them — so "no sibling domains" with no FOFA/urlscan key is a fact about the credentials, not about the operator. Every collection also records this in `meta.capability`; carry the limitation statement into the assessment and cap confidence accordingly. T2: `capabilities` · T1: `capability_check` | `/capabilities` |
| `/impersonate [domain]` | Hunt **lookalike / typosquat** domains of a seed — typosquat permutations (omission, insertion, adjacent-key, transposition, homoglyph, hyphenation, combosquat) + a curated scam-heavy TLD sweep + a crt.sh keyword hunt, then existence-checked by live DNS. Output separates **confirmed registered lookalikes** (each an `impersonation:candidate` — run `/cti-pivot` on it and compare) from an unregistered **monitoring watchlist**. FREE (crt.sh + DNS); `--fofa` / `--urlscan` add the metered sweeps. Never live-fetches the lookalike infra. Tune the TLDs/affixes per campaign in `intel_engine/WebPivot/references/impersonation.json`. T2: `impersonate` · T1: `impersonation_hunt` | `/impersonate example.com` |
| `/search-pivot [indicator]` | Multi-engine **search-engine** pivot — the general-web complement to FOFA/PublicWWW, which only see served HTML. Takes any indicator (domain, slogan, tracking ID, wallet, Telegram/Zalo handle) and emits ready-to-open, URL-encoded dork queries across Google/Yandex/DuckDuckGo/Bing/Brave. It does **not** scrape: fire the queries with WebSearch, or WebFetch the DuckDuckGo html URL, then feed new hosts back into `/cti-pivot`. FREE, no keys. T2: `search-pivot` · T1: `search_pivot` | `/search-pivot "distinctive slogan"` |
| `/censys [mode] [value]` | Censys Platform — the **server-side** view FOFA/urlscan don't give. `cert <sha256>` returns every hostname on that exact leaf certificate (near-decisive cross-brand same-operator evidence, and it works on a **free** plan); `host <ip>`, `webproperty <host>` also free-plan. `query <kind> <value>` builds the CenQL **offline and keyless**; `budget` reports the balance. ⚠️ **100 credits/MONTH per account, no rollover** — a lookup is 1, a search 5, and running the emitted CenQL in the web UI costs the same 5. Prefer handing the analyst the query over spending a search. Needs `CENSYS_PAT`. T2: `censys` · T1: `censys` | `/censys cert 1a2b3c…` |
| `/intelx [selector]` | **Intelligence X** — search ONE strong selector across a corpus nothing else here indexes: breach dumps, infostealer logs, pastes, darknet mirrors, historical WHOIS. Takes an email / domain (`*.apex` wildcard ok) / URL / IP / phone / wallet / IBAN — **never a brand or person name** (soft terms are refused *and still cost a unit*; `classify_selector()` blocks them locally). `--phonebook <domain>` inventories every email, subdomain and URL under an apex — the highest-value call, PAID-only. **Grading is not optional:** a hit in a breach dump or stealer log is **EXPOSURE**, flagged NOT clusterable — two addresses in one combolist share *victims*, not an operator. Only `whois` / `pastes` / darknet hits may carry a same-operator edge. Keyless ≈ 50%: it still types the selector and hands you the intelx.io URL. T2: `intelx` · T1: `intelx_search` | `/intelx registrant@example.com` |
| `/anyrun [indicator]` | **ANY.RUN TI Lookup — READ-ONLY.** What samples carrying this indicator *did* when **other people** detonated them: contacted domains/IPs/URLs/ports, family label, Suricata context, public task links. Run it after `/binary` on the sample's sha256, backend host or `ip:port`. It is the **only** way to recover a **packed** sample's real endpoints — those exist only at runtime, so a thin string sweep plus a `binary:protection` finding is exactly the cue. A shared *family* is same-KIT, never attribution on its own. Keyless ≈ 50%: composes the query + UI link. **⚠️ This tool never submits a sample — see the box below.** T2: `anyrun` · T1: `anyrun_lookup` | `/anyrun <sha256>` |
| `/cert-pivot [domain]` | Cert-fingerprint pivot — other hosts serving the same TLS cert + SAN siblings (keyless; Shodan/Censys with keys). **T2:** `intel.py cert-pivot <domain>`. **T1:** `cert_pivot` | `/cert-pivot scam-site.top` |
| `/sensitive-paths [list]` | Classify a Wayback/URL list for exposed paths (.git/.env/backups/configs) — severity + per-year timeline. Pure matching, **no request reaches the target**. **T2:** `intel.py sensitive-paths --file <list>`. **T1:** `sensitive_paths` | `/sensitive-paths waymore_index.txt` |
| `/email-hygiene [email]` | Grade an email domain 0–100 + A–F (disposable / MX / free / role). An RFC 7505 **null MX** (`0 .`) scores as undeliverable, not valid. **T2:** `intel.py email-hygiene <email>`. **T1:** `email_hygiene` | `/email-hygiene admin@site.top` |
| `/vuln-check [query]` | CVE/vulnerability lookup (CIRCL + NVD) **T2:** `intel.py vuln-check CVE-… | --product <p>`. **T1:** `vuln_check` | `/vuln-check CVE-2024-1234` or `/vuln-check apache/httpd` |
| `/ransomware-check [org]` | Check if org is a ransomware victim **T2:** `intel.py ransomware-check <domain>`. **T1:** `threat_check` (mode=scam) | `/ransomware-check "Acme Corp"` |
| `/stealer-log [folder]` | Triage an infostealer-log folder — stealer-family attribution, victim-vs-operator profiling, cross-log actor correlation, IOC extraction (raw passwords/cookies/autofill/history shown) | `/stealer-log ./logs` |
| `/gdoc [url]` | Extract metadata/owner from Google document **T2:** `intel.py gdoc <url>`. **T1:** `doc_metadata` | `/gdoc https://docs.google.com/...` |
| `/msftrecon [domain]` | M365/Azure tenant recon — tenant ID, federation, MDI, SharePoint **T2:** `intel.py msftrecon <domain>`. **T1:** `msft_recon` | `/msftrecon example.com` |
| `/icp [domain\|serial]` | ICP filing (工信部备案) → registered PRC entity + licence number; reverse the **licence serial** to sibling domains under the same filing (same-operator, HIGH). See `techniques/china-recon.md` **T2:** `intel.py icp <domain>`. **T1:** `cn_recon` — MIIT is CAPTCHA-walled; gates are named | `/icp scam-site.top` |
| `/cn-corp [name\|USCC]` | PRC corporate registry chain — GSXT (ground truth) → TianYanCha/QCC/Aiqicha → 信用中国 blacklist → UBO; officers, shareholders, subsidiaries, revoked-status flags **T2:** `intel.py cn-corp --company "<name>"`. **T1:** `cn_recon` — GSXT/TianYanCha gated | `/cn-corp 深圳市某某科技有限公司` |
| `/iban [value]` | Validate + decompose a bank account as a selector — mod-97 checksum, country, BBAN split, bank code, jurisdiction-mismatch signals. See `techniques/fiat-payment-osint.md` **T2:** `intel.py iban <IBAN>` | `/iban GB29NWBK60161331926819` |
| `/hash-id [hash]` | Identify a hash's algorithm **before** lookup — separates file hashes from credential material (32 hex = MD5 *or* NTLM) so it routes to the right service **T2:** `intel.py hash-id <hash> [--context file|credential]`. **T1:** `hash_id` **T2:** `intel.py hash-id <hash> [--context file|credential]`. **T1:** `hash_id` | `/hash-id 5f4dcc3b5aa765d61d8327deb882cf99` |
| `/appliance-scan [domain\|ip]` | Fingerprint internet-facing edge/VPN appliances (Citrix/F5/Cisco/Ivanti/Forti/PAN/Exchange) + exposed services → CISA KEV/CVE mapping. Passive-first (Shodan InternetDB/Censys); feeds `/vuln-check` + `/threat-model`. See `techniques/fx-edge-appliance-recon.md` **[unimplemented]** | `/appliance-scan vpn.example.com` |
| `/saas-map [domain]` | Map SaaS tenancy + identity fabric — DNS-TXT tenancy tokens, non-Microsoft IdP fingerprint (Okta/Auth0/OneLogin/Ping/Keycloak/ADFS), unauth API/GraphQL/spec discovery. See `techniques/fx-saas-identity-recon.md` **T2:** `intel.py saas-map <url>`. **T1:** `pivot_extract` (saas_ids) | `/saas-map example.com` |
| `/sharelink [url]` | Extract sharer identity from share link **T2:** `intel.py sharelink <url>`. **T1:** `sharelink_resolve` — contacts the final host | `/sharelink https://vm.tiktok.com/ABC` |
| `/binary [file\|url]` | **Built-in.** Static IOC extraction from a scam/fraud binary (sideloaded APK, desktop trading `.exe`/`.dmg`, bundled `.jar`) via the in-repo `BinaryPivot/` — signing-cert SHA-256, package name/permissions, embedded C2/backend hosts, Firebase/S3 tenants, wallets, Telegram/WhatsApp handles. Output is WebPivot-shaped → clusters the app with web infra in the shared KB. See `connectors/intel-backend.md` §7 | `/binary ./trader.apk` |
<!-- dork-integration:phase-05 start -->
| `/dork-sweep [target] [--telegram\|--docs\|--filetype\|--all] [--after DATE] [--clean]` | Zero-auth dork sweep: Telegram ecosystem, 18 doc-hosts, filetype families; 4-tier fallback cascade **T2:** `intel.py dork-sweep <target>` | `/dork-sweep example.com --filetype` |
| `/docleak [target] [--platform list] [--severity high]` | 18-platform document leak hunt with severity classification (CRITICAL/HIGH/MEDIUM/LOW) **T2:** `intel.py docleak "<target>"`. **T1:** `dork_builder` — emits queries, never runs them | `/docleak "Acme Corp"` |
<!-- dork-integration:phase-05 end -->
| `/dns-history [domain]` | Historical DNS record changes (A, NS, MX) via passive DNS **T2:** `intel.py dns-history <domain>`. **T1:** `wayback_ga` | `/dns-history example.com` |
| `/cert-history [domain]` | SSL/TLS certificate timeline from CT logs (crt.sh) **T2:** `intel.py cert-history <domain>`. **T1:** `passive_ssl` | `/cert-history example.com` |
| `/email-permute [name] [domain]` | Generate email permutations from name + domain | `/email-permute "John Smith" company.com` |
| `/proton-check [email]` | Proton Mail account creation date via PGP key **[unimplemented]** | `/proton-check user@proton.me` |
| `/pgp-lookup [email]` | PGP key search — creation date, UIDs, signatures **[unimplemented]** | `/pgp-lookup dev@example.com` |
| `/wifi [ssid]` | WiFi SSID geolocation via Wigle.net **T2:** `intel.py wifi "<ssid>"`. **T1:** `wifi_ssid` — needs a WiGLE account; discloses the gap | `/wifi "HomeNetwork"` |
| `/wifi --bssid [mac]` | Exact AP lookup by MAC address | `/wifi --bssid AA:BB:CC:DD:EE:FF` |
| `/register [name]` | Add a subject to the case workspace | `/register JohnDoe` |
| `/snapshots [url]` | List/fetch archived Wayback snapshots. WebFetch is blocked from web.archive.org (robots.txt) — this reads the archive instead, so **the request never reaches the target**. **T2:** `intel.py wayback-fetch <url> [--near latest\|earliest\|YYYY] [--list]`. **T1:** `wayback_fetch`. See `analysis/archive-explorer.md` | `/snapshots example.com` |
| `/archive-harvest [domain]` | Sweep a domain's **whole** Wayback history for indicators an operator has since scrubbed — the GA ID that clusters the estate is often only in an old capture. **T2:** `intel.py wayback-harvest <domain> --indicators [--from YYYY --to YYYY]`. **T1:** `wayback_harvest` | `/archive-harvest site-a.example` |

### Enrich

| Command | What It Does | Example |
|---------|-------------|---------|
| `/branch [data]` | Expand a discovered identifier laterally **[model]** | `/branch john@mail.com` |
| `/pivot-suggest` | Rank "what to pivot on next" from findings — leet/variant/reuse/temporal/domain clusters. **T2:** `intel.py pivot-suggest <findings.json>`. **T1:** `pivot_suggest` | `/pivot-suggest` |
| `/email-permute [name\|handle]` | Derive email **candidates** from a person name or username against case domains. VN/CN/KR family-name-first aware; folds diacritics Unicode won't. `--verify` = MX gate + Gravatar. **Output is hypotheses — see the rule below** | `/email-permute "Nguyen Van A" --domain example.com --verify` |
| `/rank-relations` | Score + rank same-operator relations across analyzed pages (noise-filtered). Mechanizes **one artifact = lead, two = cluster** — run it before asserting a cluster. **T2:** `intel.py rank-relations cases/<CASE>/raw/*.json`. **T1:** `rank_relations` | `/rank-relations` |
| `/crypto-balance [addr]` | On-chain balance + lifetime flow for a wallet, valued at spot. **T2:** `intel.py crypto-balance <addr>`. **T1:** `crypto_balance` | `/crypto-balance 1ExampleBitcoinAddressDoNotUse` |
| `/timeline [subject]` | Assemble dated event sequence | `/timeline Company Inc` |
| `/crossref` | Detect shared identifiers across subjects **T2:** `intel.py crossref [--case <id>]`. **T1:** `kb_crossref` | `/crossref` |
| `/link-subjects [A] [B]` | Define a connection between two subjects **[model]** | `/link-subjects John Jane` |
| `/show-connections` | Display all logged connections **[model]** | `/show-connections` |
| `/show-trail [subject]` | Show the evidence chain for a subject **[model]** | `/show-trail JohnDoe` |
| `/watch [subject]` | Add subject to active tracking list **[model]** | `/watch example.com` |
| `/record-finding` | Log a finding with source and confidence **[model]** | Paste data after command |
| `/show-findings` | List all recorded findings **[model]** | `/show-findings` |
| `/graph` | Full ASCII subject relationship map | `/graph` |
| `/pathfind [A] [B]` | Discover connection path between subjects **[model]** | `/pathfind A B` |
| `/diff [url]` | Diff archived versions of a URL **[model]** | `/diff example.com/page` |
### Assess

| Command | What It Does | Example |
|---------|-------------|---------|
| `/exposure [target]` | Composite exposure score (0–100) **T2:** `intel.py exposure --set k=v`. **T1:** `exposure_score` | `/exposure domain.com` |
| `/threat-model` | Build threat model from findings; every attribution claim carries an **ACH matrix** (competing hypotheses scored by inconsistency, runner-up named) per `handbook/analytic-standards.md` §3. **Backend hook (Assess):** if `/backend` is up, calibrate confidence on your own priors first — `intel.py operators list` + `intel.py risk --case <id>` + read `knowledge/{calibration.jsonl,analyst_profile.md}` — instead of scoring from scratch. See `connectors/intel-backend.md` §6 **[model]** | `/threat-model` |
| `/signatures` | Surface recurring behavioral patterns **T2:** `intel.py signatures --set k=v`. **T1:** `signature_scan` — evaluates, does not observe | `/signatures` |
| `/validate` | Quality audit — score 0–100 **[model]** | `/validate` |
| `/coverage` | Coverage matrix with identified gaps — technique matrix **plus** the 5W1H substantive pass (`Why`/`How` unanswered blocks Deliver-ready) **[model]** | `/coverage` |
| `/verify-finding [id]` | Re-check a specific finding's sources **[model]** | `/verify-finding 12` |
| `/subject [name]` | View or create subject record **[model]** | `/subject JohnDoe` |
| `/lookup [name]` | Retrieve a registered subject **[model]** | `/lookup JohnDoe` |
| `/modify [name]` | Update a subject record **[model]** | `/modify JohnDoe` |
| `/archive-subject [name]` | Remove subject from active tracking **[model]** | `/archive-subject JohnDoe` |
| `/find [query]` | Search across all subjects **[model]** | `/find domain:example.com` |
| `/show-trail [subject]` | Full evidence trail | `/show-trail JohnDoe` |
| `/blind-spots` | Prioritized investigation gap analysis **[model]** | `/blind-spots` |
| `/source-check` | Batch source URL accessibility check **[model]** | `/source-check` |
| `/drift [subject]` | Temporal risk score tracking **T2:** `intel.py drift <case> [--snapshot]`. **T1:** `case_drift` | `/drift example.com` |
| `/clarify [finding]` | Plain-language finding explanation **[model]** | `/clarify fnd-003` |
### Deliver

| Command | What It Does | Example |
|---------|-------------|---------|
| `/report` | Full report — auto-saves .md + .html + .json + .csv + IOC bundle | `/report` |
| `/report html` | Interactive self-contained HTML report (primary deliverable) | `/report html` |
| `/report brief` | Single-page executive brief | `/report brief` |
| `/report json` | Raw data as JSON | `/report json` |
| `/report csv` | Spreadsheet-compatible export | `/report csv` |
| `/report docx` | Word document (rich charts/diagrams) — on request | `/report docx` |
| `/report legal` | Evidence-formatted for legal proceedings (adds DOCX/PDF) | `/report legal` |
| `/report journalist` | Source-citation-heavy format | `/report journalist` |
| `/brief` | Plain-language summary (non-technical) **[model]** | `/brief` |
| `/render entities` | ASCII subject relationship diagram **[model]** | `/render entities` |
| `/render timeline` | Chronological event chart | `/render timeline` |
| `/render risk` | Exposure heatmap | `/render risk` |
| `/render network` | Network topology of connections | `/render network` |
| `/stats` | Counts and coverage statistics **T2:** `intel.py stats` | `/stats` |
| `/workspace save [name]` | Persist case state **[model]** | `/workspace save mycase` |
| `/workspace open [name]` | Resume a saved case | `/workspace open mycase` |
| `/workspace list` | Show saved cases | `/workspace list` |
| `/workspace diff [a] [b]` | Diff two saved workspaces | `/workspace diff case1 case2` |
| `/render threat-path` | ASCII attack path flow diagram | `/render threat-path` |
| `/render attack-surface` | ASCII attack surface exposure map | `/render attack-surface` |
| `/report ioc` | Export IOCs as STIX 2.1 or flat list | `/report ioc --format stix` |
| `/redact [file]` | Shareable variant of a report — stable numbered placeholders (`[EMAIL_1]`) + reversible JSON map; `.md`/`.json`/`.csv`. **Opt-in** — the default export set stays unredacted; request with `/redact` or `--redact` | `/redact REPORT.md` |

### UX & Navigation

| Command | What It Does | Example |
|---------|-------------|---------|
| `/flow [type]` | Guided step-by-step case workflow **[model]** | `/flow person` |
| `/template list` | Browse pre-built case templates **[model]** | `/template list` |
| `/template run [name]` | Run a pre-built template | `/template run security-audit` |
| `/novice` | Toggle simplified, low-jargon mode **[model]** | `/novice` |
| `/terms` | OSINT term glossary **[model]** | `/terms` |
| `/progress` | Current case phase and coverage **[model]** | `/progress` |
| `/opsec` | OPSEC checklist for current task **[model]** | `/opsec` |
| `/onboard` | Interactive first-time onboarding guide **[model]** | `/onboard` |
| `/quality` | Investigation quality composite score **[model]** | `/quality` |
### Configure

| Command | What It Does | Example |
|---------|-------------|---------|
| `/apikeys` | Manage premium/pro API keys (Shodan, Censys, FOFA, SecurityTrails, DNSLytics, urlscan-PRO, WhoisXML, Hudson Rock, IntelX, GitHub, SerpAPI…) — `status`/`set`/`unset`/`test`/`unlocks`. Keys **upgrade existing techniques** (especially `/webpivot`); keyless/free stays the default. Stored chmod-600 in `$SKILL_DIR/.env` (gitignored), env-var override. See `handbook/api-keys.md` | `/apikeys set shodan <KEY>` |
| `/backend` | Detect/report the optional persistent-intelligence backend and pick the tier — **Tier 1** typed MCP (`intel-harness`) → **Tier 2** CLI → **Tier 3** stateless. Runs `scripts/backend/backend.py` to resolve `$INTEL_HOME` (env → `.mcp.json` → sibling dir → symlink) and print the tier line. All the backend commands below dispatch through `scripts/backend/intel.py <op>` at Tier 2 (or the typed MCP tool at Tier 1). `intel.py list` maps **all 73 engine ops** (full CLI parity — CDN ranges, graph-build, hypothesize, calibration, evidence-report, case-store, cost, deterministic `pipeline`, …); `intel.py mcp` prints/writes the `.mcp.json` that enables Tier 1 ("the server"). See `connectors/intel-backend.md` | `/backend` · `/backend check` |
| `/kb [query]` | **Built-in.** Query the shared knowledge base. **T2:** `intel.py kb --stats`/`--entity <v>`/`--cluster <domain>`/`--shared --min N`; `intel.py operators list`. **T1:** `kb_entity`/`kb_cluster`/`kb_query_shared` | `/kb --entity example.com` |
| `/recall [seed]` | **Built-in.** "Have I seen this before?" — check a seed against every prior case before collecting. **T1:** `which_cases`/`domain_verdict` (typed MCP). **T2:** `intel.py recall <seed>` (query.py `--entity`; which_cases/domain_verdict are MCP-only). Surfaces known operators up front | `/recall scam-site.top` |
| `/risk [case]` | **Built-in.** Score a case's hosts for **NRD / bulletproof-hosting / money-trail** red flags. **T2:** `intel.py risk --case <id>` (or `--file <pivot.json>`). **T1:** `risk_signals` | `/risk CASE-0001` |
| `/reverse-whois [email\|name]` | **Built-in.** Reverse-WHOIS a registrant identity → only high-value pivots; refuses privacy/registrar terms, flags bulk resellers as noise. **T2:** `intel.py reverse-whois --reverse-email <e> --search-type historic --json`. **T1:** `reverse_whois` | `/reverse-whois owner@x.com` |
| `/cert-overlap [d1 d2 …]` | **Built-in.** KB-aware TLS/SAN same-operator **verdict** (SHARED-CERT / SIBLING-OVERLAP / NO-CT-OVERLAP) across 2+ domains — corroborates a cluster at the TLS layer. Complements the keyless `/cert-pivot`. **T2:** `intel.py cert-overlap a.com b.com`. **T1:** `cert_overlap` | `/cert-overlap a.com b.com` |
| `/reference [check\|add\|list]` | **Built-in.** Curated **false-positive control** ledger — is a fingerprint BENIGN (common logo/CDN → don't cluster), SIGNAL (distinctive, prior-case → pivot), or UNKNOWN. **T2:** `intel.py reference check <value>`. **T1:** `reference_check`/`reference_add` | `/reference check favicon:123` |
| `/pipeline [open\|status] <case> <domains-file>` | **Built-in.** The **deterministic** chain (no LLM key) — the bread-and-butter handoff: broad collect (cti-expert's `pivot_extract`) → ingest → prior-overlap → risk → shared-cluster → ICD-203 assessment, persisted under `cases/<case>/`. Prints `collector: cti-expert`. **T2:** `intel.py pipeline open <case> seeds.txt [--no-graph]` | `/pipeline open case1 seeds.txt` |
| `/harness [open\|continue\|status]` | **Built-in.** The **LLM-driven** whole-case orchestration (IntelHarness) — persistent, versioned, cross-case Collect→Correlate→Assess to convergence (needs the venv deps + an LLM key for `continue`). **T2:** `intel.py harness open CASE-0001 <seeds…>` · `continue CASE-0001 --depth 4` · `status [CASE-0001]`. Persists to `cases/`; `status` needs no key | `/harness status CASE-0001` |
| `/graph --render` | **Built-in.** **IntelGraph** publication-quality render of a case graph → PNG/SVG (distinct from the ASCII `/graph`). **T2:** `intel.py graph <case_graph.json> <out-stem> --legend`. **T1:** `render_diagram` | `/graph --render case_graph.json out` |
| `/report pdf` | **Built-in.** **IntelReport** pandoc render of an assessment `.md` → polished **PDF/DOCX** (editorial house style, cover/TOC/figures, VN-safe). Complements `/report docx`. **T2:** `intel.py report <assessment.md> <out-stem> --pdf --docx`. **T1:** `render_report` | `/report pdf assessment.md out` |
| `/clusters [case]` | **Built-in.** Partition a case into same-operator clusters **before** judging it — the unit of judgment is the cluster, not the case. Shows each binding indicator's KB-wide prevalence, so an indicator that binds 3 domains here but sits on 400 KB-wide reads as noise. Pure KB read. **T2:** `intel.py clusters <case>`. **T1:** `case_clusters` | `/clusters CASE-0001` |
| `/frontier [case]` | **Built-in.** The case's unresolved gaps — free next seeds already discovered (crt.sh SAN, passive-DNS co-host, TLS co-SAN, CORS, reverse-WHOIS) plus the **deferred metered leads** held for approval. `reopen` re-opens a converged case on new seeds. **T2:** `intel.py frontier <case>` · `intel.py reopen <case> <seed…>`. **T1:** `case_frontier`/`case_reopen` | `/frontier CASE-0001` |
| `/loop [case]` | **Built-in.** Collect → assess repeatedly until the case converges, instead of stopping at an arbitrary depth. **T2:** `intel.py loop <case>`. **T1:** `case_loop` | `/loop CASE-0001` |
| `/scope [case]` | **Built-in.** Case **intake**: the no-touch class, victim ownership and the egress gate, derived up front rather than assumed mid-run. A defaulted value is never rendered as an answer. **T2:** `intel.py scope <case>`. **T1:** `case_scope` | `/scope CASE-0001` |
| `/liveness [domain]` | **Built-in.** Is it actually alive? A 200 parking/default/suspended/soft-404 page is **not** live and a 404/403/5xx/bot-wall is **not** dead — only NXDOMAIN reports dead, and every still-controlled name sets `reuse_watch`. **T2:** `intel.py liveness <domain>`. **T1:** `domain_liveness` | `/liveness scam-site.top` |
| `/pssl [domain\|cert]` | **Built-in.** Passive SSL — the historical **cert → IP** direction that recovers an origin from behind a CDN, with the base-rate rail that keeps a shared CDN certificate out of the clustering. Free (same CIRCL account as passive DNS), so it is on by default in the pipeline. **T2:** `intel.py pssl <target>`. **T1:** `passive_ssl` | `/pssl example.com` |
| `/paths [url]` | **Built-in.** The URL **path** as a clustering indicator (`path_kit:`) — for an operator who rotates disposable hosts and selects the branded template by directory instead. A generic path (`/login`, `/assets`) emits nothing; the base-rate denylist is the whole reason this is safe. **T2:** `intel.py paths <url>`. **T1:** `url_paths` | `/paths https://host/kitname/` |
| `/serp [domain]` | **Built-in.** The **advertising** layer — Google Ads Transparency (who *paid*: a verified, billed advertiser identity) plus the cloaking probe with its falsification control. Opt-in per run: it spends a SerpApi search per host. **T2:** `intel.py serp <domain>`. **T1:** `serp_ads` | `/serp scam-site.top` |
| `/docmeta [url\|file]` | **Built-in.** Document/image metadata — PDF `/Info` + XMP, EXIF (incl. GPS), PNG chunks — the author string an operator forgot to strip. Base-rate filtered on both the pivot and ingest paths. **T2:** `intel.py docmeta <target>`. **T1:** `doc_metadata` | `/docmeta https://site/brochure.pdf` |
| `/screenshot [url]` | **Built-in.** A rendered **full-page PNG** as timestamped, hashed **visual evidence** — the page as a human sees it (a channel bio naming admins, a members-area panel, a deposit page). Renders post-JS in a real browser, so it captures what the page *displays*, not what the DOM says. `--verify` re-hashes a stored capture. **T2:** `intel.py screenshot <url> --case <id>`. **T1:** `capture_screenshot` | `/screenshot https://scam-site.top` |
| `/exhaust [case]` | **Built-in.** Which collection layers actually **RAN** versus silently never fired. A layer that never executed looks identical to a layer that found nothing — this names the difference, so "no wallets" is not read as a fact about the operator when the wallet extractor never ran. **T2:** `intel.py exhaust --file <pivot.json>`. **T1:** `collection_gaps` | `/exhaust CASE-0001` |
| `/misp-export [case]` | **Built-in.** **IntelShare** — build a MISP event from the case's own collected pivots. **Local only, no network**: it writes the event JSON so you can read every attribute before anything leaves the machine. Sets TLP, distribution, threat level and tags. **T2:** `intel.py misp-export <case> --tlp amber`. **T1:** `misp_export` | `/misp-export CASE-0001` |
| `/misp [search\|push\|publish]` | **Built-in. Two separate decisions, deliberately.** `search` asks the cheaper question first — is this indicator already known to the instance? `push` **stages** the event on your instance, organisation-only and unpublished (a real write, but still deletable). `publish` syncs it to the community and **cannot be recalled** — every indicator becomes somebody else's blocking rule, so a false positive blocks innocent infrastructure on networks you will never see. Both write paths prompt via `hooks/actionguard.py`. **T2:** `intel.py misp keycheck\|budget\|search\|push\|publish`. **T1:** `misp_search`/`misp_push`/`misp_publish` | `/misp search 1.2.3.4` |
| `/pivot-extract <.eml>` | **Built-in.** `pivot_extract` also takes a **victim's saved email**. The `.eml` is parsed to its HTML body, so every HTML-side extractor runs over **what the funnel actually sent** — then header/CDN-derived selectors (sender domains, sending platform) emit pivots like any other artifact. This is the funnel's *first hop*, and no live fetch of the landing page can recover it. **T2:** `intel.py pivot-extract ./saved.eml`. **T1:** `pivot_extract` | `/pivot-extract ./phish.eml` |
| `/victims [case]` | **Built-in.** Infer the **access vector** from the victim set, plus demography (country + sector) — who was hit tells you how. **T2:** `intel.py victims --case <id>`. **T1:** `victim_profile` | `/victims CASE-0001` |
| `/case-timeline [case]` | **Built-in.** **IntelGraph** infrastructure-lifecycle timeline — registration/expiry spans, registrant eras, IP hosting windows, cert validity, archive visibility — with an evidence ledger citing every dated fact to an online source. **T2:** `intel.py timeline <case>`. **T1:** `case_timeline` | `/case-timeline CASE-0001` |
| `/tool-calls [case]` | **Built-in.** Audit what the model **actually** called during a run, including the denied calls — `intel.py dashboard` serves the same data as a loopback-only inspector (cost, trace, tool pairing). **T2:** `intel.py tool-calls <case>` · `intel.py dashboard`. **T1:** `tool_calls` | `/tool-calls CASE-0001` |
| `/login-detect [url]` | **Built-in.** **Engage** (detection half — passive and free): find the login form, the password field and the registration page, and classify by *fields* (a confirm-password means register; an invite code is a pivot, not an OTP). **T2:** `intel.py login-detect <url>`. **T1:** `detect_login` **T2:** `intel.py login-detect <url>`. **T1:** `detect_login` | `/login-detect https://scam-site.top` |
| `/engage [url]` | **Built-in. GATED — outbound, attributable, irreversible.** Create a **synthetic-persona** account and log in to read the members area (panel, deposit/withdraw flow, affiliate tree, support handles). Refuses without explicit confirmation, refuses a non-synthetic persona or direct egress, and stops at a CAPTCHA. Same gate class as a sandbox submission — **ask first, always**. **T2:** `intel.py persona` → `intel.py engage <url>` → `intel.py engage-harvest` → `intel.py engage-report`. **T1:** `make_persona`/`engage_account`/`harvest_authenticated`/`engage_report` | `/engage https://scam-site.top` |

---

## 4. Subject & Connection Model

Reference: `engine/case-schema.json`, `engine/subject-registry.md`

### Subject Types

| Type | Emoji | Examples |
|------|-------|---------|
| Person | 👤 | Full name, alias |
| Username | @ | Social handle |
| Email | 📧 | Address, domain |
| Domain | 🌐 | Site, subdomain |
| IP Address | 🖥 | IPv4, IPv6 |
| Organization | 🏢 | Company, group |
| Phone | 📱 | E.164 format |
| Location | 📍 | GPS, address |
| Asset | 📦 | Document, image |
| Event | 📅 | Dated occurrence |
| Device | 🖥️ | IoT device, server, workstation |
| Image | 🖼️ | Photograph, screenshot |
| Crypto Address | 💰 | Bitcoin, Ethereum wallet |
| Bank Account | 🏦 | IBAN, local account no., BIC |
| ICP Filing | 📋 | PRC licence serial (one registrant, many sites) |
| Custom | 🏷️ | User-defined entity type |

### Connection Types

```
owns         — domain, email, or asset ownership
uses         — platform account or tool usage
works_at     — employment or affiliation
linked_to    — general association
alias        — same identity, different handle
communicated_with — observed contact
```

### Finding Trust Scores

| Score | Label | Meaning |
|-------|-------|---------|
| 5 | PRIMARY | Authoritative or official source |
| 4 | DERIVED | Confirmed by 2+ independent sources |
| 3 | CONFIRMED | Single reliable source, verified |
| 2 | ANECDOTAL | Reported but unverified |
| 1 | CONTESTED | Conflicting data exists |

### Source Reliability Scale

Complements numeric trust scores with source-level grading. Trust score rates finding content; source reliability rates the source itself.

| Grade | Label | Typical Sources |
|-------|-------|-----------------|
| A | Completely Reliable | Official registries, government records |
| B | Usually Reliable | Established outlets, corporate sources |
| C | Fairly Reliable | Known blogs, industry publications |
| D | Not Usually Reliable | Anonymous forums, unverified claims |
| E | Unreliable | Known disinformation, fabricated content |
| F | Cannot Be Judged | Insufficient information to assess |

### Confidence Levels

| Level | Label | Use When |
|-------|-------|---------|
| VERIFIED | Direct observation, primary source | |
| STRONG | Multiple corroborating sources | |
| MODERATE | Single reliable source | |
| WEAK | Circumstantial or inferred | |
| TENTATIVE | Analyst deduction only | |
| CHALLENGED | Contradicted by other findings | |

### Likelihood Language (judgments, not findings)

The three scales above grade **evidence**. An analytic **judgment** built on that evidence —
an attribution, a motive, a forecast — carries a probability-anchored likelihood term instead.
Without an anchor, "MODERATE" routinely means a 30-point-different thing to writer and reader.

| Term | Band | | Term | Band |
|------|------|---|------|------|
| Almost no chance | 1–5% | | Likely / probable | 55–80% |
| Very unlikely | 5–20% | | Very likely | 80–95% |
| Unlikely | 20–45% | | Almost certain | 95–99% |
| Roughly even chance | 45–55% | | | |

**Likelihood and confidence are orthogonal — report both:**
> The operator is **very likely** based in Guangdong (**moderate confidence** — single
> registry record, unverified).

Never 0% or 100%. One term per judgment. Never attach a likelihood term to a directly
observed fact. `findings[].confidence` in the report JSON stays an integer describing
**evidence quality** — likelihood lives in the narrative.

**Attribution claims additionally require an ACH matrix** (competing hypotheses, scored by
inconsistency, runner-up named). Full rules — likelihood, the 5W1H coverage overlay, and ACH:
[`handbook/analytic-standards.md`](handbook/analytic-standards.md).

### Map Rendering (ASCII Mandatory)

**ALL visualization commands produce ASCII box-drawing art by default.** This includes `/graph`, `/render entities`, `/render network`, `/render timeline`, `/render risk`, `/pathfind`, and `/show-connections`. Mermaid available only with explicit `--mermaid` flag.

**Why ASCII-first:** Universal terminal compatibility, renders correctly in .md and .docx exports, no external renderer dependency.

```
┌─────────────────────────────┐   owns   ┌───────────────────────────┐
│ 👤 John Doe          [3/5] │══════════▶│ 🌐 example.com     [4/5] │
└─────────────────────────────┘           └───────────────────────────┘
         │ works_at                       │ hosted_on
         ▼                                ▼
┌─────────────────────────────┐  ┌───────────────────────────┐
│ 🏢 Acme Corp         [4/5] │  │ 🖥 203.0.113.10    [4/5] │
└─────────────────────────────┘  └───────────────────────────┘
```

**Connection arrows:**  `═══▶` owns · `───▶` confirmed · `···▶` inferred · `←─▶` bidirectional · `─·─▶` alias · `╌╌▶` works_at
**Box styles:**  `┌──┐` confirmed · `┌ ─ ┐` unverified · `╔══╗` target
**Badge:**  `[n/5]` trust score · emoji prefix = entity type

---

## 5. Finding Framework

Reference: `engine/finding-framework.md`, `engine/conflict-resolver.md`

Every finding logged via `/record-finding` captures:

```
Source URL / method
Collection method (browser | search | fetch | manual)
Trust score (1–5)
Confidence level (VERIFIED → CHALLENGED)
Timestamp
Linked subjects
```

**Conflict detection** (`engine/conflict-resolver.md`): When two findings about the same subject contradict each other, the system flags a CONTESTED state. Both findings are preserved. Resolution options: accept one, mark both TENTATIVE, or log the conflict as its own finding.

**Deviation detection** (`analysis/deviation-detector.md`): Automatically flags behavioral anomalies — account creation gaps, platform presence inconsistencies, metadata mismatches.

**Weight engine** (`analysis/weight-engine.md`): Aggregates trust scores across findings to compute subject-level confidence.

---

## 6. Technique Catalog

Reference directory: `techniques/`

| File | Covers |
|------|--------|
| `fx-metadata-parsing.md` | EXIF, email headers, document metadata analysis |
| `fx-image-verification.md` | Image authenticity and provenance workflow |
| `fx-breach-discovery.md` | Breach database methods and paste site search |
| `fx-geolocation.md` | GPS extraction, W3W, Plus Codes, MGRS, Street View |
| `fx-social-topology.md` | Social graph construction and topology |
| `fx-email-header-analysis.md` | Header analysis, SPF/DKIM, SMTP routing |
| `fx-document-forensics.md` | Document forensics and metadata extraction |
| `fx-http-fingerprint.md` | HTTP fingerprinting and server signature analysis |
| `fx-leak-monitoring.md` | Leak and breach monitoring, paste site search |
<!-- dork-integration:phase-05 start -->
| `fx-dork-sweep.md` | Zero-auth Google/Bing dork sweeps — Telegram ecosystem, doc-hosts, filetype families + 4-tier fallback cascade (WebSearch → Bing → DDG → agent-browser) |
| `fx-document-leak-hunt.md` | 18-platform document leak discovery with severity classification, paywall handling, auto-snapshot |
<!-- dork-integration:phase-05 end -->
| `username-osint.md` | 3000+ platform enumeration with pivot extraction |
| `phone-osint.md` | Carrier lookup, VoIP detection, spam databases, FreeCNAM CallerID, WhoCalld, USPhoneBook reverse lookup |
| `ema

…（正文过长，已截断，完整版见仓库）