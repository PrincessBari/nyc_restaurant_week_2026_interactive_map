import pandas as pd

# Read your CSV
df = pd.read_csv("nyc_restaurant_week.csv")

# Append ", NYC" to Neighborhood column
df["Neighborhood"] = df["Neighborhood"].astype(str) + ", New York, NY"

# Save to a new file (safer than overwriting)
df.to_csv("nyc_restaurants_nyc.csv", index=False)

print("Done! ', New York, NY' appended to Neighborhood column.")
