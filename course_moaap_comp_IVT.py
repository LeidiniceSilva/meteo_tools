# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Jun 17, 2026"
__description__ = "This script compute IVT"

import os
import xarray as xr
import numpy as np

# Paths
path_in = "/leonardo/home/userexternal/mdasilva/leonardo_work/MOAAP/course/ERA5"
path_out = "/leonardo/home/userexternal/mdasilva/leonardo_work/MOAAP/course/ERA5"
os.makedirs(path_out, exist_ok=True)

# Constants
g = 9.80665
hpa_to_pa = 100  # 1 hPa = 100 Pa

# Open dataset
q = xr.open_dataset(f"{path_in}/q_era5_1Jan2020.nc")["q"]
u = xr.open_dataset(f"{path_in}/u_era5_1Jan2020.nc")["u"]
v = xr.open_dataset(f"{path_in}/v_era5_1Jan2020.nc")["v"]

# Select 1000–200 hPa
q = q.sel(pressure_level=slice(1000, 200))
u = u.sel(pressure_level=slice(1000, 200))
v = v.sel(pressure_level=slice(1000, 200))

# Sort pressure levels 
q = q.sortby("pressure_level", ascending=True)
u = u.sortby("pressure_level", ascending=True)
v = v.sortby("pressure_level", ascending=True)

# Convert pressure from hPa to Pa
pressure_pa = q.pressure_level * hpa_to_pa

# Compute diff
dp = np.diff(pressure_pa)
dp = np.concatenate([dp[:1], dp])

# IVT components 
weights = xr.DataArray(dp, dims="pressure_level", coords={"pressure_level": q.pressure_level})
IVTE = (q * u * weights).sum(dim="pressure_level") / g
IVTN = (q * v * weights).sum(dim="pressure_level") / g

# Save IVTE
IVTE = IVTE.to_dataset(name="IVTE")
IVTE["IVTE"].attrs["units"] = "kg m-1 s-1"
IVTE.to_netcdf(f"{path_out}/IVTE_ERA5.nc")

# Save IVTN
IVTN = IVTN.to_dataset(name="IVTN")
IVTN["IVTN"].attrs["units"] = "kg m-1 s-1"
IVTN.to_netcdf(f"{path_out}/IVTN_ERA5.nc")

