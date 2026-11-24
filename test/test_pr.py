# -*- coding: utf-8 -*-

__author__ = "Leidinice Silva"
__email__ = "leidinicesilva@gmail.com"
__date__ = "March 02, 2026"
__description__ = "This script plot trend heatmap"

import glob
import os
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.colors import BoundaryNorm
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from scipy.stats import linregress

# Indices
idx = "pr"  # pr tas
idx_cru = "pre"  # pre tmp
idx_cpc = "precip"
idx_era5 = "tp"  # tp t2m
idx_era5_land = "tp"  # tp t2m

# Path setup (observations / reanalyses)
cru_dir = f"/home/mda_silv/scratch/CORDEX-CORE2/OBS/CRU/{idx_cru}_ts"
cpc_dir = f"/home/mda_silv/scratch/CORDEX-CORE2/OBS/CPC/{idx_cpc}_ts"
era5_dir = f"/home/mda_silv/scratch/CORDEX-CORE2/OBS/ERA5/{idx_era5}_ts"
era5_land_dir = f"/home/mda_silv/scratch/CORDEX-CORE2/OBS/ERA5-Land/{idx_era5_land}_ts"

# CMIP5 GCMs
cmip5_dir = f"/home/mda_silv/scratch/CORDEX-CORE2/CMIP5/{idx}_ts"
cmip5_m1 = "ICHEC-EC-EARTH_r1"
cmip5_m2 = "MPI-M-MPI-ESM-LR_r1"
cmip5_m3 = "NCC-NorESM1-M_r1"

# CMIP6 GCMs
cmip6_m1_dir = f"/home/mda_silv/scratch/CORDEX-CORE2/CMIP6/EC-Earth3-Veg/{idx}_ts"
cmip6_m2_dir = f"/home/mda_silv/scratch/CORDEX-CORE2/CMIP6/MPI-ESM1-2-HR/{idx}_ts"
cmip6_m3_dir = f"/home/mda_silv/scratch/CORDEX-CORE2/CMIP6/NorESM2-MM/{idx}_ts"

# CORDEX-CORE 1 base directory
cordex_core1_base = "/home/mda_silv/scratch/CORDEX-CORE2/CORDEX-CORE"

# CORDEX-CORE 2 base directory
cordex_core2_base = "/home/clima-archive4-b/nzazulie/trendsCORDEX/CORDEX-CORE2"

# Base model tag prefixes for CORDEX-CORE 1
rcm4_tag_m1 = "MOHC-HadGEM2-ES_r1i1p1_ICTP-RegCM4"
rcm4_tag_m2 = "MPI-M-MPI-ESM-MR_r1i1p1_ICTP-RegCM4"
rcm4_tag_m3 = "NCC-NorESM1-M_r1i1p1_ICTP-RegCM4"
remo_tag_m1 = "NCC-NorESM1-M_r1i1p1_GERICS-REMO2015"
remo_tag_m2 = "MPI-M-MPI-ESM-LR_r1i1p1_GERICS-REMO2015"

# CORDEX-CORE 2 GCM tags for RegCM5
rcm5_gcm1 = "EC-Earth3-Veg"
rcm5_gcm2 = "MPI-ESM1-2-HR"
rcm5_gcm3 = "NorESM2-MM"

# CORDEX-CORE 2 GCM tags for REMO2020-2-2
remo2020_gcm1 = "EC-Earth3-Veg"
remo2020_gcm2 = "MPI-ESM1-2-HR"
remo2020_rcm = "GERICS_REMO2020-2-2"

# CORDEX-CORE 2 GCM tag for WRF451Q
wrf451q_gcm1 = "NorESM2-MM"
wrf451q_rcm = "BCCR-UCAN_WRF451Q"

