# PureMed Aesthetics — Discovery Constraints
*Design brief. Source of truth for all visual and copy decisions on this engagement.*
*Compiled: 23 June 2026. Reflects brand strategy document, website requirements document, and build already in progress.*

---

## Context note

This constraints doc has been written retrospectively. The prototype build is largely complete, with the colour palette partially unresolved. This document locks the decisions already made, fills any remaining gaps, and serves as the reference for anything still to be built or finalised.

---

## Spatial character

Bright, airy, and medically assured. The space should feel like the best version of a consultation room — calm, clean, and confident. Clinical enough to trust, warm enough to want to stay. Not a spa. Not a hospital.

---

## Emotional register

**Three words: Confident. Reassuring. Elevated.**

The brand sits at the intersection of medical credibility and feminine warmth. The client should feel she is in expert hands without feeling like a patient.

---

## Colour system

All colour decisions below are locked from the client's brand strategy and website requirements documents.

| Role | Name | Hex |
|------|------|-----|
| Primary | Navy Blue | `#23476A` |
| Primary hover | Hover Blue | `#2D5B88` |
| Accent (strict) | Champagne Gold | `#C6A77D` |
| Background — default | White | `#FFFFFF` |
| Background — warm | Soft Warm White | `#F8F8F6` |
| Background — secondary | Light Grey | `#F3F4F6` |

**Colour rules:**
- Navy blue is the primary active colour: CTAs, headings, icons, links, navigation accents.
- Champagne gold is an accent only. Stars, small highlights, icons, subtle dividers. Never for large sections or backgrounds.
- Backgrounds cycle between white, soft warm white, and light grey. No beige, no brown, no warm parchment tones.
- The palette must read as bright and airy. No dark backgrounds anywhere on the site.

---

## Typography

| Role | Font | Use |
|------|------|-----|
| Headings | Cormorant Garamond | Hero headings, section titles, editorial moments |
| Body | Inter | Paragraphs, buttons, menus, FAQs |

**Note:** Inter is specified by the client. It runs against the MSS default of avoiding generic system-adjacent fonts, but the client has defined it and the build is already underway. Document it as locked. If a future refresh arises, Plus Jakarta Sans would be the suggested alternative.

---

## Off-limits

Minimum two layout and aesthetic conventions this brand must never use:

1. **Dark or moody backgrounds** — this is an explicit client requirement. The site should never go dark, even for hero sections. Dark reads as masculine, heavy, or spa-adjacent, none of which fit the brief.

2. **Centred, passive hero layouts with generic smiling stock models** — the client has specifically flagged these as visual territory to avoid. Imagery must be real: real clinic, real results, real Nafisa. Soft natural lighting, editorial feel.

3. **Spa or wellness-style softness** — no water, petals, or aromatherapy visual language. PureMed is a medically-led clinic. The warmth comes from the founder and the results, not from ambient aesthetics signalling.

4. **Oversized gold sections** — champagne gold is a punctuation colour. Using it as a background or primary section treatment would undermine the clinical credibility positioning and tip into generic luxury territory.

---

## Image style

- Real clinic photography only. Real treatment imagery. Real before-and-after results.
- Soft, natural lighting. Editorial quality, not studio over-lit.
- Founder-forward: Nafisa should appear in imagery. The brand is expert-led; that expertise has a face.
- No generic injectable stock. No cheesy smiling models. No overly filtered content.

---

## What this brand is not

**Visually:** Dark. Masculine. Brown-toned. Overly clinical (sterile, cold, hospital-like). Generic spa or wellness aesthetic.

**Emotionally:** Aggressive sales energy. Fluffy salon warmth. Overcomplicated medical jargon. Anything that looks like every other aesthetics clinic website.

**Structurally:** One massive treatments page. Cluttered layouts. Low white space. Fast, busy, cheap-feeling.

---

## Voice and copy direction

**Archetype:** Warm clinical guide. Not a hard-sell medspa.

**Character:** Luxury, medically credible, emotionally persuasive, confident, natural, approachable.

**Core messaging themes:**
- Natural results — "refresh, not fake"
- Medically led — safety and anatomy expertise as the differentiator
- Ageing well — not chasing perfection
- Confidence — helping women feel like themselves again, not transformed into someone else

**What the copy never does:**
- Fluffy salon wording ("pamper yourself," "treat yourself")
- Overcomplicated clinical jargon
- Aggressive or fear-based sales copy
- Vague outcomes ("amazing results," "you'll love it")

**Tone test for any piece of copy:** would a woman aged 40 who has never had aesthetics treatments before feel reassured by this, or put off? If she'd feel pushed, it's wrong. If she'd feel understood and safe, it's right.

---

## References outside the web

Visual and tonal references for the feeling the site should carry:

- **Private members' medical clinics** (Bupa Health Clinics, the Doctors Clinic Group) — clinical authority without the NHS coldness
- **Premium skincare editorial** (Tatler, Vogue Beauty supplements) — the photography standard and the confidence of the copy
- **Scandinavian interior design** — brightness, white space, the intelligence of restraint. Not sterile. Not cold. Clean.
- **High-end dermatology clinic photography** — how light hits skin in editorial contexts, as opposed to before-and-after clinical lighting

---

## Functional notes (from website requirements)

These are not design constraints but should be visible here so nothing gets missed during build:

- Booking integration: Faces consent system
- Sticky WhatsApp button throughout
- Google Reviews integration if possible (trust bar and reviews section)
- Photo upload form — client has flagged this as a differentiator worth building
- GA4, GTM, Meta Pixel tracking to be installed
- Mobile-first: sticky CTA, compressed images, fast loading
- FAQ schema and local SEO keywords on each treatment page

---

## Brand split flag

The client profile includes Nafisa's coaching and wellness mentor activity alongside the clinic. For this build, PureMed Aesthetics is the scope. The coaching and wellness work is out of scope and should not surface on this site. If that changes, it should be treated as a separate brand conversation, not an addition to this site.

---

## Assumptions requiring validation

The following were inferred from documents rather than confirmed directly in conversation. Validate before treating as locked:

- **Exact hex values for navy** — the requirements doc specifies `#23476A` as the primary blue. Confirm this matches the actual logo file being used.
- **Inter as the final body font** — locked from the requirements doc, but worth one confirmation given the Cormorant Garamond pairing. Some weight combinations may need testing at body scale.
- **Champagne gold scope** — the requirements doc says stars, highlights, icons, and subtle dividers only. Confirm with Nafisa whether any other uses have been agreed.
