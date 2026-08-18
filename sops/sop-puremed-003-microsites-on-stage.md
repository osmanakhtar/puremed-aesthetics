# SOP-PUREMED-003: Treatment microsites on Stage (`puremed-micro`)

| | |
|---|---|
| **Purpose** | Keep the treatment-microsite review surface working: the pages Nafisa reviews and edits, and the page → booking journey the social-media POC depends on |
| **Operator** | Osman (client side: Nafisa) |
| **Verified** | 2026-08-08 (every step below run as written) |
| **Systems touched** | Stage on the Pi (`pi@192.168.1.106`, pm2 app `stage`), `02_clients/puremed/web/stage-build/`, `booking-engine/prototype/_internal-puremed-v1.0.html` |
| **Canon doc** | `02_clients/puremed/CLAUDE.md`, `booking-engine/booking-engine-plan.md` |

## What this engagement is

`puremed-micro` holds the social-media-drive POC: **seven** standalone treatment
microsites (Laser Lift, Liquid Facelift, Anti-Wrinkle, Polynucleotides, RF
Microneedling, Skin Boosters, Sculptra), a hub page that links them, and the PureMed
booking prototype as a ninth page. Each microsite is intended to get its own
Instagram presence driving traffic to it (that traffic engine is out of scope here).

**The booking journey opens inside the page.** Clicking any booking CTA slides a
drawer over the microsite containing the client-facing booking journey, with that
treatment already selected. The page stays behind it, so the treatment being sold is
never navigated away from. This is the sales mechanism: a prospect sees exactly what
their client would experience, in place. The CTA keeps a real href, so if the drawer
script fails the link still works as plain navigation.

Sculptra was rebuilt onto the shared template from its old standalone page
(`web/sculptra landing page/`, now superseded). Regenerate it with
`tools/build-sculptra-source.py`, never by hand-editing `web/puremed-sculptra.html`,
which that script overwrites.

It is deliberately **separate from `puremed-site`**, which is the surface Nafisa
edits for the real website. Nothing here touches the Astro site that ships.

| Engagement | What it is | Live-edit | Links clickable |
|---|---|---|---|
| `puremed-site` | The real website Nafisa signs off | yes | no, by design |
| `puremed-micro` | This POC | yes | yes, internal links only |

## When this runs

Whenever microsite copy, imagery or the booking mapping changes and Nafisa needs
to see it, or after any change to the booking prototype.

## Prerequisites

- SSH key access to the Pi as `pi`.
- `python3` with Pillow, and `node`, on the workstation.
- Nafisa's `nafisa` login is already scoped to `puremed-micro` in
  `/home/pi/stage/config/users.json`. Never store passwords in this repo.

## Routine operation

Run from `~/workspace/main-stage-studio/02_clients/puremed/`.

1. **Build the Stage variant** (external image files, not the inlined data URIs
   the Artifact build uses, so images stay swappable in the editor). Regenerate the
   Sculptra source first, since it is derived from the template:
   ```
   python3 tools/build-sculptra-source.py
   python3 tools/build-microsites.py --target=stage
   python3 tools/build-hub.py --target=stage
   ```
   Each page should report `booking drawer` and `sculptra nav` in its build line.

2. **Refresh the booking page** from the booking-engine prototype:
   ```
   cp ../../../booking-engine/prototype/_internal-puremed-v1.0.html web/stage-build/booking.html
   ```

3. **Tag the editable pages.** The booking page is excluded on purpose: it is a
   JavaScript app, and making its controls contenteditable would corrupt the
   journey it demonstrates.
   ```
   FILES=$(ls web/stage-build/*.html | grep -v booking.html | tr '\n' ',' | sed 's/,$//')
   node ~/workspace/scripts/stage-autotag.js --files "$FILES" --relroot web/stage-build
   ```

