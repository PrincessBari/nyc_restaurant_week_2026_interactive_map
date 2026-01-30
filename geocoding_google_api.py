import pandas as pd
import requests
import time

API_KEY = "<API key>"

GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def geocode_address(address):
    params = {
        "address": address,
        "key": API_KEY
    }

    response = requests.get(GEOCODE_URL, params=params).json()

    if response["status"] == "OK":
        result = response["results"][0]
        location = result["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        return None, None

# Load CSV
df = pd.read_csv("restaurants_with_addresses.csv")

latitudes = []
longitudes = []

for i, address in enumerate(df["Address"], start=1):
    lat, lng = geocode_address(address)
    latitudes.append(lat)
    longitudes.append(lng)

    if lat is None:
        print(f"⚠️ Failed to geocode: {address}")

    # Respect rate limits
    time.sleep(0.1)

df["Latitude"] = latitudes
df["Longitude"] = longitudes

# Save output
df.to_csv("restaurants_geocoded.csv", index=False)

print("✅ Geocoding complete.")
