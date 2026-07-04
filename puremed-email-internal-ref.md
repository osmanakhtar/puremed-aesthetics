# PureMed — Email Configuration Internal Reference
*MSS internal document. Not for distribution to client.*
*Created: 23 June 2026*

---

## What was done

Migrated `care@puremed.uk` from Stack Mail (20i) to Google Workspace Business Starter. Single mailbox, no other addresses on the domain. Migration completed 23 June 2026.

---

## Configuration overview

### DNS — 123-reg
Domain registrar and DNS host: 123-reg. Nameservers were switched from StackDNS (ns1/ns2/ns3.stackdns.com) to 123-reg defaults (ns75/ns76.domaincontrol.com) as part of this migration.

Current DNS records of note:

| Type | Name | Value | Purpose |
|------|------|-------|---------|
| A | @ | 31.43.160.6 | Framer site |
| A | @ | 31.43.161.6 | Framer site |
| CNAME | www | sites.framer.app | Framer www redirect |
| MX | @ | ASPMX.L.GOOGLE.COM (priority 1) | Google mail |
| MX | @ | ALT1.ASPMX.L.GOOGLE.COM (priority 5) | Google mail |
| MX | @ | ALT2.ASPMX.L.GOOGLE.COM (priority 5) | Google mail |
| MX | @ | ALT3.ASPMX.L.GOOGLE.COM (priority 10) | Google mail |
| MX | @ | ALT4.ASPMX.L.GOOGLE.COM (priority 10) | Google mail |
| TXT | @ | v=spf1 include:_spf.google.com ~all | SPF — Google sending |
| TXT | @ | google-site-verification=IYnVumcYEbpwXFnneSMn79tfsMsYUln_bdN16nsp73o | Domain verification |
| TXT | _dmarc | v=DMARC1; p=quarantine; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net | DMARC (pre-existing) |

**Note on DMARC:** The DMARC record was pre-existing from the old hosting provider. The `rua` reporting address (onsecureserver.net) points to the old provider's reporting inbox. This is not an immediate problem but ideally should be updated to a monitored address or removed if DMARC reporting isn't being used. Not urgent.

**DKIM:** Not yet configured. Google Workspace generates a DKIM key in the admin console under Apps, Google Workspace, Gmail, Authenticate email. Adding DKIM improves deliverability and is recommended as a follow-up task.

---

### Google Workspace

| Item | Value |
|------|-------|
| Plan | Business Starter |
| Admin account | care@puremed.uk |
| Admin console | admin.google.com |
| Users | 1 (care@puremed.uk) |
| Billing start | July 2026 |
| Cost | £7/user/month + VAT (flexible monthly) |
| Recovery email | akhtar.nafisa@gmail.com |
| 2-step verification | Enabled, phone 07758 964646 |
| IMAP | Enabled |

---

### Migration

Migration was done using a custom Python IMAP-to-IMAP script (`migrate-imap.py`) rather than Google's Data Migration Service, which required Gmail activation before it would run — and Gmail activation pushed the MX cutover before migration was complete.

**Migration scripts** are saved at:
`/Users/osmanakhtar/workspace/other-projects/puremed/`

- `test-imap-connection.py` — IMAP connection and folder count test
- `migrate-imap.py` — full IMAP-to-IMAP migration with deduplication and auto-reconnect

**Source IMAP credentials (Stack Mail):**
- Server: imap.stackmail.com, port 993, SSL
- Username: care@puremed.uk

**Migration results:**

| Folder | Copied | Skipped | Failed |
|--------|--------|---------|--------|
| Trash | 1 | 1,544 | 0 |
| Junk | 1 | 338 | 0 |
| Sent | 661 | 1 | 0 |
| Drafts | 11 | 0 | 0 |
| Inbox | 2,345 | 1 | 1 |
| **Total** | **3,019** | **1,884** | **1** |

One message failed to copy across all runs. Almost certainly a malformed or corrupted message. Not recoverable via IMAP.

---

## Troubleshooting

### Can't sign in to Gmail

1. Confirm the user is signing in with `care@puremed.uk`, not a personal Gmail address.
2. If the password is lost, go to admin.google.com, Users, select the user, and reset the password.
3. If the admin password is also lost, use the recovery email `akhtar.nafisa@gmail.com` at accounts.google.com to recover the account.

---

### Email not being received

Check in this order:

1. **DNS propagation:** Confirm MX records are live using [mxtoolbox.com](https://mxtoolbox.com). Enter `puremed.uk` and verify the five Google MX records are returned.
2. **Gmail activation:** Confirm Gmail is fully activated in the Workspace admin console. Go to admin.google.com, Apps, Google Workspace, Gmail — status should show On.
3. **Spam:** Check the Gmail Spam folder. Google's filters are aggressive on new domains. If legitimate mail is going to Spam, the sender needs to be marked as Not Spam.
4. **SPF/DKIM:** If deliverability issues persist, confirm SPF is returning correctly at mxtoolbox.com and consider adding DKIM (see below).

---

### Email going to recipients' spam

The domain is newly configured on Google Workspace. Some spam filtering is normal for the first few weeks as the domain's sending reputation builds.

Steps to improve:

1. **Add DKIM:** Go to admin.google.com, Apps, Google Workspace, Gmail, Authenticate email. Generate the DKIM key, add the TXT record to 123-reg DNS, then enable signing. This is the single most effective deliverability improvement available.
2. **Update DMARC:** The existing DMARC record points to an old provider's reporting address. Consider updating `rua` to a monitored address or removing the record until DKIM is configured — DMARC is most useful once both SPF and DKIM are in place.
3. **Warm up sending gradually:** Avoid sending bulk messages immediately. Let the domain build reputation through normal correspondence first.

---

### Framer site down

The Framer site runs on the same domain. If it goes down, check:

1. **A records in 123-reg DNS:** Confirm both A records for `@` are present (31.43.160.6 and 31.43.161.6).
2. **CNAME for www:** Confirm `www` CNAME points to `sites.framer.app`.
3. **Framer status:** Check [status.framer.com](https://status.framer.com) for platform issues.

Do not delete or modify the A records for Framer when making DNS changes for email. They are independent.

---

### Adding a new mailbox

1. Go to admin.google.com, Users, Add new user.
2. Set the email address and a temporary password.
3. Cost increases by £7/month + VAT per additional user.
4. If the new user needs existing emails from an old address, the migration scripts at the path above can be reused — update the source server, username, and destination credentials.

---

### DNS changes needed in future

All DNS changes go through 123-reg at:
`dcc.123-reg.co.uk/control/dnsmanagement?domainName=puremed.uk`

Log in with the 123-reg account credentials. Exercise care when editing — the Framer site and email are both dependent on records in this panel.

---

## Follow-up tasks (recommended, not urgent)

- [ ] Add DKIM record for improved deliverability
- [ ] Update or remove DMARC rua address (currently pointing to old provider)
- [ ] Cancel Stack Mail mailbox once Nafisa confirms she's happy with Gmail
- [ ] Update PureMed spend tracker to reflect new Google Workspace cost

---

*Internal reference document. Created by Main Stage Studio, 23 June 2026.*
