#!/usr/bin/env python3

import sys
import os
import numpy as np
import xarray as xr
import regionmask

ar6_all = regionmask.defined_regions.ar6.all

try:
    fn = sys.argv[1]
except:
    print('Need mask filename')
    sys.exit(-1)

try:
   ds = xr.open_dataset(fn, decode_times=False)
except:
   print('Open '+fn+' error.')
   sys.exit(-1)

try:
    mask_3D = ar6_all.mask_3D(ds)
except:
    try:
        ds = ds.rename({'longitude': 'lon', 'latitude': 'lat'})
        mask_3D = ar6_all.mask_3D(ds)
    except:
        print('Error in '+os.path.basename(fn))
        sys.exit(-1)

for reg in ar6_all:
    code = reg.abbrev
    name = reg.name
    r = mask_3D.isel(region=(mask_3D.abbrevs == code)).astype(np.single)
    r.name = 'mask'
    r.to_netcdf(reg.abbrev+'_mask.nc', format='NETCDF3_CLASSIC')

print('Done.')

