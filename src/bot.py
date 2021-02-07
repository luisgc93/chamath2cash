import logging
import re
import sys
from datetime import datetime, timedelta
from os import environ

import tweepy
import alpaca_trade_api as tradeapi

from .constants import CASHTAG, CHAMATH_TW_ID

logger = logging.getLogger(__name__)


def init_tweepy():
    logger.info("Initialising tweepy client")
    sys.stdout.flush()
    auth = tweepy.OAuthHandler(environ["CONSUMER_KEY"], environ["CONSUMER_SECRET"])
    auth.set_access_token(environ["ACCESS_TOKEN"], environ["ACCESS_TOKEN_SECRET"])
    return tweepy.API(auth)


def init_alpaca():
    return tradeapi.REST(
        key_id=environ["APCA_API_KEY_ID"],
        secret_key=environ["APCA_SECRET_KEY"],
        base_url=environ["APCA_BASE_URL"]
    )


def run():
    api = init_tweepy()
    statuses = api.user_timeline(user_id=CHAMATH_TW_ID, count=5)
    for status in statuses:
        stocks = get_stocks(status.text)
        if not stocks:
            continue
        for stock in stocks:
            if datetime.now() - timedelta(minutes=2) <= status.created_at:
                original_tweet_url = f"https://twitter.com/chamath/status/{status.id}"
                api.update_status(status=f"Buying ${stock} 🚀 {original_tweet_url}")
                init_alpaca().submit_order(
                    symbol=stock,
                    qty=1,
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )


def get_stocks(tweet):
    if CASHTAG in tweet:
        return re.findall(r"[$][A-Za-z]*", tweet)
