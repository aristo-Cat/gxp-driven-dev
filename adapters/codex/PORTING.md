# Porting `gxp-driven-dev` skills to OpenAI Codex CLI

This guide ports a Claude Code `skills/<name>/SKILL.md` to Codex. One skill — `gdd.urs.from-idea` — is already ported as a worked reference under `gdd-urs-from-idea/`. Use it as the template.

## Codex format facts (confirmed 2026-05, OpenAI Codex developer docs)

- **`AGENTS.md`** is Codex's durable, always-on project-instruction file ([Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)). Codex walks from the **git root down to the current working directory**, at each level taking `AGENTS.override.md` → then `AGENTS.md` (→ then configurable fallbacks), and **concatenates root-first with closer files overriding**. Global defaults live at `~/.codex/AGENTS.md`. A merged-content byte cap applies (32 KB default). Codex rebuilds the chain every run — no cache to clear.
- **Slash commands / reusable prompts** ([Slash commands](https://developers.openai.com/codex/cli/slash-commands), [Custom prompts](https://developers.openai.com/codex/custom-prompts)): Markdown files become slash-invocable prompts; the command name derives from the filename. Frontmatter supports `description` and `argument-hint`; bodies support placeholders like `$ARGUMENTS`, `$1`, `$FILE`.
- **Custom prompts are deprecated in favor of *skills*** — but both are "Markdown with frontmatter, invoked as a slash command", so a prompt file written today is forward-compatible. We ship a `prompt.md` per skill.
- Codex grants tools by **approval mode**, not per-prompt — there is no `allowed-tools` equivalent to carry over.

## The two-part split (the core of the Codex port)

A Claude Code `SKILL.md` mixes two things; Codex wants them in two different homes:

| From `SKILL.md` | Codex home | Why |
|---|---|---|
| The **procedure** (pre-flight, interview/generation flow, output shape, post-flight) | `prompt.md` → slash `/gdd-<dashed-name>` | Invoked deliberately, only when the user runs the skill. |
| The **always-on invariants** (anti-hallucination, linear status, anonymization, read-manifest-first) | a snippet pasted into the consumer's `AGENTS.md` | AGENTS.md is always merged into context, so the guardrails hold even mid-task when the slash prompt is not the active turn. |

The reference port ships both: `gdd-urs-from-idea/prompt.md` + `gdd-urs-from-idea/AGENTS.snippet.md`.

> **The `AGENTS.snippet.md` is shared across the whole skill family**, not per-skill. When you port skill #2..#6, **extend the same snippet** (it already states the invariants generically for "any `specs/*.md`"); do not create a second guardrail file.

## Step-by-step (per remaining skill)

1. **Copy** `gdd-urs-from-idea/prompt.md` → `gdd-<dashed-name>/prompt.md`. Dot→dash the Claude Code `name:` for the slash command (`gdd.ra.from-urs` → `/gdd-ra-from-urs`).
2. **Frontmatter**: set `description:` from the source skill; set `argument-hint:` if the skill takes a seed input. Drop `allowed-tools:`.
3. **Body**: paste the source `SKILL.md` procedure + the `generation-flow.md` / `interview-flow.md` summary table + the `output-template.md` shape. Reference inputs by repo-relative path (`templates/csv/<DOC>.md`, `specs/<UPSTREAM>.md`).
4. **Guardrails**: do **not** add a new `AGENTS.snippet.md` — the shared one at `gdd-urs-from-idea/AGENTS.snippet.md` already covers all skills. If the new skill needs an invariant not yet listed, add it there.
5. **Post-flight**: keep every `python <gdd-path>/skills/_scripts/*.py` call **verbatim** — the deterministic shared core is identical across harnesses.
6. **Anonymization**: these files are inside the toolkit tree, so `anti-leak-guard.py` scans them. Canonical acronyms only; no source-org names, doc codes, ID schemes, site codes, or heritage terms.

## Install instructions for consumers

- **Slash prompt**: place `prompt.md` where Codex discovers prompts/skills (e.g. `~/.codex/prompts/gdd-urs-from-idea.md`, or the repo's configured prompts dir). It then appears as `/gdd-urs-from-idea`.
- **Guardrails**: append the contents of `AGENTS.snippet.md` to the project's root `AGENTS.md` (or a nested `AGENTS.md` if the specs live in a sub-package).
- Substitute `<gdd-path>` in the post-flight commands with the local `gxp-driven-dev` install path.

## Gotchas

- **Do not put the procedure in `AGENTS.md`.** A full interview flow in an always-on file wastes the 32 KB budget and fires on unrelated turns. Procedure → slash prompt; only invariants → AGENTS.md.
- **`AGENTS.override.md`** is for the *consumer's* local overrides; the toolkit ships `AGENTS.md`-destined snippets, never an override.
- Codex has no `AskUserQuestion`; pose discrete choices as an explicit enumerated prompt and lean on the interaction principles in the body.

## Open question for the owner

- Codex *skills* (the successor to custom prompts) may gain a richer manifest than a bare `prompt.md`. Decision deferred to when Codex's skills format stabilizes: ship `prompt.md` now (forward-compatible), and revisit whether to emit a native Codex *skill* package at `v0.5.0` GA.
