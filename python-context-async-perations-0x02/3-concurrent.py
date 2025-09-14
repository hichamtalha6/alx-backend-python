#!/usr/bin/env python3
"""
Run multiple database queries concurrently using asyncio and aiosqlite
"""

import asyncio
import aiosqlite


async def async_fetch_users(db_name="users.db"):
    """
    Fetch all users asynchronously
    """
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users;") as cursor:
            results = await cursor.fetchall()
            return results


async def async_fetch_older_users(db_name="users.db"):
    """
    Fetch users older than 40 asynchronously
    """
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?;", (40,)) as cursor:
            results = await cursor.fetchall()
            return results


async def fetch_concurrently():
    """
    Execute both queries concurrently using asyncio.gather
    """
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:")
    for row in all_users:
        print(row)

    print("\nUsers older than 40:")
    for row in older_users:
        print(row)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
