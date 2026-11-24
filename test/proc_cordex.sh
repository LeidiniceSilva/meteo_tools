#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J CORDEX-CORE2
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

CDO(){
    cdo -O -L -f nc4 -z zip "$@"
}

SRC=/home/clima-archive2-b/rnoghero/CORDEX-CORE/pr/rcp85
DEST=/home/mda_silv/scratch/CORDEX-CORE2/CORDEX-CORE

mkdir -p "$DEST"

# create one folder per domain
for dom in AFR-22 AUS-22 CAM-22 EUR-22 EAS-22 NAM-22 SAM-22 SEA-22 WAS-22; do
    mkdir -p "$DEST/$dom"
done

# only ICTP-RegCM4-7 and GERICS-REMO2015
for f in "$SRC"/pr_*-22_*_*ICTP-RegCM4-7*_1980-2100.nc "$SRC"/pr_*-22_*_*GERICS-REMO2015*_1980-2100.nc; do
    [ -f "$f" ] || continue
    base=$(basename "$f")
    dom=$(echo "$base" | cut -d_ -f2)       # e.g. AFR-22
    out="${base/1980-2100/1980-2024}"       # rename to reflect the new period
    cdo selyear,1970/2024 "$f" "$DEST/$dom/$out"
done
