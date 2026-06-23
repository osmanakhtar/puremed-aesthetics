#!/usr/bin/env python3
"""
IMAP-to-IMAP migration: Stack Mail → Google Workspace
Copies Inbox, Sent, Drafts, Junk, and Trash; safe to re-run.

Prerequisites:
  - Gmail IMAP must be enabled: Settings → See all settings →
    Forwarding and POP/IMAP → Enable IMAP
  - Use a Google App Password (not your account password) if
    2-Step Verification is on: myaccount.google.com/apppasswords

Usage:
    python3 migrate-imap.py
    python3 migrate-imap.py --src-password "..." --dst-password "..."
"""

from email import message_from_bytes
from email.message import Message
import argparse
import getpass
import hashlib
import imaplib
from pathlib import Path
import re
import ssl
import sys
import time
from typing import Optional

# ── Connection parameters ──────────────────────────────────────────────────────

SRC_SERVER = "imap.stackmail.com"
SRC_PORT   = 993
DST_SERVER = "imap.gmail.com"
DST_PORT   = 993
USERNAME   = "care@puremed.uk"

# ── Folder mapping ─────────────────────────────────────────────────────────────
# Maps source folder names (case-insensitive) → Gmail destination folder names.

FOLDER_MAP = {
    "inbox":            "INBOX",
    "sent":             "[Gmail]/Sent Mail",
    "sent messages":    "[Gmail]/Sent Mail",
    "sent items":       "[Gmail]/Sent Mail",
    "drafts":           "[Gmail]/Drafts",
    "draft":            "[Gmail]/Drafts",
    "junk":             "[Gmail]/Spam",
    "junk e-mail":      "[Gmail]/Spam",
    "spam":             "[Gmail]/Spam",
    "trash":            "[Gmail]/Trash",
    "deleted":          "[Gmail]/Trash",
    "deleted items":    "[Gmail]/Trash",
    "deleted messages": "[Gmail]/Trash",
}

# Gmail only honours these flags on APPEND; others are silently dropped.
VALID_FLAGS = frozenset({r"\Seen", r"\Answered", r"\Flagged", r"\Draft"})

APPEND_DELAY      = 0.05  # seconds between appends — respects Gmail rate limits
RECONNECT_RETRIES = 3
RECONNECT_DELAY   = 5     # seconds to wait before each reconnect attempt


# ── IMAP folder quoting ────────────────────────────────────────────────────────

def _quote(folder: str) -> str:
    """
    Wrap a mailbox name in IMAP double-quote syntax (RFC 3501 §4.3).
    Required for any name containing brackets, slashes, or spaces —
    e.g. [Gmail]/Trash → "[Gmail]/Trash".
    INBOX is the one name that is always safe as an atom.
    """
    if folder.upper() == "INBOX":
        return "INBOX"
    escaped = folder.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


# ── Resilient IMAP connection ──────────────────────────────────────────────────

class ResilientConn:
    """
    IMAP4_SSL wrapper that reconnects automatically on SSL drops or
    network resets, then re-selects the previously open mailbox so the
    caller can simply retry the failed operation.
    """

    _TRANSIENT = (imaplib.IMAP4.abort, ssl.SSLError, OSError)

    def __init__(self, server: str, port: int, username: str, password: str) -> None:
        self._server   = server
        self._port     = port
        self._username = username
        self._password = password
        self._selected: Optional[tuple[str, bool]] = None
        self._conn     = self._fresh_conn()

    def _fresh_conn(self) -> imaplib.IMAP4_SSL:
        conn = imaplib.IMAP4_SSL(self._server, self._port)
        conn.login(self._username, self._password)
        return conn

    def _run(self, method: str, *args, **kwargs):
        """Run an IMAP command, reconnecting on transient network failures."""
        for attempt in range(RECONNECT_RETRIES):
            try:
                return getattr(self._conn, method)(*args, **kwargs)
            except self._TRANSIENT as exc:
                if attempt == RECONNECT_RETRIES - 1:
                    raise
                print(
                    f"\n  Connection lost ({exc.__class__.__name__}: {exc}). "
                    f"Reconnecting in {RECONNECT_DELAY}s ...",
                    end=" ", flush=True,
                )
                time.sleep(RECONNECT_DELAY)
                try:
                    self._conn.logout()
                except Exception:
                    pass
                self._conn = self._fresh_conn()
                if self._selected:
                    folder, readonly = self._selected
                    self._conn.select(folder, readonly=readonly)
                print("OK")

    def list(self):
        return self._run("list")

    def select(self, folder: str, readonly: bool = False):
        result = self._run("select", folder, readonly)
        if result and result[0] == "OK":
            self._selected = (folder, readonly)
        return result

    def search(self, charset, *criteria):
        return self._run("search", charset, *criteria)

    def fetch(self, message_set: str, message_parts: str):
        return self._run("fetch", message_set, message_parts)

    def append(self, mailbox: str, flags, date_time, message: bytes):
        return self._run("append", mailbox, flags, date_time, message)

    def logout(self) -> None:
        try:
            self._conn.logout()
        except Exception:
            pass


