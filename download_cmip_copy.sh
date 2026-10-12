#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J Copy
#SBATCH -p esp
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=mda_silv@ictp.it

# models
mdls="NorESM2-MM" # EC-Earth3-Veg MPI-ESM1-2-HR NorESM2-MM

exps="historical"
vars="pr tas tasmax tasmin"

for mdl in $mdls; do
	for exp in $exps; do
		for var in $vars; do

			dir0="/home/clima-archive2-b/mda_silv/ETCCDI/CMIP6/${mdl}"
			dir1="/home/netapp-clima-scratch/mda_silv/CMIP6/${mdl}"
			
			echo ${var} ${mdl} ${exp}
			cp ${dir0}/${var}_day_${mdl}_${exp}_r1i1p1f1_gn_*.nc ${dir1}

		done
	done
done
