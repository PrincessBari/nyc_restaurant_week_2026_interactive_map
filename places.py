import pandas as pd
import requests
import time

API_KEY = "<API key>"

def get_address(restaurant, neighborhood):
    query = f"{restaurant}, {neighborhood}"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": API_KEY
    }

    response = requests.get(url, params=params).json()
    if response["results"]:
        return response["results"][0]["formatted_address"]
    return None

df = pd.read_csv("nyc_restaurants_nyc.csv")

addresses = []
for _, row in df.iterrows():
    address = get_address(row["Restaurant"], row["Neighborhood"])
    addresses.append(address)
    time.sleep(0.1)  # be nice to the API

df["Address"] = addresses
df.to_csv("restaurants_with_addresses.csv", index=False)
