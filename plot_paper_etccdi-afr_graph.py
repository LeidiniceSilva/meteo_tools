# -*- coding: utf-8 -*-

__author__ = "Leidinice Silva"
__email__ = "leidinicesilva@gmail.com"
__date__ = "November 14, 2026"
__description__ = "This script plots annual cycles of precipitation, Tmax and Tmin"

import os
import numpy as np
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter


# ============================================================
# PATHS
# ============================================================

base_dir = "/home/mda_silv/clima-archive2-b/ETCCDI/OBS/CPC"

data_dirs = {
    "precip": os.path.join(base_dir, "precip_ts"),
    "tmax":   os.path.join(base_dir, "tmax_ts"),
    "tmin":   os.path.join(base_dir, "tmin_ts"),
}

shapefile_path = (
    "/home/clima-archive4-b/nzazulie/trendsCORDEX/"
    "IPCC-WGI-land-reference-regions-v5.shp"
)

path_out = "/home/mda_silv/clima-archive2-b/ETCCDI/figs"
os.makedirs(path_out, exist_ok=True)


# ============================================================
# REGIONS
# ============================================================

region_codes = [
    "ESAF", "MDG",  "NCAF", "NCSH", "NEAF",
    "NESH", "NWSH", "SCAF", "SCSH", "SEAF",
    "SESH", "SMED", "SWSH", "WAF",  "WSAF",
]


# ============================================================
# VARIABLES
# ============================================================

variables = {
    "precip": {
        "filename":  "precip",
        "title":     "(a)",
        "color":     "darkblue",
        "fillcolor": "steelblue",
        "ylabel":    "Precipitation (mm/day)",
        "kelvin":    False,
        "ylim":      (0, 8),
    },
    "tmax": {
        "filename":  "tmax",
        "title":     "(b)",
        "color":     "red",
        "fillcolor": "salmon",
        "ylabel":    "Tmax (°C)",
        "kelvin":    True,
        "ylim":      (5, 40),
    },
    "tmin": {
        "filename":  "tmin",
        "title":     "(c)",
        "color":     "orange",
        "fillcolor": "moccasin",
        "ylabel":    "Tmin (°C)",
        "kelvin":    True,
        "ylim":      (5, 40),
    },
}


# ============================================================
# READ SHAPEFILE
# ============================================================

gdf = gpd.read_file(shapefile_path)
if gdf.crs is not None:
    gdf = gdf.to_crs(epsg=4326)

africa = gdf[
    (gdf["CONTINENT"] == "AFRICA") &
    (gdf["ACRONYM"].isin(region_codes))
].copy()

missing = set(region_codes) - set(africa["ACRONYM"])
if missing:
    print("Missing regions in shapefile:", missing)


# ============================================================
# READ ANNUAL CYCLE
# ============================================================

def read_annual_cycle(variable, region):

    directory      = data_dirs[variable]
    prefix         = variables[variable]["filename"]
    convert_kelvin = variables[variable]["kelvin"]

    filename = os.path.join(directory, f"{prefix}_{region}_ts.nc")

    if not os.path.exists(filename):
        print(f"Missing file: {filename}")
        return None

    with xr.open_dataset(filename) as ds:

        print(f"\nReading {variable}: {region}")

        possible_vars = [
            v for v in ds.data_vars
            if v.lower() not in ["time_bnds", "time_bounds"]
        ]
        if not possible_vars:
            print(f"No data variable found: {filename}")
            return None

        da = ds[possible_vars[0]]

        time_dim = next(
            (d for d in da.dims if "time" in d.lower()), None
        )
        if time_dim is None:
            print(f"No time dimension found: {filename}")
            return None

        spatial_dims = [d for d in da.dims if d != time_dim]
        if spatial_dims:
            da = da.mean(dim=spatial_dims, skipna=True)

        monthly = (
            da.groupby(f"{time_dim}.month")
              .mean(dim=time_dim, skipna=True)
              .reindex(month=np.arange(1, 13))
        )

        values = monthly.values

        if convert_kelvin:
            values = values - 273.15

        return values


# ============================================================
# LOAD DATA
# ============================================================

data = {v: {} for v in variables}

for variable in variables:
    for region in region_codes:
        values = read_annual_cycle(variable, region)
        if values is not None and len(values) == 12:
            data[variable][region] = values


# ============================================================
# CREATE FIGURE  —  1 row × 3 columns
# ============================================================

fig, axes = plt.subplots(
    nrows=1,
    ncols=3,
    figsize=(24, 10),
    subplot_kw={"projection": ccrs.PlateCarree()},
)

lon1, lon2 = -25, 60
lat1, lat2 = -40, 40
months     = np.arange(1, 13)

