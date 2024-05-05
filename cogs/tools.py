
import discord, asyncio
from discord.ext import commands
from discord import app_commands
import string
import random
from Bot.time_utils import get_time
from Bot.db_utils import ids


class Tools(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, limit:int):
        await ctx.channel.purge(limit=limit)
        embed = discord.Embed(title="Purge done", description=f"Successfully purged {limit} messages.")
        await ctx.send(embed=embed)

    @app_commands.command(
        name="password",
        description="Sends you a randomly generated secure password, decide its length as well. Minimum length 8.")
    async def password(self, interaction, pass_length: int = None):
        if pass_length is None or pass_length < 8:
            pass_length = 8
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation
        all_chars = lower+upper+num+symbols
        temp = random.sample(all_chars,int(pass_length))
        password = "".join(temp)
        embed = discord.Embed(
            title="Password generated, whatever you may use this for.",
            description=f"```\n{password}\n```",
            timestamp=get_time()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # # my most prized posession, the gorman command.
    # @app_command(guilds=ids,name="gorman",description="responds a picture of the goat")
    # async def gorman(self,interaction):
    #     embed = discord.Embed(title = "Gorman",color = discord.Colour.blue(),timestamp=datetime.now(tz))
    #     embed.set_author(name=interaction.user.name.name,icon_url=interaction.user.name.avatar.url)
    #     random_picture = random.choice(gorman_pictures)
    #     embed.set_image(url = random_picture)
    #     await interaction.response.send_message(embed=embed)

    @app_commands.command(name="membercount",description="Returns member count of server.")
    async def mc(self, interaction: discord.Interaction):
        guild = self.bot.get_guild(interaction.guild)
        embed = discord.Embed(
            title="Member Count:",
            description=str(guild.member_count) + " members in " + str(interaction.guild),
            color=0x2ecc71,
            timestamp=get_time())
        embed.set_author(name=f"{interaction.user.name}", icon_url=interaction.user.display_icon)
        return await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="info",description = "Gives you information on a user!")	
    async def info(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        try:
            embed = discord.Embed(title= f"Information of {member} ", description="", color=000000,
                                  timestamp=get_time())
            embed.set_author(name=member.name, icon_url=member.display_avatar.url)
            embed.add_field(
                name="Account creation date: ",
                value=member.created_at.strftime("%A, %B %d, %Y • %I:%M %p"),
                inline=False
            )
            embed.add_field(
                name="Miscellaneous:",
                value=f"{member.mention}'s Discord ID is: ```\n{member.id}\n```\n ",
                inline=False
            )
            embed.add_field(
                name=f"Joined this server named: {interaction.guild.name} ",
                value=member.joined_at.strftime("`%A, %B %d, %Y • %I:%M %p`")
            )
        except Exception:
            embed = discord.Embed(
                title="Could not retrieve information about member. ",
                description="", color=000000,
                timestamp=get_time()
            )
            embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        return await interaction.response.send_message(embed = embed)

    @app_commands.command(name="work", description="check if im online")
    async def work(self, interaction):
        embed = discord.Embed(title="Status 🟢", color=discord.Colour.blue(), timestamp=get_time())
        embed.add_field(name ="Latency", value=str(round(bot.latency*1000, 4)), inline=False)
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")


async def setup(bot):
    await bot.add_cog(Tools(bot), guilds = [discord.Object(id=ids)])