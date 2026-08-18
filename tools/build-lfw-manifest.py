#!/usr/bin/env python3
"""One-off manifest builder for the standalone laserfaceliftwinslow.co.uk
microsite engagement (puremed-laser-facelift-winslow). Single page, no
prototype page-switcher entries needed beyond the one page.

    python3 tools/build-lfw-manifest.py --out /tmp/manifest-lfw.json [--base <existing manifest.json>]
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "web" / "stage-build-lfw"
AUTOTAG = pathlib.Path.home() / "workspace" / "scripts" / "stage-autotag.js"

ENGAGEMENT_NAME = "PureMed Aesthetics — Laser Facelift Winslow (microsite)"
CLIENT = "PureMed Aesthetics"


def scan():
    f = BUILD / "index.html"
    if not f.is_file():
        sys.exit(f"no built page at {f}")
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        out = pathlib.Path(tmp.name)
    subprocess.run(
        ["node", str(AUTOTAG), "--files", str(f), "--relroot", str(BUILD), "--scan", str(out)],
        check=True, capture_output=True,
    )
    data = json.loads(out.read_text())
    out.unlink()
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--base")
    ap.add_argument("--allow-drop", default="")
    args = ap.parse_args()

    data = scan()
    loc = lambda f: "Laser Facelift Winslow (single page)"  # noqa: E731

    sections = [{"id": c["id"], "label": c["label"], "location": loc(c["astroFile"]),
                 "copy": c["text"], "sourceFile": c["astroFile"]} for c in data["copy"]]
    fields = [{"id": i["id"], "label": i["label"], "location": loc(i["astroFile"]),
               "sourceFile": i["astroFile"]} for i in data["img"]]

    base = {}
    if args.base and pathlib.Path(args.base).is_file():
        base = json.loads(pathlib.Path(args.base).read_text())

    if base:
        have = {s["id"] for s in sections} | {f["id"] for f in fields}
        had = ({s["id"] for s in base.get("copy", {}).get("sections", [])}
               | {f["id"] for f in base.get("images", {}).get("fields", [])})
        lost = sorted(had - have - {i.strip() for i in args.allow_drop.split(",") if i.strip()})
        if lost:
            sys.exit("REFUSING to write: ids would be stranded:\n  " + "\n  ".join(lost))

    manifest = {
        "engagement": base.get("engagement", ENGAGEMENT_NAME),
        "client": base.get("client", CLIENT),
        "liveEditable": True,
        "allowNavigation": False,
        "hiddenFromClient": False,
        "modes": base.get("modes", ["prototype", "copy"]),
        "prototype": {
            "file": "prototype/index.html",
            "pages": [{"id": "index", "label": "Laser Facelift Winslow", "file": "prototype/index.html"}],
        },
        "copy": {"sections": sections},
        "images": {"fields": fields},
    }
    pathlib.Path(args.out).write_text(json.dumps(manifest, indent=1))
    print(f"manifest -> {args.out}")
    print(f"  copy {len(sections)}  images {len(fields)}")


if __name__ == "__main__":
    main()
