# PureMed Aesthetics — Brand Identity

*Canonical visual and voice reference. All build and copy sessions defer to this file.*
*Last reviewed: 22 June 2026*

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

The requirements document takes precedence over the brand strategy doc on hex values.
Where the two documents conflicted, requirements doc values are used throughout.

| Name | Hex | Role |
|------|-----|------|
| Primary Blue | `#23476A` | CTAs, headings, icons, links, nav accents, primary buttons |
| Hover Blue | `#2D5B88` | Interactive states on buttons and links |
| Champagne Gold | `#C6A77D` | Stars, small highlights, icons, subtle dividers only |
| White | `#FFFFFF` | Primary background throughout |
| Warm White | `#F8F8F6` | Alternating section backgrounds, softer than pure white |
| Light Grey | `#F3F4F6` | Cards, table cells, subtle separation |

```css
--color-primary:    #23476A;
--color-hover:      #2D5B88;
--color-gold:       #C6A77D;
--color-white:      #FFFFFF;
--color-warm-white: #F8F8F6;
--color-light-grey: #F3F4F6;
```

**Colour rules:**
- Gold is accent only — stars, icons, dividers, nav book button. Never as a large
  background or primary section fill.
- Black (`#000000`) is explicitly excluded. The site must not feel dark.
- Avoid beige or brown backgrounds.
- Primary Blue is the trust and authority colour — it carries the brand.
- Site feel: luxurious, clinical, clean, modern, feminine — but not soft or generic.

---

## Typography

| Role | Font | Usage |
|------|------|-------|
| Headings | Cormorant Garamond | Hero headings, section titles |
| Body | Inter | Paragraphs, buttons, menus, FAQ, nav |

**Button styles:**
- Primary CTA: filled Primary Blue (`#23476A`), white text, rounded corners, slight shadow. Copy examples: "Book Consultation", "Book Free Consultation", "Check Suitability", "Send Photos For Advice"
- Secondary CTA: white background, blue border, blue text
- Nav book button: Champagne Gold accent

---

## Logo

Blue and gold mark. Studio-created vector file (`puremedvectorbluegold.ai`) in
`brand/`. Cropped PNG (`puremed_logo_cropped.png`) and full PNG (`puremed_logo.png`)
also available. Logo animation at `brand/Logo-animation.mp4`.

**Outstanding:** Nafisa to confirm whether to use studio-created version or supply
her own SVG with transparent background. Do not treat logo as locked until confirmed.

---

## Voice and Tone

**Brand character:** Expert, warm, honest, confident, and reassuring. Human and
conversational — not corporate.

**In practice:**
- Educational without overwhelming — explain treatments clearly, don't lecture
- Confident but not pushy — state what the treatment does, let the result speak
- Luxury but approachable — premium without being intimidating
- Straight-talking and clear — no vague wellness language
- Empowerment and confidence focused — the client is the subject, not the treatment

**What it never sounds like:**
- Corporate or cold — this is a one-to-one clinic, not a hospital
- Pushy or salesy — no urgency tactics, no pressure language
- Cheap or discount-led — pricing is never the hook
- Vague or generic — no "natural beauty journey" type filler
- Overdone or exaggerated — results-focused, never promise the impossible

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