# Mapping to CORDEX domains
domain_dict = {
    "NAM-22": ["ALA", "ANA", "NWN", "NEN", "CWN", "WSN", "CNA", "CEN", "SEN", "ESN"],
    "CAM-22": ["CAM", "CAR"],
    "SAM-22": ["NWS", "NSA", "SAM", "NES", "SES", "SWS", "SSA"],
    "AFR-22": [
        "NWSH",
        "NCSH",
        "NESH",
        "SWSH",
        "SCSH",
        "SESH",
        "WAF",
        "NCAF",
        "NEAF",
        "SEAF",
        "ARP",
        "SCAF",
        "WSAF",
        "ESAF",
        "MDG",
    ],
    "WAS-22": ["WCA", "SAS"],
    "EAS-22": ["ESB", "RFE", "ECA", "TIB", "EAS"],
    "SEA-22": ["NWSEA", "NESEA", "SSEA"],
    "AUS-22": ["NAU", "CAU", "EAU", "WSAU", "ESAU", "NZE"],
    "EUR-11": ["SMED", "NMED", "NEU", "WCE"],
}

# Domain mapping lookup table from 22/11 km to 12 km (CORDEX-CORE 2)
dom_22_to_12 = {
    "NAM-22": "NAM-12",
    "CAM-22": "CAM-12",
    "SAM-22": "SAM-12",
    "AFR-22": "AFR-12",
    "AUS-22": "AUS-12",
    "EUR-11": "EUR-12",
}

# Domain grouping order & subregion-to-domain lookup map
ordered_subregs = []
subreg_to_domain = {}

for dom, subregs in domain_dict.items():
  for reg in subregs:
    if reg not in ordered_subregs:
      ordered_subregs.append(reg)
      subreg_to_domain[reg] = dom


# Helper function to find file paths using wildcard globbing
def find_rcm_file(folder, search_pattern):
  pattern = os.path.join(folder, search_pattern)
  matches = glob.glob(pattern)
  if matches:
    return matches[0]
  return None


# Helper for observational files: tries the common index name and the
# dataset-specific variable name (e.g. pr_ALA_ts.nc, pre_ALA_ts.nc, tp_ALA_ts.nc)
def resolve_obs_path(folder, var_names, subreg):
  for v in var_names:
    p = os.path.join(folder, f"{v}_{subreg}_ts.nc")
    if os.path.exists(p):
      return p
  return os.path.join(folder, f"{var_names[0]}_{subreg}_ts.nc")


# Function to resolve CORDEX-CORE 1 files ({idx}_{dom}_{tag}*_{subreg}_ts.nc)
def resolve_rcm4_path(base_dir, idx_str, dom_str, tag_prefix, subreg):
  return find_rcm_file(
      base_dir, f"{idx_str}_{dom_str}_{tag_prefix}*_{subreg}_ts.nc"
  )


time_coder = xr.coders.CFDatetimeCoder(use_cftime=True)


def _pick_data_var(ds):
  numeric_vars = [
      name
      for name, var in ds.data_vars.items()
      if np.issubdtype(var.dtype, np.number)
      and "bnds" not in name.lower()
      and "bounds" not in name.lower()
      and name.lower() != "time"
  ]
  if numeric_vars:
    return numeric_vars[0]
  return list(ds.data_vars)[0]


def _annual_days_factor(da):
  """Convert annual mean (mm/day) to annual accumulated total (mm/year)."""
  values = np.asarray(da.values, dtype=float)
  if "time" in da.coords and hasattr(da.time, "dt") and hasattr(da.time.dt, "days_in_year"):
    days = np.asarray(da.time.dt.days_in_year.values, dtype=float)
    # Alinha o eixo do tempo para multiplicar cada ano pelo seu número de dias
    if "time" in da.dims:
      time_axis = da.get_axis_num("time")
      shape = [1] * values.ndim
      shape[time_axis] = len(days)
      return values * days.reshape(shape)
  return values * 365.25


