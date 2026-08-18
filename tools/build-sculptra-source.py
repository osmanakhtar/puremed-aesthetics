#!/usr/bin/env python3
"""
Generate web/puremed-sculptra.html: the Sculptra landing page rebuilt on the shared
treatment-microsite template.

The original standalone Sculptra page (web/sculptra landing page/) carries its own
stylesheet, announcement bar and text "P" brand mark, so it did not sit with the
other six. Rather than maintain a second design, its copy is remapped onto the
template the other treatments use, which also gives it the real PureMed logo, the
practitioner section, and the booking wiring, all for free: once this file exists,
build-microsites.py treats it exactly like the others.

Copy is taken from the original page. Nothing here is newly invented: the claims,
prices and result descriptions are the ones already written and reviewed.

    python3 tools/build-sculptra-source.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
TEMPLATE = WEB / "puremed-polynucleotides.html"
DEST = WEB / "puremed-sculptra.html"

TITLE = "Sculptra Collagen Biostimulator | PureMed Aesthetics Winslow"
DESC = ("Sculptra at PureMed Aesthetics, Winslow. A collagen-stimulating treatment that "
        "rebuilds facial structure gradually and naturally, never overfilled. Results can "
        "last up to 2 years. Consultations with Nafisa Mughal.")

HERO_EYEBROW = "Collagen Biostimulator"
HERO_H1 = "Sculptra<br><em>Collagen Rejuvenation</em>"
HERO_INTRO = ("A collagen-stimulating treatment that rebuilds the deep foundations of your "
              "face, gently and gradually, so you look rested and lifted rather than filled.")
HERO_BENEFITS = [
    "Stimulates your own collagen production",
    "Natural-looking, never &quot;done&quot;",
    "Restores facial structure and lift",
    "Results can last up to 2 years",
]
HERO_IMG = "sculptra-hero.webp"
HERO_IMG_ALT = "Sculptra collagen biostimulator result — PureMed Aesthetics"

WHAT_IS = """
<section class="what-is">
  <div class="container">
    <div class="what-is-inner">
      <div class="what-is-image fade-up"><img src="../assets/web/sculptra-ba-1.webp" alt="Sculptra treatment result at PureMed Aesthetics" style="width:100%;height:100%;object-fit:cover;display:block"></div>
      <div class="fade-up">
        <span class="section-label">The Treatment</span>
        <h2 class="section-title">Not a Filler.<br>A Collagen Rejuvenation.</h2>
        <p>Sculptra (poly-L-lactic acid) works with your body, gently signalling your skin to produce its own new collagen over several months. Rather than "plumping" an area like a traditional filler, it rebuilds the deep foundations of your face.</p>
        <p>The result is firmer, fresher, more sculpted skin, because the lift is genuinely your own.</p>
        <p>It is not a wrinkle problem, it is a foundation problem. From your thirties you lose around 1% of your collagen each year, mid-face fat pads slide downward, and bone density reduces. Without that underlying architecture, no skincare or filler can restore real shape.</p>
        <div style="margin-top:28px"><a href="https://facesconsent.com/bookings/puremedaesthetics" class="btn-primary" target="_blank" rel="noopener">Book a Consultation</a></div>
      </div>
    </div>
  </div>
