# 🚖🌦️ Projet Big Data — Dashboard Météo & Trajets Taxi

Ce projet a été réalisé dans le cadre d’un module Big Data visant à concevoir une architecture complète de traitement de données batch et streaming. Il combine l'ingestion de données météo (streaming via API/fake) et de trajets taxi (batch via fichiers Parquet), leur transformation avec PySpark, la modélisation avec DuckDB, et leur visualisation via Streamlit.

---

## 🗂️ Structure du projet

```
bigdata-project/
├── dags/                    ← DAGs Airflow (orchestration)
├── data/                    ← Données brutes et transformées
│   └── raw/                 ← Données sources (weather, taxi)
│   └── processed/           ← Base DuckDB
├── ingestion/               ← Scripts d’ingestion batch/streaming
├── streaming/               ← Scripts streaming météo
├── transformations/         ← Transformations PySpark
├── scripts/                 ← Scripts utilitaires & dashboard
├── Dockerfile               ← Image Airflow + Python
├── docker-compose.yml       ← Déploiement multi-services
├── requirements.txt         ← Dépendances Python
├── README.md                ← Documentation du projet
```

---

## ⚙️ Technologies utilisées

- **Python 3.11** (ETL + Streamlit)
- **Airflow** pour l'orchestration
- **PySpark** pour la transformation des données
- **DuckDB** comme entrepôt léger
- **Streamlit** pour la visualisation interactive
- **Docker & Compose** pour l’environnement conteneurisé

---

## 🚀 Lancement rapide

### 1. Cloner le projet
```bash
git clone https://github.com/yassin006/4DDEV.git
cd bigdata-project
```

### 2. Lancer les services avec Docker
```bash
docker compose up --build
```

### 3. Vérifier Airflow
Accéder à l'interface : [http://localhost:8080](http://localhost:8080)
- user: `admin`
- password: `admin`

### 4. Exécuter les DAGs manuellement (Yellow Taxi & Weather)

### 5. Lancer le Dashboard
Dans un autre terminal :
```bash
streamlit run scripts/weather_taxi_dashboard.py
```

Accessible à [http://localhost:8501](http://localhost:8501)

---

## 📊 Fonctionnalités du dashboard

- Température par heure / jour
- Nombre de trajets par heure
- Carte interactive météo + densité de trajets (simulée)
- Croisement météo ↔ trafic

---

## 📁 Données utilisées

- `yellow_tripdata_2024-01.parquet` (dataset open NYC)
- Données météo **générées** (via `generate_fake_weather.py`)

---

## 🧪 Tests et monitoring

- Scripts Python testables individuellement
- Logs dans `./logs/`

---

## ✅ Auteurs et contributions

Réalisé par [Yassine/Leo/Marouan](https://github.com/yassin006) dans le cadre du module 4DDEV.  
Projet noté sur l'intégration complète d'un pipeline de données.

---

## 🔭 Améliorations futures

- Intégration de **MinIO** comme data lake
- Utilisation de **dbt** pour la modélisation analytique
- Enrichissement temps réel avec Kafka/Flink
