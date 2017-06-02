import twitter
import json
import USER_KEYS


def init_API(consumer_key, consumer_secret, access_token, access_token_secret):
    api = twitter.Api(consumer_key,
                      consumer_secret,
                      access_token,
                      access_token_secret,
                      sleep_on_rate_limit=True)
    return api


def tweet(message):
    api = init_API(USER_KEYS.consumer_key, USER_KEYS.consumer_secret, USER_KEYS.access_token,
                   USER_KEYS.access_token_secret)
    if len(message) < 140:
        api.PostUpdate(message)
    else:
        print("Message longer than 140 characters")

    return


def get_trending():
    api = init_API(USER_KEYS.consumer_key, USER_KEYS.consumer_secret, USER_KEYS.access_token,
                   USER_KEYS.access_token_secret)
    trends = api.GetTrendsCurrent()
    return trends


def get_tweet():
    return


#def

