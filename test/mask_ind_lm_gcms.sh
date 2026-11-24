#!/bin/bash

#SBATCH -N 1 
##SBATCH -N 1
#SBATCH -t 24:00:00
#SBATCH -J Mask
#SBATCH -p esp,long
#SBATCH -o cat_lm.out
#SBATCH -e cat_lm.err


# Mask file
mask=/home/netapp-clima/users/coppolae/AR6/CORDEX-ATLAS/MASKS/mask_2.0ok.nc

# Root directory containing all indices
indir=/home/mda_silv/scratch/CORDEX-CORE2/CMIP5/input

# Model list
list=list_GCM_all

# Indices to process
indices="tas" # pr tas tasmax tasmin

for ind in $indices; do
     echo $ind
    dir=${indir}/${ind}
     echo $dir
    for gcm in $(cat $list); do

        infile=${dir}/${ind}_${gcm}_1970-2024.nc
        #infile=${dir}/${ind}_mmday_${gcm}_1970-2024.nc
        outfile=${dir}/${ind}_${gcm}_1970-2024_lm.nc
        echo $infile
        echo $outfile
        if [ -f "$infile" ]; then
            echo "Processing $ind $gcm"
            cdo -L -O remapnn,$mask $infile aux.nc
            cdo -L -O ifthen $mask aux.nc $outfile

        else
            echo "Missing: $ind $gcm"
        fi

    done
    rm aux.nc
done

echo "Processing complete."