4. **Rebuild the manifest against the deployed one.** It refuses to write if any
   existing id would disappear, which is what protects Nafisa's in-flight edits:
   ```
   ssh pi@192.168.1.106 cat /home/pi/stage/engagements/puremed-micro/manifest.json > /tmp/base-micro.json
   python3 tools/build-stage-manifest.py --out /tmp/manifest-micro.json --base /tmp/base-micro.json
   ```
   If it refuses, **stop and read the id list**. Only if you deliberately rewrote
   that copy, and have checked the overlay for edits against it, re-run adding
   `--allow-drop <id,id>`.

5. **Deploy**, taking backups first:
   ```
   E=/home/pi/stage/engagements/puremed-micro
   ssh pi@192.168.1.106 "cd $E && cp manifest.json manifest.json.bak-$(date +%Y%m%d-%H%M%S) && cp output/client-edits.json output/client-edits.json.bak-$(date +%Y%m%d-%H%M%S)"
   scp web/stage-build/*.html pi@192.168.1.106:$E/prototype/
   scp /tmp/manifest-micro.json pi@192.168.1.106:$E/manifest.json
   ```
   Any NEW image must also go to `$E/assets/` — the Pi serves
   `/assets/<engagement>/<basename>`. Collect and copy them with:
   ```
   python3 - <<'PY'
   import re, pathlib, shutil
   refs = set()
   for f in pathlib.Path("web/stage-build").glob("*.html"):
       refs |= {pathlib.Path(m).name for m in
                re.findall(r'(?:src|href)="([^"]+\.(?:webp|png|jpg|jpeg|gif|svg|avif))"', f.read_text())}
   pathlib.Path("/tmp/asset-list.txt").write_text("\n".join(sorted(refs)) + "\n")
   print(len(refs), "assets")
   PY
   while read f; do scp "assets/web/$f" pi@192.168.1.106:$E/assets/; done < /tmp/asset-list.txt
   ```

6. **Validate:**
   ```
   ssh pi@192.168.1.106 "bash /home/pi/stage/scripts/validate.sh puremed-micro"
   ```

## Checks

- `validate.sh` prints `0 failed`.
- Zero stranded edits (must print `0`):
  ```
  ssh pi@192.168.1.106 'cd /home/pi/stage && node -e "
  const m=require(\"./engagements/puremed-micro/manifest.json\");
  const ed=require(\"./engagements/puremed-micro/output/client-edits.json\");
  const c=new Set(m.copy.sections.map(s=>s.id)), i=new Set(m.images.fields.map(f=>f.id));
  console.log(Object.keys(ed.copy||{}).filter(k=>!c.has(k)).length + Object.keys(ed.images||{}).filter(k=>!i.has(k)).length);"'
  ```
- Open a treatment page and click **Book Consultation**: a drawer must slide in
  over the page with **that treatment already selected** and the correct price and
  deposit, and the page must still be behind it. It must NOT navigate away.
- The drawer header must read "Demonstration of the booking journey. No payment is
  taken and nothing is sent."
- Stage's page switcher sits bottom-centre, collapsed, showing the current page and
  its position (e.g. "Laser Lift 2/9"). It must not cover the prototype's own header,
  and it must disappear while the booking drawer is open.
- Escape, the close button and the backdrop must all shut the drawer.
- No page should contain a `facesconsent.com` link. On the Stage build every
  booking CTA is internal:
  ```
  grep -c facesconsent web/stage-build/*.html    # expect 0 everywhere
  ```

