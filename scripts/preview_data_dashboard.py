import streamlit as st
import duckdb

st.set_page_config(page_title="🔍 Aperçu des données", layout="wide")
st.title("🔍 Aperçu des données DuckDB")

# Connexion à la base
con = duckdb.connect("data/processed/yellow_taxi.duckdb")

# === 🚖 TABLE TAXI ===
st.header("🚖 yellow_tripdata_2024_01")

try:
    df_taxi_sample = con.execute("SELECT * FROM yellow_tripdata_2024_01 LIMIT 5").df()
    df_taxi_schema = con.execute("DESCRIBE yellow_tripdata_2024_01").df()

    st.subheader("🧪 Échantillon des données")
    st.dataframe(df_taxi_sample)

    st.subheader("📐 Structure (types)")
    st.dataframe(df_taxi_schema)

except Exception as e:
    st.error(f"Erreur lors de la lecture de yellow_tripdata_2024_01 : {e}")

# === 🌦️ TABLE METEO ===
st.header("🌦️ weather_hourly")

try:
    df_weather_sample = con.execute("SELECT * FROM weather_hourly LIMIT 5").df()
    df_weather_schema = con.execute("DESCRIBE weather_hourly").df()

    st.subheader("🧪 Échantillon des données")
    st.dataframe(df_weather_sample)

    st.subheader("📐 Structure (types)")
    st.dataframe(df_weather_schema)

except Exception as e:
    st.error(f"Erreur lors de la lecture de weather_hourly : {e}")
