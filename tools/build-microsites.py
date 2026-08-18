#!/usr/bin/env python3
"""
Build standalone, self-contained PureMed treatment microsites from the web/ prototypes.

Each output page is a single HTML file with fonts and images inlined as data URIs,
so it can be published anywhere (including CSP-restricted hosts) with no external
requests. Run from the puremed project root:

    python3 tools/build-microsites.py

Source pages are never modified; everything is written to web/publish/.
"""
import base64
import mimetypes
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
OUT = WEB / "publish"
STAGE_OUT = WEB / "stage-build"
ENGAGEMENT = "puremed-micro"

# Which booking-prototype service each treatment page should deep-link into.
# Ids are the SERVICES ids in booking-engine/prototype/_internal-puremed-v1.0.html.
BOOKING_SVC = {
    "puremed-anti-wrinkle": "btx-1",
    "puremed-laser-lift": "laser-lift",
    "puremed-liquid-facelift": "liquid-facelift",
    "puremed-polynucleotides": "polynucleotides",
    "puremed-rf-microneedling": "rf-microneedling",
    "puremed-skin-boosters": "skin-boosters",
    "puremed-sculptra": "sculptra",
}
FONTS = (ROOT / "tools" / "fonts-inline.css").read_text()

# Canonical brand navy. The decisions log records #0B1F3A as explicitly rejected
# ("too dark", Nafisa's direct feedback); #23476A from the requirements doc wins.
BRAND_NAVY = "#23476A"
REJECTED_NAVY = {"#0B1F3A": BRAND_NAVY, "#122A4D": "#2D5B88", "#E4EAF1": "#E8EFF5"}

BOOKING = "https://facesconsent.com/bookings/puremedaesthetics"

PAGES = [
    ("puremed-anti-wrinkle", "Anti-Wrinkle Injections"),
    ("puremed-laser-lift", "Laser Lift"),
    ("puremed-liquid-facelift", "Liquid Facelift"),
    ("puremed-polynucleotides", "Polynucleotides"),
    ("puremed-rf-microneedling", "RF Microneedling"),
    ("puremed-skin-boosters", "Skin Boosters"),
    ("puremed-sculptra", "Sculptra"),
]


BOOKING_DRAWER_CSS = """
/* --- Embedded booking journey (Stage build only) --- */
.pm-book{position:fixed;inset:0;z-index:2000;display:none}
.pm-book.is-open{display:block}
.pm-book-veil{position:absolute;inset:0;background:rgba(16,28,42,.55);
  opacity:0;transition:opacity .3s ease}
.pm-book.is-open .pm-book-veil{opacity:1}
.pm-book-panel{position:absolute;top:0;right:0;height:100%;width:min(760px,100%);
  background:var(--warm-white);display:flex;flex-direction:column;
  box-shadow:-24px 0 70px rgba(16,28,42,.32);
  transform:translateX(100%);transition:transform .34s cubic-bezier(.22,.61,.36,1)}
.pm-book.is-open .pm-book-panel{transform:none}
.pm-book-head{flex-shrink:0;background:var(--navy);color:#fff;
  padding:16px 20px;display:flex;align-items:center;gap:16px}
.pm-book-head h2{margin:0;font-family:'Cormorant Garamond',Georgia,serif;
  font-size:21px;font-weight:500;line-height:1.2;flex:1}
.pm-book-head p{margin:3px 0 0;font-size:11.5px;line-height:1.45;
  color:rgba(255,255,255,.66);font-family:'Inter',sans-serif}
.pm-book-close{flex-shrink:0;width:34px;height:34px;border-radius:50%;
  border:1px solid rgba(255,255,255,.28);background:transparent;color:#fff;
  font-size:19px;line-height:1;cursor:pointer;transition:background .2s}
.pm-book-close:hover{background:rgba(255,255,255,.14)}
.pm-book-close:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
.pm-book-frame{flex:1;border:0;width:100%;background:var(--warm-white)}
body.pm-book-locked{overflow:hidden}
/* Stage's page switcher is docked bottom-centre, where it would sit over this
   drawer's Continue button. Hide it while the drawer is open; the drawer is a
   focused state and the switcher is one Escape away. */
body.pm-book-locked #stage-pagenav{opacity:0;pointer-events:none;transition:opacity .2s}
@media(max-width:600px){.pm-book-head h2{font-size:18px}}
@media(prefers-reduced-motion:reduce){
  .pm-book-panel,.pm-book-veil{transition:none}
}
"""

