#!/bin/bash

#SBATCH -J CORDEX-CORE2
#SBATCH -t 24:00:00
#SBATCH -p esp
#SBATCH -N 1 --ntasks-per-node=20

#__author__      = 'Leidinice Silva'
#__email__       = 'leidinicesilva@gmail.com'
#__date__        = 'Nov 20, 2023'
#__description__ = 'Compute ETCCDI indices using CDO-ECA'

{
set -eo pipefail

CDO(){
    cdo -O -L -f nc4 -z zip "$@"
}

#Dataset
DATASET="CPC" 

# Input files
INPUT="/home/mda_silv/scratch/CORDEX-CORE2/OBS/${DATASET}"

# Output
OUTPUT="/home/mda_silv/clima-archive2-b/ETCCDI/OBS/${DATASET}"

# Variables
VAR_LIST="precip tmax tmin" # tp mx2t mn2t precip tmax tmin

# Years
START_YEAR=1979
END_YEAR=2024

# Merge daily files
for VAR in ${VAR_LIST}; do

    FILE=${INPUT}/${VAR}.cpc.day.1979-2024.nc
    #FILE=${INPUT}/${VAR}_ERA5_day_1970-2024_lm.nc

    for YEAR in $(seq ${START_YEAR} ${END_YEAR}); do

        CDO -ymonmean -selyear,1979/1981 ${FILE} ${OUTPUT}/${VAR}_${DATASET}_ac_1979-2014.nc
	
    done
done

echo "Done"

}
