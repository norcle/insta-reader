#!/usr/bin/env python3
"""Simple CLI to authenticate to Instagram."""

import os
from instagrapi import Client
from dotenv import load_dotenv


def main() -> None:
    """Load environment and attempt Instagram login."""
    load_dotenv()

    username = os.getenv("INSTAGRAM_LOGIN")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print(
            "Error: INSTAGRAM_LOGIN and INSTAGRAM_PASSWORD must be set in the .env file"
        )
        return

    client = Client()
    try:
        client.login(username, password)
        print(f"Successfully logged in as {username}")
    except Exception as exc:
        print(f"Login failed: {exc}")


if __name__ == "__main__":
    main()
