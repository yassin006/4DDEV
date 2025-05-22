import os
import json
from datetime import datetime, timedelta
import random

FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "raw", "weather"))
os.makedirs(FOLDER_PATH, exist_ok=True)

start_time = datetime(2024, 1, 1, 0, 0, 0)
nb_hours = 100
weather_conditions = ["Clear", "Clouds", "Rain", "Snow", "Drizzle"]

for i in range(nb_hours):
    timestamp = start_time + timedelta(hours=i)
    temp = round(random.uniform(-5, 12), 2)
    condition = random.choice(weather_conditions)

    data = {
        "dt": int(timestamp.timestamp()),
        "main": {"temp": temp},
        "weather": [{"main": condition}],
        "dt_txt": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        # 🗺️ FAKE COORDINATES (NYC range)
        "coord": {
            "lat": round(random.uniform(40.6, 40.9), 6),
            "lon": round(random.uniform(-74.1, -73.7), 6)
        }
    }

    filename = os.path.join(FOLDER_PATH, f"weather_{timestamp.strftime('%Y-%m-%dT%H-%M-%S')}.json")
    with open(filename, "w") as f:
        json.dump(data, f)

    print(f"✅ {filename} généré")
