# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilvae@gmail.com"
__date__        = "February 15, 2026"
__description__ = "ESM lectures"

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from pathlib import Path

# =============================================================================
# DATA PATHS
# =============================================================================
data_path = Path("/home/esp-shared-a/Distribution/Diploma/ESM/data/ESM_2025/ERA5/month")

tp_file   = data_path / "tp_ERA5_1991-2020.nc"
pevr_file = data_path / "pev_ERA5_1991-2020.nc"
lwe_file  = data_path / "e_ERA5_1991-2020.nc"  

# =============================================================================
# REGIONS
# =============================================================================
regions = {
    'Ghana': {'lon': [356.5, 361.5], 'lat': [4.5, 11.5]},
    'Cameroon': {'lon': [8.5, 16.5], 'lat': [2.0, 13.0]},
    'Angola': {'lon': [11.5, 24.5], 'lat': [-18.0, -5.0]},
    'Chocó (Colombia)': {'lon': [281.5, 284.0], 'lat': [4.0, 8.0]},
    'Northeast Brazil': {'lon': [314.0, 325.0], 'lat': [-16.0, -2.0]},
    'South Brazil': {'lon': [302.0, 312.0], 'lat': [-34.0, -22.0]}
}

identifiers = [
    'a) Ghana', 'b) Cameroon', 'c) Angola',
    'd) Chocó (Colombia)', 'e) Northeast Brazil', 'f) South Brazil'
]

months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']

# =============================================================================
# LOAD DATA
# =============================================================================
ds_tp  = xr.open_dataset(tp_file)
ds_pet = xr.open_dataset(pevr_file)
ds_lwe = xr.open_dataset(lwe_file)

var_tp  = list(ds_tp.data_vars)[0]
var_pet = list(ds_pet.data_vars)[0]
var_lwe = list(ds_lwe.data_vars)[0]

region_data = {}

for region, b in regions.items():

    # --- Precipitation ---
    tp = ds_tp[var_tp].sel(
        longitude=slice(b['lon'][0], b['lon'][1]),
        latitude=slice(b['lat'][1], b['lat'][0])
    ).mean(dim=['longitude','latitude']) * 1000.0  # mm/day

    tp_m = tp.groupby('valid_time.month').mean().values

    # --- PET ---
    pet = ds_pet[var_pet].sel(
        longitude=slice(b['lon'][0], b['lon'][1]),
        latitude=slice(b['lat'][1], b['lat'][0])
    ).mean(dim=['longitude','latitude']) * 1000.0  # mm/day

    pet_m = np.abs(pet.groupby('valid_time.month').mean().values)

    # --- LWE evaporation amount ---
    lwe = ds_lwe[var_lwe].sel(
        longitude=slice(b['lon'][0], b['lon'][1]),
        latitude=slice(b['lat'][1], b['lat'][0])
    ).mean(dim=['longitude','latitude']) * 1000.0  # m → mm/day

    lwe_m = np.abs(lwe.groupby('valid_time.month').mean().values)

    region_data[region] = {
        'tp': tp_m,
        'pet': pet_m,
        'e': lwe_m
    }

ds_tp.close()
ds_pet.close()
ds_lwe.close()

# Plot figure
fig, axes = plt.subplots(3, 2, figsize=(8, 10))
axes = axes.flatten()

for i, (region, d) in enumerate(region_data.items()):
    ax = axes[i]

    ax.plot(months, d['pet'], 'k', lw=1.5, label='PET')
    ax.plot(months, d['tp'], 'b--', lw=1.5, label='P')
    ax.plot(months, d['e'], 'r--',  lw=1.5, label='E')

    ax.text(0.02, 0.90, identifiers[i],
            transform=ax.transAxes,
            fontsize=10)

    ax.set_ylabel('mm/day')
    ax.legend(fontsize=9)

# Save figure
plt.tight_layout()
plt.savefig("annual_cycle_6regions_3vars.png", dpi=400, bbox_inches='tight')
plt.show()

print("Figure saved: annual_cycle_6regions_3vars.png")
