from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from weather_stream import fetch_weather

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='weather_stream_dag',
    default_args=default_args,
    schedule_interval='@hourly',
    catchup=False,
    tags=["weather"]  # ← facilite le filtrage dans Airflow UI
) as dag:

    fetch_weather_task = PythonOperator(
        task_id='fetch_weather',
        python_callable=fetch_weather
    )
