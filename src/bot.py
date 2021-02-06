from os import environ

import tweepy
import alpaca_trade_api as tradeapi


def init_tweepy():
    auth = tweepy.OAuthHandler(environ["CONSUMER_KEY"], environ["CONSUMER_SECRET"])
    auth.set_access_token(environ["ACCESS_TOKEN"], environ["ACCESS_TOKEN_SECRET"])
    return tweepy.API(auth)


def buy(ticker):
    api = tradeapi.REST(
        key_id=environ["APCA_API_KEY_ID"],
        secret_key=environ["APCA_SECRET_KEY"],
        base_url=environ["APCA_BASE_URL"]
    )

    api.submit_order(
        symbol=ticker,
        qty=1,
        side='buy',
        type='market',
        time_in_force='gtc'
    )


def sell(ticker):
    api = tradeapi.REST(
        key_id=environ["APCA_API_KEY_ID"],
        secret_key=environ["APCA_SECRET_KEY"],
        base_url=environ["APCA_BASE_URL"]
    )

    api.submit_order(
        symbol=ticker,
        qty=1,
        side='sell',
        type='market',
        time_in_force='gtc'
    )


def run():
    api = init_tweepy()
    statuses = api.user_timeline(screen_name="chamath")
    json_tweets = [status._json for status in statuses if status.in_reply_to_status_id is None]
    text = json_tweets[0]["text"]
    stocks = get_stocks(text)

    if stocks:
        api.update_status(status=f"Chamath recommends buying {stocks[0]}")


def get_stocks(tweet):
    return ["TSLA"]
