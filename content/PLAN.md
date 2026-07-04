# PureMed Content Pipeline — Plan

**Goal:** Publish to Facebook + Instagram every 2 days (~15 posts/month) for PureMed Aesthetics, with a deterministic agentic pipeline from ideation to publication. PureMed is the pilot; the core is built client-agnostic so future MSS clients are a config directory, not a rebuild.

**Status:** Approved 3 Jul 2026; Phase 1 built same day (config, August calendar, batch 1, preview, sync). Phase 2 blocked on Meta prerequisites. Locked decisions live in `.claude/puremed-decisions-log.md`.

---

## Design principles

1. **Deterministic means state-machine, not improvisation.** Agents generate content; scripts move it. Every post is a directory of files with an explicit state. Agents are invoked at fixed stages with schema-validated inputs and outputs. No agent ever decides *whether* to publish — only humans and cron do.
2. **Git is the audit trail.** Same as Loop 2: every generated batch is a branch, every approval is a synced decision file, every published post records its platform post ID. Nothing is ephemeral.
3. **Nafisa approves everything before it goes live.** This is non-negotiable for a medical aesthetics client (see Compliance). The approval surface is Stage — she already knows it.
4. **Scale-ready, not scale-built.** Client-agnostic scripts + per-client config from day one (cheap to do now, expensive to retrofit). But no multi-tenant dashboard, no queue infrastructure, no per-client Meta app automation until client #2 exists. Rationale below.

---

## Post lifecycle (the state machine)

```
idea → drafted → review → approved → scheduled → published → measured
                    ↘ flagged (needs change) → drafted (regenerate)
                    ↘ rejected (dropped from calendar)
```

Each post lives at `content/posts/<date>-<slug>/`:

```
post.json      — state, pillar, format (static | carousel), platforms, target date/time,
                 assets (static: one image; carousel: ordered image/text slides),
                 platform post IDs once live
copy.md        — IG caption + FB caption (they differ: hashtags, length, link handling)
assets/        — final image(s), WebP + platform-sized
brief.md       — the generation brief (audit: why this post exists, which pillar/calendar slot)
```

Posts can carry a **brand overlay** (`brandOverlay: true`, default from `config/client.json → branding`): the client's logo mark in a configurable corner of photo slides and static images (text slides are already brand cards). Preview renders it as CSS; **the Phase 2 publisher must bake the mark into the exported files** (sharp composite) so what publishes matches what was approved. PureMed uses `puremed_logo_cropped.webp` — the `_transparent` variant is a huge padded canvas that renders invisibly small at overlay scale.

Every post is **static** (single image) or **carousel** (ordered slides). The format is chosen per calendar slot so Nafisa approves it with the topic. Carousel text slides live in `post.json` as structured `{kicker, headline, body, style?, bg?, numeral?}` entries following the **slide design system** (creative-director pass, 3 Jul): photo covers (image bg + blue gradient overlay), light content slides (gold hairline frame + oversized serif numerals for steps), blue gradient CTA closers — every text slide carries the PUREMED AESTHETICS footer. **Image library**: `config/image-library.json` catalogues ~320 tagged on-brand images (scenario banks, Nafisa portraits, skin close-ups, treatment heroes; before/after files excluded per compliance) — all synced to the Stage engagement assets and browsable in the admin Asset Curation grid — rendered as brand-styled cards in the preview, linted word-for-word by `content-lint.js`, and produced as sized images at publish time (Phase 2: render the same card template to PNG; both FB and IG Graph API support multi-image carousels).

`content/state.json` is the pipeline index — one entry per post, state + timestamps. Scripts operate on this file; it's the single source of truth for "what needs doing."

---

## The five stages

### Stage 0 — Client config (one-time per client, human-authored)

`content/config/`:
- `client.json` — cadence (every 2 days), platforms, posting time, timezone, Meta page/IG account IDs, asset-hosting base URL
- `voice.md` — PureMed tone of voice (feeds the copywriting skill)
- `pillars.md` — content pillars with target mix, e.g. treatment education 40%, myth-busting 20%, clinic/practitioner trust 20%, patient journey/aftercare 10%, seasonal/offers 10%
- `compliance.md` — **hard rules, human-written, never generated.** For PureMed (UK medical aesthetics) this includes at minimum:
  - **Never name or promote prescription-only medicines to the public** — "Botox"/botulinum toxin brand names cannot be advertised under CAP/ASA rules. Posts talk about "consultations for wrinkle concerns", not the POM.
  - Before/after imagery restrictions (Meta policy + ASA sensitivity), no exaggerated claims, no "guaranteed results", mandatory "results vary" framing, no targeting/appeal to under-18s.
  - Every claim must be attributable to the treatment page copy Nafisa has already approved on the site.

