# PureMed clinical platform: CRM and lifecycle gap review

16 August 2026 | Owner: Osman Akhtar

Scope of this review: read `puremed-clinical-platform-plan.md` v0.3,
`requirements-register.md` v0.3, `technical-design.md` v0.1,
`peer-review-2026-08-15.md`, `buy-vs-build-spike-2026-08-15.md`,
`../discovery/2026-08-10-as-is-operating-model.md`, `../puremed-systems-proposal.md`,
`../puremed-growth-engagement-plan.md` and `booking-engine/booking-engine-plan.md`
(§4, §13, §14). Three questions: where does the plan actually stand, what does it not
cover on the relationship/CRM side, and what else has been missed.

Findings are ordered most load-bearing first, same convention as the 15 August peer
review. Part A is the CRM gap. Part B is everything else. Part C is the concrete
proposed changes.

---

## 0. Where the plan stands

Sound, and further along than the folder makes it look. The regulatory landscape
(§2), the component model (S1-S14), the traceability mechanism and the migration
mechanics are all well-constructed, and the 15 August reconciliation did the hard part:
the Phase G/Phase R split is gone, the register is staged 1-4, and the stage tags match
the client-facing proposal's six build items exactly.

Three things are genuinely settled that were open a week ago: the deposit policy
(everyone pays, no exceptions), the working pattern (Wed 10-3, Fri 1-5, then Thu, then
Mon, as ordered capacity tiers), and Faces' export capability (none, so the DPA data
request is the only path and it is submitted).

What follows is not an argument against the posture. The build-forward decision holds.
These are gaps in coverage, not errors in direction.

---

# Part A: the CRM gap

## A0. The structural cause: CRM falls between two documents, and neither one is wrong

`booking-engine-plan.md` §14 carries an explicit risk row: *"Scope creep into a full
clinic CRM. Records, notes, stock, marketing all sit adjacent and will be asked for.
Scope is booking through to signed record and payment. Everything after the appointment
is out."*

`puremed-clinical-platform-plan.md` §3 defers booking, scheduling and payments to that
document, and picks up what happens after the appointment for **clinical** purposes:
notes, photographs, aftercare, complications, retention.

Both boundaries are defensible on their own. Together they leave the commercial
relationship unowned in both directions. S1-S14 covers the patient lifecycle from *"a
booking exists"* to *"the record is retained for eleven years"*, and nothing outside
that. There is no component for what happens before a booking exists, and no component
for the commercial relationship between bookings.

That matters more here than it would elsewhere, because the engagement this plan sits
inside exists specifically to drive bookings. `puremed-growth-engagement-plan.md` states
the problem being solved as converting Nafisa's freed capacity into more bookings.
Every mechanism for doing that sits in the two zones the clinical platform does not
cover.

Nothing below asks MSS to build a sales CRM with pipelines and deal stages. The asks
are narrower: that the people exist as records, that their origin is recorded, and that
there is a loop back to them.

---

## A1. There is no lead or enquiry entity, and PureMed is already the controller for lead data it cannot enumerate

**What's missing.** The data model in `technical-design.md` §4 has exactly one person
entity, `patients`, brought into existence by a booking. Nothing represents a person who
enquired and did not book.

**Where those people currently are.** Every top-of-funnel route lands outside any system
PureMed controls:

