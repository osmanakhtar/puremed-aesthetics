# Independent review: PureMed clinical platform plan

Reviewer: fresh-context agent, no prior involvement in authoring the plan, register or
technical design. Review date: 15 August 2026. Method: read
`puremed-clinical-platform-plan.md` v0.3, `requirements-register.md` v0.3,
`technical-design.md` v0.1 in full; skimmed `booking-engine-plan.md` and
`main-stage-studio/02_clients/puremed/CLAUDE.md`; checked current UK regulatory guidance
by web search rather than relying on training-data recall, since the plan itself flags
this area as actively moving and unreviewed.

Findings are ordered most load-bearing first, per the brief's output format. "Load-bearing"
here means: if this is wrong, how much of the rest of the document has to be redrawn.

---

## Finding 1: The remote-prescribing rule has tightened past what Section 2.2 and BOOK-001 assume, and it constrains the shape of the online booking journey, not just a process detail inside it

**What's wrong.** Plan Section 2.2 states the first prescribing assessment "may require"
being in person or by video, "not questionnaire alone" — framed as one option among a
few. Register row BOOK-001 repeats this as "online consultation booking for toxin
treatment gated behind an adequate prescribing assessment path, not questionnaire alone."
Both treat video as a live, acceptable substitute for in-person.

Current guidance has moved past that. The NMC's position, in force since 1 June 2025,
requires prescribers to have completed a face-to-face consultation before prescribing
cosmetic injectables remotely is even considered acceptable; from July 2026 the rule
tightened further, restricting "prescribe and supply" arrangements where the prescriber
has never assessed the patient in person. This is a general direction-of-travel across UK
prescribing professions (NMC explicitly, GPhC moving the same way), and there is no
indication GDC-registered dentists sit outside it — dentists prescribing outside dentistry
are still bound by the same Human Medicines Regulations 2012 "adequate assessment"
standard the plan itself cites in 2.2, and that standard is what the professional bodies
are now interpreting as requiring an in-person first assessment for this drug class.

**Why it matters.** BOOK-001 is the linchpin of the entire "online consultation" premise
for toxin bookings — the plan's Stage 1 booking journey is built around a client
completing screening online before a slot is confirmed. If the prescriber must physically
assess the patient before a first toxin prescription can be issued, "online consultation
gated behind an adequate prescribing assessment path" cannot mean what it currently
implies (a remote screening that clears the way to book). It has to mean something
narrower: online screening clears the patient to book an *in-person* first appointment
with the prescriber present, and the prescribing decision itself happens at that
appointment, not before it. That's a different UX shape (the online step becomes a
triage/eligibility gate, not a consultation substitute), and it has knock-on effects on
BOOK-007/DIARY-005 (already correctly modelled as a hard prescriber-availability
constraint, which turns out to be doing more regulatory work than the plan credits it
for) and on how the "adequate assessment" language in CONS-009 gets built.

**What I'd change.** Rewrite Section 2.2 to state plainly that remote prescribing of
botulinum toxin without a prior in-person assessment is not currently acceptable
practice for a first-time prescription (cite NMC's 1 June 2025 position and the July 2026
prescribe-and-supply tightening explicitly, and get the prescribing dentist to confirm
whether any GDC-specific equivalent exists or whether they're relying on the same HMR
2012 standard other prescribers are). Reframe BOOK-001 from "gated behind an assessment
path" to "in-person first assessment is a hard prerequisite for a first toxin
prescription; online steps establish eligibility and book that in-person slot, they do
not substitute for it." This is a design decision that needs the prescribing dentist's
sign-off before the booking journey's step sequence (booking-engine-plan.md Section 3,
steps 3/5/6) is finalised for toxin services specifically — it changes what "screening"
in step 3 is for.

---

## Finding 2: Cross-practice referral to Whitehouse raises a controllership and record-ownership question the plan names but doesn't resolve, and "verify their registration covers it" doesn't answer it

