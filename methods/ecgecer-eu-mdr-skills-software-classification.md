---
name: software-classification
description: >
  Classify medical device software (SaMD) under MDR Annex VIII — implementing rule
  3.3 and Rule 11 — and say which class it falls in and why. Use when the user asks
  "what class is our software", "is this Rule 11", "SaMD classification", "is our app
  class IIa or IIb", "MDR class for software", or describes software whose MDR class
  is in question.
argument-hint: "[describe the software and its intended purpose]"
---

# MDR Software Classification (Annex VIII)

Determine the class of software under **MDR Annex VIII**, using the verbatim text in
`references/annex-viii-software.md`. Read that file before answering.

This covers **software only**, and only the rules that bear on software: implementing
rules 3.1–3.7 and Rule 11. It does not carry Rules 1–10 or 12–22.

---

## Step 0 — Two prior questions, settled before any rule is applied

### Is the product a medical device at all?

Classification presumes qualification. If it is not established that the software meets
the Art. 2(1) device definition, that is the prior question and this skill does not
answer it. Say so:

> Before class, the product has to be a medical device under Art. 2(1). Nothing I have
> settles that, and it is a separate analysis. If qualification is already established,
> tell me and I will classify. If not, that comes first.

Do not classify a wellness app, a hospital administration tool, or a general-purpose
analytics product just because the question was asked in those terms.

### What is the intended purpose, as stated?

Implementing rule **3.1** anchors classification to the **intended purpose**, not to what
the software can technically do. Ask for it if it is not supplied:

> Classification runs on the intended purpose as you state it, not on capability. Can
> you give me the intended purpose as written in your technical documentation?

A capability outside the intended purpose does not raise the class. It raises a
different question — whether the intended purpose is stated correctly — and that is
worth flagging when you see it, as a note rather than a classification finding.

---

## Gate 1 — Does it drive or influence another device? (3.3)

**Run this before Rule 11. Every time.** It is the step most often skipped, and skipping
it produces a confident wrong answer.

> **3.3.** Software, which drives a device or influences the use of a device, shall fall
> within the same class as the device. If the software is independent of any other
> device, it shall be classified in its own right.

- **Drives or influences another device** → it takes **that device's class**. Rule 11 is
  not reached. Say which device, and that its class governs. If the driven device's class
  is unknown, the answer is "same class as X, which I need from you", not a Rule 11 class.
- **Independent** → continue to Gate 2.

Beware the middle case. Software that merely *displays* output from a device, without
driving it or influencing its use, is usually independent. Software that sets a
parameter, gates an alarm, or changes how the device is operated is not. Where it is
genuinely unclear, say which way it turns and what fact would settle it.

---

## Gate 2 — Rule 11, in order

Apply the limbs in this order. Stop at the first that matches.

### Limb 1 — information used to take diagnostic or therapeutic decisions → IIa, escalating

Base class **IIa**. Then test the **impact of the decision**, not the severity of the
disease:

- may cause **death or an irreversible deterioration** of health → **III**
- may cause **serious deterioration** of health, or **a surgical intervention** → **IIb**
- otherwise → **IIa**

The escalation asks what a wrong decision may cause. Software informing decisions in a
serious condition is not automatically III. Software whose output routinely triggers
surgery is IIb even if the condition is not itself life-threatening.

### Limb 2 — monitoring physiological processes → IIa, escalating

Base class **IIa**. Escalation to **IIb** requires **both**:

1. the parameters monitored are **vital** physiological parameters, **and**
2. the nature of their variation is such that it **could result in immediate danger**

Both. Monitoring a vital parameter that varies slowly and without urgency does not reach
IIb on this limb. Do not collapse "physiological process" into "vital parameter".

### Limb 3 — all other software → I

If neither limb 1 nor limb 2 is engaged on the stated intended purpose, the class is
**I**. Say so plainly. A class I answer is a real answer, not a failure to find something.

---

## Gate 3 — Could another rule reach it? (3.5)

> **3.5.** If several rules [...] apply to the same device [...] the strictest rule and
> sub-rule resulting in the higher classification shall apply.

Rule 11 sets a **floor, not a ceiling**. Before concluding, ask whether the intended
purpose also engages a rule this skill does not carry — for example software that is
itself an active therapeutic function, or that controls administration of a substance.

If it might, **do not conclude**. Say:

> Rule 11 gives class [X]. But 3.5 means the strictest applicable rule wins, and the
> intended purpose here may also engage [rule / concept], which I do not carry. That
> could raise the class. Worth checking Rules [n] before treating [X] as settled.

Better an incomplete answer than a confident floor presented as the class.

---

## Output

```markdown
# MDR Software Classification: [name]

**Intended purpose (as stated):** [quoted, or NOT SUPPLIED]
**Qualified as a device:** [established | not established — see note]

## Class: [I | IIa | IIb | III | cannot conclude]

**Route:** [3.3 → same class as driven device] or [3.3 independent → Rule 11 limb N]

## Reasoning
| Step | Question | Answer | Basis |
|---|---|---|---|
| 3.1 | Intended purpose | [quoted] | `[verified]` |
| 3.3 | Drives or influences another device? | [yes/no] | `[verified]` |
| Rule 11 | Which limb | [1/2/3] | `[verified]` |
| Rule 11 | Escalation | [none / IIb / III] and why | `[verified]` |
| 3.5 | Could a stricter rule apply? | [no / possibly — which] | `[verified]` |

## What would change this
[the specific facts that would move the class, named]

## Limits
[the block below, verbatim]
```

---

## Citation discipline

- **`[verified]`** — the provision is in `references/annex-viii-software.md`: Rule 11,
  implementing rules 3.1–3.7, and the Chapter I definitions carried there. Retrieved
  from EUR-Lex 2026-09-09 and re-checkable there.
- **`[verify]`** — anything else. Rules 1–10 and 12–22, Art. 2(1) qualification,
  Annex XVI, national practice.

**MDCG 2019-11 is guidance, not the rule.** It is not verified here and must never be
stated as binding. If an answer turns on it:

> This turns on MDCG 2019-11, which is Commission guidance rather than the regulation,
> and which I do not verify. The Annex VIII text takes me to [X]. I can flag the
> guidance question, or you can point me at the passage.

**No silent supplement.** A `[verify]` tag is not permission to answer from memory. If
the question turns on a rule this skill does not carry, **stop and say so**:

> That turns on [Rule N / Art. 2(1) qualification / Annex XVI], which this skill does not
> carry. I can flag it as an open question, or you can paste the text and I will work from
> it. I will not state a rule I cannot cite from the reference file.

Never state how a notified body would decide. Never invent a rule number.

## Limits

> This classifies software under MDR Annex VIII implementing rules 3.1–3.7 and Rule 11,
> retrieved verbatim from EUR-Lex on 2026-09-09. It does **not** cover Art. 2(1)
> qualification, Rules 1–10 or 12–22, Annex XVI, IVDR, MDCG guidance, notified-body
> practice, or national interpretation. Rule 11 is a floor: under 3.5 a stricter rule
> this skill does not carry may raise the class. A structured first pass and an audit
> aid, not legal or regulatory advice, and not a substitute for your notified body or a
> qualified regulatory professional.

## Before stating a class as settled

If the user is not a qualified regulatory professional, do not present the class as
final. Give the class, the route, and then:

> This is the Annex VIII text applied to the intended purpose as you stated it. The class
> drives your conformity route, whether you need a notified body, and the depth of your
> technical documentation, so it should be confirmed by your regulatory lead or notified
> body before you build on it. The three things to put in front of them: [the 3.3 call,
> the limb and escalation, and any 3.5 rule that might reach higher].
