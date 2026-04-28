import requests
import pandas as pd
import plotly.graph_objects as go

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

# Average speed (velocity in m/s → convert to km/h)
if not df.empty:
    avg_speed = df["velocity"].mean() * 3.6
else:
    avg_speed = 0

# Gauge chart
fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_speed,
    title={'text': "Average Flight Speed (km/h)"},
    gauge={'axis': {'range': [0, 1000]}}
))

fig.write_html("speed_meter.html")
print("Speed meter saved as speed_meter.html")