This file is *why* the pipeline can't be fully autonomous for this vertical, and it's per-client by design.

### Stage 1 — Ideation (monthly, agent-generated, human-approved)

Script: `content-calendar.js --client puremed --month 2026-08`

- Agent reads pillars + compliance + treatments page copy + previous month's `metrics.json` (once it exists) and generates `content/calendar/2026-08.json`: 15 slots, each with date, pillar, treatment focus, hook, and a one-line brief. Deterministic slot dates (every 2 days from config), rotation constraint (no treatment twice in a row), seasonal hooks.
- Calendar goes to Nafisa for approval **as a batch** (same Stage mechanism as Stage 3 below, rendered as a simple table page). One approval covers the month's *topics* — she's not surprised by anything later.

### Stage 2 — Creation (per batch, agent-generated)

Script: `content-generate.js --client puremed --batch <week>` — generates the next 3–4 posts from approved calendar slots.

- **Copy:** copywriting skill + `voice.md` + the slot brief → `copy.md` with IG and FB variants. Two gates before a post reaches `drafted`: (1) the **humanise pass** in voice.md — read aloud, kill AI tells (em dashes banned outright, no "isn't just X, it's Y", varied rhythm, contractions); (2) the compliance checklist against `compliance.md`. Then `content-lint.js` enforces the mechanical subset of both — POM terms, claims, urgency, **and em dashes / AI-tell phrases as blocking errors** — so the deterministic layer catches what the agent misses.
- **Visuals:** higgsfield-scene-generation skill per post, grounded in PureMed brand constraints; output compressed to WebP, sized 1080×1350 (IG portrait) with 1080×1080 fallback. Existing clinic photography (the `assets/web/` set) is preferred where it fits — generated imagery is the fallback, and **no generated imagery may depict treatment results** (compliance).
- Output committed on branch `content/<batch-date>`.

### Stage 2b — Image requests (admin, via Stage)

Stage admin has an **Image Requests** tab per engagement: a request (target + direction note) is queued to `engagements/<id>/output/asset-requests.json`. The studio pipeline drains the queue (`scripts/content-requests.js` — list/claim/resolve over SSH, host configurable for the eventual Cloudways move); generation itself always runs through the Higgsfield skills with brand grounding, results land in the engagement assets and show as thumbnails on the request. Deliberately NOT direct generation from the Stage host: no API keys or spend on the review box, and prompt quality depends on brand docs that live studio-side.

### Stage 3 — Review & approval (Nafisa, via Stage)

This is the key reuse: **render the batch as a feed-preview HTML page and push it to Stage as a `puremed-content` engagement.** Each post is a block with a `data-stage-id` (`post-2026-08-05`), showing the image, both captions, and the scheduled date — styled like an IG feed so she sees what followers see.

