---
name: golang-best-practices
description: Use when writing, reviewing, or refactoring Go code in this repository — covers idiomatic error handling, naming, package/API design, concurrency, context usage, testing, and running golangci-lint before considering Go work done.
---

# Golang Best Practices

## Overview

Idiomatic Go favors clarity and small interfaces over cleverness. This repo
(`golangllm`, a single-package SDK) is deliberately minimal — match its style,
don't add abstractions it doesn't need.

## Quick Reference

| Area | Rule |
|---|---|
| Errors | Return them, don't panic. Wrap with `fmt.Errorf("doing X: %w", err)` only when adding context the caller doesn't already have. Check every returned error. |
| Naming | Short names for short scopes (`i`, `ctx`, `err`). Exported identifiers get doc comments starting with the identifier's name. No `Get` prefix on getters. |
| Interfaces | Define them where they're *consumed*, not where implemented. Accept interfaces, return concrete types. |
| `context.Context` | First parameter, named `ctx`, never stored in a struct. Never pass `nil` — use `context.TODO()` if there's truly nothing yet. |
| Concurrency | Every goroutine you start must have a clear owner for its lifetime and errors — `sync.WaitGroup` / `errgroup.Group`, not fire-and-forget. Protect shared state with a mutex or a channel, not both. |
| Zero values | Design structs so the zero value is useful when possible; avoid requiring a constructor for simple types. |
| Package layout | Package name = last path element, lowercase, no underscores. Avoid a package growing into a dumping ground — but don't split this repo's single package without a concrete reason. |
| Tests | Table-driven, `t.Run(name, ...)` per case. Use `t.Fatalf`/`t.Errorf` with the actual/expected values in the message. Use `httptest.Server` for HTTP-dependent code (see `client_test.go`). |
| Comments | Explain *why*, not what — the code already says what. Doc comments on every exported type/func. |
| Linting | Run `golangci-lint run` before calling any Go change done; fix or justify every finding. |

## Error Handling

```go
// Wrap when adding context; don't wrap just to re-signal the same error.
resp, err := c.anthropic.Messages.New(ctx, params)
if err != nil {
    return nil, fmt.Errorf("calling anthropic messages.new: %w", err)
}
```

Prefer `errors.Is`/`errors.As` over string matching or type switches on errors.
Sentinel errors are `var ErrX = errors.New("x")`, not string comparisons.

## Concurrency & Context

- Pass `ctx` through every call that can block on I/O or another goroutine.
- Respect cancellation: check `ctx.Err()` or select on `ctx.Done()` in loops that
  don't otherwise return quickly.
- When running work concurrently (e.g. multi-tool execution), use
  `golang.org/x/sync/errgroup` to propagate the first error and cancel siblings,
  rather than hand-rolled `WaitGroup` + shared error variable.

## Testing

- One assertion failure per `t.Run` subtest should tell you exactly what broke
  without opening the code.
- Don't mock what you can run for real in-process (`httptest.Server`,
  in-memory implementations) — mock only true external boundaries.
- Never call live AWS or Anthropic in `go test`. Use `httptest`; `media`
  tests must set `BaseEndpoint` + `HTTPClient`. `internal/noaws` rejects
  `*.amazonaws.com` and IMDS if a test forgets the fake.
- A test file mirrors its source file (`client.go` → `client_test.go`).

## Linting

This repo lints with `golangci-lint` (config: `.golangci.yml`, schema v2).

```bash
golangci-lint run          # lint
gofmt -s -l .               # formatting-only check (golangci-lint's gofmt runs with -s)
gofmt -s -w <file>           # fix formatting
```

Enabled beyond golangci-lint's `standard` set: `errcheck`, `errorlint`, `gocritic`,
`gosec`, `bodyclose`, `noctx`, `revive`, `staticcheck`, `unconvert`, `unparam`,
`unused`. Treat a new finding as a real defect first — only add an exclusion in
`.golangci.yml` when the rule is genuinely wrong for a specific, narrow case, and
say why inline.

## Dependency Vulnerabilities

Run `govulncheck ./...` whenever `go.mod`/`go.sum` change (new dependency,
version bump, `go mod tidy`) — `go build`/`go test` passing says nothing about
whether a dependency has a known CVE. It found a real, reachable DoS panic in
`aws-sdk-go-v2/aws/protocol/eventstream` in this repo's history (GO-2026-5764),
fixed by bumping the module, not by code changes here. If it flags something
with no fixed version yet, don't suppress it silently — note the finding and
why it's accepted (e.g. unreachable code path) in the PR/commit, and re-check
next time deps move.

## Common Mistakes

| Mistake | Why it's wrong |
|---|---|
| `if err != nil { return err }` immediately after wrapping the same error higher up | Duplicate context in error chains. Wrap once, at the boundary that adds meaning. |
| Storing `context.Context` in a struct field | Breaks per-call cancellation and request scoping; pass it explicitly instead. |
| Naked `go func() { ... }()` with no error/completion handling | Silently swallows panics and errors; leaks goroutines on shutdown. |
| Interface defined next to its implementation, not its consumer | Forces consumers to depend on the implementation package for a type they don't need the concrete type from. |
| Ignoring a `golangci-lint` finding without comment | The next reader can't tell if it was seen and accepted or missed. Suppress with `//nolint:<linter> // reason` when it's a deliberate exception. |
