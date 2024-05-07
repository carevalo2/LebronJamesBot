import asyncpg
import os
from dotenv import load_dotenv
# Replace 'database_url' with your actual PostgreSQL database URL
load_dotenv()
ids = int(os.getenv('guild_id'))
DATABASE_URL = f"postgres://postgres:{os.getenv('db_password')}@localhost:5432/DiscordBot"


async def get_guild_ids() -> list[int]:
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        rows = await conn.fetch("SELECT guild_id FROM guilds")
        return [row['guild_id'] for row in rows]
    finally:
        await conn.close()


async def add_guild_id(guild_id, guild_name, added_by, added_at_time):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute("""
            INSERT INTO guilds (guild_id, guild_name, added_by, added_at_time)
            VALUES ($1, $2, $3, $4)
        """, guild_id, guild_name, added_by, added_at_time)
    except asyncpg.PostgresError as e:
        return f"PostgreSQL error: {e}"
    finally:
        await conn.close()


async def remove_guild_id(user_input: int, select_by: int):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        if select_by == 1:
            result = await conn.execute("DELETE FROM guilds WHERE guild_id = $1", user_input)
        elif select_by == 2:
            result = await conn.execute("DELETE FROM guilds WHERE guild_number = $1", user_input)
        return "DELETE 1" in result
    except asyncpg.PostgresError as e:
        print(e)
        return False
    finally:
        await conn.close()
