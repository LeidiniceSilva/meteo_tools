#!/bin/bash

#SBATCH -A ICT25_ESP
#SBATCH -p dcgp_usr_prod
#SBATCH -N 1
#SBATCH --ntasks-per-node=112
#SBATCH -t 1-00:00:00
#SBATCH -J Postproc
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

#__author__      = 'Leidinice Silva'
#__email__       = 'leidinicesilva@gmail.com'
#__date__        = 'May 02, 2025'
#__description__ = 'Merge files in daily means'

{

set -eo pipefail

CDO(){
  cdo -O -L -f nc4 -z zip $@
}

DIR_IN="/leonardo/home/userexternal/mdasilva"
cd ${DIR_IN}

YR="1991-2000"
IYR=$( echo $YR | cut -d- -f1 )
FYR=$( echo $YR | cut -d- -f2 )

VAR_LIST="tisr"

for VAR in ${VAR_LIST[@]}; do
    for YEAR in `seq -w ${IYR} ${FYR}`; do

	CDO daysum ${VAR}_ERA5_${YEAR}.nc ${VAR}_ERA5_day_${YEAR}.nc
	
    done
    
    CDO mergetime ${VAR}_ERA5_day_*.nc ${VAR}_ERA5_daymean_${YR}_merged.nc
    
done

}

