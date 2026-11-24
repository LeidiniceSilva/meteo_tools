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
VAR_LIST="pr tasmax tasmin" # pr tasmax tasmin

# Years
START_YEAR=1970
END_YEAR=2024

# Create directories
mkdir -p "${TMP}"
mkdir -p "${OUTPUT}"
mkdir -p "${OUTPUT}/RR1"
mkdir -p "${OUTPUT}/RX1day"
mkdir -p "${OUTPUT}/TXx"
mkdir -p "${OUTPUT}/TN20"

# Merge daily files
for n in {8..9}; do
    GCM=$( sed -n "${n}p" list_GCM_all| cut -f1 )
  
    for VAR in ${VAR_LIST}; do

        FILE=${INPUT}/${VAR}/${VAR}_${GCM}_1970-2024_lm.nc
	
        for YEAR in $(seq ${START_YEAR} ${END_YEAR}); do

            CDO selyear,${YEAR} ${FILE} ${TMP}/${VAR}_day_${GCM}_${YEAR}_lm.nc

 	    if [ ${VAR} == 'pr' ]
            then
	        CDO eca_rr1 ${TMP}/${VAR}_day_${GCM}_${YEAR}_lm.nc ${TMP}/RR1_${GCM}_${YEAR}.nc
	        CDO eca_rx1day ${TMP}/${VAR}_day_${GCM}_${YEAR}_lm.nc ${TMP}/RX1day_${GCM}_${YEAR}.nc
 	    elif [ ${VAR} == 'tasmax' ]
            then
	        CDO -subc,273.15 -yearmax ${TMP}/${VAR}_day_${GCM}_${YEAR}_lm.nc ${TMP}/TXx_${GCM}_${YEAR}.nc
	    else
	        CDO eca_tr,20 ${TMP}/${VAR}_day_${GCM}_${YEAR}_lm.nc ${TMP}/TN20_${GCM}_${YEAR}.nc
	    fi
	    
	done
    done
done

#CDO mergetime ${TMP}/RR1_${GCM}_*.nc ${OUTPUT}/RR1/RR1_${GCM}_${START_YEAR}-${END_YEAR}.nc
#CDO mergetime ${TMP}/RX1day_${GCM}_*.nc ${OUTPUT}/RX1day/RX1day_${GCM}_${START_YEAR}-${END_YEAR}.nc
#CDO mergetime ${TMP}/TXx_${GCM}_*.nc ${OUTPUT}/TXx/TXx_${GCM}_${START_YEAR}-${END_YEAR}.nc
CDO mergetime ${TMP}/TN20_${GCM}_*.nc ${OUTPUT}/TN20/TN20_${GCM}_${START_YEAR}-${END_YEAR}.nc

echo "Done"

}
