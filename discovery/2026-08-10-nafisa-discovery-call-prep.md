# Nafisa Discovery Call, Prep

*Drafted 10 Aug 2026 ahead of a discovery call with Nafisa (PureMed Aesthetics). Purpose
of this call: understand her current (as-is) operating model, systems, and workflow well
enough to (1) design the booking, payment, and document capture system, and (2) start
drafting the target-state SOP afterwards. This doc is Osman's prep, not client-facing.*

*Context already known, sourced from `clinical-platform/puremed-clinical-platform-plan.md`,
`discovery/constraints.md`, `puremed-growth-engagement-plan.md`, and
`.claude/puremed-decisions-log.md`, is marked below so the call doesn't waste time
re-covering it. Where this doc says "confirmed", that's already locked; don't re-ask, just
verify it still holds.*

---

## 1. What's already known (don't re-ask, just confirm still true)

- **Live booking system: Faces Consent** (`facesconsent.com/bookings/puremedaesthetics`),
  referenced from `puremed.uk` today. This is the sole live cutover target.
- **Acuity Scheduling** exists but is confirmed dormant, no live traffic. Unclear if it
  holds any unique historical data or simply predates Faces Consent.
- **Existing web vendor: dermis.ai** currently manages the live site and has offered a
  mobile app. Relationship to the MSS rebuild is unresolved, treat as open.
- **Sister practice: Whitehouse Dental Studio**, holds its own CQC registration. Some
  PureMed treatment is delivered under Whitehouse's registration, not PureMed's.
- **Practitioner regulation**: both treating practitioner and prescriber are confirmed
  GDC-registered dentists. PureMed is **not currently registered with JCCP or Save Face**.
- **Cancellation/reschedule window: confirmed 48 hours** before appointment.
- **Payments**: no confirmed current provider yet, PCI DSS / tokenised handling is a
  requirement for the target system, not a statement about what exists today.
- **Business load**: Nafisa spends roughly 2, 3 days a week on social/content/admin,
  competing with treatment delivery time. That's the reason for this whole engagement.
- **Regulatory horizon**: toxin bookings likely move under formal licensing 2025, 2027
  (currently lightly regulated).

## 2. Purpose of this specific call

Two outputs, in order:

1. **As-is operating model**, mapped in enough detail that the target-state SOP can be
   drafted from it (not from assumptions).
2. **Requirements clarity for the booking + payment + document capture build**, enough to
   scope S2 (booking), S3 (payments), and the consent/document capture pieces of S4/S7
   without guessing.

Don't try to solve or redesign anything on this call. Capture the as-is, flag friction
where Nafisa raises it herself, but resist pitching target-state fixes live. That's the
next session's job.

---

## 3. Questions: the booking journey (patient side)

- Walk me through what happens, step by step, from the moment someone decides they want
  a treatment to the moment they're in the chair. Where do they find you, where do they
  book, what do they fill in?
- What can currently be booked online vs. what always needs a call/DM/WhatsApp first? (Is
  there a triage or consultation gate before certain treatments can be booked directly?)
- What information does Faces Consent actually capture at booking, name, contact,
  treatment, medical history, consent, photo ID, anything else?
- Does every booking require a deposit? How much, and how is it collected today?
- What happens on a no-show or late cancellation, inside vs. outside the 48-hour window,
  in practice (not just policy), does it actually get enforced, is it manual?
- Waitlist: is there one? How does it work if someone wants a slot that's full?
- Do returning patients rebook differently to new patients (e.g. do they use an account,
  or is every booking effectively a fresh guest checkout)?

## 4. Questions: payments

- What payment methods do you actually take today, card online, card in clinic, cash,
  bank transfer? Which is most common?
- Is there a current online payment provider (Stripe, SumUp, something else), or is
  online booking deposit-only with the balance taken in clinic?
- How are refunds handled today, who approves them, how are they recorded?
- Are there package deals, course-of-treatment payments, or memberships, and if so how are
  they tracked (spreadsheet, the booking system, memory)?
- Discount codes or referral pricing, does that exist today, and if so how is it applied
  and reconciled?

## 5. Questions: consent, medical history, and document capture

- Where does the signed consent form actually live today, paper, Faces Consent digital
  form, PDF emailed back and forth?
- Is medical history captured once and updated, or re-taken per visit/per treatment?
- Photo capture: how are before/after and treatment-site photos taken and stored today,
  phone camera, a specific app, direct upload? Who has access to them?
- Is there ever a photo-upload-by-the-patient step (client has flagged this as a wanted
  differentiator), does anything like that exist in any form today, even informally?
- How is prescriber-of-record vs. treating practitioner distinguished on paperwork today,
  is that distinction even made currently, or would it be new?
- For treatments delivered under Whitehouse's CQC registration rather than PureMed's, is
  that distinction tracked anywhere today, or does it just live in Nafisa's head?
- Yellow Card (MHRA adverse event) reporting, has this ever come up in practice? Is there
  any existing process, even informal?

