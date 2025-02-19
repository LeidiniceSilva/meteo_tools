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
from mpl_toolkits.basemap import Basemap

rcParams['font.family'] = 'Liberation Serif'
font_size = 12

def import_mean(param, hw):

	arq   = '/afs/ictp.it/home/m/mda_silv/Documents/Heat_wave/ERA5/{}_era5_{}_mean.nc'.format(param, hw)	
	data  = netCDF4.Dataset(arq)
	var   = data.variables[param][:] 
	lat   = data.variables['latitude'][:]	
	lon   = data.variables['longitude'][:]
	
	if param == 'msl' or param == 't2m':
		if lat[0] > lat[-1]:  # Check if latitudes are descending
			lat = lat[::-1]  # Reverse the latitude array
			mean = var[:][0,::-1,:]
	if param == 'z':
		if lat[0] > lat[-1]:  # Check if latitudes are descending
			lat = lat[::-1]  # Reverse the latitude array
			mean = var[:][0,1,::-1,:]
	if param == 'u' or param == 'v':
		if lat[0] > lat[-1]:  # Check if latitudes are descending
			lat = lat[::-1]  # Reverse the latitude array
			mean = var[:][:,:,::-1,:]
	else:
		if lat[0] > lat[-1]:  # Check if latitudes are descending
			lat = lat[::-1]  # Reverse the latitude array
			mean = var[:][0,3,::-1,:]

	return lat, lon, mean
	

def import_anomaly(param, hw):

	arq   = '/afs/ictp.it/home/m/mda_silv/Documents/Heat_wave/ERA5/{}_era5_{}_anom.nc'.format(param, hw)	
	data  = netCDF4.Dataset(arq)
	var   = data.variables[param][:] 
	lat   = data.variables['latitude'][:]	
	lon   = data.variables['longitude'][:]
	
	if param == 'msl' or param == 't2m':
		if lat[0] > lat[-1]:  # Check if latitudes are descending
			lat = lat[::-1]  # Reverse the latitude array
			anomaly = var[:][0,::-1,:]
	if param == 'z':
		if lat[0] > lat[-1]:  # Check if latitudes are descending
			lat = lat[::-1]  # Reverse the latitude array
			anomaly = var[:][0,1,::-1,:]
	if param == 'u' or param == 'v':
		if lat[0] > lat[-1]:  # Check if latitudes are descending
			lat = lat[::-1]  # Reverse the latitude array
			anomaly = var[:][:,:,::-1,:]
	else:
		if lat[0] > lat[-1]:  # Check if latitudes are descending
			lat = lat[::-1]  # Reverse the latitude array
			anomaly = var[:][0,3,::-1,:]
	
	return lat, lon, anomaly


def basemap(lat, lon):

	map = Basemap(projection='cyl', llcrnrlon=180, llcrnrlat=-70., urcrnrlon=360,urcrnrlat=10, resolution='c')
	map.drawmeridians(np.arange(180, 360, 30), size=font_size, fontname='Liberation Serif', labels=[0,0,0,1], linewidth=0.5, color='black')
	map.drawparallels(np.arange(-70, 10, 20), size=font_size, fontname='Liberation Serif', labels=[1,0,0,0], linewidth=0.5, color='black')
	map.drawcoastlines(linewidth=0.5, color='black')
	lons, lats = np.meshgrid(lon, lat)
	xx, yy = map(lons,lats)
	
	return map, xx, yy
	
	
# Import model and obs dataset 
lat, lon, msl_anom_i = import_anomaly('msl', 'hw_1_17-27Sep2023')
lat, lon, t2m_anom_i = import_anomaly('t2m', 'hw_1_17-27Sep2023')
lat, lon, q_anom_i = import_anomaly('q', 'hw_1_17-27Sep2023')
lat, lon, u_anom_i = import_anomaly('u', 'hw_1_17-27Sep2023')
lat, lon, v_anom_i = import_anomaly('v', 'hw_1_17-27Sep2023')
lat, lon, z_anom_i = import_anomaly('z', 'hw_1_17-27Sep2023')

