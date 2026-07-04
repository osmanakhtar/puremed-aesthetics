# PureMed Asset Audit Report — 2026-06-23

---

## Section 1 — Asset References in Prototype HTML Files

**5 HTML files contain zero asset references** (no `src=`, no CSS `url()`) — they are either skeleton shells or depend on a CMS:
- `index.html`
- `puremed-homepage-v6.html`
- `puremed-homepage-bricks-ready.html`
- `puremed-digital-consultation.html`
- `puremed-treatment-bricks-ready.html`

**6 HTML files contain references** (all relative paths resolve from `puremed/web/`):

### `puremed-anti-wrinkle.html` — 5 unique refs
| Referenced Path | Ext | On Disk? |
|---|---|---|
| `../assets/generated/compressed/puremed-anti-wrinkle-hero-flux2-v1.webp` | .webp | ✅ |
| `../assets/generated/compressed/puremed-anti-wrinkle-what-is-flux2-v2.webp` | .webp | ✅ (used twice) |
| `../brand/puremed-web-assets/before-after-anti-wrinkle-treatment.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/before-after-anti-wrinkle-treatment-2.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/puremed-full face before after.webp` | .webp | ✅ |

### `puremed-laser-lift.html` — 8 refs (5 external + 3 local)
| Referenced Path | Ext | On Disk? |
|---|---|---|
| `https://d8j0ntlcm91z4.cloudfront.net/…/hf_20260622_103717_….png` | .png | ❌ External URL |
| `https://d8j0ntlcm91z4.cloudfront.net/…/hf_20260622_103719_….png` | .png | ❌ External URL |
| `https://d8j0ntlcm91z4.cloudfront.net/…/hf_20260622_103722_….png` | .png | ❌ External URL |
| `https://d8j0ntlcm91z4.cloudfront.net/…/hf_20260622_103724_….png` | .png | ❌ External URL |
| `https://d8j0ntlcm91z4.cloudfront.net/…/hf_20260622_103726_….png` | .png | ❌ External URL |
| `../brand/puremed-web-assets/laser-lift-ba-1.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/laser-lift-ba-3.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/laser-lift-ba-4.webp` | .webp | ✅ |

### `puremed-liquid-facelift.html` — 6 refs
| Referenced Path | Ext | On Disk? |
|---|---|---|
| `../assets/generated/compressed/puremed-liquid-facelift-hero-soul2-v1.webp` | .webp | ✅ |
| `../assets/generated/compressed/puremed-liquid-facelift-what-is-recraft-v1.webp` | .webp | ✅ |
| `../assets/generated/compressed/puremed-liquid-facelift-who-recraft-v1.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/before-after-Liquid-facelift.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/before-after-Combination-treatment-Liquid-facelift.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/before-after-filler-1.webp` | .webp | ✅ |

### `puremed-polynucleotides.html` — 3 refs
| Referenced Path | Ext | On Disk? |
|---|---|---|
| `../brand/puremed-web-assets/before-after-Polynucleotides.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/before-after-Microneedling-plus-polynucleotides.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/ba-polynucleotides-3.webp` | .webp | ✅ |

### `puremed-rf-microneedling.html` — 3 refs
| Referenced Path | Ext | On Disk? |
|---|---|---|
| `../brand/puremed-web-assets/before-after-Microneedling-plus-polynucleotides.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/ba-rf-microneedling-1.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/ba-rf-microneedling-2.webp` | .webp | ✅ |

### `puremed-skin-boosters.html` — 3 refs
| Referenced Path | Ext | On Disk? |
|---|---|---|
| `../brand/puremed-web-assets/ba-skin-boosters-1.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/ba-skin-boosters-2.webp` | .webp | ✅ |
| `../brand/puremed-web-assets/before-after-filler-1.webp` | .webp | ✅ |

---

## Section 2 — All Image & Video Files on Disk

### `puremed/assets/generated/compressed/` — 11 files, all .webp
| File | Size |
|---|---|
| puremed-anti-wrinkle-hero-flux2-v1.webp | 40K |
| puremed-anti-wrinkle-hero-kling-v1.webp | 37K |
| puremed-anti-wrinkle-what-is-flux2-v2.webp | 37K |
| puremed-liquid-facelift-hero-flux2-v2.webp | 113K |
| puremed-liquid-facelift-hero-kling01-v3.webp | 165K |
| puremed-liquid-facelift-hero-recraft-v1.webp | 245K |
| puremed-liquid-facelift-hero-soul2-v1.webp | 222K |
| puremed-liquid-facelift-what-is-nbb-v2.webp | 279K |
| puremed-liquid-facelift-what-is-recraft-v1.webp | 411K |
| puremed-liquid-facelift-who-nbb-v2.webp | 443K |
| puremed-liquid-facelift-who-recraft-v1.webp | 222K |

