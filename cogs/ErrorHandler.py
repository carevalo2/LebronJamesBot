
import discord
from discord import app_commands
from Bot.db_utils import ids
from Bot.time_utils import get_time
from discord.ext import commands
from discord.ext.commands import CommandError

class ErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # def cog_load(self):
    #     print(f"{self.__class__.__name__} loaded!")
    #     tree = self.bot.tree
    #     self._old_tree_error = tree.on_error
    #     tree.on_error = self.on_app_command_error

    # def cog_unload(self):
    #     tree = self.bot.tree
    #     tree.on_error = self._old_tree_error

    # @commands.Cog.listener()
    # async def on_app_command_error(
    #     self,
    #     interaction: discord.Interaction,
    #     error: app_commands.AppCommandError
    # ):
    #     await interaction.response.send_message(error)
    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, error: CommandError):
    #     embed = discord.Embed(title = "Error", description = error, timestamp = get_time())
    #     ctx.send(embed = embed)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot), guilds = [discord.Object(id=ids)])