# PureMed Clinical Platform: Requirements Traceability Register (starter)

Version 0.8 | 17 August 2026 (v0.7, 16 August 2026; v0.6, 16 August 2026; v0.5, 16 August 2026; v0.4, 16 August 2026; v0.3, 15 August 2026; v0.2, 10 August 2026; v0.1, 8 August 2026)

## v0.8 change note, 17 August 2026: prescribing dentist has signed off

Shair Mughal has confirmed his sign-off on the toxin booking pathway, closing plan action
item 13, the document's single highest-priority open item. **The specific regulatory
detail behind the sign-off (which GDC-equivalent standard he relies on; the exact allowed
shape of the online-to-in-person journey) was not captured and is left open by
direction, not assumed here.** Treat BOOK-001 as signed off in principle, not as
documented against a cited standard. If that level of detail is needed later (a
compliance review, an insurer query), it still needs to be asked for directly. Row
touched: BOOK-001.

## v0.7 change note, 16 August 2026: Nafisa's answers close out the prescriber and Whitehouse questions

Nafisa answered the questionnaire drafted in the previous session. Five things resolved:

1. **No Wed/Thu conflict.** Shair can also prescribe alongside Nafisa on Thursdays, not
   only Wednesdays. Both the 15 Aug and 16 Aug statements were correct; there was no
   contradiction, just an incomplete first read. Toxin prescribing capacity is Wednesday
   **and** Thursday. Rows BOOK-001, BOOK-007, DIARY-005 updated; plan action item 14
   closed.
2. **Whitehouse currently holds the entire clinical record**, including notes, for the
   two treatments delivered under its registration. Nothing is held in PureMed's systems
   today. Confirms the Stage 1 stub-only default was the right call for the current state,
   not just a safe guess.
3. **Nafisa is a company director of Whitehouse Dental Studio; the CQC registration is
   held by the company, not a named individual.** Reframes action item 1 from "does an
   individual's registration cover this" to "does the company's registration scope cover
   these specific regulated activities at this location", still open but now asked
   correctly.
4. **PureMed's S7 will become the full record for Whitehouse-delivered treatments
   eventually.** This is a phased migration decision, not a permanent boundary: Stage 1
   stays a stub (referral fact and provider/location tag only); full record consolidation
   is future work, not yet scheduled. REC-004 updated accordingly.
5. **The indemnity insurer question (action item 12) is resolved, not merely deferred.**
   Nafisa's indemnity cover is personal (covers her and Shair as the practitioners doing
   the treatment), not tied to which business entity the treatment is billed through, and
   the same two people are named on both PureMed's and Whitehouse's policies and business
   structures. The cross-entity liability gap the item worried about doesn't apply here.

## v0.6 change note, 16 August 2026: prescribing dentist confirmed, plan action item 13 resolved

Nafisa has confirmed the prescribing dentist is **Shair Mughal** (her husband), that he
prescribes **in person**, and that he is currently available **Wednesdays only**. This
resolves plan action item 13, the single highest-priority sign-off in the document, and
converts BOOK-007/DIARY-005 from a scheduling-convenience framing into a concrete,
currently single-day constraint. It also surfaces an unreconciled conflict against action
item 6's 15 August record that "the prescriber also works Thursdays": see BOOK-001's
notes and new action item 14 in the plan. Rows touched: BOOK-001, BOOK-007, DIARY-005.

## v0.5 change note, 16 August 2026: S15 Patient Relationship and Retention added

`crm-and-lifecycle-gap-review-2026-08-16.md` Part C2 proposed a new component so leads,
attribution, recall and the commercial relationship have somewhere to live that is not a
footnote on S5 or S8. v0.4 named this as the next work item, deliberately sequenced
behind the peer-review fold-in. That prerequisite is done, so v0.5 adds the component now.

| Change | Rows | Source |
|---|---|---|
| New component: leads/enquiries as a first-class record | CRM-001 | CRM review A1 |
| SAR, retention and transparency obligations extended to lead data | CRM-002 | CRM review A1; extends SEC-006 |
| Acquisition source on bookings and patients | CRM-003 | CRM review A2 |
| Recall interval and derived next-due date | CRM-004 | CRM review A3 |
| Recall/reactivation messages classified at template level, not per-send | CRM-005 | CRM review A3; interacts with MIG-009 |
| Treatment-plan acceptance state and follow-up | CRM-006 | CRM review A4; extends PLAN-004 |
| Post-treatment review request, suppressed on complication | CRM-007 | CRM review A6 |
| Discount codes and referral credit | CRM-008 | CRM review A6 |
| Commercial customer-master decision | CRM-009 | CRM review A5 |

This is deliberately not a sales CRM: no pipeline, no deal stages. The rows below ask
only that the people exist as records, that their origin is recorded, and that there is a
loop back to them. See `puremed-clinical-platform-plan.md` v0.5 Section 3 and 5 for why
the gap existed and `technical-design.md` v0.3 Section 4 for the schema additions this
implies.

## v0.4 change note, 16 August 2026: peer review folded in, deposit decision landed

`peer-review-2026-08-15.md`'s twelve findings had not reached this register. v0.4 folds
them in, alongside the canon fixes in `crm-and-lifecycle-gap-review-2026-08-16.md` C3.
Stage tagging and the overall posture are unchanged.

| Change | Rows | Source |
|---|---|---|
| Remote prescribing: in-person first assessment is a hard prerequisite, not one option | BOOK-001 | Finding 1 |
| Deposit policy resolved to universal; graduated model retired | BOOK-005, BOOK-006 | Nafisa, 15 Aug |
| "Scope of practice" renamed; no GDC carve-out exists for this activity | DIARY-001 | Finding 4 |
| Three rows annotated as high-confidence future-Regulatory under Amber-tier licensing | DIARY-001, PLAN-001, PLAN-002 | Finding 5 |
| Per-treatment competency granularity, not one expiry per practitioner | DIARY-006 | Finding 10 |
| Field-level RBAC backed below the application layer | REC-001 | Finding 6 |
| CQC dividing line stated as a test; record-ownership question opened | REC-004 | Findings 2, 3 |
| New: individualised risk-discussion record | PLAN-005 | Finding 7 |
| New: guest-checkout email verification | ACCT-004 | Finding 9 |
| New: fresh WhatsApp marketing opt-in | MIG-009 | Finding 8 |
| Offline-capable in-room capture | NOTE-005, PHOTO-005 | CRM review B6 |
| Match and survivorship rules for the 588-vs-475 merge | MIG-005, MIG-007 | CRM review B4 |
| Faces extraction: deadline, legal lever, priced fallback | MIG-002 | CRM review B5 |
| Consent re-basing confirmed correct rather than over-conservative | MIG-001 | Finding 11 |

**Added in v0.5:** the S15 Patient Relationship and Retention component, see the change
note above and the S15 table at the end of this document.

This is a representative first pass, not the full register. It covers the rows with the
highest traceability value (a real regulatory or accreditation source behind them) across
every component, so the mechanism is provable end to end. See
`puremed-clinical-platform-plan.md` Section 4 and 7 (Phase 8) for how to build this out to
full coverage.

