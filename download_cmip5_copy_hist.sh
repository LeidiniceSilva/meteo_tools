#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J Copy
#SBATCH -p esp
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=mda_silv@ictp.it

# models
mdls="ACCESS1-0 BCC-CSM1-1-M CanESM2 CNRM-CM5 FGOALS-G2 GFDL-CM3 GFDL-ESM2M INMCM4 IPSL-CM5A-MR MIROC5 MPI-ESM-LR MRI-CGCM3 ACCESS1-3 BNU-ESM CCSM4 CSIRO-Mk3-6-0 FGOALS-S2 GFDL-ESM2G HadGEM2-ES IPSL-CM5A-LR IPSL-CM5B-LR MIROC-ESM  MPI-ESM-MR NorESM1-M"

exps="historical"
vars="pr tasmax tasmin"

for mdl in $mdls; do
	for exp in $exps; do
		for var in $vars; do

			dir0="/home/esp-shared-a/GlobalModels/CMIP5/daily/${exp}/${mdl}"
			dir1="/home/mda_silv/clima-archive2-b/CMIP5/${mdl}"
			
			echo ${var} ${mdl} ${exp}
			#cp ${dir0}/${var}_day_${mdl}_${exp}_r1i1p1_*.nc ${dir1}
			cp ${dir0}/${var}_day_inmcm4_${exp}_r1i1p1_*.nc ${dir1}

		done
	done
done