BOOKING_DRAWER_HTML = """
<!-- EMBEDDED BOOKING JOURNEY -->
<div class="pm-book" id="pm-book" hidden>
  <div class="pm-book-veil" data-book-close></div>
  <div class="pm-book-panel" role="dialog" aria-modal="true" aria-label="Book an appointment">
    <div class="pm-book-head">
      <div>
        <h2>Book your appointment</h2>
        <p>Demonstration of the booking journey. No payment is taken and nothing is sent.</p>
      </div>
      <button class="pm-book-close" type="button" data-book-close aria-label="Close booking">&times;</button>
    </div>
    <iframe class="pm-book-frame" id="pm-book-frame" title="Booking journey" src="about:blank"></iframe>
  </div>
</div>
<script>
/* The booking journey opens over the page instead of navigating away, so the
   treatment being sold stays behind it. The CTA keeps a real href, so if this
   script never runs the link still works: the drawer is an enhancement, not the
   only route. The iframe src is set on first open, never at page load. */
(function(){
  var BOOK = "__BOOKING_URL__";
  var root = document.getElementById("pm-book");
  var frame = document.getElementById("pm-book-frame");
  var lastFocus = null;
  if(!root || !frame) return;


  function open(url){
    lastFocus = document.activeElement;
    if(frame.getAttribute("src") !== url) frame.setAttribute("src", url);
    root.hidden = false;
    document.body.classList.add("pm-book-locked");
    requestAnimationFrame(function(){ root.classList.add("is-open"); });
    root.querySelector(".pm-book-close").focus();
  }
  function close(){
    root.classList.remove("is-open");
    document.body.classList.remove("pm-book-locked");
    setTimeout(function(){ root.hidden = true; }, 340);
    if(lastFocus && lastFocus.focus) lastFocus.focus();
  }

  /* Capture phase, registered while the document is still parsing, so this runs
     before Stage's live-edit click handler and can stop it swallowing the click. */
  document.addEventListener("click", function(ev){
    var a = ev.target.closest && ev.target.closest('a[href*="/booking"]');
    if(!a || ev.altKey || ev.metaKey || ev.ctrlKey || ev.shiftKey) return;
    ev.preventDefault();
    /* stopImmediatePropagation, not stopPropagation: Stage's live-edit handler is
       bound to document too, and stopPropagation does not stop other listeners on
       the same node, so it would still navigate away underneath the drawer. */
    ev.stopImmediatePropagation();
    var href = a.getAttribute("href") || BOOK;
    open(href + (href.indexOf("?") === -1 ? "?" : "&") + "embed=1");
  }, true);

  root.addEventListener("click", function(ev){
    if(ev.target.closest("[data-book-close]")) close();
  });
  document.addEventListener("keydown", function(ev){
    if(ev.key === "Escape" && !root.hidden) close();
  });
})();
</script>
"""

# ---------------------------------------------------------------- practitioner

