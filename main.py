import twitter_interface
import sqlite3

twitter = twitter_interface
trends = twitter.get_trending()
#print(*twitter.get_tweets_text(trends[0], 50), sep='\n')


#pulls trending tweets from twitter and then adds them to tweet_text table in database
conn = sqlite3.connect('data.dp')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS tweets (tweet_text TEXT)')
for trend in trends:
    trending_tweets = twitter.get_tweets_text(trend, 50)
    #add tweets to a database
    for i in range(len(trending_tweets)):
        c.execute("INSERT INTO tweets (tweet_text) VALUES(?)", (trending_tweets[i],))
        conn.commit()




c.close()
conn.close()

