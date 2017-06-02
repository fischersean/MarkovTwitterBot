import twitter_interface


twitter = twitter_interface
trends = twitter.get_trending()
#print(twitter.rate_limit())
for trend in trends:
    print(*twitter.get_tweets_text(trend), sep='\n')
#print(trends)

