# Handoff prompt: validate the PureMed clinical platform plan

Paste this whole prompt into a fresh session (a different agent/model, or the same model
with no prior context) to get an independent check of the thinking below. Point it at
`/Users/osmanakhtar/workspace/main-stage-studio/02_clients/puremed/clinical-platform/`.

---

You are reviewing a first-draft systems plan for a UK aesthetics clinic's clinical
platform. Read these three files in `clinical-platform/` before doing anything
else:

1. `puremed-clinical-platform-plan.md`, the main plan: regulatory landscape, system
   component breakdown, migration plan, phased build plan.
2. `requirements-register.md`, a starter traceability register (requirement → regulatory
   or best-practice source → system component). It is explicitly a partial first pass,
   not full coverage.
3. `technical-design.md` (added 15 August 2026), the system-level architecture: stack,
   data model, migration mechanics, photo-capture approach. Written after the 15 August
   posture change (full Faces Consent replacement brought forward into this phase,
   plan Section 9); if reviewing before that date's context is fully absorbed, read the
   plan's v0.3 changelog at its head first.
3. The original requirements brief is reproduced in full inside
   `puremed-clinical-platform-plan.md`'s framing, but if you want the raw brief text,
   ask the user for it, it is not stored as a separate file in this repo.

For context, also skim (don't need to fully absorb):
- `booking-engine/booking-engine-plan.md`, the existing, more mature plan for the
  patient-facing booking journey specifically. PureMed is "tenant 1" there. This new plan
  treats that document as authoritative for the booking module and defers to it rather
  than re-deciding booking UX.
- `main-stage-studio/02_clients/puremed/CLAUDE.md`, for live operational facts about the
  actual PureMed client relationship (current booking provider is `facesconsent.com`).

## What to actually check

This is not a request to re-read and summarise the plan back. Independently stress-test
it. Specifically:

1. **Regulatory accuracy.** Section 2 of the plan makes claims about UK GDPR, Human
   Medicines Regulations 2012, MHRA Yellow Card, CQC scope, PECR, CAP/BCAP advertising
   rules, the Botulinum Toxin and Cosmetic Fillers (Children) Act 2021, and the pending
   non-surgical cosmetics licensing scheme under the Health and Care Act 2022. None of
   this has had legal review. Check each claim against current guidance (as of your
   knowledge, or web search if you have it) and flag anything that: (a) is stated more
   confidently than the current legal position actually supports, (b) has moved since
   this was written (8 August 2026), or (c) is missing a citation that would let a
   lawyer verify it quickly. Pay particular attention to the GDC-specific claim in
   Section 2.3: that cosmetic, non-dental botulinum toxin/filler work by a GDC-registered
   dentist is permitted under their wider prescribing competence rather than as "the
   practice of dentistry," provided they operate within a declared scope of practice.
   This is stated as a flag needing specialist sign-off, not as settled; check whether
   that hedge is actually strong enough given how load-bearing the point is (it underpins
   BOOK-001, NOTE-004, DIARY-001 in the register).
2. **Gaps in the gaps list.** Section 5 lists twelve additions the author found missing
   from the original brief (under-18 hard-block, DPIA, batch/lot recall, prescriber-of-
   record, chaperone record, practitioner qualification register, service complaints,
   accessibility, DPA register, vulnerable-patient screening, business continuity,
   interpreter support). Does this list miss anything a UK aesthetics clinic system
   would need that a domain-experienced product/compliance reviewer would immediately
   flag? Look specifically for: anything about staff training/competency records tied to
   permitted treatments, anything about multi-site/multi-brand data segregation if
   PureMed expands, anything about insurance claims defence (the whole point of several
   requirements here is defensibility if a patient later disputes what they were told).
3. **Traceability integrity.** For every row in `requirements-register.md`, is the cited
   source actually the right source for that requirement, and is the Requirement Type
   classification (Regulatory / Best-practice / Policy / UX) correct? A requirement
   mis-classified as Regulatory when it's actually Policy overstates what PureMed is
   legally forced to do; the reverse understates it. This classification is the single
   most load-bearing judgement call in the whole document, treat it as such.
4. **Architecture soundness.** Section 3's component breakdown (S1-S14) and the
   cross-cutting principles (append-only clinical record, consent as a lifecycle not a
   boolean, marketing export as a gated workflow, photography never touching the device
   camera roll). Does the component boundary make sense, or would a real build run into
   coupling problems this breakdown doesn't anticipate? Is there a simpler architecture
   that still satisfies every Reg-type requirement?
5. **Migration plan risk.** Section 6. Settled and not worth re-litigating: "Faces
   Connect" was a typo for Faces Consent (`facesconsent.com`), and Acuity Scheduling is
   confirmed dormant (no live bookings) with no live cutover needed, but is not
   valueless: a genuine bulk CSV export exists there (unlike Faces, which has none), and
   was pulled 15 Aug 2026, 588 client records, needing dedup against whatever Faces
   eventually returns. Do check whether the consent re-basing decision (6.4, treat all
   legacy consent as historical-only, never as live) is actually the right call, or
   overly conservative in a way that creates unnecessary re-consent friction the brief's
   own "exceptional experience" goal would object to.
6. **The guest-checkout reversal.** The plan now has PureMed requiring guest checkout
   (account signup offered only after booking), which directly reverses the original
   brief's "guest booking should not be available." Section 3.1 argues this is
   consistent with every consent/clinical-record requirement because only the login
   credential becomes optional, not the underlying S7 record or the consent flow. Test
   that argument specifically: walk through a guest booking a toxin treatment end to end
   and check whether every Reg-type requirement in the register (age gate, DPIA lawful
   basis, consent lifecycle, prescriber assessment) still actually fires the same way it
   would for an account holder, or whether "guest" quietly weakens any of them in
   practice.
7. **The Whitehouse Dental Studio / CQC dependency.** New in this revision: regulated
   treatments route through a sister practice's separate CQC registration (REC-004,
   plan Section 2.4/3.1). Check whether treating this as "verify their registration
   covers it" is sufficient, or whether cross-practice referral of a regulated activity
   creates data-controllership or record-ownership questions between PureMed and
   Whitehouse that the plan hasn't addressed (e.g. whose clinical record system does the
   regulated treatment ultimately live in).
8. **What needs specialist sign-off before this becomes a spec someone builds against.**
   Produce a short, explicit list of items that must go to a healthcare
   regulatory lawyer, PureMed's indemnity insurer, or PureMed's prescribing clinician
   before build, versus what an engineering team can safely proceed on as-is. The plan's
   own "Outstanding action items" section already names three; check whether that list
   is complete.

## Output format

A findings list, most load-bearing first. For each finding: what's wrong or missing,
why it matters (what breaks if it's not fixed), and what you'd change. Do not just
restate the plan's own open-questions list back; go further than what the author already
flagged as uncertain. End with a one-paragraph verdict: is this plan sound enough to
start Stage 1 (booking + calendar + record/consent migration, per plan Section 9) on,
or does something here need resolving first. Note: as of 15 Aug 2026 a data-export
request has been submitted to Faces Consent directly and its response is still pending;
treat that as a known, already-in-motion blocker on the migration-specific portion of
Stage 1, not a fresh finding to raise.