# Inset size as fraction of each axes box
INSET_W = 0.085
INSET_H = 0.110


# ============================================================
# DRAW BASE MAPS
# ============================================================

for panel, (variable, config) in enumerate(variables.items()):

    ax = axes[panel]

    ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())

    ax.add_feature(cfeature.OCEAN,     facecolor="white", zorder=0)
    ax.add_feature(cfeature.LAND,      facecolor="0.95",  zorder=0)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.7,     zorder=1)
    ax.add_feature(cfeature.BORDERS,   linestyle=":", linewidth=0.5)

    ax.add_geometries(
        africa.geometry,
        crs=ccrs.PlateCarree(),
        facecolor="none",
        edgecolor="black",
        linewidth=1.0,
        zorder=2,
    )

    # ── Ticks and coordinate labels restored ──
    ax.set_xticks(
        np.arange(lon1, lon2 + 1, 10),
        crs=ccrs.PlateCarree()
    )
    ax.set_yticks(
        np.arange(lat1, lat2 + 1, 10),
        crs=ccrs.PlateCarree()
    )
    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())

    ax.tick_params(labelsize=8)

    ax.grid(color="gray", linestyle="--", linewidth=0.4, alpha=0.4)

    ax.set_title(
        config["title"],
        fontsize=13,
        fontweight="bold",
        loc="left",
        pad=10,
    )


# ============================================================
# FORCE LAYOUT SO TRANSFORMS ARE ACCURATE
# ============================================================

plt.subplots_adjust(
    left=0.04, right=0.98,
    top=0.95,  bottom=0.05,
    wspace=0.10,
)

fig.draw_without_rendering()


# ============================================================
# COMPUTE CENTROID POSITIONS ONCE (shared by all panels)
# ============================================================

ax0     = axes[0]
ax0_pos = ax0.get_position()

centroid_fig_fracs = {}

for _, row in africa.iterrows():

    code     = row["ACRONYM"]
    centroid = row.geometry.centroid

    xy_disp = ax0.transData.transform((centroid.x, centroid.y))
    xy_axes = ax0.transAxes.inverted().transform(xy_disp)

    x_fig = ax0_pos.x0 + xy_axes[0] * ax0_pos.width
    y_fig = ax0_pos.y0 + xy_axes[1] * ax0_pos.height

    centroid_fig_fracs[code] = (x_fig, y_fig)


# ============================================================
# ADD INSET ANNUAL CYCLES
# ============================================================

for panel, (variable, config) in enumerate(variables.items()):

    ax     = axes[panel]
    ax_pos = ax.get_position()

    inset_w = INSET_W * ax_pos.width
    inset_h = INSET_H * ax_pos.height

    dx = ax_pos.x0 - ax0_pos.x0

    for _, row in africa.iterrows():

        code = row["ACRONYM"]

        if code not in data[variable] or code not in centroid_fig_fracs:
            continue

        x_fig0, y_fig = centroid_fig_fracs[code]
        x_fig  = x_fig0 + dx

        left   = x_fig - inset_w / 2
        bottom = y_fig - inset_h / 2

        left   = np.clip(left,   ax_pos.x0, ax_pos.x1 - inset_w)
        bottom = np.clip(bottom, ax_pos.y0, ax_pos.y1 - inset_h)

        inset = fig.add_axes(
            [left, bottom, inset_w, inset_h],
            zorder=5,
        )

        values = data[variable][code]

        inset.plot(
            months, values,
            color=config["color"],
            linewidth=1.5,
            marker="o",
            markersize=2.5,
        )

        inset.fill_between(
            months, values,
            color=config["fillcolor"],
            alpha=0.20,
        )

        inset.set_xlim(1, 12)
        inset.set_xticks([1, 4, 7, 10])
        inset.set_xticklabels(["J", "A", "J", "O"], fontsize=5)

        inset.set_ylim(config["ylim"])

        inset.tick_params(axis="y", labelsize=5, pad=1, length=2)
        inset.tick_params(axis="x", labelsize=5, pad=1, length=2)

        inset.set_title(code, fontsize=7, fontweight="bold", pad=2)

        inset.grid(linestyle=":", linewidth=0.4, alpha=0.5)
        inset.set_facecolor("white")

        for spine in inset.spines.values():
            spine.set_linewidth(0.6)
            spine.set_edgecolor("black")


# ============================================================
# SAVE FIGURE
# ============================================================

output_file = os.path.join(
    path_out,
    "pyplt_maps_annual_cycles_precip_tmax_tmin_Africa.png",
)

plt.savefig(output_file, dpi=400, bbox_inches="tight")
plt.show()

print("\nFigure saved:", output_file)