| Route | Where the lead lands | Source |
|---|---|---|
| AI skin scanner | dermis.ai, lead data captured there | as-is 9 |
| AI voice agent calling scan leads, plus SMS follow-up | dermis.ai | as-is 9 |
| Meta ads pushing the scanner | dermis.ai | as-is 9 |
| Instagram satellites (Shuab's GTM, ~9-10 problem-led accounts) | Nafisa's personal WhatsApp | growth-engagement plan |
| Treatment microsites | Nafisa's personal WhatsApp | CLAUDE.md, microsites workstream |
| Direct WhatsApp and email enquiry | Nafisa's phone and Gmail | as-is 2.1 |

**Why it matters, in three separate ways.**

1. **A live data-protection exposure the register already half-names.** SEC-008 states
   plainly that PureMed is the controller for skin-scanner lead data. Controller
   obligations do not wait for a booking: Article 13/14 transparency, Article 15 access,
   Article 17 erasure and a defined retention period all attach to that lead population
   now. SEC-006 designs the SAR workflow as an admin export over the patient's record
   set keyed by `patient_id` (`technical-design.md` §8). A subject access request from
   somebody who used the skin scanner, got called by Aria, and never booked cannot be
   answered by that workflow at all. This is the same class of finding as SEC-009, and
   it is arguably more likely to be exercised.

2. **The conversion step nobody can measure.** The enquiry-to-booking step is where a
   WhatsApp-first practice leaks, and it is the single number the growth engagement most
   needs. It is currently unmeasurable in principle, not just unmeasured, because the
   enquiry leaves no record anywhere.

3. **No follow-up on a non-converting enquiry.** Somebody who asks about a treatment and
   does not book gets nothing, ever, because nothing knows they exist.

**What I'd change.** A `leads` (or `enquiries`) entity in Stage 1, deliberately thin:
contact details, source, treatment interest, status, outcome, and a nullable link to the
`patients` row it converts into. Not a pipeline. The point is that the population is
enumerable, answerable to a SAR, and countable against bookings. Register rows proposed
in Part C.

---

## A2. No source attribution on a booking. Near-free to add now, impossible to add retroactively

**What's missing.** `bookings` in `technical-design.md` §4 carries no `source`,
`campaign`, `referrer` or first-touch field. `booking-engine-plan.md` §4's entity table
does not carry one either. `patients` has no acquisition source.

**Why it matters.** `puremed-growth-engagement-plan.md` lists as an open item: *"No
sign-off yet on how 'drive bookings' will be measured (diary fill rate, booking count,
source attribution)."* Under the current posture this platform becomes the system that
holds every booking. It is therefore the only place attribution can ever land. If it
does not carry the field, the answer to "did the microsites work, did the satellites
work, did the skin scanner work" is permanently unavailable, and the entire GTM
workstream is run on impression.

The channels needing distinguishing already exist and are already numerous: seven
treatment microsites, roughly ten Instagram accounts, Meta ads to the scanner, the AI
voice agent, direct WhatsApp, the MailChimp newsletter, and word of mouth.

**Why the timing is the point.** Two columns and a query-parameter convention on the
booking entry points, decided now, costs close to nothing. Decided in twelve months, it
costs the same to build and everything before that date is unattributable forever. This
is the cheapest high-value row in this entire review.

---

## A3. No recall or reactivation, against what is probably the largest single asset in the estate

**The numbers already in canon.** The 15 August Acuity extraction: 588 client records,
54 with free-text notes, median 1,365 days (about 3.7 years) since last appointment,
**only 89 with an appointment inside the last year**, against roughly 475 records in
Faces. However the dedup lands, the dormant tail is very substantially larger than the
active base.

**The clinical reality that makes it actionable.** These treatments have natural repeat
intervals. The migrated dermal filler consent form in `faces-templates/` states the
effect "can last up to 12 months" and that additional treatments are required
"periodically, generally within 4-8 months". Toxin is shorter still. Every patient in
that dormant tail has a treatment date and a treatment type, which is exactly the data a
recall needs.

**What's missing.** Nothing in S1-S14 models when a patient is next due. There is no
recall interval on a service, no derived next-due date on a patient, no lapsed state, no
recall trigger. The only marketing mechanism anywhere in the register is COMM-005, which
replaces a manual CSV export into a bulk sender with a synced one. That is a real fix to
a real PECR problem (MIG-006), but it is still one weekly newsletter to everybody. It is
list hygiene, not retention.

**Why it belongs in this system specifically.** A recall that is worth opening needs to
know what the patient had, when, from whom, and what was recommended next. That data
exists in exactly one place under the new posture: S7 through S9. No adjacent system can
do this well, which is the same argument the plan uses correctly elsewhere against
splitting stores.

**What I'd change.** The *data* has to land in Stage 1, because every record migrated in
needs a last-treatment baseline at migration time. The *engine* can sit in Stage 4 next
to the rest of the comms work. One column on services, one derived field on patients,
and a job later.

**One line that needs drawing carefully.** A recall for a clinical follow-up (checking a
result, a review appointment) is plausibly transactional. "Your filler is due, book in"
is marketing and needs the COMM-001 opt-in. This is exactly the PECR trap the peer
review's Finding 8 describes in the WhatsApp context, and a recall engine walks into it
by default. The distinction needs to be a field on the message template, not a judgement
made per send.

---

## A4. The treatment plan is generated and then abandoned

PLAN-004 (Stage 4) generates a personalised treatment plan from the consultation record
carrying the patient's photograph, the findings, the recommended sequence and the
prices, and delivers it over WhatsApp. The as-is record calls this "the highest-value
manual artefact in the business", and Nafisa raised it unprompted.

Nothing records whether the plan was accepted. Nothing turns the recommended sequence
into offered or scheduled appointments. Nothing follows up on a plan that went quiet.

As specified, PLAN-004 automates the assembly of the document, which is the half that
costs Nafisa time. The other half of its value is that it is a recommendation with money
attached, and the system that generates it will be the only system that knows it exists.

Plan §3's S8 component blurb does say "acceptance, decline", but there is no register
row behind that. PLAN-003 covers clinically declined or unsuitable recommendations,
which is a professional-records requirement, not a commercial state.

---

## A5. Two customer masters, and the plan's own parallel-store argument is not applied to the commercial layer

The plan's central architectural argument, made three times (plan §9.1, §9.6,
`technical-design.md` §2), is that splitting "the thing patients book through" from "the
thing that holds their record" is the parallel-store problem, and that two systems kept
in sync indefinitely is worse than one. It is right, and it is the reason the current
posture exists.

