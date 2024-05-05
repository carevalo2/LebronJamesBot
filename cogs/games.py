import discord
from discord.ext import commands
from discord.ui import Button, View
from Bot.db_utils import ids
from Bot.time_utils import get_time


class UserSelectionView(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.player1_button = Button(style=discord.ButtonStyle.primary, label="Seller", row=0)
        self.player1_button.callback = self.select_player1
        self.add_item(self.player1_button)

        self.player2_button = Button(style=discord.ButtonStyle.primary, label="Buyer", row=0)
        self.player2_button.callback = self.select_player2
        self.add_item(self.player2_button)

        self.player1_selected = False
        self.player2_selected = False

    async def select_player1(self, interaction):
        if self.player1_selected:
            self.player1_selected = False
            self.player1_button.disabled = False
            self.player1_button.label = "Seller"
        else:
            self.player1_button.label = interaction.user.mention
            self.player1_selected = True
            if self.player2_selected:
                self.player2_selected = False
                self.player2_button.disabled = False
                self.player2_button.label = "Buyer"

        await interaction.response.edit_message(embed=self.get_embed())

    async def select_player2(self, interaction):
        if self.player2_selected:
            self.player2_selected = False
            self.player2_button.disabled = False
            self.player2_button.label = "Buyer"
        else:
            self.player2_button.label = interaction.user.mention
            self.player2_selected = True
            if self.player1_selected:
                self.player1_selected = False
                self.player1_button.disabled = False
                self.player1_button.label = "Seller"

        await interaction.response.edit_message(embed=self.get_embed())
    
    def get_embed(self):
        embed = discord.Embed(title="User Selection")
        embed.add_field(name="Seller", value="" if not self.player1_selected else self.player1_button.label, inline=False)
        embed.add_field(name="Buyer", value="" if not self.player2_selected else self.player2_button.label, inline=False)
        return embed


class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def deal(self, ctx):
        embed = discord.Embed(
            title="Deal Initiated",
            description="Choose the corresponding seller and buyer using the buttons below.",
            color=discord.Colour.orange())
        embed2 = discord.Embed(title="Seller & Buyer",timestamp=get_time(),color=discord.Colour.orange())
        view = UserSelectionView()
        await ctx.send(embed=embed, delete_after=2.5)
        await ctx.send(embed=embed2, view=view)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")


async def setup(bot):
    await bot.add_cog(Games(bot), guilds = [discord.Object(id=ids)])