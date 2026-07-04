# PureMed — Footer Template Correction Prompt

Use this prompt to start a fresh session. It contains all the context needed without referencing any prior conversation.

---

## Briefing

You are working on the PureMed Aesthetics WordPress site built in Bricks Builder 2.3.7 on LocalWP. The footer template (ID 15) needs two things:

1. **Add the two missing global elements** — sticky mobile CTA bar and WhatsApp sticky button — which exist in the prototype but are absent from the template
2. **Move footer/CTA/WhatsApp CSS from homepage CSS into the footer template** — same split-CSS issue that was already fixed for the nav template

The site is live locally at `http://localhost:10008` (Host: `puremed.local`). Do not deploy anywhere.

---

## Environment

**Bricks MCP**
- Server: `bricks-mcp-puremed` (in `~/.claude/mcp.json`)
- URL: `http://localhost:10008/wp-json/bricks-mcp/v1/mcp`
- Auth: Basic `UHVyZW1lZC1tc3MtYnVpbGQ6eTBZRkd3ZDdvWVlHWHhONHVBckZ6NkY3`
- Host header required: `puremed.local`

**LocalWP DB**
- MySQL socket: `/Users/osmanakhtar/Library/Application Support/Local/run/pAUkkQGcC/mysql/mysqld.sock`
- MySQL binary: `/Users/osmanakhtar/Library/Application Support/Local/lightning-services/mysql-8.4.0/bin/darwin-arm64/bin/mysql`
- PHP binary: `/Users/osmanakhtar/Library/Application Support/Local/lightning-services/php-8.2.29+0/bin/darwin-arm64/bin/php`
- DB: `local`, user: `root`, pass: `root`

**WordPress**
- AUTH_KEY: `vodJV|O9[6i#wn,J0{X]8.N&3Ch5;3A6T ZV>d=!91HTK fDzYdx[2$%>)p.@~MK`
- AUTH_SALT: `6R5KCAqt+(^P2;Y>0B&NYM0,3cI&K4)h6+.PK^4AL5DC5}U ~7cF=V(MW)apZ*er`
- `wp_hash(data)` = `hash_hmac('md5', data, AUTH_KEY . AUTH_SALT)`

**Source files**
- Prototype: `/Users/osmanakhtar/workspace/other-projects/puremed/web/puremed-homepage-v6.html`
- Homepage CSS source: `/Users/osmanakhtar/workspace/other-projects/puremed/web/puremed-homepage-bricks-ready.html`

---

## Critical bugs — read before touching anything

### Bug 1 — MCP writes to wrong meta key for footer templates

`page:update_content` always writes elements to `_bricks_page_content_2`. But footer templates render from `_bricks_page_footer_2`. After **every** `page:update_content` call on template 15, run this MySQL sync or the changes will be invisible on the frontend:

```sql
DELETE FROM wp_postmeta WHERE post_id=15 AND meta_key='_bricks_page_footer_2';
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
  SELECT 15, '_bricks_page_footer_2', meta_value
  FROM wp_postmeta WHERE post_id=15 AND meta_key='_bricks_page_content_2';
```

Run via PHP:
```php
$pdo = new PDO(
  'mysql:unix_socket=/Users/osmanakhtar/Library/Application Support/Local/run/pAUkkQGcC/mysql/mysqld.sock;dbname=local',
  'root','root'
);
$pdo->exec("DELETE FROM wp_postmeta WHERE post_id=15 AND meta_key='_bricks_page_footer_2'");
$pdo->exec("INSERT INTO wp_postmeta (post_id, meta_key, meta_value) SELECT 15, '_bricks_page_footer_2', meta_value FROM wp_postmeta WHERE post_id=15 AND meta_key='_bricks_page_content_2'");
```

### Bug 2 — Element IDs must be exactly 6 lowercase alphanumeric characters

`/^[a-z0-9]{6}$/` — any violation silently fails the entire `page:update_content` call. Validate all IDs before calling. Before using any new ID, check it doesn't collide with existing element IDs on template 15 or the homepage.

### Bug 3 — MCP truncates large HTML payloads (~2KB)

If any Code element's `code` field is >~2KB (e.g. contains SVG paths), use direct PHP DB write to `_bricks_page_content_2` instead of `page:update_content`, then run the MySQL sync above.

### Bug 4 — Code elements require a signature

Any Code element using the `code` field (HTML) must include `signature = wp_hash(code_content)`. Without it, Bricks renders an empty div.

```python
import hmac, hashlib
AUTH_KEY  = 'vodJV|O9[6i#wn,J0{X]8.N&3Ch5;3A6T ZV>d=!91HTK fDzYdx[2$%>)p.@~MK'
AUTH_SALT = '6R5KCAqt+(^P2;Y>0B&NYM0,3cI&K4)h6+.PK^4AL5DC5}U ~7cF=V(MW)apZ*er'
sig = hmac.new((AUTH_KEY+AUTH_SALT).encode(), html.encode(), hashlib.md5).hexdigest()
```

