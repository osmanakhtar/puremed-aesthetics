# PureMed booking journey — UX/UI review

*Drafted 15 August 2026, ahead of a peer-review pass and implementation. Scope:
the booking widget itself (`booking-engine/prototype/_internal-puremed-v1.0.html`,
forked per-treatment as `web/book-<treatment>.html`), not the booking-engine's
production backend (`booking-engine/service/`, still unwired — see `CLAUDE.md`).
Worked example throughout: **Liquid Facelift** (`svc: 'liquid-facelift'`, £750,
75 min), per Osman's brief. The laser-facelift page already live on Stage is the
baseline this review is measuring against.*

## 1. What exists today

The booking widget is a fork of `booking-engine/prototype/_internal-puremed-v1.0.html`
— itself the *internal, never-publish* demo built for showing Nafisa her own
clinic, reused across three fictional MSS case-study tenants before that. Three
problems fall directly out of that lineage:

1. **Brand.** The widget's CSS variables (`--navy:#23476A`, `--gold:#C6A77D`,
   Cormorant Garamond + Inter) are the *internal demo's* palette, not PureMed's
   live brand. `book-laser-facelift.html` overrides the variables at the top of
   the file, which reskins colour and font correctly, but the widget's actual
   *componentry* — card-heavy service list, boxed notices, a step rail styled
   like a settings panel — was never redesigned against the live site's actual
   patterns the way the microsite was this session (asymmetric splits, plain
   eyebrows, de-boxed link lists, the real footer). It looks like a themed
   internal tool, not a page that belongs next to `laserfaceliftwinslow.html`.
2. **No shared chrome.** The microsite and the booking page each carry their own
   header/footer markup, hand-copied rather than shared. They already agree
   (same nav, same footer, same brand tokens) only because I copied them by
   hand this session — the moment either changes, they will drift.
3. **No payment reality.** The payment step is locked demo card fields only.
   No Apple/Google Pay treatment, which the systems proposal to Nafisa (10 Aug)
   named as an explicit want (`puremed-systems-proposal.md`: "Apple Pay and
   Google Pay are an explicit want").

Separately, two behavioural gaps named directly in this brief:

4. **Landing behaviour.** `openWidget('liquid-facelift')` does pin `S.svcId`,
   highlight the card, and show the right price on the footer bar — but it
   still renders the full TREATMENT step (service list, category chips) as
   step one, requiring a click through a screen showing *every other
   treatment* before the client reaches anything about the one they came for.
   For a page whose entire premise is "you already know what you want," that's
   a real tax on the journey it's supposed to shortcut.
5. **Pricing on arrival.** Every deep-linked page currently walks straight into
   the full treatment price and deposit maths. For a client who hasn't spoken
   to the clinic yet, that's the first thing they see, before any reassurance
   that a consultation exists to check suitability first.

## 2. Proposed changes

### 2.1 Deep-link should skip the treatment step

When a page arrives with a service already carried (`?svc=` or a hardcoded
default in a forked file), the widget should open **on step two**, not step
one, with the selected treatment shown as a locked, non-editable context strip
("Booking: Liquid Facelift, Dermal Fillers · £750 · 75 min · change") rather
than a still-editable card list. "Change" is a real link back to the full
picker, so nothing is a dead end — it just isn't the default view. This is a
small, contained change to `openWidget()`/`render()`'s step-selection logic,
not a rebuild.

### 2.2 Default service for context-free entry: Skin Consultation, not the treatment

This isn't in tension with 2.1, it's a different entry point. Two arrival
paths need two different defaults:

- **Treatment-specific page** (`book-liquid-facelift.html`, reached from the
  Liquid Facelift microsite or a `.bucks` Instagram bio): opens pinned to
  Liquid Facelift, per 2.1. The client already chose this by clicking through
  from a page about it.
- **Generic "Book now"** (the nav CTA pattern, or a WhatsApp link with no
  treatment context): should default to **Skin Consultation** — free or
  lowest-priced, per the catalogue — not silently pre-select whatever
  treatment happens to be hardcoded. A client who hasn't been told a price yet
  should not be walked toward paying a treatment deposit for something they
  haven't discussed. This matches the existing `RULE-004`-style reroute logic
  already in the widget (injectables with no prior consultation reroute to
  consultation) — it's the same principle applied to the entry point, not new
  machinery.

### 2.3 Full brand pass on the widget componentry, not just variables

Beyond swapping colour/font variables (already done), rebuild the widget's
visual language to match the patterns already established on the microsite
this session:

- Service list rows → the microsite's `.plain-links` treatment (divider rules,
  no card borders) instead of boxed `.svc` cards, consistent with the
  "de-box, don't card-overuse" direction from the earlier design pass.
