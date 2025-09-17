#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J CMIP6-HighRes
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

# models
mdl="CNRM-CM6-1"
mdl_family="CNRM-CERFACS"
exp="highres-future"
member="r1i1p1f2"
version="v20190314"
type="gr"
declare -a YEARS=("20150101-20241231" "20250101-20341231" "20350101-20441231" "20450101-20501231")

var_list="pr tasmax tasmin"

echo "Starting download"
for var in ${var_list[@]}; do

	base_url="https://data.ceda.ac.uk/badc/cmip6/data/CMIP6/HighResMIP/${mdl_family}/${mdl}/${exp}/${member}/day/${var}/${type}/${version}"
	dir="/home/mda_silv/clima-archive2-b/CMIP6-HighRes/${mdl}"

	for year in "${YEARS[@]}"; do
	
		filename="${var}_day_${mdl}_${exp}_${member}_${type}_${year}.nc"
		
		url="${base_url}/${filename}"
		file_dir="/home/mda_silv/clima-archive2-b/CMIP6/${mdl}/${filename}"

		if [ -f "$file_dir" ]; then
			echo "File exists: ${filename}"
		else
			echo "Downloading: $filename"
			wget -P "$dir" ${url}
		fi
	done
done

echo "Finished downloads."
