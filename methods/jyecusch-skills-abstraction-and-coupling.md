---
name: abstraction-and-coupling
description: Judge whether an abstraction earns its keep. Use when reviewing shared base classes, common interfaces, DRY refactors, generics, or any layer introduced to remove duplication — and before creating one.
---

# Abstraction and Coupling

Every abstraction adds coupling: everything sharing it is now constrained to change together, and can only diverge by breaking the abstraction. Duplication is a visible, local cost you pay once; coupling is invisible at design time and charges interest at every future change. So: prefer a little duplication over the wrong abstraction (Sandi Metz).

Worked example: `EmailNotifier` and `SmsNotifier` both store a `recipient` string, so someone extracts `BaseNotifier` holding that field. Value gained: one assignment statement deduplicated. Cost: both classes are now constrained to a single-string-recipient model — a future `WebhookNotifier(url, secret)` or multi-recipient notifier breaks the abstraction. Verdict: not worth it; delete the base class.

Flag abstractions whose coupling outweighs their value:

- Shared parents/helpers extracted to save trivial code — a couple of assignments, one duplicated call. Deduplicating *logic* can be worth coupling; deduplicating *syntax* almost never is.
- Interfaces or base classes with a single implementation and no seam need — nothing selects an implementation at runtime, and no test swaps in a fake.
- DRYing *coincidental* duplication: code that looks alike today but answers to different owners — e.g. `adminDiscount` and `loyaltyDiscount` both happen to be `price * 0.9` this quarter. Merge them and the first divergent requirement forces an awkward un-merge.

An abstraction earns its keep when it **separates deciding from doing** — the choice of implementation moves away from the point of use (factories, polymorphic call sites, a scheduler that retries "a task" without knowing which) — or when three-plus genuinely interchangeable variants exist.

Verdict per abstraction: name the coupling it introduces, name the value it delivers, and recommend inlining it if the ledger is negative.
