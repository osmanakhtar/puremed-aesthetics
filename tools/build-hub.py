#!/usr/bin/env python3
"""
Build the PureMed treatment microsite review hub.

Pulls each treatment's own hero image straight out of its built page (whether that
hero is a file reference or already base64-embedded), downsizes it to a thumbnail,
and writes a self-contained Artifact fragment to web/publish/_artifact/index.html.

Published URLs for the six microsites are read from tools/microsite-urls.json.

    python3 tools/build-hub.py
"""
import base64
import io
import json
import pathlib
import re
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
OUT = WEB / "publish" / "_artifact"
STAGE_OUT = WEB / "stage-build"
ENGAGEMENT = "puremed-micro"

# stage target writes generated images to disk instead of embedding them
TARGET = "stage" if "--target=stage" in sys.argv else "artifact"
ASSETS = ROOT / "assets" / "web"
FONTS = (ROOT / "tools" / "fonts-inline.css").read_text()
URLS = json.loads((ROOT / "tools" / "microsite-urls.json").read_text())

TREATMENTS = [
    ("puremed-laser-lift", "Laser Lift",
     "Non-surgical skin tightening that lifts and firms using laser energy, with no downtime."),
    ("puremed-liquid-facelift", "Liquid Facelift",
     "Dermal fillers used to restore lost volume and redefine facial contours."),
    ("puremed-anti-wrinkle", "Anti-Wrinkle Injections",
     "Muscle-relaxing injections that soften dynamic lines while preserving natural expression."),
    ("puremed-polynucleotides", "Polynucleotides",
     "Regenerative PNCT treatment that repairs skin quality from the inside out."),
    ("puremed-rf-microneedling", "RF Microneedling",
     "Radiofrequency and microneedling combined to stimulate deep collagen renewal."),
    ("puremed-skin-boosters", "Skin Boosters",
     "Deep hydration that improves texture, firmness and glow across the whole face."),
    ("puremed-sculptra", "Sculptra",
     "A collagen biostimulator that rebuilds facial structure gradually, lasting up to two years."),
]


# per-image vertical crop bias (0 = top of frame, 1 = bottom); default 0.30
BIAS = {"puremed-polynucleotides": 0.16}

# Where a page's own hero is a room/scene shot rather than a portrait, name a
# better card image explicitly (laser-lift's hero-1 is an empty clinic room).
THUMB_OVERRIDE = {"puremed-laser-lift": "assets/web/puremed-laser-lift-hero-4.webp"}


def thumb(slug: str, width: int = 720) -> str:
    """Extract the hero image from a built page and return a downsized data URI."""
    if slug in THUMB_OVERRIDE:
        raw = (ROOT / THUMB_OVERRIDE[slug]).read_bytes()
        return _frame(raw, slug, width)
    html = (WEB / f"{slug}.html").read_text()
    # no slice limit: an embedded base64 hero can run to megabytes
    region = html[html.find('class="tx-hero"'):]
    m = re.search(r'<img[^>]+src="(data:image/[^;]+;base64,([^"]+)|\.\./assets/[^"]+)"', region)
    if not m:
        raise SystemExit(f"no hero image found for {slug}")
    if m.group(2):
        raw = base64.b64decode(m.group(2))
    else:
        raw = (WEB / m.group(1)).resolve().read_bytes()
    return _frame(raw, slug, width)


def _frame(raw: bytes, slug: str, width: int) -> str:
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    # crop straight to the card's 16:10 frame, biased above centre so faces sit in
    # the upper third rather than being cut off by a second crop in CSS
    ratio = 16 / 10
    w, h = im.size
    if w / h > ratio:                     # too wide: trim the sides
        new_w = int(h * ratio)
        left, top, new_h = (w - new_w) // 2, 0, h
    else:                                 # too tall: trim top and bottom
        new_h = int(w / ratio)
        left, top, new_w = 0, int((h - new_h) * BIAS.get(slug, 0.30)), w
    im = im.crop((left, top, left + new_w, top + new_h))
    im = im.resize((width, int(width / ratio)), Image.LANCZOS)
    if TARGET == "stage":
        name = f"hub-thumb-{slug}.webp"
        im.save(ASSETS / name, "WEBP", quality=82, method=6)
        return f"../assets/web/{name}"
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=82, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def img_uri(rel: str, width=None) -> str:
    p = ROOT / rel
    if TARGET == "stage":
        # Stage rewrites src="....webp" to /assets/<engagement>/<basename>, so the
        # hub must reference files for its images to be swappable by the client.
        if width:
            im = Image.open(p)
            im.thumbnail((width, width * 4), Image.LANCZOS)
            name = f"hub-{pathlib.Path(rel).stem}-{width}.webp"
            im.save(ASSETS / name, "WEBP", quality=88, method=6)
            return f"../assets/web/{name}"
        return f"../assets/web/{pathlib.Path(rel).name}"
    if width:
        im = Image.open(p)
        im.thumbnail((width, width * 4), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=88, method=6)
        return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    mime = "image/webp"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