# ── IMAP helpers ───────────────────────────────────────────────────────────────

def connect(server: str, port: int, username: str, password: str) -> ResilientConn:
    print(f"  Connecting to {server}:{port} ...", end=" ", flush=True)
    conn = ResilientConn(server, port, username, password)
    print("OK")
    return conn


def list_folder_names(conn: ResilientConn) -> list[str]:
    """Return all mailbox names from an IMAP LIST response."""
    typ, data = conn.list()
    if typ != "OK":
        return []
    names = []
    for item in data:
        name = _parse_list_item(item)
        if name:
            names.append(name)
    return names


def _parse_list_item(item) -> Optional[str]:
    """Extract folder name from a single IMAP LIST response line."""
    raw = item.decode("utf-8", errors="replace") if isinstance(item, bytes) else item
    # Format: (\Flags) "delimiter" "Folder Name"
    # Split past the closing paren of the flags, then skip the separator token.
    parts = raw.split(")", 1)
    if len(parts) < 2:
        return None
    remainder = parts[1].strip()           # e.g. "/" "Sent"  or  NIL Inbox
    tokens = remainder.split(None, 1)      # [separator, name_part]
    if len(tokens) < 2:
        return None
    return tokens[1].strip().strip('"')


def fingerprint(msg: Message) -> str:
    """
    Stable per-message key used for deduplication.
    Prefer the Message-ID header; fall back to a hash of Date+From+Subject.
    """
    mid = (msg.get("Message-ID") or "").strip()
    if mid:
        return mid
    raw = "\n".join([
        msg.get("Date", ""),
        msg.get("From", ""),
        msg.get("Subject", ""),
    ])
    return "hash:" + hashlib.sha1(raw.encode("utf-8", errors="replace")).hexdigest()


def scan_existing(conn: ResilientConn, folder: str) -> set[str]:
    """
    Return the set of fingerprints for every message already in the folder.
    Fetches headers only — does not download full message bodies.
    """
    typ, data = conn.select(_quote(folder), readonly=True)
    if typ != "OK":
        return set()
    total = int(data[0])
    if total == 0:
        return set()

    typ, data = conn.search(None, "ALL")
    if typ != "OK" or not data[0]:
        return set()

    seq_nums = data[0].split()
    fps: set[str] = set()
    batch_size = 200

    for i in range(0, len(seq_nums), batch_size):
        chunk = seq_nums[i : i + batch_size]
        seq_range = b",".join(chunk).decode()
        typ, fetched = conn.fetch(
            seq_range,
            "(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID DATE FROM SUBJECT)])",
        )
        if typ != "OK":
            continue
        for part in fetched:
            if isinstance(part, tuple):
                try:
                    msg = message_from_bytes(part[1])
                    fps.add(fingerprint(msg))
                except Exception:
                    pass

    return fps


def parse_fetch_response(
    data: list,
) -> tuple[Optional[str], Optional[object], Optional[bytes]]:
    """
    Extract (flags_str, internaldate, raw_message) from a FETCH (FLAGS INTERNALDATE RFC822) response.
    flags_str    — space-separated valid Gmail flags, or None
    internaldate — time.struct_time suitable for imaplib.append(), or None
    raw_message  — full RFC 822 bytes, or None
    """
    flags_str = None
    internaldate = None
    raw_message = None

    for part in data:
        if not isinstance(part, tuple):
            continue
        meta_raw = part[0]
        raw_message = part[1]

        meta = (
            meta_raw.decode("utf-8", errors="replace")
            if isinstance(meta_raw, bytes)
            else meta_raw
        )

        m = re.search(r"FLAGS \(([^)]*)\)", meta)
        if m:
            kept = [f for f in m.group(1).split() if f in VALID_FLAGS]
            flags_str = " ".join(kept) if kept else None

        # imaplib.Internaldate2tuple() searches for INTERNALDATE "..." in the bytes
        internaldate = imaplib.Internaldate2tuple(
            meta_raw if isinstance(meta_raw, bytes) else meta_raw.encode()
        )

    return flags_str, internaldate, raw_message


