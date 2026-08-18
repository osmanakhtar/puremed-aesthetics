# PureMed Aesthetics, Claude Session Context

*MSS client engagement. Promoted from a standalone personal project on 6 August 2026
and moved into the Studio client folder, per the stream separation rule in
`main-stage-studio/CLAUDE.md`. Repositioned 9 August 2026 as a broader business growth
engagement (bookings-driven, three-person family-run delivery team, Nafisa remains
the client/owner) — see `puremed-growth-engagement-plan.md` for the engagement-level
framing. This file covers the web execution workstream specifically.*
*Working directory: ~/workspace/main-stage-studio/02_clients/puremed/*
*Last reviewed: 9 August 2026*

---

## What this project is

Full clean-slate website rebuild for PureMed Aesthetics, a medically-led aesthetics
clinic run by Nafisa. Rebuilt from an existing Framer site that scored 23/100 on a
CRO audit. This is the first live test of the MSS Astro delivery pipeline:

```
Prototype HTML → Stage review (mss-review.duckdns.org) → Nafisa signs off
  → Astro build from approved prototype → GitHub Actions → Cloudways static
```

## Current status

- Two-page prototype (Home + Treatments) deployed on Stage for client review
- Stage manifest patched with `astroFile` + `astroProp` per copy section
  (see `~/workspace/scripts/patch-manifest-astro-fields.js`)
- Astro build, GitHub Actions CI/CD, and Cloudways static app: pending
- Domain not yet migrated — staging uses the free `.cloudwaysapps.com` URL

## Context files (in `.claude/`)

| File | What it covers |
|------|----------------|
| `puremed-brand-identity.md` | Palette, logo, typography, voice, site architecture |
| `puremed-decisions-log.md` | What's locked, what's open, build constraints |

Read both before any copy or build session. The decisions log wins if anything
disagrees. Load the PureMed voice from the brand-identity file — not MSS voice.

## Stack

- **Build:** Astro static site (Bricks Builder + LocalWP retired 25 June 2026 —
  DEC-002/DEC-003 and the WordPress constraints in the decisions log are
  historical only; do not follow them)
- **Review:** Stage on the Pi — engagement `puremed`
- **Hosting:** Cloudways, DigitalOcean, London region
- **Booking:** all CTAs link to `facesconsent.com/bookings/puremedaesthetics`

## What actually ships

**Corrected 15 August 2026.** Dermis.ai's live `puremed.uk` stays, indefinitely —
confirmed by Osman in the growth-engagement reconciliation session. The Astro
rebuild below (`site/`) is **not** going live and does not replace it. Kept as
historical record of what was built and reviewed; do not present it as the launch
path without a fresh decision to revisit this.

**`site/` is the Astro rebuild, not the live site.** Two pages: Home
(`src/pages/index.astro`) and a single Treatments page
(`src/pages/treatments.astro`) carrying one anchored section per treatment,
deep-linked from the nav. Nafisa reviewed this on Stage. It is not the version
going live.

`web/` holds ten standalone HTML prototypes plus the client's source documents
(requirements, brand strategy, discovery docx). Do not treat `web/` as the shipped
site: the main site is still the two pages in `site/`, and screenshots, page counts
and case-study claims come from `site/` only.

**Treatment microsites (revived 8 August 2026; model confirmed 15 August 2026).**
The six per-treatment pages in `web/` were previously explored and dropped as
main-site pages. They are now being taken forward as *standalone microsites*
instead: one self-contained page per treatment, linkable from an ad or social
post without routing through the main site, in the same vein as the Sculptra
landing page. They are built and published for review, not signed off. See
`sops/SOP-PUREMED-002` for the build and publish procedure;
`tools/microsite-urls.json` holds the live review URLs.

**This is now the confirmed model, not a parked experiment.** Since dermis.ai
keeps `puremed.uk` indefinitely, Shuab's GTM plan (problem-landing pages built
directly onto `puremed.uk`, see `puremed-growth-engagement-plan.md`) is not
executable by MSS — there is no write access to that domain. The reconciled
funnel is: IG satellite → WhatsApp → per-treatment microsite (own URL) → booking
engine embedded on that microsite. Every treatment gets a microsite eventually;
laser is the pilot the rest of the pattern repeats from. **Brand requirement:**
each microsite must visually match the live `puremed.uk` (dermis.ai's build) —
follow the PureMed brand guide and reuse similar components to the existing site,
not a distinct sub-brand. This was the reason the laser build was paused; it is
now unblocked. Flag to Shuab that his Phase 2A (puremed.uk problem landings)
needs amending to microsite-per-treatment for the same reason.

**Booking landing page built, 15 August 2026: `web/book-laser-facelift.html`.**
Forked from `booking-engine/prototype/_internal-puremed-v1.0.html` (the internal,
never-publish demo) into a standalone, brand-matched, single-treatment page —
own file, own URL, no drawer/iframe dependency. Two purposes: the destination of
`laserfaceliftwinslow.html`'s new "Book a consultation" CTA (added alongside the
existing WhatsApp CTA, not replacing it), and a link that can be sent standalone
to jump straight into the laser-facelift journey. Pattern to repeat per treatment:
copy the file, override the `:root` colour variables and the two font-family
find/replaces (`Cormorant Garamond`→`Georgia,'Times New Roman',serif`,
`Inter`→`'Hanken Grotesk',sans-serif`) if a future microsite uses different
tokens, swap the default service id in the `openDefaultService` IIFE near the
end of the script, and swap the header/footer copy. Every deviation from the
source prototype is isolated and comment-marked ("STANDALONE BOOKING PAGE
PATCH") at the top and bottom of the file — check there before editing.

**Design pass, 15 August 2026, revised same day after a second review.** Redesigned
against the live `puremed.uk`'s actual patterns rather than the generic
centered-card layout it started with. Settled state after two rounds:
- **Hero**: split layout (text left, `laser-lift-hero.webp` right), CTA restored
  ("Book a consultation" + a smaller WhatsApp text link beneath it).
- **Eyebrows**: plain small-caps text, no pill/border — the first pass used a
  pill badge that doesn't match the live site; fixed globally.
- **Who you see**: reverted to the original circular-photo treatment
  (`nafisa-hero-v2.webp`, 9.5rem circle, image on the left) — the first pass
  swapped this for a full-bleed AI-likeness consultation photo and moved too far
  from the live site's actual pattern. Stayed moved up to block 2, no CTA button
  in this section (the hero and the deep-dive block below already carry it).
- **Treatment deep-dive** (new, replaces the old separate intro / help-list /
  treatments-we-may-use blocks): one split section — `patient-portrait.webp` left,
  eyebrow + h1 + italic accent line + lede + a 3-cell quick-facts strip (only
  verified facts: 90 min session length from the booking catalogue, non-surgical,
  consultation-led — deliberately no invented session count, downtime or results
  duration, since those aren't sourced anywhere) + an outline-numbered "How it
  works" list (the booking process, not fabricated clinical mechanism detail) +
  a checkmark "Ideal if you have" list, reframed positive-outcome rather than
  pain-point per direction, + a CTA button.
- **Before & after**: unchanged from the first pass — an honest empty state
  ("real patient photo, coming soon"), not a fabricated result. Do not replace
  with anything except real, consented patient photos from Nafisa.
- **Secondary links / proof**: de-boxed — plain divider-rule list and a plain
  quote block instead of bordered cards, less "generic container" feel.
- **Buttons**: radius changed from full pill to ~10px to match the live site's
  actual button shape (also not a pill on the real site).
- **Footer**: unchanged from the first pass, matches `puremed.uk`'s real footer
  (logo, social icons, CLINIC/LEGAL columns, VISIT block). Legal column links out
  to `puremed.uk`'s own privacy/terms/sitemap pages rather than hosting duplicate
  copies — drafting/duplicating legal text wasn't something to do unprompted,
  flag if hosting local copies is still wanted.

**Pushed to Stage, 15 August 2026: `https://mss-review.duckdns.org/prototype/puremed-laser-facelift-winslow`.**
Own engagement, separate from `puremed-micro`'s 7-treatment pipeline (SOP-002/003
don't apply here — neither script is parameterised for a lone two-page site).
Deploy procedure, since nothing existing covered it:
1. Stage copies of `laserfaceliftwinslow.html` → `index.html` and
   `book-laser-facelift.html`, with their cross-links rewritten from relative
   (`book-laser-facelift.html`, `laserfaceliftwinslow.html`) to Stage's absolute
   routing (`/prototype/puremed-laser-facelift-winslow[/book-laser-facelift]`) —
   **only in the deployed copies**, never the canonical `web/` source, which stays
   relative for real deployment.
2. Tag only the microsite copy with `scripts/stage-autotag.js --files
   <index.html> --relroot <dir>`, then `--scan` it for the copy/image inventory.
   `book-laser-facelift.html` is never tagged, same rule as `puremed-micro`'s
   `booking.html` exclusion — it's a JS app, not editable copy.
3. Hand-assemble `manifest.json` from that scan (mirroring
   `tools/build-stage-manifest.py`'s shape, since that script is hardcoded to
   `web/stage-build/` and the 9-page pipeline — not reusable as-is), two pages
   (`index`, `book-laser-facelift`), `allowNavigation: true` so the CTAs actually
   navigate instead of being swallowed by the live-edit click handler.
4. Back up `manifest.json`/`client-edits.json` on the Pi, scp both HTML files +
   manifest + any new image basenames into
   `/home/pi/stage/engagements/puremed-laser-facelift-winslow/{prototype,assets}/`,
   then `bash /home/pi/stage/scripts/validate.sh puremed-laser-facelift-winslow`
   and the stranded-edits check from SOP-001/003.

**Non-obvious server behaviour worth knowing before touching this again**
(`server.js`'s `servePrototype()`): it rewrites every `src`/`href` ending in an
image extension to `/assets/<engagement>/<basename>` automatically, regardless
of what path prefix the source HTML uses — so the `assets/laser-facelift-winslow/`
prefix in the canonical source files doesn't need rewriting for Stage, only the
basename needs to physically exist in the engagement's `assets/` folder.

**Booking journey UX pass, 15 August 2026** — full write-up, independent peer
review, and build, per `booking-journey-ux-review-2026-08-15.md` (read that
first for the reasoning; this is the summary of what changed). The widget
engine and its CSS are no longer duplicated per treatment page: extracted to
`assets/shared/booking-widget.js` and `assets/shared/booking-page.css`, loaded
by both `web/book-laser-facelift.html` and the new `web/book-liquid-facelift.html`
(back-link points at `puremed.uk/dermal-fillers.html` — there's no redesigned
Liquid Facelift microsite yet, that's a separate task). Per-page files now only
carry the head meta, the `.mb-*` header/footer content, and a ~15-line script
setting the default service id and close-button target. Behaviour changes
(in the shared engine, so both pages get them): deep-linking to a treatment now
skips the picker straight to the next active step, showing a locked "Booking:
X · price · duration · Change" strip instead; a context-free open (no
`?svc=`) shows the full picker with Consultations sorted first and a "New
here? Start with a consultation" callout — never a silently pre-selected
service. Payment step gained a Google Pay preview button (simulated
authorisation, same honesty banner) and Stripe-Elements-styled card fields.
**Apple Pay was deliberately not built** — the peer review flagged that a
generically-simulated button under a real payment brand's name is closer to
misrepresentation than the demo card fields are, and Apple Pay's real API
can't be honestly mocked cross-browser the way Google Pay's can; revisit only
with real device-context handling.

**Pushed to Stage, 15 August 2026 (same `puremed-laser-facelift-winslow`
engagement).** Both booking pages redeployed on the shared engine, plus
`book-liquid-facelift.html` added as a third manifest page. One thing that
doesn't generalise from the earlier deploy note: Stage's automatic
`src`/`href` asset rewrite only matches image extensions
(`png|jpg|jpeg|gif|svg|webp|avif`) — `.js`/`.css` aren't rewritten, and the
`/assets/:engagement/:file` route only matches a flat filename, no nested
paths. So the shared files had to be deployed flat into the engagement's
`assets/` (no `shared/` subfolder) and referenced by **absolute** URL
(`/assets/puremed-laser-facelift-winslow/booking-widget.js`) in the deployed
copies — the canonical `web/` source keeps the relative `assets/shared/...`
paths, which are correct for real deployment; only the Stage copies need the
rewrite, same pattern as the cross-page link rewriting from the first push.

**Still client-side only, no real backend.** This page runs the same in-browser
simulated logic as the internal prototype (fake availability, fake payment, no
server) — `booking-engine/service/` (the real Phases 1-6 backend) has no PureMed
tenant/service/resource seeded and no client frontend built against it yet. The
page keeps an honest preview banner for exactly this reason ("nothing here is
confirmed or charged yet") — do not remove that banner or promote this link as a
real booking channel until it's wired to the real service. That wiring
(seed a PureMed tenant + laser-lift service/resource via the admin API, replace
the in-browser resolver with real `fetch` calls to `/availability`, `/bookings`,
`/documents/sign`, `/screening/submit`, `/bookings/paid`) is separate, larger,
unstarted work — see `booking-engine/booking-engine-plan.md` §11 for the API
shape. "Integrating to the clinical platform" has no system to integrate with
yet either — `clinical-platform/` is scoping-only, no build started.

**Social-media drive POC (8 August 2026).** The microsites are now the front end of
a social POC: each treatment page is intended to get its own Instagram presence and
social engine driving traffic to it (that traffic engine is out of scope and not
built). Two build targets come off the same source:

| Target | Command | Output | Images | Used for |
|---|---|---|---|---|
| `artifact` | `build-microsites.py` | `web/publish/` | inlined data URIs | shareable review URLs |
| `stage` | `build-microsites.py --target=stage` | `web/stage-build/` | file refs | the Stage engagement |

The Stage engagement is **`puremed-micro`**: hub + 7 microsites + the PureMed
booking prototype as a ninth page, all live-editable by Nafisa (copy and images).
It is deliberately separate from `puremed-site`, which remains the surface for the
real website. Procedure: `sops/SOP-PUREMED-003`.

**The booking journey is embedded, not linked.** Clicking any booking CTA opens a
drawer over the microsite carrying the client-facing journey with that treatment
preselected, so the page being sold stays behind it. This is the sales mechanism:
the viewer sees exactly what a client would experience, in place. It relies on
`?svc=<id>&embed=1` on `booking-engine/prototype/_internal-puremed-v1.0.html`, where
`embed=1` strips the prototype to the journey alone (no demo banner, fake site,
rule trace or admin panes). CTAs keep real hrefs, so the drawer is an enhancement
and the link still works without JavaScript.

**Sculptra is the seventh microsite**, rebuilt onto the shared template by
`tools/build-sculptra-source.py`. Its old standalone page
(`web/sculptra landing page/`, own stylesheet and "P" text mark) is superseded.
Never hand-edit `web/puremed-sculptra.html`: that script overwrites it, and its copy
lives in the constants at the top of the script.

Two shared systems were extended to make this work, both additively:
`scripts/stage-autotag.js` gained `--files`/`--relroot` so plain HTML can be tagged
(the Astro globbing path is unchanged), and Stage's live-edit surface gained an
opt-in `allowNavigation` manifest flag so internal links click through instead of
being swallowed by the editor. `puremed-site` does not set that flag and is
unaffected.

`puremed-email-*.md` cover the completed email migration (historical reference).
