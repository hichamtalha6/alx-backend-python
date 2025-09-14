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


async def check_functions():
    """Run both functions concurrently and perform simple checks"""
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:")
    for user in all_users:
        print(user)

    print("\nUsers older than 40:")
    for user in older_users:
        print(user)

    # Basic programmatic checks
    assert isinstance(all_users, list), "async_fetch_users() should return a list"
    assert isinstance(older_users, list), "async_fetch_older_users() should return a list"

    # Ensure all older_users are actually older than 40
    for user in older_users:
        age = user[2]  # assuming age is the 3rd column
        assert age > 40, f"Found user with age <= 40: {age}"

    print("\nAll checks passed!")


if __name__ == "__main__":
    asyncio.run(check_functions())