</section>
"""

BENEFITS = [
    ("Stimulates Collagen", "Activates your skin's own collagen production from within, rather than adding volume from outside."),
    ("Gradual Results", "Subtle changes over weeks, with no sudden or obvious change that announces you have had something done."),
    ("Improves Skin Quality", "Firmer, smoother and more luminous, the kind of lit-from-within glow that skincare alone cannot reach."),
    ("Restores Structure", "Rebuilds the deep scaffolding of the face, lifting cheeks and refining the jawline."),
    ("Doesn't Simply Fill", "Unlike traditional filler, the result always looks unmistakably you, with no pillow-face or overfilled look."),
    ("Lasts Up to 2 Years", "Long-lasting rejuvenation that works out as exceptional value against repeat filler appointments."),
]

WHO = [
    "Women in their thirties and beyond noticing lost firmness",
    "Anyone whose face looks tired or flat rather than lined",
    "Clients wanting structure restored, not volume added",
    "People who want a gradual change nobody can pinpoint",
    "Anyone who has avoided filler for fear of looking overdone",
    "Clients who want results that last well beyond a year",
]

HOW = [
    ("Consultation", "A calm, unhurried assessment of your face and your goals. Honest advice and a personalised plan, with no pressure. Stand-alone &pound;25 consultation."),
    ("Your Sessions", "Typically 2 to 3 gentle sessions, 4 to 6 weeks apart. Sculptra is precisely placed by Nafisa, with minimal downtime."),
    ("Collagen Rebuilds", "Over the following 3 to 6 months your skin gradually firms as new collagen forms. There is no single before-and-after moment."),
    ("See Your Results", "Contours lift, skin quality improves, and the rejuvenation lasts up to 2 years."),
]

FAQ = [
    ("How is Sculptra different from filler?",
     "Both are injectable and that is where the similarity ends. Traditional hyaluronic filler adds volume by physically filling space, works instantly, and typically lasts 6 to 12 months. Sculptra stimulates your own collagen, changes gradually, improves skin quality and firmness, and can last up to 2 years."),
    ("How long until I see results?",
     "Collagen rebuilds over 3 to 6 months. This is deliberately not an instant treatment: the gradual timeline is why the result reads as natural rather than as work."),
    ("How many sessions will I need?",
     "Typically 2 to 3 sessions spaced 4 to 6 weeks apart. Your exact plan is confirmed at consultation, based on your face rather than a package."),
    ("Will it look obvious?",
     "No. The change is gradual and structural, so people tend to say you look well rather than ask what you have had done."),
    ("Is there downtime?",
     "Minimal. Most clients return to normal activities the same day. Any mild swelling or tenderness settles quickly."),
    ("How long do results last?",
     "Up to 2 years for most clients, which is considerably longer than traditional filler."),
]

BA = [
    ("sculptra-ba-1.webp", "Tired, dull skin to fresh and rested", "Softer forehead lines, a brighter under-eye area and a smoother overall complexion."),
    ("sculptra-ba-2.webp", "Lost volume to lifted contours", "Restored fullness across the cheeks and a softer, more defined lower face."),
    ("sculptra-ba-3.webp", "Deep lines softened naturally", "A subtle filling of the nasolabial folds and a more relaxed, rested expression."),
    ("sculptra-ba-4.webp", "Tired complexion to lit-from-within glow", "Visibly firmer, smoother skin with a healthier, brighter tone overall."),
    ("sculptra-ba-5.webp", "Under-eye crepiness smoothed and firmed", "Restored support beneath the eyes, so they look brighter and more open."),
    ("sculptra-ba-6.webp", "Sagging jaw to sculpted and defined", "Lifted cheek and a re-defined jawline, without any change to underlying features."),
]


def benefits_section():
    items = "".join(
        f'<div class="benefit-item fade-up">\n'
        f'          <div class="benefit-number">{i:02d}</div>\n'
        f'          <div class="benefit-title">{t}</div>\n'
        f'          <p class="benefit-desc">{d}</p>\n'
        f'        </div>'
        for i, (t, d) in enumerate(BENEFITS, 1))
    return f"""
<section class="benefits-sec">
  <div class="container">
    <div class="fade-up">
      <span class="section-label">Why Choose It</span>
      <h2 class="section-title">The Benefits</h2>
    </div>
    <div class="benefits-grid">{items}</div>
  </div>
