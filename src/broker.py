import alpaca_trade_api as tradeapi


class AlpacaClient:
    def __init__(self, api_key_id, api_key_secret, base_url):
        self.api = tradeapi.REST(
            key_id=api_key_id, secret_key=api_key_secret, base_url=base_url
        )
