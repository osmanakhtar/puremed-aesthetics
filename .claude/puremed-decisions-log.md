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
| 3 July 2026 | Social content pipeline: plan approved, Phase 1 built | Nafisa's consistency pain point. Deterministic pipeline (state machine + agent stages + Stage approval + Graph API publish) planned in `content/PLAN.md`; Phase 1 delivered same day: config, August calendar (16 slots, validated), first batch of 4 posts with copy (linted clean), feed preview, review sync script (fixture-tested). Open: posting time, Meta prerequisites, real photography. |
| 22 June 2026 | Decisions log updated with systems discovery and requirements doc | Typography confirmed (Cormorant Garamond/Inter). Systems and integrations open items added from discovery questionnaire (21 questions, answers not yet received). Booking URL conflict flagged as urgent. Brand identity file updated with confirmed typography and expanded design requirements. |
| 22 June 2026 | Decisions log created and reconciled | Previous log was technical-only (DEC-001/002/003). Brand and strategic decisions from project summary and brand strategy docs folded in. Stale studio2 files flagged for deletion. |
| 21 June 2026 | DEC-001 resolved | Nav CSS and footer/CTA/WhatsApp CSS stripped from homepage customCss. Templates 71 and 15 are now sole CSS sources for their respective elements. |
| 21 June 2026 | DEC-002 raised | Bricks MCP save_elements() bug identified — writes to wrong meta key for header templates. MySQL sync workaround in place and documented. |
| 21 June 2026 | DEC-003 raised | MCP payload truncation confirmed. PHP direct write workaround in place for homepage sections. |
| 25 May 2026 | Project summary v1.0 produced | HTML prototype complete across 7 pages. Awaiting copy and design sign-off. Key outstanding items identified: photography, logo confirmation, credentials, additional treatment pages TBC. |
