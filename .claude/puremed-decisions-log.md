---
project: main-stage-studio
status: live
next: "Keep decisions logged same-session, per the standing rule"
blocked_on: ""
owner: osman
---

# PureMed Aesthetics — Decisions Log

*Single source of truth for all project decisions: brand, strategic, and build.*
*Replaces the earlier technical-only decisions-log.md at project root.*
*Last reviewed: 22 June 2026*

---

## Locked Decisions

### Brand and Positioning

| Decision | What's locked |
|----------|---------------|
| Rebuild approach | Full clean-slate rebuild. Nothing carried forward from the original Framer site. |
| Positioning | Medically-led, premium aesthetics. Competing on expertise, trust, and natural outcomes — not price. |
| Target audience | Women aged 35–65. Professionals, mums, women entering peri-menopause. Safety and results over cheap pricing. |
| Hero treatment | Laser Lift skin tightening leads everywhere — nav, homepage grid, messaging hierarchy, cross-links. |
| Primary Blue | `#23476A` — requirements document value used, overriding brand strategy doc's `#0B1F3A` (too dark, addressed Nafisa's direct feedback) |
| Hover Blue | `#2D5B88` — interactive states |
| Champagne Gold | `#C6A77D` — accent only: stars, icons, dividers, nav book button. Never large backgrounds. |
| White | `#FFFFFF` — primary background |
| Warm White | `#F8F8F6` — alternating section backgrounds |
| Light Grey | `#F3F4F6` — cards and subtle separation |
| Black | Explicitly excluded. Site must not feel dark. |
| Voice character | Expert, warm, honest, confident, reassuring. Human and conversational, not corporate. |
| Booking system | All CTAs link to `facesconsent.com/bookings/puremedaesthetics` throughout. |
| SEO approach | Lean — strong foundations, no blog at launch. Solo practitioner reality: blog content strategy deferred until Nafisa is ready for ongoing content commitment. |
| Page-per-treatment | Each treatment has its own dedicated page and URL. Single treatments catalog rejected — individual pages required for local search competition (e.g. "Laser Lift Winslow"). |
| Site size | 13 pages (expanded from original 8 once page-per-treatment decision was made). Additional treatment pages TBC. |
| Delivery stack | WordPress (.org) + Bricks Builder, hosted on Cloudways (DigitalOcean, London region). |

---

### Build — Resolved

| Decision | What's locked |
|----------|---------------|
| DEC-001 (resolved 2026-06-21) | Nav CSS and footer/CTA/WhatsApp CSS stripped from homepage `customCss`. Nav template (71) and footer template (15) are now sole sources of their respective styles. Homepage CSS reduced from 29,383 to 21,051 chars. All 9 section selectors intact. |

### Clinical Platform — Phase 4 documents and signature (15 August 2026)

Code at `booking-engine/service/src/documents/`, `src/notifications/email.ts`,
`src/domain/{document-template,signed-document}.ts`; procedure at
`booking-engine/sops/SOP-BOOK-005-*.md`. Directly answers CONS-003 (locked,
versioned record of exactly what wording the patient accepted) and CONS-006
(complete audit trail of completion/amendment/signature) from the
requirements register.

| Decision | What's locked |
|----------|---------------|
| Scope built | Versioned/immutable consent-form templates (DB-enforced one-live-version-per-name), in-flight signature capture with full evidential metadata (method, IP, user agent, per-clause acknowledgement timestamps, verbatim rendered text), real server-side PDF generation, SHA-256 hashing, best-effort email delivery with an audit log |
| Deliverable proven live | Published a template, signed it over HTTP, downloaded the generated PDF, independently hashed the downloaded file — matched the hash from both the sign response and the download endpoint exactly. Signing with a missing clause acknowledgement correctly rejects `422` with the specific missing IDs, not a silent pass |
| Blocked | Email delivery needs real SMTP credentials, same posture Google/Stripe were in — nobody's account was created on your behalf. Signing itself needs no email config; it's logged either way |
| Not built | Countersignature enforcement (fields exist, no route sets them); external object storage for PDFs (stored in Postgres directly, deliberate scope cut) |

