import asyncio
import aiosqlite


async def async_fetch_users(db_name="users.db"):
    """Fetch all users asynchronously"""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users;") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users(db_name="users.db"):
    """Fetch users older than 40 asynchronously"""
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?;", (40,)) as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    """Run both queries concurrently using asyncio.gather"""
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    # Checks / print results
    print("All users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
