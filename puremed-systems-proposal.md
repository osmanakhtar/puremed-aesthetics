# PureMed Aesthetics: Systems Proposal

**Prepared for Nafisa by Osman Akhtar, Main Stage Studio**
10 August 2026

---

## What I heard

Every patient you treat generates seven to fifteen photographs, a consent form, a medical
form, and on toxin days a paper prescribing sheet that needs two signatures. The
photographs stay on your phone. The prescribing sheets are in a pile. You already know
both of those things, because you're the one who told me.

That is the shape of the whole problem. Not that anything is broken, but that the parts
that need a human are all landing on the same human, and there is only one of you.

Three things stood out on the call.

**Faces Consent holds the diary, 475 patient records, and consent forms that already match
what you offer.** As a record, it's doing its job.

**WhatsApp is where the business actually runs.** Patients book there. Deposit links go
out there. Aftercare only lands there, because nine times out of ten the emailed version
never gets opened. Your treatment plans exist there and nowhere else.

**The friction is in the gaps between the two, and the booking page is the one gap that
sits underneath everything else.** Faces cannot take fifteen photos at once, so you stopped
using it for photos. Faces cannot hold the prescribing form, so it stays on paper. Faces
cannot take a deposit when you book someone in yourself from a WhatsApp message, so those
bookings take none. And the booking flow itself, which we've talked about before, makes a
patient scroll the full treatment list instead of landing on what they want, in more clicks
than it needs. That's a live cost today. It becomes a disqualifying one the moment it's also
the thing asking for a deposit.

Patching five gaps around a system whose front door doesn't work isn't the right shape of
fix. Everything below is one system, built once, that does what Faces does today and does it
properly, rather than five separate repairs sitting on top of it.

---

## What I'm proposing

One system, replacing Faces Consent, built around the six things that need to work.

### 1. One booking system, one calendar

This replaces the Faces booking page as the primary way patients book you, whether that's
you putting them in yourself from a WhatsApp message or them booking directly. A patient
lands on the treatment they want and books it in a handful of steps, not a scroll through
everything you offer. Toxin slots only ever show when the prescriber is actually in, so
that constraint stops living in your head.

It also becomes the single source of truth for your calendar. Right now three different
things write to your Google Calendar, including a ChatGPT automation reading your inbox.
That works until the day two of them disagree, and the day it goes wrong is a day you don't
turn up. This replaces all three. I'll test it against dummy appointments before it goes
anywhere near a real one.

This is first because everything else in this list either runs through it or depends on it.

### 2. Patient records and consent forms

Your 475 patient records and your consent form library move across as they are. Same
forms, same content, nothing rebuilt or rewritten, because the library already matches
what you treat and there's no reason to touch it. What changes is where they live and how
they're issued: reissued forms come back pre-filled with what's already on file, and the
patient signs to confirm it's still accurate, the way you asked for on the call, rather
than starting blank every time.

I'm downloading the full current set from Faces first, so we both know exactly what's in
it before anything moves.

### 3. Photographs

You take the photos as you do now. They upload in one action, all of them, straight onto
the patient's record. Then they come off your phone, once the upload is confirmed and not
before. Time and location stay stamped on them, the way TimeMark does it now, because
that is why you use TimeMark.

Clinical photos of your patients sitting on a personal phone is the one thing in the
current setup I'd want resolved regardless of anything else.

### 4. The toxin prescribing record

The paper form becomes a digital one. Units, the site each was administered to, the batch
number, your signature and the prescriber's, completed in the room on the day. It lands
on the patient's file when you finish it, so there is no photograph, no upload, and no
pile.

I'll build it from the real form you're sending me, not from a template. The existing
backlog gets dealt with as a separate one-off exercise, because those are records of
prescription-only medicine and they need to be on file.

### 5. Deposits that hold

A deposit is requested on every booking, including the ones you make yourself after a
WhatsApp message. Card, Apple Pay and Google Pay at the point of booking.

The part that matters is not the payment. It's that when someone who has cancelled twice
tries to rebook, the system asks them for money and you don't have to. You said you need
to be able to say "I can't change it." This is what makes that true, and it only works
because the booking flow in item 1 is worth asking someone to pay through.

### 6. Aftercare and treatment plans

Aftercare goes out on WhatsApp, where patients read it, and I'll be able to tell you
whether it landed.

Treatment plans are the more interesting one. You already build them by hand: the
patient's photo, what you discussed, the recommended sequence, the prices. It's the best
thing you produce and it takes you the longest. That becomes something you generate from
the consultation in a few minutes, still personal, still yours, without the assembly.

---

## What I'm not touching

