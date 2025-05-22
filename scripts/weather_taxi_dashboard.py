import streamlit as st
import duckdb
import pandas as pd
import pydeck as pdk

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
            st.subheader("📈 Température vs Trafic taxi")
            st.line_chart(df_joined.set_index("pickup_hour")[["temp", "trip_count"]])
        else:
            st.warning("⚠️ Aucune heure commune entre météo et taxi. Pas de graphe combiné.")

# === 🗺️ Carte des points météo
if not df_weather.empty and "lat" in df_weather.columns and "lon" in df_weather.columns:
    st.subheader("🗺️ Carte des conditions météo")
    st.map(df_weather[["lat", "lon"]])
else:
    st.info("ℹ️ Les coordonnées géographiques ne sont pas disponibles pour les données météo.")

# === 🌥️ Tableau brut météo
if not df_weather.empty:
    st.subheader("🌥️ Données météo brutes")
    st.dataframe(df_weather[["pickup_hour", "temp", "weather", "lat", "lon"]])
