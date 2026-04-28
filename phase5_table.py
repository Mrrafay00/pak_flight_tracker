import requests
import pandas as pd

# API call
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()
states = data["states"]

# Pakistan ke lat/lon range
min_lat, max_lat = 23, 37
min_lon, max_lon = 60, 77

# Filter flights
pakistan_flights = []
for s in states:
    lat, lon = s[6], s[5]
    if lat and lon:
        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
            pakistan_flights.append(s)

# DataFrame
df = pd.DataFrame(pakistan_flights, columns=[
    "icao24","callsign","origin_country","time_position","last_contact",
    "longitude","latitude","baro_altitude","on_ground","velocity",
    "true_track","vertical_rate","sensors","geo_altitude","squawk",
    "spi","position_source"
])

# Save table as HTML
if not df.empty:
    df.to_html("flight_data_table.html", index=False)
    print("Flight data table saved as flight_data_table.html")
else:
    print("No flights detected in Pakistan at the moment.")
