import math

import discord
from discord import Embed
from discord.app_commands import Choice, choices, describe, command as slash_command
from discord.ext import commands
import asyncio
from Bot.time_utils import get_time
from Bot.db_utils import ids
from main import MyBot
from Coins.Coin import Coin
from Coins.CryptoCogHelper import *
import requests
from requests.exceptions import RequestException, HTTPError
import json


class CryptoCog(commands.Cog):

    def __init__(self, bot: MyBot):
        self.bot: MyBot = bot

    @slash_command(name="price", description="Get the price of a cryptocurrency")
    @describe(selected_coin="Select cryptocurrency")
    @choices(selected_coin=[
        Choice(name="Bitcoin", value=1),
        Choice(name="Ethereum", value=2),
        Choice(name="Litecoin", value=3),
    ])
    async def price(self, interaction: discord.Interaction, selected_coin: Choice[int]):
        try:
            coin: Coin = Coin(selected_coin.name)
            coin_full_name = coin.get_full_coin_name()
            coin_abbreviated_name = coin.get_abbreviated_coin_name()
            coin_icon_path = coin.get_coin_icon_path()
            coin_icon_file = discord.File(coin_icon_path, filename=f"{coin_full_name}.png")
            embed = Embed(
                title=f"Price for {coin_full_name} ({coin_abbreviated_name})",
                description="",
                timestamp=get_time()
            )
            embed.add_field(name="", value=coin.get_coin_price_to_string(), inline=False)
            embed.set_author(name=interaction.user.name)
            embed.set_thumbnail(url=f"attachment://{coin_full_name}.png")
            return await interaction.response.send_message(file=coin_icon_file, embed=embed)
        except NotImplementedError:
            embed = Embed(
                title="Coin not supported",
                description=f"{selected_coin.name} is not supported.",
                timestamp=get_time()
            )
            return await interaction.response.send_message(embed=embed)
        except RequestException:
            embed = Embed(
                title=f"Error fetching price for {selected_coin.name})",
                description="Please try again.",
                timestamp=get_time()
            )
            embed.set_author(name=interaction.user.name)
            return await interaction.response.send_message(embed=embed)

    @slash_command(name="convert", description="Convert from \n Crypto -> USD \n USD -> Crypto")
    @describe(conversion_format="Format")
    @choices(conversion_format=[
        Choice(name='Crypto to USD', value=1),
        Choice(name='USD to Crypto', value=2)
    ])
    @describe(selected_coin="Coin")
    @choices(selected_coin=[
        Choice(name='Bitcoin', value=1),
        Choice(name='Ethereum', value=2),
        Choice(name='Litecoin', value=3),
    ])
    async def convert(self, interaction: discord.Interaction, conversion_format: Choice[int],
                      selected_coin: Choice[int], amount: str):
        try:
            amount = amount.replace(',', '')
            amount = float(amount)
            coin: Coin = Coin(selected_coin.name)
            coin_full_name = coin.get_full_coin_name()
            coin_abbreviated_name = coin.get_abbreviated_coin_name()
            coin_icon_path = coin.get_coin_icon_path()
            coin_icon_file = discord.File(coin_icon_path, filename=f"{coin_full_name}.png")
            embed = Embed(
                title=conversion_format.name,
                description=f" {coin_full_name} ({coin_abbreviated_name})",
                timestamp=get_time()
            )
            if conversion_format.value == 1:
                value_string = coin.convert_coin_to_usd(amount)
            else:
                value_string = coin.convert_usd_to_coin(amount)
            embed.add_field(name="", value=value_string, inline=False)
            embed.set_author(name=interaction.user.name)
            embed.set_thumbnail(url=f"attachment://{coin_full_name}.png")
            return await interaction.response.send_message(file=coin_icon_file, embed=embed)
        except NotImplementedError:
            embed = Embed(
                title="Coin not supported",
                description=f"{selected_coin.name} is not supported.",
                timestamp=get_time()
            )
            return await interaction.response.send_message(embed=embed)
        except RequestException:
            embed = Embed(
                title=f"Error fetching price for {selected_coin.name})",
                description="Please try again.",
                timestamp=get_time()
            )
            embed.set_author(name=interaction.user.name)
            return await interaction.response.send_message(embed=embed)

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")


async def setup(bot):
    await bot.add_cog(CryptoCog(bot), guilds=[discord.Object(id=ids)])