PRACTITIONER_CSS = """
/* --- Practitioner section (added for standalone microsites) --- */
.pm-prac{padding:var(--sp) 0;background:var(--warm-white);border-top:1px solid var(--border)}
.pm-prac-inner{max-width:1200px;margin:0 auto;padding:0 24px;display:grid;
  grid-template-columns:minmax(0,420px) minmax(0,1fr);gap:64px;align-items:center}
.pm-prac-media{position:relative}
.pm-prac-media img{width:100%;border-radius:10px;display:block;
  box-shadow:0 24px 60px rgba(35,71,106,.18)}
.pm-prac-badge{position:absolute;right:-18px;bottom:28px;background:var(--white);
  border:1px solid var(--border);border-radius:8px;padding:14px 18px;
  box-shadow:0 12px 32px rgba(35,71,106,.14);text-align:center}
.pm-prac-badge strong{display:block;font-family:'Cormorant Garamond',serif;
  font-size:30px;line-height:1;color:var(--navy);font-weight:600}
.pm-prac-badge span{display:block;font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--mid-grey);margin-top:5px}
.pm-prac-eyebrow{display:flex;align-items:center;gap:12px;font-size:11px;
  letter-spacing:.18em;text-transform:uppercase;color:var(--gold);margin-bottom:18px}
.pm-prac-eyebrow::before{content:'';width:32px;height:1px;background:var(--gold)}
.pm-prac h2{font-family:'Cormorant Garamond',serif;font-size:clamp(30px,3.4vw,44px);
  line-height:1.15;font-weight:500;color:var(--navy);margin:0 0 6px}
.pm-prac h2 em{font-style:italic;color:var(--gold)}
.pm-prac-role{font-size:13px;letter-spacing:.06em;color:var(--mid-grey);margin-bottom:22px}
.pm-prac p{color:var(--mid-grey);margin:0 0 16px;max-width:56ch}
.pm-prac-creds{list-style:none;padding:0;margin:26px 0 30px;display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 24px}
.pm-prac-creds li{display:flex;gap:10px;align-items:flex-start;font-size:14px;
  color:var(--near-black)}
.pm-prac-creds svg{flex-shrink:0;width:17px;height:17px;margin-top:2px;
  fill:var(--navy)}
@media(max-width:900px){
  .pm-prac-inner{grid-template-columns:1fr;gap:36px}
  .pm-prac-media{max-width:400px}
  .pm-prac-badge{right:auto;left:20px;bottom:-16px}
  .pm-prac-creds{grid-template-columns:1fr}
}
"""

TICK = ('<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 0a10 10 0 100 20'
        'A10 10 0 0010 0zm-1.2 14.6l-4-4 1.4-1.4 2.6 2.6 5.6-5.6L15.8 7l-7 7.6z"/></svg>')

CREDS = [
    "15 years in medical aesthetics",
    "Independent prescriber",
    "Fully insured and CQC-aligned",
    "Every plan led by consultation",
]


def practitioner_html(logo_uri, nafisa_uri, treatment, booking_href=BOOKING):
    creds = "".join(f"<li>{TICK}<span>{c}</span></li>" for c in CREDS)
    return f"""
<!-- PRACTITIONER -->
<section class="pm-prac" id="about">
  <div class="pm-prac-inner">
    <div class="pm-prac-media">
      <img src="{nafisa_uri}" alt="Nafisa Mughal, aesthetic practitioner and founder of PureMed Aesthetics, at the Winslow clinic" loading="lazy">
      <div class="pm-prac-badge"><strong>15</strong><span>Years' experience</span></div>
    </div>
    <div class="pm-prac-body">
      <div class="pm-prac-eyebrow">Your practitioner</div>
      <h2>Treated by <em>Nafisa</em>, not by a chain.</h2>
      <div class="pm-prac-role">Nafisa Mughal &middot; Founder &amp; Lead Practitioner, PureMed Aesthetics</div>
      <p>PureMed is a medically-led clinic in Winslow. Every {treatment.lower()} consultation,
         plan and treatment is carried out by Nafisa herself, so the person assessing your
         face is the same person treating it, and the same person you see at review.</p>
      <p>Her approach is deliberately conservative: if a treatment is not right for you,
         she will tell you. The aim is always to look rested and like yourself, never done.</p>
      <ul class="pm-prac-creds">{creds}</ul>
      <a href="{booking_href}" class="btn-primary" target="_blank" rel="noopener">Book a Consultation with Nafisa</a>
    </div>
  </div>
</section>
"""


# ------------------------------------------------------------------- inlining

_asset_cache = {}


def data_uri(path: pathlib.Path):
    key = str(path)
    if key not in _asset_cache:
        mime = mimetypes.guess_type(path.name)[0] or "image/webp"
        b64 = base64.b64encode(path.read_bytes()).decode()
        _asset_cache[key] = f"data:{mime};base64,{b64}"
    return _asset_cache[key]


