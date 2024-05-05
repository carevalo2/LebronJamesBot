import asyncpg.exceptions
import discord 
from discord.ext import commands
from discord import app_commands
from main import MyBot
from Bot.db_utils import ids
from Bot.time_utils import get_time


class Users(commands.Cog):

    def __init__(self, bot: MyBot):
        self.bot: MyBot = bot

    @app_commands.command(name="adduser", description="adds user to authorizedUsers")
    @commands.is_owner()
    async def adduser(self, interaction: discord.Interaction, member: discord.Member) -> None:
        try:
            await self.bot.execute("INSERT INTO authorizedUsers (user_discord_id, user_name) VALUES($1, $2)",
                                   member.id, member.name)
            embed = discord.Embed(title="Added authorized user to database.", color=discord.Colour.blue())
            embed.add_field(name="🟢 User added", value=member.name + "\n" + str(member.id), inline=False)
            await interaction.response.send_message(embed=embed)
        except asyncpg.exceptions.UniqueViolationError:
            embed = discord.Embed(title="User is already in database.", color=discord.Colour.blue())
            embed.add_field(name="No action taken.", value=member.name + "\n" + str(member.id), inline=False)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="removeuser", description="Removes a user from authorizedUsers")
    @commands.is_owner()
    async def removeuser(self, interaction: discord.Interaction, member: discord.Member) -> None:
        data = await self.bot.fetch("SELECT discord_user_id FROM authorizedUsers WHERE discord_user_id = $1", member.id)
        if not data:
            return await interaction.response.send_message(
                f"{member.name} ID: {member.id} is not an authorized user.", ephemeral=True)
        await self.bot.execute("DELETE FROM authorizedUsers WHERE user = $1", member.id)
        await interaction.response.send_message(
            f"Successfully removed {member.name} ID: {member.id} from authorized users.", ephemeral=True)

    @app_commands.command(name="getusers", description="Gets users from authorizedUsers")
    @commands.is_owner()
    async def getusers(self, interaction: discord.Interaction) -> discord.Embed | str:
        data = await self.bot.fetch("SELECT * FROM authorizedUsers")
        id_table = [f"ID: {row[0]}" for row in data]
        description = "\n".join(id_table)
        embed = discord.Embed(
            title="Authorized Users by ID",
            description=description,
            color=discord.Colour.blue(),
            timestamp=get_time(),
        )
        if not data:
            return await interaction.response.send_message("Current authorized user count is 0.", ephemeral=True)
        await interaction.response.send_message(embed=embed)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

            
async def setup(bot):
    await bot.add_cog(Users(bot), guilds=[discord.Object(id=ids)])