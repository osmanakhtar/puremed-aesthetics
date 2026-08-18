# PureMed Clinical Platform: Systems Plan and Architecture

Version 0.8 | 17 August 2026 | Owner: Osman Akhtar
(v0.7, 16 August 2026; v0.6, 16 August 2026; v0.5, 16 August 2026; v0.4, 16 August 2026; v0.3, 15 August 2026; v0.2, 10 August 2026; v0.1, 8 August 2026, first draft)

Scope note: this document is a systems-scoping pass over the requirements brief supplied
by PureMed on 8 August 2026 ("aesthetics practitioner system requirements"). It has not
had compliance or legal review. Regulatory references are a starting point for
verification, not settled legal conclusions.

> **v0.8, 17 August 2026: prescribing dentist has signed off, action item 13 closed.**
>
> Shair Mughal has confirmed his sign-off on the toxin booking pathway. This closes the
> single highest-priority open item in this document. **The specific regulatory detail
> behind the sign-off, which GDC-equivalent standard he relies on and the exact allowed
> shape of the online-to-in-person journey, was not captured as part of it, and is left
> open by direction rather than assumed here.** BOOK-001 is signed off in principle, not
> documented against a cited standard; if that level of detail is needed later (a
> compliance review, an insurer query), it still needs asking for directly. No other
> action items are affected. `requirements-register.md` v0.8 carries the row-level note
> (BOOK-001).
>
> **v0.7, 16 August 2026: Nafisa's questionnaire answers close out the prescriber and
> Whitehouse questions.**
>
> Five things resolved. (1) No Wed/Thu conflict: Shair also prescribes alongside Nafisa
> on Thursdays, so toxin prescribing capacity is Wednesday and Thursday; action item 14
> closed. (2) Whitehouse currently holds the entire clinical record, including notes, for
> its two treatments; nothing sits in PureMed's systems today, confirming Stage 1's stub
> was the right call for the current state. (3) Nafisa is a company director of Whitehouse
> Dental Studio; the CQC registration is company-level, not named-individual, which
> reframes action item 1. (4) PureMed's S7 is intended to become the full record for
> Whitehouse-delivered treatments eventually, so the record-ownership question (action
> item 11) is resolved as a phased plan, not a permanent boundary. (5) The indemnity
> insurer question (action item 12) is resolved outright: cover is personal to the
> practitioners, not tied to the business entity, and the same people are named on both
> entities' policies, so the cross-entity gap the item worried about doesn't apply.
> Section 2.4 and action items 1, 11, 12, 14 updated; `requirements-register.md` v0.7
> carries the row-level detail (BOOK-001, BOOK-007, DIARY-005, REC-004).
>
> **v0.6, 16 August 2026: prescribing dentist confirmed, action item 13 resolved.**
>
> Nafisa has confirmed the prescribing dentist is Shair Mughal (her husband), that he
> prescribes in person, and that he is currently available Wednesdays only. This resolves
> action item 13, the single highest-priority sign-off in this document, and confirms
> BOOK-001's in-person-first-assessment reading is already met in current practice. It
> also surfaces an unreconciled conflict against action item 6's 15 August record that
> "the prescriber also works Thursdays": see the new action item 14. No section rewrite;
> the outstanding action items list is updated, and `requirements-register.md` v0.6
> carries the row-level detail (BOOK-001, BOOK-007, DIARY-005).
>
> **v0.5, 16 August 2026: S15 Patient Relationship and Retention added.**
>
> `crm-and-lifecycle-gap-review-2026-08-16.md` Part A found that the commercial
> relationship, leads, attribution, recall and the treatment-plan follow-up loop, falls
> between this document's clinical-only after-appointment scope and `booking-engine-
> plan.md` §14's explicit "everything after the appointment is out" boundary. v0.4 folded
> in the peer review and named this as the next work item. v0.5 adds the component:
> Section 3's table gains S15, and Section 5 gains a subsection on why the gap existed.
> `requirements-register.md` v0.5 carries the row-level detail (CRM-001 to CRM-009).
> Nothing else in this document changes; the Section 9 build posture is unaffected, since
> S15 is additive rather than a resequencing.
>
> **v0.4, 16 August 2026: the independent peer review is now folded in.**
>
> `peer-review-2026-08-15.md` produced twelve findings on 15 August. Until now only
> Finding 10 had reached this document. v0.4 folds in the rest, plus the canon fixes
> proposed in `crm-and-lifecycle-gap-review-2026-08-16.md` Part C3. The posture set in
> v0.3 (Section 9, full replacement brought forward) is unchanged. What changed is the
> regulatory statements underneath it, two of which were wrong in a way that shapes the
> Stage 1 booking journey.
>
> | Change | Source | Where |
> |---|---|---|
> | Remote prescribing: an in-person first assessment is a hard prerequisite for a first toxin prescription, not one option among several | Peer review Finding 1 | 2.2, BOOK-001 |
> | GDC removed cosmetic injectables from Scope of Practice Guidance (Nov 2025); there is no GDC carve-out to point to | Finding 4 | 2.3, DIARY-001 |
> | The CQC dividing line (diagnosed disease/disorder versus cosmetic purpose) is now stated as a test, not an enumerated list | Finding 3 | 2.4, REC-004 |
> | Licensing scheme: confirmed three-tier model, 7 August 2025 consultation response | Finding 5 | 2.9, DIARY-001/PLAN-001/PLAN-002 |
> | Field-level RBAC backed below the application layer | Finding 6 | 3.1, `technical-design.md` 8 |
> | New gaps: individualised risk-discussion record, guest-checkout email verification, offline in-room capture | Findings 7 and 9, plus CRM review B6 | 5.13 to 5.15 |
> | Consent re-basing confirmed correct rather than over-conservative | Finding 11 | 6.4 |
> | Forward-diary migration, previously undesigned | CRM review B3 | 6.6 |
> | Migrated payment ledger labelled as structurally partial | CRM review B8 | 6.3 |
> | Decision gates 1 and 2 marked resolved, reconciling 9.5 against the action-items list | CRM review B2 | 9.5 |
> | Three sign-offs added (Whitehouse controllership, indemnity insurer, prescribing dentist) | Findings 2 and 12 | Outstanding action items 11 to 13 |
>
> Regulatory statements arriving via the peer review were sourced by that reviewer's own
> web search, not verified independently here. They are recorded as the current best
> understanding and still carry this document's standing caveat: verify before build
> sign-off. Finding 1 in particular needs the prescribing dentist's confirmation, and it
> is the single highest-priority sign-off in this document.

> **v0.3, and what changed. Read this before Sections 3 to 9.**
>
> v0.2's Section 9 (10 August 2026) reversed v0.1's premise: it argued Faces Consent
> should stay, with a gap layer (Phase G) built around it, and full replacement (Phase R)
> parked as a later, trigger-based decision that might never fire.
>
> **That posture is itself now superseded, 15 August 2026.** The reason is narrower than
> it looks: the Faces Consent booking flow (a patient cannot land on a specific treatment,
> must scroll the full list, carries more clicks than it needs) was already a known,
> previously-discussed problem, not something the discovery call surfaced. It matters now
> because the replacement booking system is set to become the primary booking entry
> point and the thing that carries deposit payment. A gap-layer deposit fix sitting on
> top of a booking flow this poor undermines its own point. Decision taken 14 August 2026,
> when given the explicit choice between patching the Faces booking front end only,
> bringing forward full replacement, or leaving the scope question for Nafisa: **full
> replacement, brought forward into this phase.** `puremed-systems-proposal.md` was
> rewritten the same day to reflect it.
>
> **Sections 2 to 5 and 8 remain valid** as the regulatory landscape, the component model
> and the journey principles. **Section 6 (migration) is now first-stage work, not a
> later-phase concern**, see the note at its head. **Section 7's phased build order is
> now the closer approximation of the real build order**, since there is no gap-layer
> detour to sequence around; it still needs the record-migration timing pulled earlier,
> which the rewritten **Section 9** does. **Section 9 is rewritten in full** (the "gap
> layer first" posture, the Phase G/Phase R split and the G1-G5 workstream table are
> superseded, not deleted, see 9.7 for what changed and why, kept for the reasoning
> trail). **`technical-design.md`** (new, 15 August 2026) is the system-level architecture:
> data model, integration surfaces, migration mechanics, stack choices, that this plan
> deliberately stays above.

Relationship to existing work: `booking-engine/` already designs the patient-facing
booking journey (multi-tenant, PureMed is tenant 1) and is the more mature artifact for
Requirement Group 1. This document treats booking as one module inside a larger clinical
platform, because the brief goes well beyond booking into clinical record-keeping, which
`booking-engine` explicitly does not attempt. Where the two overlap, this plan defers to
`booking-engine-plan.md` and calls that out rather than re-deciding it. This is a new
project directory (`puremed-clinical-platform/`) rather than an extension of
`booking-engine/`, because an EHR-grade clinical record system is a different risk class
and a different build to a booking widget; flag if you want them merged into one repo
instead.

---

## 1. How to read this document

Section 2 sets the regulatory and best-practice landscape the requirements sit inside.
Section 3 maps the brief into system components (the "what needs to be built"). Section 4
proposes the traceability mechanism, with a starter register in
`requirements-register.md`. Section 5 lists gaps and additions found while analysing the
brief. Section 6 is the migration plan from Faces Consent and Acuity Scheduling, **now
first-stage work**. Section 7 is the phased build plan, close to the real build order now
that replacement isn't sequenced behind a gap layer. Section 8 covers the user-centric
journey design principles. **Section 9 is the current build posture (rewritten 15 August
2026) and is the section to build against**; 9.7 records why it changed from the 10 August
version. `technical-design.md` is the accompanying system architecture: data model,
integration surfaces, migration mechanics and stack. `handoff-validation-prompt.md` is a
self-contained prompt for a second agent to independently validate this document.

The as-is operating model this plan now sits on top of is
`../discovery/2026-08-10-as-is-operating-model.md`. Read it first. This plan describes
where PureMed is going; that document describes where it actually is, and the gap between
the two is the whole engagement.

---

## 2. Regulatory and best-practice landscape

This is the landscape, not settled fact for any specific requirement. UK non-surgical
cosmetics regulation is actively moving (see 2.9), so anything here should be
re-verified before build sign-off.

### 2.1 Data protection
- **UK GDPR + Data Protection Act 2018.** Clinical notes, photographs, medical history and
  allergy data are Article 9 special category (health) data. Requires an identified
  Article 9(2) condition (explicit consent, or "health or social care" where a
  registered health professional is involved), a lawful basis under Article 6, and very
  likely a **Data Protection Impact Assessment (DPIA)** before build, given large-scale
  processing of health data plus systematic monitoring (photography, biometric-adjacent
  imagery). DPIA is not in the brief; see Section 5.
- **ICO guidance on health records retention.** No single fixed statutory retention
  period for private clinic records; industry convention (aligned with NHS Records
  Management Code of Practice, medical defence organisation guidance, and indemnity
  insurer terms) commonly ranges from 8 to 11 years from last treatment for adults.
  **Confirmed with PureMed: retention is set at 11 years.** This must be a configuration
  value on the retention engine (S12), never hardcoded into application logic, since it
  is a policy setting PureMed owns and may need to revise if insurer or GDC guidance
  changes.
- **PECR (Privacy and Electronic Communications Regulations 2003).** Governs marketing
  SMS/email specifically, separately from UK GDPR. Marketing messages need
  opt-in consent distinct from transactional/clinical communications (appointment
  reminders, aftercare, forms) which are not "marketing" and run on a different lawful
  basis. The brief's "separate clinical and promotional communication preferences" is
  right; it should be modelled as two independent consent flags, not one toggle.

### 2.2 Medicines and prescribing
- **Human Medicines Regulations 2012.** Botulinum toxin (Botox and equivalents) is a
  Prescription Only Medicine (POM). It can only be prescribed by an independent
  non-medical or medical prescriber after an adequate individual assessment; a
  prescription cannot be issued algorithmically or by a non-prescriber on the
  practitioner's behalf. If PureMed's injector is not the prescriber, the system needs a
  distinct prescriber-of-record field and a prescribing record separate from the
  treatment note.
- **Remote prescribing guidance.** *Rewritten 16 August 2026, peer review Finding 1. The
  v0.1 to v0.3 text framed an in-person or video first assessment as one acceptable
  option among several ("may require"). That is no longer the right reading and it was
  load-bearing, so the old framing is corrected rather than softened.*

  **Remote prescribing of botulinum toxin without a prior in-person assessment is not
  currently acceptable practice for a first-time prescription.** The NMC's position, in
  force since 1 June 2025, requires a face-to-face consultation before remote prescribing
  of cosmetic injectables is even considered; from July 2026 this tightened further,
  restricting "prescribe and supply" arrangements where the prescriber has never assessed
  the patient in person. GPhC is moving the same way. There is no indication GDC-
  registered dentists sit outside this: a dentist prescribing outside dentistry is bound
  by the same Human Medicines Regulations 2012 "adequate assessment" standard, and that
  standard is what the professional bodies are now interpreting as requiring an in-person
  first assessment for this drug class.

  **What this means for the build, and it is not a process detail.** The online step
  cannot be a consultation substitute that clears a patient to be prescribed. It is a
  triage and eligibility gate whose output is a booked **in-person** appointment with the
  prescriber present, at which the prescribing decision is made. This changes what
  "screening" is for in the booking journey (`booking-engine-plan.md` Section 3, steps 3,
  5 and 6) for toxin services specifically. It also means BOOK-007 and DIARY-005 (the
  prescriber-availability constraint) are doing considerably more regulatory work than
  they were credited with: they are not a scheduling convenience, they are the mechanism
  that makes the in-person requirement structurally true.

  Fillers (currently a medical device, not a POM) are less constrained, but see 2.9.

  **Sign-off required, highest priority in this document:** the prescribing dentist must
  confirm whether a GDC-specific equivalent exists or whether he is relying on the same
  HMR 2012 standard as other prescribers, and must sign off the resulting toxin booking
  pathway before the journey's step sequence is finalised. Outstanding action item 13.
- **MHRA Yellow Card scheme.** Adverse events involving a medicine or device must be
  reportable to MHRA by the practitioner. The brief's "adverse-event and manufacturer
  reporting records" should trace directly to a Yellow Card submission workflow, not
  just an internal log.

### 2.3 Practitioner professional regulation
- **Confirmed: both the treating practitioner and the prescriber are GDC-registered
  (dentists).** GDC standards (Standards for the Dental Team) govern general professional
  conduct, honesty, fitness to practise and indemnity for both.

  *Corrected 16 August 2026, peer review Finding 4. The v0.1 to v0.3 text said "GDC
  guidance permits this provided the practitioner holds appropriate training and operates
  within their declared scope of practice", which is stated the wrong way round.*

  **The GDC's Scope of Practice Guidance update of November 2025 removed non-surgical
  cosmetic injectables from that guidance entirely**, on the basis that this work is not
  the practice of dentistry and therefore is not something GDC scope-of-practice guidance
  governs one way or the other. There is no GDC carve-out to point to, because GDC
  guidance does not reach the activity. Dentists doing this work remain accountable to
  GDC for general professional conduct, but their authority to perform it at all rests on
  generic training, competence and indemnity standards common to anyone performing
  cosmetic injectables, not on a dentistry-specific permission.

  Two consequences. First, the per-practitioner attribute feeding DIARY-001 should be
  named **declared competence and training basis**, not "scope of practice", since the
  latter implies a GDC-defined boundary that does not exist for this activity. Second,
  the sign-off ask changes shape: not "confirm the GDC carve-out applies here" but
  **"confirm what non-GDC standard PureMed is adopting for these practitioners, given
  GDC's own guidance sets none for this activity."** That is outstanding action item 2,
  and it is a harder question than the one previously being asked.

### 2.4 CQC (Care Quality Commission)
- **Confirmed with PureMed: normal cosmetic treatments do not constitute CQC-regulated
  activities.** Where a regulated activity is provided, it is delivered through the
  sister practice, **Whitehouse Dental Studio**, which holds its own CQC registration.
  This changes the architecture, not just the compliance posture: any treatment
  delivered under Whitehouse's registration needs its own provider/location record
  distinct from PureMed Aesthetics, because CQC registration is tied to a specific
  regulated activity, provider and location, not to the practitioner personally. Added
  as REC-004 in the register (Section 4). **Action item, not yet done:** verify that the
  specific regulated activity, provider and location actually delivering the treatment
  are covered by Whitehouse's existing CQC registration; do not assume coverage extends
  automatically just because the same practitioner works across both practices.

- **The dividing line, stated as a test rather than a list** (*added 16 August 2026, peer
  review Finding 3*). What makes a treatment a CQC regulated activity is whether it
  addresses a **diagnosed disease, disorder or injury** (regulated, under the Health and
  Social Care Act 2008 framework) as against a **purely cosmetic purpose** (not
  regulated). That is why toxin for hyperhidrosis (a diagnosed condition) and toxin for
  bruxism/TMJ dysfunction (a diagnosed disorder) route to Whitehouse while cosmetic toxin
  and filler do not. **The same test must be applied to every treatment added to the
  catalogue in future**, rather than treating "hyperhidrosis and jaw toxin" as a closed
  list. Toxin for chronic migraine, to take a live example of something an aesthetics
  clinic plausibly adds, would cross the same line and would silently miss BOOK-008's
  gate if the rule is implemented as an enumeration.

- **Who holds the record for a Whitehouse-delivered treatment, resolved 16 August 2026 as
  a phased plan** (*question added 16 August, peer review Finding 2; resolved same day,
  later session, via a questionnaire to Nafisa*). Verifying registration coverage is a
  coverage check, not a data-governance answer; CQC expects records of a regulated
  activity to be held by the registered provider delivering it. **Today, Whitehouse holds
  the entire clinical record, including notes, for both treatments; nothing sits in
  PureMed's systems.** That settles Stage 1: S7 builds a stub (referral fact,
  provider/location tag) for these two treatments, not a full clinical record, matching
  current reality rather than assuming it. **This is not a permanent boundary: Nafisa
  confirmed PureMed's S7 is intended to become the full record for Whitehouse-delivered
  treatments eventually.** When that consolidation happens, S7 becomes the system of
  record and PureMed becomes the Article 9 controller for that data, which needs its own
  build item at that point, not now. Also resolved: **the CQC registration is held by
  Whitehouse Dental Studio as a company, and Nafisa is a company director**, not a
  named-individual registration, which reframes action item 1 (below) to a company-level
  scope check. Outstanding action item 11 closed on this basis.

### 2.5 Accreditation and best-practice standards
- **JCCP (Joint Council for Cosmetic Practitioners)** and **Save Face** are the two main
  voluntary UK accreditation/registration schemes for aesthetics practitioners and
  premises. Both publish standards for consent (written, treatment-specific, not
  blanket), clinical photography, record-keeping and complaints handling that go beyond
  minimum legal requirements and are the practical source for several brief items (e.g.
  "practitioner reconfirms consent before every treatment", cooling-off periods).
  **Confirmed with PureMed: not currently registered with either JCCP or Save Face.**
  JCCP registration is being considered, so items sourced from JCCP standards should be
  built where practical (the marginal cost of doing so is usually low, since most JCCP
  requirements are just "make the right thing the easy default"), but treated in the
  register as Best-practice, not Regulatory, and never allowed to block a build decision
  the way a Regulatory item would. If JCCP registration is later confirmed, re-classify
  the affected register rows to Regulatory-for-accreditation at that point.

### 2.6 Advertising
- **CAP/BCAP Advertising Codes, enforced by the ASA.** POMs (toxin) cannot be advertised
  to the public by name or by implication (Human Medicines Regs, Article 5 of the
  advertising rules). Before-and-after images are restricted (CAP guidance on cosmetic
  interventions: must not be misleading, must not imply guaranteed results, no
  discounting/time-limited offers on medical procedures in certain circumstances). This
  affects the clinical photography module's marketing-export workflow directly: any
  export path from clinical photos into marketing use needs a compliance gate, not just
  a consent checkbox.

### 2.7 Payments and consumer law
- **PCI DSS** for card handling (use a tokenising payment provider so PureMed's system
  never touches raw card data).
- **Consumer Contracts (Information, Cancellation and Additional Charges) Regulations
  2013 / Consumer Rights Act 2015.** Distance-sold services booked for a specific date
  can be exempt from the standard 14-day statutory cancellation right once performed or
  once the patient agrees to waive it for a service starting within 14 days; deposits
  and cancellation charges must still be fair and clearly disclosed before payment. The
  brief already requires accepting cancellation/refund terms before paying, which is the
  right control; the T&Cs content itself needs legal drafting, not engineering.
  **Confirmed with PureMed: the reschedule/cancellation window is a minimum of 48 hours
  before the appointment.** Inside 48 hours, the cancellation policy applies and the
  booking fee is forfeited. This is a Policy value, not a legal mandate; store it as
  configuration on S2/S3 (per treatment or clinic if PureMed ever wants to vary it), not
  as a hardcoded constant.

### 2.8 Accessibility
- **Equality Act 2010** and, as a practical benchmark, **WCAG 2.2 AA** for the patient
  booking and account journeys. Not in the brief; added in Section 5.

### 2.9 Direction of travel (things that will change the requirement set)
- **The licensing scheme for non-surgical cosmetic procedures is more concrete than this
  section previously said** (*updated 16 August 2026, peer review Finding 5. The v0.1 to
  v0.3 text described it vaguely as "consultation and phased implementation ongoing
  through 2025-2027", which understated it.*)

  The government published a formal **consultation response on 7 August 2025**, over a
  year before this plan's first draft, confirming a specific **three-tier Red/Amber/Green
  risk model** under the Health and Care Act 2022 powers. **Amber tier explicitly
  includes botulinum toxin and facial dermal fillers**, which is PureMed's core menu. The
  confirmed shape requires a **local-authority licence plus oversight from a named,
  appropriately qualified regulated healthcare professional**. Detailed standards are
  expected from a further consultation during 2026.

  **This changes how three register rows should be prioritised, not just how this
  paragraph reads.** The named-professional-oversight requirement is strikingly close in
  shape to what DIARY-001 already proposes, and DIARY-001 is currently classified
  Best-practice on the basis that it is discretionary-but-recommended. Its actual
  regulatory runway is closer to "confirmed policy direction, implementation detail
  pending". PLAN-001 (cooling-off) and PLAN-002 (vulnerable-patient screening) are in the
  same position. All three are annotated in the register as **Best-practice today,
  high-confidence future-Regulatory under the Amber tier**, so build priority reflects
  that rather than treating them as ordinary discretionary items. Building DIARY-001 at a
  discretionary priority risks precisely the 2026-2027 rebuild this section's own advice
  exists to avoid.

  Build the practitioner and premises records so a licence number and expiry can be
  attached later without a schema change.
- **Dermal fillers** are expected to move toward tighter regulation (historically
  classed as a general product / medical device depending on formulation, subject to
  ongoing MHRA review). Do not hardcode "filler = unregulated" anywhere in logic.
- **Under-18 ban.** Since October 2021 (Botulinum Toxin and Cosmetic Fillers (Children)
  Act 2021), it is a criminal offence to administer botulinum toxin or cosmetic fillers
  for cosmetic purposes to a person under 18 in England. **This is not in the brief and
  is a hard blocking requirement**, see Section 5.

---

## 3. System components

Reading the brief as a set of buildable systems rather than a feature list:

| # | Component | Brief section(s) it answers | Core responsibility |
|---|---|---|---|
| S1 | **Patient Identity & Account** | 1 (account, login) | Auth, 2FA, account lifecycle, guest checkout with signup offered post-booking (reversed from the original brief, see 3.1) |
| S2 | **Booking & Scheduling Engine** | 1, 5 (diary) | Treatment catalogue, availability, waitlist, reschedule/cancel rules, calendar sync (already the subject of `booking-engine/`) |
| S3 | **Payments & Billing** | 2 | Deposits, full payment, card/wallet, cash/terminal/bank transfer recording, refunds, discount codes, payment status state machine |
| S4 | **Consent & Medical Questionnaire Engine** | 4 | Treatment-specific conditional forms, e-signature, versioning, PDF, expiry/re-issue, per-treatment reconfirmation |
| S5 | **Automated Communications Engine** | 3 | Templated, multi-channel (email/SMS), per-treatment/practitioner/clinic customisation, delivery/open/failure tracking |
| S6 | **Practitioner Diary & Resource Scheduling** | 5 | Staff/room availability, buffers, recurring hours, manual booking, double-booking prevention, confidential external sync |
| S7 | **Patient Clinical Record (core EHR)** | 6 | The single patient record aggregating everything below; role-scoped search and alerting |
| S8 | **Consultation & Treatment Planning** | 7 | Goals, findings, body/face-diagram annotation, staged plans, acceptance, decline, cooling-off scheduling |
| S9 | **Clinical Treatment Notes** | 8 | Structured, templated, lockable notes; product/batch/lot/dose tracking; amendment audit trail |
| S10 | **Clinical Photography** | 9 | In-app capture with alignment guides, no camera-roll leakage, before/after comparison, dual clinical/marketing consent, access/export audit |
| S11 | **Aftercare, Follow-up & Complications** | 10 | Automated aftercare, PROMs, complication reporting with escalation, adverse-event/manufacturer/MHRA logging |
| S12 | **Security, Identity & Compliance Platform** | 11 | RBAC, 2FA, session timeout, encryption, audit logging, retention engine, SAR/export/delete workflow, DPA register, breach register |
| S13 | **Migration & Integration Layer** | (new) | Faces Consent + Acuity ingestion, reconciliation, cutover |
| S14 | **Requirements Traceability Register** | (new, this is the "traceability" ask) | The golden thread from requirement to regulatory/best-practice source to system component |
| S15 | **Patient Relationship and Retention** | (new, v0.5, `crm-and-lifecycle-gap-review-2026-08-16.md`) | Lead/enquiry records, acquisition source, recall and reactivation, treatment-plan acceptance and follow-up, review requests, discount/referral, the commercial customer-master question. Deliberately not a sales CRM: no pipeline, no deal stages |

S7 is not a separate build so much as the data model and access layer that S4, S8, S9,
S10 and S11 all write into and that S6/reception read a filtered view of. Treat S7 as the
schema and permission boundary, not a thirteenth screen.

### 3.1 Cross-cutting architecture principles
- **One patient identity, many views.** S1 issues one patient ID used by every module.
  Reception's view of S7 is deliberately narrower than the practitioner's (brief:
  "important medical alerts immediately without exposing unnecessary information to
  reception staff"): this is a role-based field-level permission requirement, not just
  a page permission, and should be modelled as such from the start. **Enforced below the
  application layer where practical** (*added 16 August 2026, peer review Finding 6*):
  REC-001 is a Regulatory row in the same weight class as the append-only requirement
  below, and should get the same class of guarantee. Application-layer-only permission
  checks regress quietly, because every new report, export or debug endpoint has to
  re-apply the filter by hand. See `technical-design.md` Section 8 for the mechanism.
- **Guest checkout is allowed; a clinical record is not optional.** Confirmed with
  PureMed, this reverses the original brief's "guest booking should not be available."
  The distinction that keeps this consistent with everything else in this plan: what's
  now optional is the login credential, not the underlying patient record. A guest
  booking still creates the same S7 record, still runs the age gate (ACCT-003), the
  consent flow (S4) and the medical questionnaire, exactly as an account holder's booking
  would, because GDC record-keeping and consent obligations attach to the patient and
  the treatment, not to whether they have a password. What changes is delivery and
  access: a guest's consent-form PDF, aftercare instructions and confirmations still go
  out (S5), but reach them by a verified email/secure link rather than an account login,
  and the system offers account creation post-booking so they can self-serve reschedule,
  view history and manage upcoming appointments going forward. A guest who never
  converts still has a full clinical record on file, accessible to PureMed staff exactly
  as an account holder's would be. Treat MIG-003 in the register (migrated patients must
  claim/create an account) as unaffected by this: it is about not auto-granting login
  access to a legacy record on someone's behalf, which is a different question from
  whether a new booking can proceed without one.
- **Regulated-activity treatments carry a distinct provider/location record.** Where a
  treatment is delivered through Whitehouse Dental Studio under its CQC registration
  rather than under PureMed Aesthetics, S6 and S7 need to record which legal
  provider and registered location actually delivered it, not just which practitioner.
  CQC registration attaches to provider, location and activity, not to the individual
  clinician, so this has to be queryable independently of who was in the room.
- **Append-only clinical record.** S9 and S4 must never allow a destructive edit to a
  locked note or signed consent. Corrections are new, dated, linked entries. This is
  both a professional-standards requirement and the mechanism that makes the audit log
  meaningful.
- **Consent has a lifecycle, not a boolean.** Every consent (treatment, clinical photo,
  marketing photo, marketing comms) is its own row with a status, a version reference,
  an expiry/reconfirmation trigger, and a link to the document version the patient
  actually saw. "Consent" as a single yes/no field on the patient record will not satisfy
  the brief's own requirement that consent be reconfirmed per treatment.
- **Batch/lot traceability as a query, not just a field.** Store product batch/lot
  against every treatment note in a way that supports "which patients received batch
  X" in one query. This is what a manufacturer recall requires and is not explicit in
  the brief; see Section 5.
- **Photography never touches the device camera roll.** In-app capture writes directly
  to encrypted clinical storage; this needs to be a platform-level control (e.g. custom
  camera capture that never calls the OS share/save sheet), not a policy asking staff not
  to save photos manually.
- **Marketing export is a gated workflow, not a copy operation.** Moving an image from
  clinical to marketing use requires: separate marketing consent present, an
  anonymisation/crop step, and a record of who exported it and when. Withdrawing
  marketing consent removes it from marketing surfaces without touching the clinical
  original.

---

## 4. Traceability mechanism

The brief explicitly asks for traceability back to regulatory requirements, obligations
and best practice. The mechanism proposed, modelled on the pattern already proven in
`wealth-onboarding/` (a use-case register that is the source of truth, with every
downstream artifact referencing a use-case ID):

**A requirements register** with one row per discrete system requirement, columns:

| Column | Purpose |
|---|---|
| Req ID | Stable ID, e.g. `CONS-014` |
| Component | Which of S1-S14 owns it |
| Requirement | What the system must do |
| Requirement type | Regulatory / Best-practice (accreditation) / Policy (PureMed's choice) / UX (discretionary) |
| Source | The specific regulation, standard or guidance it traces to |
| Data captured | What's stored, flagging special-category data |
| Depends on | Other Req IDs this needs first |
| Priority | For phased build |
| Verification notes | Anything needing specialist sign-off before build |

A starter version covering the highest-traceability-value rows (the ones with a hard
regulatory or accreditation source) is in `requirements-register.md`. It is deliberately
a representative first pass, not the full 200+ row register the brief's scope would
ultimately need. If you want the full register built out at wealth-onboarding's fidelity
(one `data_*.py` module per component, generated `.xlsx`, automated ref-checking), that is
a follow-up build step, flagged in Section 7.

The **requirement type** column is the load-bearing one, same as in the wealth-onboarding
register: it tells you what PureMed must do regardless of preference (Regulatory), what
is expected by the accreditation bodies they may or may not have signed up to
(Best-practice), where risk appetite genuinely has a choice (Policy), and where the
competitive/experience difference lives (UX).

---

## 5. Gaps and suggested additions

Found while mapping the brief against 2. Ranked by how load-bearing the gap is.

1. **Under-18 age verification and hard block.** Criminal offence to treat under-18s
   with toxin/filler for cosmetic purposes. The brief captures date of birth but never
   states it gates anything. Add: DOB captured at booking, age calculated against
   treatment-type minimum age, hard stop (not a warning) in both the online booking flow
   and the in-clinic manual booking path, with no override.
2. **DPIA and a live Article 9 lawful-basis record**, not just "UK GDPR-compliant
   handling" as a general statement. Add as a build gate: DPIA signed off before S7-S10
   go live, referenced from the requirements register.
3. **Batch/lot recall query.** "Batch or lot number" is captured (brief, clinical notes)
   but there's no requirement to be able to look it up in reverse. Add: a recall
   workflow that, given a batch/lot number, returns every affected patient and can
   trigger the S5 communications engine.
4. **Prescriber-of-record as a distinct field from treating practitioner**, with its own
   remote-prescribing assessment record where the consultation was online. The brief has
   "practitioner and prescriber details" inside clinical notes (good) but the online
   consultation flow (brief section 1) doesn't gate booking a toxin treatment behind an
   adequate prescribing assessment.
5. **Chaperone / third-person-present record** for any treatment in an intimate or
   sensitive area, and for any video consultation involving examination. Standard
   accreditation-body and indemnity-insurer expectation, not in the brief.
6. **Practitioner qualification, insurance and indemnity register**, with expiry
   tracking, and a permission gate: a practitioner cannot be booked for a treatment
   their record doesn't currently authorise them for (qualification lapsed, indemnity
   expired). This also gives the licensing-scheme change in 2.9 somewhere to land.
7. **Service complaint workflow, distinct from clinical complication reporting.** The
   brief's "secure complication reporting" is clinical (S11). A dissatisfied-but-not-
   harmed patient complaint (refund dispute, service quality) needs its own workflow so
   it doesn't get triaged as a medical emergency or silently dropped.
8. **Accessibility standard (WCAG 2.2 AA)** as an explicit non-functional requirement on
   S1/S2, not assumed.
9. **Data Processing Agreement register** for every third-party processor (SMS gateway,
   payment provider, hosting, backup, any AI-assisted transcription for voice-to-text
   notes). The brief mentions DPAs generally; make it a maintained list with renewal
   dates, since it's an ongoing obligation, not a one-off.
10. **Vulnerable-patient / body dysmorphia screening flag**, increasingly expected by
    accreditation bodies and recommended by the Keogh Review, as a discrete question in
    consultation (S8) that can trigger a "treatment not currently appropriate" path
    (which the brief does partially cover via "record when treatment is declined or
    considered unsuitable"): recommend making this trigger explicit rather than relying
    on free text).
11. **Business continuity / clinical record availability during outage.** If S7 is
    unavailable, is there a safe minimum (e.g. read-only cached medical alerts) for a
    practitioner mid-treatment? Not in the brief; worth a policy decision.
12. **Interpreter/language support** for consent taking, given informed consent must be
    genuinely informed. Flag as a policy decision depending on PureMed's patient base.

*Gaps 13 to 15 added 16 August 2026.*

13. **A record of what was actually discussed with this patient**, distinct from the
    signed consent form. (Peer review Finding 7.) CONS-002/003/006 cover the form: what
    was signed, version-locked, audited. S8 covers goals and findings. Nothing captures
    the individualised risk conversation, the specific risks and alternatives discussed
    with *this* patient in their own case. A signed, version-controlled generic consent
    document proves the patient was given standard information; it does not prove what
    was said in the room if a patient later claims nobody told them one specific thing
    about their case. Since insurer and indemnity defence in a dispute typically turns on
    exactly that, and defensibility is the stated purpose of several requirements here,
    this is directly on-point. Add a short structured free-text or checklist field on the
    consultation record, signed and timestamped alongside the rest of the note. Low build
    cost, direct defensibility value. New register row PLAN-005.

14. **Email verification on the guest-checkout path, before any clinical document is
    dispatched.** (Peer review Finding 9.) Section 3.1's guest-checkout argument holds
    everywhere except one phrase: documents "reach them by a verified email/secure link
    rather than an account login". "Verified" is asserted, not designed. Nothing in this
    plan or `technical-design.md` specifies a confirm-your-email loop before consent
    PDFs, aftercare instructions or a record link go to an address typed in at booking
    time. An account login is by construction something only the account holder reaches;
    a link emailed to an unverified address is not. Special-category clinical documents
    going to an unverified address is a live Article 32 exposure specific to the guest
    path, and it is the one part of the 3.1 argument that was never stress-tested. Add:
    guest bookings require a confirm-link click before any clinical document is
    dispatched, and before the booking is treated as confirmed where the document is
    time-critical (pre-treatment consent). New register row ACCT-004.

15. **In-room capture must work without connectivity.** (`crm-and-lifecycle-gap-review-
    2026-08-16.md` B6.) Stage 2 puts bulk photo capture and the two-signature toxin
    prescribing record on a device in a treatment room, to be completed at the point of
    treatment. `technical-design.md` Section 6.3 sequences capture, batch upload and
    deletion assuming connectivity throughout. This plan's own acceptance bar is "fewer
    steps than today, on day one", justified by two proven abandonments of
    technically-correct processes that were slower than the shortcut. **Paper never
    fails.** A prescribing record that cannot be completed because the signal dropped,
    with the prescriber standing there waiting to sign, sends the workflow straight back
    to the paper form, and the entire point of NOTE-005 is that the paper form is the one
    document that leaves the system. One occurrence re-establishes the habit. Requirement:
    local-first capture with deferred sync, signatures captured offline, the record marked
    pending-sync and reconciled on reconnection, with PHOTO-007's device deletion still
    gated on confirmed upload (already correctly sequenced and compatible). Note this is a
    different and larger problem than gap 11 above, which is about read access during an
    outage. Rows NOTE-005 and PHOTO-005 updated accordingly.

### 5.16 Why the CRM gap existed, and why it is closed with S15 rather than a rewrite

*Added 16 August 2026, `crm-and-lifecycle-gap-review-2026-08-16.md` Part A0.*

Neither this document nor `booking-engine-plan.md` was wrong on its own. `booking-engine-
plan.md` §14 carries an explicit risk row scoping a full clinic CRM out: "records, notes,
stock, marketing all sit adjacent and will be asked for. Scope is booking through to
signed record and payment. Everything after the appointment is out." This document's §3
defers booking, scheduling and payments to that document and picks up what happens after
the appointment for clinical purposes only: notes, photographs, aftercare, complications,
retention.

Both boundaries are defensible read separately. Read together, S1-S14 covers the patient
lifecycle from "a booking exists" to "the record is retained for eleven years" and
nothing outside that. There is no component for what happens before a booking exists, and
none for the commercial relationship between bookings, even though the engagement this
plan sits inside exists specifically to drive bookings (`puremed-growth-engagement-
plan.md`). Every mechanism for doing that sat in the two zones neither document covered.

S15 (Section 3) closes this without reopening the Section 9 build posture: it is an
addition to the component model, not a resequencing of Stage 1-4, and it is deliberately
narrower than a sales CRM. The ask is that leads exist as records, that their origin is
recorded, and that there is a loop back to them, not pipelines or deal stages. See
`requirements-register.md` S15 (CRM-001 to CRM-009) for the row-level detail, and
`technical-design.md` Section 4 for the schema this implies.

---

## 6. Migration plan: Faces Consent and Acuity Scheduling

**This is now Stage 1 work, not a later-phase concern.** Under the 10 August posture
(superseded, see 9.7), migration was Phase R and explicitly not scheduled. Under the
15 August posture, the replacement system needs the 475 Faces patient records and the
consent-form library from day one, so 6.2's discovery phase is one of the first things
that needs doing, not a step gated behind months of a gap layer proving itself. Nothing
else below in this section changes on the facts; only its position in the build order
does. See Section 9 and `technical-design.md` Section 5 for the sequencing and mechanics.

Naming confirmed with PureMed: "Faces Connect" in the original brief was a typo for
**Faces Consent** (`facesconsent.com/bookings/puremedaesthetics`), the system currently
live on `puremed.uk` and referenced throughout the existing PureMed build.

**Confirmed with PureMed: only Faces Consent needs a live cutover.** Acuity Scheduling
is completely dormant, not receiving bookings; it may hold historical data worth
checking before decommissioning, but it is not part of the live cutover sequence and
should not be treated as a second active source system. All live Acuity links must be
removed during the changeover (this includes the stale `puremedappointments.as.me/
Winslow` link still in the `puremed.uk` site footer, tracked separately in
`booking-engine-plan.md`).

### 6.1 Source systems
- **Faces Consent** (`facesconsent.com`): current, live booking system. The only system
  needing a live cutover. Holds live booking history and, per the brief, "some patient
  records" (likely consent forms and/or basic demographics, scope to be confirmed by
  data export/API review; PureMed's own account admin access is the fastest way to
  determine what data model it actually holds).
- **Acuity Scheduling** (`puremedappointments.as.me/Winslow`): **dormant, confirmed by
  PureMed.** No live bookings to migrate. Treat as a one-off historical-record check
  (6.2, step 2 only needs to run against Acuity, not a full parallel discovery), then
  decommission and strip every live link to it, including the footer link on
  `puremed.uk`.
  **Revised 10 August 2026.** Dormant, but not empty of value. The call established that
  Acuity holds substantial **notes on long-standing patients** that Faces does not,
  while its contact list is expected to largely duplicate Faces (with some attrition, so
  it will also contain patients PureMed no longer has). The historical check is therefore
  not a formality: **the notes are a migration target in their own right**, handled
  separately from the contact list. See MIG-005 and as-is Section 8.

### 6.2 Discovery phase (do this before any schema decisions)
1. Get admin/owner access to Faces Consent (live) and Acuity (dormant, for the
   historical check) under PureMed's account.
2. Export or API-pull a full data dictionary from Faces Consent: what entities exist
   (patients, appointments, forms, payments, notes, photos), field-level detail, and
   record counts. For Acuity, a lighter pass is enough: confirm what historical data
   exists and whether any of it is unique (not already present in Faces Consent) before
   deciding whether it needs importing at all.
3. Determine actual overlap between the two systems (same patients in both, or genuinely
   separate populations/date ranges), since Acuity may simply predate Faces Consent.
4. Identify what, if anything, in Faces Consent constitutes a signed consent or clinical
   note versus a booking-form answer; this determines whether imported "consent" records
   can be treated as historical-only or need re-confirmation (see 6.4).
5. Confirm data processor status and get a written data export/deletion undertaking from
   Faces Consent (and from Acuity if any historical data is imported) before extraction,
   consistent with the DPA register in Section 5.

### 6.3 Data mapping
Standard entity mapping, to be detailed once 6.2 is complete:

| Source entity | Target component | Notes |
|---|---|---|
| Patient/client record | S1 (account, optional) + S7 (clinical record, demographics only) | Migrated patients are not auto-granted login access to their legacy record; they're offered a claim/create-account prompt (consistent with guest checkout, see 3.1) but the clinical record itself exists and is staff-accessible regardless of whether they ever claim it |
| Booking/appointment history | S2, read-only historical view inside S7 | Not re-entered into the live diary |
| Payment history | S3, read-only historical ledger, **structurally partial, label it as such** | Reconcile totals against source system's own reporting before cutover. **Added 16 August 2026:** five of the six live payment channels (SumUp, Dojo, bank transfer, GoCardless, Klarna) never touched Faces at all (as-is 3.1), so a migrated ledger covers only the Faces-integrated card channel. That is unavoidable, but the pre-migration ledger must be presented as a partial record and never as a statement of what a patient has actually paid |
| Consent/intake forms (if present) | S7 as historical record, NOT S4 live consent | See 6.4 |
| Any clinical notes present | S7 as historical/imported note, clearly labelled as pre-migration and not created in the new structured-template format |

### 6.4 Consent re-basing (the one migration decision with regulatory weight)
The brief itself states consent must not be treated as permanent and must be reconfirmed
before every treatment. This means legacy consents from Faces Consent (or Acuity, if any
historical consent-adjacent data is found there), however they were captured, **should be
imported as read-only historical evidence, not as live,
satisfied consent in the new system.** Any patient migrating in with an upcoming or new
booking gets S4's treatment-specific consent flow run fresh. This avoids a scenario where
the new system silently treats a five-year-old tickbox as current informed consent.

**This is the right call, not an over-conservative one, and the reasoning is worth
stating explicitly** (*added 16 August 2026, peer review Finding 11, which examined this
decision specifically against the brief's "exceptional experience" goal and concluded the
plan under-argued a decision it got right*). Three reasons. Informed consent has to be
current to the treatment being given now, and a patient's understanding of risks,
techniques and products shifts meaningfully over the gap since a legacy signature: some
Acuity records are 3.7 years stale per the 15 August extraction. GDC record-keeping
standards and indemnity-insurer guidance already require reconfirmation before every
treatment regardless of migration history, so this is not an additional burden the
migration invents. And there is no real experience cost, because CONS-007's prefill
mechanism carries the patient's prior answers forward for confirm-or-update: what the
patient actually experiences is a quick review-and-attest step, not a blank-form redo.
The friction a reviewer might expect here does not materialise given how CONS-007 is
designed.

### 6.5 Cutover approach
1. Build S13 ingestion against Faces Consent export files first (not live API sync),
   since booking volume is low enough that a live dual-write layer is unlikely to be
   worth the complexity, confirm against actual volumes from 6.2. Acuity's historical
   data, if any is worth keeping, can be ingested the same way as a one-off batch, on its
   own timeline, since it carries no live-cutover pressure.
2. Run a parallel/shadow period on Faces Consent only: new system live for new bookings,
   Faces Consent kept read-only for lookup, before decommissioning.
3. Reconcile record counts and spot-check a sample of migrated patient records against
   the Faces Consent source before decommissioning it.
4. Remove every live Acuity link (including the `puremed.uk` footer link) as part of the
   same changeover, decoupled from the Faces Consent shadow period since Acuity has no
   live traffic to protect. Coordinate the Faces Consent cutover with the `puremed.uk`
   booking CTA changes already tracked in `booking-engine-plan.md` ("migrate off Faces
   Consent, and kill [stale Acuity link]").
5. Retain an export of Faces Consent's (and, if imported, Acuity's) raw data for the
   11-year clinical retention period even after decommissioning the live systems, per
   Section 2.1.

### 6.6 The forward diary at cutover

*Added 16 August 2026. This was an undesigned gap, surfaced in
`../puremed-growth-engagement-plan.md` on 15 August and carried into this canon by
`crm-and-lifecycle-gap-review-2026-08-16.md` B3.*

6.3 maps booking and appointment **history** to a read-only view inside S7, explicitly
"not re-entered into the live diary". 6.5 keeps Faces live and readable for lookup while
the new system takes new bookings. **Neither covers the appointments already booked into
the future on cutover day**, and on a practice working Wednesday and Friday with a
48-hour cancellation window, that forward diary will be populated and live.

Left as designed, those bookings sit in a system nobody is writing to while the calendar
of record moves elsewhere. That is exactly the failure DIARY-004's single-authoritative-
writer requirement exists to prevent, reintroduced at the one moment it is most likely to
bite.

**Approach: re-enter the forward diary into the new system before cutover, by hand.** At
this volume (a two-day working week, bookings held no further out than the maximum
advance window) the count is small, and every alternative is worse: a two-calendar week
during a live migration, a dual-write layer that MIG-007's volume argument already
rejects, or a cutover that silently loses appointments patients have already been
confirmed for. Sequence it as the last step before the shadow period opens, with a
reconciliation against the Faces diary immediately after, and treat any booking made in
Faces after that reconciliation as an error the shadow period is there to catch.

Confirm the actual forward-booked count with Nafisa before committing to a manual
approach: if it is materially larger than expected, this decision gets revisited rather
than assumed. `technical-design.md` Section 5.2 carries the mechanics.

---

## 7. Phased build plan (indicative, for sequencing discussion)

*This table predates both the 10 August and 15 August posture changes. It is close to
correct again under the 15 August posture (no gap layer to sequence around), except that
migration (Phase 7 here) needs to move much earlier, in line with Section 6's note above.
Section 9.2 gives the current, authoritative phase order; treat this table as the
component-dependency shape rather than the literal sequence.*

| Phase | Focus | Depends on |
|---|---|---|
| 0 | Discovery: DPIA, GDC scope-of-practice sign-off for cosmetic (non-dental) prescribing, verification that Whitehouse's CQC registration covers the specific regulated activity/provider/location, Faces Consent data dictionary (6.2) | none |
| 1 | S1 Identity, S12 core (RBAC/2FA/audit/encryption baseline) | Phase 0 |
| 2 | S2 Booking (extends existing `booking-engine` work), S3 Payments | Phase 1 |
| 3 | S4 Consent engine, S6 Practitioner diary | Phase 1 |
| 4 | S7 Clinical record schema, S8 Consultation planning, S9 Clinical notes | Phase 2, 3 |
| 5 | S10 Clinical photography, S11 Aftercare/follow-up/complications | Phase 4 |
| 6 | S5 Communications engine (can build templates earlier but wire triggers last, since it depends on every other module's state changes) | Phases 2-5 |
| 7 | S13 Migration execution | Phase 4 complete (needs S7 to land data into) |
| 8 | S14 Full requirements register build-out to wealth-onboarding fidelity, if wanted | any time, independent |

---

## 8. User-centric journey principles

The brief's own list (live availability, immediate confirmation, reschedule within
policy, waitlist, calendar add) is already a strong baseline. Three principles to hold
across every journey, since "exceptional experience" was the brief:

1. **Never make the patient re-answer what the system already knows.** Previous
   consent-form answers carry forward for confirm-or-update (brief already states this);
   apply the same principle to demographics, payment methods and communication
   preferences.
2. **Status should always be visible in one place, in plain language.** Payment status,
   form status and appointment status collapse into a single account view; the brief
   lists these as separate capabilities but a patient shouldn't have to check three
   screens to know "what do I still need to do before Thursday."
3. **Every automated message earns a reason to open.** Templates customisable by
   treatment/practitioner/clinic (brief) should carry real information (what to expect,
   not just "your appointment is confirmed"), since generic transactional copy is what
   erodes trust in a clinical context specifically.
4. **Guest checkout removes the biggest conversion-friction point without weakening the
   clinical record.** A first-time patient can book, pay and receive their consultation
   instructions without stopping to set a password first; the account-creation offer
   lands afterward, when they have a real reason to want it (managing an upcoming
   appointment), not as a gate in front of booking. See 3.1 for how this stays
   consistent with GDC record-keeping obligations.

---

## 9. Current build posture: full replacement, brought forward

*Rewritten 15 August 2026, superseding the 10 August version in full. Decision taken by
Osman, 14 August 2026, given the explicit choice of a booking-front-end-only patch, full
replacement brought forward, or leaving the scope call to Nafisa. See 9.7 for what the
10 August version argued and why it no longer holds.*

### 9.1 The posture

**One system replaces Faces Consent: its booking flow, its diary, and its role as the
patient record. This happens in Stage 1, not as a later, trigger-based, may-never-happen
option.**

The reason is narrower than "Faces should go": the Faces booking flow itself is a known,
already-discussed problem (no direct treatment landing, a scroll through the full
treatment list, more clicks than it needs), independent of anything the discovery call
surfaced. It matters now specifically because that flow is set to become the **primary
booking entry point**, and the same route is about to carry **deposit payment**. A
deposit ask sitting at the end of a flow this poor works against the point of building
deposit enforcement at all. Fixing the flow properly, rather than routing a deposit step
through it unchanged, means owning it, which means replacing it.

Once the booking flow is being replaced, the diary and the patient record follow for the
same reason the 10 August posture gave for *not* replacing them: splitting "the thing
patients book through" from "the thing that holds their record" is the parallel-store
problem (old 9.4) in a different shape, and it is worse when the split is permanent by
design rather than a temporary bridge. One system, not two kept in sync indefinitely.

### 9.2 What this phase contains

Six pieces of work, in four stages. `puremed-systems-proposal.md` is the client-facing
version of this; the mapping is exact.

| Stage | Contains | Why here |
|---|---|---|
| **1** | Booking system + calendar (replaces the Faces booking page and the three-writer calendar problem); patient record + consent-form migration (475 records, existing consent library, unchanged content) | Nothing else in this list can go live until the booking system exists and the records it needs to show are in it |
| **2** | Clinical photo pipeline; digital toxin prescribing record | Affect every patient, carry live regulatory exposure, neither waits on a decision from anyone |
| **3** | Deposit and cancellation enforcement | Needs the Stage 1 booking system already live to sit on; gated on Nafisa's deposit-policy decision (9.5) |
| **4** | Aftercare delivery + generated treatment plans over WhatsApp | Depends on the record and booking data the earlier stages establish; loses Nafisa the least by arriving last |

| Workstream | Solves | Register rows | As-is |
|---|---|---|---|
| **Booking + calendar** | Clunky Faces booking flow about to carry deposit weight; three unmanaged calendar writers | BOOK-001-004, 007, 008; DIARY-002-005; SEC-011 | as-is booking-flow note, 8, 4.3, 6.4 |
| **Record + consent migration** | 475 patient records and the consent library need to exist in the new system from day one, not months in | REC-001-004; CONS-001-006; S13 (all MIG- rows) | 8, 2.3 |
| **Clinical photo pipeline** | 7 to 15 images per patient, every patient, stranded on a personal phone | PHOTO-001, 005, 006, 007; SEC-010 | 5 |
| **Digital prescribing record** | Paper toxin form, countersigned, photographed, never uploaded; a growing off-file backlog | NOTE-004, 005, 006, 007; CONS-009 | 4.2 |
| **Deposit and cancellation enforcement** | No deposit on the WhatsApp booking path; no-show policy with no mechanism behind it | BOOK-005, 006; PAY-004, 005, 006, 007 | 2.5, 2.6, 2.7 |
| **Patient comms over WhatsApp** | Aftercare failing nine times in ten; treatment plans built entirely by hand | COMM-004, 005, 006; PLAN-004 | 7.5, 7.6 |

**The photo pipeline and the prescribing record are still the two that matter most** once
the foundation is in, and they are also the two carrying live regulatory exposure rather
than inconvenience: special-category images on an unmanaged device, and POM
administration records with a prescriber's signature existing only as loose paper. That
part of the 10 August reasoning did not change, only what has to be built underneath it
before it can land.

### 9.3 What this phase still does not touch

Narrower than the 10 August list, because migration and the consent-form engine have
moved from "out of scope" to "Stage 1", but real boundaries remain:

- **Consent form content.** The library moves across unchanged. Owning the form *engine*
  (Stage 1) is not the same as rewriting what the forms say, which stays as-is.
- **Memberships, loyalty points and Klarna.** Still entirely inside dermis.ai, still
  unscoped until actions A5 and A6 close. PAY-009, MIG-008.
- **Faces contract exit mechanics.** *What* replaces Faces is decided; *how the account
  itself winds down* (contract terms, notice period, final export, decommission date)
  depends on facts only Nafisa can supply (9.5, item 4) and is a project-management
  question, not a system-design one.

### 9.4 The architectural questions this raises

Two, replacing the old single Faces-API question, which no longer applies in the same
form since the new system is not writing into Faces alongside it, it is replacing it.

1. **What Faces actually holds, at field level, and whether it's exportable.** This
   decides the migration mechanics (`technical-design.md` Section 5), not whether the
   build can proceed at all, since a manual/assisted export is always a fallback if no
   API or bulk-export exists. Admin access to Faces answers this in a sitting.
2. **How long a parallel-running period is needed, and how it's bounded.** Faces cannot
   be switched off on day one of Stage 1: the booking system, calendar and record
   migration need to be live and verified before Faces is retired, not before it's built.
   `technical-design.md` Section 5 sets out the shadow-period approach; the open question
   is how long that period runs and what closes it, which is a risk-tolerance call for
   Nafisa as much as a technical one.

### 9.5 Decisions that gate this phase

*Reconciled 16 August 2026. Items 1 and 2 were still written as open here while the
outstanding-action-items list later in this document recorded both as resolved on 15
August, and the register and client proposal carried a third and fourth position. That
contradiction is closed below; the superseded text is kept in place per this workspace's
dated-confirmed-direction convention.*

Four, of which **two are now resolved and two remain open**:

1. ~~**The deposit contradiction.** Nafisa stated both "everyone pays, always" and
   "discretionary first time, hard on repeat offenders". BOOK-005 and BOOK-006 encode
   the two positions. They are different systems and Stage 3 cannot start until one is
   chosen. (as-is 2.5, 11.1)~~
   **RESOLVED 15 August 2026 (Nafisa): everyone pays a deposit, no exceptions.** BOOK-005
   is the live requirement; BOOK-006's graduated, occurrence-counting model is retired as
   policy. Stage 3 is no longer gated on this. **Two consequences worth carrying
   forward.** First, keep cancellation and no-show occurrences in the event log anyway,
   even though the policy no longer consumes them: "repeat offenders" is a named live
   problem (as-is 2.7) and a universal policy is a decision that can be revisited, but
   the history cannot be reconstructed after the fact. Second, retiring BOOK-006 removes
   one of the four reasons `buy-vs-build-spike-2026-08-15.md` gives as decisive for
   building rather than buying; that spike has been corrected, and the conclusion still
   holds on BOOK-004, BOOK-007, BOOK-008 and the multi-tenant commercial argument.
2. ~~**The working pattern.** Actual days, hours, toxin days and school-run constraints,
   currently held only as low-confidence inference from a mangled transcript. The Stage 1
   booking system cannot configure availability against a guess. (as-is 6.4, 11.1)~~
   **RESOLVED 15 August 2026 (Nafisa): Wednesday 10-3, Friday 1-5**, Friday being the one
   day she can run later if needed. Expansion order when those saturate is **Thursday**
   (the prescriber also works Thursdays), then **Monday**. Build this as an ordered
   capacity-expansion sequence in DIARY-001's availability model, not as a flat list of
   possible days or a static weekly schedule.
3. **What Faces Consent holds and whether it's exportable**, plus who holds admin
   access and the contract/notice terms. Previously an 11.2 "before migration"
   item on a migration that had no date; now a Stage 1 blocker with a date. (as-is 11.2)
   **Partially resolved 15 Aug: admin access confirmed working, and a check of every
   admin-UI location (Settings, Clients, Marketing, Business insights, client profile)
   found no self-serve bulk export function exists. Nafisa has already submitted a data
   request directly to Faces; still open until they respond.** See
   `technical-design.md` §5.1.
   **Escalated to a risk with a plan behind it, 16 August 2026.** The whole of Stage 1's
   migration now depends on the goodwill of the vendor being replaced, with no deadline
   and no priced fallback. Three additions. **The legal lever, stated so it can be used:**
   Faces is a processor, and UK GDPR Article 28(3)(g) requires a processor to return or
   delete personal data at the controller's choice at the end of provision of services,
   with 28(3)(h) obliging them to assist and to make information available to demonstrate
   compliance. PureMed is the controller and can require this; it is not a favour being
   asked. The contract terms nobody has read yet (action item 4) may add notice
   mechanics on top. **A deadline:** set a date at which no useful response becomes a
   formal Article 28 request in writing rather than a support ticket. **A priced
   fallback:** cost assisted or manual extraction at 475 records *before* that date, so
   the decision is made against a number rather than under pressure. Standing constraint
   unchanged: do not re-run the export-capability check or build a scripted UI extraction
   until Faces' response is known to be inadequate.
4. **Qualifications, insurance and indemnity: where held, whether expiry is tracked.**
   Unchanged from 10 August, still unanswered, still gates DIARY-001/006.

### 9.6 What changes in risk profile, and what that means practically

A live migration of 475 real patient records off a system that is actively running the
business is a materially bigger and more sensitive piece of work than the six additive
point-fixes the 10 August posture scoped. Two consequences worth being explicit about
rather than discovering mid-build:

- **The shadow-period approach in Section 6.5 and `technical-design.md` Section 5 is now
  load-bearing, not a nice-to-have.** Faces stays live and readable throughout Stage 1
  until the new system is verified against real records, precisely because a bad cutover
  costs Nafisa the working parts of Faces while trying to fix what it was missing, the
  exact risk the 10 August posture raised (old 9.1, reason two) against a different
  conclusion.
- **The "fewer steps than today, on day one" test (old 9.1, reason three) still applies,
  now to the whole booking and record experience, not just five point fixes.** The two
  proven abandonments in the as-is record (the Dropbox photo routine, the Faces one-at-
  a-time upload) are still the evidence bar. A booking system that is slower or more
  confusing than the Faces flow it replaces fails on day one regardless of what else it
  does right.

### 9.7 Superseded: the 10 August "gap layer first" posture

Kept for the reasoning trail, not as current guidance. The 10 August version argued for
building a gap layer around a live Faces Consent (Phase G: photos, prescribing record,
deposits, calendar, comms) and treating full replacement (Phase R) as trigger-based and
possibly permanent-never, on three grounds: the value was all in the gaps Faces left, not
in things Faces did badly; a partial replacement is worse than no replacement, and Faces
was a system worth keeping, not fighting; and the as-is record shows two proven
abandonments of anything slower than the shortcut it replaced, which a long replacement
build could not clear for months.

**What changed is not that these arguments were wrong.** They correctly describe the
risk of a bad, incomplete replacement. What changed is the scope: the Faces booking flow
itself, not just the five gaps around it, turned out to already be a known problem
sitting directly underneath the deposit work, which the 10 August posture had not been
given as context. Once the booking flow has to be rebuilt anyway to carry deposits
properly, keeping the record and diary split across two systems stops being the safer
option and becomes the parallel-store risk (old 9.4, Option B) made permanent. Section
9.6 above is this document's attempt to carry the genuine risk in the old argument
forward into the new posture, rather than dropping it.

---

## Confirmed on the discovery call (10 August 2026)

*Full record in `../discovery/2026-08-10-as-is-operating-model.md`. This is the subset
that changes this plan. Section references are to that document.*

- **Faces Consent is not the problem this plan originally assumed it was, but its booking
  flow is a live one.** It is the single source of truth for the diary, holds ~475
  patient records, and its consent-form library already matches PureMed's treatment
  menu, all of which move across intact under the current posture. Its booking flow
  (already a known problem, not new to this call) does not, and that is what drives
  Section 9's 15 August revision. (as-is 1, 2.3, 8; booking-flow note added 14 Aug)
- **WhatsApp is the operating surface, not a channel.** Bookings, deposit links, the £25
  new-patient fee, aftercare and treatment plans all run through it. COMM-004 is
  load-bearing, not a convenience. (as-is 7.4)
- **Two booking paths behave differently, and one bypasses everything.** Nafisa books
  WhatsApp requests herself, and that path takes no deposit. BOOK-004 closes it. (as-is 2.1)
- **The toxin prescribing record is on paper and is not reaching patient files.** The one
  document that leaves the system entirely, with a confirmed backlog. NOTE-005 and
  NOTE-006. (as-is 4.2)
- **Clinical photographs live on a personal phone.** 7 to 15 per patient, every patient.
  Both prior attempts at a compliant routine were abandoned for being too slow. PHOTO-005
  to 007, SEC-010. (as-is 5)
- **Prescriber and treating practitioner differ on every toxin treatment**, and toxin is
  bookable only on the prescriber's days. Confirms NOTE-004 is always in play, and adds
  BOOK-007 and DIARY-005 as a hard availability constraint. (as-is 4.3)
- **Two named treatments run under Whitehouse's CQC registration**: hyperhidrosis, and
  toxin to the jaw for clenching. Both are deliberately kept off the online booking path
  today. Gives REC-004 two concrete cases and BOOK-008 its scope. (as-is 4.4)
- **Yellow Card reporting has never been triggered.** No process exists because there has
  never been an occasion for one. CARE-001 is greenfield. (as-is 4.5)
- **Six live payment channels**: Faces integrated card, SumUp links, Dojo terminal, bank
  transfer, GoCardless, Klarna. No single view of what a booking has been paid. PAY-005.
  (as-is 3.1)
- **Marketing runs on manual CSV export into MailChimp**, with unsubscribe state held only
  in MailChimp. COMM-005, and MIG-006 as the migration hazard. (as-is 7.2)
- **Acuity holds unique value after all.** Not just dormant: the notes on long-standing
  patients are worth migrating, even though the contact list largely duplicates Faces.
  Revises Section 6.1. MIG-005. (as-is 8)
- **dermis.ai's scope is far wider than recorded.** Website, mobile app, memberships,
  loyalty points, Klarna, an AI skin scanner, a Meta ads campaign, and an AI voice agent
  calling leads. Nafisa intends to stay with them. SEC-008, PAY-009, MIG-008. (as-is 9)
- **No receptionist, no admin, no second system.** One person absorbs the entire
  operational load. This is the strongest argument for the "fewer steps than today" test
  in Section 9.1. (as-is 6.1)

## Outstanding action items (need a specific answer, not a design choice)

*Items 1 to 3 carried from 8 August. Items 4 onward added 10 August.*

1. **Verify Whitehouse Dental Studio's CQC registration actually covers the specific
   regulated activity, provider and location** that would deliver any PureMed-adjacent
   regulated treatment. Do not assume coverage extends automatically. (2.4.)
   **Updated 10 Aug: two specific treatments now attached to this, hyperhidrosis and jaw
   toxin for clenching, which makes the question concrete rather than hypothetical.**
   **Updated 16 Aug (Nafisa): the registration is held by Whitehouse Dental Studio as a
   company, and Nafisa is a company director, not a named-individual registration.**
   Reframes the question from "does this specific person's registration cover it" to
   "does the company's registration scope cover these two activities at this location."
   Still open; needs sight of the actual registration document.
2. **Confirm the scope-of-practice and training-record standard** PureMed wants applied
   to its GDC-registered practitioners performing cosmetic, non-dental botulinum
   toxin/filler work, to populate DIARY-001's qualification register correctly. (2.3.)
   **Updated 10 Aug: asked on the call, answer not captured. Blocks DIARY-006.**
   **Updated 15 Aug: still open, but Nafisa has supplied two adjacent data points.**
   Qualification and indemnity records currently exist only on her laptop (no central
   store today, source for the initial DIARY-006 migration). Indemnity auto-renews
   annually, with the insurer emailing a reminder a few weeks ahead of renewal, which
   is the real-world signal the `practitioner_competencies` expiry-tracking design
   (peer review Finding 10) should key off, not a fixed annual date assumption.
3. **Complete the DPIA** before S7-S10 (clinical record, consultation planning, notes,
   photography) go live. (2.1, SEC-001.) **Updated 15 Aug: the record and consent-form
   migration is Stage 1 work, so the DPIA is a Stage 1 blocker, not a later-stage one.**
4. **Establish what Faces Consent holds at field level and whether it's exportable**,
   plus who holds admin access and the contract/notice terms. **Updated 15 Aug: this is
   now a Stage 1 migration-mechanics question (`technical-design.md` Section 5), not a
   gating architectural choice**, since the new system replaces Faces rather than
   writing into it, so the answer shapes *how* migration runs, not *whether* the build
   can start. **Partially answered 15 Aug (Nafisa): she is the Faces admin.** Field-level
   export capability and contract/notice terms still open.
   (9.4.)
5. **Resolve the deposit-policy contradiction.** One answer, not two. (9.5, as-is 2.5.)
   **RESOLVED 15 Aug (Nafisa): everyone pays a deposit, no exceptions.** PAY-005/PAY-008
   design against a single universal deposit policy.
6. **Confirm the actual working pattern**: days, hours, toxin days, school-run
   constraints. Currently low-confidence inference. (9.5, as-is 6.4.) **RESOLVED 15 Aug
   (Nafisa): Wednesday 10-3, Friday 1-5 (Friday is the one day she can run later if
   needed). Next day to open when Wed/Fri saturate is Thursday, because the prescriber
   also works Thursdays; after Thursday saturates, Monday opens next.** This is a
   real, ordered capacity-expansion sequence (Wed/Fri fixed → Thu → Mon), not a flat
   list of possible days: DIARY-001's availability model and the calendar/diary
   consolidation work should represent it as staged capacity tiers, not a static
   weekly schedule.
7. **Legal review of the blanket "no refunds" term** against CRA 2015 unfair-terms
   provisions. It appears in the consent forms, the website copy and the T&Cs, so one
   review covers all three. (PAY-008, as-is 3.2.)
8. **Take a position on the dermis.ai AI voice agent.** It presents as human to patients
   under PureMed's name and Nafisa's registration. (SEC-009, as-is 9.2, 12.3.)
9. **Map the dermis.ai app architecture** via the back-end login (A5) and the onboarding
   call (A6). Until then memberships, loyalty points and Klarna cannot be scoped.
   (as-is 11.3.) **Updated 15 Aug: Nafisa has added the dermis.ai login to the shared
   Google Sheet, so A5 is now unblocked.** A6 (onboarding call) still to arrange.
10. **Retire the ChatGPT inbox-to-calendar automation** as part of the Stage 1 booking
    and calendar build, with a test-email trial first so the two writers never collide.
    (SEC-011, DIARY-004, as-is 8, A8.)

*Items 11 to 13 added 16 August 2026, from peer review Findings 2 and 12, as sign-offs
needing a named third party rather than a design decision anyone here could take; item 14
added same day to flag a scheduling discrepancy. Later the same day, a questionnaire to
Nafisa resolved 11, 12 and 14 outright and partially resolved 13. 17 August: item 13
closed too, Shair Mughal has signed off directly. All four items in this block are now
closed.*

11. **Establish who holds the clinical record, and who is the controller, for a treatment
    delivered under Whitehouse's CQC registration.** Does the record live in PureMed's
    S7, in Whitehouse's own system, or in both with one designated authoritative? This is
    a different question from action item 1 (does the registration cover the activity),
    which is a coverage check and does not answer it. **Blocks treating REC-004's schema
    as settled**, and REC-004 is Stage 1. (2.4, peer review Finding 2.)
    **RESOLVED 16 August 2026 (Nafisa), phased.** Today, Whitehouse holds the entire
    clinical record, including notes, for both treatments; PureMed's systems hold none of
    it, which settles Stage 1 as a stub (referral fact, provider/location tag), matching
    reality rather than assuming it. Not permanent: **Nafisa confirmed PureMed's S7 is
    intended to become the full record for Whitehouse-delivered treatments eventually**,
    a later, not-yet-scheduled consolidation, at which point PureMed becomes the Article 9
    controller for that data and this needs revisiting as its own build item. See
    `requirements-register.md` REC-004.

12. **Ask PureMed's professional indemnity insurer about the Whitehouse cross-referral
    model specifically.** Does PureMed's own indemnity cover facilitating a booking for a
    regulated activity ultimately delivered by a separate legal entity, and does the data
    flow from PureMed's booking system into Whitehouse's delivery need disclosing to
    either insurer? This needs an insurer's answer, not a registration lookup. (Peer
    review Finding 12.) **RESOLVED 16 August 2026 (Nafisa): not applicable, no insurer
    review needed.** Indemnity cover is personal to the practitioner performing the
    treatment, not tied to which business entity it's billed through, and the same two
    people (Nafisa and Shair) are named on both PureMed's and Whitehouse's policies and
    business structures. The cross-entity liability gap this item was written to check
    for doesn't exist here, since there is no genuinely separate third party involved.

13. **Get the prescribing dentist's explicit sign-off on the toxin booking pathway**,
    given that remote prescribing without a prior in-person assessment is not currently
    acceptable practice for a first prescription (2.2, rewritten). Specifically: confirm
    whether a GDC-specific equivalent to the NMC position exists or whether he relies on
    the same HMR 2012 "adequate assessment" standard, and confirm what the
    online-screening-to-first-prescription journey is actually allowed to look like.
    **This is the single highest-priority sign-off in this document**, because it shapes
    the primary Stage 1 booking journey rather than a downstream detail: it decides
    whether the online step is a consultation substitute or an eligibility gate in front
    of an in-person prescriber appointment. (2.2, BOOK-001, peer review Findings 1 and
    12.) **PARTIALLY RESOLVED 16 August 2026 (Nafisa): the prescribing dentist is Shair
    Mughal, her husband, who prescribes in person and is currently available Wednesdays
    and Thursdays.** This confirms the in-person-assessment reading is already current
    practice, not just design intent, and converts BOOK-007/DIARY-005 into a hard,
    currently two-day constraint on toxin bookings. **RESOLVED 17 August 2026: Shair
    Mughal has signed off directly on the toxin booking pathway, closing this item.** The
    specific regulatory detail behind that sign-off, the GDC-equivalent standard and the
    exact allowed shape of the online-to-in-person journey (the two specific questions
    above), was not captured as part of it and is left open by direction rather than
    assumed here. Treat BOOK-001 as signed off in principle by the prescriber himself, not
    as documented against a cited standard; if that level of detail is needed later (a
    compliance review, an insurer query), it still needs asking for directly.

14. **Reconcile the Wednesday-only prescribing fact (item 13) against item 6's 15 August
    record that "the prescriber also works Thursdays".** **RESOLVED 16 August 2026
    (Nafisa): no conflict.** Shair can also prescribe alongside Nafisa on Thursdays, so
    both the 15 and 16 August statements were correct; toxin prescribing capacity is
    Wednesday and Thursday, not Wednesday only. Item closed.

## Open questions for PureMed / Nafisa (not resolvable from the brief alone)

- **Age legislation compliance is a firm requirement.** ACCT-003 (hard age gate against
  the Botulinum Toxin and Cosmetic Fillers (Children) Act 2021) stands as a must-have,
  not a discretionary addition. No override path, no policy flexibility on this one.
- **"Faces Connect" was a typo for Faces Consent.** Faces Consent (`facesconsent.com`)
  is confirmed as the only live booking system needing cutover.
- **Both the treating practitioner and the prescriber are GDC-registered.** Section 2.3
  updated; see the flagged scope-of-practice sign-off item below.
- **PureMed is not registered with JCCP or Save Face; JCCP registration is being
  considered.** Section 2.5 updated: JCCP-sourced requirements are built where
  practical but classified as Best-practice, not Regulatory, in the register.
- **PureMed's normal cosmetic treatments are not CQC-regulated activities.** Where a
  regulated activity is needed, it runs through the sister practice, Whitehouse Dental
  Studio, under its own CQC registration. Section 2.4 and 3.1 updated with the
  provider/location distinction this requires; see the verification action item below.
- **Acuity Scheduling is completely dormant**, no live bookings. Only a historical-data
  check is needed before full decommissioning; all live Acuity links removed at
  changeover. Section 6 updated to treat Faces Consent as the sole live cutover.
- **Clinical record retention is 11 years, held as configuration, not hardcoded.**
  Section 2.1 and REC-002 updated.
- **Reschedule/cancellation window is a minimum of 48 hours before the appointment**;
  inside that window the cancellation policy and loss of booking fee apply. Section 2.7
  updated.
- **Guest checkout is required, with account signup offered after booking**, reversing
  the original brief's "guest booking should not be available." Section 3.1 updated with
  how this stays consistent with the clinical-record and consent requirements: the login
  credential becomes optional, the underlying patient record and consent flow do not.
- **The PureMed treatment and waiting room are exclusive to PureMed, no one else works
  there.** Confirmed 15 Aug (Nafisa), answering the peer review's Finding 10
  (`peer-review-2026-08-15.md`) on multi-site/multi-brand data segregation: at current
  scale there is one PureMed room and no space-sharing with Whitehouse. The one
  capacity-expansion path Nafisa named is that the waiting room can convert into a
  second treatment room once busy enough, with Whitehouse's downstairs reception then
  used as shared waiting area. `provider_locations` should model this as PureMed having
  its own dedicated location record, with the waiting-room-to-treatment-room conversion
  and the shared-reception fallback captured as a future-capacity note, not built as a
  live multi-tenancy requirement now.

Two genuinely still-open, not yet asked of Nafisa:

- What is PureMed's risk appetite on any remaining Policy-type requirements in the
  register not yet given a specific value (e.g. exact SAR turnaround time, session
  timeout duration)?
- For guest checkout: should there be any limit on how many guest bookings a single
  unclaimed email/phone can make before the system prompts account creation more
  firmly, or is an open-ended guest path acceptable indefinitely?

*(A shorter duplicate of the outstanding-action-items list, carried
over unedited from v0.1, was removed here 15 August 2026 for being stale against the
fuller, updated lists earlier in this document, see "Outstanding action items" and
"Open questions for PureMed / Nafisa" above.)*
