#!/bin/bash

#SBATCH -A ICT26_ESP
#SBATCH -p dcgp_usr_prod
#SBATCH -N 1
#SBATCH --ntasks-per-node=112
#SBATCH -t 1-00:00:00
#SBATCH -J ETCCDI
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=mda_silv@ictp.it

set -eo pipefail

CDO() {
  cdo -O -L -f nc4 -z zip "$@"
}

indices=(pr tas) # RR1 RX1day TXx TN20

basedir=/home/mda_silv/scratch/CORDEX-CORE2/CMIP5
maskdir=/home/mda_silv/scratch/CORDEX-CORE2/Masks_AR7
outdir=/home/mda_silv/scratch/CORDEX-CORE2/CMIP5

model_list=${basedir}/list_GCM_all

regions="ALA ANA NWN NEN CWN WSN CNA CEN SEN ESN WSN \
         CAM CAR \
         NWS NSA SAM NES SES SWS SSA \
         NWSH NCSH NESH SWSH SCSH SESH WAF NCAF NEAF SEAF ARP SCAF WSAF ESAF MDG \
         WCA SAS \
         ESB RFE ECA TIB EAS \
         NWSEA NESEA SSEA \
         NAU CAU EAU WSAU ESAU NZE \
         SMED NMED NEU WCE"

# Model range
for n in {1..12}; do

    model=$(sed -n "${n}p" ${model_list})

    echo "===== MODEL: $model ====="
    for idx in "${indices[@]}"; do

        indir=${basedir}/${idx}
        infile=${indir}/${idx}_${model}_1970-2024.nc

        if [[ ! -f $infile ]]; then
            echo "Missing file: $infile"
            continue
        fi

        tmpdir=${outdir}/${idx}/tmp_AR7
        tsdir=${outdir}/${idx}_ts
        maskstore=${outdir}/AR7_masks_GCM

        mkdir -p $tmpdir
        mkdir -p $tsdir
        mkdir -p $maskstore

        gridfile=$infile

        for reg in $regions; do

            mask_global=${maskdir}/${reg}_mask.nc
            mask_model=${maskstore}/${reg}_mask_${model}.nc

            # Create mask 
            if [[ ! -f $mask_model ]]; then

                echo "Preparing mask for $reg on grid of $model"

                tmpgrid=${maskstore}/grid_${reg}.txt
                mask_fixed=${maskstore}/${reg}_fixed.nc

                cdo griddes $mask_global > $tmpgrid
                sed -i 's/generic/lonlat/' $tmpgrid

                cdo -O setgrid,$tmpgrid $mask_global $mask_fixed
                cdo -O remapnn,$gridfile $mask_fixed $mask_model

                rm -f $tmpgrid $mask_fixed

            fi

            outfile=${tsdir}/${idx}_${model}_${reg}_ts.nc

            echo "Processing $idx | $model | $reg"

            # mask + regional mean (single step)
            cdo -O fldmean -ifthen $mask_model $infile $outfile

        done

    done

done

echo "==== GCM processing complete ===="
