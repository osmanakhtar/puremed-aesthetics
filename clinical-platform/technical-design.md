# PureMed Clinical Platform: Technical Design

Version 0.4 | 16 August 2026 | Owner: Osman Akhtar (v0.3, 16 August 2026; v0.2, 16 August 2026; v0.1, 15 August 2026)

> **v0.4, 16 August 2026.** Nafisa confirmed, via questionnaire, that Whitehouse currently
> holds the entire clinical record (including notes) for its two CQC-regulated
> treatments, and that PureMed's S7 is intended to become the full record eventually.
> Section 4's `bookings.provider_location_id` and `provider_locations` rows are annotated
> to make explicit that Stage 1 stores only the referral fact and provider/location tag
> for these two treatments, not clinical content, and that full consolidation into S7 is
> a later, not-yet-scheduled stage. No schema change; this is a note, not a new column.
>
> **v0.3, 16 August 2026.** Folds in the C1 schema additions from `crm-and-lifecycle-gap-
> review-2026-08-16.md` Part C1, now that `requirements-register.md` v0.5 and
> `puremed-clinical-platform-plan.md` v0.5 have added S15 (Patient Relationship and
> Retention): a thin `leads` entity, `bookings.source` and `patients.acquisition_source`,
> `services.recall_interval_days` with a derived `patients.next_due_at`, and confirmation
> that `patients.dermis_user_ref` (already reserved in v0.2) is the join point CRM-009
> depends on. Section 4 states which of these are Stage 1 data versus Stage 4 engine.
> Section 8's SAR workflow description is extended to cover `leads`, per CRM-002. No other
> section changes.
>
> **v0.2, 16 August 2026.** Folds in the parts of `peer-review-2026-08-15.md` and
> `crm-and-lifecycle-gap-review-2026-08-16.md` C3 that land on architecture rather than
> requirements. Five changes: `practitioner_competencies` replaces the flat expiry fields
> on `practitioners` (§4, Finding 10); field-level RBAC gets a below-the-application-layer
> guarantee (§8, Finding 6); match and survivorship rules plus a review queue are added to
> the migration sequence (§5.2, CRM review B4); the forward diary at cutover is designed
> (§5.2, CRM review B3); and offline-capable in-room capture becomes an explicit
> constraint on the capture surface (§6, CRM review B6). The architecture decisions in §2
> (one service, not two) and §6.2 (browser `getUserMedia`, spike first) are unchanged.

Companion to `puremed-clinical-platform-plan.md` (regulatory landscape, component model,
build posture, sequencing) and `requirements-register.md` (row-level traceability). This
document is the system-level architecture those two deliberately stay above: what gets
built, in what shape, on what stack, with what data model, and how the Faces Consent
migration actually runs. It has not had engineering peer review or a second-agent
validation pass (see `handoff-validation-prompt.md` for the pattern used on the plan
document; this doc should get the same treatment before build starts).

No compliance or legal review either. Where this document makes a security or
architecture claim that discharges a **Reg**-type register row, that claim still needs
verifying against the row's cited source before build sign-off, same caveat as the plan.

---

## 1. Purpose and scope

Three questions this document answers that the plan and register don't:

1. **What system, concretely, gets built?** Not "S1 through S13," but a stack, a service
   boundary, a hosting decision, and a data model.
2. **How does migration off Faces Consent actually run**, mechanically, given the current
   posture (plan Section 9) has migration in Stage 1, not deferred?
3. **What does the one genuinely hard technical constraint (clinical photo capture that
   never touches the device photo library) mean for build shape and cost?**

Everything here should trace back to a register row or a plan section. Where it doesn't
(a pure implementation choice, e.g. which object storage provider), that's noted as such
rather than dressed up as a requirement.

---

## 2. Relationship to `booking-engine`

