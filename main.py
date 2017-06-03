import twitter_interface
import sqlite3


print("Loading Twitter Module")
twitter = twitter_interface
print("Getting trends")
trends = twitter.get_trending()

# print(*twitter.get_tweets_text(trends[0], 50), sep='\n')

# pulls trending tweets from twitter and then adds them to tweet_text table in database
print("Creating Database")
conn = sqlite3.connect('data.dp')
c = conn.cursor()

print("Retrieving tweets")
# c.execute('CREATE TABLE IF NOT EXISTS tweets (tweet_text TEXT)')
# for trend in trends:
#     trending_tweets = twitter.get_tweets_text(trend, 50)
#     #add tweets to a database
#     for i in range(len(trending_tweets)):
#         c.execute("INSERT INTO tweets (tweet_text) VALUES(?)", (trending_tweets[i],))
#         conn.commit()

# for each tweet seperate words and determine word pairs
c.execute('CREATE TABLE IF NOT EXISTS markovs_words ( word_before TEXT, word_after TEXT, instances INTEGER, probability REAL )')

# gets tweet text from database
c.execute("""SELECT * FROM tweets""")
full_tweets = c.fetchall()
tweets = []

print("Parsing words")
# splits tweets up into individual words
for line in full_tweets:
    tweets.append(line[0].split(" "))

print("Determining word pairs")
# determines how many instances of each word pair there are
# word_before = ""
# word_after = ""
# for tweet in tweets:
#     for word in tweet:
#         word_after = word
#         query_result1 = c.execute("SELECT * FROM markovs_words WHERE word_before = ?", (word_before,))
#         data1 = query_result1.fetchall()
#         if len(data1) !=0: #If 1st word is found in database, check for 2nd word
#             query_result2 = c.execute("SELECT * FROM markovs_words WHERE word_after = ? AND word_before=?",(word_after, word_before,))
#             data2 = query_result2.fetchone()
#             if data2 != None: #If word pair is found, add 1 to instances
#                 instances_of_pair = data2[2]
#                 instances_of_pair = instances_of_pair + 1
#                 c.execute("UPDATE markovs_words SET instances = ? WHERE word_before = ? AND word_after = ?",(instances_of_pair,word_before,word_after,))
#                 conn.commit()
#             else: #if second word isnt found, create new instance of that pair
#                 c.execute("INSERT INTO markovs_words (word_before,word_after,instances, probability) VALUES (?,?,?,?)"
#                           , (word_before, word_after, 1, 1,))
#                 conn.commit()
#         else: #If word pair isnt found, create a new instances of that pair
#             c.execute("INSERT INTO markovs_words (word_before,word_after,instances, probability) VALUES (?,?,?,?)"
#                       , (word_before, word_after, 1, 1,))
#             conn.commit()
#
#         word_before = word

print("Determining probabilities")

c.close()
conn.close()
