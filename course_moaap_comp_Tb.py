# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Jun 17, 2026"
__description__ = "This script compute Tb"

import os
import glob
import numpy as np
import xarray as xr
import metpy.xarray    
       
from metpy.units import units

# Paths
path_in = "/leonardo/home/userexternal/mdasilva/leonardo_work/MOAAP/course/ERA5"
path_out = "/leonardo/home/userexternal/mdasilva/leonardo_work/MOAAP/course/ERA5"
os.makedirs(path_out, exist_ok=True)

# Constants
sigma = 5.670374419e-8 * units('W / m^2 / K^4')
emis = 0.97

# Open dataset
ds = xr.open_dataset(f"{path_in}/avg_tnlwrf_era5_1-5Jan2020.nc")
rlut = ds['avg_tnlwrf'] * units('W/m^2')

# Compute Tb
Tb = (rlut / (emis * sigma))**0.25
Tb = Tb.metpy.convert_units('kelvin')

# Save to dataset
ds['Tb'] = Tb
ds['Tb'].attrs = {
	'long_name': 'Brightness temperature',
	'units': 'K',
	'emissivity': emis,
	'method': 'Stefan-Boltzmann inversion'
	}

# Save Tb
file_name="Tb_era5_1-5Jan2020.nc"
fname = os.path.basename(file_name) 
out = os.path.join(path_out, fname.replace('avg_tnlwrf', 'Tb'))
ds[['Tb']].to_netcdf(out)

