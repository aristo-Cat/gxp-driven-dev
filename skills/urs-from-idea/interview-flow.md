# `gdd.urs.from-idea` — Interview Flow

Detailed question order, conditional sections, and stop criteria for the URS interactive instantiation skill. Referenced from `SKILL.md`.

---

## Conventions

- Ask **one question or one tight cluster at a time**. Wait for the user's reply before moving on. Lock each phase before advancing.
- After every cluster, do a 1-line **confirmation echo** ("Got it: system is X for Y") so the user can correct.
- If the user gives a partial answer, **probe gently** for the missing piece. Don't fill in the gap silently.
- If the user says "I don't know" or "skip" → insert `[NEEDS CLARIFICATION: …]` in the corresponding URS field and move on.
- **Track the running count per category** so you generate IDs sequentially without collisions.

### Interaction principles (adopted from `bm-prd-creator`, 2026-05-29)

These four principles govern *how* every question in this flow is posed. They reduce friction and produce better answers — see `docs/inspirations.md` → Framework 5.

1. **Propose a default with reasoning, then ask to confirm or change. Never ask an open-ended "what do you want?"** The user edits a proposal far better than they generate from a blank prompt. Example — instead of *"What's the response-time SLA?"* ask *"For a Cat 4 lab system I'd default the response-time SLA to ≤2s for interactive transactions and 99.5% uptime — does that fit, or do you have firm numbers?"* The **anti-hallucination check still applies**: a *proposed default the user confirms* is grounded; an *unconfirmed value you wrote into the URS* is invention. Always get the confirmation before it lands in a requirement.
2. **Use `AskUserQuestion` for discrete choices; free text only for open input.** GAMP category, priority (High/Med/Low), GxP (Y/N), mode, yes/no applicability → tappable options. Brain-dump of intended use, requirement wording, names → free text. The user may be on mobile; tappable beats typing.
3. **One decision (or tight cluster) at a time, in sequence.** Don't batch unrelated questions. This flow's phase order is the sequence — don't jump ahead.
4. **Adapt interview depth to the system.** A `rigor_level: light` Cat 1 utility needs a compressed pass; a `regulated` Cat 5 custom system expands every phase. The user's Phase 1 answers tell you which. If the user shows decision fatigue, offer *"use my recommended defaults for the rest of this phase"* and batch the low-stakes confirmations.

---

## Phase 1 — System identity (always)

**Goal**: fill the system identification table.

| Question | Placeholder filled |
|---|---|
| "What's the system's name?" | `system_name` |
| "Project ID? (matches `.gxp-dev.yaml` `project_id`)" | `project_id` (cross-check) |
| "Who's the supplier — vendor name, or 'in-house' if you're building it yourself?" | `supplier` |
| "Version of the supplier product? (use `n/a` if in-house, or current dev version)" | `version` |
| "In 1-3 sentences, what's the intended use? (regulatory framing — what does it do, for whom, with what consequences?)" | `intended_use` |
| If `profile == pharma` and `gamp_category` is unset: "What GAMP category — 1 infrastructure, 3 standard product, 4 configured, 5 custom?" | `gamp_category` |

**Echo**: *"Got it: <system_name> is a Cat <X> <supplier> system for <intended_use>. Continuing to scope…"*

---

## Phase 2 — Scope (always)

| Question | Placeholder filled |
|---|---|
| "Who are the end users? (groups, sites, departments)" | `end_user_group` |
| "What systems is this connected to (interfaces, integrations)? Describe each from the perspective of the receiving side." | `related_systems` |
| "What's the project purpose in 2-3 sentences?" | `project_purpose` |
| "Anything explicitly OUT of scope that you want to document?" | `out_of_scope` |

**Echo**: *"Scope locked: <project_purpose>. Out-of-scope: <out_of_scope or 'none stated'>. Moving to functional requirements…"*

---

## Phase 3 — Functional requirements (iterative)

For each functional requirement the user states (or that you prompt for from `intended_use`), produce one `URS-FUNC-NNN` row.