That argument is never applied to the commercial relationship. Memberships, loyalty
point balances and Klarna checkout live entirely inside the dermis.ai app, with its own
user identity. PAY-009 and MIG-008 correctly refuse to design against a system nobody
has seen, and Nafisa intends to stay with dermis.ai.

But "out of scope until we know more" is a scoping decision, not an architectural
position, and the architectural consequence is not stated anywhere: after Stage 1,
PureMed has a clinical and booking master here and a commercial master (tier, points
balance, Klarna liability) there, permanently by design, with no join key between them.
A patient can be a member in one system and a patient in the other with nothing
connecting the two records.

That is the same failure mode the plan rejects everywhere else, on the commercial layer
instead of the clinical one, and nowhere named as such.

**What I'd change, without needing to know anything about dermis.ai's model.** Reserve a
`dermis_user_ref` on `patients` in Stage 1, the same way `payments.channel` already
reserves a `klarna_dermis` slot for recording rather than processing. And add one
specific question to the A6 onboarding call agenda: *which system is the customer master
for the commercial relationship, and what is the join key.* Otherwise A6 produces a
description of the app rather than the one answer that changes the schema.

---

## A6. Retention, reviews, referrals and discount codes are absent or orphaned

Individually small. Together they are the whole commercial side of the patient
relationship.

- **Discount codes** appear in plan §3's S3 component description ("deposits, full
  payment, card/wallet, cash/terminal/bank transfer recording, refunds, discount codes,
  payment status state machine") and in **no register row at all**. That is a
  traceability leak in the mechanism the plan's §4 exists to guarantee: a capability
  named in the component model with nothing behind it.
- **Referral pricing.** Nafisa said there is none today and that she is interested
  (as-is 3.5). Not in the register.
- **Post-treatment review request.** Not mentioned in any document reviewed. It is the
  standard aesthetics retention loop, it is the cheapest item on this list (one message
  on a trigger the Stage 4 aftercare engine already owns), and it has one non-obvious
  requirement: it must be suppressed for any treatment carrying a complication or
  adverse-event flag. Soliciting a public review from a patient who had a complication
  is a harm, not just a bad look.

---

## A7. Marketing execution is a stub, and one peer-review row that fixes it is unactioned

COMM-005 requires the marketing audience to be synced from the patient record rather
than rebuilt by manual CSV export. It implies MailChimp survives as the sender. Nobody
has actually decided that, or decided whether WhatsApp becomes a marketing channel,
which is where the practice's attention demonstrably is.

The peer review's Finding 8 proposed a new row (MIG-009): a distinct, fresh opt-in
capture for WhatsApp marketing specifically, never inferred from transactional WhatsApp
use or from migrated contact data. It has not been added to the register. Given that
A3's recall engine is the most likely thing to want to send over WhatsApp, this stops
being a theoretical PECR point and becomes the gate on the highest-value feature in this
review.

---

# Part B: other things missed

## B1. The 15 August peer review is essentially unactioned, and that is the largest single piece of unfinished business in the folder

