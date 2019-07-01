import tweepy
import pandas as pd
import re
import time
from textblob import TextBlob
from sqlalchemy import create_engine
import yaml
import json

TWITTER_CONFIG_FILE = '../auth.yaml'

with open(TWITTER_CONFIG_FILE, 'r') as config_file:
	config = yaml.load(config_file)

consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# get geo for top 50 US cities by population
json_data=open('cities_trunc.json').read()
data = json.loads(json_data)

# define twitter API calls by geo coordinates to a 10mi radius
def get_tweet_payload(d):
	return {d['city']: '%s,%s,%s' % (d['latitude'], d['longitude'],'10mi')}

geo = {}
i = 0
while i < len(data):
	geo.update(get_tweet_payload(data[i]))
	i += 1

# manually setting queries against set of popular competitive games - leverage twitch_top.py to keep this dynamic
api = tweepy.API(auth, wait_on_rate_limit=True)
query = ['fortnite', 'overwatch', 'starcraft', 'dota', 'league of legends', 'CSGO', 'hearthstone' ,'pubg', 'tekken', 'ssbm']
d = []

# Since we are using Standard APIs we are limited in data volume, adding additional geo regions and/or queries can result in long run-time
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

# use Pandas to format analyzed tweets into CSV file for appending to a database
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = timestr + "_tweets.csv"
cols=['Tweet','polarity','subjectivity','game','city']
df = pd.DataFrame(d, columns=cols)
df = df[['Tweet','polarity','subjectivity','game','city']]
df.drop_duplicates(['Tweet'], keep='last')
df.to_csv(filename, encoding='utf-8-sig')