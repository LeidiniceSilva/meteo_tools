# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilvae@gmail.com"
__date__        = "March 02, 2026"
__description__ = "Download ERA5"

import os
import cdsapi

client = cdsapi.Client()

var='tp'
year_i = 1970
year_f = 2024

dataset = "derived-era5-single-levels-daily-statistics"
out_dir = "/leonardo/home/userexternal/mdasilva/leonardo_work/OBS/ERA5/day"
os.makedirs(out_dir, exist_ok=True)

months = [
    "01", "02", "03", "04", "05", "06",
    "07", "08", "09", "10", "11", "12"
]

days = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
    "31"
]

for year in range(year_i, year_f+1):

    request = {
        "product_type": "reanalysis",
        "variable": ["total_precipitation"],
        "year": str(year),
        "month": months,
        "day": days,
        "daily_statistic": "daily_sum",
        "time_zone": "utc+00:00",
        "frequency": "1_hourly"
    }

    output_file = os.path.join(out_dir, f"{var}_ERA5_{year}.nc")

    print(f"Downloading {year}")
    client.retrieve(dataset, request).download(output_file)

print("Done")



