# skills/_scripts/ — local agent rules (executable enforcement code)

This folder runs code and holds the anti-leak overlay — higher risk than the rest of the repo.
These rules ADD to the root `CLAUDE.md`; they do not repeat it.

## Local security limits

- NEVER commit `.leak-overlay.txt` — it holds the real organization-specific terms (it is
  git-ignored; keep it that way). Never paste its contents into output, commit messages, or other files.
- Keep `anti-leak-guard.py` a GENERIC engine: organization-specific terms live only in the overlay
  or the `LEAK_OVERLAY` env var, never hard-coded here.
- The guard scans the working tree, NOT git history — "0 leaks" does not mean history is clean.
- Scripts are Python 3.12+, standard library + PyYAML only, and make no network calls.

## Known traps

- These scripts are the deterministic CI gates (`validate-frontmatter`, `generate-rtm`, `lint-spec`,
  `check-clarification-markers`, `anti-leak-guard`). Never change their pass/fail semantics just to
  make a check go green.
- `generate-rtm.py` WRITES `RTM.md` (a side effect) — running it mutates the target `specs/` dir;
  revert timestamp-only churn.
- `lib/gdd_common.py` `REQUIREMENT_ID_RE` mis-segments multi-part DOC-TYPEs (e.g. `RA-INIT` → category
  `INIT`); `NON_CATEGORY_MIDDLES` guards against phantom categories. Keep that guard when touching ID parsing.
