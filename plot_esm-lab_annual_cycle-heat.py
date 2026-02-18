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
# DATA PATH
# =============================================================================
data_path = Path("/home/esp-shared-a/Distribution/Diploma/ESM/data/ESM_2025/ERA5/month")

f_shf = data_path / "avg_ishf_ERA5_1991-2020.nc"    # Sensible heat flux (J m-2)
f_lhf = data_path / "avg_slhtf_ERA5_1991-2020.nc"   # Latent heat flux (J m-2)
f_sw  = data_path / "avg_snswrf_ERA5_1991-2020.nc"  # Net shortwave radiation (W m-2)
f_lw  = data_path / "avg_snlwrf_ERA5_1991-2020.nc"  # Net longwave radiation (W m-2)

# =============================================================================
# REGIONS (lon in degrees east)
# =============================================================================
regions = {
    'Ghana': {'lon': [356.5, 361.5], 'lat': [4.5, 11.5]},
    'Cameroon': {'lon': [8.5, 16.5], 'lat': [2.0, 13.0]},
    'Angola': {'lon': [11.5, 24.5], 'lat': [-18.0, -5.0]},
    'Chocó (Colombia)': {'lon': [281.5, 284.0], 'lat': [4.0, 8.0]},
    'Northeast Brazil': {'lon': [314.0, 325.0], 'lat': [-16.0, -2.0]},
    'South Brazil': {'lon': [302.0, 312.0], 'lat': [-34.0, -22.0]}
}

panel_labels = [
    'a) Ghana', 'b) Cameroon', 'c) Angola',
    'd) Chocó (Colombia)', 'e) Northeast Brazil', 'f) South Brazil'
]

months = ['Jan','Feb','Mar','Apr','May','Jun',
          'Jul','Aug','Sep','Oct','Nov','Dec']

# =============================================================================
# LOAD DATA
# =============================================================================
ds_shf = xr.open_dataset(f_shf)
ds_lhf = xr.open_dataset(f_lhf)
ds_sw  = xr.open_dataset(f_sw)
ds_lw  = xr.open_dataset(f_lw)

v_shf = list(ds_shf.data_vars)[0]
v_lhf = list(ds_lhf.data_vars)[0]
v_sw  = list(ds_sw.data_vars)[0]
v_lw  = list(ds_lw.data_vars)[0]

# =============================================================================
# COMPUTE REGIONAL MONTHLY CLIMATOLOGIES
# =============================================================================
region_data = {}

for region, box in regions.items():

    shf = ds_shf[v_shf].sel(
        longitude=slice(box['lon'][0], box['lon'][1]),
        latitude=slice(box['lat'][1], box['lat'][0])
    ).mean(dim=['longitude', 'latitude'])

    lhf = ds_lhf[v_lhf].sel(
        longitude=slice(box['lon'][0], box['lon'][1]),
        latitude=slice(box['lat'][1], box['lat'][0])
    ).mean(dim=['longitude', 'latitude'])

    sw = ds_sw[v_sw].sel(
        longitude=slice(box['lon'][0], box['lon'][1]),
        latitude=slice(box['lat'][1], box['lat'][0])
    ).mean(dim=['longitude', 'latitude'])

    lw = ds_lw[v_lw].sel(
        longitude=slice(box['lon'][0], box['lon'][1]),
        latitude=slice(box['lat'][1], box['lat'][0])
    ).mean(dim=['longitude', 'latitude'])

    # Net radiation
    rn = sw + lw

    # Ground heat flux (residual of surface energy balance)
    G = rn - (lhf*(-1) + shf*(-1))

    region_data[region] = {
        'RN' : rn.groupby('valid_time.month').mean().values,
        'LE' : lhf.groupby('valid_time.month').mean().values,
        'SH' : shf.groupby('valid_time.month').mean().values,
        'G'  : G.groupby('valid_time.month').mean().values
    }

ds_shf.close()
ds_lhf.close()
ds_sw.close()
ds_lw.close()

# =============================================================================
# PLOT
# =============================================================================
fig, axes = plt.subplots(3, 2, figsize=(8, 10))
axes = axes.flatten()

for i, (region, d) in enumerate(region_data.items()):

    ax = axes[i]

    ax.plot(months, d['RN'], 'k', lw=1.5, label='R$_n$')
    ax.plot(months, -d['LE'], 'b--', lw=1.5, label='LE')
    ax.plot(months, -d['SH'], 'r--', lw=1.5, label='SH')
    ax.plot(months, d['G'],  color='orange', ls='--', lw=1.5, label='G')
    ax.tick_params(direction='in', which='both', top=True, right=True)

    ax.text(0.02, 0.90, panel_labels[i],
            transform=ax.transAxes, fontsize=10)

    ax.set_ylabel('W m$^{-2}$')
    ax.set_ylim(-40, 200)
    ax.legend(fontsize=8)

plt.tight_layout()
plt.savefig("annual_cycle_heat_ESM2025.png",
            dpi=400, bbox_inches='tight')
plt.show()

print("Figure saved: annual_cycle_heat_ESM2025.png")