**Loop**:
1. Ask: "Tell me one functional requirement — what should the system DO?"
2. For the answer, derive:
   - **ID**: `URS-FUNC-001`, `URS-FUNC-002`, … sequential
   - **GxP**: ask "Is this GxP-relevant (Y/N)?" — if user unsure, mark `N` + clarification marker
   - **Prio**: ask "High (must-have), Medium, or Low (nice-to-have)?"
   - **Requirement text**: rephrase user's answer into a testable statement. Example: user says "fast"; you write "The system shall respond to interactive transactions in ≤2 seconds for 100 concurrent users".
3. Confirm: *"Added `URS-FUNC-NNN` — `<text>`. Another?"*
4. Stop when user says "no more" or you've collected ≥3 (for `rigor_level: light`) or ≥10 (for `regulated`) or you sense fatigue.

**Anti-hallucination check**: never write a requirement the user didn't state. If you need to flesh out detail, ask first.

---

## Phase 4 — Conditional Part 11 / Annex 11

If `presets.part11_active: true`:

> **Do NOT ask the user to draft Electronic Records / Electronic Signatures requirements.** They are pre-populated canonical content. Copy verbatim from `templates/csv/URS.md` lines that define `URS-EREC-001` through `URS-EREC-014` and `URS-ESIG-001` through `URS-ESIG-018`.

