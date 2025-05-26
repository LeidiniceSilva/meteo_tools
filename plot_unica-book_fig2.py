# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Dec 04, 2024"
__description__ = "Script to plot textbook figures"

import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker
import matplotlib.ticker as mticker

# Abrir o arquivo NetCDF
ds = xr.open_dataset('t2m_ERA5_1991-2020.nc')

# Selecionar a variável de temperatura 
t2m = ds['t2m'] - 273.15  

# Calcular a climatologia anual 
climatology_annual = t2m.mean(dim="valid_time")

# Plotar o mapa da climatologia anual 
plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())
climatology_annual.plot(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap='jet',
    cbar_kwargs={'label': 'Temperatura do ar (°C)',
        'shrink': 0.6}
)

# Adicionar feições geográficas ===
ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.set_title('Climatologia média da temperatura do ar - ERA5 (1991 - 2020)')

# Adicionar paralelos e meridianos com graus
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.7, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xformatter = cticker.LongitudeFormatter()
gl.yformatter = cticker.LatitudeFormatter()
gl.xlabel_style = {'size': 10}
gl.ylabel_style = {'size': 10}

plt.savefig('/afs/ictp.it/home/m/mda_silv/Downloads/climatologia_temperatura_era5.png', dpi=300, bbox_inches='tight')
plt.show()
exit()

