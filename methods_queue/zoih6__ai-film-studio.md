---
name: ai-film-studio
description: |
  AI Film Studio v2.1.0 — نظام إنتاج أفلام متكامل بالذكاء الاصطناعي. يحوّل فكرة بسيطة إلى حزمة إنتاج كاملة: Concept + Script + Shot List + Prompts (10-Layer A-J) + Audio + Assembly Guide. يدعم 31 تخصصًا عبر 12 مرحلة (M0–M11) تتحقق كـ 31 workflow فعلي، و 8 بوابات جودة، و Orchestration Runtime لـ 10 مسارات، و Memory Conflict Resolution بـ 6 أنواع. يُستخدم للإعلانات، Brand Films، الأفلام القصيرة، الموشن جرافيك، والشورتس.
version: 2.1.0
license: MIT
triggers:
  - "فيديو إعلاني", "إعلان ذكاء اصطناعي", "فيلم قصير", "برومبت فيديو", "موشن جرافيك"
  - "AI film", "video prompt", "brand film", "commercial", "short film", "motion graphics"
  - "مشاهد سينمائية", "سكريبت", "shot list", "video generation", "AI cinema"
inputs:
  - "فكرة أو طلب (عربي/إنجليزي)"
  - "نوع المشروع (إعلان، قصة، شرح، Brand Film)"
  - "المنصة المستهدفة (YouTube, TikTok, Instagram, TV)"
  - "المدة، اللغة، اللهجة"
outputs:
  - "5 production packages: Blueprint + Image Prompts + Motion Prompts + Audio + Assembly Guide"
  - "Continuity Bible + Frame Chain + Quality Gates log"
  - "Orchestration Runtime: 10 routes (REPAIR / SINGLE_PROMPT / IMAGE_GEN / I2V / MOTION_GFX / LIPSYNC / CONCEPT / SHOT_BUILD / SCENE / FULL)"
  - "Memory Conflict Resolution: 6 types (NoConflict, ShotOverride, SceneOverride, ProjectCanonical, UserApproved, Ambiguous)"
when_to_use: "أي مشروع فيديو يحتاج برومبتات احترافية، اتساق بصري، تخطيط صوتي، ودليل تجميع."
---

# AI Film Studio

> **نقطة الدخول الرئيسية.** اقرأ هذا الملف أولًا، ثم اتبع المسار في `workflows/intent-router.md`.

## الفلسفة

> **"كلما كان المستخدم أقل خبرة، يجب أن تكون المهارة أكثر قدرة على تعويض هذه الخبرة داخليًا."**

المهارة تُحاكي **استوديو إنتاج حقيقي**: 31 تخصصًا يعملون عبر **12 مرحلة رئيسية (M0–M11)** تتحقق كـ **31 workflow فعلي** (filesystem)، مع 8 بوابات جودة صارمة، ومخرج نهائي واحد عبر `workflows/M9a-executive-producer.md`.

## بنية المستودع (Progressive Disclosure)

```
tier 1 — يُحمَّل دائمًا (≤ 5KB)
  └─ SKILL.md (هذا الملف)        → الفلسفة + خريطة المسار
  └─ README.md                    → للقراءة البشرية
  └─ CHANGELOG.md                 → تاريخ الإصدارات

tier 2 — يُحمَّل عند بدء مشروع (workflows/)
  └─ workflows/intent-router.md   → يحدد المسار الأدنى
  └─ workflows/M0..M11/           → 12 مرحلة إنتاج (المرجع الرئيسي)
  └─ workflows/shortcuts/         → مسارات سريعة (prompt واحد، صورة، lip-sync)

tier 3 — يُحمَّل عند الحاجة المتخصصة
  └─ schemas/                     → هياكل البيانات (production outputs)
  └─ references/specs/            → مواصفات (10-Layer A-J، transitions، audio)
  └─ references/protocols/        → بروتوكولات (output, decision, state machine)
  └─ references/knowledge/        → معارف متخصصة (failure modes, memory)
  └─ quality/                     → 8 Quality Gates (G0–G8) + checklists
  └─ examples/                    → أمثلة حية كاملة
  └─ scripts/                     → أدوات فحص قابلة للتنفيذ
```

**قاعدة التحميل:** لا تُحمَّل tier 2/3 إلا بعد أن يُحدد `intent-router.md` المسار المطلوب.

## المسار السريع (Quick Start)

### 1. حدّد النية (3 ثوانٍ)

افتح `workflows/intent-router.md` → أجب عن سؤال واحد → يحدد لك المسار.

| إذا كان طلبك... | المسار |
|---|---|
| "اكتب لي برومبت واحد" | `workflows/shortcuts/single-prompt.md` |
| "صورة/فريم واحد" | `workflows/shortcuts/image-generation.md` |
| "تحريك صورة موجودة" | `workflows/shortcuts/image-to-video.md` |
| "حوار/شفاه متحركة" | `workflows/shortcuts/dialogue-lipsync.md` |
| "موشن جرافيك/تايبوجرافي" | `workflows/shortcuts/motion-graphics.md` |
| "فكرة/Concept فقط" | `workflows/shortcuts/concept-only.md` |
| "مشهد متعدد اللقطات" | `workflows/M0-intake.md` → M3 |
| "فيلم/إعلان كامل" | `workflows/M0-intake.md` → M11 |

### 2. نفّذ المسار (5-90 دقيقة)

لكل workflow في `workflows/M*.md`:
1. **اقرأ فقط القسم "Entry Conditions"** (3 شرائط)
2. **نفّذ "Core Workflow"** (5-7 خطوات)
3. **مرّر عبر "Quality Gate"** (موثّق في `quality/quality-gates.md`)