After copying:
- Ask: "Are any of these 32 Part 11 requirements (14 EREC + 18 ESIG) NOT applicable to your system? If so, which?"
- **Do NOT edit the preset rows themselves** — the legal text and its `GxP`/`Prio` cells stay **verbatim** (anti-hallucination rule #2). Editing the `GxP` cell would mutate the verbatim row.
- Instead, record applicability in a separate **"System-specific determinations"** note directly below the EREC/ESIG table. For each requirement the user marks N/A, add a line there: `<ID>: N/A — <user-provided reason>` (e.g. `URS-ESIG-018: N/A — no hybrid wet-ink signatures used`). For requirements that need a system-specific answer (e.g. EREC-011 closed/open, EREC-012 which records, ESIG-013 mechanism), record the answer in the same note.
- This preserves both the verbatim presets AND full traceability — no row is ever deleted or altered.

If `presets.part11_active: false`:
- Skip phase 4 entirely.
- Write a single sentence in section 9.2/9.3 of the URS: *"Not applicable — system is not 21 CFR Part 11 relevant per `.gxp-dev.yaml` configuration."*

If `presets.annex11_active: true`:
- After the Part 11 block (or in lieu of it), ensure `URS-SEC-NNN` and `URS-DATA-NNN` sections have explicit requirements anchored to Annex 11 §12 (User Access Mgmt) and §7 (Data integrity).

---

## Phase 5 — Performance + Quality + Deliverables

| Cluster | Questions |
|---|---|
| `URS-PERF` | "Response time SLA? Concurrent users? Uptime/availability? Data volume?" — derive ≥3 requirements |
| `URS-QUAL` | "Programming standards (if Mode B)? Test coverage threshold? Config management approach?" |
| `URS-DELIV` | "What deliverables does the supplier (or your team if Mode B) commit to? Code, docs, test results, user manuals?" |

For `mode: validate` (vendor product), `URS-DELIV` focuses on what the vendor must provide (FS, IQ scripts, SOC reports). For `mode: develop`, it focuses on what your team will produce.

---

## Phase 6 — Lifecycle support

| Cluster | Conditional |
|---|---|
| `URS-OPS` | Always. Ask: "Operational expectations — backup/recovery, monitoring, incident response, periodic review cadence?" — derive ≥2 requirements |
| `URS-ARCH` | Always. Ask: "Retention period for records? Archive media / strategy?" — derive ≥1 requirement |
| `URS-MIGR` | Only if user says they're migrating data from a legacy system. Ask: "What source system? What data formats? Cutover strategy?" — derive ≥2 requirements |

---

## Phase 7 — UI / API / Hardware

| Cluster | Conditional |
|---|---|
| `URS-UI` | If the system has a human interface. "Web UI? Desktop? Mobile? Accessibility standards (WCAG)? Browser support?" |
| `URS-API` | If the system exposes or consumes APIs. "REST/GraphQL/gRPC/SOAP/webhook? Authentication (OAuth2/API key/mTLS)? Versioning policy?" |
| `URS-HW` | If hardware constraints matter. "CPU/RAM/disk/network minimums? GPU? Specific platform requirements?" |
| `URS-PERIPH` | If peripherals are involved. "Scanners, printers, sensors, instruments connected to the system?" |

Skip clusters that don't apply.

---

## Phase 8 — Process / Training / Documentation

| Cluster | Questions |
|---|---|
| `URS-PROC` | "Are new SOPs needed? What roles are involved per GAMP §6.2.3 (Process Owner, System Owner, Quality Unit, SME)?" |
| `URS-TRAIN` | "Who needs training — devs, admins, end-users? On what topics?" |
| `URS-DOCS` | "What user-facing documentation is required — manuals, runbooks, FAQs?" |

---

## Phase 9 — Testing

`URS-TEST` requirements describe **test-specific constraints**, not the tests themselves. The actual test cases live in IQ/OQ/PQ specs later.

Ask:
- "Are there special test data requirements? (e.g. anonymized production data, synthetic datasets, edge cases)"
- "Load/stress test thresholds?"
- "Test environments needed (staging, UAT, validation)?"

Derive ≥2 requirements.

---

## Phase 10 — Dev environment (Mode B only)

If `mode != develop`, skip this phase entirely.

For `mode: develop`:
- "Programming language(s)?"
- "Build / package management (npm, pip, cargo, maven, etc.)?"
- "Source control + branching strategy?"
- "CI/CD platform (GitHub Actions, GitLab CI, Jenkins)?"
- "Code review tools (Pull Requests, Crucible, etc.)?"
- "Static analysis / linting (SAST, SonarQube, ESLint, ruff)?"

Derive `URS-DEVENV-NNN` requirements for each non-trivial choice.

---

## Phase 11 — Signature block

Always last. Ask:
- "Author — who's drafting this URS? (name + department)"
- "Reviewer 1 (Process Owner per GAMP §6.2.3) — name + department"
- "Reviewer 2 (SME) — name + department"
- "Approver 1 (System Owner) — name + department"
- "Approver 2 (Quality Unit) — name + department"

For each, if the user doesn't know, mark with `[NEEDS CLARIFICATION: assign <role>]`.

---

## Stop criteria — when URS is "complete enough to write"

You can write `specs/URS.md` (status: draft) when:

- [x] All `placeholders.required: true` are filled (no raw `{{...}}` in the output)
- [x] Phases 1, 2, 3, 11 completed
- [x] If `gamp_category == 5`: `URS-DEVENV`, `URS-QUAL`, `URS-TRAIN` have ≥3 requirements each
- [x] If `presets.part11_active`: 32 canonical Part 11 reqs copied (14 EREC + 18 ESIG) with applicability marked
- [x] If `mode: validate`: `URS-DELIV` is filled (vendor deliverables defined)
- [x] If `mode: develop`: Phase 10 completed (Dev env requirements present)
- [x] Signature block has ≥1 author + ≥1 reviewer + ≥1 approver designated (even if some are clarification markers)

Markers are OK in draft. They block status promotion to `in-review`, not the creation of the draft.

---

## What to do at the end

After writing `specs/URS.md`:

1. Run validation scripts (see SKILL.md "Post-flight" section).
2. Print a summary table: counts of requirements per category + total clarification markers.
3. Suggest the natural next step based on `mode` and `gamp_category`:
   - All flows → `/gdd.ra.from-urs` (Initial Risk Assessment — GAMP 5 §M3 step 1)
   - `gamp_category` 4 or 5 → `/gdd.fs.from-urs` after RA approval
   - Markers > 0 → `/gdd.clarify specs/URS.md` to resolve

Never claim the URS is "approved" or "validated" — that requires explicit human action.
