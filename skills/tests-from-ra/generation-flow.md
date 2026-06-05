# `gdd.tests.from-ra` — Generation Flow

Per-protocol step order, the coverage gates, stop criteria, and interaction principles for the IQ/OQ/PQ instantiation skill. Referenced from `SKILL.md`. Generate in V-Model order: **IQ → OQ → PQ**.

---

## Conventions

- Author **protocols**, not results: fill test steps + expected results; leave "Actual result" / pass columns blank for execution.
- After each protocol, echo coverage ("OQ: 4/4 high-RPN functions have positive+negative").
- Missing environment/baseline/tester info → `[NEEDS CLARIFICATION: …]`; never fabricate.

### Interaction principles (adopted from `bm-prd-creator` — see `docs/inspirations.md` Framework 5)

1. **Propose each test step with reasoning, then confirm.** Propose the verification step + expected result with the *why*, and let the user adjust. A **confirmed expected-result is grounded**; an **invented one is hallucination**. Example — *"For the unauthorized-threshold-change negative test I'd expect: action denied + attempt logged in the audit trail. Agree?"*
2. **Use `AskUserQuestion`** for discrete choices (which special test types to activate; whether a low-risk function is tested or risk-accepted). Free text for step/expected-result descriptions.
3. **One protocol (or one test case) at a time.** Don't dump all three protocols in one prompt.
4. **Adapt depth to RPN / Risk Priority.** High-RPN functions get the most test detail (positive + negative + stress); low-risk get GEP / risk-acceptance.

---

## IQ — Installation Qualification

1. **Parse install/config items** from CS (Cat 4) / DS (Cat 5) + FS: product version, hardware, configuration baseline values, connectivity/interfaces, security settings, documentation.
2. **For each item** → ≥1 `IQ-TC-NNN`: cite the CS/FS-ID (+ RA-INIT-NNN if it ties to a risk), the verification step, and the expected result (baseline value from the CS).
3. **Scale rigor** by RA-INIT Risk Priority (H exhaustive / M sampling / L basic).
4. **Sections** (template): §3.2 prerequisites, §5.2 equipment, §5.3 components, §5.4 config baseline (against CS), §5.5 connectivity/interfaces/security, §5.6 documentation.
5. IQ is the **prerequisite of the OQ** — note it.

## OQ — Operational Qualification (the RPN bridge)

1. **Parse GxP `FS-<CAT>-NNN`** from the FS with their Risk Priority (from RA-INIT) and RPN (from RA-DET).
2. **Per function, apply the RPN→rigor rule**:
   - **RPN ≥ 12** → a **positive** test case AND a **negative** test case (both cite the same `RA-INIT-NNN`). Add stress where the failure mode is performance/resilience.
   - **RPN 6-9** → positive test.
   - **RPN 1-4** → GEP / risk-accepted (documented).
3. **Negative-test attribution (TF2)**: when the negative/resilience test exercises the *mitigation's* FS-ID, cite **both** FS-IDs on the row, and reflect that in §6 — so "every Priority-H function has pos+neg" holds.
4. **Activate special test types** per active URS presets: audit-trail (EREC), e-signature incl. tamper-negative (ESIG), access/MFA negative (SEC), interface + failure/retry (API).
5. **§6 functional coverage table** must agree with the OQ-TC "Verifies" cells; low-risk untested functions are listed as **risk-accepted** (GAMP 5 §D5), never claimed as covered.

## PQ — Performance Qualification (end-to-end)

1. **Parse URS `URS-<CAT>-NNN` with prio=H** from the URS.
2. **Group them into end-to-end business processes** (not isolated functions) → each group becomes one `PQ-SCEN-NNN` with: the URS-IDs it covers, the RA-INIT-NNN risk, the **end-user role** that executes it, and the process steps.
3. **Scale depth** by Risk Priority (H full scenario + boundary + realistic volume).
4. **§8 statement of fitness** (GAMP 5 §M7): write the formal declaration template with the intended-use from the URS, left unmarked (decided at execution).
5. PQ is executed by **end users**, not IT; environment is **production-like**.

---

## Coverage gates (run before claiming complete)

- **OQ**: every GxP FS-ID with Risk Priority=H (RA-DET RPN≥12) has **both** a positive and a negative OQ-TC (cross-check §6 vs the OQ-TC rows).
- **PQ**: every URS-ID with prio=H is covered by ≥1 PQ-SCEN (or risk-accepted with rationale).
- **IQ**: every CS/FS install item has ≥1 IQ-TC.
- **Traceability**: each test ID cites its source spec ID (IQ-TC→CS/FS; OQ-TC→FS+RA-INIT; PQ-SCEN→URS+RA-INIT).

---

## Stop criteria ("complete enough to write")

- [ ] IQ/OQ/PQ all at `status: draft` with "Actual result" columns blank
- [ ] OQ: all RPN≥12 functions have positive + negative; special test types active per presets
- [ ] PQ: all URS prio=H covered end-to-end; §8 statement-of-fitness present (unmarked)
- [ ] IQ: all install/config items covered; prerequisite-of-OQ noted
- [ ] Risk-accepted functions documented (no false total coverage)
- [ ] Tester ≠ Reviewer; PQ end-users designated (markers OK in draft)

---

## What to do at the end

1. Write `specs/IQ.md`, `specs/OQ.md`, `specs/PQ.md` (`status: draft`) per `output-template.md`.
2. Run post-flight (see `SKILL.md`): validate-frontmatter ×3, markers `--draft`, generate-rtm, coverage checks.
3. Print IQ-TC / OQ-TC / PQ-SCEN counts, the high-RPN pos+neg list, risk-accepted functions.
4. Suggest `/gdd.vr.from-tests` (Validation Report — consumes the protocol summaries + the PQ fitness statement).
5. Never claim a protocol is "executed" or "approved" — those need real execution + signatures.
