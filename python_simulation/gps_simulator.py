import pandas as pd
import random
import time
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csv_file = os.path.join(
    BASE_DIR,
    "data",
    "vehicle_data.csv"
)

latitude = 12.9716
longitude = 77.5946

print("Vehicle GPS Simulator Started...")

while True:

    latitude += random.uniform(-0.0008, 0.0008)
    longitude += random.uniform(-0.0008, 0.0008)

    speed = round(random.uniform(20, 80), 2)

    maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    row = {
        "timestamp": datetime.now(),
        "latitude": latitude,
        "longitude": longitude,
        "speed": speed,
        "status": "Moving",
        "alert": "Normal",
        "maps_link": maps_link
    }

    df = pd.DataFrame([row])

    file_exists = os.path.exists(csv_file)

    df.to_csv(
        csv_file,
        mode="a",
        header=not file_exists,
        index=False
    )

    print(
        f"Lat:{latitude:.6f} "
        f"Lon:{longitude:.6f} "
        f"Speed:{speed}"
    )

    time.sleep(3)