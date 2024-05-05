import discord
from discord import app_commands
from discord.ext import commands
from HistoryView import HistoryView
from Bot.time_utils import get_time
from Bot.db_utils import ids
from main import MyBot


class CommandHistory(commands.Cog):
    def __init__(self, bot: MyBot):
        self.bot: MyBot = bot

    @app_commands.command(name="history", description="Gets commands used history.")
    async def history(self, interaction: discord.Interaction) -> discord.Embed | str:
        rows = await self.bot.fetch("SELECT * FROM commandHistory ORDER BY command_number")
        embeds = []
        commands_per_page = 5
        for i in range(0, len(rows), commands_per_page):
            embed = discord.Embed(title="Command History", color=0x00FF00)
            for row in rows[i: i + commands_per_page]:
                (
                    command_number,
                    command_used,
                    author_username,
                    author_userid,
                    used_at_time,
                ) = row
                embed.add_field(
                    name=f"{command_number}. {command_used}",
                    value=f"User: {author_username} "
                          f"({author_userid})\nTime: "
                          f"{used_at_time}",
                    inline=False,
                )
            embeds.append(embed)
        if not embeds:
            return await interaction.response.send_message(
                "No command history found.", ephemeral=True
            )
        view = HistoryView(embeds, interaction.user)
        await interaction.response.send_message(embed=embeds[0], view=view)

    @app_commands.command(name="clearhistory", description="Clears command history")
    @commands.has_permissions(administrator=True)
    async def clearhistory(self, interaction: discord.Interaction) -> None:
        await self.bot.execute("DELETE FROM commandHistory")
        await interaction.response.send_message(
            embed=discord.Embed(
                title="Command History Cleared", description="", color=0x00FF00
            )
        )

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, _) -> None:
        data = interaction.data
        name = data.get("name")
        if name in ["clearhistory", "gethistory", "history"]:
            return
        timestamp = get_time()
        await self.bot.execute("""
            INSERT INTO commandHistory (
                command_used, 
                author_username, 
                author_userid, 
                used_at_time
            )
            VALUES ($1, $2, $3, $4)""",
                               name,
                               interaction.user.name,
                               interaction.user.id,
                               timestamp,
                               ),

    @commands.Cog.listener()
    async def on_command_completion(self, interaction: discord.Interaction) -> None:
        if interaction.command.name in ["clearhistory", "gethistory", "history"]:
            return
        timestamp = get_time()
        await self.bot.execute("""
        INSERT INTO commandHistory(
        command_used, author_username, author_userid, used_at_time)
        VALUES ($1,$2,$3,$4)""",
                               interaction.command.name,
                               interaction.author.name,
                               interaction.author.id,
                               timestamp
                               )

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")


async def setup(bot):
    await bot.add_cog(CommandHistory(bot), guilds=[discord.Object(id=ids)])
