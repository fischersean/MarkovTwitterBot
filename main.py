import twitter_interface
import sqlite3
import random
import time

start_time = time.time()
print("Loading Twitter Module")
twitter = twitter_interface
api = twitter.init_API()
print("Getting trends")
trends = twitter.get_trending(api)

#creates database to store infomration
print("Creating Database")
conn = sqlite3.connect('data.dp')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS markovs_words")
c.execute("DROP TABLE IF EXISTS tweets")

c.execute('CREATE TABLE IF NOT EXISTS tweets (tweet_text TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS markovs_words ( word_before TEXT, word_after TEXT, instances INTEGER, probability REAL, counted INTEGER )')

#pulls trending tweets from twitter and then adds them to tweet_text table in database
print("Retrieving tweets")
for trend in trends:
    trending_tweets = twitter.get_tweets_text(api, trend, 10)
    #add tweets to a database
    for i in range(len(trending_tweets)):
        c.execute("INSERT INTO tweets (tweet_text) VALUES(?)", (trending_tweets[i],))
        conn.commit()

get tweets from database
c.execute("""SELECT * FROM tweets""")
full_tweets = c.fetchall()
tweets = []
print("Parsing words")
# splits tweets up into individual words
for line in full_tweets:
    tweets.append(line[0].split(" "))

print("Determining word pairs")
# determines how many instances of each word pair there are
word_before = ""
word_after = ""
for tweet in tweets:
    tweet = [x for x in tweet if x != "RT" and x[:1] != "@"]
    for word in tweet:
        word_after = word
        query_result1 = c.execute("SELECT * FROM markovs_words WHERE word_before = ?", (word_before,))
        data1 = query_result1.fetchall()
        if len(data1) !=0: #If 1st word is found in database, check for 2nd word
            query_result2 = c.execute("SELECT * FROM markovs_words WHERE word_after = ? AND word_before=?",(word_after, word_before,))
            data2 = query_result2.fetchone()
            if data2 != None: #If word pair is found, add 1 to instances
                instances_of_pair = data2[2]
                instances_of_pair = instances_of_pair + 1
                c.execute("UPDATE markovs_words SET instances = ? WHERE word_before = ? AND word_after = ?",(instances_of_pair,word_before,word_after,))
                conn.commit()
            else: #if second word isnt found, create new instance of that pair
                c.execute("INSERT INTO markovs_words (word_before,word_after,instances, probability) VALUES (?,?,?,?)"
                          , (word_before, word_after, 1, 1,))
                conn.commit()
        else: #If word pair isnt found, create a new instances of that pair
            c.execute("INSERT INTO markovs_words (word_before,word_after,instances, probability) VALUES (?,?,?,?)"
                      , (word_before, word_after, 1, 1,))
            conn.commit()

        word_before = word

word_before = ""
word_after = ""
print("Determining probabilities")
probability = 0
for tweet in tweets:
    for word in tweet:
        word_after = word
        query_result1 = c.execute("SELECT * FROM main.markovs_words WHERE word_before = ?",(word_before,))
        data1 = query_result1.fetchall()
        total_instances = 0
        #Determine total number of times given word_before apears
        if data1 != []:
            if data1[0][4] == None:
                for i in range (len(data1)):
                    total_instances = total_instances + data1[i][2]
                for i in range(len(data1)):
                    probability = data1[i][2] / total_instances
                    c.execute("UPDATE main.markovs_words SET probability = ?,counted = 1 WHERE word_before=? AND word_after=?",
                              (probability, word_before, data1[i][1]))
                    conn.commit()
        word_before = word

#create a string using markov chains
stop_conditions = [".", "!", ".", "\n", "..."]
message = ''
word_choice = c.execute("SELECT * FROM markovs_words WHERE word_before =''").fetchall()
rand_num = random.random()
total_prob = 0
n = -1

while len(message) < 100:  # random.randrange(50,101):
    while total_prob < rand_num:
        n = n + 1
        total_prob = total_prob + word_choice[n][3]
    message = message + word_choice[n][1] + " "
    if word_choice[n][1][-1:] in stop_conditions and len(message) > 50:
        break
    word_choice = c.execute("""SELECT * FROM markovs_words WHERE word_before = ?""", (word_choice[n][1],)).fetchall()
    n = -1
    total_prob = 0
    rand_num = random.random()

#make sure there are no @ symbols in tweet. if there are, get rid of them.
print("Cleaning up and tweeting")
puncs_to_remove = [""" " """]

message = list (message)
for i in range(len(message)):
    if message[i] in puncs_to_remove:
        message[i] = ""
message = "".join(message)

if len(message) < 140:
    twitter.tweet(api, message)
else:
    message = message[0:139]
    twitter.tweet(api, message[0:135])

print(message)
print("Finished in " + str(time.time()-start_time) + " seconds")

conn.commit()
c.close()
conn.close()