def inline_assets(html: str, base: pathlib.Path):
    """Replace every ../assets/... reference with a data URI."""
    missing = []

    def repl(m):
        prefix, raw = m.group(1), m.group(2)
        p = (base / raw).resolve()
        if not p.is_file():
            missing.append(raw)
            return m.group(0)
        return f"{prefix}{data_uri(p)}"

    html = re.sub(r'((?:src|href)=")(\.\./assets/[^"]+)"', lambda m: repl(m) + '"', html)
    html = re.sub(r'(url\()(\.\./assets/[^)"\']+)', repl, html)
    return html, missing


def extract_embedded(html: str, slug: str):
    """Write any base64-embedded image out to assets/web/ and reference it by file.

    Stage rewrites src="....webp" to /assets/<engagement>/<basename> and its image
    picker works on files, so an inline data URI would be invisible to the editor.
    Two source pages (rf-microneedling, skin-boosters) ship embedded heroes.
    """
    out_dir = ROOT / "assets" / "web"
    n = [0]

    def repl(m):
        prefix, mime, b64 = m.group(1), m.group(2), m.group(3)
        ext = {"jpeg": "jpg", "jpg": "jpg", "png": "png", "webp": "webp"}.get(mime, mime)
        n[0] += 1
        name = f"{slug}-embedded-{n[0]}.{ext}"
        path = out_dir / name
        if not path.exists():
            path.write_bytes(base64.b64decode(b64))
        return f'{prefix}../assets/web/{name}"'

    html = re.sub(r'(src=")data:image/([a-z]+);base64,([A-Za-z0-9+/=]+)"', repl, html)
    return html, n[0]


# --------------------------------------------------------------------- build