### Bug 5 — Never edit page CSS by byte position

Always match by CSS selector or comment string. Never use byte offsets. After any edit, verify required selectors are still present. This previously caused a 25KB CSS destruction.

---

## Current state of footer template 15

**37 elements** — footer grid only. No sticky CTA bar, no WhatsApp sticky.

Element tree (id, type, parent, notes):
```
[dfjjpe] section       ROOT
  [uplshu] container   dfjjpe
    [gpisgu] container uplshu        ← footer-grid row
      [uscjdf] container gpisgu      ← brand column
        [chtdtl] heading             "PureMed Aesthetics" (brand name)
        [leiprk] text-basic          "Winslow · Buckinghamshire" (loc tag)
        [hiqdte] text-basic          bio text
        [ttkpur] container           footer-contacts
          [khlhis] text-basic        address link
          [tektti] text-basic        email link
          [uqgprr] text-basic        WhatsApp contact link
        [pdgepr] container           footer-stars row
          [ssqrse] text-basic        5 star SVGs
        [gctrlt] text-basic          "500+ five-star reviews on Google"
      [ietppr] container gpisgu      ← Treatments column
        [iiclek] heading             "Treatments" <h4>
        [rhhsfs..fsrgjh] text-basic  6 treatment links
      [pdgfgd] container gpisgu      ← Clinic column
        [kkdkce] heading             "Clinic" <h4>
        [qreiqu..kjgfde] text-basic  5 clinic links (#about, #results, etc.)
      [rujfgr] container gpisgu      ← Book column
        [tickdf] heading             "Book" <h4>
        [phgsfd..phrhlp] text-basic  3 book links (booking URL, WhatsApp, email)
    [jpddru] container uplshu        ← footer-bottom row
      [pdcpkr] text-basic            copyright text
      [kjjspq] text-basic            location tag

Template CSS (post 15 _bricks_page_settings.customCss):
  @import url("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css");
  (nothing else — footer/CTA/WA CSS is currently in homepage CSS, see below)
```

---

## Footer CSS currently in homepage CSS (post 17)

These three blocks live in post 17's `_bricks_page_settings.customCss` and need to be **moved** to the footer template CSS, then stripped from homepage CSS:

```css
/* -- STICKY MOBILE CTA BAR (global) -- */
.mobile-cta-bar{display:none;position:fixed;bottom:0;left:0;right:0;z-index:150;background:var(--white);border-top:1px solid var(--border);padding:12px 16px;gap:10px;box-shadow:0 -4px 24px rgba(35,71,106,.12)}
.mobile-cta-bar a{flex:1;display:flex;align-items:center;justify-content:center;gap:8px;font-size:14px;font-weight:600;padding:14px 16px;border-radius:6px;text-decoration:none;text-align:center}
.mobile-cta-bar .mcta-primary{background:var(--navy);color:#fff}
.mobile-cta-bar .mcta-whatsapp{background:#25D366;color:#fff}
.mobile-cta-bar svg{width:16px;height:16px;flex-shrink:0}

/* -- WHATSAPP STICKY (global) -- */
.wa-sticky{position:fixed;bottom:88px;right:20px;z-index:200;width:52px;height:52px;border-radius:50%;background:#25D366;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px rgba(37,211,102,.38);text-decoration:none;transition:transform .2s ease,box-shadow .2s ease}
.wa-sticky:hover{transform:scale(1.08);box-shadow:0 6px 30px rgba(37,211,102,.5)}
.wa-sticky svg{width:26px;height:26px;fill:#fff}

/* -- FOOTER (global / footer template) -- */
footer{background:var(--navy);padding:64px 0 36px;color:rgba(255,255,255,.7)}
.footer-grid{display:flex;flex-wrap:wrap;gap:40px;padding-bottom:48px;border-bottom:1px solid rgba(255,255,255,.08)}
.footer-brand{flex:1 1 100%}
.footer-col{flex:1 1 140px}
.footer-brand-name{font-family:'Cormorant Garamond',serif;font-size:22px;color:#fff;text-decoration:none;display:block;margin-bottom:2px}
.footer-loc-tag{font-size:9px;font-weight:700;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);display:block;margin-bottom:16px}
.footer-bio{font-size:13px;line-height:1.75;color:rgba(255,255,255,.46);margin-bottom:20px}
.footer-contacts{display:flex;flex-direction:column;gap:9px}
.footer-contacts a{font-size:13px;color:rgba(255,255,255,.58);text-decoration:none;display:flex;align-items:center;gap:8px;transition:color .2s}
.footer-contacts a:hover{color:#fff}
.footer-contacts svg{width:13px;height:13px;flex-shrink:0;opacity:.58}
.footer-col h4{font-size:9px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.3);margin-bottom:16px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:10px}
.footer-col ul li a{font-size:13px;color:rgba(255,255,255,.58);text-decoration:none;transition:color .2s}
.footer-col ul li a:hover{color:#fff}
.footer-stars{display:flex;gap:3px;margin-top:20px}
.footer-stars svg{width:12px;height:12px;fill:var(--gold)}
.footer-stars-label{font-size:11px;color:rgba(255,255,255,.32);margin-top:5px;line-height:1.5}
.footer-bottom{display:flex;align-items:center;justify-content:space-between;padding-top:24px;gap:16px;flex-wrap:wrap}
.footer-bottom p{font-size:11px;color:rgba(255,255,255,.26)}
.footer-bottom a{color:rgba(255,255,255,.26);text-decoration:none;transition:color .2s}
.footer-bottom a:hover{color:rgba(255,255,255,.5)}
.footer-loc-bottom{font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);font-weight:600}
```

