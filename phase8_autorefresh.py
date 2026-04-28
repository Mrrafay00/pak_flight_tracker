import requests
import pandas as pd
import folium
import plotly.graph_objects as go
import plotly.express as px
import time

def generate_dashboard():
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

    # Folium map
    m = folium.Map(location=[30.3753, 69.3451], zoom_start=5)
    for s in pakistan_flights:
        lat, lon = s[6], s[5]
        callsign = s[1]
        if lat and lon:
            folium.Marker([lat, lon], popup=f"Flight: {callsign}").add_to(m)
    m.save("map_component.html")

    # Speed meter
    avg_speed = df["velocity"].mean() * 3.6 if not df.empty else 0
    fig_speed = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_speed,
        title={'text': "Average Flight Speed (km/h)"},
        gauge={'axis': {'range': [0, 1000]}}
    ))
    fig_speed.write_html("speed_component.html")

    # Altitude chart
    if not df.empty:
        fig_alt = px.line(df, x="callsign", y="baro_altitude", title="Flight Altitudes over Pakistan")
        fig_alt.write_html("altitude_component.html")

    # Data table
    if not df.empty:
        df.to_html("table_component.html", index=False)

    # Combine into single dashboard
    with open("dashboard.html", "w", encoding="utf-8") as f:
        f.write("<h1>Pakistan Flight Tracker Dashboard (Auto-Refresh)</h1>")
        f.write("<h2>Map</h2>")
        f.write(open("map_component.html", encoding="utf-8").read())
        f.write("<h2>Speed Meter</h2>")
        f.write(open("speed_component.html", encoding="utf-8").read())
        f.write("<h2>Altitude Chart</h2>")
        f.write(open("altitude_component.html", encoding="utf-8").read())
        f.write("<h2>Flight Data Table</h2>")
        f.write(open("table_component.html", encoding="utf-8").read())

    print("Dashboard updated!")

# Auto-refresh loop (every 60 seconds)
while True:
    generate_dashboard()
    time.sleep(60)
