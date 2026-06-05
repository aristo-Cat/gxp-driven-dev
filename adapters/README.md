# Adapters — `gxp-driven-dev` skills on other harnesses

> **Status: `v0.5.0` adapter framework + reference port.** This directory establishes the **porting strategy** and ships **one fully-ported reference skill** (`gdd.urs.from-idea`) for both Cursor and OpenAI Codex CLI. The other 5 operative skills are **not yet ported** — they are documented as a mechanical follow-up using the pattern proved here. This is intentionally a framework + reference port, *not* a full port of the catalog.

The toolkit's skills are **Claude Code first** (`skills/<name>/SKILL.md`). Roadmap decision #5 ports them to other AI coding harnesses. This `adapters/` layer is how a single skill definition reaches Cursor and Codex without forking the logic.

---

## The shared-core principle (load-bearing)

A skill in this toolkit is two separable things:

| Part | What it is | Harness-agnostic? |
|---|---|---|
| **Deterministic core** | The Python in `skills/_scripts/` (`validate-frontmatter.py`, `generate-rtm.py`, `check-clarification-markers.py`, `lint-spec.py`, `anti-leak-guard.py`, `lib/gdd_common.py`) + the canonical `templates/csv/*.md` they read/validate | **YES — stays put, never duplicated** |
| **Orchestration prose** | The natural-language instructions that tell the agent *how to interview, what order, when to refuse, what to copy verbatim* — today the body of `SKILL.md` + `interview-flow.md` + `output-template.md` | **NO — this is what each adapter re-expresses** |

**Rule:** an adapter re-expresses the *orchestration prose* in the host's native format and **calls the same Python scripts by the same paths**. It never re-implements RTM generation, frontmatter validation, or the anti-leak guard in a host-specific way. If a future harness cannot shell out to Python, that is a porting blocker to record — not a license to fork the logic.

Consequences:
- A bug fixed in `generate-rtm.py` is fixed for every harness at once.
- The anti-leak guard (`anti-leak-guard.py`) remains the single anonymization gate across all harnesses.
- Only prose drifts between harnesses, and prose drift is visible in review.

---

## How a Claude Code `SKILL.md` maps to each harness

```
                    Claude Code (source of truth)
                    skills/<name>/SKILL.md  (+ interview-flow.md, output-template.md)
                    frontmatter: name, description, allowed-tools
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                                             ▼
   CURSOR rule                                   CODEX
   adapters/cursor/<name>.mdc                    adapters/codex/<name>/
   frontmatter: description, globs, alwaysApply  prompt.md (slash-invokable) +
   body = orchestration prose, @-references      AGENTS.md snippet (always-on guardrails)
   to templates/scripts
```

### Field mapping (Claude Code → Cursor `.mdc`)

| Claude Code `SKILL.md` | Cursor `.mdc` | Notes |
|---|---|---|
| `name: gdd.urs.from-idea` | filename `gdd-urs-from-idea.mdc` → invoked `@gdd-urs-from-idea` | Cursor has no `name` key; the filename is the handle. |
| `description:` (when-to-invoke) | `description:` | Cursor uses it for *Agent Requested* selection — keep it a crisp "use when…". |
| `allowed-tools: [...]` | — (no equivalent) | Cursor agent has its own tool surface; drop the key, keep any tool intent as prose. |
| Manual `/gdd.*` slash invocation | `alwaysApply: false` + no `globs` → **Manual** (`@rule`) | The interview is an explicit user action, so Manual is the right Cursor rule type (not Always, not glob-attached). |
| Body + `interview-flow.md` + `output-template.md` | single `.mdc` body, with `@templates/csv/URS.md` file references | Cursor inlines linked files; one self-contained rule is simplest for a reference port. |

### Field mapping (Claude Code → Codex)

