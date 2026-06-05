# Machine-permissions layer (per harness)

The third configuration layer (see `CLAUDE.md` → **Configuration layers**): **which commands an agent
may run** when working in this repo. Team conventions live in `CLAUDE.md` / `AGENTS.md`; personal style
lives in your global config; **this layer is enforced, not asked.**

These are **reference examples**, intentionally *not* committed as live root config — so the toolkit
stays AI-agnostic and never clobbers a contributor's global setup. Copy the block for your harness into
your own clone. The git-level locks in `.githooks/` enforce the most irreversible rules regardless of
harness; these per-harness configs add the "which commands run" layer on top (defense in depth).

> Matcher/rule syntax is harness-version-specific — verify against your installed Codex / Claude Code
> version before relying on it. The *decisions* below are what matters; the exact spelling may drift.

## Codex — `~/.codex/rules/gxp-driven-dev.rules` (or repo `.codex/rules/`)

```python
# git push is paused until the git history is verified clean (see .githooks/pre-push).
prefix_rule(
    pattern = ["git", "push"],
    decision = "forbidden",
    justification = "History may name the source org; publish only via a clean-slate / orphan commit.",
)
prefix_rule(
    pattern = ["rm", "-rf"],
    decision = "forbidden",
    justification = "Use targeted deletes; rm -rf can hit files outside the repository.",
)
prefix_rule(
    pattern = ["python", "skills/_scripts"],
    decision = "allow",
    justification = "The deterministic gates are trusted and run constantly.",
)
```

## Claude Code — repo `.claude/settings.json`

```json
{
  "permissions": {
    "deny": [
      "Bash(git push:*)",
      "Bash(rm -rf:*)"
    ],
    "allow": [
      "Bash(python skills/_scripts/:*)",
      "Bash(sh .githooks/:*)"
    ]
  }
}
```

## Why these rules

- **`git push` forbidden** — the public push is paused; the git history is contaminated; publishing must
  be a clean-slate / orphan commit. `.githooks/pre-push` enforces the same at git level (defense in depth).
- **`rm -rf` forbidden** — the parent knowledge-base vault has no git (OneDrive-only history), so an
  accidental recursive delete is effectively irreversible.
- **`skills/_scripts/*` and `.githooks/*` allowed** — the trusted deterministic gates run constantly;
  no reason to prompt every time.
