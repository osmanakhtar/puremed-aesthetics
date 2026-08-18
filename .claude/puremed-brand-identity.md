# PureMed Aesthetics — Brand Identity

*Canonical visual and voice reference. All build and copy sessions defer to this file.*
*Last reviewed: 10 August 2026*

> **Reconciled 10 Aug 2026.** This file previously carried two conflicting
> palettes: an MSS-rebuild spec (navy `#23476A`, Cormorant Garamond + Inter) and
> a separate read of the actual live puremed.uk site (navy `#343a67`, Majesty +
> Hanken Grotesk, dermis.ai platform). The live site is what patients and Nafisa
> actually see today, and new client-facing build work (starting with the Stage
> review-tool upgrade) needs one source of truth rather than two — so the live
> site's palette and type are now the canonical spec below, and the old MSS-spec
> values are retired. Do not reintroduce `#23476A`/Cormorant Garamond/Inter as
> "the" PureMed palette in any future doc or build.

---

## Positioning

Medically-led, premium aesthetics clinic focused on natural-looking results, skin
quality, and advanced non-surgical rejuvenation. Not competing on price — competing
on expertise, trust, natural outcomes, and premium patient experience.

**Target audience:** Women aged 35–65. Professionals, mums, and women entering
peri-menopause. Clients wanting subtle, natural rejuvenation who prioritise safety
and expertise over cheap pricing. Frustrated with skincare that doesn't deliver
visible lift or tightening.

**Ideal brand perception:** The trusted, premium medically-led clinic for women who
want to age well naturally. Associated with trust, expertise, subtle transformation,
and confidence.

---

## Colour Palette

Read from the live puremed.uk site (dermis.ai platform, logo served from
Firebase, fonts from `onboarding.dermis.ai`) — this is what patients and Nafisa
see today, and is the single source of truth for any new build.

| Token | Hex | Role |
|---|---|---|
| `--brand` | `#343a67` | Primary buttons, headings, links |
| `--brand-deep` | `#2a2e54` | Darker fills, banner/footer bands |
| `--forest` | `#33335a` | Text on light buttons |
| `--accent` | `#d0ac61` | Logo, highlights, icon accents |
| `--accent-on-dark` | `#e0c27a` | Gold on brand-deep backgrounds |
| `--bg` | `#f8f8f6` | Page background |
| `--bg-2` | `#eceae4` | Alternating section fill |
| `--ink` | `#23262A` | Body text |
| `--muted` | `#656986` | Secondary text, captions |
| `--line` | `#ddd7c9` | Borders, hairlines |

```css
--brand:          #343a67;
--brand-deep:      #2a2e54;
--forest:          #33335a;
--accent:          #d0ac61;
--accent-on-dark:  #e0c27a;
--bg:              #f8f8f6;
--bg-2:            #eceae4;
--ink:             #23262A;
--muted:           #656986;
--line:            #ddd7c9;
```

Card radius `18px` throughout — soft, rounded, not flat.

**Colour rules:**
- Gold (`--accent`) is accent only — logo, highlights, icon accents. Never as a
  large background or primary section fill.
- Black is not used as a primary tone. The site must not feel dark.
- Avoid beige or brown backgrounds beyond the warm `--bg`/`--bg-2` neutrals above.
- `--brand` is the trust and authority colour — it carries the brand.
- Site feel: luxurious, clinical, clean, modern, feminine — but not soft or generic.

---

## Typography

| Role | Font | Usage |
|------|------|-------|
| Headings / display | Majesty (weight 300 only, self-hosted) | Hero headings, section titles, display copy |
| Body / UI | Hanken Grotesk (400/500/600/700, Google Fonts) | Paragraphs, buttons, menus, FAQ, nav |

Majesty is a light, delicate serif — do not substitute a heavier serif for it.

**Button styles:**
- Primary CTA: filled `--brand` (`#343a67`), white text, rounded corners (18px
  radius family), slight shadow. Copy examples: "Book Consultation", "Book Free
  Consultation", "Check Suitability", "Send Photos For Advice"
- Secondary CTA: white background, brand-colour border, brand-colour text
- Nav book button / dark-background accents: `--accent-on-dark` (`#e0c27a`)

---

## Logo

**Live logo (canonical):** a gold gradient mark, a stylised face-profile
silhouette built from vertical bars (reads like a sound-wave/frequency motif),
with "PUREMED" in a thin geometric sans wordmark and "AESTHETICS" tracked below
in caps. Served from Firebase storage by the site's dermis.ai platform.

Studio-created alternative exists (`puremedvectorbluegold.ai` blue/gold mark in
`brand/`, plus `puremed_logo_cropped.png` / `puremed_logo.png` / `Logo-animation.mp4`)
but is not what's live — do not treat it as current pending Nafisa's confirmation
of which mark she wants long-term.

**Platform note:** the live site runs on dermis.ai (custom font served from
`onboarding.dermis.ai/fonts/`, a skin-scan tool at `dermis.ai/puremedaesthetics/skin-scan`),
a different build to the MSS Astro rebuild in `site/`.

---

## Voice and Tone

