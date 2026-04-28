import requests
import folium

# API call
url = "https://opensky-network.org/api/states/all"
response = requests.get(url)
data = response.json()
states = data["states"]

# Pakistan ke lat/lon range
min_lat, max_lat = 23, 37
min_lon, max_lon = 60, 77

# Folium map banaye (Pakistan center)
m = folium.Map(location=[30.3753, 69.3451], zoom_start=5)

# Flights filter + markers add
for s in states:
    lat, lon = s[6], s[5]
    callsign = s[1]
    if lat and lon:
        if min_lat <= lat <= max_lat and min_lon <= lon <= max_lon:
            folium.Marker(
                [lat, lon],
                popup=f"Flight: {callsign}\nLat: {lat}, Lon: {lon}"
            ).add_to(m)

# Map save karein
m.save("pakistan_flights.html")
print("Map saved as pakistan_flights.html")
