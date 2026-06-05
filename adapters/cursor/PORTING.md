# Porting `gxp-driven-dev` skills to Cursor Project Rules

This guide ports a Claude Code `skills/<name>/SKILL.md` to a Cursor **Project Rule** (`.mdc`). One skill — `gdd.urs.from-idea` — is already ported as a worked reference (`gdd-urs-from-idea.mdc`). Use it as the template for the rest.

## Cursor format facts (confirmed 2026-05, [Cursor Rules docs](https://cursor.com/docs/context/rules))

- Project rules live in **`.cursor/rules/`** in the consumer repo, as **`.mdc`** files (Markdown + YAML frontmatter). They replace the legacy `.cursorrules` file.
- **Three frontmatter keys**, and their combination chooses the rule *type*:

  | Type | Frontmatter | Behavior |
  |---|---|---|
  | **Always** | `alwaysApply: true` | Injected into every chat; other metadata ignored. |
  | **Auto Attached** | `globs:` set, `alwaysApply: false` | Attaches when a file matching the glob is in context. |
  | **Agent Requested** | `description:` set, no `globs` | Agent reads `description` and decides whether to pull the rule in. |
  | **Manual** | no `globs`, no decisive `description` selection | Only loads when **`@rule-name`** is mentioned in chat. |

- A rule can **reference other files** with `@filename` (e.g. `@templates/csv/URS.md`); Cursor pulls the referenced file in as context. This is how the shared-core principle is honored — the rule points at the canonical template instead of duplicating it.
- The rule **filename is the handle**: `gdd-urs-from-idea.mdc` → `@gdd-urs-from-idea`.

## Why `gdd.*` skills map to the **Manual** rule type

The gxp-driven-dev skills are deliberate, user-initiated procedures (the Claude Code equivalent is a `/gdd.*` slash command). They are **not** Always (would pollute every chat) and **not** glob-attached (they are not "edit a `.tsx`" reactions). So: `alwaysApply: false`, no `globs`, invoked by `@gdd-urs-from-idea`. The `description` is still filled (it helps Cursor's Agent-Requested path surface the rule), but Manual invocation is the intended trigger.

## Step-by-step (per remaining skill)

1. **Copy** `gdd-urs-from-idea.mdc` → `gdd-<dashed-name>.mdc` (e.g. `gdd-ra-from-urs.mdc`). The dash form of the Claude Code `name:` (dots → dashes) is the filename.
2. **Frontmatter**: keep `alwaysApply: false` and empty `globs:`. Rewrite `description:` from the source skill's `description:` block — keep it a crisp "use when…" so Agent-Requested mode can find it too. Drop `allowed-tools:` (no Cursor equivalent).
3. **Body**: paste the source `SKILL.md` orchestration prose, then fold in the `generation-flow.md` / `interview-flow.md` summary table and the `output-template.md` shape. For a reference port we keep it **one self-contained `.mdc`** (Cursor has no multi-file skill bundle); link the canonical template with `@templates/csv/<DOC>.md` rather than inlining it.
4. **Post-flight**: keep every `python <gdd-path>/skills/_scripts/*.py` call **verbatim**. These are the shared deterministic core — never reword them into "manually check…". Cursor's agent shells out the same way Claude Code does.
5. **Anonymization**: the `.mdc` lives inside the toolkit tree, so `anti-leak-guard.py` scans it. Use only canonical category acronyms and never name a source organization, corporate doc code, ID scheme, site code, or heritage term.
6. **Install location for consumers**: end users drop the `.mdc` into their project's `.cursor/rules/` (or symlink from the toolkit). Document the `<gdd-path>` they must substitute in the post-flight commands.

## Gotchas

- **`globs:` left empty** is correct for Manual rules — do **not** set it to `**/*` (that would silently make the rule Auto-Attached to everything).
- Cursor does not have Claude Code's `AskUserQuestion` tool; express discrete choices as an explicit enumerated prompt ("reply 1/2/3") and rely on the interaction principles in the body.
- A multi-file Claude skill (SKILL.md + flow + output-template) collapses into **one** `.mdc`. If the prose is very long, you may split into companion rules and `@`-reference them, but for the reference port a single file is clearer.

## Open question for the owner

- Should adapters ship the `.mdc` files **inside** `adapters/cursor/` (current choice, keeps them under the anti-leak gate) **and** provide an install script that copies them into a consumer's `.cursor/rules/`, or should we publish a separate `cursor-rules/` distribution? Current decision: keep authoring copies here; defer the install-script/distribution question to `v0.5.0` packaging.