**What's wrong.** Section 2.4 and the outstanding action items correctly flag that
Whitehouse's CQC registration needs verifying against the specific regulated activity,
provider and location. But that's a coverage check, not a data-governance answer. Once a
regulated treatment (hyperhidrosis toxin, jaw toxin for bruxism/clenching — both
correctly identified, see Finding 3 below on why) is delivered under Whitehouse's
registration, CQC expects the records of that regulated activity to be held by the
registered provider delivering it. `technical-design.md` Section 4 puts `provider_locations`
as a table inside PureMed's own Postgres schema, with a `provider_location_id` foreign
key on `bookings`, and REC-004 describes this as "distinct from the treating
practitioner." But the plan never asks: is PureMed's system the system of record for a
Whitehouse-regulated treatment, or does Whitehouse's own record system need to be the
authoritative one, with PureMed's copy demoted to a reference/scheduling artefact? Those
are materially different answers, because CQC registration carries its own record-keeping
obligations attached to the registered provider, and "PureMed operated the booking flow
and holds the note" versus "PureMed booked it, Whitehouse's own system holds the clinical
record" changes who's the Article 9 data controller for that specific treatment, not just
where a foreign key points.

**Why it matters.** This isn't a hypothetical edge case — two named treatments already
run this way today (as-is 4.4), so it's live volume from day one, and S9/S7 (Stage 1-2)
are being built now. If the schema is built assuming PureMed is the controller/record-
holder for Whitehouse-delivered treatments and that turns out to be wrong, it's a rebuild
of the S7/S9 access model and the DPA/controllership documentation, not a config change.

**What I'd change.** Add an explicit question to the outstanding action items: "For
treatments delivered under Whitehouse's CQC registration, does the clinical record live
in PureMed's S7, in Whitehouse's own system, or in both with one designated as
authoritative — and who is the data controller for that record?" This needs answering by
whoever holds Whitehouse's CQC registration (may not be Nafisa), not inferred from
PureMed's own preference, before REC-004's schema is treated as settled.

---

## Finding 3: The CQC basis for the two named regulated treatments is correct but uncited, and the underlying mechanism should be named explicitly

**What's wrong.** REC-004 and BOOK-008 correctly single out hyperhidrosis toxin and jaw
toxin for clenching/bruxism as needing Whitehouse's CQC registration, while the plan is
equally correct that ordinary cosmetic botox/filler doesn't need CQC registration at all.
But nowhere does the document state *why* these two specific treatments cross the line
while cosmetic toxin doesn't. Current CQC guidance draws that line on "treatment of
disease, disorder or injury" (a regulated activity under the Health and Social Care Act
2008 framework): botox for hyperhidrosis treats a diagnosed medical condition (excess
sweating), and botox for bruxism/TMJ dysfunction treats a diagnosed disorder, whereas
purely cosmetic injectable use for cosmetic purposes does not. This is exactly the kind
of thing the review brief asks for under point 1(c): a claim stated correctly but without
the citation that would let a lawyer verify it in one pass.

