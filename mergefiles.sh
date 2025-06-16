#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J Mergefile
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

#__author__      = 'Leidinice Silva'
#__email__       = 'leidinicesilva@gmail.com'
#__date__        = 'May 02, 2025'
#__description__ = 'Merge files in daily means'

{

# load required modules
source /opt-ictp/ESMF/env202108
set -eo pipefail

CDO(){
  cdo -O -L -f nc4 -z zip $@
}

YR="1992-1994"
IYR=$( echo $YR | cut -d- -f1 )
FYR=$( echo $YR | cut -d- -f2 )

VAR_LIST="tisr"

for VAR in ${VAR_LIST[@]}; do
    for YEAR in `seq -w ${IYR} ${FYR}`; do

	CDO daymean ${VAR}_ERA5_${YEAR}.nc ${VAR}_ERA5_day_${YEAR}.nc
	
    done
    
    #CDO mergefiles ${VAR}_ERA5_day_*.nc ${VAR}_ERA5_daymean_${YR}_merged.nc
    
done

}

