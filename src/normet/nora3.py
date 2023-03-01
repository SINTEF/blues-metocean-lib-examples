"""Demonstration of how to use the nora3 module."""
from datetime import datetime
from bluesmet.normet.nora3 import wave_sub_time, arome3km_3hr

# Coordinates we want to get data for
lat_pos = 64.731729
lon_pos = 5.835813
start_date = datetime(2020, 10, 21)
end_date = datetime(2020, 11, 21)

requested_values = [
    "hs",
    "tp"
]
values = wave_sub_time.get_values_between(
    lat_pos, lon_pos, start_date, end_date, requested_values
)

# Coordinates we actually to get data for (nearest grid point)
alat = values["latitude_actual"]
alon = values["longitude_actual"]
print(f"Actual coordinates: {alat} lon: {alon}")

for requested_value in requested_values:
    print(f"{requested_value}_mean: {values[requested_value].mean()}")

requested_values = ["wind_speed", "wind_direction"]
values = arome3km_3hr.get_values_between(
    lat_pos, lon_pos, start_date, end_date, requested_values
)
alat = values["latitude_actual"]
alon = values["longitude_actual"]
print(f"Actual coordinates 2: {alat} lon: {alon}")
for requested_value in requested_values:
    print(f"{requested_value}_mean: {values[requested_value].mean()}")
