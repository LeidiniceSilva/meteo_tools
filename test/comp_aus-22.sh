#!/bin/bash

#SBATCH -J AUS-22
#SBATCH -t 24:00:00
#SBATCH -p esp
#SBATCH -N 1 --ntasks-per-node=20

CDO(){
    cdo -O -L -f nc4 -z zip "$@"
}

dom="AUS-22"
indir=/home/mda_silv/scratch/CORDEX-CORE2/CORDEX-CORE
MEMBER_FILE=listMembersAUS22
 
while IFS= read -r member; do
    [[ -z "$member" ]] && continue
 
    echo "Processing member: $member"
 
    # pr: kg m-2 s-1 -> mm/day
    pr_in=${indir}/${dom}/pr/pr_${dom}_${member}_1980-2024_lm.nc
    pr_out=${indir}/${dom}/pr/pr_${dom}_${member}_1980-2024_lm_yr.nc
    CDO yearmean -mulc,86400 "$pr_in" "$pr_out"
 
    # tas: K -> degC
    tas_in=${indir}/${dom}/tas/tas_${dom}_${member}_1980-2024_lm.nc
    tas_out=${indir}/${dom}/tas/tas_${dom}_${member}_1980-2024_lm_yr.nc
    CDO yearmean -subc,273.15 "$tas_in" "$tas_out"
 
done < "$MEMBER_FILE"
 
echo "Done."
