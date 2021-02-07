from unittest.mock import call

import pytest
from src import bot


class TestBot:
    @pytest.mark.parametrize(
        "tweet, stock_tickers",
        [
            (
                "For those who are interested, here is "
                "the post in r/wsb drawing up the play to "
                "gamma squeeze $GME and send the HFs to the "
                "hospital. It’s a thing of beauty.",
                ["GME"],
            ),
            ("My latest climate investment: $SPRQ", ["SPRQ"]),
            (
                "My newest SaaS investment: $TSIA We just "
                "announced this morning that $TSIA is merging "
                "with @latchaccess and taking them public. "
                "This is the “???” from the tweet below.",
                ["TSIA"],
            ),
        ],
    )
    def test_returns_stock_tickers_when_tweet_contains_stocks(
        self, tweet, stock_tickers
    ):

        assert bot.get_stocks(tweet) == stock_tickers

    @pytest.mark.usefixtures("mock_get_account")
    def test_publishes_current_portfolio_value(
        self, mock_tweepy_client,
    ):
        expected_call = [
            call().update_status(
                status="My current portfolio value is: $100,000.00"
            ),
        ]

        bot.tweet_portfolio_value()

        assert expected_call in mock_tweepy_client.mock_calls
