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
exp="hist-1950"
member="r1i1p1f2"
version="v20190401"
type="gr"
var_list="pr tasmax tasmin"

echo "Starting download"

for var in ${var_list[@]}; do

	base_url="https://data.ceda.ac.uk/badc/cmip6/data/CMIP6/HighResMIP/${mdl_family}/${mdl}/${exp}/${member}/day/${var}/${type}/${version}"

	filename1="${var}_day_${mdl}_${exp}_${member}_${type}_19700101-19791231.nc"	
	filename2="${var}_day_${mdl}_${exp}_${member}_${type}_19800101-19891231.nc"	
	filename3="${var}_day_${mdl}_${exp}_${member}_${type}_19900101-19991231.nc"	
	filename4="${var}_day_${mdl}_${exp}_${member}_${type}_20000101-20091231.nc"	
	filename5="${var}_day_${mdl}_${exp}_${member}_${type}_20100101-20141231.nc"	

	url1="${base_url}/${filename1}"
	url2="${base_url}/${filename2}"
	url3="${base_url}/${filename3}"
	url4="${base_url}/${filename4}"
	url5="${base_url}/${filename5}"

	echo "Downloading: $filename"
	wget ${url1} 
	wget ${url2} 
	wget ${url3} 
	wget ${url4} 
	wget ${url5} 

	if [ $? -ne 0 ]; then
		echo "Failed to download: $filename1"
	fi
done

echo "Finished downloads."

