import tweepy
import USER_KEYS

USWOEID = 23424977

def init_API():
    auth = tweepy.OAuthHandler(USER_KEYS.consumer_key, USER_KEYS.consumer_secret)
    auth.set_access_token(USER_KEYS.access_token, USER_KEYS.access_token_secret)
    api = tweepy.API(auth)
    api.wait_on_rate_limit = True
    return api


def tweet(api, message):
    if len(message) < 140:
        api.update_status(message)
    else:
        print("Message longer than 140 characters")

    return

#Top 10 trending topics
def get_trending(api):
    trendsPulled = api.trends_place(USWOEID)
    trends = []
    for trend in trendsPulled[0]['trends']:
        trends.append(trend['name'])
    return trends

#Top n results for a given search parameter
def get_tweets_text(api, search_term, count):
    search_result = api.search(search_term, count=count, lang="eng")
    tweets = []
    for status in search_result:
        tweets.append(status.text)
    return tweets


def rate_limit(api):
    return api.rate_limit_status()
