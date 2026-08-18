# Buy vs. build spike: UK aesthetic-clinic practice management platforms

15 August 2026 | Owner: Osman Akhtar

Requested before Stage 1 starts, because `booking-engine-plan.md` Section 11's
"why not wrap Cal.com or another scheduler" only evaluated a generic scheduler. It never
priced or evaluated the more relevant comparator: vertical UK aesthetic-clinic
practice-management platforms that already bundle booking, calendar, consent forms,
clinical notes and photo storage. This spike closes that gap before Stage 1 commits.

## Platforms evaluated

Researched by web search, not hands-on trial. Pricing and feature claims are
vendor-marketing-sourced, not verified against a live account; treat as directional.

| Platform | Origin | Positioning | Entry pricing |
|---|---|---|---|
| **Consentz** | UK, built by an aesthetic doctor | Purpose-built for cosmetic/aesthetic practitioners, ISO 27001:2013 | From ~$49/mo |
| **Pabau** | UK | Multi-specialty (aesthetics, wellness, physio) practice management | From ~$62/mo, tiers by user/client count |
| **MERIDIQ** | Sweden, UK-ready | Small/mid aesthetic clinics, GDPR-focused | Affordable, transparent (exact figure not confirmed) |
| **Aesthetic Nurse Software (ANS)** | UK | Solo/nurse-led aesthetic practitioners, 2,700+ users | Not confirmed |
| **Clinicminds** | International | Multi-practitioner, injectables through surgical | Not confirmed |
| **Cliniko** | Australia, UK usage | Generalist allied-health practice management | Predictable flat pricing; **lacks injection plotting and aesthetic-specific consent workflows** per third-party comparison |
| **Aesthetic Record** | US, UK-usable | Aesthetic-specific EMR | $15-19/user/mo + $399 onboarding, **but one user-reported $1,120 fee to export two years of patient data** |
| **Semble** | UK | General private-practice EHR (insurance billing focus) | £50-80/user/mo, priced for insurance-billing practices, not really a fit here |

## Coverage against the requirements register

Checked against `requirements-register.md` (S1-S13). Grouped by what's genuinely
covered off-the-shelf versus what isn't.

### Covered competently, cheaply, by more than one vendor

- Online booking with deposit collection at time of booking (BOOK-001-003, 005)
- Digital consent forms with conditional logic, attached to the appointment and flowing
  into the record (CONS-001-006 territory)
- Before/after photo capture and storage, some with ghost-imaging/markup (PHOTO-001-007
  territory, though PureMed's specific 7-15-shot burst-capture workflow isn't a named
  feature anywhere)
- Practitioner diary/calendar with per-provider scheduling (S6 territory)
- Automated pre/aftercare emails and reminders (S5, S11 territory, though WhatsApp
  specifically, versus email/SMS, is not confirmed as native on any of these)
- Basic audit trail of user actions (Aesthetic Record and MERIDIQ both claim this)

This is a materially wider slice of the register than the "scheduling is 20%, consent
is the other 80% and no scheduler has it" argument in `booking-engine-plan.md` §11
implies. That argument is correct against Cal.com. It does not hold against Consentz,
which is a UK-built, aesthetics-specific platform covering booking, consent, photos and
diary as one product: the actual comparator that should have been priced.

### Not covered by any platform found, and not something a vertical SaaS would plausibly build for one clinic

- **BOOK-007: the prescriber-AND-practitioner hard dependency.** Toxin bookings must
  only be offerable when *both* the treating practitioner and the named prescriber are
  available, not just a single resource. General clinic software handles
  practitioner-OR-room resource locking (confirmed by multiple sources); an AND-gated
  dependency across two specific named individuals for POM administration is a bespoke
  rule no vendor markets.
- **BOOK-008: CQC-scope routing to a different legal entity.** Hyperhidrosis and jaw
  toxin route to Whitehouse Dental Studio's own CQC registration and provider/location
  record, a cross-practice, cross-entity referral. This is UK-regulatory-specific logic
  tied to PureMed and Whitehouse's actual corporate structure. No vertical SaaS is
  built to model two legally separate clinical entities sharing a practitioner and
  routing bookings between them by regulated-activity type.
- **BOOK-004: channel parity.** A staff-executed WhatsApp booking must run the
  identical requirement path (age gate, consent, deposit, screening) as a self-serve
  online booking. Every platform's admin-side manual booking exists specifically to let
  staff *skip* the online flow's gates, which is the opposite of what this row needs.
  This is the same failure mode PureMed has today with Faces (WhatsApp bookings take no
  deposit); switching vendors does not fix it unless the vendor enforces gate parity by
  design, and none reviewed claim to.