`booking-engine-plan.md` already made and justified the core architecture decision for
the booking, scheduling and payment orchestration slice: **a single Node/TypeScript
service (Fastify) with PostgreSQL, an embeddable front-end widget, Stripe for payments,
and a calendar-sync job runner.** PureMed is tenant 1 there. `puremed-clinical-platform-
plan.md` Section 3 already defers to that document for the booking module rather than
re-deciding it, and this document does the same.

**What this document adds is everything `booking-engine` explicitly does not attempt**:
the patient clinical record (S7), consultation and treatment planning (S8), clinical
treatment notes including the toxin prescribing record (S9), clinical photography (S10),
aftercare and complications (S11), and the migration of ~475 existing patient records and
their consent history out of Faces Consent (S13). Under the 10 August posture these sat
in a separate, undecided-timing project. Under the current posture (plan Section 9) they
are Stage 1-2 work, on the same timeline as booking itself, which is the reason this
document treats them as one system rather than two integrated ones.

**Decision: one service, not two integrated services.** `booking-engine`'s own Section 11
rejected wrapping a third-party scheduler because "the scheduling core is roughly 20% of
the work... the consent, screening and evidence layer is the other 80%." That argument
applies with more force here: splitting booking (Node/Fastify/Postgres, already designed)
from the clinical record (this document) into two services synchronised over an API would
recreate the exact parallel-store risk the plan's Section 9.1 and 9.6 argue against, in a
new form. **The clinical record modules (S7-S11) extend the same Postgres schema and the
same Fastify service that `booking-engine` already designs**, as additional route groups
and tables, not a second deployable.

---

## 3. System architecture

```
┌──────────────────────────────────────────────────────────────────┐
│  puremed.uk (Astro static, Cloudways)                            │
│  embedded booking + patient portal widget                        │
└────────────────────────┬────────────────────────────────────────┘
                          │ HTTPS, tenant-scoped API
┌─────────────────────────▼─────────────────────────────────────────┐
│  PureMed platform service (Node + TypeScript + Fastify)          │
│                                                                   │
│  booking-engine modules (per booking-engine-plan.md §11):        │
│    availability engine · rules engine · journey state machine    │
│    document renderer + signature capture · payment orchestration │
│                                                                   │
│  clinical-platform modules (this document):                      │
│    patient record (S7) · consultation/planning (S8)              │
│    clinical notes + prescribing record (S9) · photo pipeline (S10)│
│    aftercare/complications (S11) · migration jobs (S13)          │
│                                                                   │
│  shared: admin API + admin UI · RBAC/audit (S12)                 │
│  job runner: calendar sync · WhatsApp delivery · reminders       │
│              reconciliation · migration ingestion                │
└──┬──────────┬───────────┬────────────┬─────────────┬─────────────┘
   │          │           │            │             │
┌──▼─────┐ ┌──▼────────┐ ┌▼──────────┐ ┌▼───────────┐ ┌▼───────────┐
│Postgres│ │Object     │ │Google Cal/│ │Stripe      │ │WhatsApp    │
│        │ │storage    │ │MS Graph   │ │            │ │Business API│
│patients│ │encrypted: │ │           │ │payments    │ │            │
│bookings│ │clinical   │ │           │ │(tokenising,│ │bookings,   │
│consent │ │photos,    │ │           │ │ PCI DSS)   │ │aftercare,  │
│notes   │ │signed PDFs│ │           │ │            │ │treatment   │
│events  │ │           │ │           │ │            │ │plans       │
└────────┘ └───────────┘ └───────────┘ └────────────┘ └────────────┘
```

**Native/PWA capture surface** (patient photos, S10) sits outside this diagram as its own
client, described in Section 6, because it is a distinct build artefact from the web
widget, not another backend service.

**Hosting: Cloudways or a comparable managed host, UK region**, consistent with
`booking-engine-plan.md` Section 11's "why not build on the Pi" reasoning: Stage
(`mss-review.duckdns.org`) is fine for static client review, not for special-category
health data, payment flows and uptime obligations. This platform is operationally
separate from Stage and from the `puremed.uk` Astro site's own hosting, though it can sit
on the same Cloudways account.

