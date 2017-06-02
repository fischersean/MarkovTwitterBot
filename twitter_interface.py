import tweepy
import json
import USER_KEYS

USWOEID = 23424977


def init_API(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.wait_on_rate_limit = True
    return api


def tweet(message):
    api = init_API(USER_KEYS.consumer_key, USER_KEYS.consumer_secret, USER_KEYS.access_token,
                   USER_KEYS.access_token_secret)
    if len(message) < 140:
        api.update_status(message)
    else:
        print("Message longer than 140 characters")

    return

#Top 10 trending topics
def get_trending():
    api = init_API(USER_KEYS.consumer_key, USER_KEYS.consumer_secret, USER_KEYS.access_token,
                   USER_KEYS.access_token_secret)
    trendsPulled = api.trends_place(USWOEID)
    trends = []
    for trend in trendsPulled[0]['trends']:
        trends.append(trend['name'])
    return trends

#Top n results for a given search parameter
def get_tweets_text(search_term, count):
    api = init_API(USER_KEYS.consumer_key, USER_KEYS.consumer_secret, USER_KEYS.access_token,
                   USER_KEYS.access_token_secret)
    search_result = api.search(search_term, count=count)
    tweets = []
    for status in search_result:
        tweets.append(status.text)
    return tweets


def rate_limit():
    api = init_API(USER_KEYS.consumer_key, USER_KEYS.consumer_secret, USER_KEYS.access_token,
                   USER_KEYS.access_token_secret)
    return api.rate_limit_status()