## When it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| Clicking a CTA does nothing, caret appears instead | Browser cached an old `live-edit.js` | Hard reload. The script is now served with an mtime cache-buster (`/live-edit.js?v=…`), so this should not recur; if it does, check `liveEditVersion()` still exists in `server.js` |
| CTA navigates to the booking page instead of opening the drawer | The drawer's click handler is not winning against Stage's | It must call `stopImmediatePropagation`, not `stopPropagation`: both handlers are bound to `document`, and `stopPropagation` does not stop other listeners on the same node |
| Drawer opens but shows the prototype's demo shell, rule trace and fake site | `embed=1` missing from the iframe URL | The drawer appends it; check the booking page still reads the flag in its `deepLink` block |
| Page switcher covers the prototype's header again | An old `live-edit.js` is cached, or the CSS was reverted | The switcher is docked `bottom:18px`, never the top. Hard reload; check `#stage-pagenav-trigger` exists in the served script |
| Switcher sits over the drawer's Continue button | `body.pm-book-locked #stage-pagenav` rule missing | It lives in `BOOKING_DRAWER_CSS` in `tools/build-microsites.py`; rebuild and redeploy |
| Links dead on every page | `allowNavigation` missing from the manifest | It is emitted by `build-stage-manifest.py`; confirm it survived a hand-edit |
| Booking opens but no treatment selected | `?svc=` id does not match a SERVICES id | Check `BOOKING_SVC` in `tools/build-microsites.py` against the prototype's `SERVICES` list |
| Images broken on Stage only | Asset not copied to `$E/assets/` | Re-run the asset copy in step 5 |
| Manifest build refuses to write | An id would disappear | Intended. Read the list; use `--allow-drop` only for copy you rewrote on purpose |
| A saved copy edit silently disappears from `client-edits.json` a few seconds after being saved (no error shown to the client) | **Known bug, unresolved as of 2026-08-08.** `saveEdits()` in `live-edit-routes.js` does a full read-modify-write of the whole `client-edits.json` file per request, with no locking or merge. Two edits saved close together (e.g. the client tabs quickly between two fields) can race: the request that finishes writing last wins and silently drops whichever field the other one hadn't captured yet. Reproduced during the 2026-08-08 E2E test — a copy edit was present in the submitted digest but gone from disk under a minute later, with no other edit visibly in flight. | No fix applied yet. Workaround: after any editing session, diff `client-edits.json` against what you expect before trusting it, especially after several fast edits. A real fix needs the save handlers to merge into a freshly-read file (or lock) rather than write a full snapshot taken at request-start. This is shared code (`live-edit-routes.js`), so a fix would apply to every live-edit engagement, not just `puremed-micro`. |

Escalation: `web/stage-build/` is generated, so any bad build is fixed by deleting
it and re-running from step 1. The source prototypes in `web/` are never modified.

## Image swapping and the shared asset library

Every image tagged `data-stage-img` (all hero and content photos on all 9 pages)
is swappable in place: click the image, then **Upload new** or **Choose from
library**. This needs no extra wiring per image — `stage-autotag.js` tags every
`<img>` automatically at build time.

**"Choose from library" lists every file physically sitting in
`/home/pi/stage/engagements/puremed-micro/assets/`** — there is no curation/
approval gate on this engagement (that gate exists elsewhere in Stage for a
different, unused review mode). Whatever is in that folder is what any logged-in
user — Nafisa or admin — sees and can place on any page.

- **Current library (set 2026-08-08):** the 148-file curated set from
  `assets/web/` — real photography, chosen hero/treatment shots, before/afters,
  logos — deliberately excluding the ~318 raw multi-model AI generation trial
  batches (`nafisa-NN-*`, `skin-NN-*`, `nafisa-library-*`, `hf_*` dumps) and
  anything named `do-not-use`. Those stay local; pushing them would flood the
  picker with rejected/test renders Nafisa could accidentally put on the site.
- **To add more assets later:** either `scp` additional `.webp` files straight
  into `$E/assets/` on the Pi (no rebuild or redeploy needed — the library reads
  the directory live), or use **Upload new** from any image's panel while
  logged in — that endpoint (`POST /api/client-edits/:engagement/upload`) only
  requires `requireAuth`, not admin, so it works for Nafisa's account too.
  Verified 2026-08-08: a file uploaded through the panel landed in `$E/assets/`
  and immediately appeared in the Library grid for every other image on the
  site, no restart required.

## Submit for publishing (the approval workflow)

The orange **Submit for publishing** pill (bottom-left, appears once there is
at least one unsaved-to-server edit) is the client's send-to-Osman step. It does
**not** publish anything live — `puremed-micro` has no build/deploy target of
its own (see Boundaries). It POSTs to `/api/client-edits/:engagement/submit`,
which:

