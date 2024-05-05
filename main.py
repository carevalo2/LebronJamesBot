import os
import discord
from discord.ext import commands
from typing import Literal, Optional
import asyncpg
import asyncio
from dotenv import load_dotenv

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix='-',
            intents=intents
        )
        self.db = None
        self.cog_names = []

    async def setup_hook(self) -> None:
        self.db = await asyncpg.create_pool(database='DiscordBot', user='postgres', password=os.getenv("db_password"))
        await self.execute("""
            CREATE TABLE IF NOT EXISTS guilds(
                guild_number bigserial PRIMARY KEY,
                guild_id bigint UNIQUE,
                guild_name VARCHAR(30),
                added_by VARCHAR(30),
                added_at_time date
            );
        """)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS commandHistory(
                command_number bigserial PRIMARY KEY,
                command_used VARCHAR(32),
                author_username VARCHAR(32),
                author_userid bigint,
                used_at_time date
            );
        """)
        await self.execute("""
            CREATE TABLE IF NOT EXISTS authorizedUsers(
                user_discord_id bigserial PRIMARY KEY,
                user_name VARCHAR(32)
            );
        """)
        for files in os.listdir('./cogs'):
            if files.endswith('.py'):
                await self.load_extension(f"cogs.{files[:-3]}")

    async def get_cog_names(self):
        return self.cog_names

    async def fetch(self, query, *args):
        async with self.db.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute(self, query, *args):
        async with self.db.acquire() as connection:
            return await connection.execute(query, *args)


async def main() -> None:
    load_dotenv()
    bot = MyBot()

    @bot.event
    async def on_ready():
        print(f"Logged in as user {bot.user}")

    @bot.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object],
                   spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    await bot.start(os.getenv("discord_token"))

if __name__ == '__main__':
    asyncio.run(main())

