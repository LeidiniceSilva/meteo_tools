# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Jun 25, 2026"
__description__ = "This script compute MOAAP input"

import os
import xarray as xr
import numpy as np

# Paths
path_in  = "/leonardo/home/userexternal/mdasilva/leonardo_work/MOAAP/course/ERA5"
path_out = "/leonardo/home/userexternal/mdasilva/leonardo_work/MOAAP/course/ERA5/processed"

os.makedirs(path_out, exist_ok=True)

# Input files
files = {
    "IVTE_era5_1Jan2020.nc": "IVTE",
    "IVTN_era5_1Jan2020.nc": "IVTN",
    "msl_era5_1Jan2020.nc":  "SLP",
    "q850_era5_1Jan2020.nc": "Q850",
    "t850_era5_1Jan2020.nc": "T850",
    "Tb_era5_1Jan2020.nc":   "Tb",
    "tp_era5_1Jan2020.nc":   "PR",
    "u200_era5_1Jan2020.nc": "U200",
    "u850_era5_1Jan2020.nc": "U850",
    "v200_era5_1Jan2020.nc": "V200",
    "v850_era5_1Jan2020.nc": "V850",
    "z500_era5_1Jan2020.nc": "Z500"
}


# Variable attributes
attrs = {
"IVTE": {"units": "kg m-1 s-1", "long_name": "zonal integrated vapor transport", "cell_methods": "time: point"},
"IVTN": {"units": "kg m-1 s-1", "long_name": "meridional integrated vapor transport", "cell_methods": "time: point"},
"PR":   {"units": "mm h-1", "long_name": "precipitation at surface", "cell_methods": "time: sum"},
"Q850": {"units": "kg kg-1", "long_name": "vapor mixing ratio at 850 hPa", "cell_methods": "time: point"},
"SLP":  {"units": "Pa", "long_name": "pressure at sea level", "cell_methods": "time: point"},
"T850": {"units": "K", "long_name": "air temperature at 850 hPa", "cell_methods": "time: point"},
"Tb":   {"units": "K", "long_name": "brightness temperature", "cell_methods": "time: point"},
"U200": {"units": "m s-1", "long_name": "zonal wind at 200 hPa", "cell_methods": "time: point"},
"U850": {"units": "m s-1", "long_name": "zonal wind at 850 hPa", "cell_methods": "time: point"},
"V200": {"units": "m s-1", "long_name": "meridional wind at 200 hPa", "cell_methods": "time: point"},
"V850": {"units": "m s-1", "long_name": "meridional wind at 850 hPa", "cell_methods": "time: point"},
"Z500": {"units": "gpm", "long_name": "500 hPa geopotential height", "cell_methods": "time: point"}
}

# Process files
processed = []

for f, varname in files.items():
    print("Processing:", f)

    ds = xr.open_dataset(f"{path_in}/{f}")

    # Remove pressure dims
    for dim in ["pressure_level",
                "pressure_level_2",
                "pressure_level_3"]:
        if dim in ds.dims:
            ds = ds.squeeze(dim, drop=True)

    # Rename dimensions
    ds = ds.rename({
        "valid_time": "time",
        "latitude": "y",
        "longitude": "x"
    })
    
    # Convert longitude from 0-360 to -180-180
    ds = ds.assign_coords(
        x=((ds.x + 180) % 360) - 180
    )

    # Sort longitudes
    ds = ds.sortby("x")

    # Fix encoding issue (IMPORTANT)
    ds.encoding = {}
    for v in ds.variables:
        ds[v].encoding = {}

    # Rename variable inside file
    old = list(ds.data_vars)[0]
    ds = ds.rename({old: varname})

    # Conversions
    if varname == "PR":
        ds[varname] = ds[varname] * 1000.0

    # Attributes
    ds[varname] = ds[varname].astype(np.float64)
    ds[varname].attrs = attrs[varname]
    ds["time"].attrs = {}

    # Save processed file
    out = f"{path_out}/{varname}.nc"

    ds.to_netcdf(
        out,
        encoding={
            varname: {"dtype": "float64", "_FillValue": np.nan},
            "time": {
                "dtype": "int64",
                "units": "hours since 2020-01-01 00:00:00",
                "calendar": "proleptic_gregorian"
            }
        },
        unlimited_dims=["time"]
    )

    processed.append(out)

# Merge all variables
print("\nMerging files...")

ds_all = xr.open_mfdataset(processed, combine="by_coords")

# Create lat/lon 2D
lon1d = ds_all["x"].values
lat1d = ds_all["y"].values

lon2d, lat2d = np.meshgrid(lon1d, lat1d)

ds_all["lat"] = xr.DataArray(
    lat2d,
    dims=("y", "x"),
    attrs={
        "long_name": "Latitudes, y-coordinate in Cartesian system",
        "standard_name": "latitude",
        "units": "degrees_north"
    }
)

ds_all["lon"] = xr.DataArray(
    lon2d,
    dims=("y", "x"),
    attrs={
        "long_name": "Longitudes, x-coordinate in Cartesian system",
        "standard_name": "longitude",
        "units": "degrees_east"
    }
)

ds_all = ds_all.drop_vars(["x", "y"])

# Global attributes
ds_all.attrs = {
    "history": "MOAAP input created from ERA5 single-variable files"
}

# Final save
final_file = f"{path_out}/MOAAP_input.nc"

ds_all.to_netcdf(
    final_file,
    unlimited_dims=["time"]
)

print("Saved:", final_file)
