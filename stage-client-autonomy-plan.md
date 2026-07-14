# Stage Client Autonomy — PureMed Free-Edit Plan

**Goal:** Nafisa gets full autonomy to update her built website — inline copy editing on
every text field, image upload/swap/repositioning — with **one human gate: Osman
publishes.** New pages still go through the existing prototype → review → build flow;
once built, a page flips to free-edit.

**Requirements (Osman, 14 Jul 2026):**
1. The editor must feel like **editing a webpage** — every text field editable inline.
   No locked fields (the current `isComplexEl` lock must go).
2. Images: **drag to adjust positioning** within their frame; upload/swap with
   browser-side WebP conversion (high-res masters not needed).
3. **Submit for Publishing** replaces sign-off: it submits the updated site to Osman,
   who reviews and publishes manually. This stays a human step until the PureMed
   domain migrates off Framer. Repeat submissions must work (no one-shot lock).

**Scope:** PureMed engagement `puremed` on the Pi only. Structure/layout stays gated
by Osman; Phase 4 adds client-cloneable blocks for regions Osman designates.

**Last updated:** 2026-07-14 (initial, grounded against Pi + repo — see §1)

---

## 1. Codebase ground truth (verified 14 Jul)

| Fact | Where |
|---|---|
| Client copy editor is already visual click-to-edit on `[data-stage-id]`, but panel-based and `isComplexEl()` locks elements with nested markup | Pi `views/partials/copy.html` (~line 599, 631–669) |
| `puremed` engagement: 94 copy sections, all with `astroFile`/`astroProp` | Pi `engagements/puremed/manifest.json` |
| Astro site exists: `site/src/pages/index.astro` (32 anchors), `treatments.astro` (62), `Layout.astro` (1) | `other-projects/puremed/site/` |
| **Anchor drift:** prototype HTML has 145 anchors vs 95 in Astro — ~50 prototype sections have no publish target | Pi `engagements/puremed/prototype/` |
| **No image anchors anywhere** (`data-stage-img*` = 0); images hardcoded `src="/assets/web/…"` | Astro pages + prototype |
| Client upload + browser-WebP patch built but **NOT deployed to Pi** (`multer` absent from live `server.js`) | `scripts/stage-patches/2026-07-08-client-upload/` |
| Loop 2 exists: SSH-fetch from Pi, apply copy to Astro by stage-id, review branch, never pushes | `scripts/mss-loop2.js` |
| Loop 2 constraints: needs a `status` per section (overlay files would be skipped); `replaceStageText()` only replaces trailing text after inner markup | `mss-loop2.js` `normaliseDecisions()`, `replaceStageText()` |
| Loop 1 sign-off poller + ntfy push exists | `scripts/mss-loop1.js` |
| GitHub Actions: merge-to-main → staging, manual → production | `puremed/.github/workflows/` |
| Sign-off is a hard one-shot lock (409 on second attempt; admin reset only) | Pi `server.js` ~492 |
| Cloudways static app / secrets / domain migration: **not verified live** — Framer still serves production | `puremed/CLAUDE.md`, DEPLOY.md |
| Three engagements on Pi: `puremed` (website — this plan), `puremed-content` (social), `fsc-content` | Pi `engagements/` |

---

## 2. Architecture decisions

### D1 — One editing surface: the built Astro HTML, not the hand-made prototype
"Feels like editing a webpage" + "no locked fields" makes dual-surface (prototype on
Pi vs Astro in repo) untenable — inline edits must round-trip to the publish source
exactly. So for free-edit pages:

- Retire the hand-made prototype as the review surface.
- Pipeline: `astro build` → deploy `dist/` HTML+assets to the Pi engagement as the
  editing surface. Anchors written in Astro **source** carry through the build, so
  editor surface and publish target share ids **by construction**. Drift impossible.
- The 145-vs-95 drift audit becomes moot for free-edit pages.

### D2 — Auto-tag everything; kill the locked-field problem at the addressing layer
A one-time (re-runnable) **auto-tagger script** walks `src/pages/*.astro` +
`src/layouts/*.astro` and:
- adds `data-stage-id` (stable slug ids) to every text-bearing element missing one,
- adds `data-stage-img="<id>"` to every `<img>` / CSS-background element,
- regenerates the manifest's `copy.sections` + new `images.fields` lists
  (id → astroFile mapping) and pushes to the Pi.

