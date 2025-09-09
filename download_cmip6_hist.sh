#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J CMIP6
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

mdl="TaiESM1"

if [ ${mdl} == 'ACCESS-ESM1-5' ]; then
	mdl_family="CSIRO"
	exp="historical"
	member="r1i1p1f1"
	type="gn"
	version="v20191115"
	declare -a YEARS=("18500101-18991231" "19000101-19491231" "19500101-19991231" "20000101-20141231")
elif [ ${mdl} == 'CMCC-ESM2' ]; then
	mdl_family="CMCC"
	exp="historical"
	member="r1i1p1f1"
	type="gn"
	version="v20210114"
	declare -a YEARS=("18500101-18741231" "18750101-18991231" "19000101-19241231" "19250101-19491231" "19500101-19741231" "19750101-19991231" "20000101-20141231")
elif [ ${mdl} == 'FGOALS-g3' ]; then
	mdl_family="CAS"
	exp="historical"
	member="r1i1p1f1"
	type="gn"
	version="v20190826"
	declare -a YEARS=($(seq 1970 2014))
elif [ ${mdl} == 'HadGEM3-GC31-MM ' ]; then
	mdl_family="MOHC"
	exp="historical"
	member="r1i1p1f3"
	type="gn"
	version="v20191207"
	declare -a YEARS=("19500101-19541230" "19550101-19591230" "19600101-19641230" "19650101-19691230" "19700101-19741230" "19750101-19791230" "19800101-19841230" "19850101-19871230" "19880101-19891230" "19900101-19941230" "19950101-19991230" "20000101-20041230" "20050101-20091230" "20100101-20141230")
elif [ ${mdl} == 'NorESM2-LM' ]; then # NorESM2-MM
	mdl_family="NCC"
	exp="historical"
	member="r1i1p1f1"
	type="gn"
	version="v20190815" # v20191108
	declare -a YEARS=("19500101-19591231" "19600101-19691231" "19700101-19791231" "19800101-19891231" "19900101-19991231" "19900101-19991231" "20000101-20091231" "20100101-20141231")
else
	mdl_family="AS-RCEC"
	exp="historical"
	member="r1i1p1f1"
	type="gn"
	version="v20210517"
	declare -a YEARS=("19500101-19591231" "19600101-19691231" "19700101-19791231" "19800101-19891231" "19900101-19991231" "19900101-19991231" "20000101-20091231" "20100101-20141231")
fi

var_list="pr tasmax tasmin"

echo "Starting download"
for var in ${var_list[@]}; do

	base_url="https://data.ceda.ac.uk/badc/cmip6/data/CMIP6/CMIP/${mdl_family}/${mdl}/${exp}/${member}/day/${var}/${type}/${version}"
	dir="/home/mda_silv/clima-archive2-b/CMIP6/${mdl}"

	for year in "${YEARS[@]}"; do

		if [ ${mdl} == 'FGOALS-g3' ]; then
			filename="${var}_day_${mdl}_${exp}_${member}_${type}_${year}0101-${year}1231.nc"
		else
			filename="${var}_day_${mdl}_${exp}_${member}_${type}_${year}.nc"
		fi
		
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
