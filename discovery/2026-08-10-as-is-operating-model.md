---
project: main-stage-studio
status: done
next: "None. Captured discovery artefact; feeds puremed-systems-proposal.md"
blocked_on: ""
owner: osman
updated: 2026-08-10
---

# PureMed: As-Is Operating Model

*Discovery artefact. Captured 10 August 2026 from the Nafisa discovery call, against the
question set in `2026-08-10-nafisa-discovery-call-prep.md`. Source transcript:
`~/Downloads/puremed discovery call.txt`.*

*This is the as-is only. It records what Nafisa said happens today, not what should
happen. Target-state design lives in `clinical-platform/puremed-clinical-platform-plan.md`
and `booking-engine/booking-engine-plan.md`. Design implications are quarantined in
Section 12 and are Osman's reading, not the client's statements.*

---

## 0. Read this first: source reliability

The transcript is a rough auto-transcription with heavy mis-hearing. Product and
person names arrive mangled ("cases" for Faces Consent, "clone/clanor" for Klarna,
"some up" for SumUp, "time stamp" for TimeMark). Several of Nafisa's answers are
missing entirely because only the question survived the transcription.

**The recording is truncated**, ending mid-sentence during the dermis.ai discussion
("...my barrier for injury for something like that is the fact that it's, I'm giving out
my data. There was no."). **Confirmed by Osman, 10 August 2026: nothing of substance was
lost.** The dermis.ai Klarna and membership journey was the last item of value covered, and
it is captured in Sections 3.3 and 9. **Treat this document as a complete record of the
call.**

Confidence is marked throughout:

- **[Confirmed]** stated clearly and unambiguously in the transcript
- **[Inferred]** the meaning is clear but the words are mangled; reconstruction stated
- **[Unanswered]** asked but the answer did not survive, or was never given
- **[Not covered]** in the prep doc, never reached on the call

Nothing marked Inferred should be built against without a one-line confirmation from
Nafisa. Section 11 collects everything needing that confirmation.

---

## 1. The operating model in one paragraph

PureMed runs on **Faces Consent as the system of record** and **WhatsApp as the actual
operating surface**. Faces holds the diary, the patient records, the treatment-specific
consent forms, the generic medical form and the automated confirmation and aftercare
emails. Almost everything that requires a human runs through WhatsApp instead: inbound
booking requests, deposit payment links, aftercare that patients actually read, and
personalised treatment plans. The gap between those two surfaces is where all the
friction sits. There is no receptionist, no admin, and no second system: one person
absorbs the whole operational load.

---

## 2. The booking journey

### 2.1 Two entry routes

**Route A, direct message.** [Confirmed] A patient WhatsApps or emails asking to book.
Nafisa offers roughly two slot options, they pick one, and **Nafisa executes the booking
herself on the patient's behalf**. This route is predominantly existing patients.

**Route B, online.** [Confirmed] The patient books themselves through Faces Consent at
`facesconsent.com/bookings/puremedaesthetics`.

[Confirmed, raised separately from the call itself] **The Faces Consent booking flow is
clunky.** A patient cannot land directly on the treatment they want; they must scroll the full
treatment list to find and select it, and the journey carries more clicks than it needs to.
This was not covered in the discovery call because it had already been discussed prior to it.
It is material to the proposal because the **replacement booking system**, not Faces itself,
is set to become the primary booking entry point, on the basis that it is also the system that
will carry deposit payment once deposits are enforced (2.5). This flow's friction is therefore
a defect the replacement needs to design out, not a thing the new system should inherit
unchanged.

The two routes behave differently, and that difference is a live problem:

| | Route A (Nafisa books) | Route B (patient books online) |
|---|---|---|
| Deposit taken | **No** [Confirmed] | Handled by Faces |
| Consent form issued | Yes, automatically [Confirmed] | Yes, automatically [Confirmed] |
| Who does the work | Nafisa, manually | The patient |

### 2.2 What happens once a booking exists

[Confirmed] Adding the appointment to the Faces diary automatically fires an email to
the patient carrying the appointment confirmation, the **treatment-specific consent
form** and the **generic medical form**. Completed forms save back onto the patient's
record in Faces.

### 2.3 Forms

- [Confirmed] **Consent forms are treatment-specific.** Booking anti-wrinkle sends the
  toxin consent form; booking filler sends a different one. They are all different.
- [Confirmed] **The medical form is generic**, one version for everyone.
- [Confirmed] Faces ships a library of consent form templates covering more treatments
  than PureMed offers. The subset PureMed actually uses is under
  **Settings, then Forms, then "My forms"** (reached via the initials menu, top right).
  That subset already matches the treatments Nafisa delivers.
- [Confirmed] **Consent is refreshed per appointment**, every time. There is no separate
  refresh policy because reconfirmation is unconditional.
- [Confirmed] **Medical history persists between visits.** If a patient already has a
  medical form on file it stays valid, and they update it only if something changed.
- [Confirmed] **Faces duplicates medical questions.** The toxin consent form carries
  medical questions and a separate generic medical form is sent alongside it. Nafisa
  cannot change this.
- [Confirmed] **Nafisa cannot customise the forms as much as she wants.** A new
  requirement to phone toxin patients before their appointment cannot be added to the
  form, so it has to be added manually.

### 2.4 What Nafisa wants forms to do

[Confirmed] She wants reissued forms to come back **prefilled with the data already
held**, with the patient signing to confirm it is true and accurate each time. That
applies to both the medical form and the consent form. Her reason for keeping it as a
signed form rather than folding it into the patient record: **"I want them to sign it to
say that it's true and accurate."**

[Confirmed] She has no objection to it being fully online and digital rather than a
document, provided the signature and the per-visit attestation survive.

### 2.5 Deposits

[Confirmed] Deposits are currently **inconsistent**. Route A bookings take none.

[Confirmed] **Nafisa's stated position: everyone should pay a deposit, across the
board.** Her reasoning, in her words, is that uniformity is the point: "it's just a
standard procedure", and taking it from everybody removes the awkwardness of asking
selectively.

[Confirmed] The specific problem she is trying to solve is social, not financial. She
has patients she has known for years who cancel on the day, and she cannot bring herself
to charge them. She explicitly wants the **system to be the one saying no**: her framing
was that she needs to be able to say "I can't change it, pay me before I can book you
again."

Osman's live counterpoint, recorded because it is unresolved: enforcing this uniformly
carries relationship and reputational risk with long-standing patients, and losing repeat
business may cost more than the forfeited deposit. Nafisa's response was that enforcement
should be **discretionary for first offences and hard for repeat offenders**, which is
in tension with the "everyone, always" position above. **This needs a single decision.**

### 2.6 New patient booking fee

[Confirmed] A new patient who has never been seen before and WhatsApps for a
consultation is charged a **non-refundable £25 booking fee**. Nafisa sends a **SumUp
payment link over WhatsApp** with the non-refundable terms stated in the message text.
[Inferred] The appointment is not held until that fee is paid.

### 2.7 No-shows and late cancellation

[Confirmed] There is **no enforcement mechanism today**. It is entirely discretionary
and entirely manual. The 48-hour window recorded in the existing plan documents is a
policy statement, not something the system applies.

[Confirmed] Repeat offenders exist and are a known, named problem: "there's always a few
ones that are the same people, repeat offenders. Something just happens to happen every
single time."

### 2.8 Waitlist

[Confirmed] **None today.** Nafisa's reason: "I'm not busy enough. If I do get busy
enough, then yeah, there should be a waiting list."

[Confirmed] Two scenarios were discussed and both were accepted as real:

1. **Same-day cancellation backfill.** The dentist model: a patient asks to be called if
   anything opens up on a specific day.
2. **Partial-slot fit.** The 12:00 appointment cancels, and someone wanted 12:30. The
   freed time does not match the wanted time exactly, and today nothing bridges that.

Treat waitlist as a confirmed future requirement with no current process to migrate.

---

## 3. Payments

### 3.1 Channels in use today

| Channel | Used for | Notes |
|---|---|---|
| Faces Consent, integrated card | Online bookings | [Inferred] Nafisa believes this runs on Stripe. **Unverified**, see 11.4 |
| **Stripe** | Already held | [Confirmed] account exists, free to set up, per-transaction cost |
| **SumUp** | Deposit and booking-fee payment links over WhatsApp | [Confirmed] higher rate than Dojo, but "their link works better", so it is the one she uses |
| **Dojo** | In-clinic card machine | [Confirmed] lower transaction rate |
| **Bank transfer** | Regulars, and generally anything over £500 | [Confirmed] "it's cheaper for me" |
| **GoCardless** | Direct debit, patients spreading treatment cost monthly | [Confirmed] |
| **Klarna** | Memberships, via the dermis.ai app | [Confirmed] see 3.3 |

[Confirmed] **Apple Pay and Google Pay are an explicit want.** Her words on Apple Pay:
"if you can do Apple Pay, that will be sick." Neither exists today outside whatever the
dermis.ai app provides.

### 3.2 Refunds

[Confirmed] The published terms say **no refunds**, on the grounds that outcomes on a
treatment-based service cannot be guaranteed. This wording appears in the consent forms,
the website copy and the terms and conditions, and patients agree to it.

[Confirmed] Refunds are **very rare**. When one is issued it is processed as a reversal
on whichever platform originally took the payment. There is no approval step, no log,
and no reconciliation process, because Nafisa is the only person who could issue one.

### 3.3 Memberships, Klarna and the cash-flow motive

[Confirmed] **All memberships live in the dermis.ai app.** Nafisa cannot recall the
membership tiers from memory ("it's quite a lot") and needs to share the dermis.ai
back-end login before they can be documented.

[Confirmed] The commercial mechanic she cares about: a patient selecting a membership
checks out through **Klarna**, Klarna pays PureMed **the full year up front**, and the
patient repays Klarna monthly. Nafisa's current memberships are paid monthly direct to
her, which is the cash-flow position she wants to change. Her framing: "you want to get
as many people joining a membership, because when they check out they check out with
Klarna, and it pays the whole year's worth of amount all in one go."

[Confirmed] Osman's characterisation, which Nafisa accepted: it is an unsecured loan.

### 3.4 Loyalty points

[Confirmed] The dermis.ai app runs a **points scheme**: points accrue per pound spent
and are redeemable against add-ons to a treatment. **Constraint stated by Nafisa: the
redeemable add-on has to be low cost to her.**

### 3.5 Discount codes and referral pricing

[Confirmed] **None today.** Nafisa is interested in having them.

[Unanswered] Osman referenced an existing "£25 off" and Nafisa answered affirmatively,
but the exchange immediately pivots to the points scheme, so it is unclear whether a £25
discount actually exists somewhere in the app or whether this was a mis-hearing of the
£25 booking fee from 2.6. **Do not assume either way.**

---

## 4. Consent, medical history and documents

### 4.1 Where documents live

[Confirmed] **Everything lives inside the client record in Faces Consent**, with exactly
one exception: the toxin prescribing form.

### 4.2 The paper toxin prescribing form

This is the single largest documented breakage in the current operation.

[Confirmed] The process today:

1. The patient is in the chair for a toxin treatment.
2. A **paper form** is completed by hand, on the day, in the room.
3. Nafisa writes the **units administered** and the **batch number** on it.
4. **The prescriber signs it physically**, and Nafisa signs it.
5. Nafisa **photographs it** on her phone.
6. She **uploads the photograph to the patient's file in Faces**.

[Confirmed] **Step 6 does not happen.** In her words: "which I never get around to
doing. So I've got shitloads of paperwork sitting there that I haven't done."

[Confirmed] There is a **backlog of loose paper prescribing records** that are not on any
patient file. Nafisa knows the file is where they belong: "it's much easier and much more
secure that it's on their file."

[Confirmed] What she needs a digital version to carry: **units administered, the site
each was administered to, her signature as the treating clinician, and the prescriber's
signature.** She committed to photographing a completed sample and sending it so the
digital version can be built from the real thing rather than invented.

[Confirmed] **Toxin is the only treatment with this requirement.** Everything else is
handled entirely inside Faces.

### 4.3 Prescriber constraint on the diary

[Confirmed] Toxin can only be booked **on days the prescriber is present**, because he
must see the patient face to face. This is a hard scheduling dependency between a
treatment type and a second person's availability.

[Inferred] The prescriber is referred to in the transcript as "Shak" (spelling
unconfirmed, rendered variously as Shak, Shaq, chat and shut). He is a separate person
from **Shuab**, the brother running GTM and social per
`puremed-growth-engagement-plan.md`. **Confirm the spelling and confirm these are two
different people before any document names either.**

### 4.4 Whitehouse Dental Studio and CQC-regulated treatments

[Confirmed] Whitehouse Dentistry is **completely separate** from PureMed and holds its
own CQC registration.

[Confirmed] **Two named treatments must be delivered under the CQC registration**, not
under PureMed:

- **Hyperhidrosis** (excessive sweating)
- **Toxin in the jaw for clenching / bruxism**

[Confirmed] The current handling is deliberately manual and deliberately offline: Nafisa
books those patients in **by hand** and sees them at the dental practice. Her reason for
keeping them off the online path: "it just gets too confusing if they're doing it
online."

[Confirmed] The typical origin of these cases is the **hygienist's patients** presenting
with jaw clenching, who then need toxin.

This directly validates REC-004 in the requirements register: the provider and registered
location that delivered a treatment is a distinct fact from which practitioner delivered
it, and it is currently tracked nowhere except in Nafisa's head.

### 4.5 Yellow Card / adverse event reporting

[Confirmed] **Has never come up.** No adverse event has required MHRA reporting. There is
no process, formal or informal, because there has never been an occasion for one.

---

## 5. Clinical photography

This is the second largest breakage, and the one Nafisa is most explicit about.

### 5.1 Current process

[Confirmed] Photographs are taken in an app called **TimeMark** (transcribed as "time
stamp, I think it is, yeah, time, mark"), chosen because it **stamps the location and
the time** onto the image.

[Confirmed] **Volume: 7 to 15 photographs per patient**, covering different angles and
different treatment sites, **for every patient**.

[Confirmed] **The photographs stay on Nafisa's personal phone.** Her own assessment:
**"which it shouldn't."**

### 5.2 The workflow she abandoned

[Confirmed] She previously ran a manual routine: create a folder named with the date,
put that day's patients into it, upload the folder to Dropbox, then delete from the
phone. She stopped: "I haven't been doing it because it's an extra step that is just so
long."

### 5.3 Why the Faces upload path fails

[Confirmed] Faces does support uploading before and after photographs to a patient file,
and Nafisa has used it when she had time. It fails at volume because it is **one photo at
a time**: select a photo, wait for it to upload, select the next. At 7 to 15 photos per
patient this is unusable.

### 5.4 The requirement, in her words

[Confirmed] "I need to be able to select all and then just upload it straight away, and
then it not be on my phone anymore."

Three distinct requirements in one sentence: **bulk multi-select**, **immediate upload**,
and **removal from the device afterwards**.

### 5.5 Photography consent

[Confirmed] Clinical photography consent is captured within the existing forms.

[Confirmed] **Marketing consent is a separate yes/no**, which patients can decline.

[Confirmed] The stated marketing commitment: "if we're using your pictures for marketing
we'll do our best to conceal your identity." That is a promise the system needs to make
mechanically enforceable, not a policy sentence.

---

## 6. Staff, diary and premises

### 6.1 Staff

[Confirmed] **No receptionist. No admin. Nobody else in the business day to day.**
Nafisa runs the whole operation, plus the prescriber for toxin days.

### 6.2 The diary

[Confirmed] **Faces Consent is the single central booking system** and the single source
of truth for availability. There is no competing calendar governing what is bookable.

### 6.3 Rooms and resources

[Unanswered] Asked whether the treatment room is hers alone or shared and double-booked.
The answer did not survive transcription. The context implies it is hers, but this is
**not confirmed**, and it matters given the shared premises with Whitehouse.

### 6.4 Working pattern

[Inferred, low confidence] The transcript is badly mangled here. The reconstruction:

- She does **hygiene on Friday morning**.
- **Monday** appears to be the only day she can work later into the evening.
- **Friday afternoon she must leave at 15:00** for the school run.
- **Toxin days are constrained to the prescriber's availability.**
- The prescriber has an **admin day** on which he does the school run.

**Every line of this needs confirming before it is configured as a working pattern.**
Availability is the one thing that is silently wrong until a patient turns up to a locked
door.

### 6.5 Qualification, insurance and indemnity

[Unanswered] Asked directly, including whether expiries are tracked. The answer did not
survive transcription beyond a fragment ("everything I said in one place"), which is not
enough to record. **Re-ask.** This gates DIARY-001.

---

## 7. Communications

### 7.1 Automatic, from Faces

[Confirmed] Faces sends, on booking: **appointment confirmation**, **consent form** and
**aftercare**. [Inferred] The sender is a no-reply-style address on the Google Workspace
domain set up during the email migration.

### 7.2 Marketing, from MailChimp

[Confirmed] Roughly **weekly** newsletters, entirely manual:

1. Export patient email addresses from the Faces database.
2. Import into MailChimp.
3. Build and send the campaign.

[Confirmed] Unsubscribes are respected and suppressed. Consent basis stated as "they were
giving it permission" at capture.

[Confirmed] The most recent campaign promoted **the new website and the AI skin scanner**.

[Confirmed] The sender is masked but replies land in **Nafisa's own Gmail inbox**.

There is **no integration between MailChimp and Faces**. Every send starts with a manual
CSV export, which means the list drifts out of date between campaigns and unsubscribes
only hold inside MailChimp.

### 7.3 Email client

[Confirmed] **Gmail web browser on desktop, Gmail app on phone.** No other client.

### 7.4 Dominant channel

[Confirmed] **WhatsApp.** Stated flatly when asked to pick between email, SMS and
WhatsApp.

### 7.5 Aftercare

[Confirmed] Faces sends aftercare automatically, and **it does not land**. Nafisa's
experience: "nine times out of ten, when I say, oh, did you get your aftercare from your
email, they're like, I haven't checked it, or they don't know." She then **re-sends it
over WhatsApp** manually.

[Confirmed] The aftercare documents are **AI-generated PDFs, one per treatment**, generic
in structure ("after your Botox, do these things, don't do these things"). They are **not
personalised** to the patient, the practitioner or the prescriber.

### 7.6 Treatment plans, the one personalised artefact

[Confirmed] Nafisa produces **bespoke treatment plans** for individual patients. Each
carries: **the patient's own photograph**, what was discussed in their appointment, the
recommended sequence of treatments, and **the prices**. Example given: a patient needing
polynucleotides under the eyes, plus microneedling, plus peels.

[Confirmed] **Sent over WhatsApp.** Produced by hand.

[Confirmed] She raised this herself, unprompted, as the thing she has tried to
personalise. Origin: three patients from the same workplace came in for different things,
which prompted her to start doing it. This is the highest-value manual artefact in the
business and it currently has no system behind it.

---

## 8. Data estate

| Fact | Detail |
|---|---|
| Patient records in Faces | **~475** [Confirmed], explicitly not thousands |
| Acuity Scheduling | Dormant, holds **old patients and their notes** [Confirmed] |
| Spreadsheets, other CRMs, notebooks | **None** [Confirmed], asked directly |
| Photographs | On Nafisa's phone, some in Dropbox [Confirmed] |

[Confirmed] On Acuity: she used it for a long time and expects it holds patients she no
longer has, through natural attrition. She expects the **exported contact list to be
broadly the same**, but the **notes on long-standing patients are the unique value**:
"long-standing patients, yeah, loads" of notes. Access to that data is needed.

[Confirmed] **What Acuity had that Faces does not: Google Calendar integration.** A
booking in Acuity wrote through to her Google Calendar. This is the one capability she
named as a regression.

[Confirmed] **Her current workaround is an LLM automation.** She has ChatGPT connected to
her email, and when it sees a booking confirmation email it creates the Google Calendar
event. Osman's response on the call: test any replacement with a test email first, and
design a non-overlapping approach so the two automations do not both write events.

[Confirmed] The dermis.ai app does **not** integrate with Faces. [Inferred] It also
writes into Google Calendar, which makes calendar accuracy load-bearing across three
independent writers.

**Three systems, no integration, and an unmanaged LLM automation writing to the calendar
that governs whether she turns up.** This is the single most fragile thing in the
current estate.

---

## 9. dermis.ai

[Confirmed] Scope is **considerably wider** than the "manages the live site and has
offered an app" recorded in `puremed-growth-engagement-plan.md`. dermis.ai currently
runs:

| Service | Detail |
|---|---|
| Website | The live `puremed.uk` site and its maintenance [Confirmed] |
| Mobile app | Memberships, loyalty points, Klarna checkout [Confirmed] |
| Payments | Klarna, inside the app [Confirmed] |
| AI skin scanner | Lead-generation tool, lead data captured [Confirmed] |
| Meta ads | A campaign to push the skin scanner, included in the package [Confirmed] |
| **AI voice agent** | Calls skin-scan leads to convert them to bookings [Confirmed] |
| SMS follow-up | Reminder texts every day or two after the call [Confirmed] |

### 9.1 Nafisa's position

[Confirmed] **She intends to stay with them for now.** "I like the skin scan, I'll see how
it goes." This is not a vendor she is looking to exit.

[Confirmed] **She does not know how the app works.** She has not had the onboarding call
and does not know how the app's payments and memberships relate to anything else. She
committed to putting the **dermis.ai back-end login into the shared Google Sheet**.

[Confirmed] Osman proposed that he or Shuab **join the dermis.ai onboarding call** to
understand the architecture, integrations and orchestration. Nafisa agreed.

[Confirmed] The live site carries a **large pop-up pushing app download** on arrival.
Nafisa added it deliberately to drive installs, but has **not started advertising the app**
and acknowledges it is not really active.

### 9.2 Two flags raised on the call

**Brand positioning conflict.** [Confirmed] Osman positioned PureMed on Nafisa herself as
the product, with the personal touch as the differentiator. dermis.ai's current
positioning is heavily AI-forward. These are pulling in opposite directions on the same
brand, at the same time, on the same domain.

**The undisclosed AI caller.** [Confirmed] The voice agent introduces itself as "Aria from
PureMed Aesthetics". Nafisa's own description: it is convincingly human, with typing and
call-centre background noise mixed in, and **"I don't think they'd realise that it's
AI."** Her patient base skews older.

Recorded here as fact, not as a judgement. It is flagged for a decision in Section 12.3
because it is a real exposure sitting under Nafisa's brand and involves health-adjacent
lead data.

[Not covered] Contract terms and notice period with dermis.ai. In the prep doc, never
reached. **The call transcript is truncated at this point**, so it is possible this was
discussed and lost.

---

## 10. Actions committed on the call

| # | Action | Owner |
|---|---|---|
| A1 | Download every consent form from Faces per treatment into Dropbox, as a single controlled set, so nothing is "flying around all over the place" | Osman |
| A2 | Review the downloaded consent forms before anything is built against them | Nafisa |
| A3 | Add the new "must call the patient beforehand" step to the toxin form | Nafisa |
| A4 | Photograph a completed paper toxin prescribing form and send it, so the digital version is built from the real artefact | Nafisa |
| A5 | Put the dermis.ai back-end login into the shared Google Sheet | Nafisa |
| A6 | Join the dermis.ai onboarding call to map the app architecture and integrations | Osman and/or Shuab |
| A7 | Get access to the Acuity historical data, specifically the notes on long-standing patients | Osman, needs Nafisa's credentials |
| A8 | Test any calendar automation with a test email first, and design it not to collide with the existing ChatGPT automation | Osman |
| A9 | Read this as-is document back to Nafisa for a sanity check before target-state design is finalised | Osman |

---

## 11. Open questions carried forward

Grouped by whether they block work.

### 11.1 Blocking, needed before build

1. **Deposit policy, one answer.** "Everyone always" versus "discretionary first offence,
   hard on repeat offenders". These are different systems. (2.5)
2. **Working pattern.** Actual days, actual hours, actual toxin days, actual school-run
   constraints. Currently low-confidence inference. (6.4)
3. **Qualification, insurance and indemnity tracking.** Never answered. Gates DIARY-001. (6.5)
4. **Is the room shared?** Never answered. Affects resource modelling. (6.3)

### 11.2 Blocking, needed before migration

5. **What Faces Consent actually holds**, at field level, and whether it can be exported.
   Requires admin access.
6. **Who holds admin access** to Faces and to Acuity today. Not asked.
7. **Faces Consent contract terms and notice period.** Not asked.
8. **Whether Faces payments genuinely run on Stripe.** Nafisa believes so. Unverified.
   Affects whether payment history can be reconciled or migrated at all. (3.1)

### 11.3 Blocking the proposal's boundary

9. **dermis.ai contract terms and notice period.** (9.2)
10. **What the dermis.ai app actually does**, architecturally. Blocked on A5 and A6. Until
    this is known, the boundary between what dermis.ai owns and what MSS would build
    cannot be drawn, and memberships, loyalty points and Klarna cannot be scoped.

### 11.4 Non-blocking, confirm when convenient

11. Prescriber's name spelling, and confirmation he is a different person from Shuab. (4.3)
12. Whether a £25 discount exists in the app, separate from the £25 booking fee. (3.5)
13. Whether Whitehouse's CQC registration covers hyperhidrosis and jaw toxin specifically,
    at the provider, location and activity level. Carried over from the existing plan's
    action item, now with two named treatments attached to it. (4.4)

*A fourteenth item, whether anything was discussed after the transcript's truncation
point, was closed on 10 August 2026: nothing material was lost. See Section 0.*

---

## 12. Design implications

**Osman's reading, not Nafisa's statements.** Separated deliberately so the as-is record
above stays clean. These feed the target-state design and the proposal; they are not
discovery findings.

### 12.1 Superseded 14 August 2026: full replacement, not gap-first

**This subsection originally argued for a gap-first build over replacing Faces. That
position is superseded.** Osman decided on 14 August 2026 that the Faces booking flow
itself, not just the five gaps around it, is now in scope for this phase: it is clunky (no
direct treatment landing, excess clicks), it is set to become the primary booking entry
point, and it is about to carry deposit payment. Asking a patient to pay at the end of a
bad flow undermines the deposit work directly, so the replacement moves from "later,
if the first stage earns it" to part of this stage. `puremed-systems-proposal.md` reflects
this: one system now replaces Faces Consent's booking, diary and record-holding functions,
migrating the 475 patient records and the existing consent form library unchanged, rather
than five point fixes sitting on top of Faces.

The original five gaps still stand and are still the five things that most directly cost
Nafisa time and carry regulatory exposure. What's changed is the foundation they get built
on:

| Gap | Cost today | Section |
|---|---|---|
| Bulk clinical photo capture and offload | 7 to 15 photos per patient stuck on a personal phone, every patient, indefinitely | 5 |
| Digital toxin prescribing record | A growing backlog of loose paper with prescriber signatures, off-file | 4.2 |
| Enforced deposits | No mechanism, so no enforcement, so repeat no-shows continue | 2.5, 2.7 |
| Calendar sync | An unmanaged LLM automation writing to her working calendar | 8 |
| Aftercare and treatment plans over WhatsApp | Aftercare fails 9 times in 10, treatment plans are fully manual | 7.5, 7.6 |

This raises the size and risk profile of the first stage considerably: a booking and record
migration off a live system with 475 patients is a materially bigger and more sensitive
piece of work than five additive point fixes, and it depends on answers to 11.2 (what Faces
holds at field level, whether it can be exported, admin access, contract/notice terms) that
were previously only needed before a later migration conversation. Those are now
first-stage blockers, not later-stage ones.

### 12.2 WhatsApp is not a channel, it is the operating surface

Bookings arrive there. Deposit links go out there. The £25 fee is collected there.
Aftercare only lands there. Treatment plans only exist there. **A system that treats
WhatsApp as an optional notification channel will be bypassed within a fortnight**, the
same way the Dropbox photo routine and the Faces photo upload were both abandoned for
being one step too long.

The corollary: every workflow needs to survive the "is this fewer steps than what she
does now" test, because the as-is record contains two separate examples of a
technically-correct process being silently dropped for being slower than the shortcut.

### 12.3 Three things need a decision, not a design

- **The undisclosed AI caller.** An AI agent presenting as a human, calling patients under
  PureMed's name, working from health-adjacent lead data, with an older patient base. This
  sits under Nafisa's brand and her professional registration, not dermis.ai's. It needs a
  position taken before it is discovered by someone else. (9.2)
- **Two brands on one domain.** AI-forward versus practitioner-led. Both are live right
  now. (9.2)
- **The dermis.ai boundary.** Memberships, loyalty points and Klarna are real revenue
  mechanics living entirely inside a vendor system nobody on the MSS side has seen. The
  proposal cannot draw a scope line through this until A5 and A6 are done. (11.3)

### 12.4 The photography requirement is a build constraint, not a feature

"Select all, upload immediately, gone from the phone" plus PHOTO-001 (never touches the
device photo library) plus the TimeMark metadata she relies on, together mean a **native
in-app capture surface**. It cannot be a web upload form, because a web form cannot stop
the OS writing to the camera roll first. This is the one requirement in the whole set
that dictates a platform choice, and it should be priced and sequenced accordingly.

---

## 13. Resume prompt

> Read `main-stage-studio/02_clients/puremed/discovery/2026-08-10-as-is-operating-model.md`.
> The as-is model is captured from the 10 Aug 2026 Nafisa discovery call. Next step is
> A9 (read it back to Nafisa) and closing the Section 11.1 blocking questions. Target
> state and phasing live in `clinical-platform/puremed-clinical-platform-plan.md`
> Section 9; the client-facing version is `puremed-systems-proposal.md`.
