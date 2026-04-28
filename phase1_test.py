import requests
import pandas as pd

# API call
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()

# Raw flight states
states = data["states"]

# Pakistan ke lat/lon range
min_lat, max_lat = 23, 37
min_lon, max_lon = 60, 77

# Filter flights jo Pakistan ke andar hain
pakistan_flights = []
for s in states:
    lat, lon = s[6], s[5]   # API structure: lon index=5, lat index=6
    if lat and lon:
        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
            pakistan_flights.append(s)

# Table banaye
df = pd.DataFrame(pakistan_flights, columns=[
    "icao24","callsign","origin_country","time_position","last_contact",
    "longitude","latitude","baro_altitude","on_ground","velocity",
    "true_track","vertical_rate","sensors","geo_altitude","squawk",
    "spi","position_source"
])

print(df.head())
