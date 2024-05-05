
import discord
from discord import app_commands
from discord.ext import commands
from Bot.time_utils import get_time_formatted
from Bot.db_utils import add_guild_id, remove_guild_id, ids
from main import MyBot
from HistoryView import HistoryView


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot: MyBot = bot

    @app_commands.command(name="get_authorized_guilds", description="Returns authorized guilds allowed to use commands.")
    async def get_authorized_guilds(self, interaction: discord.Interaction) -> discord.Embed | str:
        rows = await self.bot.fetch("SELECT * FROM guilds")
        embeds = []
        for start in range(0, len(rows), 10):
            embed = discord.Embed(title="Authorized Guilds", color=0x00ff00)
            for row in rows[start:start + 10]:
                guild_number, guild_id, guild_name, added_by, added_at_time = row
                embed.add_field(name = f" {guild_number}. {guild_name} (ID: {guild_id})",
                                value=f"Added by: {added_by}\nAdded on: {added_at_time}", inline=False)
            embeds.append(embed)
        if not embeds:
            await interaction.response.send_message("No authorized guilds found.", ephemeral=True)
            return
        view = HistoryView(embeds, interaction.user)
        await interaction.response.send_message(embed=embeds[0], view=view)

    @app_commands.command(name="add_guild", description="Adds a guild ID to authorized guilds.")
    async def add_guild(self, interaction: discord.Interaction, guild_name: str, guild_id: str) -> discord.Embed:
        added_by = f"{interaction.user.name} (ID: {interaction.user.id})"
        added_at_time = get_time()
        await add_guild_id(int(guild_id), guild_name, added_by, added_at_time)
        embed = discord.Embed(title=f"Successfully added {guild_name} to authorized guilds.", color=0x00ff00)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove_guild", description="Removes a guild ID from authorized guilds.")
    @app_commands.describe(select_by="Select by guild id or index number from database.")
    @app_commands.choices(select_by=[
        discord.app_commands.Choice(name='Guild ID', value=1),
        discord.app_commands.Choice(name='Database ID', value=2)
    ])
    async def remove_guild(self, interaction: discord.Interaction, select_by: discord.app_commands.Choice[int],
                           user_input: str,) -> discord.Embed:
        if not user_input.isdigit():
            await interaction.response.send_message("Invalid input. Please provide a valid guild id.", ephemeral=True)
            return
        try:
            result = await remove_guild_id(int(user_input), select_by.value)
            if result:
                embed = discord.Embed(title=f"Successfully removed guild ID {user_input} from authorized guilds.",
                                      color=0x00ff00)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"No matching guild found for ID {input}.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Failed to remove guild: {e}", ephemeral=True)

    async def cog_load(self) -> None:
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self) -> None:
        print(f"{self.__class__.__name__} unloaded!")


async def setup(bot):
    await bot.add_cog(Database(bot), guilds = [discord.Object(id=ids)])