*Refined 9 August 2026 from Nafisa's direct guidance. This supersedes the earlier
"in practice" bullets below where the two differ — the earlier bullets are kept as
a compressed summary, but the rules and examples in this section are the working
reference for any copy session.*

**Brand character:** PureMed should sound like an experienced medical aesthetics
practitioner speaking directly to a patient — knowledgeable, honest and reassuring,
without sounding clinical, corporate or overly polished.

**The voice is:**
- Expert, but easy to understand
- Warm and approachable
- Honest about limitations and expected results
- Consultation-led, never pushy
- Confident without exaggeration
- Focused on natural-looking results and patient safety
- Written primarily for women aged 35–65
- Personal enough to feel like Nafisa, while using "we" when speaking as PureMed

**Writing rules:**
- Use plain English and explain medical terminology where necessary
- Short paragraphs, natural sentences
- "You" when speaking to the reader, "we" when speaking as PureMed
- No emojis in website copy, blogs, emails or standard posts
- No em dashes, ever (comma, colon or full stop instead)
- Avoid generic AI-style phrases: "unlock your best self", "embark on your journey",
  "transform your confidence", "say goodbye to ageing", "game-changing treatment"
- Never promise perfection, guaranteed results or permanent outcomes
- Never make the reader feel embarrassed about ageing
- Avoid sales-focused wording, urgency tactics, exaggerated claims
- Always explain downtime, risks, suitability, and when more than one treatment
  may be needed

**Worked examples:**

| Instead of | Use |
|---|---|
| "Turn back the clock and unlock younger-looking skin with this revolutionary treatment." | "This treatment is designed to improve skin firmness and support collagen production gradually. It won't completely change how you look, but it can help the skin appear firmer, smoother and better supported over time." |
| "Book now before it's too late!" | "If you're unsure whether this is the right treatment for you, the best place to start is with a consultation." |
| "We can eliminate your lines and wrinkles." | "We can soften certain lines while maintaining natural movement and keeping the result balanced." |

**What it never sounds like:**
- Corporate or cold — this is a one-to-one clinic, not a hospital
- Pushy or salesy — no urgency tactics, no pressure language
- Cheap or discount-led — pricing is never the hook
- Vague or generic — no "natural beauty journey" type filler
- Overdone or exaggerated — results-focused, never promise the impossible

**In practice (summary):**
- Educational without overwhelming — explain treatments clearly, don't lecture
- Confident but not pushy — state what the treatment does, let the result speak
- Luxury but approachable — premium without being intimidating
- Straight-talking and clear — no vague wellness language
- Empowerment and confidence focused — the client is the subject, not the treatment

Social-specific rules (hashtags, emoji allowance on Instagram/Facebook, humanise-pass
checklist) live in `content/config/voice.md` and build on this section — that file
defers to this one on anything that conflicts.

---

## Site Architecture

13 pages. Laser Lift leads in nav order, homepage treatment grid, and all related
treatment cross-links. All CTAs use `facesconsent.com/bookings/puremedaesthetics`.

| Page | Status | Notes |
|------|--------|-------|
| Homepage | Prototype complete, Bricks build in progress | |
| Laser Lift | Prototype exists, rebuild needed | Predates new template — rebuild to match other treatment pages |
| Liquid Facelift | Prototype complete | |
| Anti-Wrinkle | Prototype complete | |
| Polynucleotides | Prototype complete | |
| RF Microneedling | Prototype complete | |
| Skin Boosters | Prototype complete | |
| Thread Lifting | Not built | TBC — confirm with Nafisa whether at launch or later phase |
| EMSLIM NEO | Not built | TBC |
| Fat Dissolving | Not built | TBC |
| Semi-Permanent Makeup | Not built | TBC |
| OBAGI Skincare | Not built | TBC |
| Gallery page | Not built | Placeholder structure on homepage — full page deferred |

---

## Photography Status

Real photography is required before launch. AI-generated placeholders exist for
several slots across the site and must be replaced. Key outstanding items:

- Hero photography (Nafisa to confirm or replace)
- Before/after gallery — real results photography needed for RF Microneedling,
  Polynucleotides, and Skin Boosters slots (others confirmed from provided assets)
- Nafisa portrait — confirm current placeholder or provide professional portrait
- Polynucleotides treatment image (`pnct-treatment.png`) — AI-generated, replace

Full image inventory is documented in `brand/puremed-project-summary.docx` Section 04b.

---

## Patient and Audience Photography Direction

*Added 9 August 2026. The existing prompt files (`puremed-nafisa-prompts.md`,
`puremed-asset-generation-prompts.md`) are practitioner-side — Nafisa performing
treatment. This section covers the other half: images representing the patient,
i.e. the target reader herself. Use it whenever a placement calls for a "who this
is for" shot, a lifestyle/social image, or any stock-style photography of a woman
rather than the practitioner.*

**Who she is:** UK-based woman aged roughly 35–65. Professional, mum, or a woman
entering peri-menopause. Not a fashion model, not a "wellness influencer" — someone
who could plausibly be a patient in a Winslow or Buckinghamshire clinic. Spans three
loose bands worth casting distinctly rather than defaulting to one look:
- **Mid-30s to mid-40s** — juggling work and young family, first exploring
  prevention/maintenance rather than correction
