import json
from binance.client import Client

class CriptoBot:
    def __init__(self, config_path="config.json"):
        # Carregar configurações
        with open(config_path, "r") as f:
            self.config = json.load(f)

        # Inicializar cliente da Binance
        self.client = Client(self.config["api_key"], self.config["api_secret"])

    def get_balance(self):
        # Obtém o saldo disponível
        account = self.client.get_account()
        balances = {asset["asset"]: float(asset["free"]) for asset in account["balances"]}
        return balances

    def get_price_data(self, pair):
        """
        Obtém o preço atual e a variação percentual de um par específico.
        """
        ticker = self.client.get_ticker(symbol=pair)
        return float(ticker["lastPrice"]), float(ticker["priceChangePercent"])
