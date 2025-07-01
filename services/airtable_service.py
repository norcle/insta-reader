from __future__ import annotations

import os
from typing import Iterable, Mapping

from dotenv import load_dotenv
from pyairtable import Table


def _get_table() -> Table:
    """Return an authenticated Airtable Table instance."""
    load_dotenv()
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME")

    if not api_key or not base_id or not table_name:
        raise RuntimeError(
            "AIRTABLE_API_KEY, AIRTABLE_BASE_ID and AIRTABLE_TABLE_NAME must be set in .env"
        )

    return Table(api_key, base_id, table_name)


def upsert_followers(followers: Iterable[Mapping[str, str]]) -> None:
    """Create or update follower records in Airtable."""
    table = _get_table()

    for follower in followers:
        username = follower.get("username")
        if not username:
            continue
        existing = table.first("username", username)
        if existing:
            table.update(existing["id"], follower)
        else:
            table.create(follower)
