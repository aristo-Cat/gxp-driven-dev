# examples/ — local agent rules (generated reference instances)

These are INSTANCES produced by the cascade — generated output, not hand-authored sources. The danger
is treating them as editable specs or letting a real instance leak identity. These rules ADD to the
root `CLAUDE.md`; they do not repeat it.

## Local invariants

- Examples are **generated output, NOT exempt** from anonymization — `anti-leak-guard.py` scans them.
  Keep them 100% anonymous (no org name, internal codes, site codes, or heritage terms).
- The instances are **drafts** (`status: draft`): IQ/OQ/PQ protocols are authored but NOT executed, so
  never declare fitness or release. A draft VR keeps `fitness_conclusion: pending-execution` until PQ runs.
- IDs and traceability come FROM the cascade skills — don't hand-edit requirement IDs. To change content,
  re-run the skill, then re-run the gates.
- `generate-rtm.py` WRITES `specs/RTM.md` here (a side effect). Running it mutates this dir — revert
  timestamp-only churn; don't commit a no-op RTM rewrite.
- `[NEEDS CLARIFICATION: …]` markers are EXPECTED in drafts. Validate with
  `check-clarification-markers.py --draft` (exits 0); a bare run exits 1 by design — that's not a failure.

## Known traps

- `temp-logger-gmp-chamber/` is the canonical reference instance; its shape (`.gxp-dev.yaml` + `IDEA.md`
  + `specs/`) is documented in `docs/project-layout.md`. Keep it consistent when regenerating.
- `bash.exe.stackdump` is a git-bash crash dump (git-ignored via `*.stackdump`). Never commit it; safe to
  delete locally.
