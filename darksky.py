import requests, json
weather = requests.get("https://api.darksky.net/forecast/560a289d9a108079c47564ebf2fbaad0/42.37,-71.11").json()
print(json.dumps(weather["currently"], indent = 2))