---

## 4. Data model

Postgres, one schema, tenant-scoped tables (reusing `booking-engine`'s tenant-isolation
pattern via row-level security, even though PureMed is presently the only clinical
platform tenant, since the multi-tenant booking-engine showcase already establishes the
pattern and there is no cost to keeping the clinical tables consistent with it).

**Core entities**, deliberately named to match the register component IDs so a schema
review can walk the register row by row:

| Table | Register component | Notes |
|---|---|---|
| `patients` | S1, S7 | One row per patient. `account_id` nullable (guest checkout, ACCT-001). `legacy_faces_id` for migration traceability, never deleted even after full cutover |
| `bookings` | S2 (booking-engine) | Extended with `provider_location_id` (REC-004: which legal provider/CQC location delivered it, e.g. Whitehouse) |
| `consents` | S4 | One row per consent instance, not a boolean on `patients`: `treatment_id`, `form_version_id`, `signed_at`, `attested_accurate` (CONS-007), `status`. Never updated in place; a reconfirmation is a new row |
| `consent_form_versions` | S4 | Locked, versioned form content (CONS-003). Migrated Faces forms import here as historical, `is_live = false` (MIG-001) |
| `clinical_photos` | S10 | `patient_id`, `taken_at`, `location` (PHOTO-006, TimeMark-equivalent metadata), `upload_confirmed_at` (PHOTO-007), `marketing_consent_id` nullable, `object_storage_key` |
| `treatment_notes` | S9 | `treating_practitioner_id`, `prescriber_id` (NOTE-004, distinct fields, nullable prescriber where not applicable), `batch_lot` (NOTE-007, `NOT NULL` for POM treatments), locked once signed (NOTE-003), corrections are new linked rows |
| `prescribing_records` | S9 | The toxin form specifically (NOTE-005): `units`, `site`, `batch_lot`, `clinician_signature_id`, `prescriber_signature_id`, `pre_treatment_contact_completed_at` (CONS-009) |
| `treatment_plans` | S8, PLAN-004 | Generated artefact: `photo_id`, `findings`, `sequence` (array of treatment refs), `prices`, `delivered_via` |
| `practitioners` | S6 | Identity, GDC registration number, `declared_competence_basis` (renamed from `scope_of_practice` in v0.2, peer review Finding 4: GDC removed cosmetic injectables from its Scope of Practice Guidance in Nov 2025, so the field cannot claim a GDC-defined boundary). Expiry fields moved to `practitioner_competencies` below |
| `practitioner_competencies` | S6, DIARY-001/006 | **New in v0.2, peer review Finding 10.** Join table: `practitioner_id` × `treatment_type_id` × `basis` (training/qualification evidence) × `indemnity_ref` × `expires_at`. Replaces one expiry per practitioner, which could not express "trained and insured for toxin but not for this filler technique". Also matches the Amber-tier licensing scheme's per-procedure named-oversight shape (plan 2.9). The booking gate reads this table, not `practitioners` |
| `dermis_links` or `patients.dermis_user_ref` | (boundary) | **Reserved, unpopulated.** Same pattern as `payments.channel`'s `klarna_dermis` slot: costs one nullable column now, and is the only thing standing between "two customer masters with no join key" and a recoverable position once A5/A6 land. MIG-008, CRM review A5 |
| `provider_locations` | S7, REC-004 | PureMed Aesthetics and Whitehouse Dental Studio as distinct rows, each with its own CQC registration reference where applicable. **v0.4:** Whitehouse currently holds the full clinical record for its two treatments; PureMed's tables carry only the referral fact and this provider/location tag (Stage 1), not clinical content. Full record consolidation into S7 is confirmed as a future direction, not scheduled here |
| `payments` | S3 (booking-engine) | Extended with `channel` enum (`platform`, `sumup_link`, `dojo`, `bank_transfer`, `gocardless`, `klarna_dermis`) so out-of-platform payments (PAY-005) are recordable, not just platform-native ones |
| `audit_log` | S12 | Append-only. Every access to `clinical_photos`, `treatment_notes`, `prescribing_records` and `consents` is logged (PHOTO-004, SEC-007) |
| `migration_jobs` | S13 | Tracks the Faces/Acuity ingestion run: source, row counts, reconciliation status, per Section 5 below |
| `leads` | S15 | **New in v0.3.** `contact_details`, `source`, `treatment_interest`, `status`, `outcome`, nullable `patient_id` (set on conversion). Deliberately thin: no pipeline, no deal stages. CRM-001 |
| `bookings.source` / `patients.acquisition_source` | S15 | **New in v0.3.** Columns on the existing `bookings` and `patients` tables, plus `campaign`/first-touch where the entry point supplies it. CRM-003 |
| `services.recall_interval_days` / `patients.next_due_at` | S15 | **New in v0.3.** `recall_interval_days` on `services`; `next_due_at` on `patients`, derived from the most recent `treatment_notes` row for that service. CRM-004 |
| `patients.dermis_user_ref` | S15, (boundary) | **Confirmed, already reserved in v0.2.** See the row above in this table (`dermis_links` / `patients.dermis_user_ref`); CRM-009 depends on this column being populated once A5/A6 land |

