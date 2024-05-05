import math
import discord
from discord import app_commands
from discord.ext import commands
from Bot.time_utils import get_time
from Bot.db_utils import ids
from main import MyBot
import requests
import locale


class CryptoCurrencyCog(commands.Cog):

    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    def __init__(self, bot: MyBot):
        self.bot: MyBot = bot
        self.supported_coins_dict = {
            1: 'BTC',
            2: 'ETH',
            3: 'LTC'
        }

    @app_commands.command(name="price", description="Get the price of a cryptocurrency")
    @app_commands.describe(select_by="Select cryptocurrency")
    @app_commands.choices(select_by=[
        discord.app_commands.Choice(name='Bitcoin', value=1),
        discord.app_commands.Choice(name='Ethereum', value=2),
        discord.app_commands.Choice(name='Litecoin', value=3),
    ])
    async def price(self, interaction: discord.Interaction, select_by: discord.app_commands.Choice[int]):
        price = CryptoCurrencyCog.get_crypto_price_usd(self.supported_coins_dict.get(select_by.value))
        if price == -1:
            embed = discord.Embed(
                title=f"Error fetching {select_by.name} price. Try again!",
                description="",
                timestamp=get_time())
            embed.set_author(name=interaction.user.name)
            return await interaction.response.send_message(embed=embed)
        else:
            path_to_coin_image = f'CryptoCurrencyIcons/{select_by.name}.png'
            coin_image = discord.File(path_to_coin_image, filename=f"{select_by.name}.png")
            embed = discord.Embed(
                title=f"{select_by.name}",
                description="",
                timestamp=get_time(),
            )
            embed.add_field(name="Price", value=CryptoCurrencyCog.format_currency(price))
            embed.set_author(name=interaction.user.name)
            embed.set_thumbnail(url=f"attachment://{select_by.name}.png")
            return await interaction.response.send_message(file=coin_image, embed=embed)

    @app_commands.command(name="convert", description="Convert from crypto -> USD or USD -> crypto")
    @app_commands.describe(select_by="Format")
    @app_commands.choices(select_by=[
        discord.app_commands.Choice(name='Crypto to USD', value=1),
        discord.app_commands.Choice(name='USD to Crypto', value=2)
    ])
    @app_commands.describe(select_by2="Coin")
    @app_commands.choices(select_by2=[
        discord.app_commands.Choice(name='Bitcoin', value=1),
        discord.app_commands.Choice(name='Ethereum', value=2),
        discord.app_commands.Choice(name='Litecoin', value=3),
    ])
    async def convert(self, interaction: discord.Interaction, select_by: discord.app_commands.Choice[int], select_by2:
                    discord.app_commands.Choice[int], amount: str):
        path_to_coin_image = f'CryptoCurrencyIcons/{select_by2.name}.png'
        coin_image = discord.File(path_to_coin_image, filename=f"{select_by2.name}.png")
        if select_by.value == 1:
            output = CryptoCurrencyCog.convert_crypto_to_usd_formatted(
                amount, self.supported_coins_dict.get(select_by2.value))
        else:
            output = CryptoCurrencyCog.convert_usd_to_crypto_formatted(
                amount, self.supported_coins_dict.get(select_by2.value))
        embed = discord.Embed(
            title=f"{select_by.name}",
            description="",
            timestamp=get_time(),
        )
        if select_by.value == 1:
            embed.add_field(
                name="Output",
                value=f"{amount} {self.supported_coins_dict.get(select_by2.value)} is {output}")
        else:
            embed.add_field(
                name="Output",
                value=f"${float(amount):,.2f} USD is {output} {self.supported_coins_dict.get(select_by2.value)}")
        embed.set_author(name=interaction.user.name)
        embed.set_thumbnail(url=f"attachment://{select_by2.name}.png")
        return await interaction.response.send_message(file=coin_image, embed=embed)

    @staticmethod
    def format_currency(number: str) -> str:
        number = float(number)
        number = math.ceil(number * 100) / 100
        return f"${number:,.2f}"

    @staticmethod
    def get_crypto_price_usd(coin: str):
        try:
            if not CryptoCurrencyCog.is_supported_coin(coin):
                return -1
            response = requests.get(f"https://api.coinbase.com/v2/prices/{coin}-USD/spot")
            data = response.json()
            return data["data"]["amount"]
        except Exception:
            return -1

    @staticmethod
    def get_usd_price_crypto(coin: str):
        try:
            if not CryptoCurrencyCog.is_supported_coin(coin):
                return -1
            response = requests.get(f"https://api.coinbase.com/v2/prices/USD-{coin}/spot")
            data = response.json()
            return data["data"]["amount"]
        except Exception:
            return -1

    @staticmethod
    def convert_crypto_to_usd_formatted(amount: int, selected_coin: str):
        return CryptoCurrencyCog.format_currency(
            float(amount) * float(CryptoCurrencyCog.get_crypto_price_usd(selected_coin)))

    @staticmethod
    def convert_usd_to_crypto_formatted(usd_amount: str, selected_coin: str):
        return f"{float(usd_amount) * float(CryptoCurrencyCog.get_usd_price_crypto(selected_coin)):.8f}"

    @staticmethod
    def is_supported_coin(coin: str) -> bool:
        return coin in ('BTC', 'ETH', 'LTC')

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")


async def setup(bot):
    await bot.add_cog(CryptoCurrencyCog(bot), guilds=[discord.Object(id=ids)])
