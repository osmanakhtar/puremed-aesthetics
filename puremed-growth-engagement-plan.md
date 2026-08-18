# PureMed Business Growth Engagement

*Canon doc. Drafted 9 Aug 2026 from Osman's brief, restructured 15 Aug 2026 to list
every live workstream. This is the engagement-level doc: it sits above the microsite
build, the booking engine, clinical-platform scoping and GTM, and is the answer to
"what is PureMed, across everything" — read this first, not `CLAUDE.md`, which only
covers the web-execution workstream in build detail. Working directory:
`~/workspace/main-stage-studio/02_clients/puremed/`. Booking engine itself lives
outside this directory, at `~/workspace/booking-engine/` — see the Workstreams
section below for why.*

---

## What changed

The PureMed engagement is repositioning from "MSS builds Nafisa a website" into a
broader growth engagement aimed at driving more bookings into Nafisa's diary. The
business is still owned and operated by Nafisa: this is a client engagement, not a
three-way joint venture, even though it is run day to day by family.

## Roles

- **Nafisa**: owns the business, runs the treatment/clinical operation. Client.
- **Osman**: responsible for the website build and website execution, and for the
  operational/technology side generally (stack, tooling, infrastructure).
- **Shuab (brother)**: manages the social media content strategy, and is writing the
  go-to-market strategy, covering Instagram strategy and execution, and web strategy
  and execution.

Osman and Shuab jointly support Nafisa on the operational and technology side of the
business (the stack, not the clinical work).

## The problem being solved

Nafisa currently spends roughly two to three days a week on social media, content, and
admin, time that competes directly with treatment delivery (her actual revenue). The
intent of this engagement is to reduce that load and convert the freed capacity into
more bookings, not just a nicer website or a content calendar for its own sake.

## Existing vendor context

Nafisa has a live engagement with **dermis.ai**, who currently manage her live website
and have also offered her a mobile app. This engagement runs alongside/ahead of that
relationship; the handover or coexistence between dermis.ai's live site and MSS's
rebuild is not yet resolved and should be treated as an open item, not assumed away.

## Workstreams

**Restructured 15 August 2026** to actually list every live workstream — the
version above only named three and had drifted out of step with what's actually
being built (no mention of the booking engine or the microsites as their own
thing). This section is now the answer to "what is PureMed, across everything":
five workstreams, five owners, cross-referenced rather than duplicated.

### Website hub — dermis.ai, out of MSS scope

`puremed.uk` is owned and managed by dermis.ai and **stays that way
indefinitely** (confirmed 15 Aug 2026). Not a workstream MSS executes. Relevant
here only because every other workstream has to route around it: no MSS write
access to that domain, so it cannot carry problem-landing pages, microsite
content, or anything else. dermis.ai's wider footprint (app, memberships,
loyalty, Klarna, the AI voice agent) is tracked in [[project-puremed]] memory,
not here — this doc only needs the access-boundary fact.

### Treatment microsites (Osman) — the live web build

One microsite per treatment, own URL, replacing the two-page Astro rebuild as
the actual go-to-market web surface (the Astro rebuild in `site/` does **not**
go live, kept as historical record only — see `CLAUDE.md`). Seven built on Stage
(`puremed-micro`), none signed off. Laser Facelift
(`web/laserfaceliftwinslow.html`) is the pilot: paused on a brand question
(resolved 15 Aug — must visually match live `puremed.uk`, reuse its components),
now unblocking. Build detail, SOPs and defect history: `CLAUDE.md`. This is the
workstream the booking engine below plugs into.

### Booking engine (Osman, shared build with MSS) — the microsites' entry point

Lives in its own repo/folder, `~/workspace/booking-engine/`, deliberately kept
separate from this client directory: it's built multi-tenant on purpose
(Thackray Vane and Marbury Hale are fictional non-PureMed tenants for the MSS
Systems case study; PureMed is tenant 1, not the only one). Canon:
`booking-engine/booking-engine-plan.md`. Each treatment microsite above embeds
this as its booking entry point (drawer, treatment preselected). Production
Phases 1-6 done and live-verified; PureMed-specific go-live blocked on the open
items below, not on further engine build — see the plan's §16 resume prompt for
the reordered next steps.

### Clinical platform (scoping only)

`clinical-platform/` (moved here 9 Aug 2026 from the top-level `puremed-clinical-platform/`
project dir) holds the EHR-grade clinical/booking/consent system scoping. It remains its
own component within this engagement: see `clinical-platform/puremed-clinical-platform-plan.md`.
Not yet validated, no build started.

### GTM / social (Shuab)

Instagram strategy and execution, and web strategy, authored by Shuab at
`https://puremedig-desk.vercel.app/business-growth-strategy` (found and reviewed
15 Aug 2026 — previously undocumented here). Multi-account Instagram model (one
main account + ~9-10 problem-led ".bucks" satellites) driving to WhatsApp is
unaffected by anything above. His website-strategy tab assumes puremed.uk write
access that the dermis.ai boundary above rules out; needs amending with him to
route to the microsites workstream instead of puremed.uk subpages — flagged, not
yet actioned.

## Open items

- ~~Resolve the dermis.ai relationship~~ **Resolved 15 August 2026: dermis.ai keeps
  `puremed.uk` indefinitely.** The Astro rebuild in `CLAUDE.md`'s web-execution
  workstream does not go live and does not replace it. Consequence: Shuab's GTM
  plan (below) cannot land its problem-landing pages on `puremed.uk` as written —
  MSS has no write access to that domain — so the funnel resolves to
  microsite-per-treatment instead. See `CLAUDE.md`'s microsite section.
- ~~Shuab's GTM/Instagram strategy is not yet captured~~ **It now exists**, at
  `https://puremedig-desk.vercel.app/business-growth-strategy` (Instagram
  strategy, Instagram execution, website strategy, website execution tabs).
  Reviewed 15 August 2026. His website-strategy tab assumes puremed.uk write
  access that the dermis.ai decision above rules out — needs amending with him to
  microsite-per-treatment, laser-first, same GTM logic (WhatsApp prefill per
  problem, .bucks Instagram naming) otherwise unchanged.
- No sign-off yet on how "drive bookings" will be measured (diary fill rate, booking
  count, source attribution) — worth defining once Shuab's strategy lands.
- **New gap surfaced 15 August 2026:** no design exists for migrating *existing
  bookings/diary state* into the new booking engine — the systems proposal covers
  migrating the 475 patient records and consent library, not booking history.
  Needed before any real cutover from Faces Consent.
- **Still blocking a dated go-live, independent of the web/microsite track:** the
  three open decisions in `puremed-systems-proposal.md` (deposit policy — universal
  vs. discretionary; Nafisa's actual working pattern; where quals/insurance/
  indemnity are tracked) and Faces Consent's API availability and contract/exit
  terms, named repeatedly across docs as the single most load-bearing unknown.