### Clinical Platform — Phase 3 payments, and a real RLS bug fixed (15 August 2026)

Code at `booking-engine/service/src/payments/` and
`src/domain/{payment,paid-booking}.ts`; procedure at
`booking-engine/sops/SOP-BOOK-004-*.md`.

| Decision | What's locked |
|----------|---------------|
| Scope built | Stripe PaymentIntents (manual capture), fixed-amount deposits, signature-verified webhooks, PAY-007 refunds (actor/reason/timestamp recorded), PAY-005 recording of the five non-Stripe payment rails |
| Deliverable proven | The Phase 3 spec's own test: two concurrent paid-booking attempts on the same slot, both authorise a card, exactly one commits + captures, the other's authorisation is cancelled and never charged. Proven against a real Postgres exclusion-constraint race, not mocked |
| **Real bug found #1** | **Row-level security had never actually been enforced, since Phase 1.** The app connected as a Postgres superuser, which bypasses RLS unconditionally. Every tenant-isolation policy was syntactically present but inert. No production deployment exists, so nothing real was exposed, but it needed fixing before one does. Fixed with a dedicated non-superuser `app_runtime` role; a permanent regression test now exists (`test/rls-enforcement.test.ts`) |
| **Real bug found #2** | A Postgres transaction-abort bug in the Phase 1 booking-commit code, invisible until Phase 3's payment flow needed to keep working in the same transaction after a conflict. Fixed with a SAVEPOINT |
| Side effect | Fixing bug #1 required resetting the local dev database, which wiped Nafisa's Google Calendar connection from earlier the same day — she'll need to reconnect it (SOP-BOOK-003), a 2-minute repeat, not a data-loss incident |
| Blocked | Stripe test-mode keys needed to verify live, same posture Google Calendar was in before its OAuth client existed — account creation isn't something done on your behalf. Test-mode keys need no business verification (SOP-BOOK-004 has the signup steps) |

### Clinical Platform — Phase 2 calendar integration (15 August 2026)

Code at `booking-engine/service/src/calendar/`; procedure at
`booking-engine/sops/SOP-BOOK-003-*.md`.

