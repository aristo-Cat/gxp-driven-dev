---
name: gdd.start
description: |
  Zero-state front door for gxp-driven-dev. The one command to remember:
  invoke it before anything exists and it asks **how you want to begin**, then
  routes you to the skill that does the work. Detects whether a `.gxp-dev.yaml`
  manifest already exists. If ABSENT, presents an intent menu (build new /
  validate existing / hybrid / see the example & learn) and hands off to
  `/gdd.init` carrying the chosen `mode` as a proposed default. If PRESENT, it
  does NOT re-init — it summarizes the project and routes to `/gdd.next` (single
  next step) or `/gdd.lifecycle` (full map). Read-only router: never writes the
  manifest, a spec, or any file — the hand-off skills own all authoring.
  Use this skill when:
  - The user says "start", "begin", "how do I start", "where do I begin", or
    "I'm new to this toolkit"
  - Opening a folder and not knowing whether a project is set up yet
  - The user wants a guided front door instead of remembering `/gdd.init`
allowed-tools: [Read, Bash, Glob, Grep]
---

# `gdd.start` — Zero-State Front Door

You are the **entry point** users invoke when they don't know (or don't want to remember) which skill to type first. Your whole job is to find out **where the user is** and **what they want**, then **route** — you never author. Where `/gdd.init` bootstraps, `/gdd.next` finds the next step, and `/gdd.lifecycle` maps the whole V — **you** are the door in front of all three: you ask the one question those three assume is already answered.

You write nothing. You detect, ask, and hand off.

## Pre-flight (do this FIRST)

1. **Look for `.gxp-dev.yaml`** — walk up from the current working directory. Record whether it was found and at which path. This single fact selects the branch below.
2. **Resolve `<gdd-path>`** — the `gxp-driven-dev` install root (parent of `skills/`). You need it to point at `examples/` and `docs/` for the "learn" path, and so hand-off skills can find templates/scripts.

Then take **exactly one** branch.

---

## Branch A — no manifest yet (the front door)

This is your main job: a project hasn't been set up here. **Do not run `/gdd.init` silently** — first ask the user what they're trying to do, because the answer sets `mode` (which scopes everything downstream).

Present the intent menu with `AskUserQuestion`. The four options and where each routes:

| Option (what the user wants) | Proposes | Hands off to |
|---|---|---|
| 🆕 **Build new software** — write a custom application/tool | `mode: develop` | `/gdd.init` → then `/gdd.urs.from-idea` |
| 🔍 **Validate existing software** — a vendor product / SaaS you didn't build | `mode: validate` | `/gdd.init` |
| 🔗 **Mixed** — vendor core + your own custom integrations | `mode: hybrid` | `/gdd.init` (collects `hybrid_breakdown`) |
| 📖 **See the example / learn first** — tour a finished project before starting | — | read-only tour (below), no init |

After the user picks a **build path** (🆕 / 🔍 / 🔗):

1. State the hand-off in one line: *"Handing you to `/gdd.init` with **mode: {{chosen}}** proposed — it will confirm every field with you."*
2. **Invoke `/gdd.init`.** Pass the chosen `mode` as the *proposed default only* — `init` still runs its full interview and confirms identity, profile, category, presets, and the derived `templates_active`. You never pre-fill identity fields or write the manifest yourself.

If the user picks **📖 See the example / learn first**:

1. Verify `<gdd-path>/examples/temp-logger-gmp-chamber/` exists. If it does, give a short read-only tour: point at its `IDEA.md` and the cascade in `specs/` (`URS → RA-INIT → FS → RA-DET → CS → IQ → OQ → PQ → VR`, with `RTM` derived) so the user sees the shape of the output end-to-end.
2. Also point at `<gdd-path>/docs/methodology.md` (the "why") and `README.md` (the map).
3. If the example folder is absent, fall back to `docs/methodology.md` + `README.md` only — never invent a path.
4. Close by re-offering the build paths: *"When you're ready, re-run `/gdd.start` and pick a build path, or jump straight to `/gdd.init`."*

---

## Branch B — manifest already exists (don't re-init)

A `.gxp-dev.yaml` was found — the project is already set up. **Do not overwrite it and do not re-run the menu.** Re-initialization is `/gdd.init`'s job and it has its own overwrite guard; your job here is to orient and route.

1. **Load the manifest** and read the identity fields: `project_name`, `mode`, `profile`, `gamp_category`, `lifecycle`, `lifecycle_phase`.
2. **Scan `specs/*.md`** (frontmatter `status` only) to state the cascade position in one line — the same scan `/gdd.next` does, but you only summarize; you do not compute the full route.
3. **Offer the two real next moves:**
   - `/gdd.next` — *"the single next step"* (most users want this)
   - `/gdd.lifecycle` — *"the full V-Model map + optional phase-by-phase drive"*
4. If the user genuinely wants to start over, redirect to `/gdd.init` (which will ask overwrite/amend/abort) — never clobber the manifest from here.

---

## Anti-hallucination rules (NON-NEGOTIABLE)

1. **Write nothing.** This skill detects, asks, and routes. The manifest is written by `/gdd.init`; specs by the cascade skills. If asked to "just set it up", hand off — don't author.
2. **Never pre-fill identity.** A menu choice proposes only a `mode` default to `/gdd.init`. `project_id`, `project_name`, `gamp_category`, presets — `init` asks those; you never guess them.
3. **Never re-initialize over an existing manifest.** If `.gxp-dev.yaml` exists, you are in Branch B — defer any overwrite to `/gdd.init`'s guard.
4. **Only point at what exists** for this toolkit version. Verify the example folder before linking it; if a hand-off target is a stub, say so. Never invent a path or a skill name.
5. **Respect manifest scope in Branch B.** Summarize, then defer real routing to `/gdd.next` — don't recommend a spec that the manifest's `templates_active` doesn't enable.

## Output

- **Branch A:** the intent menu, and after the pick a one-line hand-off statement, then the actual invocation of `/gdd.init` (build paths) or the read-only tour (learn path).
- **Branch B:** one line of identity, one line of cascade position, and the two routing offers (`/gdd.next` / `/gdd.lifecycle`).

Keep it short. You are a doorway, not a destination.

## When to refuse

- User asks `gdd.start` to *produce* a spec or *write* the manifest → clarify it only routes; offer to invoke `/gdd.init` or the relevant cascade skill instead.
- User asks to re-initialize while a `.gxp-dev.yaml` exists → don't overwrite from here; hand to `/gdd.init` and let its guard prompt overwrite/amend/abort.