**S15 schema additions: which are Stage 1 data versus Stage 4 engine, and why the data
cannot wait.** *New in v0.3.* `leads`, `bookings.source`/`patients.acquisition_source` and
`services.recall_interval_days`/`patients.next_due_at` are all Stage 1, even though the
CRM-004/CRM-005/CRM-006 *engines* that act on them (recall sends, template-level
transactional/marketing classification, treatment-plan follow-up) are Stage 4. The reason
is the same one that puts consent migration in Stage 1 rather than Stage 4: every record
migrated in from Faces and Acuity needs a last-treatment baseline set **at migration
time**, because that baseline cannot be reconstructed afterwards from a system that no
longer holds it. A patient migrated with no `next_due_at` and no `acquisition_source`
stays permanently unattributable and un-recallable, the same failure mode
`crm-and-lifecycle-gap-review-2026-08-16.md` A2 and A3 describe for a field skipped now
and added later. `leads` is Stage 1 for the same reason MIG-002/CRM-002 need it to exist
before any SAR can be answered against the lead population, not because a lead-management
UI is wanted this early.

**Append-only enforcement** (plan Section 3.1, "Append-only clinical record") is a
database-level constraint, not application discipline: `treatment_notes`, `consents` and
`prescribing_records` get `UPDATE` revoked at the role level for the application's normal
runtime credential, with corrections modelled as new rows carrying a `supersedes_id`
foreign key back to the original. This makes NOTE-003 and CONS-006 structurally
impossible to violate by a future code change, not merely policy.

---

## 5. Migration mechanics

*Referenced from `puremed-clinical-platform-plan.md` Sections 6 and 9.4. This is now
Stage 1 work, not a later-phase concern, per the 15 August posture.*

### 5.1 What's actually known versus what's a placeholder

**Resolved, 15 Aug 2026.** Admin access to Faces was used directly to check every
plausible location for a bulk export function: Settings (all ten sub-pages), the
Clients list's ⋮ menu (import-only: "Download CSV template" / "Upload CSV", no export),
Marketing → Emails (an in-platform campaign sender, not a data export), Business
insights (a gamification leaderboard), and an individual client profile (no
download/export control on the record). **No self-serve bulk export exists in the
Faces admin UI**, at any level a business-tier account can reach. This also puts a
question mark over the 10 Aug as-is-doc §7.2 claim that Nafisa "exports patient email
addresses from Faces" for MailChimp; no such export button was found, so either it's
support-assisted, plan-gated, or she was describing something else. Worth confirming
with her directly rather than treating that transcript line as settled.

The **manual/assisted extraction** path below is therefore the one in play, not a
contingency:

