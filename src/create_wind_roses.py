"""Demonstration of how to generate wind roses from the nora3 module."""
import calendar
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

import numpy as np
from bluesmet.normet.nora3 import arome3km_3hr
from windrose import WindroseAxes

name = "Sørlig Nordsjø II"
lat_pos = 56.758896
lon_pos = 4.903143
path = Path(f"./output/windroses/{name}")
# Delete folder if it exists
if path.exists() and path.is_dir():
    shutil.rmtree(path)
os.makedirs(path, exist_ok=True)

# Start timing
start = time.time()

years = [2019]

all_values = {}

requested_values = ["wind_speed", "wind_direction", "height"]

# Get the heights from the first dataset
heights = None

for year in years:
    yearly = {}
    all_values[year] = yearly

    for month in range(1, 13):
        start_date = datetime(year, month, 1)
        mrange = calendar.monthrange(year, month)
        end_date = datetime(year, month, mrange[1])
        print(f"Collection data from {start_date} to {end_date}...")
        monthly = arome3km_3hr.get_values_between(
            lat_pos, lon_pos, start_date, end_date, requested_values
        )
        yearly[month] = monthly

        if heights is None:
            heights = monthly["height"]
            lat_actual = monthly["latitude_actual"]
            lon_actual = monthly["longitude_actual"]
            print(f"Actual location (nearest grid point): {lat_actual}, {lon_actual}")

all_speed = np.ndarray(0)
all_direction = np.ndarray(0)

# Select the height from available heights
height_idx = 2
height = heights[height_idx]

print(f"Available heights: {heights} m")
print(f"Selected height: {height} m")

for month in range(1, 13):
    speed = np.ndarray(0)
    direction = np.ndarray(0)

    for year in years:
        yearly = all_values[year]
        monthly = yearly[month]

        mspeed = monthly["wind_speed"][:, height_idx]
        # Met: North West Up, wind_going_to
        # Wind rose: North East Down, wind coming from
        mdir = np.fmod(monthly["wind_direction"][:, height_idx] + 180.0, 360.0)
        speed = np.concatenate((speed, mspeed))
        direction = np.concatenate((direction, mdir))

    ax = WindroseAxes.from_ax()
    ax.bar(direction, speed, bins=9, nsector=36, opening=0.8, edgecolor="white")
    ax.set_legend()
    name = calendar.month_name[month]

    ax.set_title(f"Montly wind - {name} - years {years} at {height} m")
    ax.figure.savefig(path / f"{month}_{name}_{height}m.png")

    all_speed = np.concatenate((all_speed, speed))
    all_direction = np.concatenate((all_direction, direction))

ax = WindroseAxes.from_ax()
ax.bar(all_direction, all_speed, bins=9, nsector=36, opening=0.8, edgecolor="white")
ax.set_legend()
ax.set_title(f"Wind - all data - years {years} at {height} m")
ax.figure.savefig(path / f"all_{height}m.png")

print(f"File successfully created at {path}")

# End timing and print elapsed time
end = time.time()
print("Elapsed time: " + str(end - start) + " seconds")
