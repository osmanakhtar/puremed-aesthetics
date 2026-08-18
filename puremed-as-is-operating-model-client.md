# PureMed Aesthetics: How the Business Runs Today

**Prepared for Nafisa by Osman Akhtar, Main Stage Studio**
14 August 2026

---

## Why you're reading this

This is my record of what you told me on the discovery call, written back to you before any
of it turns into a build. Read it the way you'd read minutes: correct anything I've got wrong,
add anything I've missed, and don't worry about anything I've phrased more formally than you
said it. Where I've had to guess at something because the recording was unclear, I've marked
it, and those are the bits I most need you to check.

Nothing here is a proposal. That's a separate document. This is just us agreeing on what's
true today.

---

## The shape of it

Faces Consent holds your diary, your patient records, and your consent forms. WhatsApp is
where the business actually happens: patients book there, you send deposit links there,
aftercare only lands there, and your treatment plans exist there and nowhere else. There's no
receptionist and no admin. It's you, and the prescriber on toxin days.

The friction is in the gap between those two systems. Faces can't take fifteen photos at once,
so you stopped using it for photos. Faces can't hold the toxin prescribing form, so it stays on
paper. Faces can't take a deposit when you book someone yourself from a WhatsApp message, so
those bookings take none.

Everything below is the detail behind that.

---

## How a booking happens

There are two routes in.

**You book them.** A patient messages you on WhatsApp or by email, you offer a couple of slot
options, they pick one, and you put it in the diary yourself. This is mostly existing
patients. No deposit gets taken this way.

**They book themselves.** The patient goes through Faces Consent directly and books online.
Faces handles the deposit on this route.

The online route runs through Faces Consent's own booking page, and we've already talked
about this one separately from the call, so I'm noting it here rather than treating it as new.
It's clunky. A patient can't land directly on the treatment they want, they have to scroll
through the full list and pick it out. There are more clicks in the journey than there need to
be. Clients do book through it today, which is exactly why this is one of the things the
replacement booking system needs to fix, rather than something the new system inherits
unchanged from Faces.

Either way, adding the appointment to Faces fires off an automatic email: the appointment
confirmation, the consent form for that specific treatment, and a generic medical form.
Consent forms are different per treatment, toxin gets a different one to filler, and Faces
already has the right set for what you offer. The medical form is the same for everyone, and
it carries forward between visits unless something's changed. You asked for reissued forms to
come back pre-filled with what's already on file, with the patient just signing to confirm
it's still accurate, rather than starting from blank every time.

**Deposits are inconsistent right now**, and that's the thing you were clearest about wanting
fixed. You said everyone should pay a deposit, every time, because consistency is the whole
point. You also said it should be more forgiving on someone's first cancellation and firm with
repeat offenders. I've flagged that these are two different systems and we need to pick one,
in the proposal.

**New patients pay a £25 non-refundable booking fee** by SumUp link before you'll hold the
consultation slot.

**No-shows and late cancellations have no enforcement today.** It's entirely down to your
judgement in the moment, and you named a small group of repeat offenders this happens with.

**There's no waitlist**, by your own choice, because you're not busy enough yet to need one.
Two situations you did want covered when the time comes: someone asking to be called if a
specific day frees up, and a freed slot that doesn't quite match what someone else wanted.

---

## Payments

You're currently running six different ways of taking money: Faces' own card payment for
online bookings, SumUp for links sent over WhatsApp, a card machine in clinic, bank transfer
for regulars and anything over £500, GoCardless for patients spreading a treatment cost
monthly, and Klarna through the dermis.ai app for memberships. You said Apple Pay and Google
Pay would make a real difference and neither exists today outside whatever the app provides.

Your terms say no refunds, on the basis that a treatment's outcome can't be guaranteed.
Refunds are rare in practice, and when one happens, you process it yourself directly on
whichever platform took the original payment.

Memberships live entirely inside the dermis.ai app, and you weren't able to tell me the tiers
from memory, so I still need the back-end login to see them properly. The mechanic you're
chasing: a patient checking out for a membership through Klarna pays PureMed the full year up
front, and repays Klarna monthly themselves. Right now memberships pay you monthly instead,
and getting the year up front is the change you want. There's also a points scheme in the app,
points per pound spent, redeemable against add-ons, and you were clear the redeemable items
need to stay low-cost to you. You don't currently run discount codes or referral pricing, but
you're interested in having them.

---

## Consent, forms, and the toxin paperwork

Almost everything lives inside the patient's file in Faces, with one exception.

**The toxin prescribing form is still paper.** On the day, in the room, you fill it in by
hand: units administered, batch number, your signature and the prescriber's. Then you
photograph it and are supposed to upload it to the patient's Faces file. By your own
description, that last step mostly doesn't happen, and there's a backlog of completed forms
that were never filed. You know they belong on the patient record and want that fixed. This is
the one I'm building from a real photographed sample of the form, once you send it over.

Toxin can only be booked on days the prescriber is in, since he has to see the patient in
person, so that's a hard constraint on the diary.

Two treatments, hyperhidrosis and jaw toxin for clenching, are delivered under Whitehouse
Dental's CQC registration rather than PureMed's, and you book those by hand and see them at
the dental practice specifically to keep them off the online booking path.

