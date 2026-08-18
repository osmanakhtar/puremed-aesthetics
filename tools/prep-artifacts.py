#!/usr/bin/env python3
"""
Turn the self-contained pages in web/publish/ into Artifact-ready fragments.

The Artifact host supplies its own <!doctype>/<head>/<body> skeleton, so the
uploaded file must contain page content only. This strips the document wrapper
and keeps <title>, <style> and the body markup.

Optionally rewrites the relative cross-page links (the "Treatments" dropdown,
footer treatment list and nav logo) to published Artifact URLs, supplied as a
JSON map on argv[1]:

    {"puremed-laser-lift": "https://...", "index": "https://..."}

Run from the puremed project root:

    python3 tools/prep-artifacts.py [urls.json]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "web" / "publish"
OUT = ROOT / "web" / "publish" / "_artifact"


def strip_wrapper(html: str) -> str:
    # keep everything inside <head> except the document-level link/meta noise
    head = re.search(r"<head[^>]*>(.*?)</head>", html, re.S)
    body = re.search(r"<body[^>]*>(.*?)</body>", html, re.S)
    if not head or not body:
        raise SystemExit("unexpected document shape")
    h = head.group(1)
    keep = []
    t = re.search(r"<title>.*?</title>", h, re.S)
    if t:
        keep.append(t.group(0))
    for s in re.findall(r"<style[^>]*>.*?</style>", h, re.S):
        keep.append(s)
    for s in re.findall(r'<script[^>]*type="application/ld\+json".*?</script>', h, re.S):
        keep.append(s)
    return "\n".join(keep) + "\n" + body.group(1)


def apply_urls(html: str, urls: dict) -> str:
    for slug, url in urls.items():
        html = html.replace(f'href="{slug}.html"', f'href="{url}"')
    return html


def main():
    urls = {}
    if len(sys.argv) > 1 and pathlib.Path(sys.argv[1]).is_file():
        urls = json.loads(pathlib.Path(sys.argv[1]).read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(SRC.glob("puremed-*.html")):
        html = strip_wrapper(f.read_text())
        if urls:
            html = apply_urls(html, urls)
        dest = OUT / f.name
        dest.write_text(html)
        left = len(re.findall(r'href="puremed-[a-z-]+\.html"|href="index\.html"', html))
        print(f"  {dest.name:38s} {dest.stat().st_size/1048576:5.2f} MB  unresolved-links={left}")


if __name__ == "__main__":
    main()