| Decision | What's locked |
|----------|---------------|
| Scope built | Google Calendar + ICS as free/busy readers, Google as event writer, reconciliation sweep, disconnected-state handling (a broken connection degrades availability, doesn't fail it) |
| DIARY-004 enforcement | "Exactly one authoritative writer per resource" is a Postgres partial unique index, not a policy reminder — a second authoritative connection attempt fails at insert time (`409`), same pattern as the Phase 1 booking exclusion constraint |
| Verified | ICS path fully live: connecting a feed removes its busy block from `/availability`; a second authoritative connection is rejected; a broken feed degrades gracefully. All proven with a local fixture server, not just unit tests |
| Google Calendar — LIVE, 15 Aug | OAuth client registered (Google Cloud project `puremed-booking`, owned by osman.akhtar@gmail.com). Full flow verified against a real account: freeBusy correctly read an actual recurring commitment, a test booking synced a real event and was deleted again, no trace left. Fixed a real bug in the process (OAuth callback couldn't carry the tenant header; now reads tenant from the OAuth `state` param). |
| Nafisa connected — LIVE, 15 Aug | She ran the consent flow herself against `care@puremed.uk` (screen-share/same-machine session, since only `localhost:3300` is a registered redirect URI so far). Connection confirmed `connected`, authoritative writer, real free/busy read back successfully with zero writes to her actual calendar. Real `resources` row created for her under tenant `puremed` (no longer throwaway test data). |
| Still needed | App is still in **Testing mode** (test users only, "unverified app" warning, 100-user cap) — fine for now, becomes a blocker only once real client bookings need to go live publicly. Production redirect URI still needs adding to the OAuth client once a real host exists. |
| Not built | MS Graph (stubbed, not needed for PureMed per `technical-design.md` §7.3); async job runner for outbound sync (currently synchronous best-effort + manual reconcile retry) |

### Clinical Platform — Stage 1 build started (15 August 2026)

Phase 1 of `booking-engine-plan.md` (scheduling core) built and verified same day
as the buy-vs-build spike below confirmed the custom-build decision. Code at
`booking-engine/service/`; procedure at `booking-engine/sops/SOP-BOOK-002-*.md`.

| Decision | What's locked |
|----------|---------------|
| Stack | Node/TypeScript + Fastify + Postgres 16 (`btree_gist`), row-level security tenant-scoped from day one per `technical-design.md` §4 |
| Correctness guarantee | Postgres `EXCLUDE USING gist` constraint on `bookings` (resource_id, time_range) — database-level, not application-lock-based. Verified: two concurrent commits for the identical resource/slot, exactly one succeeds, confirmed by automated test and a manual HTTP walkthrough |
| Scope built | Resources, services, working patterns (admin API), availability computation (pure function, DST-correct), booking commit/conflict. No auth yet (`x-tenant-id` header stands in until Phase 7), no calendar sync, no payments, no consent |
| Next | Phase 2, calendar integration (Google/MS Graph free-busy, outbound write, ICS fallback) per `booking-engine-plan.md` §12 |

### Clinical Platform — buy vs. build (spiked and locked 15 August 2026)

Spike: `clinical-platform/buy-vs-build-spike-2026-08-15.md`. Requested because
`booking-engine-plan.md` §11 had only evaluated generic schedulers (Cal.com) as the
rejected alternative, not vertical UK aesthetic-clinic platforms (Consentz, Pabau,
MERIDIQ, Aesthetic Record, Cliniko, Semble).

| Decision | What's locked |
|----------|---------------|
| Build vs. buy verdict | **Custom build confirmed for Stage 1**, but on corrected grounds. Vertical SaaS (esp. Consentz, UK-built and aesthetics-specific) covers booking, consent forms, calendar and photo storage competently and cheaply — the original "no scheduler covers the 80%" argument was true against Cal.com but false against these, and has been corrected in `booking-engine-plan.md` §11. |
| What actually justifies building | No vendor found supports: (1) the prescriber-AND-practitioner hard scheduling dependency (BOOK-007), (2) cross-entity CQC-scope routing between PureMed and Whitehouse (BOOK-008), (3) requirement-gate parity between online and staff-executed WhatsApp bookings (BOOK-004). Buying also reproduces the Faces-style export/lock-in risk (Aesthetic Record's reported $1,120 export fee cited as a concrete example). The multi-tenant booking-engine product/case-study reason stands independently of all of this. |
| Not verified | No vendor contacted directly; findings are web-search/marketing-sourced. If challenged later, get a real Consentz demo plus a written API/export answer before relying on this further. |

### Clinical Platform (answers locked 15 August 2026)

Plan: `clinical-platform/puremed-clinical-platform-plan.md`. Answers from Nafisa,
folded into the plan's "Outstanding action items" and "Open questions" sections the
same day.

| Decision | What's locked |
|----------|---------------|
| Deposit policy | Universal: everyone pays a deposit, no exceptions. Resolves the 9.5 contradiction. |
| Working pattern | Wed 10-3, Fri 1-5 (Friday is the day she can run later). Capacity expands in order: Thursday next (prescriber also works Thursdays), then Monday once Thursday saturates. Model as staged capacity tiers, not a flat weekly schedule. |
| Faces Consent admin | Nafisa is the Faces admin. Field-level export capability and contract/notice terms still open. |
| Qualification/indemnity records | Currently held only on Nafisa's laptop, no central store. Indemnity auto-renews annually; insurer emails a reminder a few weeks ahead, the real signal for expiry-tracking design rather than a fixed date. Scope-of-practice standard itself (action item 2) is still unanswered. |
| PureMed premises exclusivity | PureMed's treatment and waiting room are exclusive to PureMed, no shared staff. Future capacity path: waiting room converts to a second treatment room, Whitehouse's downstairs reception becomes shared waiting area at that point. Not a live multi-tenancy requirement today. |
| dermis.ai access | Login credentials added to the shared Google Sheet, unblocking the app-architecture mapping (action item 9). |

### Social Content Pipeline (locked 3 July 2026)

Plan: `content/PLAN.md`. Phase 1 built 3 July 2026.

| Decision | What's locked |
|----------|---------------|
| Cadence | One post every 2 days (~15/month), Facebook + Instagram, same content adapted per platform |
| Architecture | Deterministic state machine on files (`idea → drafted → review → approved → scheduled → published → measured`); agents generate at fixed stages, scripts move state, git is the audit trail. Client-agnostic scripts (`~/workspace/scripts/content-*.js`, `--client` flag + registry) with all client specifics in `content/config/` |
| Approval surface | Stage, as a feed-preview engagement (`puremed-content`) — one `data-stage-id` per post, existing approve/change/flag mechanics, synced back by `content-sync.js` (Loop 2 pattern). Nothing publishes without Nafisa's per-post approval |
| Publishing route | Meta Graph API direct (Phase 2): system user token via Business Manager, cron publisher on the Pi, idempotent by recorded post ID. Fallback: manual upload to Meta Business Suite Planner |
| Compliance | Hard human-authored rules in `content/config/compliance.md` + deterministic term lint (`content-lint.js`, errors block review). Core rule: no POM advertising (CAP 12.12) — anti-wrinkle content is consultation-led only, no drug/brand names, no prices. No before/after imagery in pipeline posts; no AI imagery depicting treatment results |
| Scale posture | Scale-ready, not scale-built: config-driven from day one, but no multi-tenant infra, no Meta onboarding automation, no generalised compliance engine until client #2 exists |

---

## Open Decisions

| Decision | Why it's open | Blocker? |
|----------|---------------|---------|
| Rebuild brand vs. live dermis.ai brand | Live puremed.uk (dermis.ai platform) uses `#343a67` navy, `#d0ac61` gold, Majesty + Hanken Grotesk, and a different gold face-profile logo — none of which match the MSS rebuild's locked spec (`#23476A`, Cormorant Garamond/Inter, blue/gold vector). Unclear whether this is Nafisa's actual current preference (adopted since the spec was locked) or a legacy vendor site the rebuild is meant to replace with its own distinct identity. See "Live Site Reference" in `puremed-brand-identity.md` | Blocks finalising the rebuild's colour/type system |
| Logo — studio vs supplied | Nafisa to confirm whether to use studio-created vector (`puremedvectorbluegold.ai`) or supply her own SVG with transparent background | Blocks finalising header template |
| Photography — hero, portrait, placeholders | Nafisa to confirm or replace hero photo, Nafisa portrait, and AI-generated placeholder slots. Full inventory in `brand/puremed-project-summary.docx` Section 04b | Required before launch |
| Google review count | Currently showing 500+ as an estimate. Nafisa to confirm actual count | Before launch |
| Qualifications and credentials | Specific credentials for the credibility section currently showing generic placeholders | Before launch |
| Additional treatment pages | Thread Lifting, EMSLIM NEO, Fat Dissolving, Semi-Permanent Makeup, OBAGI skincare — confirm whether at launch or in a later phase | Affects total site scope |
| Laser Lift page rebuild | Current Laser Lift page predates the new treatment template. Recommend rebuilding to match the other five treatment pages | Affects launch quality |
| Typography | Confirmed: Cormorant Garamond (headings), Inter (body/UI). Updated in brand-identity.md. | No |
| Booking URL conflict — URGENT | The current live site has two conflicting booking URLs simultaneously: `facesconsent.com/bookings/puremedaesthetics` (primary CTAs) and `puremedappointments.as.me/Winslow` (Acuity Scheduling, footer and older buttons). Clients on different parts of the site are being routed to different platforms. Prototype uses Faces Consent throughout — confirm this is the active system before launch. Old Acuity URL must be removed. | Blocks launch |
| Booking system scope | Does Faces Consent handle just booking, or also consent forms and client records? Determines what can be replaced vs what must be kept. | Informs tech stack |
| Email — Stackmail migration | Nafisa wants to move away from Stackmail. Unclear whether Stackmail hosts the `care@puremed.uk` inbox or just handles sending. If it hosts the inbox, migration is a larger operation. Replacement not yet recommended pending answers. | Before launch |
| Newsletter list | Footer newsletter signup exists on current site. Unclear where submissions go — may be routing to nothing. Must be checked before old site is taken down. | Before cutover |
| Analytics | No visible analytics code found on current site. Unclear if GA4 or Meta Pixel were ever installed or whether historical data exists. GA4, GTM, and Meta Pixel are confirmed build tasks for the new site. | Build phase |
| Google Business Profile | Claimed and managed status unknown. Booking link in it may point to old Acuity URL. Requires Nafisa to grant access for Google Business setup and optimisation. | Before launch |
| Domain ownership | Domain registrar and DNS access not yet confirmed. DNS access is required to point `puremed.uk` to Cloudways. Third-party control adds lead time. | Required for go-live |
| Payment plan provider | PureMed offers payment plans — provider (Payl8r, Tabby, Klarna, or other) not confirmed. If third-party finance is used, it needs a presence and integration on the new site. | Affects site structure |
| Online shop | OBAGI skincare and other products — sold in-clinic only or online sales planned? E-commerce adds significant complexity if needed. | Affects site structure |
| Photo upload form | Nafisa noted this as a high-value feature: allow clients to upload photos for advice, unique in the market. Not built yet. Would require a form with file upload, secure handling, and email routing. | Future phase or launch |
| WhatsApp — personal vs Business | Currently unknown whether Nafisa uses a personal number, WhatsApp Business, or a third-party inbox tool. WhatsApp Business API could connect to a CRM. Personal number is a single point of failure. | Informs integration recommendation |
| DEC-002 — Header template MCP bug | `save_elements()` always writes to `_bricks_page_content_2` regardless of template type, but `get_elements()` on headers reads from `_bricks_page_header_2`. Every header edit requires running the MySQL sync script. Options: (A) one-line patch to `BricksService.php` (overwritten on plugin update), (B) keep MySQL sync step documented and required, (C) check if newer Bricks MCP version fixes this. | Every future header edit |
| DEC-003 — MCP payload truncation | `page:update_content` silently truncates code element content above ~2KB. Current workaround: PHP direct write via `/tmp/build_puremed_direct.php`. Options: (A) patch MCP plugin for larger payloads, (B) keep PHP direct write for homepage sections, (C) rebuild sections using native Bricks elements instead of Code elements. | Every future homepage section edit |
| Social posting time | `18:00 Europe/London` set provisionally in `content/config/client.json`. Nafisa to confirm preferred time | Before first scheduled publish |
| Meta account prerequisites | IG → Business account linked to FB Page (Nafisa, ~10 min); MSS Business Manager + partner access + system user token (Osman). Business verification can take days–weeks — start early | Blocks Phase 2 (automated publishing) |
| Social photography | Batch 1 uses site imagery as placeholders (some AI-generated). Real clinic photography preferred for social trust — ask Nafisa what she can supply ongoing | Before first publish, per post |

---

## Flagged — Needs Check

| Item | What needs checking |
|------|---------------------|
| DEC-003 not in `mss-production-ops.md` | The payload truncation bug is a confirmed exception in the same category as the three already documented in production-ops. Should be added as Exception 4 before the next Bricks session on any project. |
| `index.html` at project root | Confirmed stale (older v6 prototype). Safe to delete. |
| `studio2-decisions-log.md` and `studio2-decis...g-updated.md` | Stale Studio 2 era files. Studio 2 was reversed 17 June 2026. These should be deleted — they have no bearing on current project status. |
| Typography gap in brand identity file | `puremed-brand-identity.md` has a placeholder for typography. Extract font names and weights from the HTML prototype files in `web/` and update the file before running any Bricks global styles session. |
| Google Business Profile | Listed as a studio build task in project summary. Not started. Requires Nafisa to grant access. High-ROI local SEO action — confirm priority and timing. |
| GA4 + GTM + Meta Pixel | Listed as studio build tasks. Not yet installed. Set up at build stage, before go-live. |
| Schema markup | Local business schema (homepage) and MedicalProcedure schema (all treatment pages). Not yet implemented. |

---

## Technical Reference

### DEC-002 — Header template MySQL sync (required after every MCP edit to template 71)

```sql
DELETE FROM wp_postmeta WHERE post_id=71 AND meta_key='_bricks_page_header_2';
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
  SELECT 71, '_bricks_page_header_2', meta_value
  FROM wp_postmeta WHERE post_id=71 AND meta_key='_bricks_page_content_2';
```

Root cause: `BricksService.php` line 192 always writes to `_bricks_page_content_2`
regardless of template type. The header frontend reads from `_bricks_page_header_2`.
Affected file: `/Users/osmanakhtar/Local Sites/puremed/app/public/wp-content/plugins/bricks-mcp/includes/MCP/Services/BricksService.php`

### DEC-003 — Homepage section updates (PHP direct write required, not MCP)

Current build script: `/tmp/build_puremed_direct.php`

Do not use `page:update_content` for homepage sections. It silently truncates
Code element content above ~2KB — confirmed with inline SVG paths (WhatsApp icon,
calendar icon). MCP reports success but stored content is shorter than what was sent.

---

## Change History

| Date | What changed | Why |
|------|-------------|-----|
| 10 Aug 2026 | **Systems build posture reversed: gap layer first, Faces Consent stays.** Nafisa discovery call captured as `discovery/2026-08-10-as-is-operating-model.md`; requirements register to v0.2 (50 rows to 84); clinical-platform plan to v0.2 with a new Section 9 superseding Section 7 for sequencing; `booking-engine/booking-engine-plan.md` to v1.6; client-facing `puremed-systems-proposal.md` drafted (scope and phasing, no pricing, systems workstream only) | The clinical-platform plan v0.1 was written from the requirements brief alone and assumed Faces Consent needed replacing wholesale (S1-S14). The call disproved the premise: Faces holds the diary, ~475 patient records and a consent library already matched to the treatment menu, and does those adequately. The real cost sits in five gaps Faces leaves: bulk clinical photo handling (7-15 images per patient, every patient, stranded on a personal phone), the paper toxin prescribing form (countersigned, meant to be photographed onto the patient file, with a confirmed backlog that never was), deposits absent on the WhatsApp booking path Nafisa executes herself, three competing writers to her Google Calendar including a ChatGPT inbox automation, and aftercare that fails roughly nine times in ten. Decisive argument for staging: the as-is record contains two proven abandonments (a Dropbox photo routine and the Faces one-at-a-time upload), both correct processes dropped for being slower than the shortcut, so anything shipped must be fewer steps than today on day one. Phase R (replacement) is now trigger-based, not scheduled, and explicitly may never happen. Also surfaced: WhatsApp is the operating surface not a channel; prescriber and treating practitioner differ on every toxin treatment and toxin is bookable only on his days; hyperhidrosis and jaw toxin run under Whitehouse's CQC registration; dermis.ai's scope is far wider than "site and maintenance" (app, memberships, loyalty points, Klarna, skin scanner, Meta ads, and an AI voice agent presenting as human to patients under PureMed's name) |
| 10 Aug 2026 | Four domain-model gaps logged against the booking engine, none PureMed-specific: cross-resource availability (a service requiring two resources simultaneously, not just one of several eligible), payments taken outside the engine (six live channels at PureMed with no single view of what a booking has been paid), provider/location as a service attribute distinct from practitioner (CQC registration attaches to provider, location and activity), and staff-executed bookings as a first-class journey rather than an admin afterthought | Surfaced by the PureMed call but each recurs in any regulated practice with a supervising or prescribing role, so they belong in the multi-tenant model rather than in tenant configuration. Recorded at the end of `booking-engine-plan.md` §13 rather than rewriting the design, since the production system is not started |
| 9 Aug 2026 | Discovered live puremed.uk runs on the dermis.ai platform with a different palette/type/logo than the MSS rebuild spec (`#343a67` + Majesty/Hanken Grotesk vs. the locked `#23476A` + Cormorant Garamond/Inter); flagged at the top of `.claude/puremed-brand-identity.md` with the live values recorded in a new "Live Site Reference" section, spec left unchanged pending Nafisa | Osman asked for a brand guide sourced from the live site; the fonts/colours pulled from puremed.uk's actual CSS and logo asset didn't match what's documented, and the asset host (Firebase project `dermis-d86a7`, `onboarding.dermis.ai` fonts) confirms it's a different vendor build, not the MSS Astro rebuild. This is the "dermis.ai to reconcile" item from the growth-engagement plan surfacing concretely — needs a decision on whether the rebuild adopts the live dermis.ai brand or keeps its own | Open |
| 9 Aug 2026 | Brand guide refreshed: Voice and Tone section rewritten from Nafisa's detailed guidance (writing rules, banned phrases, worked before/after examples); new "Patient and Audience Photography Direction" section added covering stock/lifestyle imagery of the target reader (British women 35-65, three age bands, authenticity principles, four prompt templates) | Colours, fonts and logo were already confirmed against the requirements doc and live site and needed no change. The gap was voice detail and patient-facing image direction — prior prompt files (`puremed-nafisa-prompts.md`, `puremed-asset-generation-prompts.md`) only covered Nafisa/practitioner shots, not the patient herself. Canon = `.claude/puremed-brand-identity.md` |
| 8 Aug 2026 | Stage page switcher redesigned (shared chrome, affects every live-edit engagement) | It was pinned full-width across the top of the viewport, which is exactly where every prototype puts its own header, so the thing under review was permanently half-covered; with nine pages the labels also wrapped to two lines and the active pill rendered as a circle. Now docked bottom-centre and collapsed to a single glass pill naming the current page and its position ("Laser Lift 2/9"), opening upward on demand, single-line labels, active row marked with a rail rather than a filled blob. Hides itself while the booking drawer is open so it cannot cover the Continue button. `puremed-site` gets the same improvement and was re-verified: its links remain blocked, as that surface intends. |
| 8 Aug 2026 | Social-media-drive POC: microsites on Stage as `puremed-micro`, booking journey embedded in-page, Sculptra added as a seventh microsite | Each treatment page is to get its own Instagram presence driving traffic to it (traffic engine out of scope). Booking CTAs no longer navigate away: they open a drawer over the page carrying the client-facing journey with that treatment preselected, via a new `embed=1` mode on the booking prototype that hides the demo banner, mock site, rule trace and admin panes. Showing a working journey in place is the sales mechanism, so the treatment being sold stays on screen behind it. Sculptra was rebuilt from its own standalone page onto the shared template, gaining the real logo, practitioner section and booking wiring. Two shared systems were extended additively: `scripts/stage-autotag.js` gained `--files`/`--relroot` so plain HTML can be tagged, and Stage's live-edit surface gained an opt-in `allowNavigation` manifest flag so internal links click through instead of being swallowed by the editor (`puremed-site` does not set it and is unchanged). `live-edit.js` also gained an mtime cache-buster after a stale cached copy silently swallowed clicks during verification. Nafisa is scoped to the new engagement; her two in-flight edits survived the redeploy with zero stranded ids. Procedure: SOP-PUREMED-003. Still not signed off, and the before/after client photography still needs her approval. |
| 8 Aug 2026 | Six treatment pages revived as standalone microsites, rebuilt self-contained and published for review | Previously explored and dropped as main-site pages; now taken forward as one-per-treatment landing pages in the Sculptra mould, linkable from ads or social without routing through the main site. Rebuild fixed four defects found on review: (1) the nav/footer logo used the untrimmed `puremed_logo_transparent.webp`, whose mark occupies under half the canvas, rendering the wordmark ~20px tall and illegible on navy, so a trimmed `puremed-logo-trimmed.webp` was generated from the alpha bbox; (2) ~76 links pointed at `puremed-homepage-v3/v5/v6.html`, which have never existed in `web/`, rewired to in-page anchors and the hub; (3) `puremed-laser-lift.html` still used `#0B1F3A` as brand navy, the value rejected on Nafisa's feedback, corrected to the locked `#23476A`; (4) no page carried a practitioner section at all, Nafisa appeared only as a dead nav link and two text mentions, so a section using the approved real photo `nafisa-hero-v2.webp` was added to all six. Pages are self-contained (fonts and images inlined) so they publish anywhere. Build/publish procedure in `sops/SOP-PUREMED-002`; live URLs in `tools/microsite-urls.json`. NOT signed off, and the before/after client photography on these pages still needs Nafisa's approval before anything is public. |
| 6 Aug 2026 | Treatments page hero image swapped; mobile hero layout restructured | Hero used `nafisa-20-seedream5lite-v1.webp`, an AI-generated approximation that didn't resemble Nafisa and showed the wrong setting (generic clinical room vs the real branded lobby). Swapped to `nafisa-hero-v2.webp`, a real photo already in `assets/web/` (there's also a `puremed-nafisa-hero--do-not-use.webp`, a flat-background cutout variant, correctly left unused). Separately, below 900px the photo ran full-bleed behind the text with only a diagonal gradient for contrast, so the heading/stats sat on top of her face; restructured to stack the photo as its own block above the content on mobile, matching the clean split the desktop layout already has. `site/src/pages/treatments.astro`. MSS case study at `01_mss/website/site/src/pages/work/puremed.astro` reuses two screenshots of this page and was recaptured via `01_mss/website/tools/clips/shoot-site.js` to match. |
| 3 July 2026 | Social content pipeline: plan approved, Phase 1 built | Nafisa's consistency pain point. Deterministic pipeline (state machine + agent stages + Stage approval + Graph API publish) planned in `content/PLAN.md`; Phase 1 delivered same day: config, August calendar (16 slots, validated), first batch of 4 posts with copy (linted clean), feed preview, review sync script (fixture-tested). Open: posting time, Meta prerequisites, real photography. |
| 22 June 2026 | Decisions log updated with systems discovery and requirements doc | Typography confirmed (Cormorant Garamond/Inter). Systems and integrations open items added from discovery questionnaire (21 questions, answers not yet received). Booking URL conflict flagged as urgent. Brand identity file updated with confirmed typography and expanded design requirements. |
| 22 June 2026 | Decisions log created and reconciled | Previous log was technical-only (DEC-001/002/003). Brand and strategic decisions from project summary and brand strategy docs folded in. Stale studio2 files flagged for deletion. |
| 21 June 2026 | DEC-001 resolved | Nav CSS and footer/CTA/WhatsApp CSS stripped from homepage customCss. Templates 71 and 15 are now sole CSS sources for their respective elements. |
| 21 June 2026 | DEC-002 raised | Bricks MCP save_elements() bug identified — writes to wrong meta key for header templates. MySQL sync workaround in place and documented. |
| 21 June 2026 | DEC-003 raised | MCP payload truncation confirmed. PHP direct write workaround in place for homepage sections. |
| 25 May 2026 | Project summary v1.0 produced | HTML prototype complete across 7 pages. Awaiting copy and design sign-off. Key outstanding items identified: photography, logo confirmation, credentials, additional treatment pages TBC. |
