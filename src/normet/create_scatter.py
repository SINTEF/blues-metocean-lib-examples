"""Create a scatter table from wave data and save it to an Excel file"""
from datetime import datetime

from bluesmet.common.scatter import Scatter
from bluesmet.normet.nora3 import wave_sub_time

from utils.scatter_writer import ScatterExcelWriter


def write_scatter():
    """Write a scatter table to an excel file"""
    lat_pos = 62.5365
    lon_pos = 4.1770
    start_date = datetime(2020, 10, 21)
    end_date = datetime(2020, 11, 21)
    requested_values = ["hs","tp"]
    values = wave_sub_time.get_values_between(
        lat_pos, lon_pos, start_date, end_date, requested_values
    )

    bin_size = 2.0
    scatter = Scatter(bin_size=bin_size)
    for hs,tp in zip(values["hs"],values["tp"]):
        scatter.add(hs,tp)

    writer = ScatterExcelWriter(scatter, "hs", "tp")
    writer.write_occurences()
    writer.append([])



    # Save the Excel file
    filename = "./output/scatter.xlsx"
    writer.save(filename)
    print(f"Saved to {filename}")


if __name__ == "__main__":
    write_scatter()
