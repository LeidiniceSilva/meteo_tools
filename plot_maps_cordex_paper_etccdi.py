# -*- coding: utf-8 -*-

__author__      = "Leidinice Silva"
__email__       = "leidinicesilva@gmail.com"
__date__        = "May 14, 2025"
__description__ = "This script plot CORDEX projection"

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.mpl.ticker as cticker
from pathlib import Path

base = "/afs/ictp.it/home/m/mda_silv/Downloads/cordex"

# function 
def read_var(folder, varname):
    ds = xr.open_dataset(Path(base) / folder / "map.nc")
    return ds["lon"], ds["lat"], ds[varname]

# load vars
lon_c, lat_c, cdd_cam = read_var("CDD_CAM", "ds_anom")
lon_s, lat_s, cdd_sam = read_var("CDD_SAM", "ds_anom")

lon_tc, lat_tc, txx_cam = read_var("TXx_CAM", "TXx_anom")
lon_ts, lat_ts, txx_sam = read_var("TXx_SAM", "TXx_anom")

# load consensus
_, _, cdd_cam_cons = read_var("CDD_CAM", "ds_anom_consensus")
_, _, cdd_sam_cons = read_var("CDD_SAM", "ds_anom_consensus")

_, _, txx_cam_cons = read_var("TXx_CAM", "TXx_anom_consensus")
_, _, txx_sam_cons = read_var("TXx_SAM", "TXx_anom_consensus")

# figure
fig, axes = plt.subplots(1, 2, figsize=(10, 5), subplot_kw={"projection": ccrs.PlateCarree()})

fig.suptitle("Long Term (2081-2100) RCP8.5 (rel. to 1986-2005) - Annual (21 models)")

def add_grid(ax):
    gl = ax.gridlines(draw_labels=True, linewidth=0.75, color="gray", alpha=0.5, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 8}
    gl.ylabel_style = {"size": 8}

# TXx
mask_cc = cdd_cam_cons != 1
mask_cs = cdd_sam_cons != 1

pcm1 = axes[0].pcolormesh(lon_tc, lat_tc, txx_cam, transform=ccrs.PlateCarree(), cmap="Reds")
axes[1].scatter(lon_c[mask_cc], lat_c[mask_cc], transform=ccrs.PlateCarree(), s=1, c="black", alpha=0.6)
axes[0].pcolormesh(lon_ts, lat_ts, txx_sam, transform=ccrs.PlateCarree(), cmap="Reds")
axes[1].scatter(lon_s[mask_cs], lat_s[mask_cs], transform=ccrs.PlateCarree(), s=1, c="black", alpha=0.6)
     
axes[0].coastlines()
add_grid(axes[0])
axes[0].set_title("(a) TXx Change deg C (CAM + SAM)")
cbar1 = fig.colorbar(pcm1, ax=axes[0], orientation="horizontal", pad=0.05, shrink=0.8)
cbar1.set_label("deg C")

# CDD
pcm2 = axes[1].pcolormesh(lon_c, lat_c, cdd_cam, transform=ccrs.PlateCarree(), cmap="BrBG")
axes[1].pcolormesh(lon_s, lat_s, cdd_sam, transform=ccrs.PlateCarree(), cmap="BrBG")
axes[1].coastlines()
add_grid(axes[1])
axes[1].set_title("(b) CDD Change days (CAM + SAM)")
cbar2 = fig.colorbar(pcm2, ax=axes[1], orientation="horizontal", pad=0.05, shrink=0.8)
cbar2.set_label("days")

# save
plt.savefig("TXx_CDD_CAM-SAM_CORDEX_domains.png", dpi=400, bbox_inches="tight")
plt.show()


