---
project: main-stage-studio
status: live
next: "Work the OPEN section. Superseded for brand and strategy by .claude/puremed-decisions-log.md"
blocked_on: ""
owner: osman
---

# PureMed Decisions Log

Items that need a decision or carry architectural risk. Each entry has enough context to understand the root cause without referring back to session transcripts.

---

## OPEN

---

### DEC-001 — Nav CSS is split across two locations (fragile)

**Status:** Resolved 2026-06-21  
**Raised:** 2026-06-21

**Root cause:**  
The source HTML `puremed-homepage-bricks-ready.html` includes a full nav CSS block (`.nav-links`, `.nav-dropdown`, `.nav-inner`, `.nav-actions`, etc.) in its `<style>` tag. When that HTML was used to populate the homepage `customCss` (post 17, `_bricks_page_settings`), the nav CSS came with it. The nav template (template 71) also has its own CSS via `code:set_page_css`.

Bricks loads page CSS before template CSS in the rendered `<style>` block. The homepage nav rules therefore appeared first and took precedence — the template nav overrides only worked because they carried `!important`.

**Resolution (Option A):**  
Stripped all nav CSS from homepage `customCss` in three passes:
1. Entire `/* -- NAV ... */` + `/* -- MOBILE MENU ... */` block (3528 chars, pos 4216–7744)
2. Four nav rules from `@media(max-width:900px)` (kept `.mobile-cta-bar` and `footer` lines)
3. TIER 3 nav pseudo-element / scroll-shadow / hamburger-morph rules

Homepage CSS reduced from 29383 → 24483 chars. Template 71 already contained all these rules in updated form. Verified: `left:50%` gone from rendered page, all 9 section selectors intact. The `!important` in template 71 now only overrides Bricks' own container defaults (width:1100px), not homepage CSS.

**Further fix applied 2026-06-21 (footer template):**  
Same CSS isolation fix applied to footer template (template 15). The `/* -- STICKY MOBILE CTA BAR */`, `/* -- WHATSAPP STICKY */`, and `/* -- FOOTER */` blocks (3343 chars) — plus the `@media(max-width:900px)` responsive rules for `.mobile-cta-bar` and `footer` — were stripped from homepage `customCss` and added to footer template 15's `customCss`. Two Code elements (`mctbar` — mobile CTA bar, `wastky` — WhatsApp sticky) were also added to template 15 as root-level elements. Homepage CSS reduced from 24483 → 21051 chars. Verified: all three selectors appear exactly once in rendered output, all 9 section selectors intact. Template CSS isolation is now complete for both nav (71) and footer (15).

---

### DEC-002 — Bricks MCP `save_elements()` bug forces MySQL workaround for header templates

**Status:** Open  
**Raised:** 2026-06-21

**Root cause:**  
In Bricks MCP ≤2.3.7, `BricksService.php::save_elements()` (line 192) always writes to `_bricks_page_content_2` regardless of template type. But `get_elements()` routes by template type: headers read from `_bricks_page_header_2`, footers from `_bricks_page_footer_2`. The two methods call different keys.

This means any `page:update_content` call on template 71 (header) writes to the wrong meta key — the elements are stored but never render. The frontend sees the old header until a manual MySQL sync copies from `_bricks_page_content_2` to `_bricks_page_header_2`.

**Problem to solve:**  
Every future header edit (adding elements, updating nav links, etc.) requires running the MySQL sync script. This is easy to forget. If forgotten, the header appears unchanged even though the MCP call succeeded.

**Options to consider:**  
A. Patch `BricksService.php::save_elements()` to call `resolve_elements_meta_key()` instead of `self::META_KEY`. One-line fix; will be overwritten on plugin updates.  
B. Continue with the MySQL sync step (documented in memory); add it to any build script that touches template 71.  
C. Check if a newer Bricks MCP version fixes this before next header edit.

**Affected file:** `/Users/osmanakhtar/Local Sites/puremed/app/public/wp-content/plugins/bricks-mcp/includes/MCP/Services/BricksService.php` — line 192.  
**Sync SQL:**
```sql
DELETE FROM wp_postmeta WHERE post_id=71 AND meta_key='_bricks_page_header_2';
INSERT INTO wp_postmeta (post_id, meta_key, meta_value)
  SELECT 71, '_bricks_page_header_2', meta_value
  FROM wp_postmeta WHERE post_id=71 AND meta_key='_bricks_page_content_2';
```

---

### DEC-003 — Bricks MCP silently truncates large HTML payloads (~2KB limit)

**Status:** Open  
**Raised:** 2026-06-21

**Root cause:**  
The Bricks MCP `page:update_content` action silently truncates code element `code` field content when the HTML string exceeds ~2KB. Elements with inline SVG paths (WhatsApp icon, calendar icon) were confirmed cut mid-string. The MCP reports success (`element_count: N`) but the stored content is shorter than what was sent.

All 9 homepage sections were written via direct PHP DB write to `_bricks_page_content_2` as a workaround. The PHP script bypasses the MCP entirely and uses the LocalWP MySQL socket.

**Problem to solve:**  
Any future homepage section update must use the same PHP direct write approach. If someone uses `page:update_content` to update a section (e.g., to change a treatment card), the content will be truncated and the section will break.

**Options to consider:**  
A. Patch the Bricks MCP plugin to handle larger payloads (chunked transfer or increased limit).  
B. Keep using the PHP direct write script (`/tmp/build_puremed_direct.php`) for all homepage section updates. Requires knowing the pattern and having MySQL access.  
C. Rebuild homepage sections using native Bricks elements (Section > Container > content) rather than Code elements with large HTML — removes the truncation risk but requires significant rework and departs from the prototype design.

**Current state:** Option B in place. Build script at `/tmp/build_puremed_direct.php`.

---

## RESOLVED

- **DEC-001** (2026-06-21) — Nav CSS + footer/CTA/WA CSS stripped from homepage; templates 71 and 15 are now sole sources of their respective styles.
