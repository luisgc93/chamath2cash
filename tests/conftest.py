from unittest.mock import patch

import pytest
from alpaca_trade_api.entity import Account


@pytest.fixture(autouse=True)
def mock_env_variables(monkeypatch):
    monkeypatch.setenv("CONSUMER_KEY", "123")
    monkeypatch.setenv("CONSUMER_SECRET", "123")
    monkeypatch.setenv("ACCESS_TOKEN", "123")
    monkeypatch.setenv("ACCESS_TOKEN_SECRET", "123")
    monkeypatch.setenv("BOT_USER_ID", "123")


@pytest.fixture(autouse=True)
def mock_tweepy_client():
    with patch("src.bot.init_tweepy") as mock:
        yield mock


@pytest.fixture(autouse=True)
def mock_alpaca_client():
    with patch("src.bot.init_alpaca") as mock:
        yield mock


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
def mock_get_account(mock_alpaca_client, account):
    mock_alpaca_client.return_value.get_account.return_value = account
    return mock_alpaca_client