`peer-review-2026-08-15.md` produced twelve findings. Grepping canon for their effects:
**only Finding 10 has been folded in**, referenced twice (the multi-site question,
answered by Nafisa's confirmation that the PureMed room is exclusive, and the
`practitioner_competencies` expiry-tracking note in action item 2).

Not reflected anywhere in the plan, register or technical design:

| Finding | Status in canon |
|---|---|
| 1. Remote prescribing has tightened; video is not a substitute for a first in-person assessment | §2.2 still says "may require"; BOOK-001 unchanged. The reviewer called this the single highest-priority sign-off gap because it shapes the Stage 1 booking journey |
| 2. Whitehouse record-ownership and controllership | Not added to the outstanding action items |
| 3. The CQC dividing line (diagnosed disease/disorder vs cosmetic purpose) is uncited | Not added to §2.4 or REC-004 |
| 4. GDC removed cosmetic injectables from Scope of Practice Guidance, Nov 2025 | §2.3 still frames it as "GDC guidance permits this provided..." |
| 5. Licensing scheme three-tier model confirmed 7 Aug 2025; DIARY-001/PLAN-001/PLAN-002 are closer to future-Regulatory than Best-practice | §2.9 still describes an ongoing consultation; no register annotations added |
| 6. Field-level RBAC enforced only in the application layer | `technical-design.md` §8 unchanged |
| 7. No requirement capturing the individualised risk conversation, separate from the signed form | No S8 row added |
| 8. WhatsApp marketing opt-in (proposed MIG-009) | Not added |
| 9. Guest checkout: email verification before dispatching clinical documents | Not added |
| 11. Consent re-basing is correct, worth stating explicitly | Not stated |
| 12. Two missing sign-offs (indemnity insurer on cross-referral; prescribing dentist on the toxin pathway) | Not added to the action list |

The reviewer's verdict was that Findings 1 and 2 *shape* rather than inform Stage 1 and
should be resolved in parallel with starting it. Anything I propose in Part C sits
behind that.

## B2. The plan contradicts itself on two of its four decision gates, and one resolution weakens the buy-vs-build case

Plan §9.5 lists four decisions gating this phase. Items 1 (the deposit contradiction)
and 2 (the working pattern) are written as open, with item 1 saying "Stage 3 cannot
start until one is chosen".

Later in the same file, outstanding action items 5 and 6 record both as **RESOLVED on 15
August**: everyone pays a deposit with no exceptions, and Wed 10-3 / Fri 1-5 expanding
to Thu then Mon.

Meanwhile the register still carries BOOK-005 and BOOK-006 as "conflicts, needs one
decision", and `puremed-systems-proposal.md` still asks Nafisa for both as two of its
three open decisions. Four documents, three positions.

**The consequence nobody has traced.** "Everyone pays, no exceptions" retires BOOK-006's
graduated, occurrence-counting no-show model. BOOK-006 is one of the four reasons
`buy-vs-build-spike-2026-08-15.md` gives as decisive for building rather than buying:

> 2. Channel-parity (BOOK-004) and graduated no-show enforcement (BOOK-006) are also
> unsupported, and BOOK-004 in particular reproduces PureMed's current failure mode if
> bought rather than built.

Half of reason 2 has now evaporated. The case still stands on BOOK-004 (channel parity),
BOOK-007 (the prescriber-AND-practitioner dependency), BOOK-008 (cross-entity CQC
routing) and the commercial multi-tenant argument, so the conclusion does not change.
But the spike should be corrected rather than left overstating its own case, for the
same reason it was written: it would not survive a specialist reading it.

Separately, I would still keep the occurrence counting in the event log even though the
policy no longer uses it, because "repeat offenders" is a named, live problem (as-is
2.7) and a universal deposit policy is a decision that can be revisited.

## B3. Future bookings and diary state have no migration design

Plan §6.3 maps booking and appointment history to a read-only historical view inside S7,
explicitly *"not re-entered into the live diary"*. §6.5's shadow period keeps Faces live
and readable for lookup while the new system takes new bookings.

Neither covers the appointments already booked into the future on cutover day. On a two-
day-a-week practice with a 48-hour cancellation window, that forward diary will be
populated and live. As currently designed, those bookings sit in a system nobody is
writing to, while the calendar of record moves elsewhere. That is the exact failure the
whole DIARY-004 single-writer requirement exists to prevent, reintroduced at the moment
of cutover.

