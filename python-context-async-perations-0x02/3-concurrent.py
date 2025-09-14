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
    Run both queries concurrently using asyncio.ga
