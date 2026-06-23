# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilvae@gmail.com"
__date__        = "March 02, 2026"
__description__ = "Download ERA5"

import cdsapi

client = cdsapi.Client()

var_nc = 'avg_tnlwrf'
dataset = 'reanalysis-era5-single-levels'
var_name = 'mean_top_net_long_wave_radiation_flux'

for year in range(2000, 2010):
    for m in range(1, 13):
        month = f'{m:02d}' 

        request = {
            "product_type": ["reanalysis"],
            "variable": [var_name],
            "year": [str(year)],
            "month": [month],
            "day": [
                "01", "02", "03", "04", "05", "06",
                "07", "08", "09", "10", "11", "12",
                "13", "14", "15", "16", "17", "18",
                "19", "20", "21", "22", "23", "24",
                "25", "26", "27", "28", "29", "30",
                "31"
            ],
            "time": [
                "00:00", "01:00", "02:00", "03:00",
                "04:00", "05:00", "06:00", "07:00",
                "08:00", "09:00", "10:00", "11:00",
                "12:00", "13:00", "14:00", "15:00",
                "16:00", "17:00", "18:00", "19:00",
                "20:00", "21:00", "22:00", "23:00"
            ],
            "data_format": "netcdf",
            "download_format": "unarchived"
        }

        output_file = f'/leonardo/home/userexternal/mdasilva/leonardo_work/OBS/ERA5/1hr/{var_nc}_ERA5_{year}_{month}.nc'

        print(f'Downloading {year}-{month}...')
        client.retrieve(dataset, request, output_file)

print('All downloads completed')


