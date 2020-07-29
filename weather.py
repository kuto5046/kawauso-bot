import requests
import json
import os

apiKey = os.environ["WEATHER_API_KEY"]
apiUrl = "https://api.openweathermap.org/data/2.5/forecast?units=metric&lat={lat}&lon={lon}&APPID={key}"


def Weather(lat, lon):
    url = apiUrl.format(lat=lat, lon=lon, key=apiKey)
    response = requests.get(url)
    js = response.json()
    counter = 0
    newList = []
    # Extract only the first 10 entries of weather info
    for item in js["list"]:
        while counter <= 9:
            newList.append(item)
            counter += 1
            break
    return newList