- Step rail → plain uppercase small-caps labels with a single underline on the
  active step (matches the microsite's `.eyebrow`/section-label language)
  rather than the current pill-tab look.
- Notices (`.notice.reroute/.block/.info/.ok`) → restyled to the brand palette;
  currently still using the internal demo's amber/red/blue tokens, which don't
  exist anywhere else on the live pages.
- Buttons → the microsite's `.btn` shape (10px radius, shimmer-on-hover)
  everywhere the widget currently uses `.btn-pm`'s own separate button style.

### 2.4 Shared header/footer component

Extract the `.mb-header`/`.mb-preview-note`/`.mb-footer`/`.wa-sticky` block
(currently duplicated between the microsite and the booking page) into one
include point. Given the no-build-step, single-file convention this project
has followed throughout (deliberate, per `booking-engine-plan.md` §11's "no
build step" reasoning for the public prototypes), a literal shared file isn't
available without introducing a build step. Pragmatic alternative: keep them
as copy-pasted blocks but mark them clearly (`<!-- SHARED CHROME: keep in sync
with laserfaceliftwinslow.html -->`) and treat any nav/footer change as a
two-file edit, checked in the same session. A real shared partial is a
justified reason to introduce a lightweight build step later, not now.

### 2.5 Stripe Elements + Google/Apple Pay, still a mockup

Since `booking-engine/service/`'s real Stripe integration isn't wired to any
client page yet (per `CLAUDE.md`'s "still client-side only" note), this stays
a faithful **UI mockup**, not a real integration — same honesty posture as the
rest of the page. Concretely:

- Replace the current locked plain `<input>` card fields with a Stripe
  Elements-styled card row (the real Stripe Elements visual language: a single
  bordered field with an inline card-brand icon, not three separate boxes) —
  visually accurate, still non-functional/locked, same "demonstration only"
  banner.
- Add a **Google Pay button** above the card fields, built to Google's actual
  button spec (black pill, white "G Pay" wordmark, not a generic button with
  text) since that's a real brand asset with real usage rules — clicking it in
  this mockup simulates the same "Authorised" state the card flow produces,
  clearly labelled simulated.
- Apple Pay is named in the systems proposal too, but Apple Pay's real button
  can only render correctly on Safari/an Apple device context in production;
  for a cross-browser mockup I'd represent it the same way as Google Pay
  (static button, simulated click) rather than trying to fake device
  detection. Flagging this as a mockup-fidelity trade-off, not hiding it.
- Both buttons sit **above** the card fields (matches Stripe's and most
  payment UIs' convention: express checkout methods first, card as fallback).

### 2.6 Liquid Facelift as the second worked example

Build `web/book-liquid-facelift.html` from the corrected pattern above (not
cloned from the laser-facelift file with find/replace — cloned from a
*template* once 2.1–2.5 are settled, so both pages share the fixed pattern
rather than the laser page needing a second retrofit). Confirms the pattern
genuinely repeats before a third treatment is asked for.

## 3. What I'm deliberately not doing

- Not wiring the real `booking-engine/service/` backend. That's the larger,
  separate task named in the 15 Aug reconciliation session's next steps
  (tenant/service seeding, real API calls) — out of scope for a UX pass.
- Not rebuilding `puremed-liquid-facelift.html` (the old-template microsite
  that already exists in `web/`) as part of this pass — that's a content/copy
  job matching the laser-facelift redesign pattern, and is a reasonable
  next piece of work but is a separate task from the booking journey itself.
- Not inventing real deposit percentages, session counts, or downtime claims
  for Liquid Facelift beyond what's already in the catalogue (£750, 75 min,
  25% studio-assumption deposit, same placeholder status as laser lift).

## 4. Peer review, incorporated

An independent review (fork, verified claims against the actual code before
answering) returned five substantive points, all accepted:

1. **§1.4 was understated.** Verified: `openWidget()` sets `S.step='service'`
   unconditionally after `selectService()`, so the widget doesn't "still
   render" the treatment step on deep-link, it **forces** it every time, with
   no path that skips it. Corrected understanding, same fix (§2.1), just a
   blunter bug than described.
2. **§2.4's "no build step forces hand-sync" claim was wrong, rejected.** A
   shared external CSS file loaded by `<link>` needs no build tooling and
   directly removes the drift risk, especially now that a second forked page
   (§2.6) doubles the surface for exactly the kind of silent divergence this
   flagged. **Extended past the review's ask**: the same drift risk applies far
   more to the ~1300-line widget JS engine duplicated between forked pages than
   to the small chrome CSS block, so both get extracted to shared files —
   `assets/shared/booking-widget.js` (engine + rules + SERVICES data) and
   `assets/shared/chrome.css` (header/footer/nav/wa-sticky), loaded by every
   forked page. Per-page files shrink to brand tokens + a small init call.
3. **§2.5 Apple Pay mockup: accepted the stronger recommendation.**
   A generic simulated button under a real payment brand's name is closer to
   misrepresentation than the demo card fields elsewhere on the page, which are
   at least honestly generic. **Apple Pay is dropped from this pass** rather
   than shipped mislabelled — flagged as deferred, needs real device-context
   handling to do honestly. Google Pay is built (its Web API is testable
   cross-browser, so a labelled preview button doesn't carry the same
   device-exclusivity deception risk).
4. **§2.2 reversed: no silent default.** Pre-selecting Consultation for
   context-free entry is the same category of problem as pre-selecting a
   treatment — presenting an unmade choice as made. Fixed shape: context-free
   entry shows the **full picker**, unchanged, with Consultation sorted first
   and a small callout ("New here? Start with a consultation") above the list.
   Nudges without deciding for the client.
5. **§1's `RULE-004` analogy softened.** The existing reroute logic fires
   *after* screening answers, reacting to information the client gave, not at
   an empty landing state — a weaker precedent than §2.2 implied. Noted, no
   code consequence.

§2.1 and §2.3/§2.6 were explicitly endorsed as-is by the review.

## 5. Risks / open questions for the peer-review pass

- Does skipping the treatment step on deep-link ever strand a client who
  clicked the wrong CTA? Mitigated by the "change" link in 2.1, but worth a
  second opinion on whether that's discoverable enough.
- Is defaulting generic entry to Consultation actually right, or should it
  default to nothing selected (today's un-pinned landing view)? These aren't
  the same: "default to Consultation" pre-commits a choice the client didn't
  make; "no default" shows the full picker. Worth checking which is less
  presumptuous.
- Google Pay button mockup: real brand guidelines are exacting about colour,
  radius and clear-space. Getting this visibly wrong on a page that also
  claims to be a rigorous, verifiable system undercuts the whole pitch — this
  needs to be right or not attempted.