`puremed-growth-engagement-plan.md` flags this as a new gap surfaced on 15 August. The
clinical-platform canon does not carry it. It needs a stated approach (most likely:
re-enter the forward diary manually into the new system before cutover, since the
volume is small and the alternative is a two-calendar week) and it belongs in §6.

## B4. No dedup or survivorship design for 588 versus 475

`technical-design.md` §5.2 loads into a staging schema and reconciles record counts and
a spot-check sample before promotion. It never merges the two sources, and no rules are
stated for how.

Two hard questions are unanswered: what key matches an Acuity record to a Faces record
(email, phone, name plus DOB, and what happens when they disagree), and which value wins
when both hold a different address or phone number. Acuity's records are a median 3.7
years stale, so contact details will conflict routinely rather than exceptionally.

Both error modes are serious in a clinical record. Merging two different people produces
a record with someone else's medical history in it. Splitting one person in two produces
two half-histories, one of which will be missing an allergy. A count reconciliation
catches neither.

This needs explicit match and survivorship rules, plus a human-review queue for anything
that is not an exact match, which given the volumes (a few hundred candidates at most) is
entirely tractable.

## B5. The migration depends entirely on the goodwill of the vendor being replaced, with no deadline and no priced fallback

Confirmed on 15 August: Faces has no self-serve bulk export anywhere in the admin UI, so
the DPA data request is the only path, and it is submitted and unanswered.

The plan carries this as a status, not as a risk with a plan behind it. Missing: the
legal lever stated explicitly (Article 28(3)(g), a processor must return or delete
personal data at the controller's choice at the end of provision of services, plus the
28(3)(h) assistance obligation, plus whatever the contract says, which nobody has read
yet, per action item 4); a date at which no response becomes an escalation; and a costed
fallback, which at 475 records is plausibly assisted or manual re-keying and is a real
line item, not a footnote.

Per the standing note on this, do not re-run the export check or build a scripted UI
extraction until Faces' response is known to be inadequate. This is about setting the
date and pricing the fallback, not about going around them.

## B6. In-room offline behaviour is unaddressed, and it is the sharpest form of the abandonment risk the whole plan is built around

Stage 2 puts two things on a device in a treatment room: bulk photo capture, and the
toxin prescribing record with two signatures, "completed at the point of treatment"
(NOTE-005). `technical-design.md` §6.3 sequences capture, batch upload and deletion
assuming connectivity throughout.

The plan's own acceptance bar, argued at length and correctly, is "fewer steps than
today, on day one", justified by two proven abandonments of technically-correct
processes that were slower than the shortcut.

Paper never fails. A prescribing record that cannot be completed because the signal
dropped, with a prescriber standing there waiting to sign, sends the workflow straight
back to the paper form, and the entire point of NOTE-005 is that the paper form is the
one document that leaves the system. One occurrence is enough to re-establish the habit.

This needs an explicit requirement: local-first capture with deferred sync, signatures
captured offline, the record marked pending-sync and reconciled when connectivity
returns, and PHOTO-007's device deletion gated on confirmed upload as already specified
(which is compatible, and already correctly sequenced). Plan §5 gap 11 raises business
continuity as a policy question about read access during an outage, which is a different
and lesser problem than write access mid-treatment.

## B7. The compliance workflows this plan creates have no operator

There is no receptionist, no admin, and nobody else in the business day to day
(as-is 6.1). The plan's own strongest argument rests on that fact.

Stage 1 and 2 create, correctly and for good reasons: a DPA register maintained with
renewal dates (SEC-005, SEC-008), a breach register and 72-hour notification capability
(SEC-007), a SAR workflow with a defined turnaround (SEC-006), an 11-year retention
engine (REC-002), a batch/lot recall query (NOTE-002), a one-off paper backlog
remediation (NOTE-006), and a marketing consent reconciliation (MIG-006).

Every one of those is right. All of them land on the person who stopped uploading
clinical photographs because it was one step too long, and who has "shitloads of
paperwork sitting there" she has not done.

The plan applies the "fewer steps than today" test rigorously to the clinical workflows
it is replacing, and not at all to the compliance workflows it is creating. Those
obligations are worse than absent if they exist on paper and are not operated, because
an unoperated register is evidence of a known, undischarged obligation.