**Why it matters.** Without the mechanism named, nobody building against this register
row can tell whether a *third* treatment (say, toxin for chronic migraine, if PureMed
ever adds it) needs the same routing, because the rule as written ("hyperhidrosis, and
jaw toxin for clenching") reads as an enumerated list rather than an application of a
general test. A new treatment that also treats a diagnosed disorder would silently miss
this gate unless the underlying rule is explicit.

**What I'd change.** Add one sentence to Section 2.4 and REC-004: "The dividing line is
whether the treatment addresses a diagnosed disease, disorder or injury (a CQC regulated
activity) versus a purely cosmetic purpose (not regulated); this is why hyperhidrosis and
bruxism-related jaw toxin are routed to Whitehouse and cosmetic toxin/filler is not, and
the same test should be applied to any future treatment added to the catalogue."

---

## Finding 4: Section 2.3's GDC framing is now stated the wrong way round, following a real guidance change the plan predates in spirit even though it postdates it in time

**What's wrong.** Section 2.3 frames the dentist-doing-cosmetic-injectables question as
"GDC guidance permits this provided the practitioner holds appropriate training… operates
within their declared scope of practice," i.e. a specific accommodation carved out by GDC
guidance. As of the GDC's Scope of Practice Guidance update (November 2025 — before this
plan's 8 August 2026 first draft, so this isn't a currency gap in the "moved since it was
written" sense the brief asked about, it's a plain sourcing miss), non-surgical cosmetic
injectables were *removed* from that guidance entirely, on the basis that this work is
not the practice of dentistry at all and therefore isn't something GDC scope-of-practice
guidance governs one way or the other. Dentists doing this work remain accountable to GDC
for general professional conduct (honesty, fitness to practise, indemnity), but the
"permitted under wider prescribing competence, provided declared scope" framing overstates
how specifically GDC has blessed it — there's no GDC carve-out to point to, because GDC
guidance doesn't reach this activity at all.

**Why it matters.** The task brief specifically asks whether the hedge here is strong
enough given how load-bearing this point is (it underpins BOOK-001, NOTE-004, DIARY-001).
It isn't quite the right hedge. As currently written it reads as "GDC has considered this
and permits it under conditions," which invites a reader to go looking for the specific
GDC clause that says so. The more accurate (and, if anything, more cautious) framing is
"GDC guidance is silent on this because it falls outside dentistry; the practitioner's
authority to do it at all rests on generic training/competence/indemnity standards common
to any professional performing cosmetic injectables, not a dentistry-specific permission."
That's a materially different thing to ask a specialist to sign off on: not "confirm GDC's
scope-of-practice carve-out applies here" but "confirm what standard — since GDC's own
guidance doesn't set one for this activity — PureMed is holding its dentists to."

**What I'd change.** Rewrite Section 2.3 to state the GDC's November 2025 position
correctly (cosmetic injectables removed from Scope of Practice Guidance as outside
dentistry) and reframe the sign-off ask from "confirm the GDC carve-out" to "confirm what
non-GDC-specific training/competence standard PureMed is adopting," since that's the
actual open question. DIARY-001's "scope-of-practice attribute" language should be
renamed to something like "declared competence and training basis," since "scope of
practice" implies a GDC-defined boundary that, per the update, doesn't exist for this
activity.

---

## Finding 5: Section 2.9 undersells how concrete the incoming licensing scheme already is, and several register rows currently tagged Best-practice are closer to becoming Regulatory than the plan implies

**What's wrong.** Section 2.9 describes the Health and Care Act 2022 licensing scheme in
vague terms ("consultation and phased implementation ongoing through 2025-2027"). The
government actually published a formal consultation response on 7 August 2025 — over a
year before this plan's first draft — confirming a specific three-tier Red/Amber/Green
risk model. Amber tier explicitly includes botulinum toxin and facial dermal fillers, and
the confirmed shape requires a local-authority licence *plus* oversight from a named,
appropriately qualified regulated healthcare professional. That "named professional
oversight" requirement is strikingly close in shape to what DIARY-001 (currently tagged
Best-practice, sourced only from indemnity-insurer/GDC-CPD norms) already proposes.
Similarly PLAN-001 (cooling-off period) and PLAN-002 (vulnerable-patient screening) are
JCCP/Save Face-sourced Best-practice items that the Amber-tier licensing standards are
likely to formalise into something closer to Regulatory once the scheme's detailed
standards consultation (expected during 2026) lands.

