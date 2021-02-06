from os import environ
from urllib.parse import quote_plus

import requests
import tweepy
from google.cloud import language_v1

from constants import MID_TO_TICKER_QUERY, WIKIDATA_QUERY_URL, WIKIDATA_QUERY_HEADERS


def init_tweepy():
    auth = tweepy.OAuthHandler(environ["CONSUMER_KEY"], environ["CONSUMER_SECRET"])
    auth.set_access_token(environ["ACCESS_TOKEN"], environ["ACCESS_TOKEN_SECRET"])
    return tweepy.API(auth)


def run():
    api = init_tweepy()
    statuses = api.user_timeline(screen_name="elonmusk")
    json_tweets = [status._json for status in statuses if status.in_reply_to_status_id is None]

    text = json_tweets[0]["text"]
    stocks = get_stocks(text)
    if stocks:
        api.update_status(status=f"Elon recommends buying {stocks[0]}")


def get_stocks(tweet):
    stocks = []
    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": tweet, "type_": type_, "language": language}
    response = client.analyze_entities(request={'document': document, 'encoding_type': language_v1.EncodingType.UTF8})
    for entity in response.entities:
        metadata = entity.metadata
        mid = metadata["mid"]
        company_data = get_company_data(mid)
        stocks += [data["ticker"] for data in company_data]

    return stocks


def get_company_data(mid):
    """Looks up stock ticker information for a company via its Knowledge Graph API ID.
    """
    ticker_bindings = make_wikidata_request(MID_TO_TICKER_QUERY % mid)
    companies = []
    if ticker_bindings:
        for binding in ticker_bindings:
            data = {
                "name": binding.get("companyLabel").get("value"),
                "ticker": binding.get("tickerLabel").get("value"),
                "exchange": binding.get("exchangeNameLabel").get("value"),
            }
            if data not in companies:
                companies.append(data)
    return companies


def make_wikidata_request(query):
    """Makes a request to the Wikidata SPARQL API."""
    query_url = WIKIDATA_QUERY_URL % quote_plus(query)
    response = requests.get(query_url, headers=WIKIDATA_QUERY_HEADERS)
    response.raise_for_status()
    response_json = response.json()
    results = response_json["results"]
    bindings = results["bindings"]

    return bindings
