from unittest.mock import MagicMock

import pytest
from alpaca_trade_api.entity import Account

from src.bot import Bot


@pytest.fixture(autouse=True)
def bot():
    return Bot(twitter_client=MagicMock(), broker=MagicMock())


@pytest.fixture()
def account():
    return Account(
        {
            "buying_power": "400000",
            "cash": "100000",
            "created_at": "2021-02-06T16:07:44.291497Z",
            "currency": "USD",
            "daytrade_count": 0,
            "daytrading_buying_power": "400000",
            "equity": "100000",
            "last_equity": "100000",
            "long_market_value": "0",
            "maintenance_margin": "0",
            "multiplier": "4",
            "pattern_day_trader": False,
            "portfolio_value": "100000",
            "regt_buying_power": "200000",
            "short_market_value": "0",
            "shorting_enabled": True,
            "sma": "0",
            "status": "ACTIVE",
        }
    )


@pytest.fixture
def mock_get_account(bot, account):
    bot.broker.get_account.return_value = account
    yield bot