**Why it matters.** This is a traceability-integrity issue (task point 3), not just a
currency one: several rows are classified Best-practice on the basis that they're
discretionary-but-recommended, when the actual regulatory runway for at least DIARY-001
is now roughly "confirmed policy direction, implementation detail pending" rather than
"industry good practice PureMed may or may not choose to hold itself to." Building
DIARY-001 to a Best-practice priority level risks a rebuild in 2026-2027 when the licensing
detail lands, exactly when Section 2.9's own advice ("build so a licence number can be
attached later without a schema change") is trying to avoid.

**What I'd change.** Update Section 2.9 with the confirmed three-tier model and its
7 August 2025 publication date. Add a register annotation on DIARY-001, PLAN-001 and
PLAN-002 flagging them as "Best-practice today, high-confidence future-Regulatory under
the Amber-tier licensing scheme" so build priority reflects that rather than treating
them as ordinary discretionary best-practice.

---

## Finding 6: Field-level RBAC is enforced only in the application layer, inconsistent with the append-only design's own stated philosophy

**What's wrong.** `technical-design.md` Section 8 states RBAC and field-level permission
checks "live in the Fastify service layer, not the client," explicitly contrasted with
the append-only enforcement in Section 4, which is deliberately pushed to the database
role level so it's "structurally impossible to violate by a future code change, not
merely policy." REC-001 (reception sees medical alerts without full clinical detail) is
tagged Regulatory in the register, sourced to UK GDPR data minimisation and professional
confidentiality — the same weight class as the append-only requirement. But the design
doc gives it a weaker enforcement guarantee: any new report, export, or debug endpoint
written in the service layer could leak full clinical fields to a reception-role token
unless every new code path is manually disciplined to re-apply the filter.