CSS = """
:root{
  --navy:#23476A; --navy-deep:#1B3752; --gold:#C6A77D; --gold-soft:#EDD9BA;
  --white:#FFFFFF; --warm:#F8F8F6; --ink:#1A1A2E; --muted:#6B7280; --line:#E5E7EB;
}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--warm);color:var(--ink);
  font-family:'Inter',system-ui,sans-serif;font-size:16px;line-height:1.6;
  -webkit-font-smoothing:antialiased}
img{max-width:100%;display:block}
a{color:inherit}
.wrap{max-width:1180px;margin:0 auto;padding:0 28px}

.masthead{background:var(--navy);color:var(--white);padding:56px 0 64px}
.masthead-top{display:flex;align-items:center;justify-content:space-between;gap:32px;
  padding-bottom:44px;border-bottom:1px solid rgba(255,255,255,.16)}
.masthead-logo{height:56px;width:auto}
.masthead-meta{font-size:12px;letter-spacing:.14em;text-transform:uppercase;
  color:rgba(255,255,255,.62);text-align:right;line-height:1.9}
.masthead-body{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:56px;
  align-items:end;padding-top:48px}
.eyebrow{display:flex;align-items:center;gap:12px;font-size:11px;letter-spacing:.2em;
  text-transform:uppercase;color:var(--gold);margin-bottom:20px}
.eyebrow::before{content:'';width:34px;height:1px;background:var(--gold)}
.masthead h1{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;
  font-size:clamp(36px,4.6vw,58px);line-height:1.1;margin:0 0 18px;text-wrap:balance}
.masthead h1 em{font-style:italic;color:var(--gold-soft)}
.masthead p{margin:0;color:rgba(255,255,255,.76);max-width:60ch}
.prac-card{display:flex;gap:16px;align-items:center;background:rgba(255,255,255,.07);
  border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:16px}
.prac-card img{width:72px;height:72px;border-radius:8px;object-fit:cover;object-position:50% 18%}
.prac-card strong{display:block;font-family:'Cormorant Garamond',Georgia,serif;
  font-size:21px;font-weight:600;letter-spacing:.01em}
.prac-card span{display:block;font-size:12px;color:rgba(255,255,255,.62);margin-top:3px;line-height:1.5}

.sec{padding:72px 0}
.sec-head{margin-bottom:36px}
.sec-head h2{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;
  font-size:clamp(27px,3vw,38px);color:var(--navy);margin:0 0 10px;text-wrap:balance}
.sec-head p{margin:0;color:var(--muted);max-width:66ch}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(316px,1fr));gap:26px}
.card{display:flex;flex-direction:column;background:var(--white);border:1px solid var(--line);
  border-radius:10px;overflow:hidden;text-decoration:none;
  transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
.card:hover,.card:focus-visible{transform:translateY(-3px);border-color:var(--gold);
  box-shadow:0 18px 44px rgba(35,71,106,.15)}
.card:focus-visible{outline:2px solid var(--navy);outline-offset:3px}
.card-media{aspect-ratio:16/10;overflow:hidden;background:var(--navy)}
.card-media img{width:100%;height:100%;object-fit:cover}
.card-body{padding:24px 24px 26px;display:flex;flex-direction:column;gap:9px;flex:1}
.card-body h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;
  font-size:25px;color:var(--navy);margin:0;line-height:1.2}
.card-body p{margin:0;font-size:14.5px;color:var(--muted);flex:1}
.card-go{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:600;
  letter-spacing:.09em;text-transform:uppercase;color:var(--navy);margin-top:6px}
.card-go svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:1.8;
  transition:transform .22s ease}
.card:hover .card-go svg{transform:translateX(4px)}

.notes{background:var(--white);border-top:1px solid var(--line)}
.note-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:0;
  border:1px solid var(--line);border-radius:10px;overflow:hidden}
.note{padding:26px 28px;border-right:1px solid var(--line);background:var(--white)}
.note:last-child{border-right:none}
.note h4{margin:0 0 8px;font-size:12px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--gold)}
.note p{margin:0;font-size:14.5px;color:var(--muted)}
.note strong{color:var(--ink);font-weight:600}

.foot{background:var(--navy-deep);color:rgba(255,255,255,.68);padding:34px 0;font-size:13px}
.foot .wrap{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
.foot a{color:var(--gold-soft)}

@media(max-width:860px){
  .masthead-body{grid-template-columns:1fr;gap:34px;align-items:start}
  .masthead-top{flex-direction:column;align-items:flex-start;gap:20px}
  .masthead-meta{text-align:left}
  .note{border-right:none;border-bottom:1px solid var(--line)}
  .note:last-child{border-bottom:none}
}
@media(prefers-reduced-motion:reduce){
  *{transition:none!important;animation:none!important}
}
"""

ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

