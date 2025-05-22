from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import os
import sys

# Ajouter le dossier ingestion au PYTHONPATH pour le PythonOperator
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ingestion")))

from yellow_taxi_ingest import download_yellow_taxi_data

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
}

with DAG(
    dag_id="yellow_taxi_pipeline",
    default_args=default_args,
    schedule_interval=None,  # Exécution manuelle
    catchup=False,
    tags=["yellow", "pipeline"],
) as dag:

    download_task = PythonOperator(
        task_id="download_yellow_taxi_data",
        python_callable=download_yellow_taxi_data,
        op_kwargs={
            "output_path": "data/raw/yellow_taxi/yellow_tripdata_2024-01.parquet"
        },
    )

    transform_task = BashOperator(
        task_id="transform_yellow_taxi_data",
        bash_command="PYTHONPATH=/opt/airflow python /opt/airflow/scripts/run_transform_taxi.py"
    )

    download_task >> transform_task