Committed into source → ids stable across rebuilds. Every text field is addressable,
so nothing needs to be locked.

### D3 — Inline contenteditable with innerHTML round-trip (replaces the panel + isComplexEl lock)
- Every `[data-stage-id]` becomes `contenteditable` directly in the page iframe.
  Edit in place, save on blur/debounce. No side panel for plain text edits.
- Persistence: overlay file `output/client-edits.json` —
  `{ copy: { "<id>": { html, editedAt } }, images: { "<id>": { file?, objectPosition?, editedAt } } }`.
  Client overlay wins over `admin-copy.json` for free-edit sections.
- Because we round-trip **innerHTML** (not trailing text), nested markup
  (`<strong>`, icons in CTAs) is editable — the reason `isComplexEl` existed is gone.
- Guardrails for contenteditable mess: paste-as-plain-text, Enter → `<br>`,
  server-side sanitizer on save (allowlist: `b strong i em br a span`; strip
  styles/scripts/classes not originally present). Final safety net = Osman's git
  diff review before publishing (the human gate is part of the design, not a bolt-on).
- Structure stays gated: editing is confined to *inside* anchored elements; the DOM
  around them isn't editable.

### D4 — Images: swap + drag-to-reposition, WebP in the browser
- Deploy the existing 2026-07-08 upload patch (multer route + browser
  `canvas → toBlob('image/webp')`) — prerequisite, unchanged.
- Click an image → small overlay: **Replace** (upload or pick from approved library)
  and **drag to reposition** — pointer-drag adjusts `object-position` live
  (images render under `object-fit: cover`), saved as percentages to the overlay.
- **Effects inheritance (requirement, 14 Jul):** swaps rewrite ONLY the `src`
  attribute on the existing `<img>`; reposition writes ONLY `object-position`.
  Wrapper markup, classes, transitions, hover transforms (`.tx-featured:hover img
  {transform:scale(1.04)}` etc.) are never touched, so ken-burns/zoom-on-hover
  effects inherit automatically. Editor consequences: (a) while dragging, inject a
  temporary `.stage-editing` style that disables transitions/animations on the
  target img so the drag tracks 1:1, restore on release; (b) several imgs carry
  inline `object-position` already — read the computed baseline and update the
  inline style in place (both editor and Loop 2), never append duplicates.
- **Transcode guarantee (requirement, 14 Jul):** input accepts JPEG/PNG/AVIF/GIF —
  browser transcodes to WebP q0.85 before upload (already the patch's behaviour;
  GIF passes through for animation). Close the server hole: multer currently also
  accepts raw jpeg/png — add a sharp→WebP transcode fallback on the Pi for anything
  arriving non-WebP, so a WebP master is guaranteed regardless of client path.
  iPhone HEIC is covered by iOS converting HEIC→JPEG at the file picker; anything
  the browser can't decode → clear reject message, not a silent failure.
- Publish side: Loop 2 gains `replaceStageImage()` — rewrites `src` and updates
  `object-position` inline style on the anchored `<img>` in Astro source, **and
  copies the uploaded `.webp` binaries** from Pi `engagements/puremed/assets/` into
  repo `site/public/assets/web/`. (Attribute rewrite without file transport =
  broken images — called out because it was missing from the v1 plan.)

### D5 — Submit for Publishing: versioned submissions, human publish
- Remove the one-shot sign-off lock. `POST /api/submit/:engagement` creates
  `output/submissions/<n>-<date>.json` — a snapshot of `client-edits.json` +
  a human-readable `publish-request.md` (what changed, before → after digest).
  Editing continues immediately; resubmission any time.
- Loop 1 repointed: poll for new submissions (not `signedOff`) → ntfy push to Osman.
- Osman runs Loop 2 (extended with `--from-overlay`: treat every overlay entry as
  `changed`, `text = entry.html`; plus image apply per D4) → review branch →
  **reads the git diff** (compliance check — medical claims) → merge → staging
  workflow builds → **redeploy the fresh build back to the Pi editing surface** so
  Nafisa sees published state as her new baseline.
- Production stays manual/parked until the Framer → Cloudways domain migration.
  Until then "published" = Cloudways staging URL; Osman decides when it goes further.