- Nafisa uses the existing approve / request-change / flag mechanics per post. Zero new client-facing UX to build or teach.
- The admin can also **edit copy directly in Stage** (admin Copy tab): edits store in an `admin-copy.json` overlay, become the baseline everyone sees, and `content-sync.js` pulls them back into the source `copy.md` (post returns to `drafted`; run the lint and re-push the preview after).
- A thin adapter on the Loop 2 pattern (`content-sync.js`, sharing mss-loop2's fetch/normalise code) pulls the decisions back: approved → state `approved`; changed → regenerate with her note as an additional brief constraint; flagged → hold.

### Stage 4 — Scheduling & publication (cron, fully deterministic)

Script: `content-publish.js --client puremed`, run by cron (on the Pi, same host as Stage — it's already always-on and already serves public URLs).

- Every run: read `state.json`, find posts in `approved` whose target datetime has passed, publish, record post IDs, set state `published`. Idempotent — a post with a recorded ID is never re-sent. Failures set state `publish-failed` and notify (PushNotification / email), never retry silently more than N times.
- **Publishing route: Meta Graph API direct** (recommended — see Decision 1):
  - FB Page: `POST /{page-id}/photos` with caption.
  - IG: `POST /{ig-user-id}/media` (container, `image_url` must be a public URL — served from the Pi at `mss-review.duckdns.org/content-assets/...` or from Cloudways) → `POST /{ig-user-id}/media_publish`.
  - Auth: Meta Business Manager **system user token** (non-expiring) with `pages_manage_posts` + `instagram_content_publish`. Nafisa's IG must be a Business/Creator account linked to the FB Page; MSS gets partner/agency access via Business Manager.

### Stage 5 — Measurement (weekly, feeds Stage 1)

`content-insights.js` pulls reach/engagement per published post ID via Graph API into `content/metrics.json`. Next month's calendar generation reads it: double down on pillars that perform, cut what doesn't. This closes the loop without any human analytics work.

---

## Loop mapping (matches existing MSS loop architecture)

| Loop | Cadence | Trigger | Human gate |
|---|---|---|---|
| Calendar | Monthly | Manual session (or /schedule routine) | Nafisa approves topics |
| Generate batch | Weekly | Manual session (or /schedule routine) | — (output goes to review) |
| Review sync | Poll while batch pending | Loop-1 pattern (ScheduleWakeup) or same session | Nafisa approves posts |
| Publish | Every run, cron on Pi | cron (e.g. hourly) | none — only publishes pre-approved posts |
| Insights | Weekly | cron on Pi | none |

The only always-on infrastructure is two cron entries on the Pi. Everything agentic runs in Claude Code sessions (interactive or scheduled), same as Loop 2 today.

## Repo layout

```
~/workspace/scripts/
  content-calendar.js      # client-agnostic, --client flag
  content-generate.js
  content-sync.js          # shares code with mss-loop2.js
  content-publish.js       # deployed to Pi cron
  content-insights.js
  content-lint.js          # compliance term lint

~/workspace/other-projects/puremed/content/
  PLAN.md                  # this file
  config/                  # client.json, voice.md, pillars.md, compliance.md
  calendar/2026-08.json
  posts/2026-08-05-laser-lift-myths/{post.json,copy.md,brief.md,assets/}
  state.json
  metrics.json
```

Client #2 = new `content/` directory under their project + credentials. No script changes.

---

## Scale: what we build for and what we deliberately don't

**Built to scale now (cheap):** config-driven scripts with `--client`; per-client compliance/voice/pillars files; state-machine file schema; Stage as the universal approval surface.

**Deliberately NOT built to scale (rationale):**
1. **Meta onboarding automation.** Getting page access, IG Business linking, and Business Manager partner access is a per-client human/legal process regardless of tooling. Automating it at n=1 is pure waste; the per-client cost is a one-time ~1-hour checklist (documented as `ONBOARDING.md` when client #2 arrives).
2. **Multi-tenant scheduler/queue infra.** At every-2-days cadence, even 10 clients is ~75 posts/month — trivially handled by one cron script iterating client configs. Real queue infrastructure earns its keep at ~50+ clients or sub-hour posting precision, neither of which is on the horizon.
3. **Compliance engine.** PureMed's rules are UK medical-aesthetics-specific (ASA/CAP POM rules). A future gym or restaurant client has entirely different constraints. A generalized rules engine at n=1 would be designed against imagined requirements; a per-client `compliance.md` + term lint is both simpler and *more* correct.
4. **Third-party scheduler (Publer/Metricool/etc.).** Would add recurring per-client cost and an approval UX that competes with Stage. Only revisit if Graph API maintenance (token/API-version churn) proves >1 hr/month.

## Prerequisites (client / user actions — DEPLOY.md pattern)

1. Nafisa's Instagram → Business account, linked to the PureMed Facebook Page.
2. MSS Meta Business Manager + app; partner access to PureMed's Page + IG account; system user token with `pages_manage_posts`, `instagram_content_publish`, `read_insights`.
3. Confirm Nafisa's preferred posting time + first-month treatment priorities (one WhatsApp question).
4. Public asset URL path on the Pi (or Cloudways once live) for IG image containers.

## Build phases

- **Phase 1 (no Meta account needed):** config files, calendar generator, post generator + compliance lint, Stage feed-preview + review sync. *Deliverable: Nafisa approves a real August calendar and first batch.*
- **Phase 2:** publisher + Pi cron + token setup. *Deliverable: first post goes live automatically.*
- **Phase 3:** insights loop + metrics-informed September calendar.

Fallback if Meta API access stalls: Phase 1 output loads into Meta Business Suite Planner manually (~15 min/batch) — the pipeline still saves 90% of the work.

## Open decisions

1. **Publishing route:** Graph API direct (recommended) vs third-party scheduler vs manual Business Suite upload.
2. **Approval surface:** Stage feed-preview engagement (recommended) vs email/WhatsApp batch PDF.
3. **Asset strategy:** how much real clinic photography can Nafisa supply? Real photos outperform generated imagery for local trust; generated fills gaps only.
