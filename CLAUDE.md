# PureMed Aesthetics — Claude Session Context

*Standalone personal project. Not an MSS client engagement.*
*Working directory: ~/workspace/other-projects/puremed/*
*Last reviewed: 3 July 2026*

---

## What this project is

Full clean-slate website rebuild for PureMed Aesthetics, a medically-led aesthetics
clinic run by Nafisa. Rebuilt from an existing Framer site that scored 23/100 on a
CRO audit. This is the first live test of the MSS Astro delivery pipeline:

```
Prototype HTML → Stage review (mss-review.duckdns.org) → Nafisa signs off
  → Astro build from approved prototype → GitHub Actions → Cloudways static
```

## Current status

- Two-page prototype (Home + Treatments) deployed on Stage for client review
- Stage manifest patched with `astroFile` + `astroProp` per copy section
  (see `~/workspace/scripts/patch-manifest-astro-fields.js`)
- Astro build, GitHub Actions CI/CD, and Cloudways static app: pending
- Domain not yet migrated — staging uses the free `.cloudwaysapps.com` URL

## Context files (in `.claude/`)

| File | What it covers |
|------|----------------|
| `puremed-brand-identity.md` | Palette, logo, typography, voice, site architecture |
| `puremed-decisions-log.md` | What's locked, what's open, build constraints |

Read both before any copy or build session. The decisions log wins if anything
disagrees. Load the PureMed voice from the brand-identity file — not MSS voice.

## Stack

- **Build:** Astro static site (Bricks Builder + LocalWP retired 25 June 2026 —
  DEC-002/DEC-003 and the WordPress constraints in the decisions log are
  historical only; do not follow them)
- **Review:** Stage on the Pi — engagement `puremed`
- **Hosting:** Cloudways, DigitalOcean, London region
- **Booking:** all CTAs link to `facesconsent.com/bookings/puremedaesthetics`

## Source material

`web/` holds the HTML prototypes (index, treatments, per-treatment pages) and
the client's source documents (requirements, brand strategy, discovery docx).
`puremed-email-*.md` cover the completed email migration (historical reference).