1. Snapshots the current `copy` / `images` / `repeatables` overlay to
   `output/submissions/NNN.json`.
2. Writes a human-readable `output/submissions/publish-request-NNN.md` digest
   (Was/Now per field) — this is what you read to review the changes.
3. Records `lastSubmission` in `client-edits.json`; the button becomes
   "Resubmit for publishing" with a "Last sent" timestamp. Editing is not
   locked — she can keep going and resubmit any time.

Verified end-to-end 2026-08-08: a copy edit + the pre-existing pending edits
were submitted, produced an accurate digest (`Was`/`Now` correctly diffed,
correct treatment label per field, correct `submittedBy`), and the button state
updated correctly. **Note for testing this flow:** the button's confirm step is
a native `window.confirm()`, which is not just a UI dialog — it blocks the page
entirely, including remote/automated control of the tab, until dismissed. Don't
trigger it site-wide without a way to dismiss it (in a real browser session,
just click OK/Cancel as normal; this only bites headless/remote testing).

## SOP for the live-edit tool itself

This section (and the equivalent one in `SOP-PUREMED-001` §C, for the real
`puremed-site` engagement) *is* the operator SOP for "the edit your site tool."
There is no separate, engagement-agnostic Stage SOP — each engagement's SOP
covers the tool as it applies there, because the publish step differs
(`puremed-site` builds and deploys Astro; `puremed-micro` only notifies you via
a digest, nothing ships).

## Boundaries

- **Nothing here is signed off.** Before/after imagery on these pages is real
  client photography and still needs Nafisa's approval before any of it is used
  publicly or driven traffic.
- The booking journey is a **demonstration prototype**: no payment is taken and
  nothing connects to a live system. Do not present it to a client as live, and
  do not enter real card or medical details.
- Do not set `allowNavigation` on `puremed-site`. That surface blocks links on
  purpose so the client cannot wander off mid-edit.
- Do not tag `booking.html`.
- Nafisa edits **copy and images only**. Structural change is a build-side job.

## Change log

- 2026-08-08: created. Engagement built from the six microsites plus hub, booking
  prototype added as a page with `?svc=` deep-linking, `allowNavigation` added to
  the live-edit surface as an opt-in flag, and `live-edit.js` given an mtime
  cache-buster after a stale copy silently swallowed clicks during verification.
- 2026-08-08 (later still): Stage's page switcher redesigned. It ran full-width across
  the top, where every prototype puts its own header, so it covered the thing being
  reviewed, and long labels wrapped and turned the active pill into a circle. It is now
  docked bottom-centre and collapsed to a single pill naming the current page, opening
  upward on demand, with the active row marked by a rail rather than a filled blob. This
  is shared chrome: `puremed-site` gets the same improvement and was re-checked (links
  still blocked there, as intended).
- 2026-08-08 (later): booking journey embedded as an in-page drawer rather than a
  navigation, using a new `embed=1` mode on the booking prototype that strips it to
  the client-facing journey. Sculptra added as a seventh microsite, rebuilt onto the
  shared template. Both verified on the Pi with two client edits already in the
  overlay, which survived the redeploy.
- 2026-08-08 (later still): fixed the desktop hero image on all 7 treatment pages
  stretching to match the text column's height instead of the viewport (a CSS grid
  `align-items:stretch` default with no explicit height on `.tx-hero-image`) —
  gave it an explicit height plus `align-self:start` on all 7 source files, rebuilt
  and redeployed. Pushed a curated 148-file image library to `$E/assets/` so every
  hero/content photo is swappable via the existing per-image Library picker (no code
  change needed, it already reads the assets directory live). Ran a full E2E pass on
  the live-edit tool: image swap from the new library, admin/client upload adding a
  file to the shared pool, and Submit for publishing end to end (digest generation,
  Was/Now diff, resubmit state) — all verified working, test artifacts cleaned up
  after. Found and documented (not yet fixed) a copy-save race condition that can
  silently drop an edit — see "When it breaks."
