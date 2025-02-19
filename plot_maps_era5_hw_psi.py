# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Mar 04, 2024"
__description__ = "This script plot bias maps"

import os
import netCDF4
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from matplotlib import rcParams
from scipy.integrate import cumulative_trapezoid
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.basemap import Basemap


rcParams['font.family'] = 'Liberation Serif'
font_size = 12

def import_mean(param, hw, lev):

	arq   = '/afs/ictp.it/home/m/mda_silv/Documents/Heat_wave/ERA5/{0}_era5_{1}_anom.nc'.format(param, hw)	
	data  = netCDF4.Dataset(arq)
	var   = data.variables[param][:] 
	lat   = data.variables['latitude'][:]	
	lon   = data.variables['longitude'][:]
	
	if lat[0] > lat[-1]:  # Check if latitudes are descending
		lat = lat[::-1]  # Reverse the latitude array
		mean = var[:][0,lev,::-1,:]
	
	return lat, lon, mean
	

def basemap(lat, lon):

	map = Basemap(projection='cyl', llcrnrlon=0, llcrnrlat=-90., urcrnrlon=360, urcrnrlat=90, resolution='c')
	map.drawmeridians(np.arange(0, 360, 30), size=font_size, fontname='Liberation Serif', labels=[0,0,0,1], linewidth=0.5, color='black')
	map.drawparallels(np.arange(-90, 90, 30), size=font_size, fontname='Liberation Serif', labels=[1,0,0,0], linewidth=0.5, color='black')
	map.drawcoastlines(linewidth=0.5, color='black')
	lons, lats = np.meshgrid(lon, lat)
	xx, yy = map(lons,lats)
	
	return map, xx, yy


def calculate_streamfunction(u, v, lat, lon):

        # Integrate to get streamfunction
        psi = cumulative_trapezoid(u, lat, axis=0, initial=0) 
        psi -= cumulative_trapezoid(v, lon, axis=1, initial=0)  

        # Calculate anomaly
        psi_mean_lat = np.mean(psi, axis=1, keepdims=True)  
        psi_anomaly = (psi - psi_mean_lat) / 1000
        
        return psi_anomaly
    

def plot_streamfunction(lat, lon, u, v, psi, level):

	X, Y = np.meshgrid(lon, lat)
	
# Import model and obs dataset 
lat, lon, u_mean_200_i = import_mean('u', 'hw_1_17-27Sep2023', 0)
lat, lon, v_mean_200_i = import_mean('v', 'hw_1_17-27Sep2023', 0)

lat, lon, u_mean_850_i = import_mean('u', 'hw_1_17-27Sep2023', 3)
lat, lon, v_mean_850_i = import_mean('v', 'hw_1_17-27Sep2023', 3)

lat, lon, u_mean_200_ii = import_mean('u', 'hw_2_11-18Nov2023', 0)
lat, lon, v_mean_200_ii = import_mean('v', 'hw_2_11-18Nov2023', 0)

lat, lon, u_mean_850_ii = import_mean('u', 'hw_2_11-18Nov2023', 3)
lat, lon, v_mean_850_ii = import_mean('v', 'hw_2_11-18Nov2023', 3)

# Compute streamfunction for 850 hPa level as an example
psi_850_i = calculate_streamfunction(u_mean_850_i, v_mean_850_i, lat, lon)
psi_200_i = calculate_streamfunction(u_mean_200_i, v_mean_200_i, lat, lon)

psi_850_ii = calculate_streamfunction(u_mean_850_ii, v_mean_850_ii, lat, lon)
psi_200_ii = calculate_streamfunction(u_mean_200_ii, v_mean_200_ii, lat, lon)

# Define levels for the contour
levels_850_i = np.linspace(np.nanmin(psi_850_i), np.nanmax(psi_850_i), 20)
levels_200_i = np.linspace(np.nanmin(psi_200_i), np.nanmax(psi_200_i), 20)

levels_850_ii = np.linspace(np.nanmin(psi_850_ii), np.nanmax(psi_850_ii), 20)
levels_200_ii = np.linspace(np.nanmin(psi_200_ii), np.nanmax(psi_200_ii), 20)

# Plot figure
fig = plt.figure(figsize=(10, 8))

ax = fig.add_subplot(2, 1, 1)   
map, xx, yy = basemap(lat, lon)
plt_map1 = map.contourf(xx, yy, psi_200_i, levels=levels_200_i, cmap="bwr", extend='both')
plt_map2 = map.contour(xx, yy, psi_850_i, levels=4, linewidths=0.5, colors='black')
plt.clabel(plt_map2, inline=True)
plt.title(u'(a)', loc='left', fontsize=font_size, fontname='Liberation Serif', fontweight='bold')
cbar = plt.colorbar(plt_map1)
cbar.ax.tick_params(labelsize=font_size)

ax = fig.add_subplot(2, 1, 2)   
map, xx, yy = basemap(lat, lon)
plt_map1 = map.contourf(xx, yy, psi_200_ii, levels=levels_200_ii, cmap="bwr", extend='both')
plt_map2 = map.contour(xx, yy, psi_850_ii, levels=2, linewidths=0.5, colors='black')
plt.clabel(plt_map2, inline=True)
plt.title(u'(b)', loc='left', fontsize=font_size, fontname='Liberation Serif', fontweight='bold')
cbar = plt.colorbar(plt_map1)
cbar.ax.tick_params(labelsize=font_size)

# Path out to save figure
path_out = '/afs/ictp.it/home/m/mda_silv/Documents/Heat_wave/figs'
name_out = 'pyplt_maps_psi_era5_heat-waves_2023.png'
plt.savefig(os.path.join(path_out, name_out), dpi=400, bbox_inches='tight')
plt.show()
exit()
