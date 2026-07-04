# PureMed — RF Microneedling Asset Manifest
Generated: 2026-06-23

## Page
`puremed-rf-microneedling.html`

## Placements

### hero — hero-image — 9:16
**Section selector:** `.tx-hero-image img` (element needs to be added to HTML — currently only overlay div exists)
**Copy context:** RF Microneedling — Skin Tightening & Resurfacing. A dual-action skin treatment combining microneedling with radiofrequency energy to stimulate deep collagen production.

**Prompt used:**
> Woman in her early 40s, three-quarter face turned slightly toward window light, seated in a minimal interior space with clean white walls and a suggested architectural frame. Soft directional light rakes across cheekbones and jaw, picking out fine skin surface detail — pore texture, subtle luminosity, an almost imperceptible warmth in the skin tone. Camera at eye level, tight crop from collarbone up, shallow depth of field with background dissolving to pale warm white. The mood is quiet precision and natural confidence — not a procedure, not a result, just skin that has clearly been cared for. Muted tones throughout: cool white walls, warm ivory skin, navy or warm grey fabric suggestion at the collar. Avoid: dark backgrounds, medical equipment, anything clinical or procedural, generic stock-model expressions, spa-style softness, beige or brown dominant tones.

| Variant | Model | URL |
|---------|-------|-----|
| v1 | Flux 2.0 Pro (seed 877488) | https://d8j0ntlcm91z4.cloudfront.net/user_33ylt5CvJwzQ3wD9Au6wHSPDMkv/hf_20260623_151732_87be1049-54b6-4c3f-b3ff-967654ed94b6.png |
| v1 | Kling O1 Image | https://d8j0ntlcm91z4.cloudfront.net/user_33ylt5CvJwzQ3wD9Au6wHSPDMkv/hf_20260623_151737_26be64f7-002e-4447-9e3b-5428c742e507.png |
| v1 | Nano Banana 2 | https://d8j0ntlcm91z4.cloudfront.net/user_33ylt5CvJwzQ3wD9Au6wHSPDMkv/hf_20260623_151740_f32cc46a-6280-4591-a552-7e5dcbae26a7.png |

**Preferred:** Not yet set — mark in manifest.json before running compression.

## Skipped placements
- **Before/After images** — real client photography already in place, do not replace
- **What-Is section** — text-only on this page (no image div in HTML)
- **Who section** — text-only on this page

## Notes
- The hero image `<img>` element does not currently exist in the HTML. The compression script's HTML update step will need to inject `<img>` into `.tx-hero-image` rather than update an existing src. Handle manually or mark `preferred: true` and run the compress script, then add the `<img>` tag pointing to the compressed path.
