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
DATASET="ERA5-Land" 

# Input files
INPUT="/home/netapp-clima-scratch/mda_silv/CORDEX-CORE2/OBS/${DATASET}"

# Variables
VAR_LIST="tp t2m" # tp t2m mx2t mn2t precip tmax tmin

# Years
START_YEAR=1970
END_YEAR=2024

# Merge daily files
for VAR in ${VAR_LIST}; do

    #FILE=${INPUT}/${VAR}_${DATASET}_mon_1901-2024.nc
    #FILE=${INPUT}/${VAR}.${DATASET}.day.1979-2024.nc
    #FILE=${INPUT}/${VAR}_${DATASET}_mon_1970-2024.nc
    FILE=${INPUT}/${VAR}_${DATASET}_mon_1970-2024_lm.nc

    if [ ${VAR} == 'tp' ] # tp ot precip
    then
    CDO -mulc,1000 -yearmean ${FILE} ${INPUT}/${VAR}/${VAR}_${DATASET}_${START_YEAR}-${END_YEAR}.nc
    else
    CDO -subc,273.15 -yearmean ${FILE} ${INPUT}/${VAR}/${VAR}_${DATASET}_${START_YEAR}-${END_YEAR}.nc
    fi

done

echo "Done"

}