# Function to compute mean of annual accumulated total, linear trend and p-value (sliced 1980-2014)
def get_stats(file_path, start_year=1980, end_year=2014):
  if file_path is None or not os.path.exists(file_path):
    return np.nan, np.nan, np.nan
  try:
    with xr.open_dataset(file_path, decode_times=time_coder) as ds:
      var_name = _pick_data_var(ds)
      da = ds[var_name].squeeze()

      if not np.issubdtype(da.dtype, np.number):
        return np.nan, np.nan, np.nan

      if "time" in da.coords:
        try:
          da = da.sel(time=slice(f"{start_year}-01-01", f"{end_year}-12-31"))
        except Exception:
          years = da.time.dt.year if hasattr(da.time, "dt") else da.time.values
          da = da.isel(time=(years >= start_year) & (years <= end_year))

      # Acumulado anual (mm/ano) a partir da média anual (mm/dia)
      annual_acc = _annual_days_factor(da)
      if annual_acc.size == 0:
        return np.nan, np.nan, np.nan

      # Média do acumulado anual no período
      mean_val = float(np.nanmean(annual_acc))

      # Série temporal do acumulado anual para tendência linear
      if "time" in da.dims:
        time_axis = da.get_axis_num("time")
        other_axes = tuple(i for i in range(annual_acc.ndim) if i != time_axis)
        y = np.nanmean(annual_acc, axis=other_axes) if other_axes else annual_acc.ravel()
      else:
        y = annual_acc.ravel()

      x = np.arange(len(y), dtype=float)
      valid = np.isfinite(y)

      if np.sum(valid) < 2:
        return mean_val, np.nan, np.nan

      slope, _, _, p_val, _ = linregress(x[valid], y[valid])
      return mean_val, float(slope), float(p_val)

  except Exception as e:
    print(f"Error reading {file_path}: {e}")
    return np.nan, np.nan, np.nan


# Column definition (order = order in the heatmap)
# (key, label)
columns = [
    # Observations / reanalyses
    ("cru",       "CRU"),
    ("cpc",       "CPC"),
    ("era5",      "ERA5"),
    ("era5_land", "ERA5-Land"),
    # CMIP5
    ("cmip5_m1",  "EC-Earth"),
    ("cmip5_m2",  "MPI-ESM-MR"),
    ("cmip5_m3",  "NorESM1-M"),
    # CMIP6
    ("cmip6_m1",  "EC-Earth3-Veg"),
    ("cmip6_m2",  "MPI-ESM1-2-HR"),
    ("cmip6_m3",  "NorESM2-MM"),
    # CORDEX-CORE 1
    ("rcm4_m1",   "RegCM4-HadGEM2-ES"),
    ("rcm4_m2",   "RegCM4-MPI"),
    ("rcm4_m3",   "RegCM4-Nor"),
    ("remo_m1",   "REMO2015-Nor"),
    ("remo_m2",   "REMO2015-MPI"),
    # CORDEX-CORE 2
    ("rcm5_m1",     "RegCM5-EC-Earth3"),
    ("rcm5_m2",     "RegCM5-MPI"),
    ("rcm5_m3",     "RegCM5-Nor"),
    ("remo2020_m1", "REMO2020-EC-Earth3"),
    ("remo2020_m2", "REMO2020-MPI"),
    ("wrf451q_m1",  "WRF451Q-Nor"),
]
col_keys = [k for k, _ in columns]
cols = [l for _, l in columns]
n_cols = len(columns)

# Data extraction containers: stats[key] = {"mean": [], "trend": [], "pval": []}
stats = {k: {"mean": [], "trend": [], "pval": []} for k in col_keys}


def store(key, result):
  m, t, p = result
  stats[key]["mean"].append(m)
  stats[key]["trend"].append(t)
  stats[key]["pval"].append(p)


nan3 = (np.nan, np.nan, np.nan)

