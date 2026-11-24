#!/bin/bash

#SBATCH -A ICT26_ESP
#SBATCH -p dcgp_usr_prod
#SBATCH -N 1
#SBATCH --ntasks-per-node=112
#SBATCH -t 1-00:00:00
#SBATCH -J ETCCDI
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

#__author__      = 'Leidinice Silva'
#__email__       = 'leidinicesilva@gmail.com'
#__date__        = 'Nov 20, 2023'
#__description__ = 'Compute ETCCDI indices using CDO-ECA'

{
set -eo pipefail

CDO(){
    cdo -O -L -f nc4 -z zip "$@"
}

# Input files
INPUT="/home/mda_silv/scratch/CORDEX-CORE2/CMIP5/input"

# Output
OUTPUT="/home/mda_silv/scratch/CORDEX-CORE2/CMIP5"
TMP="${OUTPUT}/tmp"

# Variables
VAR_LIST="pr tas" # pr tasmax tasmin

# Years
START_YEAR=1970
END_YEAR=2024

# Merge daily files
for n in {1..20}; do
    GCM=$( sed -n "${n}p" list_GCM_all| cut -f1 )
  
    for VAR in ${VAR_LIST}; do

        FILE=${INPUT}/${VAR}/${VAR}_${GCM}_1970-2024_lm.nc

 	if [ ${VAR} == 'pr' ]
        then
	    CDO yearmean ${FILE} ${OUTPUT}/${VAR}/pr_${GCM}_${START_YEAR}-${END_YEAR}.nc
	else
	    CDO -subc,273.15 -yearmean ${FILE} ${OUTPUT}/${VAR}/tas_${GCM}_${START_YEAR}-${END_YEAR}.nc
	fi
	    
    done
done

echo "Done"

}