- **Mid-40s to mid-50s** — established professional or established mum, perimenopausal,
  starting to notice change and wanting expert reassurance
- **Mid-50s to mid-60s** — confident, established, not chasing youth, wants to look
  well-rested and like herself, not different

Cast British-realistic: predominantly White British with some diversity reflecting a
Home Counties clinic's real patient base. Natural, uncoloured or naturally-greying
hair options at the older end are welcome, not something to hide. Everyday smart-casual
or professional wardrobe (the kind of clothing a real client would wear to a
consultation, not a photoshoot). Real skin texture, not airbrushed plastic — the
brand's own promise is "natural, never frozen," and the imagery has to hold to the
same standard the copy does.

**Authenticity principles (tied directly to the tone-of-voice rules above):**
- The image should never look like it's selling "perfection" — a person, not a
  retouched ideal. Visible pores, natural under-eye shadow, real expression lines are
  fine and often correct; this is what "we don't promise permanent or guaranteed
  outcomes" looks like in a photograph.
- Confident, comfortable expressions — not the wide "stock photo" grin, not a
  vacant beauty-ad stare. Somewhere between a genuine laugh caught mid-moment and a
  quiet, relaxed half-smile.
- No "before" photography that reads as sad, insecure, or ashamed of ageing. If a
  contrast is needed, it is a contrast in confidence or ease, never in looking upset
  about how she currently looks.
- No exaggerated youth-casting — do not cast a 28-year-old to represent a 45-year-old
  brief. Age should read as genuinely mid-life, because that's who is actually reading.
- Editorial and warm rather than clinical-cold or glamour-fashion. Sits between a
  premium skincare editorial and a real photograph of an actual person.

**Setting and lighting:** Follows the same environment rules as the practitioner
prompts — bright, airy, natural daylight, white/warm-white tones, navy and champagne
gold as the only accent colours, no dark or moody lighting. For lifestyle placements
(social content, "who it's for" sections) the setting can extend beyond the clinic:
home, outdoors, everyday professional settings — provided the same lighting and
colour discipline holds.

**What to avoid, specifically for patient/audience imagery:**
- Airbrushed, waxy, "AI-smooth" skin with no texture
- Glamour-model or fashion-editorial casting that reads as aspirational rather than
  relatable
- Obvious stock-photo staging (exaggerated laughing-alone-with-salad energy)
- Sad, insecure, or embarrassed "before" framing
- Anyone who reads as under 35 representing the brief

**Prompt templates:**

*Everyday confidence portrait (lifestyle/social, no clinic setting)*
> British woman aged 45-55, warm natural smile, looking directly at camera. Smart-casual
> clothing appropriate for a professional or a busy mum. Real skin texture visible —
> natural, not airbrushed. Soft natural daylight, neutral warm background (home
> interior or outdoor setting), slightly out of focus. Confident, comfortable, at ease
> in her own skin — not a glamour or fashion shot. Editorial quality, not staged stock
> photography. 4:5 or 1:1.

*Patient representation, consultation context*
> British woman aged 40-50, seated in a bright consultation room, looking toward
> someone off-camera with an engaged, relaxed expression. Everyday smart-casual
> clothing, natural hair and makeup. Real skin texture. Bright white clinic
> environment, natural light from left, navy accent detail visible. This represents
> the patient, not the practitioner — warm and present, not clinical or stiff. 4:3
> or 16:9.

*Real-skin close-up (result, not procedure)*
> Extreme close-up of a woman's skin, aged 45-plus, cheek or jawline area. Skin looks
> healthy, hydrated and well-cared-for with visible natural texture retained — this is
> "cared for," not "airbrushed." Soft natural sidelight, warm neutral background out
> of focus. No devices, no hands, no makeup product. The editorial quality of a
> premium skincare feature, not a retouched beauty-ad image. 4:3 or 1:1.

*Quiet confidence, older band*
> British woman aged 55-65, natural or naturally-greying hair, relaxed genuine
> expression, slight smile or caught mid-laugh. Well-presented, professional or
> smart-casual clothing. Real skin texture, visible expression lines. Bright, warm
> natural light. She looks well-rested and like herself, not younger or different —
> the emphasis is on ease and confidence, not transformation. 4:5 or 4:3.

---

## What to Avoid

**Design:**
- Beige or brown backgrounds
- Dark or heavy compositions (black excluded as primary)
- Gold used as a large section colour or dominant fill
- Generic stock imagery (replace all AI placeholders before launch)
- Masculine aesthetic
- Spa-style softness or over-decoration
- Overly clinical coldness

**Image style:**
- No generic injectable stock images
- No cheesy smiling stock models
- No overly filtered imagery
- Use: real clinic photography, real treatment imagery, real before/afters, soft natural lighting, luxury/editorial feel

**Copy:**
- No fluffy salon wording
- No overcomplicated medical jargon
- No aggressive sales copy
- No vague wellness language
