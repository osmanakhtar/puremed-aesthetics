# SOP-PUREMED-001: PureMed live-edit website surface

| | |
|---|---|
| **Purpose** | Keep the surface Nafisa edits her own website on working, current, and safe to regenerate |
| **Operator** | Osman (client side: Nafisa) |
| **Verified** | 2026-07-21 (every step below run as written) |
| **Systems touched** | Stage on the Pi (`pi@192.168.1.106`, pm2 app `stage`, nginx), Astro source at `other-projects/puremed/site`, Loop 1 / Loop 2 / `mss-review.js` |
| **Canon doc** | `other-projects/puremed/stage-client-autonomy-plan.md` |

## When this runs

- **Regeneration**: any time the Astro source changes and Nafisa needs to see it
  (new sections, copy fixes, design changes).
- **Publish**: on an ntfy ping saying she submitted changes.
- **Diagnosis**: whenever she reports the editor misbehaving.

The engagement she edits is **`puremed-site`**. The older `puremed` engagement is
the retired hand-made prototype: it still exists, and anything she does there
(including its "add section" box) goes nowhere. Point her at `puremed-site` only.

## Prerequisites

- SSH key access to the Pi as `pi` (passwordless sudo available there).
- Node + the repo at `~/workspace`; Astro deps installed in `site/`.
- Her login is `nafisa` in `/home/pi/stage/config/users.json`, scoped to
  `puremed`, `puremed-content`, `puremed-site`. Never store passwords here.

## Routine operation

### A. Regenerate the editing surface after changing the Astro source

Her unsubmitted edits live in an overlay keyed by `data-stage-id`. Regeneration is
only safe because ids are never renamed. Run in order:

1. Tag any new elements (insertion-only, existing ids untouched):
   ```
   node scripts/stage-autotag.js --dry-run     # review the counts
   node scripts/stage-autotag.js
   ```
2. Rebuild the manifest. It **refuses to write** if any existing copy id would
   disappear, which is the guard that protects her edits:
   ```
   node scripts/stage-build-manifest.js \
     --out /tmp/manifest.json \
     --base <(ssh pi@192.168.1.106 cat /home/pi/stage/engagements/puremed-site/manifest.json)
   ```
   If it refuses, STOP and find out which ids moved. Do not force it.
3. Build and deploy:
   ```
   cd other-projects/puremed/site && npx astro build
   PI=pi@192.168.1.106; E=/home/pi/stage/engagements/puremed-site
   ssh $PI "cd $E && cp manifest.json manifest.json.bak-$(date +%Y%m%d-%H%M%S) && cp output/client-edits.json output/client-edits.json.bak-$(date +%Y%m%d-%H%M%S)"
   scp dist/index.html $PI:$E/prototype/index.html
   scp dist/treatments/index.html $PI:$E/prototype/treatments.html
   scp /tmp/manifest.json $PI:$E/manifest.json
   ```
   Any NEW image referenced by the source must also be copied to
   `$E/assets/` (the Pi serves `/assets/<engagement>/<basename>`).
4. Confirm zero stranded edits (must print `0`):
   ```
   ssh $PI 'cd /home/pi/stage && node -e "
   const m=require(\"./engagements/puremed-site/manifest.json\");
   const ed=require(\"./engagements/puremed-site/output/client-edits.json\");
   const c=new Set(m.copy.sections.map(s=>s.id)), i=new Set(m.images.fields.map(f=>f.id));
   console.log(Object.keys(ed.copy).filter(k=>!c.has(k)).length + Object.keys(ed.images).filter(k=>!i.has(k)).length);"'
   ```

### B. Let her add a new item type ("+ Add …")

1. In the Astro source, put `data-stage-region="<id>"` on the container whose
   element children are the repeating items. Each item must contain at least one
   `data-stage-id` or `data-stage-img`.
2. Add a label and max to `REGION_META` in `scripts/stage-build-manifest.js`
   (the label is the button text: `treatment section` gives "+ Add treatment
   section").
3. Re-run section A. Check the manifest build output lists the new region.

### C. Publish what she submits

Unchanged from Phase 2b: **ntfy ping arrives with the branch already built**, then
```
node ~/workspace/scripts/mss-review.js
```
and answer the y/N prompts (digest, diff, merge, push/staging, Pi baseline
redeploy + overlay prune, delete branch). Read the diff: added items appear as
plain cloned markup with `__c<n>` ids, and that diff is the compliance gate for
medical claims.

## Checks

- `ssh pi@192.168.1.106 'pm2 list'` shows `stage` **online**.
- Open `https://mss-review.duckdns.org/prototype/puremed-site` as an admin: the
  page-switcher pill sits top-centre, text outlines on hover, and each repeatable
  region has a dashed "+ Add …" button under it.
- Her saved work: `client-edits.json` copy/image counts should only ever grow
  between publishes, never drop unexpectedly.

## When it breaks

| Symptom | Likely cause | Fix |
|---|---|---|
| Image upload fails on anything but tiny files | nginx `client_max_body_size` (default 1MB) rejecting before Node | `/etc/nginx/sites-available/stage` must contain `client_max_body_size 20M;` then `sudo nginx -t && sudo systemctl reload nginx` |
| "Upload not available (multer not installed)" | Pi deps missing after a rebuild | `ssh pi@… 'cd /home/pi/stage && npm install multer sharp && pm2 restart stage'` |
| Her edits vanished from the page | surface regenerated with renamed ids | restore `manifest.json.bak-*` / `client-edits.json.bak-*`, then redo section A properly |
| "+ Add" button missing on a region | region attribute lost in an edit, or the manifest was not rebuilt | check `data-stage-region` in the source, re-run section A |
| A clone shows another item's wording | the template item (first child) was itself edited and the browser cached it | reload the page; clones always derive from the pristine template |
| Client says content is missing that she can see elsewhere | she is looking at the retired `puremed` engagement | point her at `puremed-site`; port the missing content into the Astro source |

Escalation: the plan doc §7 records the 18-21 Jul feedback round and the failure
modes it exposed. Rollback for any Pi-side patch is the `.bak` file beside it plus
`pm2 restart stage`.

## Boundaries

- Never edit `client-edits.json` by hand to "fix" content. It is her work.
- Never regenerate the surface without the section A step 4 check passing.
- Nothing here publishes to production. "Published" ends at the Cloudways staging
  URL until the Framer domain migration; Osman decides what goes further.
- The clone approach copies the template's links and alt text. Check both in the
  publish diff before merging.

## Change log

- 2026-07-21: created, covering Phases 0-4 (inline editing, images, submit/publish
  loop, repeatable items) plus the nginx upload fix.