### `puremed/assets/generated/` — 11 files, all .png (source originals)
| File | Size |
|---|---|
| puremed-anti-wrinkle-hero-flux2-v1.png | 1.6M |
| puremed-anti-wrinkle-hero-kling-v1.png | 1.4M |
| puremed-anti-wrinkle-what-is-flux2-v2.png | 1.6M |
| puremed-liquid-facelift-hero-flux2-v2.png | 4.1M |
| puremed-liquid-facelift-hero-kling01-v3.png | 5.8M |
| puremed-liquid-facelift-hero-recraft-v1.png | 6.2M |
| puremed-liquid-facelift-hero-soul2-v1.png | 3.3M |
| puremed-liquid-facelift-what-is-nbb-v2.png | 8.5M |
| puremed-liquid-facelift-what-is-recraft-v1.png | 6.7M |
| puremed-liquid-facelift-who-nbb-v2.png | 9.2M |
| puremed-liquid-facelift-who-recraft-v1.png | 5.8M |

### `puremed/brand/` — 21 files (source originals)
| File | Ext | Size |
|---|---|---|
| Logo-animation.mp4 | .mp4 | 111K |
| Nafisa-hero.png | .png | 5.4M |
| PureMed-Logo.jpeg | .jpeg | 41K |
| PureMed-Logo.png | .png | 153K |
| anti-wrinkle-hero.png | .png | 2.3M |
| endolift-poster.png | .png | 4.0M |
| hero-micro-needling.png | .png | 2.3M |
| liquid-facelift-hero.png | .png | 1.5M |
| nafisa-hero-v2.png | .png | 1.3M |
| pnct-treatment.png | .png | 7.2M |
| puremed-Microneedling.png | .png | 1.4M |
| puremed-nafisa-doing-treatment.png | .png | 1.8M |
| puremed-nafisa-hero--do-not-use.png | .png | 1.5M |
| puremed-older lady smiling.png | .png | 1.2M |
| puremed-skin rejuvination.png | .png | 1.5M |
| puremed-skin-glow.png | .png | 7.7M |
| puremed-treatment pic.png | .png | ~1–2M |
| puremed_logo.png | .png | 91K |
| puremed_logo_cropped.png | .png | 104K |
| puremed_logo_transparent.png | .png | 147K |
| puremedvectorbluegold.ai.png | .png | 635K |

### `puremed/brand/before after watermark/` — 15 files, all .png
| File | Size |
|---|---|
| anti-wrinkle-treatment.png | 1.6M |
| ba-polynucleotides-3.png | 8.2M |
| ba-rf-microneedling-1.png | 8.9M |
| ba-rf-microneedling-2.png | 7.3M |
| ba-skin-boosters-1.png | 8.4M |
| ba-skin-boosters-2.png | 6.8M |
| before-after-Combination-treatment-Liquid-facelift.png | 1.7M |
| before-after-Liquid-facelift.png | 1.6M |
| before-after-Microneedling-plus-polynucleotides.png | 1.5M |
| before-after-Polynucleotides.png | 1.5M |
| before-after-anti-wrinkle-treatment-2.png | 1.2M |
| before-after-anti-wrinkle-treatment.png | 1.6M |
| before-after-filler-1.png | 1.6M |
| before-after-filler.png | 1.7M |
| before-after-lip-filler.png | 1.2M |

### `puremed/brand/laser lift BEFORE AFTER WATERMARK/` — 4 files, all .png
| File | Size |
|---|---|
| 1.png | 1.8M |
| 3.png | 1.9M |
| 4.png | 1.9M |
| 5.png | 1.8M |