- **BOOK-006: graduated no-show enforcement** (discretionary first occurrence,
  enforced prepayment after a configured threshold). Every platform supports a flat
  deposit/no-show policy. A stateful, occurrence-counting graduated policy is not a
  named feature anywhere found.
- **The traceability mechanism itself** (`puremed-clinical-platform-plan.md` Section 4:
  requirement → regulatory source → system component → register row, replayable via
  event log). This is a compliance-engineering artefact specific to this project's
  audit posture, not a commercial software feature. No vendor should be expected to
  have it, and none claim to.

### A risk that switching vendors does not remove

Aesthetic Record's cited **$1,120 fee to export two years of patient data** is the same
risk category driving this entire replacement: PureMed is leaving Faces Consent partly
*because* it has no confirmed self-serve bulk export (`puremed-clinical-platform-plan.md`
§9.5 item 3). Moving to another proprietary vertical SaaS does not structurally fix that
risk, it relocates it to a different vendor. Consentz's API availability is reported
inconsistently across sources (one says no API, another implies third-party
integration exists), and this would need direct vendor confirmation before it could be
trusted as an exit path either.

## What this changes about the build-vs-buy case

**The original stated reason (booking-engine-plan.md §11) needs correcting, not the
conclusion.** "No scheduler has the consent/screening layer" is true of Cal.com and
false of Consentz, Pabau, and similar vertical platforms, which cover a genuinely large
share of Stage 1 and Stage 2's register rows out of the box, cheaply, with less
build time than the current plan assumes.

**The decisive reasons to still build rather than buy are narrower and specific, not
the broad 80/20 split originally argued:**

1. Two of the highest regulatory-stakes rows in the entire register (BOOK-007's
   prescriber-AND dependency, BOOK-008's cross-entity CQC routing) have no off-the-shelf
   equivalent anywhere found. These are exactly the rows the plan's Section 9 posture
   (`full replacement, brought forward`) treats as carrying live regulatory exposure,
   not convenience.
2. ~~Channel-parity (BOOK-004) and graduated no-show enforcement (BOOK-006) are also
   unsupported, and BOOK-004 in particular reproduces PureMed's current failure mode if
   bought rather than built.~~
   **Corrected 16 August 2026: half of this reason has gone.** Nafisa resolved the
   deposit contradiction on 15 August in favour of a universal deposit, no exceptions
   (BOOK-005), which **retires BOOK-006's graduated, occurrence-counting model as
   policy**. A flat deposit and no-show policy is something every platform reviewed here
   supports, so BOOK-006 can no longer be cited as a capability gap. **Channel parity
   (BOOK-004) stands unchanged and is the stronger half anyway**: every platform's
   admin-side manual booking exists specifically to let staff skip the online flow's
   gates, which is the opposite of what PureMed needs and is the exact failure mode it has
   today with Faces.

   The recommendation below does not change. It now rests on three reasons rather than
   four: BOOK-004, the BOOK-007/BOOK-008 pair in reason 1, the export/lock-in risk in
   reason 3, and the commercial multi-tenant argument in reason 4. But this document
   should not be cited as-is, because as written it overstates its own case, which is
   precisely the failure it was created to fix in `booking-engine-plan.md` §11.
3. Buying reintroduces the export/lock-in risk this replacement exists to escape,
   evidenced concretely by Aesthetic Record's reported export fee.
4. The commercial reason from `booking-engine-plan.md` §11 stands independently:
   PureMed is tenant 1 of a multi-tenant booking-engine product MSS is building as a
   case study and sales asset (`project-booking-engine`). Buying vertical SaaS for
   PureMed forfeits that asset; it was not re-examined here because it isn't a
   requirements-coverage question.

**Recommendation: proceed with the custom build for Stage 1, on the corrected
rationale above, not the original one.** Update `booking-engine-plan.md` §11's "why not
wrap a scheduler" argument to name Consentz/Pabau specifically rather than only Cal.com,
since the current text overstates the case and would not survive a specialist reading
it. The register rows a vertical SaaS *would* cover (deposits, consent forms, diary,
basic photo storage) are not a reason to buy instead of build; they are a floor the
custom build needs to clear at minimum, since a bought system would have cleared it
for less money if bespoke rules didn't exist.

## Not resolved by this spike

- No vendor was contacted directly; pricing, API and export claims are third-party or
  marketing-sourced only. If this recommendation is challenged later, get a real demo
  and a written export/API answer from Consentz specifically, since it's the closest
  domain fit found.
- WhatsApp-native integration (rather than SMS/email) was not confirmed as available on
  any platform researched, which matters given `content/config` and the Stage 1 comms
  workstream both assume WhatsApp as PureMed's actual channel.
