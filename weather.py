import requests
import pandas as pd
import math
from scrapy import Selector


API_key = "7b6bed7b239becc69848d0a6f5a04e9e"
# URL entiere exemple --> api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=7b6bed7b239becc69848d0a6f5a04e9e


i = 0
y = 0

villes = [
    "Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg",
    "Montpellier", "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre",
    "Saint-Étienne", "Toulon", "Grenoble", "Angers", "Dijon", "Brest",
    "Le Mans", "Nîmes", "Aix-en-Provence", "Clermont-Ferrand", "Tours",
    "Amiens", "Limoges", "Villeurbanne", "Metz", "Besançon", "Perpignan",
    "Orléans", "Caen", "Mulhouse", "Boulogne-Billancourt", "Rouen"
]

weather_URL = "https://api.openweathermap.org/data/2.5/weather"
#forecast_URL = "https://api.openweathermap.org/data/2.5/forecast"


data_list = []

while i < len(villes):
    #print (f"api.openweathermap.org/data/2.5/weather?q={villes[i]},fr&APPID=7b6bed7b239becc69848d0a6f5a04e9e")
    response = requests.get(f"{weather_URL}?q={villes[i]},fr&APPID={API_key}")
    #print (f"{forecast_URL}?q={villes[i]},fr&APPID={API_key}&units=metric")
    data = response.json()
    data_list.append({
        "city": villes[i],
        "lat": data["coord"]["lat"],
        "lon": data["coord"]["lon"]
    })
    i = i + 1
df = pd.DataFrame(data_list)
df.to_csv("villes_localisation.csv", index=False)


weather = []

for villes in df["city"]:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={villes},fr&appid={API_key}&units=metric"
    r = requests.get(url)
    data2 = r.json()

    temp = data2["main"]["temp"]
    clouds = data2["clouds"]["all"]

    score = 100 - abs(temp - 22) * 2 - clouds * 0.3

    weather.append({
        "city": villes,
        "temp": round(temp, 1),
        "clouds": round(clouds, 1),
        "weather_score": round(score, 1)
    })

df_weather = pd.DataFrame(weather)
df_weather.to_csv("weather_data.csv", index=False)


df_weather = df_weather.sort_values("weather_score", ascending=False)

top5 = df_weather[:5]

top5.to_csv("top_cities.csv", index=False)

print("Top 5 cities with best weather:")
print(top5)
