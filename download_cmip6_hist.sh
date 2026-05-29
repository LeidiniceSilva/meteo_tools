#!/bin/bash

model_list=( 'AWI-CM-1-1-MR' 'CESM2-WACCM' 'EC-Earth3' 'FGOALS-g3' 'GISS-E2-1-G' 'GISS-E2-1-H' 'INM-CM4-8' 'INM-CM5-0' 'IPSL-CM6A-LR' 'MCM-UA-1-0' 'MIROC6' 'MIROC-ES2L' 'MRI-ESM2-0' 'NorESM2-LM' 'NorESM2-MM' ) 

var_list=( 'hus' 'ta' 'tas' 'ts' )     
exp='historical'

echo "Starting download"
for mdl in ${model_list[@]}; do
    for var in ${var_list[@]}; do

        if [ ${mdl} == 'AWI-CM-1-1-MR' ]; then
	    mdl_family='AWI'
	    type='gn'
	    member='r1i1p1f1'
            if [ ${var} == 'ta' ] || [ ${var} == 'hus' ]; then
	        version='d20181218'
            elif [ ${var} == 'tas' ]; then
	        version='d20200720'
            else [ ${var} == 'ts' ]
	        version='d20200511'
	    fi 
            declare -a YEARS=($(seq 1850 2014))

	elif [ ${mdl} == 'CESM2-WACCM' ]; then
	     mdl_family='NCAR'
	     type='gn'
	     member='r1i1p1f1'
             version='d20190227'
	     declare -a YEARS=('185001-201412')

        elif [ ${mdl} == 'EC-Earth3' ]; then
	    mdl_family='EC-Earth-Consortium'
	    type='gr'
	    member='r1i1p1f1'
	    version='d20200310'	   
            declare -a YEARS=($(seq 1850 2014)) 

        elif [ ${mdl} == 'FGOALS-g3' ]; then
	    mdl_family='CAS'
	    type='gn'
	    member='r1i1p1f1'
	    version=' d20190818'
            declare -a YEARS=( '185001-185912' '186001-186912' '187001-187912' '188001-188912' '189001-189912' '190001-190912' '191001-191912' '192001-192912' '193001-193912' '194001-194912' '195001-195912' '196001-196912' '197001-197912' '198001-198912' '199001-199912' '200001-200912' '201001-201412' )	
 
        elif [ ${mdl} == 'GISS-E2-1-G' ]; then
	     mdl_family='NASA-GISS'
	     type='gn'
	     member='r1i1p1f1'
	     version='d20180827'
	     declare -a YEARS=('185001-190012' '190101-195012' '195101-200012' '200101-201412' )

        elif [ ${mdl} == 'GISS-E2-1-H' ]; then
	     mdl_family='NASA-GISS'
	     type='gn'
	     member='r1i1p1f1'
	     version='d20190403'
	     declare -a YEARS=('185001-190012' '190101-195012' '195101-200012' '200101-201412' )

        elif [ ${mdl} == 'INM-CM4-8' ]; then
	     mdl_family='INM'
	     type='gr1'
	     member='r1i1p1f1'
	     if [ ${var} == 'hus' ] || [ ${var} == 'ta' ]; then
             version='d20190605'
             declare -a YEARS=( '185001-185912' '186001-186912' '187001-187912' '188001-188912' '189001-189912' '190001-190912' '191001-191912' '192001-192912' '193001-193912' '194001-194912' '195001-195912' '196001-196912' '197001-197912' '198001-198912' '199001-199912' '200001-200912' '201001-201412')
	     else
             version='d20190530'
             declare -a YEARS=( '185001-194912' '195001-199912' '200001-201412')
             fi

        elif [ ${mdl} == 'INM-CM5-0' ]; then
	     mdl_family='INM'
	     type='gr1'
	     member='r1i1p1f1'
	     if [ ${var} == 'hus' ] || [ ${var} == 'ta' ]; then
             version='d20190610'
             declare -a YEARS=( '185001-185912' '186001-186912' '187001-187912' '188001-188912' '189001-189912' '190001-190912' '191001-191912' '192001-192912' '193001-193912' '194001-194912' '195001-195912' '196001-196912' '197001-197912' '198001-198912' '199001-199912' '200001-200912' '201001-201412')
	     else
             version='d20190610'
             declare -a YEARS=( '185001-194912' '195001-201412')
	     fi

        elif [ ${mdl} == 'IPSL-CM6A-LR' ]; then
	     mdl_family='IPSL'
	     type='gr'
	     member='r1i1p1f1'
	     version='d20180803'
	     declare -a YEARS=('185001-201412')

	elif [ ${mdl} == 'MCM-UA-1-0' ]; then
	     mdl_family='UA'
	     type='gn'
	     member='r1i1p1f1'
             version='d20190731'
	     declare -a YEARS=('185001-201412')

	elif [ ${mdl} == 'MIROC6' ]; then
	     mdl_family='MIROC'
	     type='gn'
	     member='r1i1p1f1'
             version='d20190311'
             declare -a YEARS=( '185001-185912' '186001-186912' '187001-187912' '188001-188912' '189001-189912' '190001-190912' '191001-191912' '192001-192912' '193001-193912' '194001-194912' '195001-195912' '196001-196912' '197001-197912' '198001-198912' '199001-199912' '200001-200912' '201001-201412' )

	elif [ ${mdl} == 'MIROC-ES2L' ]; then
	     mdl_family='MIROC'
	     type='gn'
	     member='r1i1p1f2'
	     version='d20190823'
	     declare -a YEARS=('185001-201412')

	elif [ ${mdl} == 'MRI-ESM2-0' ]; then
	     mdl_family='MRI'
	     type='gn'
	     member='r1i1p1f1'
             version='d20190308'
	     declare -a YEARS=('185001-189912' '190001-1949012' '195001-199912' '200001-201412' )

	elif [ ${mdl} == 'NorESM2-LM' ]; then
	     mdl_family='NCC'
	     type='gn'
	     member='r1i1p1f1'
	     version='d20190815'
             declare -a YEARS=( '185001-185912' '186001-186912' '187001-187912' '188001-188912' '189001-189912' '190001-190912' '191001-191912' '192001-192912' '193001-193912' '194001-194912' '195001-195912' '196001-196912' '197001-197912' '198001-198912' '199001-199912' '200001-200912' '201001-201412' )

	else
	     mdl_family='NCC'
	     type='gn'
	     member='r1i1p1f1'
	     version='d20191108'
             declare -a YEARS=( '185001-185912' '186001-186912' '187001-187912' '188001-188912' '189001-189912' '190001-190912' '191001-191912' '192001-192912' '193001-193912' '194001-194912' '195001-195912' '196001-196912' '197001-197912' '198001-198912' '199001-199912' '200001-200912' '201001-201412' )
	fi
	
	base_url="https://dap.ceda.ac.uk/badc/cmip6/data/CMIP6/CMIP/${mdl_family}/${mdl}/${exp}/${member}/Amon/${var}/${type}/files/${version}"
	dir="/leonardo/home/userexternal/mdasilva/leonardo_scratch/CMIP6/historical/${mdl}"

	for year in "${YEARS[@]}"; do

            if [ ${mdl} == 'AWI-CM-1-1-MR' ] || [ ${mdl} == 'EC-Earth3' ]; then
	    filename="${var}_Amon_${mdl}_${exp}_${member}_${type}_${year}01-${year}12.nc"
	    else
	    filename="${var}_Amon_${mdl}_${exp}_${member}_${type}_${year}.nc"
	    fi

	    url="${base_url}/${filename}"
	    file_dir="/leonardo/home/userexternal/mdasilva/leonardo_scratch/CMIP6/historical/${mdl}/${filename}"

	    wget -P "$dir" ${url}
	    
	done
    done
done

echo "Finished downloads."
