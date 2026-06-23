#!/usr/bin/env python3
"""
Phase 3 — IMAP connection test for PureMed Stack Mail migration.
Tests login, lists folder structure, and reports mailbox counts.

Usage:
    python3 test-imap-connection.py
    python3 test-imap-connection.py --password "yourpassword"
"""

import imaplib
import argparse
import getpass
import sys

SERVER = "imap.stackmail.com"
PORT = 993
USERNAME = "care@puremed.uk"


def test_connection(password: str) -> None:
    print(f"\nConnecting to {SERVER}:{PORT} (SSL)...")

    try:
        mail = imaplib.IMAP4_SSL(SERVER, PORT)
    except Exception as e:
        print(f"  FAIL — could not connect: {e}")
        sys.exit(1)

    print("  Connected.")

    print(f"Logging in as {USERNAME}...")
    try:
        mail.login(USERNAME, password)
    except imaplib.IMAP4.error as e:
        print(f"  FAIL — login rejected: {e}")
        sys.exit(1)

    print("  Login successful.\n")

    # List all folders
    print("Folder structure:")
    status, folder_list = mail.list()
    folders = []
    for item in folder_list:
        parts = item.decode().split('"/"')
        name = parts[-1].strip().strip('"')
        folders.append(name)
        print(f"  {name}")

    # Count messages in each folder
    print("\nMessage counts:")
    for folder in folders:
        try:
            status, data = mail.select(f'"{folder}"', readonly=True)
            if status == "OK":
                count = int(data[0])
                print(f"  {folder}: {count} messages")
        except Exception:
            pass

    mail.logout()
    print("\nDone. Connection test passed — credentials are valid.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--password", help="Stack Mail password for care@puremed.uk")
    args = parser.parse_args()

    password = args.password or getpass.getpass(f"Password for {USERNAME}: ")
    test_connection(password)