### `puremed/brand/puremed-web-assets/` — 55 files
| File | Ext | Size |
|---|---|---|
| Nafisa-hero.webp | .webp | 107K |
| PureMed-Logo.webp | .webp | 19K |
| anti-wrinkle-hero.webp | .webp | 66K |
| anti-wrinkle-treatment.webp | .webp | 100K |
| ba-polynucleotides-3.webp | .webp | 165K |
| ba-rf-microneedling-1.webp | .webp | 132K |
| ba-rf-microneedling-2.webp | .webp | 207K |
| ba-skin-boosters-1.webp | .webp | 252K |
| ba-skin-boosters-2.webp | .webp | 159K |
| before-after-Combination-treatment-Liquid-facelift.webp | .webp | 98K |
| before-after-Liquid-facelift.webp | .webp | 107K |
| before-after-Microneedling-plus-polynucleotides.webp | .webp | 78K |
| before-after-Polynucleotides.webp | .webp | 100K |
| before-after-anti-wrinkle-treatment-2.webp | .webp | 64K |
| before-after-anti-wrinkle-treatment.webp | .webp | 109K |
| before-after-filler-1.webp | .webp | 91K |
| before-after-filler.webp | .webp | 126K |
| before-after-lip-filler.webp | .webp | 58K |
| endolift-poster.webp | .webp | 94K |
| hero-micro-needling.webp | .webp | 72K |
| hf_20260617_103402_31e6f35c-eda1-4d41-871a-fb1eee11345a.webp | .webp | 47K |
| hf_20260617_103539_e4eb126a-c0a7-4124-bce2-f9737aed9af3.webp | .webp | 49K |
| hf_20260617_103702_faaa7d5f-5881-4d4e-a4e0-0f4a01e79b3a.webp | .webp | 36K |
| hf_20260617_111819_b4c15d4e-682f-4572-aa7e-78a172960a15.webp | .webp | 30K |
| hf_20260617_111833_15664b71-8dd8-4571-96f4-d78692b20480.webp | .webp | 108K |
| hf_20260617_111837_a25747ea-454b-457c-aff1-69745048afdf.webp | .webp | 201K |
| hf_20260617_112321_0d8e6ba0-9b36-49db-ba16-4506706e20b8.webp | .webp | 136K |
| hf_20260617_112359_798198e5-deb3-4b3d-a6d0-7c0e68bad07a.webp | .webp | 120K |
| hf_20260617_112413_21fb0ef3-c8e0-498c-8590-fc4e607241f1.webp | .webp | 36K |
| hf_20260617_112726_334f3f6e-b3eb-453a-a66b-166bc27e13f6.webp | .webp | 92K |
| hf_20260617_163700_6ae933db-d42d-4587-b50e-4bfd568a6d78.webp | .webp | 42K |
| hf_20260617_165027_2886927a-5c5b-4844-bd0e-6ca1d47f3ac1.webp | .webp | 81K |
| hf_20260617_165044_6c275b7f-693f-48fd-b22d-acd5780239c0.webp | .webp | 73K |
| hf_20260617_165047_aefa9c69-4463-409f-b664-7d7ab60ffe25.webp | .webp | 61K |
| laser-lift-ba-1.webp | .webp | 186K |
| laser-lift-ba-3.webp | .webp | 148K |
| laser-lift-ba-4.webp | .webp | 159K |
| laser-lift-ba-5.webp | .webp | 151K |
| liquid-facelift-hero.webp | .webp | 35K |
| nafisa-hero-v2.webp | .webp | 49K |
| pnct-treatment.webp | .webp | 123K |
| puremed-Lower face before after.webp | .webp | ~50K |
| puremed-Microneedling.webp | .webp | 56K |
| puremed-Naf with PM sign.webp | .webp | 219K |
| puremed-full face before after.webp | .webp | ~50K |
| puremed-hero-consultation.webp | .webp | 52K |
| puremed-naf doing treatment 1.webp | .webp | 49K |
| puremed-nafisa-doing-treatment.webp | .webp | 42K |
| puremed-nafisa-hero--do-not-use.webp | .webp | 40K |
| puremed-older lady smiling.webp | .webp | 36K |
| puremed-skin rejuvination.webp | .webp | 100K |
| puremed-skin-glow.webp | .webp | 149K |
| puremed-treatment pic.webp | .webp | ~50K |
| puremed_logo.webp | .webp | 38K |
| puremed_logo_cropped.webp | .webp | 57K |
| puremed_logo_transparent.webp | .webp | 73K |
| puremedvectorbluegold.ai.webp | .webp | 18K |

---

## Section 3 — Cross-Reference

### 3A — Referenced but missing on disk
**None.** Every local relative path resolves to an existing file.

### 3B — Referenced but NOT WebP/WebM
| File | Issue | Prototype |
|---|---|---|
| `hf_20260622_103717_….png` (CloudFront) | PNG served from external CDN | puremed-laser-lift.html |
| `hf_20260622_103719_….png` (CloudFront) | PNG served from external CDN | puremed-laser-lift.html |
| `hf_20260622_103722_….png` (CloudFront) | PNG served from external CDN | puremed-laser-lift.html |
| `hf_20260622_103724_….png` (CloudFront) | PNG served from external CDN | puremed-laser-lift.html |
| `hf_20260622_103726_….png` (CloudFront) | PNG served from external CDN | puremed-laser-lift.html |

These are the hero images for the laser lift page — they live on Higgsfield's CloudFront and have never been downloaded or converted to WebP locally.

### 3C — Orphans (on disk, not referenced in any prototype)

**`assets/generated/compressed/`** — 6 orphan WebPs (alternate generations not chosen):
- puremed-anti-wrinkle-hero-kling-v1.webp
- puremed-liquid-facelift-hero-flux2-v2.webp
- puremed-liquid-facelift-hero-kling01-v3.webp
- puremed-liquid-facelift-hero-recraft-v1.webp
- puremed-liquid-facelift-what-is-nbb-v2.webp
- puremed-liquid-facelift-who-nbb-v2.webp

