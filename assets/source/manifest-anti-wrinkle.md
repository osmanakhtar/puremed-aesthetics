# PureMed — Generated Asset Manifest (Anti-Wrinkle)
Generated: 2026-06-22
Source page: puremed-anti-wrinkle.html

---

## Placements

### hero-flux2
- Type: hero-image (cross-section v1)
- Aspect ratio: 9:16
- Model: Flux 2.0 Pro (`flux_2`, variant: pro)
- Seed: 357135
- Dimensions: 720 × 1280
- Output URL: https://d8j0ntlcm91z4.cloudfront.net/user_33ylt5CvJwzQ3wD9Au6wHSPDMkv/hf_20260622_152359_d838098c-e376-4cfe-ae1f-86aaa04cc155.png
- Thumbnail: https://d8j0ntlcm91z4.cloudfront.net/user_33ylt5CvJwzQ3wD9Au6wHSPDMkv/hf_20260622_152359_d838098c-e376-4cfe-ae1f-86aaa04cc155_min.webp
- Job ID: `d838098c-e376-4cfe-ae1f-86aaa04cc155`
- Prompt: Woman aged 38–50, refined features, calm and composed expression — not smiling to camera, looking slightly past it. Seated or leaning gently in a bright airy interior. Camera at medium distance, subject centred or slightly left, warm natural light from a large window fills the frame softly. Skin visible, smooth and natural — not retouched into flatness. A sense of ease and quiet self-possession — a woman who is at home in herself. Background: pale warm interior, white or warm-white walls, clean architectural detail, suggestion of considered space. Soft diffuse daylight. No hard-edged shadows. Palette: clean warm whites, soft muted mid-tones, a whisper of champagne warmth in the light. Avoid: before-and-after framing, injectable imagery, models smiling directly at camera, clinical or sterile environments, spa-style staging, anything that reads as a medical or beauty treatment advertisement.
- Notes: SELECTED as final hero.

---

### hero-kling
- Type: hero-image (cross-section v1)
- Aspect ratio: 9:16
- Model: Kling O1 Image (`kling_omni_image`)
- Dimensions: 768 × 1360
- Output URL: https://d8j0ntlcm91z4.cloudfront.net/user_33ylt5CvJwzQ3wD9Au6wHSPDMkv/hf_20260622_152401_3e4679a6-8e38-43b7-839e-310c298d4871.png
- Thumbnail: https://d8j0ntlcm91z4.cloudfront.net/user_33ylt5CvJwzQ3wD9Au6wHSPDMkv/hf_20260622_152401_3e4679a6-8e38-43b7-839e-310c298d4871_min.webp
- Job ID: `3e4679a6-8e38-43b7-839e-310c298d4871`
- Prompt: Woman aged 38–50, refined features, calm and composed expression — not smiling to camera, looking slightly past it. Seated or leaning gently in a bright airy interior. Camera at medium distance, subject centred or slightly left, warm natural light from a large window fills the frame softly. Skin visible, smooth and natural — not retouched into flatness. A sense of ease and quiet self-possession — a woman who is at home in herself. Background: pale warm interior, white or warm-white walls, clean architectural detail, suggestion of considered space. Soft diffuse daylight. No hard-edged shadows. Palette: clean warm whites, soft muted mid-tones, a whisper of champagne warmth in the light. Avoid: before-and-after framing, injectable imagery, models smiling directly at camera, clinical or sterile environments, spa-style staging, anything that reads as a medical or beauty treatment advertisement.
- Notes: NOT SELECTED. Flux chosen as final hero.

---

### what-is
- Type: editorial-image
- Aspect ratio: 3:4
- Model: Flux 2.0 Pro (`flux_2`, variant: pro)
- Seed: 112646
- Dimensions: 768 × 1024
- Output URL: https://d8j0ntlcm91z4.cloudfront.net/user_33ylt5CvJwzQ3wD9Au6wHSPDMkv/hf_20260622_160557_b58299e3-698e-4ec6-b86e-60354265a65a.png
- Thumbnail: https://d8j0ntlcm91z4.cloudfront.net/user_33ylt5CvJwzQ3wD9Au6wHSPDMkv/hf_20260622_160557_b58299e3-698e-4ec6-b86e-60354265a65a_min.webp
- Job ID: `b58299e3-698e-4ec6-b86e-60354265a65a`
- Prompt: A woman in her early forties, sitting by a window in a light-filled room at home. She is not posed — head slightly turned, looking toward the light, expression relaxed and unhurried. Camera pulled back to shoulders and face, natural framing with some breathing room around her. Morning light comes through softly diffused glass, wrapping her face evenly with no hard shadows. Her skin looks healthy and rested — texture is there, real and warm, not smoothed away. She is wearing simple, unshowy clothes. The room behind her is domestic and quiet — pale walls, nothing staged. The mood is an ordinary morning made beautiful by light. Palette: warm ivory and soft neutral skin tones, pale warm whites in the background, gentle amber quality to the natural light. Avoid: studio lighting, beauty campaign styling, models looking at the camera, clinical or medical settings, injected or frozen-looking faces, before-and-after framing, spa or wellness clichés.
- Notes: v2 — reshot after v1 felt too posed/editorial. Shifted to candid window-light framing. CSS specifies 4:5 — if build needs true 4:5, reframe with outpaint_image or re-run with Nano Banana (supports 4:5 natively).

---

## Skipped
- **before-after cards**: requires real client photography — placeholder retained in HTML.
- **who section**: HTML has only one grid column (text/cards) — no image slot confirmed in markup. Revisit if layout is expanded.
- **how section**: steps-only layout, no image slot.

---

## Notes
- `brand/anti-wrinkle-hero.png` exists in the brand folder — real photo. Consider using it in place of the generated hero if Nafisa confirms it as suitable.
- Hero selection pending: compare hero-flux2 vs hero-kling. Kling rendered taller (1360px) which may crop better on mobile.
