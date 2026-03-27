#!/bin/bash

#SBATCH -N 2
#SBATCH -t 24:00:00
#SBATCH -J ESM_2026
#SBATCH -p esp
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

#__author__      = 'Leidinice Silva'
#__email__       = 'leidinicesilva@gmail.com'
#__date__        = 'Mar 10, 2026'
#__description__ = 'Split yearly to monthly files'
 
{
set -eo pipefail

CDO(){
  cdo -O -L -f nc4 -z zip $@
}

# Split files
vars="slhf sshf"
years=$(seq 1991 2020)

for var in $vars; do
    for year in $years; do
        infile=${var}_ERA5_${year}.nc

	if [ -f "$infile" ]; then
	    echo "Processing $infile"

  	for mon in $(seq -w 1 12); do
	    outfile=${var}_ERA5_${year}_${mon}.nc
	    CDO selmon,$((10#$mon)) $infile $outfile
  	done

	else
	    echo "File not found: $infile"
	fi
	
    done
done

}
