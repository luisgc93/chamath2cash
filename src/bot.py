import logging
import re
from datetime import datetime, timedelta
from os import environ
from typing import List

from tweepy import Status

from .broker import AlpacaClient
from .twitter import TwitterClient
from .constants import CASHTAG, CHAMATH_TW_ID

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, twitter_client, broker):
        self.twitter = twitter_client
        self.broker = broker

    def get_new_tweets(self) -> List[Status]:
        statuses = self.twitter.api.user_timeline(user_id=CHAMATH_TW_ID, count=5)
        return [status for status in statuses if self._is_recent(status)]

    def _is_recent(self, status) -> bool:
        return datetime.now() - timedelta(minutes=2) <= status.created_at

    def tweet(self, status):
        self.twitter.api.update_status(status=status)

    def get_stocks(self, tweet):
        if CASHTAG in tweet:
            return list(
                set(
                    [ticker.strip("$") for ticker in re.findall(r"[$][A-Za-z]*", tweet)]
                )
            )

    def get_portfolio_value(self) -> str:
        return "${:,.2f}".format(float(self.broker.get_account().portfolio_value))

    def buy(self, ticker, amount) -> None:
        self.broker.api.submit_order(
            symbol=ticker, qty=amount, side="buy", type="market", time_in_force="gtc"
        )

    def sell(self, ticker, amount) -> None:
        self.broker.api.submit_order(
            symbol=ticker, qty=amount, side="sell", type="market", time_in_force="gtc"
        )


def run():
    twitter_client = TwitterClient(
        environ["CONSUMER_KEY"],
        environ["CONSUMER_SECRET"],
        environ["ACCESS_TOKEN"],
        environ["ACCESS_TOKEN_SECRET"],
    )
    broker = AlpacaClient(
        environ["APCA_API_KEY_ID"], environ["APCA_SECRET_KEY"], environ["APCA_BASE_URL"]
    )
    bot = Bot(twitter_client, broker)

    statuses = bot.get_new_tweets()
    for status in statuses:
        stocks = bot.get_stocks(status.text)
        if not stocks:
            continue
        for stock in stocks:
            bot.buy(stock, 1)
            original_tweet_url = f" https://twitter.com/chamath/status/{status.id}"
            portfolio = bot.get_portfolio_value()
            bot.tweet(
                f"Buying ${stock} 🚀. Current portfolio value: {portfolio} "
                f"{original_tweet_url}"
            )
