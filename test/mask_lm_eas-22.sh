#!/bin/bash

#SBATCH -J EAS-22
#SBATCH -t 24:00:00
#SBATCH -p esp
#SBATCH -N 1 --ntasks-per-node=20

#__author__      = 'Leidinice Silva'
#__email__       = 'leidinicesilva@gmail.com'
#__date__        = 'Nov 20, 2023'
#__description__ = 'Compute ETCCDI indices using CDO-ECA'

CDO(){
    cdo -O -L -f nc4 -z zip "$@"
}


dom="EAS-22"
maindir=/home/mda_silv/scratch/CORDEX-CORE2/CORDEX-CORE
indir=/home/mda_silv/scratch/CORDEX-CORE2/CORDEX-CORE/${dom}

# Masks
MASK_REG=/home/clima-archive3-b/nzazulie/indices/${dom}/mask_${dom}_RegCM.nc
MASK_GERICS=/home/clima-archive3-b/nzazulie/indices/${dom}/mask_${dom}_GERICS.nc

MEMBER_FILE=listMembersEAS22

indices=(pr tas)

# Read the member file line by line
while IFS= read -r member; do
    [[ -z "$member" ]] && continue   # skip empty lines

    # Determine correct mask
    if [[ "$member" == *"RegCM4"* ]]; then
        mask="$MASK_REG"
    elif [[ "$member" == *"GERICS"* ]]; then
        mask="$MASK_GERICS"

    else
        echo "WARNING: Could not determine mask for member: $member"
        continue
    fi

    echo "Processing member: $member"
    echo "Using mask: $mask"

    for idx in "${indices[@]}"; do
            infile=${indir}/${idx}/${idx}_${dom}_${member}_1980-2024.nc
            outfile=${indir}/${idx}/${idx}_${dom}_${member}_1980-2024_lm.nc

            if [[ -f "$infile" ]]; then
                echo "  Masking $infile → $outfile"
                CDO ifthen "$mask" "$infile" "$outfile"
            else
                echo "  WARNING: File not found: $infile"
            fi

    done

done < "$MEMBER_FILE"

echo "Masking completed."
