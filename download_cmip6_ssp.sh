#!/bin/bash

model_list=( 'MIROC-ES2L' ) 

#model_list=( 'AWI-CM-1-1-MR' 'CESM2-WACCM' 'EC-Earth3' 'FGOALS-g3' 'GISS-E2-1-G' 'GISS-E2-1-H' 'INM-CM4-8' 'INM-CM5-0' 'IPSL-CM6A-LR' 'MCM-UA-1-0' 'MIROC6' 'MIROC-ES2L' 'MRI-ESM2-0' 'NorESM2-LM' 'NorESM2-MM' ) 

var_list=( 'hus' 'ta' 'tas' 'ts' )     # 'hus' 'ta' 'tas' 'ts'
exp='ssp245'

echo "Starting download"
for mdl in ${model_list[@]}; do
    for var in ${var_list[@]}; do

        if [ ${mdl} == 'AWI-CM-1-1-MR' ]; then
	    mdl_family='AWI'
	    type='gn'
	    member='r1i1p1f1'
            version='d20190529'
            declare -a YEARS=($(seq 2015 2100))

	elif [ ${mdl} == 'CESM2-WACCM' ]; then
	     mdl_family='NCAR'
	     type='gn'
	     member='r1i1p1f1'
             version='d20190815'
	     declare -a YEARS=('201501-206412' '206501-210012')

        elif [ ${mdl} == 'EC-Earth3' ]; then
	    mdl_family='EC-Earth-Consortium'
	    type='gr'
	    member='r1i1p1f1'
	    version='d20200310'	   
            declare -a YEARS=($(seq 2015 2100))

        elif [ ${mdl} == 'FGOALS-g3' ]; then
	    mdl_family='CAS'
	    type='gn'
	    member='r1i1p1f1'
	    version=' d20190818'
            declare -a YEARS=( '201501-201912' '202001-202912' '203001-203912' '204001-204912' '205001-205901' '206001-206901' '207001-207901' '208001-208901' '209001-209912' '210001-210012' )	

        elif [ ${mdl} == 'GISS-E2-1-G' ]; then
	     mdl_family='NASA-GISS'
	     type='gn'
	     member='r1i1p1f2'
	     version='d20200115'
	     declare -a YEARS=('201501-205012' '205101-210012')

        elif [ ${mdl} == 'INM-CM4-8' ]; then
	     mdl_family='INM'
	     type='gr1'
	     member='r1i1p1f1'
	     if [ ${var} == 'hus' ] || [ ${var} == 'ta' ]; then
             version='d20190605'
            declare -a YEARS=( '201501-202412' '202501-203412' '203501-204412' '204501-205412' '205501-206401' '206501-207401' '207501-208401' '208501-209401' '209501-210012' )
	     else
             version='d20190603'
	     declare -a YEARS=('201501-210012')
	     fi

        elif [ ${mdl} == 'INM-CM5-0' ]; then
	     mdl_family='INM'
	     type='gr1'
	     member='r1i1p1f1'
             version='d20190619'
	     if [ ${var} == 'hus' ] || [ ${var} == 'ta' ]; then
            declare -a YEARS=( '201501-202412' '202501-203412' '203501-204412' '204501-205412' '205501-206401' '206501-207401' '207501-208401' '208501-209401' '209501-210012' )
	     else
	     declare -a YEARS=('201501-210012')
	     fi

        elif [ ${mdl} == 'IPSL-CM6A-LR' ]; then
	     mdl_family='IPSL'
	     type='gr'
	     member='r1i1p1f1'
	     version='d20190119'
	     declare -a YEARS=('201501-210012')

	elif [ ${mdl} == 'MCM-UA-1-0' ]; then
	     mdl_family='UA'
	     type='gn'
	     member='r1i1p1f1'
             version='d20190731'
	     declare -a YEARS=('201501-210012')

	elif [ ${mdl} == 'MIROC6' ]; then
	     mdl_family='MIROC'
	     type='gn'
	     member='r1i1p1f1'
             version='d20190627'
	     if [ ${var} == 'hus' ] || [ ${var} == 'ta' ]; then
            declare -a YEARS=( '201501-202412' '202501-203412' '203501-204412' '204501-205412' '205501-206401' '206501-207401' '207501-208401' '208501-209401' '209501-210012' )
	     else
	     declare -a YEARS=('201501-210012')
	     fi

	elif [ ${mdl} == 'MIROC-ES2L' ]; then
	     mdl_family='MIROC'
	     type='gn'
	     member='r1i1p1f2'
	     version='d20190823'
	     declare -a YEARS=('201501-210012')

	elif [ ${mdl} == 'MRI-ESM2-0' ]; then
	     mdl_family='MRI'
	     type='gn'
	     member='r1i1p1f1'
	     if [ ${var} == 'hus' ] || [ ${var} == 'ta' ]; then
             version='d20190308'
	     declare -a YEARS=('201501-206412' '206501-210012')
	     else
             version='d20190222'
	     declare -a YEARS=('201501-210012')
	     fi

	elif [ ${mdl} == 'NorESM2-LM' ]; then
	     mdl_family='NCC'
	     type='gn'
	     member='r1i1p1f1'
	     version='d20191108'
            declare -a YEARS=( '201501-202012' '202101-203012' '203101-204012' '204101-205012' '205101-206001' '206101-207001' '207101-208001' '208101-209001' '209101-210012' )

	else
	     mdl_family='NCC'
	     type='gn'
	     member='r1i1p1f1'
	     version='d20191108'
            declare -a YEARS=( '201501-202012' '202101-203012' '203101-204012' '204101-205012' '205101-206001' '206101-207001' '207101-208001' '208101-209001' '209101-210012' )
	fi
	
	base_url="https://dap.ceda.ac.uk/badc/cmip6/data/CMIP6/ScenarioMIP/${mdl_family}/${mdl}/${exp}/${member}/Amon/${var}/${type}/files/${version}"
	dir="/leonardo/home/userexternal/mdasilva/leonardo_scratch/CMIP6/ssp245/${mdl}"

	for year in "${YEARS[@]}"; do

            if [ ${mdl} == 'AWI-CM-1-1-MR' ] || [ ${mdl} == 'EC-Earth3' ]; then
	    filename="${var}_Amon_${mdl}_${exp}_${member}_${type}_${year}01-${year}12.nc"
	    else
	    filename="${var}_Amon_${mdl}_${exp}_${member}_${type}_${year}.nc"
	    fi

	    url="${base_url}/${filename}"
	    file_dir="/leonardo/home/userexternal/mdasilva/leonardo_scratch/CMIP6/ssp245/${mdl}/${filename}"

	    wget -P "$dir" ${url}
	    
	done
    done
done

echo "Finished downloads."
