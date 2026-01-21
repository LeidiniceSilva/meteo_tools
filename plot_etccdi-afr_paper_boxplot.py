# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "Jan 12, 2026"
__description__ = "This script plot annual cycle"

import os
import netCDF4
import numpy as np
import matplotlib.pyplot as plt


def import_dataset_i(param, dataset, domain):

	arq  = '/home/mda_silv/data/{0}_{1}_{2}_mon_1979-2014.nc'.format(param, dataset, domain)
	data = netCDF4.Dataset(arq)
	var  = data.variables[param][:]
	lat  = data.variables['lat'][:]
	lon  = data.variables['lon'][:]
	value = var[:][:,:,:]
	mean = np.nanmean(np.nanmean(value, axis=1), axis=1)
	mean_ = mean[:-120]
	
	return mean_, mean

def import_dataset_ii(param, dataset, domain):

        arq  = '/home/mda_silv/data/{0}_{1}_{2}_mon_1979-2014.nc'.format(param, dataset, domain)
        data = netCDF4.Dataset(arq)
        var  = data.variables[param][:]
        lat  = data.variables['latitude'][:]
        lon  = data.variables['longitude'][:]
        value = var[:][:,:,:]
        mean = np.nanmean(np.nanmean(value, axis=1), axis=1)
        mean_ = mean[:-120]

        return mean_, mean
    
    
# Import model and obs dataset
pr_cpc_wz_p1, pr_cpc_wz_p2 = import_dataset_i('precip', 'cpc', 'wz')
pr_cpc_cz_p1, pr_cpc_cz_p2 = import_dataset_i('precip', 'cpc', 'cz')
pr_cpc_sz_p1, pr_cpc_sz_p2 = import_dataset_i('precip', 'cpc', 'sz')

pr_era5_wz_p1, pr_era5_wz_p2 = import_dataset_ii('tp', 'era5', 'wz')
pr_era5_cz_p1, pr_era5_cz_p2 = import_dataset_ii('tp', 'era5', 'cz')
pr_era5_sz_p1, pr_era5_sz_p2 = import_dataset_ii('tp', 'era5', 'sz')

tmp_cpc_wz_p1, tmp_cpc_wz_p2 = import_dataset_i('tmax', 'cpc', 'wz')
tmp_cpc_cz_p1, tmp_cpc_cz_p2 = import_dataset_i('tmax', 'cpc', 'cz')
tmp_cpc_sz_p1, tmp_cpc_sz_p2 = import_dataset_i('tmax', 'cpc', 'sz')

tmp_era5_wz_p1, tmp_era5_wz_p2 = import_dataset_ii('mn2t', 'era5', 'wz')
tmp_era5_cz_p1, tmp_era5_cz_p2 = import_dataset_ii('mn2t', 'era5', 'cz')
tmp_era5_sz_p1, tmp_era5_sz_p2 = import_dataset_ii('mn2t', 'era5', 'sz')

# Plot figure
fig, axes = plt.subplots(3,2, figsize=(16,14))

labels = ['CPC 1979-2005', 'CPC 1979-2014', 'ERA5 1979-2005', 'ERA5 1979-2014']
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
colors = ['lightblue', 'blue', 'lightgreen', 'green']

ax = axes[0,0]
datasets = [pr_cpc_wz_p1, pr_cpc_wz_p2, pr_era5_wz_p1, pr_era5_wz_p2]
data_to_plot = []
for m in range(12):
    for ds in datasets:
        month_values = ds[m::12]
        data_to_plot.append(month_values)
positions = []
for k in range(12):
    positions.extend(np.array(range(len(datasets))) + k*(len(datasets)+1))
bplot = ax.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)
for patch, color in zip(bplot['boxes'], colors*12):
    patch.set_facecolor(color)

ax.set_ylim(0, 10)
ax.set_yticks(np.arange(0, 11, 1))
ax.set_xticks([k*(len(datasets)+1) + (len(datasets)-1)/2 for k in range(12)])
ax.set_xticklabels(months)
ax.set_title('a) West Africa', loc='left', fontsize=10, fontweight='bold')
ax.set_ylabel('Precipitation (mm/d)')
ax.grid(True, linestyle='--', alpha=0.5)

ax = axes[0,1]
datasets = [tmp_cpc_wz_p1, tmp_cpc_wz_p2, tmp_era5_wz_p1, tmp_era5_wz_p2]
data_to_plot = []
for m in range(12):
    for ds in datasets:
        month_values = ds[m::12]
        data_to_plot.append(month_values)
positions = []
for k in range(12):
    positions.extend(np.array(range(len(datasets))) + k*(len(datasets)+1))
bplot = ax.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)
for patch, color in zip(bplot['boxes'], colors*12):
    patch.set_facecolor(color)