Worth being just as clear about this.

**Your consent forms don't change.** They move across as they are, not rebuilt or
rewritten. The library already matches your treatments and there's no reason to touch the
content, only where it lives.

**Nothing moves until you've seen it move.** I'm downloading the full current set from
Faces first, migrating in a way I can test against real records before anything patient-
facing switches over, and you'll see it working before it's live.

**Memberships, loyalty points and Klarna are out of scope** until I understand how the
dermis.ai app actually works. Those are live revenue mechanics and I'm not designing
around a system I haven't seen.

**Your relationship with Faces itself** (contract terms, notice period, who holds admin
access) is something I still need from you before I can tell you how the move away from it
actually happens in practice. That's separate from what gets built.

---

## The order, and why

The booking system and the record migration come first, because everything else in this
list is built on top of them and none of it can go live until they're solid.

Photographs and the prescribing record follow closely behind. They affect every patient,
they're the two where the current position carries real regulatory exposure, and neither
is waiting on a decision from anyone.

Deposits next, once you've settled the policy question below, because it needs the
booking system already live to sit on.

Aftercare and treatment plans last, because neither is losing you anything today in the
way the others are.

I'm not putting dates against these yet. I'll do that once the three questions below are
answered, because two of them change how long the first stage takes, and this is now a
bigger first stage than it would have been if I were only patching around Faces.

---

## What I need from you

**One decision left.** *(Updated 16 August 2026: two of the original three are answered.
Kept here so you can see what I've recorded, and correct me if I've got either wrong.)*

1. ~~**Deposits.**~~ **Answered: everyone pays, no exceptions.** That's what I'm
   building. It also means the system, not you, is the one asking a long-standing patient
   for money before it will rebook them.

2. ~~**Your working pattern.**~~ **Answered: Wednesday 10 to 3, Friday 1 to 5**, with
   Friday the day you can run later if you need to. When those fill up, Thursday opens
   next because the prescriber is in, and Monday after that. I'm building it as that
   order rather than as a fixed weekly timetable, so opening a day is a setting rather
   than a rebuild.

3. **Qualifications, insurance and indemnity.** Where these are held now and whether
   anything tracks expiry dates. We ran out of time on this one, and it's the last thing
   holding up the diary side of the first stage.

**One new question, and it needs someone other than you.** For the treatments that run
under Whitehouse's CQC registration (the hyperhidrosis and the jaw toxin), whose system
is supposed to hold the clinical record: yours, or Whitehouse's? I'd assumed yours, and
on checking I don't think I can assume that. It changes how I build the record for those
two treatments, so I'd rather ask now than rebuild it later. Whoever holds Whitehouse's
registration is the person who can answer it.

**Four things to send me.**

- A photo of a completed paper prescribing form, so I build the real thing
- The dermis.ai back-end login, into the shared sheet
- Access to the old Acuity account, for the notes on your long-standing patients
- Confirmation of who holds admin access on Faces Consent, and whether you're in contract

**One thing to do.** Add the pre-appointment call step to the toxin form, so I can see how
Faces handles it.

---

## Three things to flag

Not part of the build, but they came out of the call and you should have them in writing.

**The AI caller.** The voice agent introducing itself as Aria calls your patients under
your name, and by your own description they wouldn't know it isn't a person. That sits
against your GDC registration and your brand, not dermis.ai's. I'm not telling you to
switch it off. I am saying it needs a decision you've made deliberately, rather than one
that gets made for you later. The straightforward version is that it discloses it's an
assistant at the start of the call. Most people don't mind. Being told afterwards is
what people mind.

**Two brands on one website.** I positioned PureMed on you: your expertise, your
judgement, the fact that patients are choosing a person. The live site currently leads
with AI. Both are running right now on the same domain and they pull against each other.
Worth a conversation with Shuab in the room.

**Your "no refunds" terms.** They appear in the consent forms, the website and the terms
and conditions. A blanket no-refund clause on a consumer service is the kind of term that
doesn't always hold up. It's a half-hour job for a solicitor and it fixes all three at
once. I'd get it looked at before we build anything that repeats it.

---

## What happens next

I'll send you the as-is write-up first, which is my record of everything you told me on
the call, so you can correct anything I've misheard before it turns into a build.

Once you've read that back and answered the three decisions, I'll come back with a
sequence, timings, and the commercial side. I'm deliberately not putting numbers against
this yet. Two of those answers change the size of the first stage, and I'd rather quote
you something real than something I have to revise.

The short version: one system replaces Faces, the photographs come off your phone, the
paper goes away, and it starts asking for the deposit so you don't have to.
