# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilvae@gmail.com"
__date__        = "February 15, 2026"
__description__ = "ESM lectures"

import os
import cdsapi

client = cdsapi.Client()

dataset = "reanalysis-era5-single-levels"

var_nc="slhf"
var_name="surface_upward_latent_heat_flux"
path="/home/mda_silv/clima-archive2-b/ESM_2025/ERA5"

for year in range(1991, 2021):

    request = {
        "product_type": ["reanalysis"],
        "variable": [var_name],
        "year": [str(year)],
        "month": [
            "01", "02", "03", "04", "05", "06",
            "07", "08", "09", "10", "11", "12"
        ],
        "day": [
            "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
            "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
            "31"
        ],
        "time": [
            "00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
            "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
            "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
            "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
        ],
        "data_format": "netcdf",
        "download_format": "unarchived"
    }

    output_file = os.path.join(path, f"{var_nc}_ERA5_{year}.nc")

    print(f"Downloading {year}...")
    client.retrieve(dataset, request, output_file)

print("All downloads completed.")