Requirement type key: **Reg** = Regulatory (mandatory), **BP** = Best-practice /
accreditation standard, **Pol** = Policy (PureMed's choice), **UX** = discretionary
experience.

## v0.3 change note, 15 August 2026: Phase G/Phase R retired, replaced by Stage 1-4

`puremed-clinical-platform-plan.md` Section 9 was rewritten 15 August 2026: full
replacement of Faces Consent is now brought forward into this build, not held back as a
later, trigger-based Phase R that might never happen. The **Phase G / Phase R** tagging
throughout this register is retired and replaced with the plan's **Stage 1-4** sequence
(plan 9.2), which matches `puremed-systems-proposal.md`'s six client-facing build items:

| Stage | Contains |
|---|---|
| **1** | Booking system + calendar (replaces the Faces booking page); patient record + consent-form migration |
| **2** | Clinical photo pipeline; digital toxin prescribing record |
| **3** | Deposit and cancellation enforcement |
| **4** | Aftercare delivery + generated treatment plans |

Rows previously tagged **Phase R** (deferred, not scheduled, might never happen) that sit
inside record migration, consent-form ownership, or the booking/calendar system itself
are **reclassified into Stage 1**, since that work is no longer deferred. Rows genuinely
still deferred on grounds unrelated to the Faces-replacement question (the waitlist,
BOOK-009, deferred because Nafisa said she isn't busy enough to need one yet, not because
of build sequencing) keep a **Backlog** tag instead, to distinguish "not now, by client
choice" from the old "maybe never, trigger-based" meaning Phase R carried.

## v0.2 change note, 10 August 2026 (superseded by v0.3 above, kept for the row-level
## rationale it recorded)

v0.1 was derived entirely from the written requirements brief. v0.2 added rows sourced
from the **Nafisa discovery call of 10 August 2026**, captured in
`../discovery/2026-08-10-as-is-operating-model.md`. Those rows are marked with a
**"Call, 10 Aug"** source and cite the as-is section they come from.

Two things to hold when reading those rows, still true under v0.3:

1. **They describe observed operational failure, not hypothetical risk.** Where a row
   says "must", there is a corresponding thing that is currently not happening: paper
   prescribing records off-file, clinical photographs on a personal phone, deposits taken
   on one booking channel and not the other.
2. **Priority now follows the staged posture** set in `puremed-clinical-platform-plan.md`
   Section 9, Stage 1 through 4 as of v0.3, not the retired Phase G/Phase R split.

## S1: Patient Identity & Account

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| ACCT-001 | Guest checkout allowed; account signup offered post-booking, not required to book | Pol | PureMed direction, 8 Aug 2026, reversing the original brief | **Stage 1.** Login credential is optional; the underlying S7 clinical record and CONS-001 lawful-basis tracking are not, see plan 3.1 |
| ACCT-002 | Two-factor authentication available on patient accounts | BP | Good practice for accounts holding special-category health data (ICO security guidance) | **Stage 1.** |
| ACCT-003 | Age (DOB) captured and validated against treatment-type minimum age at booking, hard stop, no override | **Reg** | Botulinum Toxin and Cosmetic Fillers (Children) Act 2021 | **Stage 1.** Gap identified in Section 5.1; not explicit in brief, treat as must-have |
| ACCT-004 | A guest booking requires email verification (confirm-link click) before any clinical document is dispatched to that address, and before the booking is treated as confirmed where the document is time-critical | **Reg** | UK GDPR Art 32 security principle; peer review Finding 9, 15 Aug 2026 | **Stage 1, new in v0.4.** ACCT-001 made the login credential optional and plan 3.1 defends that correctly on record-keeping grounds. The weak point is elsewhere: "verified email/secure link" was asserted, never designed. An account login is by construction reachable only by the account holder; a link sent to an address typed in at booking time is not. Special-category documents (consent PDFs, aftercare carrying treatment detail) going to an unverified address is the one live exposure specific to the guest path. Cheap to close |

## S2: Booking & Scheduling

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| BOOK-001 | **An in-person first assessment by the prescriber is a hard prerequisite for a first toxin prescription.** Online steps establish eligibility and book that in-person slot; they never substitute for it | **Reg** | Human Medicines Regulations 2012 "adequate assessment"; NMC position in force 1 June 2025 and the July 2026 prescribe-and-supply tightening; peer review Finding 1 | **Stage 1. Rewritten in v0.4, and the rewrite changes the booking journey's shape.** The v0.1-v0.3 wording ("gated behind an adequate prescribing assessment path, not questionnaire alone") implied a remote screening that clears the way to book, with video as an acceptable substitute. That is no longer the right reading. The online step is a triage and eligibility gate whose output is a booked in-person appointment with the prescriber present. This changes what "screening" is for in `booking-engine-plan.md` §3 steps 3/5/6 for toxin specifically, and it means BOOK-007 and DIARY-005 carry regulatory weight, not scheduling convenience. **PARTIALLY RESOLVED 16 Aug 2026 (Nafisa): the prescribing dentist is Shair Mughal, who prescribes in person and is currently available Wednesdays and Thursdays.** This confirms BOOK-001's Regulatory reading is met in current practice, not just designed for, and converts BOOK-007/DIARY-005 into a hard, currently two-day availability constraint on toxin bookings. **Wed/Thu discrepancy resolved, no conflict:** Nafisa confirmed Shair can also prescribe alongside her on Thursdays, so both the 15 Aug and 16 Aug statements were correct. Plan action item 14 closed. **17 Aug 2026: Shair Mughal has signed off on the pathway directly, closing action item 13.** The specific regulatory detail (which GDC-equivalent standard, the exact allowed journey shape) was not captured as part of that sign-off and is left open by direction, not assumed; treat as signed off in principle, not documented against a cited standard |
| BOOK-002 | Reschedule/cancel permitted up to 48 hours before appointment; inside 48 hours cancellation policy and booking-fee loss apply | Pol | PureMed direction, 8 Aug 2026 | **Stage 1.** Confirmed value; store as configuration, not a constant |
| BOOK-003 | Accessible booking journey (WCAG 2.2 AA) | BP | Equality Act 2010 | **Stage 1.** Gap identified, Section 5.8 |
| BOOK-004 | A staff-executed booking (Nafisa booking on a patient's behalf from a WhatsApp request) runs the identical requirement path as a self-serve booking: age gate, consent issue, deposit, screening. No channel bypasses a requirement | **Reg**/Pol | Call, 10 Aug (as-is 2.1) | **Stage 1** (was Phase G). Today this path takes no deposit at all while the online path does. The regulatory weight is on the age gate and consent, which must not be channel-dependent; the deposit element depends on BOOK-005/006 landing in Stage 3 |
| BOOK-005 | Deposit or booking fee required on every booking, every channel, as the configured default | Pol | Call, 10 Aug (as-is 2.5); **decision confirmed by Nafisa 15 Aug 2026** | **Stage 3. LIVE REQUIREMENT.** The BOOK-005/BOOK-006 conflict is resolved: everyone pays a deposit, no exceptions. Nafisa's reasoning is social rather than financial, and it holds: uniformity removes the awkwardness of asking selectively, and it is what lets her say "I can't change it" to a long-standing patient. Stage 3 is no longer gated on this decision |
| BOOK-006 | ~~Late-cancellation and no-show enforcement is graduated: discretionary on a first occurrence, prepayment enforced on rebooking after a configured threshold~~ | Pol | Call, 10 Aug (as-is 2.5, 2.7) | **RETIRED as policy, 15 Aug 2026**, superseded by BOOK-005's universal deposit. Kept in place, not deleted, per the dated-confirmed-direction convention. **Two things survive it.** (1) **Keep counting.** Cancellation and no-show occurrences stay in the event log even though no policy consumes them: "repeat offenders" is a named live problem (as-is 2.7), a universal policy can be revisited, and the history cannot be reconstructed retrospectively. (2) **The buy-vs-build case is thinner than it was.** BOOK-006's graduated model was one of four decisive build-not-buy reasons in `buy-vs-build-spike-2026-08-15.md`; that spike is corrected, and the conclusion still stands on BOOK-004, BOOK-007, BOOK-008 and the multi-tenant commercial argument |
| BOOK-007 | Toxin services are bookable only on dates the prescriber is available, enforced by the availability engine, not by policy | **Reg** | Human Medicines Regs 2012 (POM prescribing requires individual assessment by the prescriber); Call, 10 Aug (as-is 4.3) | **Stage 1** (was Phase G). The prescriber must see the patient face to face. This is a hard cross-resource scheduling dependency, feeds DIARY-005. **Confirmed 16 Aug 2026: the prescriber is Shair Mughal, in-person prescribing only, currently available Wednesdays and Thursdays.** The constraint is concrete, not placeholder: toxin slots exist only where Wednesday/Thursday capacity exists. Wed/Thu discrepancy against action item 6 resolved, see BOOK-001 |
| BOOK-008 | CQC-regulated treatments (confirmed: hyperhidrosis, and toxin to the jaw for clenching/bruxism) are excluded from the public online booking path and routed to a manual booking carrying the Whitehouse provider/location record | **Reg** | CQC registration scope; Call, 10 Aug (as-is 4.4) | **Stage 1** (was Phase G). Codifies what Nafisa already does by hand. Depends on REC-004 and on the outstanding Whitehouse registration-scope verification |
| BOOK-009 | Waitlist supporting same-day cancellation backfill and partial-slot matching (freed 12:00 slot offered against a wanted 12:30) | UX/Pol | Call, 10 Aug (as-is 2.8) | **Backlog** (was Phase R). No current process, so nothing to migrate. Deferred by Nafisa's own choice, not by build sequencing: confirmed as wanted once volume justifies it, explicitly not now |

## S3: Payments & Billing

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| PAY-001 | Card payment handling via PCI DSS-compliant tokenising provider, no raw card data stored | **Reg** | PCI DSS | **Stage 1.** Foundational: the booking system cannot take the £25 new-patient fee or any payment without this |
| PAY-002 | Patient accepts booking/cancellation/refund terms before paying | **Reg**/Pol | Consumer Contracts (Information, Cancellation and Additional Charges) Regs 2013; Consumer Rights Act 2015 | **Stage 1.** The disclosure obligation is Reg; the 48-hour window content (BOOK-002) is Pol, confirmed |
| PAY-003 | Non-refundable booking fees, cancellation/no-show charges clearly disclosed pre-payment | **Reg** | Consumer Rights Act 2015 (unfair terms) | **Stage 1.** |
| PAY-004 | Non-refundable new-patient booking fee (currently £25) disclosed with its terms before payment is taken, on whatever surface collects it | **Reg**/Pol | Consumer Rights Act 2015; Call, 10 Aug (as-is 2.6) | **Stage 3** (was Phase G). Today the terms are typed into a WhatsApp message alongside a SumUp link. The disclosure obligation is Reg, the £25 value is Pol |
| PAY-005 | Payments taken outside the platform (SumUp link, Dojo terminal, bank transfer, GoCardless, Klarna) are recordable against the booking so its payment state is complete | Pol | Call, 10 Aug (as-is 3.1) | **Stage 3** (was Phase G). Six live payment channels, no single view of what a booking has actually been paid. Recording, not processing: the platform does not take over these rails |
| PAY-006 | Apple Pay and Google Pay supported at checkout | UX | Call, 10 Aug (as-is 3.1), explicit client want | **Stage 3** (was Phase G). Falls out of a tokenising provider (PAY-001) at near-zero marginal cost |
| PAY-007 | Refunds recorded with actor, reason, timestamp and the original channel reversed against | BP | Professional record-keeping; audit standard; Call, 10 Aug (as-is 3.2) | **Stage 3** (was Phase G). Currently reversed on the source platform with no record anywhere. Rare, but unlogged |
| PAY-008 | The published "no refunds" term reviewed against CRA 2015 unfair-terms provisions before it is carried into any new system | **Reg** | Consumer Rights Act 2015 Part 2 (unfair terms); CMA guidance | **Verification item, not a build item.** A blanket no-refund term on a consumer service is a known unfair-terms risk. It is currently repeated across the consent forms, the website and the T&Cs, so a single legal review fixes all three. **Needs a solicitor, not an engineer** |
| PAY-009 | Membership and loyalty-point mechanics are out of scope until the dermis.ai app architecture is known | Pol | Call, 10 Aug (as-is 3.3, 3.4, 11.3) | **Blocked, unscoped.** Memberships, points and Klarna checkout all live inside the dermis.ai app. Nobody on the MSS side has seen it. Do not design against assumptions here |

## S4: Consent & Medical Questionnaire

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| CONS-001 | Explicit Article 9(2) condition and lawful basis recorded for all health data capture | **Reg** | UK GDPR Art 9, DPA 2018 | **Stage 1.** Requires the DPIA gap (Section 5.2) resolved first |
| CONS-002 | Consent is treatment-specific, not blanket; reconfirmed before every treatment | **Reg** | Human Medicines Regs (informed consent for POM administration); GDC standards | **Stage 1.** JCCP/Save Face are not currently held (confirmed 8 Aug 2026), but this specific item is independently Regulatory via GDC/prescribing law, not solely JCCP-sourced |
| CONS-003 | Locked, version-controlled record of exactly what wording the patient accepted | **Reg** | UK GDPR accountability principle; GDC record-keeping standards | **Stage 1.** |
| CONS-004 | Separate consent for clinical photography and marketing use of images | **Reg** | UK GDPR (purpose limitation); CAP Code (2.6) | **Stage 1.** The consent flag lands in Stage 1 with the rest of the consent engine; the photo capture surface it gates arrives in Stage 2 |
| CONS-005 | Chaperone/third-person-present record for intimate-area treatment or video assessment | BP | Accreditation-body and indemnity-insurer standard | **Stage 1.** Gap identified, Section 5.5; not currently mandatory (no JCCP/Save Face accreditation held), build where practical since JCCP registration is being considered |
| CONS-006 | Complete audit trail of completion, amendment, and signature | **Reg** | UK GDPR accountability; professional record-keeping standards | **Stage 1.** |
| CONS-007 | A reissued form arrives prefilled from the data already held; the patient confirms or amends it and signs to attest it is true and accurate, every time | **Reg**/Pol | GDC record-keeping (accuracy of medical history at the point of treatment); Call, 10 Aug (as-is 2.4) | **Stage 1** (was Phase G, and consistent now: the 10 Aug plan had called this Phase R since it needs the form engine, this register had already tagged it Phase G; owning the form engine is Stage 1 work, which resolves the inconsistency). Nafisa's own framing: "I want them to sign it to say that it's true and accurate." The attestation is the requirement; the prefill is what makes it survivable. Implements plan principle 8.1 |
| CONS-008 | No question is asked twice across the medical form and the treatment consent form for the same appointment | UX/Pol | Call, 10 Aug (as-is 2.3) | **Stage 1** (was Phase G, same reconciliation as CONS-007 above). Faces sends a toxin consent form carrying medical questions plus a separate generic medical form, and Nafisa cannot change it. Named client friction, not an inferred nicety |
| CONS-009 | Where a treatment requires the patient to be contacted before the appointment (confirmed for toxin), that contact is a tracked step with a completion state, not a line of text on a form | **Reg** | Prescribing assessment requirements (Human Medicines Regs 2012); Call, 10 Aug (as-is 2.3) | **Stage 2** (was Phase G), grouped with the digital prescribing record. Nafisa cannot add this to the Faces form at all, so it is currently held in her head. A pre-treatment prescribing contact that is not recorded cannot be evidenced |

## S5: Automated Communications

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| COMM-001 | Marketing messages require opt-in consent distinct from transactional/clinical messages | **Reg** | PECR 2003 | **Stage 1.** Two independent flags, not one toggle (Section 2.1); the flags belong in the consent engine even though marketing sends themselves are Stage 4 |
| COMM-002 | Delivery/open/failure status visible per message | Pol/UX | Brief | **Stage 1.** Operational, not externally mandated; needed as soon as any automated message exists (booking confirmations) |
| COMM-003 | POM (toxin) never named/advertised to the public in automated marketing content | **Reg** | Human Medicines Regs Art 5 advertising restriction; CAP/BCAP Code | **Stage 1.** Applies to marketing sends specifically, not clinical/transactional |
| COMM-004 | WhatsApp is a first-class delivery channel for aftercare, treatment plans, booking confirmations and payment links, not a fallback | Pol/UX | Call, 10 Aug (as-is 7.4, 7.5) | **Stage 4, and load-bearing** (was Phase G). WhatsApp is the dominant channel and the only one aftercare reliably lands on. PECR still applies: marketing over WhatsApp needs the COMM-001 opt-in, transactional does not |
| COMM-005 | Marketing audience is synced from the patient record, not rebuilt by manual CSV export, with unsubscribe state single-sourced | **Reg** | PECR 2003; UK GDPR accuracy principle; Call, 10 Aug (as-is 7.2) | **Stage 4** (was Phase G). Today every MailChimp send starts with a fresh export from Faces. Unsubscribes only hold inside MailChimp, so the source list is permanently stale and a suppressed contact can be re-added by the next export |
| COMM-006 | Aftercare delivery is tracked to a confirmed-received state, with an automatic second channel where the first is unread | Pol | Call, 10 Aug (as-is 7.5) | **Stage 4** (was Phase G). Aftercare fails roughly nine times in ten today and is re-sent by hand over WhatsApp. Depends on COMM-002 and COMM-004 |

## S6: Practitioner Diary

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| DIARY-001 | Practitioner cannot be booked for a treatment their current **declared competence and training basis**, qualification and indemnity record doesn't authorise | BP/Pol, **high-confidence future-Reg** | Indemnity insurer terms; GDC general conduct standards; Health and Care Act 2022 licensing scheme consultation response, 7 Aug 2025 | **Stage 1, blocked** on decision-gate item 4 (plan 9.5). Gap identified, Section 5.6. **Two v0.4 changes.** (1) *Renamed*, peer review Finding 4: the attribute is a "declared competence and training basis", not a "scope of practice", because GDC removed non-surgical cosmetic injectables from its Scope of Practice Guidance in Nov 2025 as not being the practice of dentistry. There is no GDC-defined boundary to point at. The open question is therefore what non-GDC standard PureMed adopts, which is a harder ask than the one previously logged (plan action item 2). (2) *Reclassified in priority*, peer review Finding 5: the confirmed Amber-tier licensing shape requires oversight by a named, appropriately qualified regulated healthcare professional, which is close in shape to this row. Treat as **Best-practice today, high-confidence future-Regulatory**, and build it at that priority rather than as a discretionary nicety, or it gets rebuilt in 2026-27 |
| DIARY-002 | External calendar sync shows minimal, non-identifying detail | **Reg** | UK GDPR data minimisation; confidentiality obligation to patients | **Stage 1.** |
| DIARY-003 | Double-booking prevention | Pol | Brief | **Stage 1.** |
| DIARY-004 | Exactly one authoritative writer to the practitioner's external calendar; competing automations are retired at cutover, not left running alongside | Pol | Call, 10 Aug (as-is 8) | **Stage 1, and do this early** (was Phase G). Three things currently write to that Google Calendar: an LLM automation Nafisa wired to her inbox, the dermis.ai app, and (prospectively) this system. The calendar governs whether she turns up. Test with a test email first, per action A8 |
| DIARY-005 | Prescriber availability is modelled as a bookable resource constraint on toxin services, distinct from the treating practitioner's availability | **Reg**/Pol | Human Medicines Regs 2012; Call, 10 Aug (as-is 4.3, 6.4) | **Stage 1** (was Phase G). Two people's diaries must intersect before a toxin slot can be offered. Implements BOOK-007. **16 Aug: prescriber identified as Shair Mughal, in-person prescribing, Wednesdays and Thursdays currently.** Populates the real-world constraint behind the `practitioner_competencies` join table (`technical-design.md` §4) once DIARY-006's qualification/indemnity data is captured |
| DIARY-006 | Competency, insurance and indemnity are tracked **per practitioner per treatment type**, each with its own expiry, and are the gate behind DIARY-001 | BP/Pol | Indemnity insurer terms; GDC standards; Call, 10 Aug (as-is 6.5); peer review Finding 10 | **Stage 1, blocked.** Asked on the call, answer not captured. Cannot be configured until PureMed states what is tracked today and where. **v0.4, Finding 10: granularity corrected.** A flat `qualification_expiry`/`indemnity_expiry` pair on `practitioners` implies one expiry per person. A practitioner trained and insured for toxin but not for a newer filler technique needs the gate to work at treatment-type granularity. Model as a `practitioner_competencies` join table (practitioner × treatment type × basis × expiry), which also matches the Amber-tier scheme's per-procedure named-oversight shape. **15 Aug, two data points from Nafisa:** records currently exist only on her laptop (that is the initial migration source), and indemnity auto-renews annually with an insurer email a few weeks ahead of renewal, which is the real-world signal expiry tracking should key off rather than a fixed annual date |

## S7: Patient Clinical Record

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| REC-001 | Role-based, field-level access; reception sees medical alerts without full clinical detail | **Reg**/BP | UK GDPR data minimisation; professional confidentiality duty | **Stage 1.** Field-level, not just page-level permissions. **v0.4, peer review Finding 6: enforce below the application layer where practical.** This is a Regulatory row in the same weight class as the append-only requirement (NOTE-003, CONS-006), which `technical-design.md` §4 deliberately pushes to the database role level so it is structurally impossible to violate by a future code change. Field-level RBAC was given a weaker guarantee (service-layer checks only), which means any new report, export or debug endpoint can leak clinical fields to a reception token unless every new code path re-applies the filter by hand. Back it with column-level policies or role-scoped views; at minimum, a CI test asserting no reception-scoped query returns restricted fields, so a regression fails the build |
| REC-002 | Retention period held as configuration, set to 11 years, not hardcoded | **Reg**/Pol | ICO retention guidance, no single statutory figure; PureMed confirmed 11 years, 8 Aug 2026 | **Stage 1.** The obligation to have a defined, defensible period is Reg; the specific 11-year value is Pol |
| REC-003 | Closing a patient account does not delete records where retention obligation still applies | **Reg** | UK GDPR Art 17(3) (exemption where processing necessary for legal claims/obligations) | **Stage 1.** Brief already states this correctly |
| REC-004 | Regulated-activity treatments record which legal provider and CQC-registered location delivered them (Whitehouse Dental Studio, where applicable), distinct from the treating practitioner | **Reg** | CQC registration attaches to provider/location/activity, not practitioner | **Stage 1.** New row, added following PureMed's 8 Aug 2026 confirmation; see plan Section 2.4 action item to verify Whitehouse's registration scope. **Two v0.4 additions.** (1) *The test, not the list* (Finding 3): a treatment is a regulated activity where it addresses a **diagnosed disease, disorder or injury**, as against a purely cosmetic purpose. That is why hyperhidrosis and bruxism jaw toxin route to Whitehouse and cosmetic toxin/filler does not. Implement as a test applied to every new catalogue item, not as an enumeration, or a future addition (toxin for chronic migraine, say) silently misses BOOK-008's gate. (2) *Record ownership is unresolved and this row is not settled without it* (Finding 2): CQC expects records of a regulated activity to be held by the registered provider delivering it. Whether PureMed's S7 is the system of record for a Whitehouse-delivered treatment, or Whitehouse's own system is authoritative, decides **who is the Article 9 controller** for that record, not just where a foreign key points. Two treatments already run this way, so it is live volume from day one. Getting this wrong is a rebuild of the S7/S9 access model, not a config change. Plan action item 11. **RESOLVED 16 Aug 2026 (Nafisa), phased.** Today, everything, including notes, for a Whitehouse-delivered treatment is held entirely at Whitehouse; PureMed's systems hold none of it. That confirms **Stage 1 builds a stub**: `provider_location_id` and the fact of the referral, no clinical content, matching current reality rather than an assumption. But this is not a permanent boundary: **Nafisa confirmed PureMed's S7 is intended to become the full record for Whitehouse-delivered treatments eventually.** Full consolidation is a later, not-yet-scheduled stage, and when it happens the controllership answer changes with it (S7 becomes the system of record, so PureMed becomes controller for that data, which needs revisiting at that point, not now). **Also resolved: the CQC registration is held by the company** (Nafisa is a director of Whitehouse Dental Studio), not a named individual, which reframes action item 1 to a company-level scope check rather than an individual-coverage one, still open |

## S8: Consultation & Treatment Planning

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| PLAN-001 | Cooling-off period schedulable where required | BP/Pol, **likely future-Reg** | JCCP/Save Face guidance on high-risk or larger treatment plans; Amber-tier licensing standards consultation expected 2026 | **Stage 1**, part of the core consultation record. Trigger conditions are a Policy decision; JCCP not currently held, build where practical. **v0.4, Finding 5:** likely to be formalised by the Amber-tier licensing standards, so treat as more than discretionary |
| PLAN-002 | Explicit vulnerable-patient/body dysmorphia screening question with a "not currently appropriate" outcome path | BP, **likely future-Reg** | Keogh Review recommendations; JCCP standards; Amber-tier licensing standards consultation expected 2026 | **Stage 1.** Gap identified, Section 5.10; JCCP not currently held, build where practical. **v0.4, Finding 5:** same reclassification as PLAN-001 |
| PLAN-003 | Record of declined/unsuitable treatment recommendations | **Reg**/BP | Informed consent documentation standard | **Stage 1.** |
| PLAN-004 | A personalised treatment plan is generated from the consultation record, carrying the patient's own photograph, the findings discussed, the recommended treatment sequence and the prices, and is deliverable to the patient | UX/Pol | Call, 10 Aug (as-is 7.6) | **Stage 4** (was Phase G). Nafisa already does this by hand and raised it unprompted as the one thing she has personalised. It is the highest-value manual artefact in the business and has no system behind it. Depends on PHOTO-005 for the image and on the S3 price catalogue for the figures. **Note, 16 Aug:** as specified this automates the *assembly* and stops there. Nothing records acceptance, converts the recommended sequence into offered bookings, or follows up. See `crm-and-lifecycle-gap-review-2026-08-16.md` A4 and proposed row CRM-006 |
| PLAN-005 | A structured record of the specific risks and alternatives discussed with **this** patient, beyond the standard consent-form content, signed and timestamped alongside the rest of the consultation note | BP | Indemnity/insurer defensibility standard; professional record-keeping; peer review Finding 7, 15 Aug 2026 | **Stage 1, new in v0.4.** CONS-002/003/006 evidence the *form*: what was signed, which version, audited. That proves the patient was given standard information. It does not prove what was said in the room if a patient later claims nobody warned them about one specific thing in their case, which is what an indemnity defence usually turns on. Since defensibility is the stated purpose of several rows here, this gap is directly on-point. Short free-text or checklist, low build cost |

## S9: Clinical Treatment Notes

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| NOTE-001 | Product, manufacturer, batch/lot, expiry, quantity recorded per treatment | **Reg** | Human Medicines Regs traceability requirement for POMs; MHRA device traceability | **Stage 2**, alongside the prescribing record it shares a data model with |
| NOTE-002 | Batch/lot lookup returns all affected patients (recall support) | BP | Manufacturer recall / MHRA field safety notice response capability | **Stage 2.** Gap identified, Section 5.3 |
| NOTE-003 | Completed notes locked; corrections are dated amendments, original never silently changed | **Reg** | Professional record-keeping standards (GMC/NMC/GPhC); UK GDPR accuracy + accountability | **Stage 2.** |
| NOTE-004 | Prescriber-of-record distinct from treating practitioner where they differ | **Reg** | Human Medicines Regs (POM supply chain accountability) | **Stage 2.** Gap identified, Section 5.4; both roles confirmed GDC-registered at PureMed, field still required since the two roles can differ per treatment. **Confirmed live on the call: the two roles do differ on every toxin treatment** |
| NOTE-005 | Digital toxin prescribing record capturing units administered, the site of each administration, batch number, the treating clinician's signature and the prescriber's signature, completed at the point of treatment | **Reg** | Human Medicines Regs 2012 (POM administration record); GDC record-keeping; Call, 10 Aug (as-is 4.2) | **Stage 2. Highest-priority single row in this register** (was Phase G). This is the one document that leaves the system today: paper, hand-completed in the room, countersigned, photographed, and then not uploaded. Build from the real form Nafisa is sending (action A4), never from an invented template. **v0.4: it must complete without connectivity.** Local-first capture, both signatures taken offline, record marked pending-sync and reconciled on reconnection. A prescribing record that cannot be completed because the signal dropped, with the prescriber standing there waiting to sign, sends the workflow straight back to the paper form this row exists to eliminate. Paper never fails; one occurrence re-establishes the habit. Plan 5.15 |
| NOTE-006 | The existing backlog of loose paper prescribing forms is captured against patient files as scanned historical evidence, clearly labelled as pre-migration | **Reg** | GDC record-keeping (contemporaneous records must be retrievable); Call, 10 Aug (as-is 4.2) | **Stage 2, and a one-off remediation, not a feature** (was Phase G). Nafisa's words: "I've got shitloads of paperwork sitting there that I haven't done." Records of POM administration exist on paper and are not on any patient file. Scope the backlog before scoping the fix |
| NOTE-007 | Batch number capture is mandatory, not optional, on any POM administration record | **Reg** | Human Medicines Regs traceability; Call, 10 Aug (as-is 4.2) | **Stage 2** (was Phase G). Batch is already written on the paper form, so the discipline exists. Making it a required field is what turns NOTE-002's recall query from aspiration into something that returns complete results |

## S10: Clinical Photography

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| PHOTO-001 | In-app capture never reaches the device's normal photo library | **Reg** | UK GDPR security principle | **Stage 2** (was Phase G). Platform-level control, not a staff policy; also a JCCP/Save Face expectation but independently Regulatory via UK GDPR regardless of accreditation status |
| PHOTO-002 | Marketing export requires marketing consent present + anonymisation/crop step + export logged | **Reg** | UK GDPR purpose limitation; CAP Code | **Stage 2.** |
| PHOTO-003 | Withdrawing marketing consent removes marketing use without touching clinical original | **Reg** | UK GDPR Art 7(3) right to withdraw consent | **Stage 2.** |
| PHOTO-004 | Access/download/export of any clinical image logged | **Reg** | UK GDPR accountability; audit standard | **Stage 2.** |
| PHOTO-005 | Bulk multi-select capture and single-action upload of a full patient set (7 to 15 images), not one image at a time | Pol/UX | Call, 10 Aug (as-is 5.3, 5.4) | **Stage 2, and the make-or-break row** (was Phase G). Nafisa's words: "I need to be able to select all and then just upload it straight away." Faces supports upload but one photo at a time, which is why she stopped using it. A correct feature that is slower than the shortcut gets abandoned; the as-is record has two separate precedents for exactly that. **v0.4: capture must work offline**, queueing locally and syncing on reconnection, for the same reason as NOTE-005. PHOTO-007's confirmed-upload-before-deletion sequencing is unaffected and already correct. Plan 5.15 |
| PHOTO-006 | Capture records the time and location metadata Nafisa currently relies on the TimeMark app for | BP | Clinical photography evidential standards; Call, 10 Aug (as-is 5.1) | **Stage 2** (was Phase G). She chose TimeMark specifically for the timestamp and location stamp. Anything replacing it that loses that metadata is a downgrade she will route around |
| PHOTO-007 | Images are removed from the capture device once upload is confirmed, and confirmation is explicit | **Reg** | UK GDPR Art 32 security principle; Call, 10 Aug (as-is 5.1, 5.4) | **Stage 2** (was Phase G). Special-category images of every patient currently sit indefinitely on a personal phone. Nafisa flagged this herself: "which it shouldn't." Deletion must follow a confirmed successful upload, never precede it |
| PHOTO-008 | Identity concealment (crop or anonymisation) is a mandatory, non-skippable step on the marketing export path, matching the promise made to patients in the consent wording | **Reg** | UK GDPR purpose limitation; CAP Code; Call, 10 Aug (as-is 5.5) | **Stage 2** (was Phase R, reclassified: the old Phase R meaning, "deferred, may never happen," no longer applies once the photo pipeline itself is Stage 2. Build immediately after PHOTO-002's core export path, not deferred). Tightens PHOTO-002 from "an anonymisation step exists" to "it cannot be bypassed." PureMed tells patients "we'll do our best to conceal your identity," which is a commitment the platform should enforce rather than leave to intent |

## S11: Aftercare, Follow-up & Complications

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| CARE-001 | Adverse event/complication reportable to MHRA Yellow Card scheme from within the workflow | **Reg** | MHRA Yellow Card scheme | **Stage 4**, alongside aftercare and follow-up; greenfield, no current process to migrate (as-is 4.5) |
| CARE-002 | Urgent complication alert reaches the practitioner with escalation/emergency-contact instructions | BP | Indemnity insurer and accreditation-body expectation | **Stage 4.** |
| CARE-003 | Manufacturer adverse-event reporting record kept, separate from MHRA report | **Reg**/BP | Product liability / manufacturer post-market surveillance obligations | **Stage 4.** |

## S12: Security, Identity & Compliance

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| SEC-001 | DPIA completed before processing special-category data at scale | **Reg** | UK GDPR Art 35 | **Stage 1 blocker** (was "before S7-S10 go-live," now a Stage 1 gate since record migration and consent are Stage 1). Gap identified, Section 5.2 |
| SEC-002 | Encryption in transit and at rest | **Reg** | UK GDPR Art 32 security principle | **Stage 1.** |
| SEC-003 | Two-factor authentication for staff accounts | **Reg**/BP | UK GDPR Art 32; accreditation-body expectation | **Stage 1.** |
| SEC-004 | UK/adequate-jurisdiction data hosting | **Reg** | UK GDPR international transfer rules | **Stage 1.** |
| SEC-005 | Data Processing Agreement register, maintained with renewal dates, for every processor | **Reg** | UK GDPR Art 28 | **Stage 1.** Gap identified, Section 5.9: must be a living register, not a one-off exercise |
| SEC-006 | Subject Access Request workflow with defined turnaround | **Reg** | UK GDPR Art 15 | **Stage 1.** |
| SEC-007 | Data breach detection and the 72-hour ICO notification obligation supportable from audit logs | **Reg** | UK GDPR Art 33 | **Stage 1.** |
| SEC-008 | Every third party processing patient or lead data on PureMed's behalf appears in the DPA register, including dermis.ai (website, app, skin scanner, AI voice agent, Meta ads audience) and MailChimp | **Reg** | UK GDPR Art 28; Call, 10 Aug (as-is 7.2, 9) | **Do this now, independent of any build stage.** PureMed is the controller for skin-scanner lead data and for the marketing list. dermis.ai is running at least five distinct processing activities and MailChimp a sixth. Extends SEC-005 from a principle to a named list |
| SEC-009 | Automated voice or chat contact with patients and leads discloses that it is not a human, at the start of the interaction | **Reg** | Consumer Protection from Unfair Trading Regulations 2008 (misleading actions); UK GDPR Art 5(1)(a) transparency; GDC honesty and integrity standards | **Decision item, needs legal review, not engineering, and not staged.** The dermis.ai voice agent presents as "Aria from PureMed Aesthetics" with simulated call-centre ambience. Nafisa's own read: "I don't think they'd realise that it's AI." The exposure attaches to PureMed's brand and to Nafisa's GDC registration, not to dermis.ai. See as-is 9.2 and 12.3 |
| SEC-010 | Clinical images are not held on personal, unmanaged devices | **Reg** | UK GDPR Art 32; Call, 10 Aug (as-is 5.1) | **Stage 2, and a live exposure today, not a future requirement.** Special-category images of every patient sit indefinitely on a personal phone. PHOTO-007 is the mechanism; this row is the obligation it discharges. Worth an interim manual remediation before the build lands |
| SEC-011 | Patient data is not exposed to a general-purpose LLM assistant without a processing basis and a DPA | **Reg** | UK GDPR Art 28, Art 32; Call, 10 Aug (as-is 8) | **Stage 1.** Nafisa has ChatGPT connected to her inbox, reading booking confirmations to write calendar events. That inbox also carries patient correspondence. Retiring it is already required by DIARY-004; this row records why it is not merely a tidiness issue |

## S13: Migration & Integration

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
**All rows in this component moved from "Phase R, not scheduled" to Stage 1** on 15
August 2026, since the replacement system needs the migrated record and consent data
from day one rather than months into a gap layer proving itself. See plan Section 6.

| MIG-001 | Legacy consent records imported as historical evidence only, never as live satisfied consent | **Reg** | Follows directly from CONS-002; UK GDPR consent must be specific and current | **Stage 1.** See plan Section 6.4. **v0.4, peer review Finding 11: independently reviewed and confirmed correct, not over-conservative.** Consent must be current to the treatment being given now; some Acuity records are 3.7 years stale; GDC and indemnity guidance already require reconfirmation before every treatment regardless of migration. And there is no experience cost, because CONS-007's prefill turns re-consent into a review-and-attest step rather than a blank-form redo. Do not revisit this as a friction concern |
| MIG-002 | Written data export/deletion undertaking obtained from Faces Consent (and Acuity, only if any historical data is imported) before extraction | **Reg** | UK GDPR Art 28 processor obligations | **Stage 1.** Acuity confirmed dormant, 8 Aug 2026; only a historical-record check needed, not a live-system undertaking unless data is actually imported. **15 Aug: admin-UI check confirmed Faces has no self-serve bulk export, so this request is now the only extraction path, not a compliance formality on top of a CSV pull. Nafisa has already submitted the data request to Faces; awaiting their response.** **16 Aug: escalated from a status to a managed risk.** Stage 1 now depends entirely on the goodwill of the vendor being replaced. Three additions. *The legal lever, stated so it can be used:* Art 28(3)(g) requires a processor to return or delete personal data at the controller's choice at end of service, and 28(3)(h) obliges assistance; PureMed is the controller and can require this, it is not a favour. *A deadline:* a date at which no useful response becomes a formal written Art 28 request rather than a support ticket. *A priced fallback:* cost assisted or manual extraction at 475 records before that date, so the call is made against a number. Standing constraint: do not re-run the export check or build a scripted UI extraction until Faces' response is known inadequate |
| MIG-003 | Migrated patients are offered account claim/creation, not auto-granted login access to their legacy record | Pol | Follows from ACCT-001 (guest checkout, confirmed 8 Aug 2026) | **Stage 1.** Revised: no longer "must create an account," since booking itself no longer requires one; this row is now specifically about not silently granting login access to a pre-existing record |
| MIG-004 | All live Acuity Scheduling links removed at changeover | Pol | PureMed direction, 8 Aug 2026 | **Stage 1.** Includes the `puremed.uk` footer link tracked in `booking-engine-plan.md` |
| MIG-005 | Acuity's historical patient notes are migrated as read-only historical record, separately from its contact list | Pol | Call, 10 Aug (as-is 8) | **Stage 1. Revises the 8 Aug assumption.** Acuity was treated as "dormant, check for historical data". The call establishes the notes on long-standing patients are the unique asset ("long-standing patients, yeah, loads"), while the contact list is expected to substantially duplicate Faces. Migrate the notes, deduplicate the contacts. **15 Aug: unlike Faces, Acuity has a real working bulk CSV export (Settings → Clients → Import/Export). Exported: 588 records (vs Faces' ~475), 54 with a non-empty free-text Notes field, median 1,365 days (~3.7 yr) since last appointment, only 89 with an appointment inside the last year. Dedup against the Faces migration is now a real reconciliation task, not a formality: 588 vs 475 is a materially different scope than assumed 10 Aug.** **16 Aug: the merge needs explicit rules, which do not exist yet.** Two unanswered questions: what key matches an Acuity record to a Faces one (email, phone, name plus DOB) and what happens when they disagree; and which value wins when both hold different contact details, given Acuity's records are a median 3.7 years stale so conflicts will be routine rather than exceptional. Both error modes are serious in a clinical record: merging two people produces a record carrying someone else's medical history, splitting one person produces two half-histories one of which is missing an allergy. A count reconciliation catches neither. Requires stated match and survivorship rules plus a human-review queue for every non-exact match, which at a few hundred candidates is entirely tractable. `technical-design.md` §5.2 |
| MIG-006 | Marketing consent and unsubscribe state is reconciled across Faces and MailChimp at migration, with suppression taking precedence in any conflict | **Reg** | PECR 2003; UK GDPR Art 7(3); Call, 10 Aug (as-is 7.2) | **Stage 1.** Unsubscribes currently live only in MailChimp while the source list is re-exported from Faces each send. A naive migration from Faces alone would silently resurrect every suppressed contact. Depends on COMM-005 |
| MIG-007 | Record count and scope are confirmed before migration design: approximately 475 patient records in Faces | Pol | Call, 10 Aug (as-is 8) | **Stage 1.** Confirms the low-volume assumption in plan 6.5, which is what justifies a file-export ingestion rather than a live dual-write layer. Two orders of magnitude below the threshold where that choice would need revisiting |
| MIG-008 | Nothing is migrated out of the dermis.ai app until its data model is known | Pol | Call, 10 Aug (as-is 11.3) | **Blocked on actions A5 and A6, not staged.** Memberships, loyalty-point balances and Klarna payment history are patient-facing financial state held in a system nobody on the MSS side has seen. Pairs with PAY-009. **Note, 16 Aug:** the *architectural* consequence of leaving this out of scope is not the same as the scoping decision, and is unaddressed. After Stage 1, PureMed has a clinical/booking master here and a commercial master (tier, points, Klarna liability) in dermis.ai, permanently and with no join key. That is the same parallel-store failure plan §9.1 rejects for the clinical layer. Minimum action costing nothing: reserve `patients.dermis_user_ref`, and put "which system is the customer master, and what is the join key" explicitly on the A6 agenda. See CRM review A5 and proposed row CRM-009 |
| MIG-009 | A fresh, distinct opt-in is captured for **WhatsApp marketing** specifically, never inferred from transactional WhatsApp use or from migrated contact data | **Reg** | PECR 2003; ICO guidance that a number collected for a booking is not consent to market to it; peer review Finding 8, 15 Aug 2026 | **Before any Stage 4 marketing send, new in v0.4.** COMM-004 makes WhatsApp a first-class channel and correctly notes PECR applies to marketing but not transactional sends. The gap is at migration: MIG-006 reconciles Faces/MailChimp *email* opt-outs and has no WhatsApp equivalent, so the migrated contacts' numbers, gathered for booking purposes, carry no marketing basis. The practical risk is a future send built on "we already WhatsApp these people for bookings, so it's fine", which is exactly the trap, on exactly the channel PureMed relies on most, at the same maximum fine tier as email. Gates COMM-005 and COMM-006, and gates the recall engine proposed as CRM-004/005 |

## S15: Patient Relationship and Retention

*New component, v0.5, 16 August 2026.* `booking-engine-plan.md` §14 scoped a clinic CRM
out ("everything after the appointment is out") and this document only ever picked up
clinical work after an appointment exists. Neither boundary was wrong on its own; together
they left the commercial relationship, before and between bookings, unowned by either
document. See `crm-and-lifecycle-gap-review-2026-08-16.md` Part A and
`puremed-clinical-platform-plan.md` v0.5 Section 5 for the fuller account. Deliberately
narrow: no pipeline, no deal stages, no lead-scoring. The people exist as records, their
origin is recorded, and there is a loop back to them.

| Req ID | Requirement | Type | Source | Notes |
|---|---|---|---|---|
| CRM-001 | A lead/enquiry is a first-class record, distinct from a patient, carrying contact details, source, treatment interest, status and outcome, with a nullable link to the patient record it converts into | **Reg**/Pol | UK GDPR Art 5(1)(c) data minimisation and Art 30 records-of-processing; CRM review A1 | **Stage 1.** SEC-008 already names PureMed as controller for skin-scanner lead data; controller obligations attach to that population from first contact, not from booking. Every top-of-funnel route (scanner, voice agent, Instagram satellites, microsites, direct WhatsApp/email) currently lands outside any system PureMed controls, so the population is neither enumerable nor answerable to a request. Deliberately thin: not a pipeline |
| CRM-002 | SEC-006's SAR workflow, SEC-005's retention policy and the Art 13/14 transparency notices extend to lead data, not only patient data | **Reg** | UK GDPR Art 13, 14, 15, 17 | **Stage 1.** SEC-006 designs the SAR workflow as an admin export keyed on `patient_id` (`technical-design.md` §8). A subject access request from somebody who used the skin scanner, was called by the voice agent, and never booked cannot be answered by that workflow at all today, and Article 13/14/15/17 obligations do not wait for a booking to attach. Same class of finding as SEC-009, arguably more likely to be exercised given scanner volume. Depends on CRM-001 existing as a queryable population |
| CRM-003 | Every booking and every patient carries an acquisition source, with campaign/first-touch where the entry point supplies it | Pol/UX | `puremed-growth-engagement-plan.md` open measurement item; CRM review A2 | **Stage 1.** `bookings` and `patients` carry no source field today. Near-free to add now (two columns and a query-parameter convention on the booking entry points); retroactively impossible once a booking has been taken without it. Seven treatment microsites, roughly ten Instagram accounts, Meta ads to the scanner, the AI voice agent, direct WhatsApp and the MailChimp newsletter all need distinguishing, and this platform is the only place the answer can ever land |
| CRM-004 | Each service carries a clinically-appropriate recall interval; each patient carries a derived next-due date maintained from the treatment record | BP/Pol | Manufacturer/consent-form treatment intervals (migrated dermal filler consent: "periodically, generally within 4-8 months"); CRM review A3 | **Stage 1 (data), Stage 4 (engine).** The *data* has to land at migration, because every migrated record needs a last-treatment baseline set at that point or it can never be reconstructed. The *engine* that acts on it sits in Stage 4 next to the rest of the comms work. Against 588 Acuity records with only 89 seen in the last year, this is plausibly the largest single retention asset in the estate |
| CRM-005 | Recall and reactivation messages are classified transactional or marketing **at the message-template level**, never as a per-send judgement, with marketing gated on the COMM-001 opt-in | **Reg** | PECR 2003 regs 22/23; peer review Finding 8, 15 Aug 2026 | **Stage 4.** A clinical follow-up (checking a result, a review appointment) is plausibly transactional; "your filler is due, book in" is marketing. This is exactly the PECR trap peer review Finding 8 describes for WhatsApp, and a recall engine walks into it by default if the classification is left to whoever sends the message. Fixing it at the template level, not the send, is the only version of this that is auditable. Interacts with MIG-009: a recall over WhatsApp needs the fresh WhatsApp marketing opt-in that row requires, not the transactional-use inference it explicitly forbids |
| CRM-006 | A treatment plan carries an acceptance state, and its recommended sequence is convertible into offered bookings with follow-up on a plan that goes quiet | Pol/UX | CRM review A4; extends PLAN-004 | **Stage 4, extends PLAN-004.** PLAN-004 automates assembly of the plan document, which is the half that costs Nafisa time. Nothing currently records whether it was accepted, turns the recommended sequence into offered or scheduled appointments, or follows up on one that went quiet, so the system that generates the highest-value manual artefact in the business is also the only system that knows it exists and does nothing further with that knowledge |
| CRM-007 | Post-treatment review request is an aftercare trigger, gated on marketing consent, and is suppressed for any treatment carrying a complication or adverse-event flag | Pol/UX + **Reg** edge | UK GDPR Art 9 (special-category linkage to the suppression logic); CRM review A6 | **Stage 4.** The standard aesthetics retention loop, not mentioned in any document reviewed, and the cheapest item in S15 to build: one message on a trigger the Stage 4 aftercare engine already owns. The non-obvious part is the edge case: soliciting a public review from a patient who had a complication is a harm, not just a bad look, so the suppression check against CARE-001/CARE-002 data is not optional |
| CRM-008 | Discount codes and referral credit, named in plan §3's S3 component blurb with no register row behind it until now | Pol | PureMed direction (discount codes); Nafisa, as-is 3.5 (referral pricing, wanted, not built) | **Backlog.** A traceability leak in the mechanism the register's §4 exists to guarantee: a capability named in the component model with nothing behind it. Individually small; not urgent enough to gate Stage 1-4 |
| CRM-009 | A stated position on which system is the customer master for membership, loyalty and commercial state, with a join key back to the patient record | Pol | CRM review A5; pairs with MIG-008 | **Blocked on A5/A6.** Memberships, loyalty points and Klarna checkout live entirely inside dermis.ai, with its own user identity, and MIG-008 correctly refuses to design against a system nobody has seen. But that is a scoping decision, not an architectural position: after Stage 1, PureMed has a clinical/booking master here and a commercial master there, permanently, with no join key, unless this is answered. `patients.dermis_user_ref` is reserved in the schema for exactly this (`technical-design.md` §4) so the position is recoverable once A5/A6 land |
