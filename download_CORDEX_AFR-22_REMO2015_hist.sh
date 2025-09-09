#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J AFR-22_CORDEX
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

rcm="REMO2015"
gcm="MOHC-HadGEM2-ES"
member="r1i1p1"

if [ ${gcm} == 'NCC-NorESM1-M' ]; then
	exp="historical"
	version="v20191015"
	declare -a YEARS=("19700101-19701231" "19710101-19751231" "19760101-19801231" \
                  "19810101-19851231" "19860101-19901231" "19910101-19951231" \
                  "19960101-20001231" "20010101-20051231")
elif [ ${gcm} == 'MPI-M-MPI-ESM-LR' ]; then
	exp="historical"
	version="v20191015"
	declare -a YEARS=("19700101-19701231" "19710101-19751231" "19760101-19801231" \
                  "19810101-19851231" "19860101-19901231" "19910101-19951231" \
                  "19960101-20001231" "20010101-20051231")
elif [ ${gcm} == 'MOHC-HadGEM2-ES' ]; then
	version=" v20191015"
	exp="historical"
	declare -a YEARS=("19700101-19701230" "19710101-19751230" "19760101-19801230" \
                  "19810101-19851230" "19860101-19901230" "19910101-19951230" \
                  "19960101-20001230" "20010101-20051230")
else 
	exp="evaluation"
	version="v20191030" # ECMWF-ERAINT
	declare -a YEARS=("19790102-19801231" "19810101-19851231" "19860101-19901231" \
                  "19910101-19951231" "19960101-20001231" "20010101-20051231" \
                  "20060101-20101231" "20110101-20151231" "20160101-20171231")
fi

var_list="pr tasmax tasmin"

echo "Starting download"
for var in ${var_list[@]}; do

	base_url="https://data.meteo.unican.es/thredds/fileServer/esgf/replica/raw/cordex/output/AFR-22/GERICS/${gcm}/${exp}/${member}/${rcm}/v1/day/${var}/${version}"

	for year in "${YEARS[@]}"; do

		filename="${var}_AFR-22_${gcm}_${exp}_${member}_GERICS-${rcm}_v1_day_${year}.nc"	   
		url=${base_url}/${filename}
		
		dir="/home/mda_silv/clima-archive2-b/CORDEX/AFR-22/${rcm}/${gcm}"

		echo "Downloading: $filename"
		wget -c -P "$dir" ${url}
	done
done

echo "Finished downloads."
