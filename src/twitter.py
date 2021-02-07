import sys

import tweepy


class TwitterClient:
    def __init__(self, api_key, api_key_secret, access_token, access_token_secret):
        print("Initialising tweepy client")
        sys.stdout.flush()
        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
