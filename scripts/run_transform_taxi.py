import sys
import os

# ➕ Ajouter le dossier "transformations" au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "transformations")))

from transform_taxi import transform_yellow_taxi_data

if __name__ == "__main__":
    transform_yellow_taxi_data()