| Claude Code `SKILL.md` | Codex artifact | Notes |
|---|---|---|
| `name: gdd.urs.from-idea` | prompt file `prompt.md` → slash `/gdd-urs-from-idea` (Codex derives the command from the filename / its location under a prompts dir) | Codex *custom prompts* are deprecated in favor of *skills*, but both are Markdown-with-frontmatter and invoked the same way; we ship a prompt file that is forward-compatible with the skills mechanism. |
| `description:` | prompt frontmatter `description:` (+ `argument-hint:`) | Shown in the slash menu. |
| `allowed-tools:` | — | Codex grants tools by approval mode, not per-prompt. |
| Always-on guardrails (anti-hallucination, anonymization, "never set status: approved") | a snippet for the **consumer project's `AGENTS.md`** | AGENTS.md is *always* in context (root→cwd merge), so it is the right home for invariants that must hold even when the slash prompt is not active. The slash prompt carries the *procedure*; AGENTS.md carries the *guardrails*. |
| Body + flow + output template | `prompt.md` body, referencing `templates/csv/URS.md` and the `_scripts/` paths by relative path | Codex reads referenced files from the repo. |

---

## Status matrix — 6 operative skills × 3 harnesses

| Skill (Claude Code source) | Claude Code | Cursor (`.mdc`) | Codex (prompt + AGENTS.md) |
|---|---|---|---|
| `gdd.urs.from-idea` | ✅ source of truth | ✅ **reference port** (`cursor/gdd-urs-from-idea.mdc`) | ✅ **reference port** (`codex/gdd-urs-from-idea/`) |
| `gdd.ra.from-urs` | ✅ | ⬜ planned (port mechanically) | ⬜ planned |
| `gdd.fs.from-urs` | ✅ | ⬜ planned | ⬜ planned |
| `gdd.ra.detail.from-urs-fs` | ✅ | ⬜ planned | ⬜ planned |
| `gdd.cs.from-fs` | ✅ | ⬜ planned | ⬜ planned |
| `gdd.tests.from-ra` | ✅ | ⬜ planned | ⬜ planned |

Legend: ✅ done · ⬜ planned (pattern proven, port is mechanical) · 🚫 blocked.

> Stub skills (`trace-validate`, `lint-spec`, `init-project`, `next`, `lifecycle`) are **not** in scope for adapters until they are operative on Claude Code first.

---

## Porting workflow (for the remaining 5 skills)

1. Read the source `skills/<name>/SKILL.md` (+ `generation-flow.md` / `output-template.md`).
2. **Cursor**: copy `cursor/gdd-urs-from-idea.mdc` → `cursor/<dashed-name>.mdc`; swap the body for the skill's prose; keep `alwaysApply: false`, no `globs` (Manual); replace `@templates/...` references with the skill's real inputs; keep all `python skills/_scripts/...` post-flight calls **verbatim**.
3. **Codex**: copy `codex/gdd-urs-from-idea/` → `codex/<dashed-name>/`; adapt `prompt.md`; the `AGENTS.md` guardrail snippet is **shared** across all skills — extend it, don't fork it per skill.
4. Run `python skills/_scripts/anti-leak-guard.py` from the toolkit root — adapters are inside the tree, so they are scanned by the same gate.
5. Flip the skill's row in the status matrix above.

See `cursor/PORTING.md` and `codex/PORTING.md` for the host-specific step-by-step.

---

## Machine-permissions layer

The "which commands may run" layer (per harness) lives in `machine-permissions.md` — reference
`.codex/rules` and `.claude/settings.json` examples that pin this repo's permission decisions
(git-push forbidden until history is clean, `rm -rf` forbidden, the `_scripts/` gates allowed). They
complement the git-level locks in `.githooks/` and stay examples (not live root config) to keep the
toolkit AI-agnostic.

## Versioning note

These adapters track the `v0.5.0` line. The reference port mirrors `gdd.urs.from-idea` as it exists at this version (`based_on_template_version: 0.1.0` for the URS template). When the source `SKILL.md` changes, the adapter is **regenerated**, not hand-patched — the source of truth is always `skills/<name>/`.
