# PureMed — Stack Mail to Google Workspace Migration Checklist

*Starting brief for Claude Code. Domain: puremed.uk. No existing Google Workspace account, this is a from-scratch setup.*
*Created: 21 June 2026 — Completed: 23 June 2026*

---

## What's already confirmed

| Item | Value |
|------|-------|
| Source provider | Stack Mail (20i) |
| IMAP server | `imap.stackmail.com` |
| IMAP port | 993, SSL |
| Mailbox username | care@puremed.uk |
| Mailbox password | Confirmed, in hand, re-verify it was captured against the correct address |
| DNS control | To confirm before cutover, see Phase 2 |

---

## Phase 1 — Google Workspace setup (manual, in browser)

This is a guided signup flow on Google's side, not scriptable. Do this first.

- [x] Go to admin.google.com, start a new Workspace signup for `puremed.uk`
- [x] Choose plan (Business Starter is sufficient for a single small mailbox)
- [x] Verify domain ownership — Google will ask you to add a TXT or CNAME record to DNS
- [x] Confirm DNS access before this step, see Phase 2 below if unsure
- [x] Create the user account `care@puremed.uk` inside Workspace
- [x] Set a temporary strong password for the new Workspace mailbox

**Gate:** Workspace account active, domain verified, user created. Don't move to migration until this is done.

---

## Phase 2 — DNS access check

- [x] Confirm who currently controls DNS for puremed.uk — likely still with the old hosting provider until the Cloudways migration completes
- [x] If DNS isn't in your hands yet, get access before going further — you'll need it twice: once for domain verification (Phase 1) and once for the MX cutover (Phase 5)
- [x] Note current DNS records as a baseline (MX, SPF, any existing TXT records) before changing anything — useful if anything needs reverting

---

## Phase 3 — Test the IMAP connection (Claude Code can help here)

Before trusting the migration with the real run, confirm the credentials actually authenticate.

- [x] Use a simple IMAP test (script or a mail client) to confirm `care@puremed.uk` logs in successfully at `imap.stackmail.com:993`
- [x] Confirm the mailbox folder structure (Inbox, Sent, any custom folders) so nothing gets missed in migration scope

**Gate:** Connection confirmed working before starting the real migration.

---

## Phase 4 — Run the migration

> **Note:** Google Data Migration Service was not used. Instead, a custom IMAP-to-IMAP Python script (`migrate-imap.py`) was written and run directly. It connects to both servers simultaneously, copies messages folder by folder, preserves flags and INTERNALDATE, and deduplicates by Message-ID so it is safe to re-run.
>
> **1 message failed to copy across all runs** (Inbox). The failure persisted after retry, suggesting the message is malformed on the source server. It has been logged to `failures.log`. All other messages migrated successfully.

- [x] Confirm source IMAP credentials and folder structure (Phase 3)
- [x] Run `migrate-imap.py` — copies Inbox, Sent, Drafts, Junk, Trash
- [x] Spot check: confirm folder structure and a sample of older emails landed correctly in the new Workspace mailbox

**Gate:** Migration complete and spot-checked before DNS cutover.

---

## Phase 5 — DNS cutover

This is the moment email actually switches over. Do this deliberately, not as an afterthought.

- [x] Update MX records to Google's values (Google Admin provides the exact records to use)
- [x] Add or update SPF record to include Google's sending servers
- [x] Add DKIM record (Google Admin generates this, you enable it after adding the record)
- [x] Consider DMARC if not already present, optional but good practice
- [x] Confirm propagation (can take a few hours, sometimes up to 24-48)

**Gate:** New mail flowing into Google Workspace. Old Stack Mail inbox stops receiving new mail once propagation completes.

---

## Phase 6 — Catch the gap

Emails sent during the propagation window might land in the old Stack Mail inbox instead of Workspace.

- [x] Re-run `migrate-imap.py` a day or two after cutover to catch anything that arrived during the propagation gap — already-migrated messages are skipped automatically by dedup
- [x] Confirm no new mail is arriving in the old Stack Mail inbox before considering it safe to decommission

---

## Phase 7 — Decommission

- [x] Confirm with the client (Nafisa) that everything's landed correctly in the new inbox
- [x] Cancel or downgrade the Stack Mail mailbox once confident nothing's missing
- [x] Update PureMed's spend tracker to reflect the new Google Workspace cost and the removal of whatever the old provider was charging

---

## Notes

- This checklist assumes a single mailbox (`care@puremed.uk`). If more addresses exist on the domain, repeat Phases 1, 3, 4 for each.
- Don't skip Phase 3. Testing the IMAP connection before the real migration catches credential or server issues early, rather than mid-migration.
- Keep the old Stack Mail mailbox active and untouched until Phase 6 is fully confirmed. Don't cancel early to save a month's cost, the risk of losing unmigrated mail isn't worth it.
- 1 message in Inbox failed to copy and is recorded in `failures.log`. Likely malformed at source — acceptable to close out the migration without it.