</section>
"""


def build():
    if not TEMPLATE.is_file():
        raise SystemExit(f"template missing: {TEMPLATE}")
    html = TEMPLATE.read_text()

    def swap_section(doc, cls, new):
        pat = re.compile(rf'<section class="{cls}">.*?</section>\s*', re.S)
        if not pat.search(doc):
            raise SystemExit(f"section .{cls} not found in template")
        return pat.sub(new.strip() + "\n", doc, count=1)

    # head
    html = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", html, count=1, flags=re.S)
    html = re.sub(r'(<meta name="description" content=")[^"]*(")', rf"\g<1>{DESC}\g<2>", html, count=1)

    # body sections
    html = swap_section(html, "what-is", WHAT_IS)
    html = swap_section(html, "benefits-sec", benefits_section())

    def sub_once(doc, pattern, repl, what):
        """Substitute exactly once and fail loudly. A silent no-op here leaves
        polynucleotide copy sitting on a Sculptra page, which is worse than a crash."""
        out, n = re.subn(pattern, repl, doc, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"sculptra build: {what} did not match the template")
        return out

    # hero: substitute into the template's own markup so the eyebrow rule, tick
    # icons, review badge and image overlay all keep their exact structure
    html = sub_once(html, r'(<span class="tx-hero-eyebrow-text">).*?(</span>)',
                    rf"\g<1>{HERO_EYEBROW}\g<2>", "hero eyebrow")
    html = sub_once(html, r'(<h1>).*?(</h1>)', rf"\g<1>{HERO_H1}\g<2>", "hero h1")
    html = sub_once(html, r'(<p class="tx-hero-intro">).*?(</p>)',
                    rf"\g<1>{HERO_INTRO}\g<2>", "hero intro")
    bens = "\n".join(
        '<li><span class="check"><svg viewBox="0 0 12 10">'
        '<polyline points="1,5 4,8 11,1"></polyline></svg></span>' + b + '</li>'
        for b in HERO_BENEFITS)
    html = sub_once(html, r'(<ul class="tx-hero-benefits">).*?(</ul>)',
                    rf"\g<1>{bens}\g<2>", "hero benefits")
    html = sub_once(html, r'(<div class="tx-hero-image">\s*<img src=")[^"]+(" alt=")[^"]*(")',
                    rf"\g<1>../assets/web/{HERO_IMG}\g<2>{HERO_IMG_ALT}\g<3>", "hero image")

    # "who is it for"
    who = "".join(
        f'<div class="who-item"><div class="who-item-dot"></div><p>{w}</p></div>' for w in WHO)
    html = sub_once(html, r'(<div class="who-ideal">).*?(</div>\s*</div>\s*</div>)',
                    rf"\g<1>{who}\g<2>", "who list")
    html = sub_once(html, r'<h2 class="section-title">Who Is It<br><em>Right For\?</em></h2>',
                    '<h2 class="section-title">Is Sculptra<br><em>Right For You?</em></h2>',
                    "who heading")
    html = sub_once(html, r'(<section class="who">.*?<p class="section-subtitle">).*?(</p>)',
                    r"\g<1>Sculptra suits clients who want facial structure rebuilt gradually, "
                    r"rather than volume added instantly.\g<2>", "who subtitle")

    # process steps
    steps = "".join(
        f'<div class="how-step">\n'
        f'          <div class="how-step-num">{i}</div>\n'
        f'          <div><h3>{t}</h3><p>{d}</p></div>\n'
        f'        </div>'
        for i, (t, d) in enumerate(HOW, 1))
    html = sub_once(html, r'(<div class="how-steps">).*?(</div>\s*</div>\s*</section>)',
                    rf"\g<1>{steps}\g<2>", "how steps")

    # FAQ
    faq = "".join(
        f'<div class="faq-item">\n'
        f'          <button class="faq-q" onclick="toggleFaq(this)">{q}'
        f'<span class="faq-icon"><svg viewBox="0 0 12 12"><path d="M6 1v10M1 6h10"></path></svg></span></button>\n'
        f'          <div class="faq-a"><p>{a}</p></div>\n'
        f'        </div>'
        for q, a in FAQ)
    html = sub_once(html, r'(<section class="faq-sec">.*?<div>)<div class="faq-item">.*?(</div>\s*</div>\s*</div>\s*</section>)',
                    rf"\g<1>{faq}\g<2>", "faq list")

    # before & after grid (three tiles, sits outside the numbered sections)
    tiles = "".join(
        f'<div style="border-radius:8px;overflow:hidden">'
        f'<img src="../assets/web/{img}" alt="{t} — Sculptra at PureMed Aesthetics" '
        f'style="width:100%;aspect-ratio:3/2;object-fit:cover;display:block" loading="lazy"></div>'
        for img, t, _ in BA[:3])
    html = sub_once(html, r'(<div style="display:grid;grid-template-columns:repeat\(3,1fr\);gap:12px;margin-top:40px">).*?(</div>\s*</div>\s*</section>)',
                    rf"\g<1>{tiles}\g<2>", "before/after grid")
    html = sub_once(html, r'<h2 class="section-title">Polynucleotides<br>Before &amp; After</h2>',
                    '<h2 class="section-title">Sculptra<br>Before &amp; After</h2>', "b/a heading")

    # the "who is it for" section keeps the template's supporting image, which is
    # a polynucleotide shot, so point it at a Sculptra one
    html = html.replace("../assets/web/puremed-pnct-who-kling-v1.webp",
                        "../assets/web/sculptra-ba-2.webp")

    # name swaps outside the rewritten sections (nav label, CTAs, footer, schema).
    # Plural before singular, so "Polynucleotides" is not left as "Sculptras".
    for a, b in (("Polynucleotides (PNCT)", "Sculptra"), ("Polynucleotides", "Sculptra"),
                 ("Polynucleotide", "Sculptra"), ("polynucleotides", "sculptra"),
                 ("polynucleotide", "sculptra"), ("PNCT", "Sculptra")):
        html = html.replace(a, b)

    DEST.write_text(html)
    print(f"wrote {DEST.relative_to(ROOT)}  {DEST.stat().st_size // 1024}KB")


if __name__ == "__main__":
    build()
