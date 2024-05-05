import discord
from discord import app_commands
from discord.ext import commands
import asyncio
from Bot.time_utils import get_time
from Bot.db_utils import ids
from main import MyBot


class CogManagerView(discord.ui.View):
    def __init__(self, bot, cog_names):
        super().__init__(timeout=None)  # Persistent view
        self.bot = bot
        self.selected_cog = None

        # Dropdown for cog selection
        self.select = discord.ui.Select(custom_id="select", placeholder='Choose a cog')
        for cog in cog_names:
            self.select.add_option(label=cog, value=cog, description=f'Load/unload/reload the {cog} cog')
        self.select.callback = self.select_callback  # Attach the callback
        self.add_item(self.select)

        # Buttons for Load, Unload, and Reload
        self.load_button = discord.ui.Button(label='Load', style=discord.ButtonStyle.green,
                                             custom_id='load_cog')
        self.load_button.callback = self.load_cog  # Attach the callback
        self.add_item(self.load_button)

        self.unload_button = discord.ui.Button(label='Unload', style=discord.ButtonStyle.red,
                                               custom_id='unload_cog')
        self.unload_button.callback = self.unload_cog  # Attach the callback
        self.add_item(self.unload_button)

        self.reload_button = discord.ui.Button(label='Reload', style=discord.ButtonStyle.blurple,
                                               custom_id='reload_cog')
        self.reload_button.callback = self.reload_cog  # Attach the callback
        self.add_item(self.reload_button)

    async def select_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.selected_cog = interaction.data['values'][0]

    async def load_cog(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.selected_cog is not None:
            try:
                await self.bot.load_extension(f'cogs.{self.selected_cog}')
                embed = discord.Embed(title="Successfully loaded cog", description=self.selected_cog,
                                      timestamp=discord.utils.utcnow())
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                message = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
            except Exception as e:
                embed = discord.Embed(title="Failed to load cog", description=str(e), timestamp=discord.utils.utcnow())
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                message = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()

    async def unload_cog(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.selected_cog is not None:
            try:
                await self.bot.unload_extension(f'cogs.{self.selected_cog}')
                embed = discord.Embed(title="Successfully unloaded cog", description=self.selected_cog,
                                      timestamp=discord.utils.utcnow())
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                message = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
            except Exception as e:
                embed = discord.Embed(title="Failed to unload cog", description=str(e),
                                      timestamp=discord.utils.utcnow())
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                message = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()

    async def reload_cog(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if self.selected_cog is not None:
            try:
                await self.bot.reload_extension(f'cogs.{self.selected_cog}')
                embed = discord.Embed(title="Successfully reloaded cog", description=self.selected_cog,
                                      timestamp=discord.utils.utcnow())
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                message = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()
            except Exception as e:
                embed = discord.Embed(title="Failed to reload cog", description=str(e),
                                      timestamp=discord.utils.utcnow())
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                message = await interaction.followup.send(embed=embed)
                await asyncio.sleep(5)
                await message.delete()


class CogHelper(commands.Cog):
    def __init__(self, bot):
        self.bot: MyBot = bot

    @commands.is_owner()
    @commands.command()
    async def load(self, ctx, cog: str):
        try:
            await self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(title="load", description=f"Could not load the `{e}` cog.")
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="Load", description=f"Successfully loaded the `{cog}` cog.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(title="Unload", description=f"{e}")
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="Unload", description=f"Successfully unloaded the `{cog}` cog.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
        except Exception as e:
            embed = discord.Embed(title="Reload", description=f"{e}")
            await ctx.send(embed=embed)
            return
        embed = discord.Embed(title="Reload", description=f"Successfully reloaded the `{cog}` cog.")
        await ctx.send(embed=embed)

    @app_commands.command(name="manage_cogs", description="Manages cogs.")
    async def manage_cogs(self, interaction: discord.Interaction):
        cog_names = await self.bot.get_cog_names()
        view = CogManagerView(self.bot, cog_names)
        await interaction.response.send_message(view=view)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")


async def setup(bot):
    await bot.add_cog(CogHelper(bot), guilds=[discord.Object(id=ids)])
