import requests
from requests.exceptions import RequestException, HTTPError
from typing import Final

# Parent class of all crypto coins. I can probably get rid of the restriction, but for now, I've only thoroughly tested
# BTC, ETH, and LTC. This means I also have to get a bunch of icons :)


class Coin:

    supported_coins: Final[dict] = {
        'Bitcoin': 'BTC',
        'Ethereum': 'ETH',
        'Litecoin': 'LTC'
    }

    def __init__(self, full_coin_name: str, amount: float = None) -> None:
        self.full_coin_name = full_coin_name
        self.abbreviated_coin_name = Coin.supported_coins.get(self.full_coin_name)
        self.amount = amount
        if self.abbreviated_coin_name is None:
            raise NotImplementedError("Coin is not supported.")
        self.coin_price_usd_url = f"https://api.coinbase.com/v2/prices/{self.abbreviated_coin_name}-USD/spot"
        self.usd_price_coin_url = f"https://api.coinbase.com/v2/prices/USD-{self.abbreviated_coin_name}/spot"
        self.coin_icon_path = f"Coins/CryptocurrencyIcons/{self.full_coin_name}.png"

    def get_coin_price_usd(self) -> float | None:
        try:
            response = requests.get(self.coin_price_usd_url)
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                raise RequestException
            return float(data["data"]["amount"])
        except RequestException:
            raise RequestException

    def get_usd_price_coin(self) -> float | None:
        try:
            response = requests.get(self.usd_price_coin_url)
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                raise RequestException
            return float(data["data"]["amount"])
        except RequestException:
            raise RequestException

    def convert_to_usd(self, coin_amount: float) -> float | None:
        coin_price_usd = get_coin_price_usd(self)
        return coin_price_usd * coin_amount

    def get_abbreviated_coin_name(self) -> str:
        return self.abbreviated_coin_name

    def get_full_coin_name(self) -> str:
        return self.full_coin_name

    def get_coin_icon_path(self) -> str:
        return self.coin_icon_path

    def get_coin_price_to_string(self) -> str:
        return f"${self.get_coin_price_usd():,.2f}"

    def convert_coin_to_usd(self, amount: float) -> str:
        coin_amount_to_usd = self.get_coin_price_usd() * amount
        formatted_amount = f"{amount:,.8f}".rstrip('0')
        if formatted_amount.endswith('.'):
            formatted_amount = formatted_amount[:-1]
        return f"{formatted_amount} {self.get_abbreviated_coin_name()} is ${coin_amount_to_usd:,.2f}"

    def convert_usd_to_coin(self, amount: float) -> str:
        amount_in_formatted_usd = f"${amount:,.2f}"
        return f"{amount_in_formatted_usd} is " \
               f"{amount * self.get_usd_price_coin():.8f} {self.get_abbreviated_coin_name()}"
