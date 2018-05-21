import tweepy
import pandas as pd
import re
from textblob import TextBlob
from sqlalchemy import create_engine
import json

settings = {
	'user': ''
}

consumer_key = "MWPfhlK89zKnVZvtISuSvTlyd"
consumer_secret = "mu0csop48M2tKbND2Cvu4HlslncVtbB09jJY5rx8sbYAEwfgeq"

access_token = "441556445-BX9Ij1hETlvU53Dx1f2eiiCr29RFTMJfTMK6RVWO"
access_token_secret = "o2rEjnPXKSAd2bg7JyzB9O4HFBEka2nZ5h7RzlBcL8W9N"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# geo cities.json setup 
json_data=open('cities_trunc.json').read()
data = json.loads(json_data)

def get_tweet_payload(d):
	return {d['city']: '%s,%s,%s' % (d['latitude'], d['longitude'],'10mi')}

geo = {}
i = 0
while i < len(data):
	geo.update(get_tweet_payload(data[i]))
	i += 1

api = tweepy.API(auth, wait_on_rate_limit=True)
query = ['fortnite', 'overwatch', 'starcraft', 'dota', 'league of legends', 'CSGO', 'hearthstone' ,'pubg', 'tekken', 'ssbm']
d = []

for game in query:
	for city,coords in geo.items():
		public_tweets = [status for status in tweepy.Cursor(api.search,q=game, geocode=coords, count=100).items(1000)]
		for tweet in public_tweets:
			analysis = TextBlob(tweet.text)
			TweetText = re.sub('[^A-Za-z0-9]+', ' ', tweet.text)
			polarity = analysis.sentiment.polarity
			subjectivity = analysis.sentiment.subjectivity
			d.append((TweetText,
						polarity,
						subjectivity,
						game,
						city))

cols=['Tweet','polarity','subjectivity','game','city']
df = pd.DataFrame(d, columns=cols)
df = df[['Tweet','polarity','subjectivity','game','city']]
df.to_csv("all_tweets.csv", encoding='utf-8-sig')