### 3. استلم المخرجات (5 ملفات)

| # | الملف | الوصف |
|---|---|---|
| 01 | `schemas/production-blueprint.md` | النظرة الشاملة (Concept + Script + Scenes) |
| 02 | `schemas/image-prompts-package.md` | كل prompt صورة (10 طبقات A-J) |
| 03 | `schemas/motion-prompts-package.md` | كل prompt فيديو |
| 04 | `schemas/audio-package.md` | كل الطبقات الصوتية + lip-sync |
| 05 | `schemas/assembly-guide.md` | دليل التجميع خطوة بخطوة |

## المراحل الـ 12 / الـ 31 Workflow

> **النموذج الرسمي للمراحل:** `references/protocols/production-state-machine.md`.
> **الـ Orchestration Executable Spec:** `references/protocols/orchestration-runtime.md`.
> **Source of truth تشغيلي:** `workflows/M*.md` (filesystem).

| المرحلة | الاسم | الـ Workflows الفعلية | الجودة |
|---|---|---|---|
| **M0** | Intake | `M0-intake.md` | G0 |
| **M1** | Research + Concept | `M1a-creative-direction`، `M1b-concept-expansion`، `M1c-research-lab` | G1 |
| **M2** | Narrative | `M2-narrative.md` | G2 |
| **M3** | Shot Architecture | `M3a-shot-design`، `M3b-shot-list` | G3.1 |
| **M4** | Continuity + Transitions | `M4a-continuity`، `M4b-character-world`، `M4c-continuity-qc` (MANDATORY في multi-shot)، `M4d-transitions` | G3.2, G5 |
| **M5** | Graphics + Text | `M5a-graphics`، `M5b-text-motion` | G6 |
| **M6** | Audio | `M6-audio`، `M6b-sound-design`، `M6c-dialogue-lipsync` | G7 |
| **M7** | Image Prompts | `M7a-prompt-architecture`، `M7b-image-prompts` | G4 (Hard) |
| **M8** | Motion Prompts | `M8a-motion-prompts`، `M8b-motion-direction`، `M8c-animation-ready`، `M8d-motion-graphics` | G4 (Hard) |
| **M9** | Quality + Orchestration | `M9a-executive-producer`، `M9b-quality-gates`، `M9c-preflight`، `M9d-localization` | G4, G8 (Hard) |
| **M10** | Pre-Production Review | `M10a-production-architecture`، `M10b-hybrid-assembly`، `M10c-edit-color` | G8 (Hard) |
| **M11** | Final Delivery | `M11a-reference-analyst`، `M11b-visual-research` | Final |

## المبادئ المؤسِّسة (Core Principles)

1. **جودة الـ Prompt أهم من الاختصار** — لا تختصر لتوفير الوقت
2. **Identity String حرفي** — لا تُعد صياغة صفات الشخصية أبدًا
3. **Frame Chain إلزامي** — `SC(N+1)_START = SC(N)_END` بصريًا
4. **النص في الفيديو = Single Locked Visual Plane** — طبقة واحدة محكومة
5. **الصوت يصلح الصورة** — خطط للصوت مبكرًا، لا في النهاية
6. **8 Quality Gates صارمة** — Hard Gates (G4, G8) لا تُتجاوز
7. **Backward Compatible** — كل v1.x يعمل كما هو
8. **5 Output Files منفصلة** — لا تخرج برومبتات خام أبدًا

## المرجعيات الحرجة (اقرأ عند الحاجة)

- **10 طبقات Prompt Architecture (A-J):** `references/specs/prompt-architecture.md`
- **Continuity Bible Schema:** `references/specs/continuity-bible-schema.md`
- **12 نوع انتقال:** `references/specs/transition-types.md`
- **شجرة قرار الصوت:** `references/specs/audio-decision-tree.md`
- **نماذج مدعومة:** `references/specs/model-matrix.md`
- **Memory Schema:** `references/knowledge/memory-schema.md`
- **Failure Modes:** `references/knowledge/failure-modes.md`

## أوامر سريعة

```bash
# فحص السلامة البنيوية
python3 scripts/verify_structure.py

# فحص وظيفي شامل
bash scripts/verify_all.sh

# فحص مسار الموشن جرافيك
python3 scripts/verify_motion.py
```

## متى لا تستخدم هذه المهارة

- ❌ صورة ثابتة بسيطة (استخدم image generation skill مباشرة)
- ❌ ترجمة/صياغة نصوص بحتة (استخدم writing skill)
- ❌ سؤال تقني عن نموذج (ارجع لـ `references/specs/model-matrix.md` مباشرة)
- ❌ مشروع يحتاج أكثر من ساعة من الحوسبة بدون automation

## معلومات المشروع

- **License:** MIT
- **Repository:** github.com/zoih6/ai-film-studio
- **Maintainer:** AI Film Studio Team
- **Status:** Production-ready (v2.0+)
- **Compatibility:** Claude Sonnet/Opus, GPT-4+, Gemini Pro/Ultra

## النسخة

- **v2.1.0** — Memory Conflict Contract + Prompt Layer Alignment + Multi-fixture verify
- **v2.0.2** — Stage Model Unification (M0–M11) + Orchestration Runtime
- **v2.0.1** — Agent Skills Standard restructure (workflows/schemas/references/quality/scripts)
- **v2.0.0** — من Prompt Writer إلى AI Film Production System
- **v1.5.0** — Pre-flight + Localization
- **v1.0–1.4** — Initial release → production runtime

راجع `CHANGELOG.md` للتفاصيل.