| Path | What it means | Status |
|---|---|---|
| ~~Bulk export exists (CSV/API pull)~~ | ~~Standard ETL: pull, map, load, reconcile~~ | **Ruled out, 15 Aug**: no such function found anywhere in the admin UI |
| **No bulk export, manual/assisted extraction** | A data request to Faces' support desk under the DPA (MIG-002) | **In progress.** Nafisa has already submitted the data request to Faces directly; migration mechanics below wait on their response |

Either way, the migration is a **file-based batch load, not a live dual-write sync**.
`booking-engine-plan.md`'s equivalent reasoning (6.5, "booking volume is low enough that
a live dual-write layer is unlikely to be worth the complexity") applies directly: 475
records is two orders of magnitude below where a live sync would be justified (MIG-007).

### 5.2 Sequence

1. **Discovery** (plan 6.2): admin access to Faces and Acuity; data dictionary; overlap
   analysis between the two sources; identify what in Faces counts as a signed consent
   versus a booking-form answer.
2. **Extraction**: whichever path 5.1 resolves to. Output: a versioned, timestamped
   export snapshot, stored as the immutable input to ingestion, not queried live against
   Faces during the load.
3. **Mapping and load** into a **staging schema**, not directly into the live tables in
   Section 4. This is the one addition this document makes beyond the plan's Section
   6.3 entity-mapping table: staging exists so reconciliation (step 4) happens against a
   loaded copy, not against production data that patients or staff might already be
   touching mid-migration.
4. **Match and merge across the two sources.** *New step in v0.2 (CRM review B4). v0.1
   went straight from load to reconciliation, which silently assumed the two sources
   could be loaded side by side without deciding who is who.* 588 Acuity records against
   roughly 475 in Faces, with unknown overlap and no shared key.

   - **Match key, in priority order**: normalised email, then normalised phone, then
     surname plus date of birth. Anything matching on two or more is an auto-merge
     candidate; anything matching on exactly one goes to review.
   - **Survivorship**: Faces wins on contact details and demographics, because it is the
     live system and Acuity's records are a median 1,365 days stale. Acuity wins on
     nothing except its own notes, which are additive (MIG-005) and never overwrite a
     Faces field. Every superseded value is retained on the record, not discarded, so a
     wrong survivorship call is recoverable.
   - **A human-review queue for every non-exact match**, no exceptions. At a few hundred
     candidates this is a morning's work and it is the only defence against the two
     failure modes that matter: merging two different people produces a record carrying
     someone else's medical history, and splitting one person produces two half-histories,
     one of which is missing an allergy. Neither is detectable by a count reconciliation.
   - Merge decisions are written to `migration_jobs` with the actor and the rule that
     fired, so the merge is auditable after the fact.

5. **Reconciliation**: record counts, spot-check sample against source (plan 6.5, step 3),
   and specifically verify the consent re-basing rule (plan 6.4): every migrated consent
   record lands with `is_live = false`, no exceptions, checked as an automated assertion
   over the staged data before promotion, not a manual spot-check alone.
6. **Promotion**: staged data moves into the live schema in a single transaction per
   patient batch, not row-by-row, so a failure partway through a batch cannot land a
   patient in a half-migrated state.
7. **Forward diary re-entry.** *New step in v0.2 (plan 6.6, CRM review B3).* Plan 6.3
   migrates booking *history* as a read-only view and explicitly does not re-enter it
   into the live diary. That leaves the appointments already booked into the future on
   cutover day sitting in a system nobody writes to, while the calendar of record moves
   elsewhere: the exact failure DIARY-004 exists to prevent, at the worst possible
   moment. Re-enter the forward diary by hand as the last step before the shadow period
   opens, then reconcile immediately against the Faces diary. Volume makes this the right
   call (two working days a week, bounded by the maximum advance window) and every
   alternative is worse: a two-calendar week mid-migration, a dual-write layer MIG-007's
   volume argument already rejects, or losing appointments patients have been confirmed
   for. Confirm the actual forward-booked count with Nafisa first; if it is materially
   larger than expected, revisit rather than assume. Any booking appearing in Faces after
   this reconciliation is an error the shadow period exists to catch.