lat, lon, q_mean_i = import_mean('q', 'hw_1_17-27Sep2023')
lat, lon, u_mean_i = import_mean('u', 'hw_1_17-27Sep2023')
lat, lon, v_mean_i = import_mean('v', 'hw_1_17-27Sep2023')
lat, lon, z_mean_i = import_mean('z', 'hw_1_17-27Sep2023')

lat, lon, msl_anom_ii = import_anomaly('msl', 'hw_2_11-18Nov2023')
lat, lon, t2m_anom_ii = import_anomaly('t2m', 'hw_2_11-18Nov2023')
lat, lon, q_anom_ii = import_anomaly('q', 'hw_2_11-18Nov2023')
lat, lon, u_anom_ii = import_anomaly('u', 'hw_2_11-18Nov2023')
lat, lon, v_anom_ii = import_anomaly('v', 'hw_2_11-18Nov2023')
lat, lon, z_anom_ii = import_anomaly('z', 'hw_2_11-18Nov2023')

lat, lon, q_mean_ii = import_mean('q', 'hw_2_11-18Nov2023')
lat, lon, u_mean_ii = import_mean('u', 'hw_2_11-18Nov2023')
lat, lon, v_mean_ii = import_mean('v', 'hw_2_11-18Nov2023')
lat, lon, z_mean_ii = import_mean('z', 'hw_2_11-18Nov2023')

# Plot figure 
fig = plt.figure(figsize=(10, 10))

# Subplot 1
ax = fig.add_subplot(4, 2, 1)  
map, xx, yy = basemap(lat, lon)
plt_map = map.contour(xx, yy, msl_anom_i/100, colors='black', levels=[-15,-10,-5,-1,1,5,10,15], linewidths=0.5)
plt.clabel(plt_map, inline=1, fontsize=font_size)
plt_map = map.contourf(xx, yy, t2m_anom_i, cmap=cm.bwr, levels=[-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10], extend='both') 
plt.title(u'(a)', loc='left', fontsize=font_size, fontname='Liberation Serif', fontweight='bold')
    
# Subplot 2
ax = fig.add_subplot(4, 2, 2)  
map, xx, yy = basemap(lat, lon)
plt_map = map.contour(xx, yy, msl_anom_ii/100, colors='black', levels=[-15,-10,-5,-1,1,5,10,15], linewidths=0.5)
plt.clabel(plt_map, inline=1, fontsize=font_size)
plt_map = map.contourf(xx, yy, t2m_anom_ii, cmap=cm.bwr, levels=[-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7,8,9,10], extend='both') 
plt.title(u'(b)', loc='left', fontname='Liberation Serif', fontsize=font_size, fontweight='bold')
# Set colobar
cbar = plt.colorbar(plt_map,  cax=fig.add_axes([0.92, 0.705, 0.01, 0.18]))
cbar.ax.tick_params(labelsize=font_size)

# Subplot 3
ax = fig.add_subplot(4, 2, 3) 
map, xx, yy = basemap(lat, lon)
plt_map = map.contour(xx, yy, z_mean_i/10, 6, colors='black', linewidths=0.5)
plt.clabel(plt_map, inline=1, fontsize=font_size)
plt_map = map.contourf(xx, yy, z_anom_i/10, cmap=cm.PiYG, levels=[-200,-180,-160,-140,-120,-100,-80,-60,-40,-20,20,40,60,80,100,120,140,160,180,200], extend='both') 
plt.title(u'(c)', loc='left', fontname='Liberation Serif', fontsize=font_size, fontweight='bold')

