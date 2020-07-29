

import json
import requests
import os

apiKey = os.environ["NEWS_API_KEY"]
apiUrl = "https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={apiKey}"


def fetchNews(country, category):
    url = apiUrl.format(country=country, category=category, apiKey=apiKey)
    response = requests.get(url)
    js = response.json()
    counter = 0
    # Skip through the first 10 entries and then pop the rest
    for articles in js["articles"]:
        while counter <= 9:
            counter += 1
            break
        while counter <= int(js["totalResults"]):
            js["articles"].pop()
            counter += 1
            break
    return js