8. **Shadow period**: Faces Consent stays live and readable (plan 6.5, step 2; plan 9.6)
   for lookup only, no new writes accepted into it, while the new system takes new
   bookings. This is the mechanism that makes plan 9.6's risk-management argument
   ("a bad cutover costs the working parts of Faces") actually true in practice rather
   than asserted: staff always have a fallback read path during the period, and nothing
   is deleted from Faces until decommissioning.
9. **Decommission**: remove live Acuity links (plan 6.5, step 4) and Faces booking-page
   references from `puremed.uk`, coordinated with the `booking-engine-plan.md` CTA
   migration item. Retain the raw export from step 2 for the 11-year retention period
   (REC-002) independent of whether Faces itself is decommissioned.

### 5.3 What's still genuinely open

How long the shadow period (step 8) runs, and what specifically closes it, is a
risk-tolerance decision for Nafisa, not something this document can size in the
abstract, per plan 9.4 item 2. A sensible default to propose once volumes are confirmed:
close it on the first full month where every booking in the new system reconciles
cleanly against Faces with zero discrepancies, not a fixed calendar date.

---

## 6. Photo capture architecture

*The as-is discovery record's design-implications section (superseded content, see
`../discovery/2026-08-10-as-is-operating-model.md` Section 12.4) called this "the one
requirement in the whole set that dictates a platform choice." This section is where
that gets resolved concretely.*

### 6.1 The constraint

PHOTO-001 (register): capture must never reach the device's normal photo library. PHOTO-
005: bulk multi-select, single-action upload of a full patient set. PHOTO-006: TimeMark-
equivalent time/location metadata. PHOTO-007: deletion from the device only after
confirmed upload.

A plain HTML `<input type="file">` upload form cannot satisfy PHOTO-001: on both iOS and
Android, triggering the native camera through a standard file-picker writes the photo to
the OS camera roll first, before the browser ever sees it. That single fact is what
rules out the cheapest option.

### 6.2 Two ways to actually satisfy it, and the recommendation

| Option | How it avoids the camera roll | Cost |
|---|---|---|
| **A. Browser `getUserMedia` capture (PWA)** | Streams the camera directly into a `<canvas>`/`MediaStream` inside the web app; the resulting frame is captured as a Blob in memory and uploaded, without ever going through the OS camera app or its save path | Lower build cost, ships as part of the existing web platform, no app-store distribution. Camera UI (framing guides, burst capture for 7-15 shots) has to be hand-built in-browser, and iOS Safari's `getUserMedia` support has had rough edges historically, worth a spike before committing |
| **B. Native or Capacitor-wrapped app** | Full native camera API access, no ambiguity about camera-roll behaviour | Higher build and maintenance cost, app-store review and distribution overhead, for a single practitioner's device |

**Recommendation: Option A, browser-based capture, with a short technical spike before
Stage 2 starts** to confirm `getUserMedia` behaves correctly for burst/multi-shot capture
on Nafisa's actual device (as-is Section 5 doesn't record the device model; worth
confirming). Nafisa is a single user on a known device, not a fleet of staff phones, which
significantly de-risks the "does this work reliably in practice" question a native app
would otherwise justify. If the spike fails, Option B is the fallback, not a redesign.

### 6.2a The constraint v0.1 missed: it has to work with no signal

*Added in v0.2 (plan gap 5.15, CRM review B6).*

Both Stage 2 surfaces live on a device in a treatment room: bulk photo capture, and the
toxin prescribing record completed at the point of treatment with two signatures. 6.3
below sequences capture, batch upload and deletion assuming connectivity throughout,
which is the wrong assumption to build on given what this whole plan's acceptance bar is.