# Subplot 4
ax = fig.add_subplot(4, 2, 4) 
map, xx, yy = basemap(lat, lon)
plt_map = map.contour(xx, yy, z_mean_ii/10, 6, colors='black', linewidths=0.5)
plt.clabel(plt_map, inline=1, fontsize=font_size)
plt_map = map.contourf(xx, yy, z_anom_ii/10, cmap=cm.PiYG, levels=[-200,-180,-160,-140,-120,-100,-80,-60,-40,-20,20,40,60,80,100,120,140,160,180,200], extend='both') 
plt.title(u'(d)', loc='left', fontname='Liberation Serif', fontsize=font_size, fontweight='bold')
# Set colobar
cbar = plt.colorbar(plt_map,  cax=fig.add_axes([0.92, 0.505, 0.01, 0.18]))
cbar.ax.tick_params(labelsize=font_size)

# Subplot 5
ax = fig.add_subplot(4, 2, 5) 
map, xx, yy = basemap(lat, lon)
plt_map = map.contour(xx, yy, u_mean_i[0,0,:,:], colors='black', linewidths=0.5)
plt.clabel(plt_map, inline=1, fontsize=font_size)
plt_map = map.contourf(xx, yy, u_anom_i[0,0,:,:], cmap=cm.RdBu_r, levels=[-30,-27,-24,-21,-18,-15,-12,-9,-6,-3,3,6,9,12,15,18,21,24,27,30], extend='both') 
plt.title(u'(e)', loc='left', fontsize=font_size, fontname='Liberation Serif', fontweight='bold')

# Subplot 6
ax = fig.add_subplot(4, 2, 6) 
map, xx, yy = basemap(lat, lon)
plt_map = map.contour(xx, yy, u_mean_ii[0,0,:,:], colors='black', linewidths=0.5)
plt.clabel(plt_map, inline=1, fontsize=font_size)
plt_map = map.contourf(xx, yy, u_anom_ii[0,0,:,:], cmap=cm.RdBu_r, levels=[-30,-27,-24,-21,-18,-15,-12,-9,-6,-3,3,6,9,12,15,18,21,24,27,30], extend='both') 
plt.title(u'(f)', loc='left', fontsize=font_size, fontname='Liberation Serif', fontweight='bold')
# Set colobar
cbar = plt.colorbar(plt_map, cax=fig.add_axes([0.92, 0.305, 0.01, 0.18]))
cbar.ax.tick_params(labelsize=font_size)

# Subplot 7
ax = fig.add_subplot(4, 2, 7) 
map, xx, yy = basemap(lat, lon)
plt_map = map.contourf(xx, yy, q_anom_i*1000, cmap=cm.BrBG, levels=[-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5], extend='both') 
plt.title(u'(g)', loc='left', fontsize=font_size, fontname='Liberation Serif', fontweight='bold')
map.streamplot(xx, yy, u_mean_i[0,3,:,:], v_mean_i[0,3,:,:], color='black', density=3, linewidth=0.5)
	
# Subplot 8
ax = fig.add_subplot(4, 2, 8) 
map, xx, yy = basemap(lat, lon)
plt_map = map.contourf(xx, yy, q_anom_ii*1000, cmap=cm.BrBG, levels=[-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5], extend='both') 
plt.title(u'(h)', loc='left', fontsize=font_size, fontname='Liberation Serif', fontweight='bold')
map.streamplot(xx, yy, u_mean_ii[0,3,:,:], v_mean_ii[0,3,:,:], color='black', density=3, linewidth=0.5)
# Set colobar
cbar = plt.colorbar(plt_map,  cax=fig.add_axes([0.92, 0.105, 0.01, 0.18]))
cbar.ax.tick_params(labelsize=font_size)

# Path out to save figure
path_out = '/afs/ictp.it/home/m/mda_silv/Documents/Heat_wave/figs'
name_out = 'pyplt_maps_anom_era5_heat-waves_2023.png'
plt.savefig(os.path.join(path_out, name_out), dpi=400, bbox_inches='tight')
plt.show()
exit()