### D6 — Cloneable blocks (deferred, per-region)
For regions Osman designates (e.g. treatment cards): refactor that region in Astro to
render from a JSON data file (`src/data/<region>.json`); editor gets "+ Add card"
which clones the block client-side and appends to a `repeatables` key in the overlay;
Loop 2 writes the JSON file. Client can delete only clones she created. Single
surface (D1) means the refactor happens once, in Astro only.

---

## 3. Build phases

| Phase | What | Size | Depends on |
|---|---|---|---|
| **0. Surface unification** — **DONE 14 Jul** | Auto-tagger over Astro source; `astro build`; deploy dist as the Pi editing surface; regenerate manifest; mark pages `liveEditable` | S–M | — |
| **1. Inline editor** | contenteditable on all anchors, paste/Enter guards, overlay save + revert-per-element, "edited" badges, sanitizer route on Pi | M | 0 |
| **2. Submit pipeline** | Versioned submissions + `publish-request.md`; Loop 1 repoint; Loop 2 `--from-overlay` + innerHTML write-back; end-to-end test: edit → submit → diff → merge → staging → redeploy to Pi | M | 1 |
| **3. Images** | Deploy upload patch; image overlay UI (replace + drag-reposition); `replaceStageImage()` + asset file transport in Loop 2 | M | 0 (patch deploy can parallel 1–2) |
| **4. Cloneable blocks** | Per-region Astro refactor + "+ Add" UI + Loop 2 JSON write | M–L per region | 2 |

Rationale for order: 0→1→2 gets Nafisa editing and submitting copy end-to-end with
the publish loop proven; images ride the same overlay/submit machinery once it exists.

## 4. Open items / risks

- **Cloudways staging app + workflow secrets never verified live** — must be stood up
  or confirmed before Phase 2's end-to-end test.
- contenteditable HTML hygiene: sanitizer + paste-plain mitigates; Osman's diff review
  is the backstop. Watch the first few real submissions for junk markup.
- Anchor-id stability: auto-tagger must never rename existing ids (only add missing).
- Admin/client overlay precedence: client wins on `liveEditable` sections; admin
  copy-editor should badge those "client-owned".
- The old approve/changed/flag review flow remains untouched for **new** pages
  (prototype-based, pre-build) — both modes coexist per page via `liveEditable`.

## 5. Phase 0 build record (14 Jul 2026)

- **Tagger:** `scripts/stage-autotag.js` — insertion-only scanner; `--dry-run`,
  `--manifest <out>` (additions report), `--scan <out>` (full anchor inventory).
  Overlap-free rules: tags the element owning direct text; children covered by
  parent innerHTML; warns instead of tagging when text + tagged descendant collide.
- **Result:** +215 `data-stage-id`, +20 `data-stage-img`; existing 95 untouched.
  Totals now 310 copy + 20 img anchors. Verified in dist: 0 nested tags, 0 dup ids.
- **Source fixes:** 1 warning hand-fixed (`trust-five-star-reviews` — tag moved from
  inner `<strong>` to the whole div); **3 unclosed `<span data-stage-id>` bugs in
  treatments.astro closed** (would have broken close-tag matching in Loop 2 —
  scanner now warns loudly on unclosed tagged elements).
- **Config:** `astro.config.mjs` → `build.inlineStylesheets: "always"` (single-file
  HTML; Pi can't serve extracted `/_astro/*.css`).
- **Deployed to Pi as DEV engagement `puremed-site`** (live `puremed` untouched):
  dist pages → `prototype/index.html` + `prototype/treatments.html`, 19 assets flat
  in `assets/` (the Pi's `servePrototype` rewrites any img path to
  `/assets/<engagement>/<basename>` — dist's absolute paths work unmodified),
  manifest generated from the anchor inventory (310 sections + `images.fields` 20,
  `liveEditable: true`). `loadManifest("puremed-site")` validates OK on the Pi.
- Astro repo changes uncommitted (tagged pages, config, closed spans,
  `stage-manifest-additions.json`) — commit when ready.

## 6. Resume prompt

```
Read other-projects/puremed/stage-client-autonomy-plan.md — free-edit plan for the
puremed engagement. Phase 0 DONE (see §5: auto-tagger scripts/stage-autotag.js,
310+20 anchors, DEV engagement puremed-site live on the Pi). Next = Phase 1 (§3):
inline contenteditable editor on all anchors + client-edits.json overlay +
sanitizer route, replacing the panel editor + isComplexEl lock for liveEditable
engagements.
```
