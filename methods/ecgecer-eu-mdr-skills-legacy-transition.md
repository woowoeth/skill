---
name: legacy-transition
description: >
  Answer whether a legacy medical device can still be placed on the EU market under
  MDR Article 120 as amended by Regulation (EU) 2023/607, and by when. Use when the
  user asks "how long can we keep selling", "MDR transition deadline", "Article 120",
  "legacy device", "our MDD certificate", "do we still have until 2024", "extension",
  or describes a device certified under 90/385/EEC or 93/42/EEC.
argument-hint: "[device class, certificate basis, and what you need to know]"
---

# MDR Article 120 — the legacy transition

Answer from the **amended** text in `references/art120-amended.md`. Read it before
answering.

**The single most important thing about this provision:** Article 120 was substantially
rewritten by Regulation (EU) 2023/607 in March 2023. The original 2017 text set one
deadline — **26 May 2024** — for placing legacy devices on the market. That is superseded.
An answer citing 26 May 2024 as the market deadline is quoting law that no longer applies,
and it is the answer a model recalling the 2017 text will give.

---

## Step 0 — Three facts before any date

Ask for whatever is missing. The deadline is class-dependent and condition-dependent, so a
date given without these is a guess.

1. **Class under MDR** — III, IIb, IIa, or I. And if IIb, whether it is **implantable**,
   and if implantable whether it is one of the listed exceptions (sutures, staples, dental
   fillings, dental braces, tooth crowns, screws, wedges, plates, wires, pins, clips,
   connectors). Those exceptions move down a tier.
2. **The certificate basis** — a notified-body certificate under 90/385/EEC or 93/42/EEC
   (paragraph 3a), or formerly self-certified under 93/42 with a DoC before 26 May 2021
   and now requiring a notified body (paragraph 3b). Different routes, different rules.
3. **Whether the 3c conditions were met** — in particular the QMS by 26 May 2024 and the
   application lodged by 26 May 2024, with the written agreement signed by 26 September
   2024.

If 3 is unknown, say the date **conditionally** and name what would remove it:

> On class alone that device runs to [date]. But the extension is conditional, not
> automatic — it applies only if all five conditions in 120(3c) were met, including a
> quality management system in place by 26 May 2024 and a formal application lodged with
> a notified body by the same date, with the written agreement signed by 26 September
> 2024. If any of those was missed, the extension was never available and the answer is
> different. Can you confirm?

---

## The dates, the conditions, and what 26 May 2024 now means

All of it is in `references/art120-amended.md`, verbatim: the class-dependent deadlines,
the exception list, route 3b, and the five cumulative conditions in 3c. **Read it rather
than answering from memory** — the whole reason this skill exists is that the 2017 text
and the amended text give different answers, and only one of them is in front of you.

Two things to carry out of it, because they are what people get wrong:

- **The extension is conditional.** 120(3c) is cumulative, and two of its conditions had
  deadlines in 2024 that have passed. A device that met the class date but had no QMS in
  place by 26 May 2024 never qualified.
- **26 May 2024 changed job rather than disappearing.** It is no longer the market
  deadline; it is when the QMS and the notified-body application were due, with the
  written agreement due 26 September 2024. State both halves — someone told only the good
  news will not check whether they qualified.

## Output

```markdown
## [device]

**Class:** [as stated, or NOT SUPPLIED]
**Route:** [120(3a) certificate | 120(3b) formerly self-certified | not established]
**Deadline:** [date] — conditional on 120(3c)

| Question | Answer | Basis |
|---|---|---|
| Which paragraph applies | | `[verified]` |
| Class-dependent date | | `[verified]` |
| 3c conditions met? | | |

**What would change this:** [the fact that moves the date or removes the extension]

## Limits
[the block below]
```

## Citation discipline

- **`[verified]`** — Article 120(3), (3a), (3b), (3c), (3d) as amended, in
  `references/art120-amended.md`, from OJ L 80, 20.3.2023, retrieved 2026-09-10.
- **`[verify]`** — everything else: Article 120's other paragraphs, IVDR Article 110,
  MDCG guidance, Annex VII, Article 97, national practice.

**No silent supplement.** A `[verify]` tag is not permission to answer from memory. If
the question turns on something outside `references/`, **stop and say so** rather than
producing content with a tag on it:

> That turns on [IVDR Art. 110 / another Art. 120 paragraph / MDCG guidance], which this
> skill does not carry. I can flag it as an open question, or you can paste the provision
> and I will work from it. I will not give you dates I cannot cite from the reference
> file.

This matters most for **IVDR Article 110**. The IVD transition has its own dates on its
own clock, and producing them from recall — even tagged — is exactly the failure this
skill exists to prevent on the MDR side.

Never state a notified body's position or how an authority would treat a borderline case.

## Limits

> This covers MDR Article 120(3) and (3a)–(3d) as amended by Regulation (EU) 2023/607,
> retrieved verbatim from the Official Journal on 2026-09-10. It does **not** cover
> Article 120's other paragraphs, **IVDR Article 110** (the parallel IVD transition, whose
> dates differ), MDCG guidance including on what counts as a significant change, Annex VII,
> or national practice. The transition is conditional and fact-specific; this is a
> first-pass aid, not legal or regulatory advice, and not a substitute for your notified
> body or a qualified regulatory professional.