## 6. Questions: prescribing and treatment-specific medication

Nafisa has previously mentioned prescribing specifics tied to particular treatments,
this needs its own pass rather than being folded into the general consent questions,
since it may vary treatment by treatment rather than being one uniform process.

- For each treatment on the current menu, is there a prescription-only medicine (POM)
  involved, toxin being the obvious one, and if so what's the actual process today, is
  it prescribed at consultation, on the day, or in advance of the appointment?
- Does the prescription get tied to a named batch/product, and is that batch/lot number
  recorded anywhere today (this matters for MHRA traceability and Yellow Card reporting)?
- Is the prescriber always the same person as the treating practitioner, or does that
  split by treatment? (The clinical-platform scoping already treats prescriber-of-record
  as distinct from treating practitioner, worth confirming which treatments actually
  trigger that split in practice.)
- Are there treatments where the prescription has to happen at a genuine remote/video
  consultation before the in-person appointment (this is the norm for injectables under
  current prescribing guidance), and if so, how is that consultation currently booked
  and recorded, is it inside Faces Consent at all or handled entirely outside it?
- Is there any per-treatment contraindication or medical-history checklist used today
  (e.g. pregnancy, certain medications, allergies), and does it differ treatment to
  treatment, or is it one generic form for everything?
- Dosage/product records: is what was actually administered (product, dose, site)
  recorded per treatment today, and where, paper chart, Faces Consent notes, memory?
- Are there treatments that require a cooling-off or mandatory time gap between
  consultation and treatment, and is that currently enforced by anything other than
  Nafisa's own judgement?
- Any treatments where a second practitioner or supervision is required by policy, even
  if Nafisa is the one delivering most of them?

## 7. Questions: the practitioner/diary/staff side

- Who else works in the business day to day besides Nafisa, practitioners, reception,
  admin, family? What does each person actually do?
- How is the diary managed today, is Faces Consent the single source of truth for
  availability, or is there a second calendar (paper, Google Calendar, WhatsApp
  coordination) that actually governs what's bookable?
- How are room/resource constraints handled (if relevant, e.g. shared space with
  Whitehouse Dental Studio)?
- Are there recurring hours, or does availability change week to week and get set
  manually?
- How is a practitioner's qualification/insurance/indemnity currently tracked, is there
  any expiry-tracking today, or is that entirely informal?

## 8. Questions: communications

- What actually gets sent to a patient automatically today (confirmation, reminder,
  aftercare), vs. what's sent manually by a person?
- What channel dominates, email, SMS, WhatsApp? Is WhatsApp used operationally
  (rebooking, questions, aftercare) even though it's not a "system"?
- Aftercare instructions, are these standardised per treatment, or improvised per
  patient/practitioner?

## 9. Questions: data, records, and the Faces Consent/Acuity migration

- Roughly how many active patient records are we talking about, order of magnitude?
- Who currently has admin access to Faces Consent? Same question for Acuity.
- Is there anything in Acuity you know isn't in Faces Consent, old clients, a different
  date range, anything unique?
- Historical consent forms, if PureMed's own consent-refresh policy is "reconfirm before
  every treatment", how far back would you want migrated consent to be trusted vs.
  treated as expired on cutover?
- Is there a existing spreadsheet, CRM, or notebook running alongside Faces Consent that
  isn't obvious from the booking system alone? (This is very often where the real as-is
  process lives.)

## 10. Questions: the dermis.ai relationship (handle carefully)

- What exactly does dermis.ai currently do, site hosting/maintenance only, or anything
  operational (booking, CRM, content)?
- Is there a contract or notice period in place?
- Does Nafisa see dermis.ai and this engagement as sequential (replace) or is there a
  world where both continue in some form (e.g. dermis.ai's mobile app alongside an MSS
  booking/payment system)? This shapes whether target-state design needs an integration
  seam or a clean cutover.

## 11. Regulatory/compliance context to sense-check, not interrogate

These are lower priority for this call (they belong more to Osman's own build risk than
to Nafisa's daily operating model) but worth a light touch if time allows:

- Whether Whitehouse's CQC registration is confirmed to cover the specific regulated
  activity, provider, and location PureMed uses it for (flagged as unverified in the
  clinical-platform plan).
- Any appetite/plan to register with JCCP or Save Face, given the 2025, 2027 licensing
  horizon for toxin treatments.

---

## 12. After the call

- Update this doc or a new `as-is-operating-model.md` in `discovery/` with what's
  actually said, don't fold it silently into the constraints doc, keep discovery
  artefacts separate from the locked design constraints.
- Feed anything that changes booking/payment/document-capture scope back into
  `clinical-platform/puremed-clinical-platform-plan.md` and `booking-engine/booking-engine-plan.md`.
  as an update, not a rewrite.
- Only start the target-state SOP once the as-is model is written down and, ideally,
  read back to Nafisa for a sanity check, don't draft target-state from memory of the
  call.