def build_page(slug: str, label: str, logo_uri: str, nafisa_uri: str,
               target: str = "artifact"):
    src = WEB / f"{slug}.html"
    html = src.read_text()
    notes = []

    # 1. Brand navy correction (laser-lift shipped the rejected dark navy)
    for bad, good in REJECTED_NAVY.items():
        if bad.lower() in html.lower():
            html = re.sub(re.escape(bad), good, html, flags=re.I)
            notes.append(f"navy {bad}->{good}")

    # 2. Anchor IDs so in-page nav works standalone
    for cls, anchor in (("faq-sec", "faq"), ("faq", "faq"), ("ba", "results"),
                        ("related", "related")):
        html = re.sub(rf'<section class="{cls}"(?![^>]*\bid=)',
                      f'<section id="{anchor}" class="{cls}"', html, count=1)
    # before/after block is a comment-marked section on most pages
    html = html.replace("<!-- BEFORE & AFTER -->", '<!-- BEFORE & AFTER --><a id="results"></a>', 1)

    # 3. Rewrite dead cross-page links (homepage v3/v5/v6 never existed here)
    html = re.sub(r'href="puremed-homepage-v\d\.html#(about|results|faq|treatments|reviews)"',
                  lambda m: f'href="#{ {"treatments":"related","reviews":"results"}.get(m.group(1), m.group(1)) }"',
                  html)
    html = re.sub(r'href="puremed-homepage-v\d\.html"', 'href="index.html"', html)

    if target == "stage":
        # Cross-page links become Stage prototype routes, and every booking CTA
        # deep-links into the booking prototype carrying this page's treatment.
        html = re.sub(r'href="(puremed-[a-z-]+)\.html"',
                      rf'href="/prototype/{ENGAGEMENT}/\1"', html)
        html = html.replace('href="index.html"', f'href="/prototype/{ENGAGEMENT}/index"')
        svc = BOOKING_SVC[slug]
        html = re.sub(r'href="https://facesconsent\.com/[^"]*"',
                      f'href="/prototype/{ENGAGEMENT}/booking?svc={svc}"', html)
        notes.append(f"booking->{svc}")

    # 3b. Sculptra joined the set after these pages were written, so its links are
    #     added at build time rather than hand-editing the nav in every source file.
    if 'href="puremed-sculptra.html"' not in html:
        html = html.replace(
            '<a href="puremed-skin-boosters.html">Skin Boosters</a>',
            '<a href="puremed-skin-boosters.html">Skin Boosters</a>\n'
            '<a href="puremed-sculptra.html">Sculptra</a>')
        html = html.replace(
            '<li><a href="puremed-skin-boosters.html">Skin Boosters</a></li>',
            '<li><a href="puremed-skin-boosters.html">Skin Boosters</a></li>\n'
            '<li><a href="puremed-sculptra.html">Sculptra</a></li>')
        notes.append("sculptra nav")
    # the dropdown bolds whichever treatment you are on
    if slug == "puremed-sculptra":
        html = html.replace(
            '<a href="puremed-sculptra.html">Sculptra</a>',
            '<a href="puremed-sculptra.html" style="font-weight:600;color:var(--navy)">Sculptra</a>', 1)

    # 4. Trimmed logo
    html = html.replace("../assets/web/puremed_logo_transparent.webp",
                        "../assets/web/puremed-logo-trimmed.webp")

    # 5. Practitioner section, before the "related treatments" block
    booking_href = (f"/prototype/{ENGAGEMENT}/booking?svc={BOOKING_SVC[slug]}"
                    if target == "stage" else BOOKING)
    prac = practitioner_html(logo_uri, nafisa_uri, label, booking_href)
    m = re.search(r'<section id="related" class="related"', html)
    if not m:
        m = re.search(r'<section class="related"', html)
    if m:
        html = html[:m.start()] + prac + html[m.start():]
        notes.append("practitioner added")
    else:
        notes.append("!! no insertion point")

    if target == "stage":
        # after the practitioner section is in place, so its CTA is covered too
        html = re.sub(r'\s(target="_blank"|rel="noopener")(?=[\s>])', "", html)
        drawer = BOOKING_DRAWER_HTML.replace(
            "__BOOKING_URL__", f"/prototype/{ENGAGEMENT}/booking?svc={BOOKING_SVC[slug]}")
        html = html.replace("</body>", drawer + "</body>", 1)
        html = html.replace("</style>", BOOKING_DRAWER_CSS + "\n</style>", 1)
        notes.append("booking drawer")

    # 6. Practitioner CSS. Fonts are inlined only for the Artifact target, whose
    #    CSP blocks font CDNs; Stage serves over plain HTTP and can fetch them.
    html = html.replace("</style>", PRACTITIONER_CSS + "\n</style>", 1)
    if target == "artifact":
        html = re.sub(r'<link[^>]+fonts\.googleapis\.com[^>]*>', '', html)
        html = re.sub(r'<link[^>]+fonts\.gstatic\.com[^>]*>', '', html)
        html = re.sub(r'<link rel="preconnect"[^>]*>', '', html)
        html = html.replace("<style>", "<style>\n" + FONTS + "\n", 1)

    # 7. Images: inlined for Artifact, left as files for Stage so they stay editable
    if target == "artifact":
        html, missing = inline_assets(html, WEB)
        if missing:
            notes.append("MISSING:" + ",".join(sorted(set(missing))[:3]))
    else:
        html, n = extract_embedded(html, slug)
        if n:
            notes.append(f"extracted {n} embedded img")

    dest = (OUT if target == "artifact" else STAGE_OUT) / f"{slug}.html"
    dest.write_text(html)
    return dest, notes


def main():
    target = "stage" if "--target=stage" in sys.argv else "artifact"
    dest_dir = OUT if target == "artifact" else STAGE_OUT
    dest_dir.mkdir(parents=True, exist_ok=True)
    print(f"target: {target} -> {dest_dir.relative_to(ROOT)}")
    if target == "artifact":
        logo_uri = data_uri(ROOT / "assets/web/puremed-logo-trimmed.webp")
        nafisa_uri = data_uri(ROOT / "assets/web/nafisa-hero-v2.webp")
    else:
        logo_uri = "../assets/web/puremed-logo-trimmed.webp"
        nafisa_uri = "../assets/web/nafisa-hero-v2.webp"

    for slug, label in PAGES:
        dest, notes = build_page(slug, label, logo_uri, nafisa_uri, target)
        size = dest.stat().st_size / 1_048_576
        flag = "!!" if any(n.startswith(("!!", "MISSING")) for n in notes) else "ok"
        print(f"[{flag}] {dest.name:38s} {size:6.2f} MB   {'; '.join(notes)}")


if __name__ == "__main__":
    sys.exit(main())
