#!/usr/bin/env python3
"""
Build the Stage manifest for the `puremed-micro` live-edit engagement.

The anchor inventory comes from the tagger's --scan mode, so the manifest and the
tags in the HTML always come from one source of truth. The Astro-oriented
scripts/stage-build-manifest.js cannot be reused here: it globs an Astro project
and carries a hardcoded Astro location map.

    python3 tools/build-stage-manifest.py --out /tmp/manifest-micro.json
      [--base <existing manifest.json>]

--base preserves the engagement's identity fields on a regenerate. It also acts
as the safety guard: if any copy or image id in the base manifest would vanish
from the new one, the build refuses to write, because a disappearing id strands
whatever the client had already edited against it.
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "web" / "stage-build"
AUTOTAG = pathlib.Path.home() / "workspace" / "scripts" / "stage-autotag.js"

ENGAGEMENT_NAME = "PureMed Aesthetics — Treatment Microsites (POC)"
CLIENT = "PureMed Aesthetics"

# Page order is the order Nafisa sees in Stage's page switcher.
PAGES = [
    ("index", "All treatments (start here)"),
    ("puremed-laser-lift", "Laser Lift"),
    ("puremed-liquid-facelift", "Liquid Facelift"),
    ("puremed-anti-wrinkle", "Anti-Wrinkle"),
    ("puremed-polynucleotides", "Polynucleotides"),
    ("puremed-rf-microneedling", "RF Microneedling"),
    ("puremed-skin-boosters", "Skin Boosters"),
    ("puremed-sculptra", "Sculptra"),
    ("booking", "Booking journey (demo)"),
]
LOCATION = {f"{slug}.html": label for slug, label in PAGES}


# The booking prototype is a JavaScript application, not editable copy. It is
# served as a page so the journey is clickable, but it is never tagged: making its
# rendered controls contenteditable would corrupt the journey it is demonstrating.
NEVER_TAG_PAGES = {"booking.html"}


def scan():
    files = sorted(f for f in BUILD.glob("*.html") if f.name not in NEVER_TAG_PAGES)
    if not files:
        sys.exit(f"no built pages in {BUILD}; run build-microsites.py --target=stage first")
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        out = pathlib.Path(tmp.name)
    subprocess.run(
        ["node", str(AUTOTAG), "--files", ",".join(str(f) for f in files),
         "--relroot", str(BUILD), "--scan", str(out)],
        check=True, capture_output=True,
    )
    data = json.loads(out.read_text())
    out.unlink()
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--base")
    ap.add_argument("--allow-drop", default="",
                    help="comma-separated ids that are allowed to disappear, for when "
                         "source copy was deliberately rewritten. Check the overlay first: "
                         "any client edit against a dropped id is lost.")
    args = ap.parse_args()

    data = scan()
    loc = lambda f: LOCATION.get(f, f)  # noqa: E731

    sections = [{"id": c["id"], "label": c["label"], "location": loc(c["astroFile"]),
                 "copy": c["text"], "sourceFile": c["astroFile"]} for c in data["copy"]]
    fields = [{"id": i["id"], "label": i["label"], "location": loc(i["astroFile"]),
               "sourceFile": i["astroFile"]} for i in data["img"]]

    base = {}
    if args.base and pathlib.Path(args.base).is_file():
        base = json.loads(pathlib.Path(args.base).read_text())

    # Guard: never drop an id the client may already have edited against.
    if base:
        have = {s["id"] for s in sections} | {f["id"] for f in fields}
        had = ({s["id"] for s in base.get("copy", {}).get("sections", [])}
               | {f["id"] for f in base.get("images", {}).get("fields", [])})
        lost = sorted(had - have - {i.strip() for i in args.allow_drop.split(",") if i.strip()})
        if lost:
            sys.exit("REFUSING to write: these ids exist in the base manifest but not in "
                     "the new one, so any client edit against them would be stranded:\n  "
                     + "\n  ".join(lost[:20])
                     + (f"\n  ... and {len(lost) - 20} more" if len(lost) > 20 else ""))

    manifest = {
        "engagement": base.get("engagement", ENGAGEMENT_NAME),
        "client": base.get("client", CLIENT),
        "liveEditable": True,
        # Lets internal links (prototype routes + same-page anchors) navigate
        # instead of being swallowed by the editor, so the page -> booking journey
        # is clickable. External links stay blocked. Opt-in per engagement:
        # puremed-site deliberately does not set this.
        "allowNavigation": True,
        "modes": base.get("modes", ["prototype", "copy"]),
        "prototype": {
            "file": "prototype/index.html",
            "pages": [{"id": s, "label": l, "file": f"prototype/{s}.html"} for s, l in PAGES],
        },
        "copy": {"sections": sections},
        "images": {"fields": fields},
    }
    pathlib.Path(args.out).write_text(json.dumps(manifest, indent=1))
    print(f"manifest -> {args.out}")
    print(f"  pages {len(PAGES)}  copy {len(sections)}  images {len(fields)}")


if __name__ == "__main__":
    main()
