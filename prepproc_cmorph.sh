#!/bin/bash

#SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J Postproc
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

#__author__      = 'Leidinice Silva'
#__email__       = 'leidinicesilva@gmail.com'
#__date__        = '02/09/2023'
#__description__ = 'Posprocessing CMORPH satelite data'

{

# load required modules
module purge
source /opt-ictp/ESMF/env202108
set -eo pipefail

CDO(){
  cdo -O -L -f nc4 -z zip $@
}

YR="2000-2009"
IYR=$( echo $YR | cut -d- -f1 )
FYR=$( echo $YR | cut -d- -f2 )

DIR_OUT="/home/mda_silv/users/OBS/CMORPH"

echo
cd ${DIR_OUT}
echo ${DIR_OUT}
	    
for YEAR in `seq -w ${IYR} ${FYR}`; do
    for MON in 01 02 03 04 05 06 07 08 09 10 11 12; do
	for DAY in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31; do
	    
	    DIR_IN="/home/esp-shared-a/Observations/CMORPH/30min/${YEAR}/${MON}/${DAY}"
	    
	    for HOUR in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23; do
	    
	        echo "Posprocessing: CMORPH_V1.0_ADJ_8km-30min_${YEAR}${MON}${DAY}${HOUR}.nc"
		echo "1. Set domain: SESA"
		CDO sellonlatbox,-80,-30,-40,-10 ${DIR_IN}/CMORPH_V1.0_ADJ_8km-30min_${YEAR}${MON}${DAY}${HOUR}.nc CMORPH_V1.0_ADJ_SA_8km-30min_${YEAR}${MON}${DAY}${HOUR}.nc
		
		echo "2. Convert frequence: Hourly"
		CDO hoursum CMORPH_V1.0_ADJ_SA_8km-30min_${YEAR}${MON}${DAY}${HOUR}.nc CMORPH_V1.0_ADJ_SA_8km_hr_${YEAR}${MON}${DAY}${HOUR}.nc
		rm CMORPH_V1.0_ADJ_SA_8km-30min_${YEAR}${MON}${DAY}${HOUR}.nc
		
	    done
        done
    done
done	

echo "3. Concatenate files"			
CDO mergetime CMORPH_V1.0_ADJ_SA_8km_hr_*.nc CMORPH_V1.0_ADJ_SA_hr_${YR}.nc
rm CMORPH_V1.0_ADJ_SA_8km_*.nc

}
