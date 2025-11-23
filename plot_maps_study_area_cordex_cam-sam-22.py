# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "May 14, 2025"
__description__ = "This script plot study area"

import os
import sys
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

from cartopy import config
from netCDF4 import Dataset as nc
from matplotlib.patches import Rectangle
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def import_orog(dirnc, domain):

	number = 9
	
	if len(sys.argv) > 1:
		RCMf = nc(sys.argv[1], mode='r')
	else:
		RCMf = nc(os.path.join(dirnc,'orog_{0}_ECMWF-ERAINT_evaluation_r1i1p1_ICTP-RegCM4-7_v0_fx.nc'.format(domain)), mode='r')

	lat  = RCMf.variables['lat'][:,:]
	lon  = RCMf.variables['lon'][:,:]
	topo = RCMf.variables['orog'][:,:]
	RCMf.close()

	print(topo.shape)
	
	ny,nx = topo.shape
	border_mask = np.full((ny, nx), np.nan)
	border_mask[:number, :] = 1
	border_mask[-number:, :] = 1
	border_mask[:, :number] = 1
	border_mask[:, -number:] = 1

	return lat, lon, border_mask


# Import dataset
lat_i, lon_i, border_mask_i = import_orog('/afs/ictp.it/home/m/mda_silv/Downloads', 'CAM-22')
lat_ii, lon_ii, border_mask_ii = import_orog('/afs/ictp.it/home/m/mda_silv/Downloads', 'SAM-22')

# Plot figure
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
font_size = 8

ax.contourf(lon_i, lat_i, border_mask_i, cmap='gray', levels=[0, 1])
ax.contourf(lon_ii, lat_ii, border_mask_ii, cmap='gray', levels=[0, 1])
ax.stock_img()

plt.text(130, -85, u'\u25B2 \nN', color='black', fontsize=6, fontweight='bold')
plt.text(-49, -46, u'SAM', color='gray', fontsize=font_size, fontweight='bold')
plt.text(-130, -10, u'CAM', color='gray', fontsize=font_size, fontweight='bold')

ax.coastlines()
ax.add_feature(cfeature.BORDERS, linestyle=':', linewidth=0.5)

gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.75, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': font_size}
gl.ylabel_style = {'size': font_size}
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()
gl.xlocator = plt.FixedLocator(np.arange(-180, 181, 30))
gl.ylocator = plt.FixedLocator(np.arange(-90, 91, 30))

# Path out to save figure
path_out = '/afs/ictp.it/home/m/mda_silv/Downloads'
name_out = 'pyplt_CORDEX_CAM-SAM_domains.png'
plt.savefig(os.path.join(path_out, name_out), dpi=400, bbox_inches='tight')
plt.show()
exit()

