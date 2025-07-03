#!/usr/bin/env python3
"""Simple CLI to authenticate to Instagram."""

import os
import logging
from instagrapi import Client
from delayed_client import DelayedClient
from dotenv import load_dotenv


def main() -> None:
    """Load environment and attempt Instagram login."""
    logging.basicConfig(level=logging.DEBUG)
    load_dotenv()

    username = os.getenv("INSTAGRAM_LOGIN")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print(
            "Error: INSTAGRAM_LOGIN and INSTAGRAM_PASSWORD must be set in the .env file"
        )
        return

    min_delay = float(os.getenv("IG_DELAY_MIN", "2"))
    max_delay = float(os.getenv("IG_DELAY_MAX", "7"))
    jitter = float(os.getenv("IG_DELAY_JITTER", "0.5"))

    client = DelayedClient(min_delay=min_delay, max_delay=max_delay, jitter=jitter)
    try:
        client.login(username, password)
        print(f"Successfully logged in as {username}")
    except Exception as exc:
        print(f"Login failed: {exc}")


if __name__ == "__main__":
    main()
