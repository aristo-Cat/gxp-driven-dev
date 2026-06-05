# adapters/ — local agent rules (ports to Cursor / Codex)

This folder re-expresses skills for other harnesses. The danger here is logic drift and vendor
lock-in leaking toward the core. These rules ADD to the root `CLAUDE.md`; they do not repeat it.

## Local invariants

- **Shared-core principle (load-bearing):** an adapter re-expresses ONLY the orchestration prose and
  **calls the same `skills/_scripts/*.py` by the same paths**. It NEVER re-implements RTM generation,
  frontmatter validation, or the anti-leak guard in a host-specific way. A bug fixed in the Python is
  fixed for every harness at once.
- **Source of truth is always `skills/<name>/SKILL.md`.** Adapters are REGENERATED from it, never
  hand-patched to diverge. If the source skill changes, regenerate the adapter — don't fork it.
- The Codex `AGENTS.snippet.md` guardrail block is **shared across all skills** — extend it, don't fork
  a copy per skill.
- If a future harness cannot shell out to Python, record a **porting blocker** — that is NOT a license
  to fork the logic into the host.
- Vendor-specific behavior lives ONLY here. Never let a single-vendor feature leak into core
  `templates/` or `skills/` (Anti-goal #1: AI-agnosticism).

## Known traps

- Only `gdd.urs.from-idea` is actually ported; the other 5 skills are **planned** in the status matrix.
  Don't present a planned row as done — flip the matrix row only when the files exist AND the gate passed.
- Cursor ports are **Manual** rules: `alwaysApply: false`, no `globs`. Don't make them Always or
  glob-attached.
- Adapter files emit script paths via a `<gdd-path>` placeholder (the `toolkit_path` resolver is
  backlog) — don't hardcode an absolute local path.
- Adapters live inside the tree, so `anti-leak-guard.py` scans them too — run it after any port.
