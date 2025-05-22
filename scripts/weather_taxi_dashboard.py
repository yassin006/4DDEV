import streamlit as st
import duckdb
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Météo & Taxis", layout="wide")
st.title("🚖🌦️ Dashboard Météo & Trajets Taxi")

# Connexion à DuckDB
con = duckdb.connect("data/processed/yellow_taxi.duckdb")

# === 🌦️ Charger les données météo ===
df_weather = con.execute("""
    SELECT 
        timestamp,
        temp,
        weather,
        lat,
        lon
    FROM weather_hourly
    ORDER BY timestamp
""").df()

# ✅ Conversion et nettoyage
if not df_weather.empty:
    df_weather["pickup_hour"] = pd.to_datetime(df_weather["timestamp"]).dt.floor("h")
    df_weather = df_weather.dropna(subset=["pickup_hour", "temp", "lat", "lon"])
    df_weather = df_weather[
        (df_weather["pickup_hour"] >= "2024-01-01") & 
        (df_weather["pickup_hour"] < "2024-02-01")
    ]
else:
    st.warning("⚠️ Aucune donnée météo disponible dans weather_hourly.")
    df_weather["pickup_hour"] = pd.NaT

# 🔍 Aperçu brut météo
st.subheader("🛠️ Aperçu brut météo")
st.write(df_weather.head())

# === 🚖 Charger les données taxi nettoyées ===
df_taxi = con.execute("""
    SELECT 
        strftime(tpep_pickup_datetime, '%Y-%m-%d %H:00:00') AS pickup_hour,
        COUNT(*) AS trip_count,
        AVG(trip_distance) AS avg_distance
    FROM yellow_tripdata_2024_01
    WHERE trip_distance BETWEEN 0.1 AND 50
      AND fare_amount >= 2
      AND tpep_pickup_datetime BETWEEN '2024-01-01' AND '2024-02-01'
    GROUP BY pickup_hour
    ORDER BY pickup_hour
""").df()

df_taxi["pickup_hour"] = pd.to_datetime(df_taxi["pickup_hour"])

# === 🔁 Jointure météo + taxi
df_joined = pd.merge(df_weather, df_taxi, on="pickup_hour", how="inner")

# === 📊 Visualisations
if df_weather.empty:
    st.error("❌ Impossible d'afficher les graphiques météo : données manquantes.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌡️ Température par heure")
        st.line_chart(df_weather.set_index("pickup_hour")["temp"])

        st.subheader("📆 Température moyenne par jour")
        df_weather["day"] = df_weather["pickup_hour"].dt.date
        daily_temp = df_weather.groupby("day")["temp"].mean()
        st.line_chart(daily_temp)

        st.subheader("📏 Distance moyenne des trajets")
        st.line_chart(df_taxi.set_index("pickup_hour")["avg_distance"])

    with col2:
        st.subheader("🚖 Nombre de trajets par heure")
        st.bar_chart(df_taxi.set_index("pickup_hour")["trip_count"])

        if not df_joined.empty:
            st.subheader("📈 Température vs Trafic taxi (double axe)")

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df_joined["pickup_hour"],
                y=df_joined["temp"],
                name="Température (°C)",
                mode='lines',
                yaxis="y1"
            ))

            fig.add_trace(go.Scatter(
                x=df_joined["pickup_hour"],
                y=df_joined["trip_count"],
                name="Nombre de trajets",
                mode='lines',
                yaxis="y2"
            ))

            fig.update_layout(
                xaxis=dict(title="Heure"),
                yaxis=dict(title="Température (°C)", side="left"),
                yaxis2=dict(title="Trajets", overlaying="y", side="right"),
                legend=dict(x=0, y=1.1, orientation="h")
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Aucune heure commune entre météo et taxi.")

# Vérification préalable : df_weather et taxi_map doivent être bien formatés
if not df_weather.empty and "lat" in df_weather.columns and "lon" in df_weather.columns:

    st.subheader("🗺️ Carte interactive : météo + trafic taxi")

    # Générer des coordonnées aléatoires proches de NYC pour les trajets (si pas réelles)
    import numpy as np
    taxi_map = df_joined.copy()
    taxi_map["lon"] = np.random.normal(loc=-73.98, scale=0.01, size=len(taxi_map))
    taxi_map["lat"] = np.random.normal(loc=40.75, scale=0.01, size=len(taxi_map))

    # Définir les couches
    weather_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_weather[["lat", "lon", "temp", "weather"]],
        get_position='[lon, lat]',
        get_fill_color='[0, 100, 255, 160]',
        get_radius=200,
        pickable=True
    )

    taxi_layer = pdk.Layer(
        "HeatmapLayer",
        data=taxi_map[["lat", "lon", "trip_count"]],
        get_position='[lon, lat]',
        get_weight='trip_count'
    )

    view_state = pdk.ViewState(
        latitude=40.75,
        longitude=-73.98,
        zoom=10,
        pitch=30
    )

    deck = pdk.Deck(
        layers=[weather_layer, taxi_layer],
        initial_view_state=view_state,
        tooltip={"text": "Temp: {temp}°C\nWeather: {weather}"}
    )

    st.pydeck_chart(deck)

else:
    st.info("ℹ️ Les coordonnées géographiques ne sont pas disponibles.")

# === 🌥️ Tableau brut météo
if not df_weather.empty:
    st.subheader("🌥️ Données météo brutes")
    st.dataframe(df_weather[["pickup_hour", "temp", "weather", "lat", "lon"]])
