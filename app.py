import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# Title
st.title("✈️ Pakistan Flight Tracker Dashboard")

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

# Map
st.subheader("📍 Flight Map")
m = folium.Map(location=[30.3753, 69.3451], zoom_start=5)
for s in pakistan_flights:
    lat, lon = s[6], s[5]
    callsign = s[1]
    if lat and lon:
        folium.Marker([lat, lon], popup=f"Flight: {callsign}").add_to(m)
st_folium(m, width=700, height=500)

# Speed Meter
st.subheader("🚀 Average Flight Speed")
avg_speed = df["velocity"].mean() * 3.6 if not df.empty else 0
fig_speed = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_speed,
    title={'text': "Average Speed (km/h)"},
    gauge={'axis': {'range': [0, 1000]}}
))
st.plotly_chart(fig_speed)

# Altitude Chart
st.subheader("📈 Flight Altitudes")
if not df.empty:
    fig_alt = px.line(df, x="callsign", y="baro_altitude", title="Flight Altitudes over Pakistan")
    st.plotly_chart(fig_alt)

# Speed Distribution
st.subheader("📊 Speed Distribution")
if not df.empty:
    fig_hist = px.histogram(df, x="velocity", nbins=20, title="Flight Speed Distribution (m/s)")
    st.plotly_chart(fig_hist)

# Data Table
st.subheader("📋 Flight Data Table")
st.dataframe(df)
