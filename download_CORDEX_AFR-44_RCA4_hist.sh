#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J AFR-44_CORDEX
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

rcm="RCA4"
gcm="ECMWF-ERAINT"
member="r1i1p1"

if [ ${gcm} == 'NCC-NorESM1-M' ]; then
	exp="historical"
	version="v20130927"
	declare -a YEARS=("19660101-19701231" "19710101-19751231" "19760101-19801231" "19810101-19851231" "19860101-19901231" "19910101-19951231" "19960101-20001231" "20010101-20051231")
elif [ ${gcm} == 'MPI-M-MPI-ESM-LR' ]; then
	exp="historical"
	version="v20130927"
	declare -a YEARS=("19660101-19701231" "19710101-19751231" "19760101-19801231" "19810101-19851231" "19860101-19901231" "19910101-19951231" "19960101-20001231" "20010101-20051231")
elif [ ${gcm} == 'MOHC-HadGEM2-ES' ]; then
	version="v20130927"
	exp="historical"
	declare -a YEARS=("19660101-19701230" "19710101-19751230" "19760101-19801230" "19810101-19851230" "19860101-19901230" "19910101-19951230" "19960101-20001230" "20010101-20051230")
else 
	exp="evaluation"
	version="v20130927" # ECMWF-ERAINT
	declare -a YEARS=("19800101-19801231" "19810101-19851231" "19860101-19901231" "19910101-19951231" "19960101-20001231" "20010101-20051231" "20060101-20101231")

fi

var_list="pr tasmax tasmin"

echo "Starting download"
for var in ${var_list[@]}; do

	base_url="https://data.meteo.unican.es/thredds/fileServer/esgf/replica/raw/cordex/output/AFR-44/SMHI/${gcm}/${exp}/${member}/${rcm}/v1/day/${var}/${version}"

	for year in "${YEARS[@]}"; do

		filename="${var}_AFR-44_${gcm}_${exp}_${member}_SMHI-${rcm}_v1_day_${year}.nc"	   
		url=${base_url}/${filename}
		
		dir="/home/mda_silv/clima-archive2-b/CORDEX/AFR-44/${rcm}/${gcm}"

		echo "Downloading: $filename"
		wget -c -P "$dir" ${url}
	done
done

echo "Finished downloads."
