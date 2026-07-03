# Deployment — PureMed Astro site

Two workflows, two gates:

| Workflow | Trigger | Gate | Target |
|---|---|---|---|
| `staging.yml` | Push/merge to `main` touching `site/` | PR review + merge | Cloudways staging webroot |
| `deploy.yml` | Manual dispatch, type `deploy` to confirm | Explicit human confirmation | Cloudways production webroot |

The pipeline this completes: Stage sign-off → Loop 2 opens a `signoff/*` branch →
admin reviews the PR diff → **merge = staging deploy**. Production stays manual
until the domain cutover.

## One-time setup (not yet done)

1. **GitHub remote** — this repo has no remote yet:
   `gh repo create osmanakhtar/puremed --private --source . --push`
2. **Cloudways static app** — create the PHP/static app on `mss-do-lon-01`
   per `main-stage-studio/01_mss/strategy/mss-astro-cloudways-setup.md`.
3. **Repo secrets** (Settings → Secrets → Actions):
   - `CLOUDWAYS_SSH_KEY` — private key (`~/.ssh/github_actions_mss` per migration plan)
   - `CLOUDWAYS_HOST` — server IP/host
   - `CLOUDWAYS_USER` — SSH user
   - `CLOUDWAYS_WEBROOT_STAGING` — staging app webroot path (e.g. `applications/<app>/public_html`)
   - `CLOUDWAYS_WEBROOT_PROD` — production app webroot path (set later, at cutover)

Note: the migration plan named a single `CLOUDWAYS_WEBROOT` secret; this splits
it into `_STAGING`/`_PROD` so merge-to-main can never touch production.