Paper never fails. A prescribing record that cannot be completed because the signal
dropped, with the prescriber standing there waiting to sign, routes straight back to the
paper form, and the entire point of NOTE-005 is that the paper form is the one document
that leaves the system. The as-is record contains two proven abandonments of
technically-correct processes that were slower than the shortcut; one failed treatment is
enough to re-establish the habit.

**Requirement on the capture surface, both options in 6.2:**

- Capture, form completion and signature capture all complete **locally**, with no
  network call on the critical path.
- The record is persisted to local storage immediately and marked `pending_sync`.
- Sync happens opportunistically on reconnection, with an unmissable indicator of
  anything still pending and how old it is.
- PHOTO-007's deletion-after-confirmed-upload rule is unchanged and remains correct:
  local copies clear only once the platform confirms a durable write.

This is a point in Option A's favour that 6.2 did not weigh: a PWA with a service worker
and IndexedDB handles offline queueing as a well-trodden pattern, and the spike should
now cover offline capture and deferred sync alongside burst capture, not just
`getUserMedia`.

### 6.3 Upload and deletion sequencing

Bulk upload (PHOTO-005) queues all captured frames client-side, uploads as a batch with
per-image progress, and only after the platform confirms every image in the batch has
been durably written to object storage does the client offer (or automatically trigger,
per Nafisa's stated preference, as-is 5.4) deletion of the in-app captured frames. Since
Option A never wrote to the camera roll in the first place, "deletion from the device"
here means clearing the app's own temporary in-memory/cache copy, not a camera-roll
delete permission, which is itself a simplification PHOTO-007's Faces-based alternative
(delete from a photo library the OS controls) would not have had.

---

## 7. Integration surfaces

### 7.1 WhatsApp Business API

COMM-004 makes WhatsApp a first-class channel, not a notification fallback. This needs
the **WhatsApp Business Platform (Cloud API)**, not a personal WhatsApp Web automation:
booking confirmations, deposit payment links, aftercare and treatment-plan delivery all
need template-message approval and delivery-status webhooks (COMM-002, COMM-006), which
only the official Business API provides reliably at this volume and with this compliance
weight. Message templates need submission and approval through Meta before Stage 1 build
completes, since approval lead time is outside MSS's control and should not sit on the
critical path discovery.

### 7.2 Payments

Stripe (per `booking-engine-plan.md` Section 11) as the PCI DSS tokenising provider
(PAY-001), which also yields Apple Pay and Google Pay (PAY-006) at near-zero marginal
cost. The `payments.channel` field (Section 4) records the five other rails PureMed
already uses (SumUp, Dojo, bank transfer, GoCardless, Klarna) without the platform
processing them, since PAY-005 is explicitly a recording requirement, not a mandate to
consolidate every payment rail onto Stripe.

### 7.3 Calendar

Google Calendar as the external sync target (matching what Nafisa already uses), via
Google Calendar API, one authoritative writer (DIARY-004). The job runner owns this
write; no other process, including any dermis.ai integration, is granted write access
once cutover completes. MS Graph and ICS remain available per `booking-engine-plan.md`'s
existing multi-provider design, unused for PureMed specifically unless that changes.

### 7.4 dermis.ai boundary

No integration is designed here, deliberately: PAY-009 and MIG-008 keep memberships,
loyalty points and Klarna checkout out of scope until the dermis.ai app architecture is
known (blocked on actions A5, A6). If and when that boundary is drawn, it is an addition
to this document, not a retrofit of the schema in Section 4, since `payments.channel`
already has a `klarna_dermis` slot reserved for recording (not processing) that activity.

---

## 8. Security and compliance architecture

Maps directly to S12 register rows; listed here as build-shape decisions rather than
requirements restated:

- **Encryption** (SEC-002): TLS in transit; Postgres and object storage encrypted at
  rest via the hosting provider's managed encryption, not application-level crypto.
- **RBAC** (SEC-003, REC-001): role and field-level permission checks live in the Fastify
  service layer, not the client; reception-role tokens never receive the full clinical
  fields in an API response, not merely a UI that hides them.
  **Strengthened in v0.2 (peer review Finding 6).** v0.1 gave this a service-layer-only
  guarantee while deliberately pushing append-only enforcement down to the database role
  level so it would be "structurally impossible to violate by a future code change, not
  merely policy". REC-001 is a Regulatory row in the same weight class and deserves the
  same treatment: application-layer-only checks regress quietly, because every new
  report, export or debug endpoint has to remember to re-apply the filter. Back it with
  Postgres column-level policies or role-scoped views wherever practical. **Non-negotiable
  minimum where that isn't practical:** a CI test suite asserting that no reception-scoped
  query can return the restricted fields, so a regression fails the build rather than
  surfacing in production.
- **Audit logging** (PHOTO-004, SEC-007): the `audit_log` table (Section 4) is
  application-write-only, append-only at the database role level, same enforcement
  pattern as the clinical tables in Section 4.
- **DPA register** (SEC-005, SEC-008): not a system component, a maintained document
  (already flagged as "do this now, independent of any build" in the register); this
  design doc doesn't model it as a table, it's operational, not architectural.
- **SAR workflow** (SEC-006): an admin-role export function over the patient's full
  record set (all tables in Section 4 keyed by `patient_id`), assembled on request, not
  pre-built exports sitting at rest. **Extended in v0.3 (CRM-002) to cover `leads`, not
  only `patients`.** A subject access request can come from someone who used the skin
  scanner, was contacted by the voice agent, and never booked, and SEC-008 already names
  PureMed as controller for that population. The same admin-role export function runs
  against a `lead_id` as well as a `patient_id`; a lead that later converts is resolvable
  through the `leads.patient_id` link so its pre-conversion and post-conversion history
  are returned as one set.
- **LLM assistant boundary** (SEC-011): explicitly, no general-purpose LLM (the ChatGPT
  inbox automation being retired per DIARY-004) is granted any credential or data access
  to this platform's database, storage or APIs, at any point, including for
  administrative convenience.

---

## 9. Open technical decisions

Things this document deliberately leaves open, either because they're genuinely
downstream of decisions in the plan, or because they're implementation choices with no
single right answer yet worth debating in the abstract:

1. **Object storage provider** (S3-compatible: AWS S3, Cloudflare R2, or Cloudways'
   equivalent). No requirement forces a specific vendor; pick on cost and UK-region
   availability (SEC-004) when build starts.
2. **The `getUserMedia` spike outcome** (Section 6.2) determines whether Stage 2's photo
   pipeline is a web-platform feature or a native build, which has a real cost and
   timeline consequence worth resolving before Stage 2 is quoted, not during it.
   **Scope widened in v0.2:** the spike must also cover **offline capture and deferred
   sync** (Section 6.2a), not only burst `getUserMedia` behaviour. Offline is the harder
   of the two requirements to retrofit and the one whose failure sends the workflow back
   to paper.
3. **Shadow-period exit criteria** (Section 5.3), pending Nafisa's risk tolerance once
   migration volumes and Faces export capability are confirmed.
4. **Practitioner qualification/indemnity data source** (DIARY-006): the `practitioners`
   table's `qualification_expiry`/`indemnity_expiry` fields are designed, but populating
   them is blocked on plan decision-gate item 4 (where this is tracked today, if
   anywhere).

---

## 10. Build sequencing

This document does not re-state sequencing; `puremed-clinical-platform-plan.md` Section 9
is authoritative. Cross-reference for build planning: Section 4's tables map cleanly onto
Stage 1 (`patients`, `consents`, `consent_form_versions`, `provider_locations`,
`migration_jobs`, plus `bookings`/`payments`/`practitioners` from `booking-engine`) and
Stage 2 (`clinical_photos`, `treatment_notes`, `prescribing_records`), with `payments`
gaining its deposit-enforcement behaviour in Stage 3 and `treatment_plans` arriving in
Stage 4 alongside the WhatsApp comms integration (Section 7.1).