The homepage CSS `/* -- STICKY MOBILE CTA BAR */` comment is at the start of this block. The section ends at `/* -- PAGE SECTIONS */` / `/* -- HERO */`. Strip this block from post 17 the same way nav CSS was stripped: by matching the comment markers, not byte offsets. Verify `.hero{`, `.stats-bar{`, `.treatments{` etc. are still present after stripping.

---

## What to build

### Task 1 — Add sticky mobile CTA bar to footer template

Add these elements to template 15 as siblings of the existing `[dfjjpe]` section (i.e. root-level, parent=`0`):

**Mobile CTA bar** — a `code` element (HTML) since it needs a fixed-position div with SVG icons and `display:none` toggled by the CSS. Content from prototype:

```html
<div class="mobile-cta-bar">
  <a href="https://facesconsent.com/bookings/puremedaesthetics" class="mcta-primary" target="_blank" rel="noopener">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
    Book Consultation
  </a>
  <a href="https://wa.me/447850087025" class="mcta-whatsapp" target="_blank" rel="noopener">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 2C6.477 2 2 6.477 2 12c0 1.89.518 3.66 1.418 5.18L2 22l4.82-1.418A9.978 9.978 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18c-1.687 0-3.27-.467-4.63-1.28l-.332-.196-3.184.937.938-3.185-.196-.332A7.964 7.964 0 014 12c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8z"/></svg>
    WhatsApp
  </a>
</div>
```

### Task 2 — Add WhatsApp sticky button to footer template

Add a second `code` element at root level with this content:

```html
<a href="https://wa.me/447850087025" class="wa-sticky" target="_blank" rel="noopener" aria-label="WhatsApp PureMed Aesthetics">
  <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 2C6.477 2 2 6.477 2 12c0 1.89.518 3.66 1.418 5.18L2 22l4.82-1.418A9.978 9.978 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18c-1.687 0-3.27-.467-4.63-1.28l-.332-.196-3.184.937.938-3.185-.196-.332A7.964 7.964 0 014 12c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8z"/></svg>
</a>
```

### Task 3 — Move footer CSS from homepage to footer template

**Step A:** Add the full CSS block (sticky CTA bar + WhatsApp sticky + footer CSS, shown above) to footer template 15's `_bricks_page_settings.customCss` via `code:set_page_css`. Prepend it after the FA import so the existing `@import` line is preserved.

**Step B:** Strip those three comment-delimited blocks from post 17's `_bricks_page_settings.customCss` by matching the comment markers `/* -- STICKY MOBILE CTA BAR */` through the end of the footer block, ending just before `/* -- PAGE SECTIONS */` or `/* -- HERO */`. Use exact string replacement, not byte offsets.

**Step C:** After stripping, verify post 17 still contains: `.hero{`, `.stats-bar{`, `.treatments{`, `.why{`, `.results{`, `.reviews{`, `.process{`, `.faq{`, `.final-cta{`

---

## Build order

1. Read current template 15 elements from `_bricks_page_footer_2` to confirm existing IDs (avoid collisions)
2. Add new Code elements (CTA bar + WA sticky) via `page:update_content` — include signature for each
3. Run the MySQL sync for `_bricks_page_footer_2`
4. Move the footer CSS block (Task 3)
5. Curl the rendered page and verify:
   - `.mobile-cta-bar{` appears once in the CSS (from footer template, not homepage)
   - `.wa-sticky{` appears once
   - `footer{` appears once
   - All 9 homepage section selectors still present

---

## Decisions log

`/Users/osmanakhtar/workspace/other-projects/puremed/decisions-log.md` — update DEC-001 to note that the same fix was applied to the footer CSS as part of this session. DEC-002 and DEC-003 remain open.