No adverse event has ever required MHRA (Yellow Card) reporting, so there's no process for it
because there's never been an occasion to build one.

---

## Photographs

You take seven to fifteen photos per patient in an app called TimeMark, chosen because it
stamps the time and location onto the image. They stay on your phone. By your own words,
"which it shouldn't."

You used to run a manual routine, folder per day, upload to Dropbox, delete from the phone,
and stopped because it was too many steps. Faces does support photo uploads to a patient file,
but one at a time, which doesn't work at the volume you're shooting.

What you told me you actually need: select all the photos in one go, upload them straight
away, and have them gone from the phone the moment that's done.

Clinical photography consent is captured in the existing forms. Marketing consent is a
separate, optional yes or no, and where you do use images for marketing you told me you do
your best to conceal the patient's identity.

---

## Staff, diary, and working pattern

No receptionist, no admin, nobody else in the day-to-day running of the business besides you
and the prescriber on toxin days. Faces is the one and only source of truth for what's
bookable, no competing calendar.

**On your working pattern, I want to check what I've got:** hygiene on Friday mornings,
Mondays being the day you can work later into the evening, needing to leave by 3pm on Fridays
for the school run, toxin days constrained to when the prescriber is available, and the
prescriber having an admin day on which he does his own school run. Some of this was hard to
hear clearly on the recording, so please correct anything that's off before I configure a
diary against it. This is the one thing that's invisibly wrong until a patient turns up to a
locked door.

I also still need to understand where your qualifications, insurance and indemnity are held,
and whether anything currently tracks the expiry dates. We ran out of time on this on the
call.

One thing I wasn't able to confirm: whether your treatment room is yours alone or shared,
given the space you're in with Whitehouse.

---

## Communications

Faces sends the booking confirmation, consent form and aftercare automatically by email.

Your newsletter goes out roughly weekly through MailChimp, and it's entirely manual: export
patient emails from Faces, import into MailChimp, build and send. Unsubscribes are respected.
The two systems don't talk to each other, so the list drifts between sends.

You check email through Gmail on desktop and on your phone, but WhatsApp is where the business
actually runs, and that's what you told me when I asked you to pick between email, SMS and
WhatsApp.

**Aftercare fails through the official channel.** Faces emails it automatically and, by your
estimate, nine times out of ten the patient hasn't seen it, so you end up re-sending it
yourself over WhatsApp. The aftercare documents themselves are generic AI-generated PDFs, one
per treatment, not personalised to the patient or to whoever treated them.

**Treatment plans are the thing you're proudest of and the thing that takes you longest.**
Patient's own photo, what you discussed, the recommended sequence, the prices, built by hand
and sent over WhatsApp. You brought this up yourself, unprompted, as the thing you've tried
hardest to personalise.

---

## Your data today

Faces holds around 475 patient records. Acuity Scheduling is dormant but holds older patients
and notes on long-standing ones that you said are genuinely valuable and worth recovering.
There are no spreadsheets, other systems or notebooks holding patient data anywhere else.

One thing Acuity did that Faces doesn't: write straight through to your Google Calendar. Your
current workaround is a ChatGPT automation reading your booking confirmation emails and
creating the calendar event itself. On top of that, the dermis.ai app appears to also write to
your calendar. That's three separate things potentially writing to the one calendar that
tells you where to be, and none of them are talking to each other.

---

## dermis.ai

Wider than I originally understood it to be. As things stand, dermis.ai runs your live
website, the mobile app (memberships, loyalty points, Klarna checkout), the AI skin scanner
that generates leads, a Meta ads campaign pushing that scanner, an AI voice agent that calls
scan leads to try to convert them into bookings, and SMS follow-up after those calls.

You told me you're staying with them for now, that you like the skin scanner and want to see
how it performs, and that you haven't had the onboarding call yet so you don't fully know how
the app's payments and memberships work under the hood. You agreed to put the dermis.ai
back-end login into our shared sheet, and for me or Shuab to sit in on the onboarding call so
we understand what it's actually doing.

**Two things came up here that I want you to have in writing**, separate from anything to do
with the build:

The voice agent, "Aria," calls your patients under the PureMed name, and by your own
description it's convincing enough that people wouldn't know it's not a person. That's worth
a deliberate decision on your part rather than something that gets discovered by a patient
later.

The live site currently leads with AI messaging, while the direction I've taken your brand in
leads with you and your judgement as the reason someone chooses PureMed. Both are true on the
same domain at the same time, and that's worth resolving, ideally with Shuab in the room.

---

## What I still need from you

**Four confirmations**, so I'm not building against a guess:

1. The deposit policy: everyone, always, or discretionary on a first offence and firm after
   that. One decision, because they're two different systems.
2. Your actual working days and hours, the prescriber's actual toxin-day availability, and the
   school-run constraint, exactly as they really are.
3. Where your qualifications, insurance and indemnity are held, and whether expiry is tracked
   anywhere.
4. Whether your treatment room is exclusively yours.

**And the things you already agreed to send**: a photo of a completed paper prescribing form,
the dermis.ai back-end login, and confirmation of who holds admin access on Faces Consent.

Once I've heard back on the corrections above, the proposal that follows this document is
where I set out what I'd actually build and in what order.
