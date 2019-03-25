import requests
import pprint
import json

url = 'https://api.twitch.tv/helix/games/top'
headers = {'Client-ID': '60ykge3lpa751jtwd2hrllzrvpf5mh'}

r = requests.get(url, headers=headers)

resp_dict = json.loads(r.text)


games = []
for i in resp_dict['data']:
	games.append(i['name'])

print(games)