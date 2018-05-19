import tweepy
import pandas as pd
from textblob import TextBlob

consumer_key = "MWPfhlK89zKnVZvtISuSvTlyd"
consumer_secret = "mu0csop48M2tKbND2Cvu4HlslncVtbB09jJY5rx8sbYAEwfgeq"

access_token = "441556445-BX9Ij1hETlvU53Dx1f2eiiCr29RFTMJfTMK6RVWO"
access_token_secret = "o2rEjnPXKSAd2bg7JyzB9O4HFBEka2nZ5h7RzlBcL8W9N"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.search(q="fortnite", geocode="40.714353,-74.00597,20km")

d = []
for tweet in public_tweets:
	analysis = TextBlob(tweet.text)
	TweetText = tweet.text
	polarity = analysis.sentiment.polarity
	subjectivity = analysis.sentiment.subjectivity
	d.append((TweetText,
				polarity,
				subjectivity))

cols=['Tweet','polarity','subjectivity']
df = pd.DataFrame(d, columns=cols)
print(df.head)