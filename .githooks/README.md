# .githooks/ — the locks (L7: the file ASKS, the hooks ENFORCE)

`CLAUDE.md` / `AGENTS.md` express *intent*. Intent is not enforcement: a model may forget, and an
autonomous agent running unattended will eventually do the thing the file told it not to. These hooks
turn the load-bearing red lines into **locks** that hold regardless of what the model decides.

## The four enforcement layers

| Layer | Mechanism | In this repo |
|---|---|---|
| intent (softest) | `AGENTS.md` / `CLAUDE.md` | anonymization rule, ID scheme, "stop and ask" |
| **intercept** | **git hook** (pre-commit / pre-push) | **these files** |
| permission | rules / `permissions.deny` | documented per-harness for Codex in `adapters/` (roadmap) |
| boundary (hardest) | sandbox | n/a for a Markdown repo |

> The more irreversible the action, the lower (harder) the layer it belongs in. The single most
> irreversible action here — a public push of contaminated history — gets the hardest lock a git repo
> offers: a `pre-push` hard-block.

## What each hook catches

### `pre-commit`
- **(A) anti-leak** — runs `anti-leak-guard.py` over the whole tree; blocks the commit if the
  source-organization identity appears anywhere. Moves the CI gate to the earliest possible moment —
  before the leak enters history, where removal is expensive.
- **(C) single source** — every `CLAUDE.md` must be the `@AGENTS.md` import stub (L10: one source, no
  mirror), not a copy. Catches editing `CLAUDE.md` directly instead of the canonical `AGENTS.md`.
- **(D) staged frontmatter** — runs `validate-frontmatter.py` on staged `templates/csv/*.md`
  (`--dry-run`) and `examples/*/specs/*.md` (instance mode).

### `pre-push`
- Runs the anti-leak guard, then **hard-blocks by default**. The guard scans the working tree, **not git
  history**, so "0 leaks" does not prove history is clean. Override only after verifying history:
  `GDD_ALLOW_PUSH=i-have-verified-history-is-clean git push ...`

## Install (once per clone)

```sh
sh .githooks/install.sh   # sets core.hooksPath -> .githooks
```

## Bypass

Hooks are guardrails against accidents and unattended agents, not against a determined human.
`git commit --no-verify` skips them — use it consciously, never as a habit.
