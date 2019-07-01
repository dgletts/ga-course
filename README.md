# eSport Sentiment Analyser

## Context
Due to the significant financial incentive to capitalize on booming demand for eSports content, many cities are seeing eSports Bars or Cafes opening to cater to fans looking for social places to congregate. 

Running an eSports Bar or Cafe can then mean hard decisions given time/space restrictions for what specific eSport content to promote. Challenges include:
* eSport Event Calendars are crowded
* Local fans have local preferences
* Public opinion is highly volatile

## Approach
[Twitter API](https://developer.twitter.com/en/docs.html) provides access to high volume of market opinion easily sorted by geographic region (here we use top 50 most populous U.S cities) and by content (here looking for keyword list of most popular eSports game titles)

[Tweepy](https://www.tweepy.org/) Python library makes interacting with the Twitter API straightforward for simple implementation and also provides helper functions against [Twitter Streaming API](https://tweepy.readthedocs.io/en/latest/streaming_how_to.html) for real-time implementation.

[TextBlob](https://textblob.readthedocs.io/en/dev/) Python library used for processing the textual data from retrieved Tweets and perform [sentiment analysis](https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis)

[Twitch Games API](https://dev.twitch.tv/docs/api/reference#get-games) used to keep analytics on most popular competitive game streams to make sure the games/tournaments you are analyzing stays current to market opinion

## Example Usage
![Animated chart example](/spiritBombChart.gif)
