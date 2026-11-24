#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J NAM-22
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

set -euo pipefail

CDO(){
    cdo -O -L -f nc4 -z zip "$@"
}

DOMAIN=NAM-22
ENS=r1i1p1
START=1980
END=2024
VAR=tasmax

DEST=/home/mda_silv/scratch/CORDEX-CORE2/CORDEX-CORE/${DOMAIN}
#SRC_hist=/home/clima-archive2-b/rnoghero/CORDEX-CORE/${VAR}/historical
SRC_rcp=/home/clima-archive2-b/rnoghero/CORDEX-CORE/${VAR}/rcp85

# Regional model -> list of driving GCMs
# (REMO2015 is driven by MPI-ESM-LR, RegCM4-7 by MPI-ESM-MR)
declare -A GCMS=([GERICS-REMO2015]="MOHC-HadGEM2-ES MPI-M-MPI-ESM-LR NCC-NorESM1-M")

for RCM in "${!GCMS[@]}"; do
    for GCM in ${GCMS[$RCM]}; do
        base="${VAR}_${DOMAIN}_${GCM}_${ENS}_${RCM}"
        #hist="$SRC_hist/${base}_historical_1980-2005.nc"
        rcp="$SRC_rcp/${base}_1980-2100_rcp85.nc"
        out="$DEST/${base}_${START}-${END}.nc"

        for f in "$rcp"; do
            if [[ ! -f "$f" ]]; then
                echo "ERROR: missing input file $f" >&2
                exit 1
            fi
        done

        echo "Processing ${RCM} / ${GCM}"
        # merge historical + rcp85 and keep only START-END, no intermediate 1980-2100 file
        CDO selyear,${START}/${END} "$rcp" "$out"
    done
done

echo "All done."