# ── Per-folder migration ───────────────────────────────────────────────────────

def _copy_one(
    src: ResilientConn,
    dst: ResilientConn,
    seq: bytes,
    dst_folder: str,
    existing: set[str],
) -> str:
    """
    Fetch one message from src and append it to dst.
    Returns "copied", "skipped", or "failed".
    Mutates `existing` on success so duplicates within the same run are caught.
    """
    try:
        typ, data = src.fetch(seq, "(FLAGS INTERNALDATE RFC822)")
        if typ != "OK":
            return "failed"

        flags_str, internaldate, raw_message = parse_fetch_response(data)
        if raw_message is None:
            return "failed"

        msg = message_from_bytes(raw_message)
        fp = fingerprint(msg)
        if fp in existing:
            return "skipped"

        flags_arg = f"({flags_str})" if flags_str else None
        typ, _ = dst.append(_quote(dst_folder), flags_arg, internaldate, raw_message)
        if typ != "OK":
            return "failed"

        existing.add(fp)
        time.sleep(APPEND_DELAY)
        return "copied"

    except Exception:
        return "failed"


def _log_failures(
    src: ResilientConn,
    src_folder: str,
    dst_folder: str,
    failed_seqs: list[bytes],
    log_path: Path,
) -> None:
    """Append header details for each persistently-failed message to failures.log."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "",
        "─" * 72,
        f"Run: {timestamp}   {src_folder} → {dst_folder}",
        f"{len(failed_seqs)} message(s) failed after retry:",
    ]

    for seq in failed_seqs:
        lines.append("")
        lines.append(f"  seq {seq.decode()}")
        try:
            typ, data = src.fetch(
                seq,
                "(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID DATE FROM SUBJECT)])",
            )
            if typ == "OK":
                for part in data:
                    if isinstance(part, tuple):
                        msg = message_from_bytes(part[1])
                        lines.append(f"  Message-ID : {(msg.get('Message-ID') or '(none)').strip()}")
                        lines.append(f"  Date       : {(msg.get('Date') or '(none)').strip()}")
                        lines.append(f"  From       : {(msg.get('From') or '(none)').strip()}")
                        lines.append(f"  Subject    : {(msg.get('Subject') or '(none)').strip()}")
                        break
            else:
                lines.append("  (could not fetch headers)")
        except Exception as exc:
            lines.append(f"  (header fetch error: {exc})")

    lines.append("")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def _retry_and_log(
    src: ResilientConn,
    dst: ResilientConn,
    src_folder: str,
    dst_folder: str,
    failed_seqs: list[bytes],
    existing: set[str],
    stats: dict,
    log_path: Path,
) -> None:
    """Retry failed sequences once; log any that still fail to failures.log."""
    print(f"    Retrying {len(failed_seqs)} failed message(s) ...")
    still_failed: list[bytes] = []

    for seq in failed_seqs:
        outcome = _copy_one(src, dst, seq, dst_folder, existing)
        if outcome == "copied":
            stats["copied"] += 1
            stats["failed"] -= 1
        else:
            still_failed.append(seq)

    if still_failed:
        _log_failures(src, src_folder, dst_folder, still_failed, log_path)
        print(f"    {len(still_failed)} still failed — details written to {log_path.name}")
    else:
        print(f"    All recovered on retry.")


def migrate_folder(
    src: ResilientConn,
    dst: ResilientConn,
    src_folder: str,
    dst_folder: str,
    verbose_failures: bool = False,
    log_path: Optional[Path] = None,
) -> dict:
    stats = {"copied": 0, "skipped": 0, "failed": 0}

    typ, data = src.select(_quote(src_folder), readonly=True)
    if typ != "OK":
        print(f"    SKIP — cannot open source '{src_folder}': {data}")
        return stats

    total = int(data[0])
    print(f"    Source messages : {total}")

    if total == 0:
        print(f"    Nothing to copy.")
        return stats

    print(f"    Scanning destination for duplicates ...", end=" ", flush=True)
    existing = scan_existing(dst, dst_folder)
    print(f"{len(existing)} already present.")

    # scan_existing changed dst's selected mailbox; restore src selection.
    src.select(_quote(src_folder), readonly=True)
    typ, data = src.search(None, "ALL")
    if typ != "OK" or not data[0]:
        print("    No messages returned by source search.")
        return stats

    seq_nums = data[0].split()
    failed_seqs: list[bytes] = []

    for i, seq in enumerate(seq_nums, 1):
        _progress(i, len(seq_nums), stats)
        outcome = _copy_one(src, dst, seq, dst_folder, existing)
        if outcome == "copied":
            stats["copied"] += 1
        elif outcome == "skipped":
            stats["skipped"] += 1
        else:
            stats["failed"] += 1
            failed_seqs.append(seq)

    _progress(len(seq_nums), len(seq_nums), stats, final=True)

    if failed_seqs and verbose_failures:
        _retry_and_log(src, dst, src_folder, dst_folder, failed_seqs, existing, stats, log_path)

    return stats


def _progress(current: int, total: int, stats: dict, final: bool = False) -> None:
    width = 28
    filled = int(width * current / total) if total else width
    bar = "█" * filled + "░" * (width - filled)
    line = (
        f"\r    [{bar}] {current}/{total}"
        f"  copied={stats['copied']}"
        f"  skipped={stats['skipped']}"
        f"  failed={stats['failed']}"
    )
    if final:
        print(line)
    else:
        print(line, end="", flush=True)


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrate IMAP mailbox from Stack Mail to Google Workspace."
    )
    parser.add_argument("--src-password", help=f"Stack Mail password for {USERNAME}")
    parser.add_argument(
        "--dst-password",
        help=f"Google Workspace App Password for {USERNAME}",
    )
    parser.add_argument(
        "--verbose-failures",
        action="store_true",
        help="Retry failed messages and log Message-ID/Date/From/Subject to failures.log",
    )
    args = parser.parse_args()

    src_password = args.src_password or getpass.getpass(
        f"Stack Mail password for {USERNAME}: "
    )
    dst_password = args.dst_password or getpass.getpass(
        f"Google Workspace App Password for {USERNAME}: "
    )

    print("\n── Connecting ─────────────────────────────────────────────────────────")
    try:
        src = connect(SRC_SERVER, SRC_PORT, USERNAME, src_password)
    except Exception as exc:
        sys.exit(f"Source connection failed: {exc}")

    try:
        dst = connect(DST_SERVER, DST_PORT, USERNAME, dst_password)
    except Exception as exc:
        sys.exit(f"Destination connection failed: {exc}")

    # Discover which source folders map to Gmail destinations
    src_folders = list_folder_names(src)
    plan: list[tuple[str, str]] = []
    for name in src_folders:
        dst_name = FOLDER_MAP.get(name.lower())
        if dst_name:
            plan.append((name, dst_name))

    if not plan:
        sys.exit(
            "No matching folders found on source. "
            "Run test-imap-connection.py to see available folder names."
        )

    print(f"\n── Migration plan ─────────────────────────────────────────────────────")
    for src_name, dst_name in plan:
        print(f"  {src_name!r:<30} → {dst_name!r}")

    log_path = Path(__file__).parent / "failures.log"

    # Run
    results: list[tuple[str, str, dict]] = []
    for src_folder, dst_folder in plan:
        print(f"\n── {src_folder} → {dst_folder} {'─' * max(0, 60 - len(src_folder) - len(dst_folder))}")
        stats = migrate_folder(
            src, dst, src_folder, dst_folder,
            verbose_failures=args.verbose_failures,
            log_path=log_path,
        )
        results.append((src_folder, dst_folder, stats))

    # Summary
    print("\n" + "=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    total_copied = total_skipped = total_failed = 0

    for src_folder, dst_folder, stats in results:
        label = f"{src_folder} → {dst_folder}"
        print(
            f"  {label:<44}"
            f"  copied={stats['copied']:>5}"
            f"  skipped={stats['skipped']:>5}"
            f"  failed={stats['failed']:>5}"
        )
        total_copied  += stats["copied"]
        total_skipped += stats["skipped"]
        total_failed  += stats["failed"]

    print("-" * 72)
    print(
        f"  {'TOTAL':<44}"
        f"  copied={total_copied:>5}"
        f"  skipped={total_skipped:>5}"
        f"  failed={total_failed:>5}"
    )
    print("=" * 72)

    if total_failed:
        print(
            f"\n  {total_failed} message(s) failed to copy. "
            "Re-run the script to retry — already-copied messages will be skipped."
        )
    else:
        print("\n  All messages copied successfully.")

    src.logout()
    dst.logout()


if __name__ == "__main__":
    main()
