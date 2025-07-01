#!/usr/bin/env python3
"""CLI tool for Instagram interactions."""

from __future__ import annotations

import argparse
import csv
import os
from pathlib import Path

from dotenv import load_dotenv
from instagrapi import Client

from services.airtable_service import upsert_followers


SESSION_FILE = Path("session.json")


def get_authenticated_client() -> Client | None:
    """Authenticate to Instagram and return a client instance."""
    load_dotenv()
    username = os.getenv("INSTAGRAM_LOGIN")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print("Error: INSTAGRAM_LOGIN and INSTAGRAM_PASSWORD must be set in the .env file")
        return None

    client = Client()

    if SESSION_FILE.exists():
        try:
            client.load_settings(SESSION_FILE)
            client.login(username, password)
            return client
        except Exception:
            print("Stored session invalid, logging in fresh...")

    try:
        client.login(username, password)
        client.dump_settings(SESSION_FILE)
        return client
    except Exception as exc:
        print(f"Login failed: {exc}")
        return None


def cmd_login(_: argparse.Namespace) -> None:
    """Authenticate using .env credentials."""
    client = get_authenticated_client()
    if client:
        print(f"Successfully logged in as {client.username}")


def cmd_followers(args: argparse.Namespace) -> None:
    """Fetch followers for a username and export to CSV."""
    client = get_authenticated_client()
    if not client:
        return

    target_username = args.username
    limit = args.limit
    try:
        user_id = client.user_id_from_username(target_username)
        followers = client.user_followers(user_id, amount=limit)
    except Exception as exc:
        print(f"Failed to fetch followers: {exc}")
        return

    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)
    csv_path = export_dir / f"followers_{target_username}.csv"

    records = []
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "full_name", "profile_url"])
        for follower in followers.values():
            print(f"{follower.username} - {follower.full_name}")
            record = {
                "username": follower.username,
                "full_name": follower.full_name,
                "profile_url": f"https://instagram.com/{follower.username}",
            }
            records.append(record)
            writer.writerow([
                record["username"],
                record["full_name"],
                record["profile_url"],
            ])

    try:
        upsert_followers(records)
    except Exception as exc:
        print(f"Airtable upload failed: {exc}")

    print(f"Exported {len(followers)} followers to {csv_path}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Instagram CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    login_parser = subparsers.add_parser("login", help="Authenticate to Instagram")
    login_parser.set_defaults(func=cmd_login)

    followers_parser = subparsers.add_parser(
        "followers", help="Export followers list to CSV"
    )
    followers_parser.add_argument("--username", required=True, help="Target account")
    followers_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of followers to fetch (default 10)",
    )
    followers_parser.set_defaults(func=cmd_followers)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
