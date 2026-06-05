# MEMORY — gxp-driven-dev (durable lessons)

Auditable, in-Git memory of durable lessons — the traps and agent-failures that bite again.
NOT current state (that's `STATE.md`), NOT the deep journal (private `PROGRESS.md`).

**How to use:** read at the start of any serious task; at the end, propose an entry if a lesson
emerged. Keep only lessons that will matter again in ~30 days. No secrets, no client/org data.
Health test: deletable + shows in a git diff = healthy; vague or ephemeral = contamination, cut it.

## Recurring traps

- **Windows ships a fake `python3` execution-alias stub.** `command -v python3` resolves it but it
  errors ("Python was not found") instead of running. Resolve an interpreter by EXECUTING each
  candidate, not by name alone:
  `for p in python3 python py; do command -v "$p" >/dev/null && "$p" -c "import sys" >/dev/null 2>&1 && { PY=$p; break; }; done`
- **`AGENTS.md` is the single source; `CLAUDE.md` is just `@AGENTS.md`** (L10). Edit `AGENTS.md`, never
  `CLAUDE.md`. History: the two were once byte-mirrored and drifted silently (editing `AGENTS.md` without
  Reading it first dropped the edit and shipped a stale mirror). L10 removed that failure mode by
  collapsing to one source; `.githooks/pre-commit` (C) now just checks `CLAUDE.md` stays the stub.
- **`anti-leak-guard.py` scans the WORKING TREE, not git history.** "0 leaks" does not prove history is
  clean — any public publish must be a clean-slate / orphan commit. The `.leak-overlay.txt` is
  git-ignored, so a fresh clone or public CI has zero patterns unless `LEAK_OVERLAY` is set.
- **Parallel / background sub-agents share the account session limit.** A mid-run reset can return an
  error instead of the agent's report and leave NOTHING on disk — verify the filesystem before trusting
  an agent's "done."
- **`generate-rtm.py` writes `RTM.md` (a side effect).** Running it mutates the specs dir — revert
  timestamp-only churn; don't commit a no-op RTM rewrite.
- **`gdd_common.REQUIREMENT_ID_RE` mis-segments multi-part DOC-TYPEs** (`RA-INIT` → category `INIT`).
  `NON_CATEGORY_MIDDLES` guards against phantom categories — keep that guard when touching ID parsing.
- **Shell gotcha:** `cmd | while read …; fail=1` runs the loop in a subshell, so `fail` never escapes.
  Use `for x in $(cmd)` when a loop must mutate outer state. (Hit while writing `.githooks/pre-commit`.)

## Commands that fixed real problems

- Strip CRLF from shell scripts edited on Windows: `sed -i 's/\r$//' <file>` (CRLF breaks `sh`).
- Activate the repo's git locks: `git config core.hooksPath .githooks` (or `sh .githooks/install.sh`).

## Decisions → see `STATE.md`

The "why" behind load-bearing choices (brand `gxp-`, Apache 2.0, CR vs CC, EU Annex 11 2025 edition,
the 22 categories, presets-conditional) lives in `STATE.md`'s consolidated-decisions table. Not
duplicated here — this file is for traps, not decisions.