NOTES = [
    ("Imagery", "Every page carries its own hero, treatment and before/after imagery. "
                "Before/after photos are <strong>real client results</strong> and need your sign-off before anything goes public."),
    ("Nafisa", "Each page now ends with a practitioner section using the real clinic photo. "
               "The AI-generated likenesses were <strong>deliberately not used</strong>."),
    ("Still to confirm", "The <strong>500+ Google reviews</strong> figure is still an estimate, and Nafisa's "
                         "credentials line needs checking against what she can evidence."),
]


def link(slug: str) -> str:
    """Artifact build links to published URLs; Stage links to prototype routes."""
    if TARGET == "stage":
        return f"/prototype/{ENGAGEMENT}/{slug}"
    if slug not in URLS:
        raise SystemExit(
            f"no published Artifact URL for {slug}. Publish that page first, then add "
            f"its URL to tools/microsite-urls.json.")
    return URLS[slug]


def main():
    logo = img_uri("assets/web/puremed-logo-trimmed.webp", width=560)
    nafisa = img_uri("assets/web/nafisa-hero-v2.webp", width=220)

    cards = []
    for slug, name, desc in TREATMENTS:
        cards.append(f"""
      <a class="card" href="{link(slug)}">
        <div class="card-media"><img src="{thumb(slug)}" alt="{name} at PureMed Aesthetics"></div>
        <div class="card-body">
          <h3>{name}</h3>
          <p>{desc}</p>
          <span class="card-go">View microsite {ARROW}</span>
        </div>
      </a>""")

    notes = "".join(f'<div class="note"><h4>{h}</h4><p>{b}</p></div>' for h, b in NOTES)

    head_open = "" if TARGET == "artifact" else (
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500'
        '&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">')
    html = f"""{head_open}<title>PureMed Aesthetics — Treatment Microsites</title>
<style>
{FONTS if TARGET == "artifact" else ""}
{CSS}
</style>
{"" if TARGET == "artifact" else "</head><body>"}

<header class="masthead">
  <div class="wrap">
    <div class="masthead-top">
      <img class="masthead-logo" src="{logo}" alt="PureMed Aesthetics">
      <div class="masthead-meta">Treatment microsites<br>For review &middot; August 2026</div>
    </div>
    <div class="masthead-body">
      <div>
        <div class="eyebrow">Seven standalone pages</div>
        <h1>One page per treatment,<br>each able to stand <em>on its own</em>.</h1>
        <p>Every treatment gets a self-contained page that can be linked from an ad, a
           social post or a Google listing without sending anyone through the main site
           first. Same brand, same practitioner, one subject each.</p>
      </div>
      <div class="prac-card">
        <img src="{nafisa}" alt="Nafisa Mughal at the PureMed clinic in Winslow">
        <div>
          <strong>Nafisa Mughal</strong>
          <span>Founder &amp; Lead Practitioner<br>Winslow, Buckinghamshire</span>
        </div>
      </div>
    </div>
  </div>
</header>

<main>
  <section class="sec">
    <div class="wrap">
      <div class="sec-head">
        <h2>The treatments</h2>
        <p>Open any page to review it end to end. Each one runs hero, explanation,
           benefits, suitability, process, FAQs, before and after, Nafisa, and a booking CTA.</p>
      </div>
      <div class="grid">{''.join(cards)}
      </div>
    </div>
  </section>

  <section class="sec notes">
    <div class="wrap">
      <div class="sec-head">
        <h2>What to look at</h2>
        <p>Three things worth a decision before these go anywhere public.</p>
      </div>
      <div class="note-grid">{notes}</div>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap">
    <div>PureMed Aesthetics &middot; 34a High Street, Winslow, MK18 3HB</div>
    <div>{"Bookings via <a href=\"https://facesconsent.com/bookings/puremedaesthetics\">facesconsent.com</a>" if TARGET == "artifact" else f"<a href=\"/prototype/{ENGAGEMENT}/booking\">Open the booking journey</a>"}</div>
  </div>
</footer>
{"" if TARGET == "artifact" else "</body></html>"}
"""
    dest_dir = OUT if TARGET == "artifact" else STAGE_OUT
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "index.html"
    dest.write_text(html)
    print(f"[{TARGET}] hub -> {dest}  {dest.stat().st_size/1048576:.2f} MB")


if __name__ == "__main__":
    main()
