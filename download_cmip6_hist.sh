#!/bin/bash

model_list=( 'EC-Earth3-Veg' ) # EC-Earth3-Veg MPI-ESM1-2-HR NorESM2-MM

var_list=( 'tas' ) # pr tas tasmax tasmin    
exp='historical'

echo "Starting download"
for mdl in ${model_list[@]}; do
    for var in ${var_list[@]}; do

        if [ ${mdl} == 'EC-Earth3-Veg' ]; then
	    mdl_family='EC-Earth-Consortium'
	    type='gr'
	    member='r5i1p1f1'
	    version='v20200312'	   
            declare -a YEARS=($(seq 1970 2014)) 

	elif [ ${mdl} == 'MPI-ESM1-2-HR' ]; then
	     mdl_family='MPI-M'
	     type='gn'
	     member='r1i1p1f1'
             version='v20190710'
             declare -a YEARS=( '18500101-18541231' '18550101-18591231'  '18600101-18641231' '18650101-18691231' '18700101-18741231' '18750101-18791231' '18800101-18841231' '18850101-18891231' '18900101-18941231' '18950101-18991231' '19000101-19041231' '19050101-19091231' '19100101-19141231' '19150101-19191231' '19200101-19241231' '19250101-19291231' '19300101-19341231' '19350101-19391231' '19400101-19441231' '19450101-19491231' '19500101-19541231' '19550101-19591231' '19600101-19641231' '19650101-19691231' '19700101-19741231' '19750101-19791231' '19800101-19841231' '19850101-19891231' '19900101-19941231' '19950101-19991231' '20000101-20041231' '20050101-20091231' '20100101-20141231' )
  
	else
	     mdl_family='NCC'
	     type='gn'
	     member='r1i1p1f1'
	     version='v20191108'
             declare -a YEARS=( '19700101-19791231' '19800101-19891231' '19900101-19991231' '20000101-20091231' '20100101-20141231' )
	fi
	
	base_url="https://dap.ceda.ac.uk/badc/cmip6/data/CMIP6/CMIP/${mdl_family}/${mdl}/${exp}/${member}/3hr/${var}/${type}/${version}"
	dir="/home/mda_silv/scratch/CORDEX-CORE2/CMIP6/${mdl}/${var}"

	for year in "${YEARS[@]}"; do

            if [ ${mdl} == 'EC-Earth3-Veg' ]; then
	    filename="${var}_3hr_${mdl}_${exp}_${member}_${type}_${year}01010000-${year}12312100.nc"
	    else
	    filename="${var}_day_${mdl}_${exp}_${member}_${type}_${year}.nc"
	    fi
	    
	    url="${base_url}/${filename}"
	    wget -P "$dir" ${url}
	    
	done
    done
done

echo "Finished downloads."