Two ways out, and it should be a decision rather than a discovery: design each of these
to be near-zero-touch (the DPA register as a static document with a calendar reminder,
retention as an automated job with an exception report, SAR as a one-click export), or
somebody other than Nafisa operates them. The second is a commercial question as much as
a design one, and it is the natural shape of a retainer.

## B8. Smaller notes

- **The migrated payment ledger will be structurally incomplete and should be labelled
  as such.** Plan §6.3 maps payment history from Faces into a read-only ledger and says
  to reconcile totals against the source. Five of the six live payment channels (SumUp,
  Dojo, bank transfer, GoCardless, Klarna) never touched Faces at all (as-is 3.1), so
  the migrated ledger covers only the Faces-integrated card channel. That is fine and
  unavoidable, but it should be stated, so that nobody downstream treats the pre-
  migration ledger as a financial record of what a patient has actually paid.
- **`booking-engine-plan.md` §14's CRM risk row needs rewording.** "Everything after the
  appointment is out" was a sound boundary when that document described a booking
  widget. Under the current posture it describes a boundary nobody is holding, since the
  same service now owns the clinical record, aftercare and treatment plans. Left as-is,
  it will be cited later to reject exactly the work in Part A.

---

# Part C: proposed changes

Ordered by whether they cost anything to do now.

## C1. Do in Stage 1 because they are near-free now and impossible later

Four schema additions, all small, all irreversible if skipped:

| Addition | Why now |
|---|---|
| `leads` entity (contact, source, treatment interest, status, outcome, nullable `patient_id`) | The population has to exist to be SAR-answerable and countable |
| `bookings.source` and `patients.acquisition_source` (plus campaign / first-touch where a URL carries it) | Retroactive attribution is impossible; every booking taken without it is permanently unattributable |
| `services.recall_interval_days`, derived `patients.next_due_at` | Every migrated record needs a last-treatment baseline set at migration time |
| `patients.dermis_user_ref` (reserved, unpopulated) | Same pattern as `payments.channel`'s reserved `klarna_dermis` slot; costs one nullable column |

Plus: keep cancellation and no-show occurrences in the event log even though the
universal deposit policy no longer consumes them (B2).

## C2. New register component and rows

Propose **S15: Patient Relationship and Retention**, so these have somewhere to live
that is not a footnote on S5.