ax.set_ylim(20, 32)
ax.set_yticks(np.arange(20, 36, 1))
ax.set_xticks([k*(len(datasets)+1) + (len(datasets)-1)/2 for k in range(12)])
ax.set_xticklabels(months)
ax.set_title('b) West Africa', loc='left', fontsize=10, fontweight='bold')
ax.set_ylabel('Temperature (°C)')
ax.grid(True, linestyle='--', alpha=0.5)

ax = axes[1,0]
datasets = [pr_cpc_cz_p1, pr_cpc_cz_p2, pr_era5_cz_p1, pr_era5_cz_p2]
data_to_plot = []
for m in range(12):
    for ds in datasets:
        month_values = ds[m::12]
        data_to_plot.append(month_values)
positions = []
for k in range(12):
    positions.extend(np.array(range(len(datasets))) + k*(len(datasets)+1))
bplot = ax.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)
for patch, color in zip(bplot['boxes'], colors*12):
    patch.set_facecolor(color)

ax.set_ylim(0, 10)
ax.set_yticks(np.arange(0, 11, 1))
ax.set_xticks([k*(len(datasets)+1) + (len(datasets)-1)/2 for k in range(12)])
ax.set_xticklabels(months)
ax.set_title('c) Coast zone', loc='left', fontsize=10, fontweight='bold')
ax.set_ylabel('Precipitation (mm/d)')
ax.grid(True, linestyle='--', alpha=0.5)

ax = axes[1,1]
datasets = [tmp_cpc_cz_p1, tmp_cpc_cz_p2, tmp_era5_cz_p1, tmp_era5_cz_p2]
data_to_plot = []
for m in range(12):
    for ds in datasets:
        month_values = ds[m::12]
        data_to_plot.append(month_values)
positions = []
for k in range(12):
    positions.extend(np.array(range(len(datasets))) + k*(len(datasets)+1))
bplot = ax.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)
for patch, color in zip(bplot['boxes'], colors*12):
    patch.set_facecolor(color)

ax.set_ylim(20, 32)
ax.set_yticks(np.arange(20, 36, 1))
ax.set_xticks([k*(len(datasets)+1) + (len(datasets)-1)/2 for k in range(12)])
ax.set_xticklabels(months)
ax.set_title('d) Coast zone', loc='left', fontsize=10, fontweight='bold')
ax.set_ylabel('Temperature (°C)')
ax.grid(True, linestyle='--', alpha=0.5)

ax = axes[2,0]
datasets = [pr_cpc_sz_p1, pr_cpc_sz_p2, pr_era5_sz_p1, pr_era5_sz_p2]
data_to_plot = []
for m in range(12):
    for ds in datasets:
        month_values = ds[m::12]
        data_to_plot.append(month_values)
positions = []
for k in range(12):
    positions.extend(np.array(range(len(datasets))) + k*(len(datasets)+1))
bplot = ax.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)
for patch, color in zip(bplot['boxes'], colors*12):
    patch.set_facecolor(color)

ax.set_ylim(0, 10)
ax.set_yticks(np.arange(0, 11, 1))
ax.set_xticks([k*(len(datasets)+1) + (len(datasets)-1)/2 for k in range(12)])
ax.set_xticklabels(months)
ax.set_title('e) Sahel zone', loc='left', fontsize=10, fontweight='bold')
ax.set_ylabel('Precipitation (mm/d)')
ax.set_xlabel('Months')
ax.grid(True, linestyle='--', alpha=0.5)

ax = axes[2,1]
datasets = [tmp_cpc_sz_p1, tmp_cpc_sz_p2, tmp_era5_sz_p1, tmp_era5_sz_p2]
data_to_plot = []
for m in range(12):
    for ds in datasets:
        month_values = ds[m::12]
        data_to_plot.append(month_values)
positions = []
for k in range(12):
    positions.extend(np.array(range(len(datasets))) + k*(len(datasets)+1))
bplot = ax.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True)
for patch, color in zip(bplot['boxes'], colors*12):
    patch.set_facecolor(color)

ax.set_ylim(20, 32)
ax.set_yticks(np.arange(20, 36, 1))
ax.set_xticks([k*(len(datasets)+1) + (len(datasets)-1)/2 for k in range(12)])
ax.set_xticklabels(months)
ax.set_title('f) Sahel zone', loc='left', fontsize=10, fontweight='bold')
ax.set_ylabel('Temperature (°C)')
ax.set_xlabel('Months')
ax.grid(True, linestyle='--', alpha=0.5)

for i in range(len(labels)):
    axes[0,0].plot([], c=colors[i], label=labels[i])
axes[0,0].legend(loc='upper left')

# Path out to save figure
path_out = '/home/mda_silv'
name_out = 'pyplt_graph_annual_cycle_1979-2014.png'
plt.savefig(os.path.join(path_out, name_out), dpi=400, bbox_inches='tight')
plt.show()
exit()
