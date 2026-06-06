# Skills — `gxp-driven-dev`

This directory contains the AI-callable skills of `gxp-driven-dev`. Skills are how the toolkit's templates become **executable**: a skill takes a template + the consumer's manifest + (optionally) upstream approved specs as input, and produces a draft of a new spec, validation report, or other artifact.

Skills are **Claude Code first** (per Decision #10), with planned port to Cursor / Codex in `v0.5.0`. The Markdown + frontmatter format is deliberately runtime-agnostic — a thin adapter per host is all that's required. The `adapters/` directory holds the v0.5.0 adapter framework + a reference port (`urs-from-idea`) for Cursor (`.cursor/rules/*.mdc`) and Codex (`AGENTS.md` + prompt).

---

## Folder convention

```
skills/
├── README.md                       ← this file
├── _scripts/                       ← deterministic auxiliary scripts (Python 3.12+)
│   ├── requirements.txt            ← PyYAML>=6.0
│   ├── validate-frontmatter.py     ← validate spec frontmatter against template spec
│   ├── generate-rtm.py             ← derive RTM.md from specs/*.md
│   ├── check-clarification-markers.py  ← find [NEEDS CLARIFICATION:] markers
│   ├── lint-spec.py                ← combines the 3 above
│   └── lib/
│       └── gdd_common.py           ← shared helpers (parse frontmatter, walk specs)
├── start/                          ← zero-state front door (asks how to begin, routes)
├── urs-from-idea/                  ← one folder per skill (kebab-case, no prefix)
│   ├── SKILL.md                    ← Claude Code skill entry point
│   ├── interview-flow.md           ← (optional) interview question order
│   └── output-template.md          ← (optional) output shape reference
├── cs-from-fs/                     ← STUB until implemented
│   └── SKILL.md
└── …
```

### Rules

1. **One folder per skill**, named in kebab-case. The folder name (without prefix) is the skill's identifier.
2. **`SKILL.md`** is the entry point. Claude Code reads its frontmatter to discover the skill.
3. **Naming convention**: the slash command exposed to users is `/gdd.<skill-name-with-dots>`. Example: folder `urs-from-idea/` exposes `/gdd.urs.from-idea`.
4. **Auxiliary scripts** live in `_scripts/` (underscore prefix = not a skill folder). Skills invoke them via the `Bash` tool.
5. **Scripts are deterministic**. They handle YAML parsing, frontmatter validation, RTM generation, grep-based checks — work the LLM should not do because (a) LLM is non-deterministic, (b) wastes tokens, (c) cannot guarantee exhaustive coverage on large spec sets.
6. **Stub skills** carry a `SKILL.md` with frontmatter + `## Status: stub — not implemented yet` body. They allow Claude Code to list the skill as planned but immediately redirect to next-best-skill if invoked.

---

## Skill catalog

| Folder | Slash command | Status | Role |
|---|---|---|---|
| `start/` | `/gdd.start` | ⚡ Operative (v0.5.0) | **Zero-state front door**: detect manifest → ask how to begin → route to `/gdd.init` (build paths) or `/gdd.next` / `/gdd.lifecycle` (existing project). Read-only |
| `urs-from-idea/` | `/gdd.urs.from-idea` | ⚡ Operative (Sprint 2) | Interactive interview → `specs/URS.md` |
| `fs-from-urs/` | `/gdd.fs.from-urs` | ⚡ Operative (Sprint 2) | Functional Spec (GAMP 5 §D1) — realizes URS GxP=Y → `specs/FS.md` (full coverage) |
| `ra-from-urs/` | `/gdd.ra.from-urs` | ⚡ Operative (Sprint 2) | Initial Risk Assessment (GAMP 5 §M3 steps 1-2) → `specs/RA-INIT.md` |
| `ra-detail-from-urs-fs/` | `/gdd.ra.detail.from-urs-fs` | ⚡ Operative (Sprint 2) | Detailed RA / FMEA (GAMP §M3 step 3) — O×R×D→RPN on RA-INIT high-risk functions → `specs/RA-DET.md` |
| `tests-from-ra/` | `/gdd.tests.from-ra` | ⚡ Operative (Sprint 2) | IQ/OQ/PQ protocols (GAMP Table 4.1) — RA-DET RPN→test rigor → `specs/{IQ,OQ,PQ}.md` |
| `cs-from-fs/` | `/gdd.cs.from-fs` | ⚡ Operative (Sprint 2) | (Cat 4 only) Configuration Spec (GAMP §D3.3.1.1) — configured values per FS item → `specs/CS.md` |
| `trace-validate/` | `/gdd.trace.validate` | ⚡ Operative (v0.5.0) | Derive RTM, assert 0 dangling + anti-orphan check URS↔FS↔RA↔Tests |
| `lint-spec/` | `/gdd.lint.spec` | ⚡ Operative (v0.5.0) | Wraps `lint-spec.py`; frontmatter + markers + RTM gate; draft→in-review→approved promotion logic |
| `init-project/` | `/gdd.init` | ⚡ Operative (v0.5.0) | Bootstrap consumer: `.gxp-dev.yaml` + folders + STATE stub; F4-B Cat×mode soft warning |
| `next/` | `/gdd.next` | ⚡ Operative (v0.5.0, orchestrator) | Read-only router: scans specs → recommends next artifact + its skill |
| `lifecycle/` | `/gdd.lifecycle` | ⚡ Operative (v0.5.0, orchestrator) | V-Model overview + optional cascade orchestration (lint/trace gate between phases) |

---

## Auxiliary scripts (`_scripts/`)

All scripts target **Python 3.12+** with a single dependency: `PyYAML>=6.0`. Installation:

```bash
cd skills/_scripts
pip install -r requirements.txt
```

### `validate-frontmatter.py`

Parses the YAML frontmatter of a spec instance and verifies it against the template's declared `instance_frontmatter_spec`. Returns exit 0 if valid, non-zero with detailed error if not.

Usage:
```bash
python skills/_scripts/validate-frontmatter.py specs/URS.md
python skills/_scripts/validate-frontmatter.py --dry-run templates/csv/URS.md   # validates the template itself
```

### `generate-rtm.py`

Walks `specs/*.md` in the consumer project, extracts requirement IDs (`<DOC>-<CATEGORY>-<NNN>`), follows cross-references, and writes a derived `specs/RTM.md` with an upstream→downstream matrix.

Usage:
```bash
python skills/_scripts/generate-rtm.py
python skills/_scripts/generate-rtm.py --specs-dir specs --output specs/RTM.md
```

### `check-clarification-markers.py`

Greps for `[NEEDS CLARIFICATION:` markers across `specs/*.md`. Reports file, line number, and the clarification question. Used as a gate before promoting a spec from `draft` to `in-review`.

Usage:
```bash
python skills/_scripts/check-clarification-markers.py specs/URS.md
python skills/_scripts/check-clarification-markers.py --all     # scans specs/*.md
```

### `lint-spec.py`

Convenience wrapper. Runs `validate-frontmatter.py` + `check-clarification-markers.py` + `generate-rtm.py` (in dry-run mode) on a target. Useful for CI gates.

Usage:
```bash
python skills/_scripts/lint-spec.py specs/URS.md
python skills/_scripts/lint-spec.py --all
```

### `anti-leak-guard.py`

Enforces the **geographic anonymization rule** (CLAUDE.md). Greps the toolkit tree for banned identifiers (source organization name, corporate document codes, corporate ID schemes, site codes, non-English heritage terms) and exits non-zero on any leak. A small allowlist of governance/memory files (`CLAUDE.md`, `AGENTS.md`, `STATE.md`, `PROGRESS.md`, the guard itself) is permitted to name the rule. Run by the CI lint workflow as a blocking gate.

Usage:
```bash
python skills/_scripts/anti-leak-guard.py          # scan the toolkit root
python skills/_scripts/anti-leak-guard.py --quiet  # exit code only
```

### `lib/gdd_common.py`

Shared helpers. Not invoked directly; imported by the scripts above. Provides:
- `parse_frontmatter(path: Path) -> dict` — extract YAML block from a markdown file
- `find_active_templates(manifest: dict) -> list[str]` — read `templates_active` from `.gxp-dev.yaml`
- `walk_specs(specs_dir: Path) -> Iterator[Path]` — yield spec files in canonical order
- `extract_requirement_ids(content: str) -> set[str]` — regex-based ID extraction

---

## Anti-hallucination policies (applied to all skills)

Every skill MUST observe these rules:

1. **Never invent IDs.** Sequential numbering within each `<DOC>-<CATEGORY>` block. Read the highest existing N, then continue from N+1.
2. **Never invent regulatory citations.** Only cite what the source template already cites. If a new citation seems necessary, insert `[NEEDS CLARIFICATION: should we cite <citation> here?]` instead.
3. **Never invent package names.** When suggesting `npm install <pkg>` / `pip install <pkg>`, verify the package exists on the registry first (planned: `slopcheck` integration in Cat 0).
4. **Never invent architectural choices.** When the user hasn't decided architecture (web framework, database, etc.), insert `[NEEDS CLARIFICATION: …]` and stop.
5. **Read `.gxp-dev.yaml` first.** Skip skills should refuse to run if the manifest is missing or malformed; redirect to `/gdd.init`.
6. **Status transitions are linear.** `draft → in-review → approved → superseded`. Skipping requires explicit override + reason.

---

## Adding a new skill

(For contributors, post-`v0.5.0` when contribution opens.)

1. Create `skills/<skill-name>/SKILL.md` with frontmatter `name: gdd.<dot.separated.identifier>` and `description:` summarizing when to invoke.
2. If interview-driven, add `interview-flow.md` with question order + stop criteria.
3. If complex output, add `output-template.md` referencing the target template family.
4. If using new deterministic logic, add a script to `_scripts/` (Python 3.12+ stdlib + PyYAML).
5. Update this README's skill catalog.
6. Update `STATE.md` skills counter.
