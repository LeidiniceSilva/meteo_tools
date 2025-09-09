#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J CMIP6
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

mdl="TaiESM1"

if [ ${mdl} == 'ACCESS-ESM1-5' ]; then # ACCESS-ESM1-5
	mdl_family="CSIRO"
	exp="ssp585"
	member="r1i1p1f1"
	type="gn"
	version="v20210318"
	declare -a YEARS=("20150101-20641231" "20650101-21001231")
elif [ ${mdl} == 'GFDL-ESM4' ]; then
	mdl_family="NOAA-GFDL"
	exp="ssp585"
	member="r1i1p1f1"
	type="gr1"
	version="v20180701"
	declare -a YEARS=("20150101-20341231" "203650101-20741231" "20750101-20941231" "20950101-21001231")
elif [ ${mdl} == 'HadGEM3-GC31-MM' ]; then
	mdl_family="MOHC"
	exp="ssp585"
	member="r1i1p1f3"
	type="gn"
	version="v20200515"
	declare -a YEARS=("20150101-20191230" "20200101-20241230" "20250101-20291230" "20300101-20341230" "20350101-20391230" "20400101-20441230" "20450101-20491230" "20500101-20541230" "20550101-20591230" "20600101-20641230" "20650101-20691230" "20700101-20741230" "20750101-20791230" "20800101-20841230" "20850101-20891230" "20900101-20941230" "20950101-20991230" "21000101-21001230")
elif [ ${mdl} == 'MPI-ESM1-2-LR' ]; then
	mdl_family="MPI-M"
	exp="ssp585"
	member="r1i1p1f1"
	type="gn"
	version="v20190710"
	declare -a YEARS=("20150101-20341231" "203650101-20741231" "20750101-20941231" "20950101-21001231")
elif [ ${mdl} == 'NorESM2-MM' ]; then
	mdl_family="NCC" # NorESM2-LM
	exp="ssp585"
	member="r1i1p1f1"
	type="gn"
	version="v20191108"
	declare -a YEARS=("20150101-20201231" "20210101-20301231" "20310101-20401231" "20410101-20501231" "20510101-20601231" "20610101-20701231" "20710101-20801231" "20810101-20901231" "20910101-21001231")
else
	mdl_family="AS-RCEC"
	exp="ssp585"
	member="r1i1p1f1"
	type="gn"
	version="v20210721"
	declare -a YEARS=("20150101-20241231" "20250101-20341231" "20350101-20441231" "20450101-20541231" "20550101-20641231" "20650101-20741231" "20750101-20841231" "20850101-20941231" "20950101-21001231")
fi

var_list="pr tasmax tasmin"

echo "Starting download"
for var in ${var_list[@]}; do

	base_url="https://data.ceda.ac.uk/badc/cmip6/data/CMIP6/ScenarioMIP/${mdl_family}/${mdl}/${exp}/${member}/day/${var}/${type}/${version}"
	dir="/home/mda_silv/clima-archive2-b/CMIP6/${mdl}"
	
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
