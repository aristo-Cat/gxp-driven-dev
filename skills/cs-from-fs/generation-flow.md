# `gdd.cs.from-fs` — Generation Flow

Detailed step order, the by-area organization, the citation gate, stop criteria, and interaction principles for the CS instantiation skill. Referenced from `SKILL.md`.

---

## Conventions

- Work **area by area** (§3.1 → §3.5); lock each before the next.
- After each area, echo coverage ("Security: 7 config items documented").
- If a concrete value is not decided → `[NEEDS CLARIFICATION: define <X>]`; never invent it.

### Interaction principles (adopted from `bm-prd-creator` — see `docs/inspirations.md` Framework 5)

1. **Propose a configured value with reasoning, then confirm.** For each config item, propose the value with the *why*, and let the user correct. A **confirmed value is grounded**; an **unconfirmed value you write into the CS is invention** (anti-hallucination rule #1). Example — *"For the alarm band I'd configure lower 2.0 °C / upper 8.0 °C (the GMP cold-storage range). Confirm, or is your range different?"*
2. **Use `AskUserQuestion`** for discrete config choices (a value from a known set, `lives_in_tool` yes/no, custom-code present yes/no). Free text for parameter descriptions/justifications.
3. **One area (or tight cluster) at a time.** Don't dump the whole config in one prompt.
4. **Adapt depth to risk.** Config items that mitigate high-RPN RA-DET risks get explicit values + justification (cite the `RA-DET-NNN`); routine settings can be concise.

---

## Flow

### 1. Identify the configurable items
From `specs/FS.md`, select the `FS-<CAT>-NNN` items that have a **concrete configurable setting** (threshold, interval, role mapping, endpoint, encryption parameter, schedule, template…). **Do not mirror every FS-ID** — only those that are actually configured. Cross-check RA-DET: every config item a high-RPN mitigation relies on must be included.

### 2. Document each config item
For each, produce a `CS-<CATEGORY>-NNN` row in the right area table:
- **Configures** — the `FS-<CAT>-NNN` it implements.
- **Setting / Parameter** — what is being set.
- **Configured value** — the concrete value (or `[NEEDS CLARIFICATION:]` if undecided).
- **Justification** — why this value; cite the `RA-DET-NNN` if it realizes a risk mitigation, or the URS/regulatory anchor.

### 3. Organize by area (the template's §3.1-3.5)
- **§3.1 Workflows and business rules** — `CS-FUNC-NNN` / `CS-PROC-NNN` (intervals, alarm bands, notification rules, report generation).
- **§3.2 Security, roles and signatures** — `CS-SEC-NNN` / `CS-ESIG-NNN` (role-permission matrix, encryption, MFA, password policy, signature manifestation, tamper-evidence).
- **§3.3 Integrations / interfaces** — `CS-API-NNN` (endpoints, payload mappings, retry).
- **§3.4 Audit trail / records** — `CS-EREC-NNN` (audit-trail scope/fields, reason prompt, review workflow).
- **§3.5 Other** — `CS-DATA/FLOW/REPORT/OPS/PERIPH-NNN` (retention, buffer, report template, backup schedule, recalibration interval).

### 4. Configuration dependencies (§4)
List config items that depend on external systems (corporate IdP for MFA, messaging gateway for notifications, key store/HSM for encryption).

### 5. Custom code (§5)
List any macro/script/custom code as **Cat 5 → DS** (cross-reference only). If none, state "None — pure configured COTS; no custom code." If the platform requires substantial custom code, flag that the system may not be a pure Cat 4.

---

## Citation gate (the core check)

Before claiming complete: **every `CS-<CAT>-NNN`'s "Configures" must cite an `FS-<CAT>-NNN` that exists in `specs/FS.md`.** A CS item with no upstream FS item is an orphan (either the FS is incomplete or the config item is invented).

---

## Stop criteria ("complete enough to write")

- [ ] `gamp_category == 4` confirmed (else refused in pre-flight)
- [ ] `traces_to` points to the FS (warn if not `approved`)
- [ ] Every configurable FS item has a `CS-<CAT>-NNN` with a value (or a clarification marker)
- [ ] Every CS row cites its FS-ID; high-RPN mitigations cite the RA-DET-NNN
- [ ] §5 custom-code resolved (none, or flagged Cat 5 → DS)
- [ ] Author + SME/System Owner/Quality Unit designated — markers OK in draft

---

## What to do at the end

1. Write `specs/CS.md` (`status: draft`) per `output-template.md`.
2. Run post-flight (see `SKILL.md`): validate-frontmatter, markers `--draft`, generate-rtm, **citation check**.
3. Print config-item count by area, # `[NEEDS CLARIFICATION]` values, custom-code flag.
4. Suggest `/gdd.tests.from-ra` (IQ verifies the config baseline; OQ verifies it works).
5. Never claim the CS is "approved" — it configures an approved FS and needs its own signatures; keep it in sync with the live config.
