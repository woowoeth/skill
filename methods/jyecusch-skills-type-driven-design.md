---
name: type-driven-design
description: Make types carry proof instead of comments and runtime checks. Use when reviewing or writing type/interface definitions, signatures that pass raw strings/numbers for domain concepts (ids, money, quantities, units), validation logic, or comments stating constraints ("must be positive", "whole units only", "see constants in ../x").
---

# Type-Driven Design

Core rule: **parse, don't validate** (Alexis King). Validation inspects a value and returns it unchanged — the knowledge that it passed evaporates immediately, so every downstream function must either re-check or blindly trust. Parsing converts less-structured input into a more-structured type that *cannot represent* the invalid case, once, at the boundary. From then on, possession of the value is compiler-enforced proof of validity everywhere it travels.

Flag:

1. **Primitive obsession**: domain concepts passed as bare `string`/`number`. `userId: string` accepts an email, an id from the wrong system, or `""` — all compile. Replace with a branded type whose parse function is the *only* producer:
   ```ts
   type UserId = string & { readonly __brand: "UserId" };
   function parseUserId(raw: string): UserId { /* check or throw */ }
   ```
   Branding is required in structurally-typed languages — a bare `type UserId = string` alias enforces nothing. (Rust/Haskell: newtype; elsewhere: a small nominal wrapper class.) Keep the brand/constructor private so the parse function can't be bypassed.

2. **Comments doing a type's job**: "Amount in whole cents; no decimals" on `amount: number` is a plea. A `Cents` type whose parser rejects decimals is a law. Any doc comment stating a constraint on a field or parameter is a type waiting to be written — and once the type exists, the comment is deleted, not kept as decoration.

3. **Prose links where the compiler could enforce**: a comment like "see `REGION_CODES` in `../constants`" is an unenforced pointer that goes stale silently. Derive instead — `type Region = (typeof REGION_CODES)[number]` — so the constant is the single source of truth and drift is a compile error, not a doc bug.

4. **Correlated fields typed independently**: when one field's valid values depend on another ("the shape of `value` depends on `unit`"), a comment can only warn; generics or discriminated unions can forbid:
   ```ts
   interface SensorReading<U extends Unit = Unit> {
     unit: U;
     value: UnitValue[U];   // value's type varies with the unit
   }
   ```
   Make the illegal combination unrepresentable, not documented.

5. **Domain types defined at the wrong layer**: a concept used across the system (`UserId`) defined locally inside one service file will fragment into rival definitions and defeat the proof. Domain types live in the domain model and replace the primitive *everywhere* it flows — report the full replacement as a finding with its blast radius rather than quietly typing one file. The one exception: two systems with genuinely different concepts behind one word (internal `OrderId` vs the vendor's `VendorOrderId`) get two types plus one explicit mapping at the seam where the systems meet — never one type doing double duty.

6. **Re-validation downstream**: interior code re-checking what a type should already prove means either the boundary isn't parsing or the type isn't really proof (an unbranded alias, an exported constructor). Parse at every boundary — API edge, DB read, queue consumer — and let interior signatures accept only parsed types.

Cost check (see `abstraction-and-coupling`): brand the concepts with real invariants or real mix-up risk — ids, money, quantities with units, sanitized/escaped content, verified credentials — not every string in the program. The test: would confusing this value with another string-shaped value, or skipping its check, cause a real bug? If yes, it earns a type.