**`assets/generated/`** — 11 orphan PNGs (source originals, all have a compressed .webp counterpart). Combined ~53M.

**`brand/`** (root) — 21 orphan files (~50M combined):
All brand-root files: 20 PNGs + 1 MP4 (`Logo-animation.mp4`). Most have a `.webp` counterpart in `puremed-web-assets/`.

**`brand/before after watermark/`** — 15 orphan PNGs (~63M combined):
All 15 PNG source files. These have `.webp` equivalents in `puremed-web-assets/`.

**`brand/laser lift BEFORE AFTER WATERMARK/`** — 4 orphan PNGs (~7.4M):
`1.png`, `3.png`, `4.png`, `5.png` — the `.webp` equivalents (`laser-lift-ba-1/3/4/5.webp`) exist in `puremed-web-assets/` but only `-1`, `-3`, `-4` are referenced in the laser-lift prototype; **`laser-lift-ba-5.webp` is also an orphan**.

**`brand/puremed-web-assets/`** — 34 orphan WebPs (web-ready but unused in any prototype):
| File | Notes |
|---|---|
| Nafisa-hero.webp | |
| PureMed-Logo.webp | |
| anti-wrinkle-hero.webp | |
| anti-wrinkle-treatment.webp | |
| before-after-filler.webp | Note: `before-after-filler-1.webp` IS used; this variant is not |
| before-after-lip-filler.webp | |
| endolift-poster.webp | |
| hero-micro-needling.webp | |
| hf_20260617_103402_… through hf_20260617_165047_… (14 files) | Higgsfield generations from 17 Jun |
| laser-lift-ba-5.webp | ba-1/3/4 used, ba-5 not referenced |
| liquid-facelift-hero.webp | |
| nafisa-hero-v2.webp | |
| pnct-treatment.webp | |
| puremed-Lower face before after.webp | |
| puremed-Microneedling.webp | |
| puremed-Naf with PM sign.webp | |
| puremed-hero-consultation.webp | |
| puremed-naf doing treatment 1.webp | |
| puremed-nafisa-doing-treatment.webp | |
| puremed-nafisa-hero--do-not-use.webp | |
| puremed-older lady smiling.webp | |
| puremed-skin rejuvination.webp | |
| puremed-skin-glow.webp | |
| puremed-treatment pic.webp | |
| puremed_logo.webp | |
| puremed_logo_cropped.webp | |
| puremed_logo_transparent.webp | |
| puremedvectorbluegold.ai.webp | |

---

## Section 4 — All WebP and WebM Files on Disk, Grouped by Subdirectory

**No `.webm` files exist anywhere in the project.**

### `puremed/assets/generated/compressed/` — 11 WebPs
puremed-anti-wrinkle-hero-flux2-v1.webp, puremed-anti-wrinkle-hero-kling-v1.webp, puremed-anti-wrinkle-what-is-flux2-v2.webp, puremed-liquid-facelift-hero-flux2-v2.webp, puremed-liquid-facelift-hero-kling01-v3.webp, puremed-liquid-facelift-hero-recraft-v1.webp, puremed-liquid-facelift-hero-soul2-v1.webp, puremed-liquid-facelift-what-is-nbb-v2.webp, puremed-liquid-facelift-what-is-recraft-v1.webp, puremed-liquid-facelift-who-nbb-v2.webp, puremed-liquid-facelift-who-recraft-v1.webp

### `puremed/brand/puremed-web-assets/` — 55 WebPs
(See full listing in Section 2 above)

---

## Summary of Key Action Items

| # | Issue | Count | Severity |
|---|---|---|---|
| 1 | Laser-lift hero images are external CloudFront PNGs — not local, not WebP | 5 files | High — CDN dependency, wrong format |
| 2 | `laser-lift-ba-5.webp` exists on disk but is never referenced in the prototype | 1 file | Low — missing slot or deliberate |
| 3 | 6 alternate-generation WebPs in `compressed/` are orphaned (runner-up picks) | 6 files | Low — safe to delete |
| 4 | 11 PNG source originals in `assets/generated/` are orphaned (~53M) | 11 files | Low — archival weight |
| 5 | All 20 brand-root PNGs + 1 MP4 are orphaned (~50M) | 21 files | Low — archival weight |
| 6 | All 15 `before after watermark/` PNGs are orphaned (~63M) | 15 files | Low — archival weight |
| 7 | All 4 `laser lift BEFORE AFTER WATERMARK/` PNGs are orphaned | 4 files | Low — archival weight |
| 8 | 34 web-ready WebPs in `puremed-web-assets/` are not referenced in any prototype | 34 files | Medium — need to be wired up or cleaned |
| 9 | 5 HTML prototypes have zero asset references (homepage, consultation, treatment shells) | 5 files | Note — not yet built out |