for reg in ordered_subregs:
  dom = subreg_to_domain[reg]

  # OBS: CRU, CPC, ERA5, ERA5-Land
  store("cru", get_stats(resolve_obs_path(cru_dir, [idx_cru], reg)))
  store("cpc", get_stats(resolve_obs_path(cpc_dir, [idx_cpc], reg)))
  store("era5", get_stats(resolve_obs_path(era5_dir, [idx_era5], reg)))
  store("era5_land", get_stats(resolve_obs_path(era5_land_dir, [idx_era5_land], reg)))

  # CMIP5
  store("cmip5_m1", get_stats(os.path.join(cmip5_dir, f"{idx}_{cmip5_m1}_{reg}_ts.nc")))
  store("cmip5_m2", get_stats(os.path.join(cmip5_dir, f"{idx}_{cmip5_m2}_{reg}_ts.nc")))
  store("cmip5_m3", get_stats(os.path.join(cmip5_dir, f"{idx}_{cmip5_m3}_{reg}_ts.nc")))

  # CMIP6
  store("cmip6_m1", get_stats(os.path.join(cmip6_m1_dir, f"{idx}_{reg}_ts.nc")))
  store("cmip6_m2", get_stats(os.path.join(cmip6_m2_dir, f"{idx}_{reg}_ts.nc")))
  store("cmip6_m3", get_stats(os.path.join(cmip6_m3_dir, f"{idx}_{reg}_ts.nc")))

  # CORDEX-CORE 1 (RegCM4 & REMO2015)
  core1_dir = os.path.join(cordex_core1_base, dom, f"{idx}_ts")
  print(core1_dir)

  store("rcm4_m1", get_stats(resolve_rcm4_path(core1_dir, idx, dom, rcm4_tag_m1, reg)))
  store("rcm4_m2", get_stats(resolve_rcm4_path(core1_dir, idx, dom, rcm4_tag_m2, reg)))
  store("rcm4_m3", get_stats(resolve_rcm4_path(core1_dir, idx, dom, rcm4_tag_m3, reg)))

  store("remo_m1", get_stats(find_rcm_file(core1_dir, f"{idx}_{dom}_{remo_tag_m1}*_{reg}_ts.nc")))
  store("remo_m2", get_stats(find_rcm_file(core1_dir, f"{idx}_{dom}_{remo_tag_m2}*_{reg}_ts.nc")))

  # CORDEX-CORE 2 (RegCM5, REMO2020-2-2, WRF451Q — all at 12km)
  dom12 = dom_22_to_12.get(dom, None)
  if dom12:
    core2_dir = os.path.join(cordex_core2_base, dom12, f"{idx}_ts_AR7")

    # RegCM5
    store("rcm5_m1", get_stats(find_rcm_file(core2_dir, f"{idx}_{dom12}_{rcm5_gcm1}_*_{reg}_ts.nc")))
    store("rcm5_m2", get_stats(find_rcm_file(core2_dir, f"{idx}_{dom12}_{rcm5_gcm2}_*_{reg}_ts.nc")))
    store("rcm5_m3", get_stats(find_rcm_file(core2_dir, f"{idx}_{dom12}_{rcm5_gcm3}_*_{reg}_ts.nc")))

    # REMO2020-2-2 (exact filename first, wildcard fallback)
    for key, gcm in (("remo2020_m1", remo2020_gcm1), ("remo2020_m2", remo2020_gcm2)):
      p = find_rcm_file(
          core2_dir,
          f"{idx}_{dom12}_{gcm}_r1i1p1f1_{remo2020_rcm}_1970-2100_{reg}_ts.nc",
      )
      if p is None:
        p = find_rcm_file(
            core2_dir, f"{idx}_{dom12}_{gcm}_*_{remo2020_rcm}_*_{reg}_ts.nc"
        )
      store(key, get_stats(p))

    # WRF451Q (NorESM2-MM)
    p = find_rcm_file(
        core2_dir,
        f"{idx}_{dom12}_{wrf451q_gcm1}_r1i1p1f1_{wrf451q_rcm}_1970-2100_{reg}_ts.nc",
    )
    if p is None:
      p = find_rcm_file(
          core2_dir, f"{idx}_{dom12}_{wrf451q_gcm1}_*_{wrf451q_rcm}_*_{reg}_ts.nc"
      )
    store("wrf451q_m1", get_stats(p))

  else:
    for key in (
        "rcm5_m1",
        "rcm5_m2",
        "rcm5_m3",
        "remo2020_m1",
        "remo2020_m2",
        "wrf451q_m1",
    ):
      store(key, nan3)

# Combine matrices
means_matrix = np.column_stack([stats[k]["mean"] for k in col_keys])
trends_matrix = np.column_stack([stats[k]["trend"] for k in col_keys])
pvals_matrix = np.column_stack([stats[k]["pval"] for k in col_keys])

n_domains = len(ordered_subregs)

# Column positions that divide the families
# (OBS: 4 | CMIP5: 3 | CMIP6: 3 | CORDEX-CORE1: 5 | CORDEX-CORE2: 6)
family_divs = [4, 7, 10, 15]

# Significance level
alpha = 0.05

# Discrete levels for Mean (mm/yr) and Trend (mm/yr per yr)
levels_mean = np.linspace(0, 3000, 21)
levels_trend = np.linspace(-15, 15, 21)