**Why it matters.** This is exactly the kind of gap the plan's own architecture
principles (3.1: "this is a role-based field-level permission requirement, not just a
page permission, and should be modelled as such from the start") warn against, applied
inconsistently one layer down in the technical design. A real build with multiple
contributors over time is where application-layer-only permission checks quietly regress.

**What I'd change.** Where practical, back field-level RBAC with Postgres row-level
security / column-level policies or restricted views scoped to role, not just service-
layer logic, mirroring the append-only pattern. At minimum, add an automated test suite
asserting no reception-scoped query can return the restricted fields, run in CI, so a
regression fails the build rather than surfacing in production.

---

## Finding 7: The gaps list misses a distinct "defensibility of what was actually discussed" requirement, separate from the signed consent form itself

**What's wrong.** The brief for this review specifically asked whether the gaps list
missed anything around insurance claims defence — the point of several requirements here
being defensibility if a patient later disputes what they were told. CONS-002/003/006
cover the *form* (what was signed, version-locked, audited). S8's consultation record
covers goals and findings. But there's no distinct requirement for capturing what was
specifically discussed and warned about with *this* patient, in their own case — the
individualised risk conversation that a signed generic consent document doesn't evidence
on its own. Insurer/indemnity defence in a dispute typically turns on whether the
practitioner can show the specific risks discussed with this patient (not just that a
standard form was signed), especially for anything outside the textbook case.

**Why it matters.** A signed, version-controlled consent form (which the plan does
handle well) proves the patient was given standard information. It does not, on its own,
prove what was actually said in the room if a patient later claims "nobody told me X
specific thing about my case." Since the stated purpose of several of these requirements
is exactly this kind of defensibility, the gap is directly on-point for what this
document is trying to achieve.

**What I'd change.** Add a gap: a structured, brief free-text or checklist field on the
consultation record (S8) capturing the specific risks/alternatives discussed with this
patient beyond the standard form content, signed/timestamped alongside the rest of the
note. Low build cost, direct defensibility value.

---

## Finding 8: WhatsApp's status as "first-class channel" blurs a PECR line the register technically keeps separate

**What's wrong.** COMM-004 correctly notes PECR applies to marketing sends over WhatsApp
and not to transactional ones, and COMM-001 requires a distinct opt-in flag. But COMM-004
also describes WhatsApp as carrying "booking confirmations, deposit payment links,
aftercare and treatment plans" as one undifferentiated first-class channel, and the
existing operating model (as-is 7.4) already treats WhatsApp as the general operating
surface, not something patients experience as split into "transactional WhatsApp" and
"marketing WhatsApp." Current ICO guidance is explicit that a phone number collected for
a booking is not consent to receive marketing on that number, and messaging-app
promotional sends are squarely inside PECR (subject to the same £17.5m/4%-of-turnover
maximum fine tier as email). MIG-006 reconciles Faces/MailChimp *email* opt-outs at
migration but has no equivalent row for WhatsApp number reuse — the 475+588 migrated
contacts' WhatsApp numbers, gathered for booking purposes, need their own fresh marketing
opt-in before COMM-005 (Stage 4, marketing audience sync) or COMM-006 could lawfully use
them for anything promotional.

**Why it matters.** Given how central WhatsApp already is operationally, the practical
risk is that a future marketing send over WhatsApp gets built on the assumption "we
already message these people on WhatsApp for bookings, so it's fine" — which is precisely
the PECR trap the guidance warns about, and precisely the channel PureMed relies on most.

**What I'd change.** Add a register row (extending MIG-006 or a new MIG-009) requiring a
distinct, fresh opt-in capture for WhatsApp marketing use specifically, not inferred from
transactional WhatsApp usage or migrated contact data, before COMM-005/006 go live in
Stage 4.

---

## Finding 9: Guest checkout's "verified email/secure link" delivery mechanism for special-category documents isn't specified, and that's exactly where the reversal is weakest

**What's wrong.** Section 3.1's guest-checkout argument is otherwise solid: the
underlying S7 record, age gate, and consent flow all fire identically for a guest, which
correctly answers what the review brief asked (walk it through end to end). Where it
thins out is the phrase "reach them by a verified email/secure link rather than an
account login" — "verified" is asserted, not designed. An account login is, by
construction, something only the account holder can access after the initial
authentication. A "secure link" sent to an email address typed in at booking time is only
as strong as whatever verifies that email actually belongs to the person being treated
(or, for a minor's guardian, the right adult) — and nothing in the plan or technical
design specifies an email-verification step (confirm-your-email loop) before consent
PDFs, aftercare instructions or the S7 record link are sent to it.

**Why it matters.** This is the actual place the guest-checkout reversal is weaker than
an account-holder flow, not the places the plan's own defence in 3.1 addresses (the
clinical-record and consent-lifecycle obligations, which do fire the same either way).
Special-category clinical documents (consent PDFs, aftercare containing treatment
details) going to an unverified email address is a live UK GDPR Article 32 security
exposure specific to the guest path, and it's the one part of the argument the plan
doesn't actually stress-test.

**What I'd change.** Add a requirement: guest bookings require email verification
(confirm-link click, standard pattern) before any clinical document is dispatched to that
address, and before the booking is treated as confirmed if the document delivery is
time-critical (e.g. pre-treatment consent). This is a small, cheap addition that closes
the actual gap in an otherwise sound argument.

---

## Finding 10: Two further gaps in the gaps list — per-treatment competency granularity, and multi-site data segregation

Two items the review brief asked to check for specifically, both genuinely missing:

- **Per-treatment competency, not just overall qualification.** DIARY-001/006 model a
  practitioner's qualification and indemnity as a single gate ("cannot be booked for a
  treatment their record doesn't authorise"), which is good, but the underlying data
  model (`practitioners.qualification_expiry`, `indemnity_expiry`) implies one expiry per
  practitioner rather than per treatment-type competency. A practitioner trained and
  insured for toxin but not for a newer filler technique needs the gate to work at
  treatment-type granularity, not practitioner granularity — increasingly important given
  the Amber-tier licensing scheme's named-professional-oversight-per-procedure shape
  (Finding 5). Recommend a `practitioner_competencies` join table (practitioner ×
  treatment type × qualification/indemnity/expiry), not a flat field on `practitioners`.

- **Multi-site/multi-brand data segregation.** Not addressed anywhere. PureMed and
  Whitehouse already operate as two clinical entities sharing at least one practitioner
  (Finding 2 territory). If PureMed opens a second location, or the Whitehouse
  relationship deepens, the schema needs the provider/location distinction already
  established for REC-004 to generalise cleanly to genuine multi-tenancy within PureMed
  itself, not just the booking-engine's cross-client multi-tenancy. Worth a one-line
  design note confirming `provider_locations` is intended to carry this weight if it
  comes up, since nothing currently states that intent explicitly.

---

## Finding 11: The consent re-basing decision (6.4) is the right call, not overly conservative — this is a place the plan under-argues a decision it got right

The review brief asked specifically whether treating all legacy consent as
historical-only is correct or overly conservative given the brief's "exceptional
experience" goal. It's correct, and more clearly so than the plan's own reasoning states.
Informed consent has to be current to the specific treatment being given now — a
patient's understanding of risks, techniques and products can meaningfully shift over the
gap since a legacy signature (some Acuity records are 3.7 years stale per the 15 August
extraction), and GDC record-keeping standards plus indemnity-insurer guidance already
require reconfirmation before every treatment regardless of migration history. There is
no real "exceptional experience" cost here either: because the consent-form content
itself (CONS-007's prefill mechanism) carries forward the patient's prior answers for
confirm-or-update, the patient experience of re-consenting is a quick review-and-attest
step, not a blank-form redo. The friction the brief worried about doesn't actually
materialise given how CONS-007 is designed. Worth stating this explicitly in the plan
rather than leaving it implicit, since it's a place a reviewer might otherwise flag it as
an open risk that it isn't.

---

## Finding 12: The specialist sign-off list is missing two items

The plan's own outstanding action items (1-10) are a reasonably complete list, but two
more belong on it given the findings above:

1. **PureMed's professional indemnity insurer, specifically on the Whitehouse
   cross-referral model** (Finding 2): does PureMed's own indemnity cover facilitating a
   booking for a regulated activity ultimately delivered by a separate legal entity, and
   does the data flow from PureMed's booking system into Whitehouse's delivery need
   disclosing to either insurer. This is a different question from "does Whitehouse's
   CQC registration cover it" (already on the list) and needs answering by an insurer,
   not verified from a registration lookup.
2. **The prescribing dentist, specifically on whether the online-booking-to-first-toxin-
   prescription pathway (BOOK-001) is compliant** given the tightened remote-prescribing
   position described in Finding 1. This is the single highest-priority sign-off gap in
   the document, because it affects the shape of the primary booking journey being built
   in Stage 1, not a downstream detail.

---

## Verdict

The plan is sound enough to start Stage 1 on the pieces that don't depend on the open
findings above: the data model, the Faces/Acuity migration mechanics, guest-account
infrastructure, and the calendar/diary consolidation can all proceed now, and the overall
component boundary and traceability mechanism are well-constructed and mostly correctly
classified. But two things should be resolved in parallel with the start of Stage 1, not
after it, because they shape rather than merely inform the build: get the prescribing
dentist's explicit sign-off on what the online-to-first-prescription toxin journey is
actually allowed to look like under the tightened remote-prescribing rules (Finding 1),
since that determines the shape of the core booking flow being designed right now, and
get an answer on Whitehouse record-ownership/controllership (Finding 2) before the S7/S9
schema for cross-practice treatments is treated as final, since that's also being built in
Stage 1-2. Neither blocks starting the build; both block calling the current design of
those two specific pieces finished. Everything else in this review (the GDC citation
fix, the licensing-scheme currency update, the RBAC enforcement layer, the defensibility
and WhatsApp-consent gaps, the guest-checkout email verification) is real but genuinely
additive: worth fixing before those specific rows are built, not reasons to hold the
programme.
