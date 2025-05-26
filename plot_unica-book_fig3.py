# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Dec 04, 2024"
__description__ = "Script to plot average annual accumulated precipitation climatology"

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
import matplotlib.ticker as mticker

# Abrir o arquivo NetCDF
ds = xr.open_dataset('tp_ERA5_clim_1991-2020.nc')
pr = ds['tp'] 

# Plotar o mapa da climatologia 
plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
pr.plot(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap='Blues',
    vmin=0,
    vmax=3000,
    cbar_kwargs={
        'label': 'Precipitação acumulada anual média (mm/ano)',
        'shrink': 0.6
    }
)

ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.set_title('Climatologia da precipitação acumulada anual - ERA5 (1991–2020)', fontsize=12)

gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.7, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xformatter = cticker.LongitudeFormatter()
gl.yformatter = cticker.LatitudeFormatter()
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}

# Salvar a figura
plt.savefig('/afs/ictp.it/home/m/mda_silv/Downloads/precipitacao_anual_acumulada_era5.png', dpi=300, bbox_inches='tight')
plt.show()
exit()
