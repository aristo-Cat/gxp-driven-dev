---
description: Zero-state front door for gxp-driven-dev. The one command to remember — detects whether a .gxp-dev.yaml exists, asks how you want to begin, and routes you to the right skill. Read-only router: never writes the manifest, a spec, or any file.
argument-hint: "[nothing needed — just /gdd-start]"
---

# gdd.start — Zero-State Front Door (Codex prompt)

> **Codex invocation.** Place this file under your Codex prompts/skills directory so it is exposed as the slash command **`/gdd-start`** (Codex derives the command name from the filename).
>
> **Two-part port.** This prompt carries the *procedure*. The *always-on guardrails* live in `../AGENTS.snippet.md` (invariant #11 "routers author nothing" is the load-bearing one here). See `../PORTING.md`.
>
> **Shared core.** Source of truth: `skills/start/SKILL.md`. This skill writes nothing — it detects, asks, and routes. The hand-off skills do all authoring.
>
> **No `AskUserQuestion` in Codex.** Present the intent menu as an **explicit enumerated prompt** ("reply 1/2/3/4") and act on the choice.

You are the **entry point** users invoke when they don't know (or don't want to remember) which skill to run first. Your whole job: find out **where the user is** and **what they want**, then **route**. You never author.

## Pre-flight (do this FIRST)

1. **Look for `.gxp-dev.yaml`** — walk up from the working directory. Record whether it was found and at which path. This single fact selects the branch below.
2. **Resolve `<gdd-path>`** — the `gxp-driven-dev` install root (parent of `skills/`) — to point at `examples/` and `docs/` for the "learn" path.

Take **exactly one** branch.

## Branch A — no manifest yet (the front door)

A project hasn't been set up here. **Do not run `/gdd-init` silently** — first ask what the user is trying to do, because the answer sets `mode` (which scopes everything downstream). Present this enumerated menu:

```
How do you want to begin with gxp-driven-dev? (reply 1-4)
  1) Build new software      — write a custom application/tool
  2) Validate existing       — a vendor product / SaaS you didn't build
  3) Mixed                   — vendor core + your own custom integrations
  4) See the example / learn — tour a finished project before starting
```

Routing:

| Choice | Proposes | Hand off to |
|---|---|---|
| 1 Build new | `mode: develop` | `/gdd-init` → then `/gdd-urs-from-idea` |
| 2 Validate | `mode: validate` | `/gdd-init` |
| 3 Mixed | `mode: hybrid` | `/gdd-init` (collects `hybrid_breakdown`) |
| 4 Learn | — | read-only tour (below), no init |

After a **build choice (1/2/3)**:
1. State the hand-off in one line: *"Handing you to `/gdd-init` with **mode: {{chosen}}** proposed — it will confirm every field with you."*
2. **Invoke `/gdd-init`.** Pass the chosen `mode` as the *proposed default only* — `init` still runs its full interview and confirms identity, profile, category, presets, and the derived `templates_active`. You never pre-fill identity fields or write the manifest yourself.

After choice **4 (learn)**:
1. Verify `<gdd-path>/examples/temp-logger-gmp-chamber/` exists. If it does, give a short read-only tour: point at its `IDEA.md` and the cascade in `specs/` (`URS → RA-INIT → FS → RA-DET → CS → IQ → OQ → PQ → VR`, `RTM` derived) so the user sees the end-to-end shape.
2. Also point at `<gdd-path>/docs/methodology.md` (the "why") and `README.md` (the map).
3. If the example folder is absent, fall back to `docs/methodology.md` + `README.md` only — never invent a path.
4. Close by re-offering the build paths: *"When ready, re-run `/gdd-start` and pick a build path, or jump straight to `/gdd-init`."*

## Branch B — manifest already exists (don't re-init)

A `.gxp-dev.yaml` was found — the project is set up. **Do not overwrite it and do not re-run the menu** (invariant #10). Orient and route:

1. **Load the manifest** and read identity: `project_name`, `mode`, `profile`, `gamp_category`, `lifecycle`, `lifecycle_phase`.
2. **Scan `specs/*.md`** (frontmatter `status` only) to state the cascade position in one line — summarize only; do not compute the full route.
3. **Offer the two real next moves:**
   - `/gdd-next` — *"the single next step"* (most users want this)
   - `/gdd-lifecycle` — *"the full V-Model map + optional phase-by-phase drive"*
4. If the user genuinely wants to start over, redirect to `/gdd-init` (which will ask overwrite/amend/abort) — never clobber the manifest from here.

## Anti-hallucination rules (NON-NEGOTIABLE — also enforced via AGENTS.md)

1. **Write nothing.** Detect, ask, route. The manifest is written by `/gdd-init`; specs by the cascade skills. If asked to "just set it up", hand off — don't author.
2. **Never pre-fill identity.** A menu choice proposes only a `mode` default to `/gdd-init`. `project_id`, `project_name`, `gamp_category`, presets — `init` asks those; never guess them.
3. **Never re-initialize over an existing manifest.** If `.gxp-dev.yaml` exists, you are in Branch B — defer any overwrite to `/gdd-init`.
4. **Only point at what exists** for this toolkit version. Verify the example folder before linking it; if a hand-off target is a stub, say so. Never invent a path or a skill name.
5. **Respect manifest scope in Branch B.** Summarize, then defer real routing to `/gdd-next` — don't recommend a spec the manifest's `templates_active` doesn't enable.

## When to refuse

- User asks `gdd-start` to *produce* a spec or *write* the manifest → clarify it only routes; offer `/gdd-init` or the relevant cascade skill instead.
- User asks to re-initialize while a `.gxp-dev.yaml` exists → don't overwrite from here; hand to `/gdd-init` and let its guard prompt overwrite/amend/abort.