| Req ID | Requirement | Type | Stage |
|---|---|---|---|
| CRM-001 | A lead/enquiry is a first-class record distinct from a patient, carrying source, treatment interest, status and outcome, and convertible into a patient record | **Reg**/Pol | 1 |
| CRM-002 | SEC-006's SAR workflow, SEC-005's retention policy and the Art 13/14 transparency notices extend to lead data, not only patient data | **Reg** | 1 |
| CRM-003 | Every booking and every patient carries an acquisition source, with campaign/first-touch where the entry point supplies it | Pol/UX | 1 |
| CRM-004 | Each service carries a clinically-appropriate recall interval; each patient carries a derived next-due date maintained from the treatment record | BP/Pol | 1 (data), 4 (engine) |
| CRM-005 | Recall and reactivation messages are classified transactional or marketing at the template level, with marketing gated on the COMM-001 opt-in | **Reg** | 4 |
| CRM-006 | A treatment plan carries an acceptance state, and its recommended sequence is convertible into offered bookings with follow-up | Pol/UX | 4, extends PLAN-004 |
| CRM-007 | Post-treatment review request as an aftercare trigger, gated on marketing consent and suppressed for any treatment carrying a complication or adverse-event flag | Pol/UX + **Reg** edge | 4 |
| CRM-008 | Discount codes and referral credit (currently named in plan §3's S3 blurb with no register row behind it) | Pol | Backlog |
| CRM-009 | A stated position on which system is the customer master for membership, loyalty and commercial state, with a join key | Pol | Blocked on A5/A6 |
| MIG-009 | Fresh, distinct opt-in for WhatsApp marketing, never inferred from transactional WhatsApp use or migrated contact data | **Reg** | Before any Stage 4 marketing send |

MIG-009 is the peer review's Finding 8, restated here because it now gates CRM-004/005
as well as COMM-005.

## C3. Fix in canon

> **APPLIED 16 August 2026, all eight items.** Plan bumped to v0.4 (peer review folded in
> across 2.2, 2.3, 2.4, 2.9, 3.1, new gaps 5.13 to 5.15, 6.4, new 6.6, 9.5 reconciled,
> action items 11 to 13 added). Register bumped to v0.4 (BOOK-001 rewritten, BOOK-005/006
> resolved, DIARY-001/006, REC-001/004, PLAN-001/002 annotated, new ACCT-004, PLAN-005,
> MIG-009, plus NOTE-005/PHOTO-005 offline, MIG-001/002/005/008 updated).
> `technical-design.md` bumped to v0.2 (`practitioner_competencies`, RBAC hardening, match
> and survivorship rules, forward-diary step, offline capture 6.2a).
> `buy-vs-build-spike-2026-08-15.md` reason 2 corrected. `booking-engine-plan.md` §14 CRM
> risk row reworded. `../puremed-systems-proposal.md` cut from three open decisions to
> one, with the Whitehouse record-ownership question added.
>
> **C1 and C2 APPLIED 16 August 2026, same day, later session.** `requirements-register.md`
> bumped to v0.5 (new S15 component, CRM-001 to CRM-009, real Reg/BP/Pol/UX sources against
> each, not placeholders). `puremed-clinical-platform-plan.md` bumped to v0.5 (S15 added to
> the Section 3 component table; new Section 5.16 stating the A0 structural cause).
> `technical-design.md` bumped to v0.3 (Section 4 gains `leads`, `bookings.source` /
> `patients.acquisition_source`, `services.recall_interval_days` / `patients.next_due_at`,
> and confirms `patients.dermis_user_ref`; states which are Stage 1 data versus Stage 4
> engine and why the data cannot wait for the engine; Section 8's SAR workflow extended to
> `leads`, not only `patients`, per CRM-002). Kept deliberately narrow throughout: no
> pipeline, no deal stages. The transactional/marketing line for recall messages is drawn
> at the message-template level (CRM-005), not per-send, per Finding 8's PECR trap.

1. **Fold the peer review in.** Findings 1 and 2 first, since the reviewer flagged both
   as shaping Stage 1 rather than informing it. This is the single highest-value pass
   available on this folder right now, and it predates anything in this document.
2. **Resolve the §9.5 contradiction** (B2). Mark decision gates 1 and 2 resolved in
   §9.5, retire or reclassify BOOK-005/BOOK-006 in the register, and update the
   proposal's three-decisions section to two. Keep the superseded text in place per the
   dated-confirmed-direction convention.
3. **Correct the buy-vs-build spike's reason 2** (B2), since BOOK-006's graduated model
   is retired by the universal deposit decision.
4. **Add the forward-diary migration approach to plan §6** (B3).
5. **Add match and survivorship rules plus a review queue to `technical-design.md` §5.2**
   (B4).
6. **Add offline-capable in-room capture as an explicit requirement** on NOTE-005 and
   PHOTO-005, and to `technical-design.md` §6 (B6).
7. **Label the migrated payment ledger as partial** in plan §6.3 (B8).
8. **Reword `booking-engine-plan.md` §14's CRM scope-creep risk row** (B8).

## C4. Decisions and questions for other people

Additions to the outstanding action items list:

1. **Add to the A6 dermis.ai onboarding call agenda:** which system is the customer
   master for the commercial relationship, and what is the join key (A5). Without this
   the call yields a description rather than the one fact that changes the schema.
2. **Set a response deadline on the Faces data request**, and cost the assisted or
   manual extraction fallback at 475 records before that date rather than after it (B5).
3. **Decide who operates the compliance registers** (B7): near-zero-touch design, or a
   retainer. This is commercial, not architectural, but it needs deciding before the
   obligations exist.
4. **The two sign-offs from peer review Finding 12** (indemnity insurer on the
   Whitehouse cross-referral, prescribing dentist on the toxin booking pathway), still
   not on the action list.

---

## Resume prompt

> Read `main-stage-studio/02_clients/puremed/clinical-platform/crm-and-lifecycle-gap-review-2026-08-16.md`.
> It reviews plan v0.3 / register v0.3 / technical-design v0.1 and finds that CRM falls
> between `booking-engine-plan.md`'s explicit "everything after the appointment is out"
> boundary and the clinical platform's clinical-only after-appointment scope, leaving
> leads, attribution, recall and the commercial relationship unowned. Part C lists the
> proposed changes. Nothing in canon has been edited yet. The highest-value next action
> is folding `peer-review-2026-08-15.md`'s eleven unactioned findings into the plan and
> register, starting with Findings 1 and 2.