if idx == "pr":
  cmap_mean = plt.colormaps["Blues"].resampled(len(levels_mean) - 1)
  cmap_trend = plt.colormaps["BrBG"].resampled(len(levels_trend) - 1)
else:
  cmap_mean = plt.colormaps["Reds"].resampled(len(levels_mean) - 1)
  cmap_trend = plt.colormaps["bwr"].resampled(len(levels_trend) - 1)

norm_mean = BoundaryNorm(levels_mean, ncolors=cmap_mean.N, clip=True)
norm_trend = BoundaryNorm(levels_trend, ncolors=cmap_trend.N, clip=True)

# Plot heatmap
fig, ax = plt.subplots(figsize=(21, 14))
ax.set_facecolor("white")
pad = 0.08

for row in range(n_domains):
  for col in range(n_cols):
    m_val = means_matrix[row, col]
    t_val = trends_matrix[row, col]
    p_val = pvals_matrix[row, col]

    x_min, x_max = col + pad, col + 1 - pad
    y_min, y_max = row + pad, row + 1 - pad

    # Mean triangle (upper-left split)
    if not np.isnan(m_val):
      p1 = Path([(x_min, y_min), (x_max, y_min), (x_min, y_max), (x_min, y_min)])
      patch1 = PathPatch(p1, facecolor=cmap_mean(norm_mean(m_val)), edgecolor="none")
      ax.add_patch(patch1)

    # Trend triangle (lower-right split)
    if not np.isnan(t_val):
      p2 = Path([(x_max, y_min), (x_max, y_max), (x_min, y_max), (x_max, y_min)])
      patch2 = PathPatch(p2, facecolor=cmap_trend(norm_trend(t_val)), edgecolor="none")
      ax.add_patch(patch2)

      # Dot for significant trend (p < 0.05) at the centroid of the trend triangle
      if not np.isnan(p_val) and p_val < alpha:
        x_dot = (2 * x_max + x_min) / 3
        y_dot = (y_min + 2 * y_max) / 3
        ax.plot(
            x_dot,
            y_dot,
            marker="o",
            color="black",
            markersize=3,
            linestyle="none",
            zorder=3,
        )

# Black lines dividing the families
for x_div in family_divs:
  ax.axvline(x_div, color="black", linewidth=1.5, zorder=4)

# Configure axes
ax.set_aspect("equal")
ax.set_xlim(0, n_cols)
ax.set_ylim(0, n_domains)
ax.set_xticks(np.arange(n_cols) + 0.5)
ax.set_xticklabels(cols, fontsize=10, rotation=30, ha="right")
ax.set_yticks(np.arange(n_domains) + 0.5)
ax.set_yticklabels(ordered_subregs, fontsize=10)
ax.invert_yaxis()

for spine in ax.spines.values():
  spine.set_visible(False)

# Colorbars setup
sm_mean = plt.cm.ScalarMappable(cmap=cmap_mean, norm=norm_mean)
sm_trend = plt.cm.ScalarMappable(cmap=cmap_trend, norm=norm_trend)

cax_mean = inset_axes(
    ax,
    width="4%",
    height="42%",
    loc="upper right",
    bbox_to_anchor=(0.22, 0.0, 1.0, 1.0),
    bbox_transform=ax.transAxes,
)
cbar_mean = plt.colorbar(
    sm_mean, cax=cax_mean, orientation="vertical", ticks=levels_mean
)
cbar_mean.set_label("Mean (mm/yr)", fontsize=10)

cax_trend = inset_axes(
    ax,
    width="4%",
    height="42%",
    loc="lower right",
    bbox_to_anchor=(0.22, 0.0, 1.0, 1.0),
    bbox_transform=ax.transAxes,
)
cbar_trend = plt.colorbar(
    sm_trend, cax=cax_trend, orientation="vertical", ticks=levels_trend
)
cbar_trend.set_label("Trend (mm/yr/yr)", fontsize=10)

# Save figure
out_dir = "/home/mda_silv/scratch/CORDEX-CORE2/figs"
os.makedirs(out_dir, exist_ok=True)
plt.savefig(
    f"{out_dir}/{idx}_CORDEX-CORE2_heatmap_AR7.png",
    dpi=400,
    bbox_inches="tight",
)
plt.show()
