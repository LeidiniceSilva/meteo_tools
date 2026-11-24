#!/bin/bash

#SBATCH -J CORDEX-CORE2
#SBATCH -t 24:00:00
#SBATCH -p esp
#SBATCH -N 1 --ntasks-per-node=20

set -eo pipefail

CDO() {
  cdo -O -L -f nc4 -z zip "$@"
}

regions=(ALA ANA NWN NEN CWN WSN CNA CEN SEN ESN WSN 
         CAM CAR 
         NWS NSA SAM NES SES SWS SSA 
         NWSH NCSH NESH SWSH SCSH SESH WAF NCAF NEAF SEAF ARP SCAF WSAF ESAF MDG 
         WCA SAS 
         ESB RFE ECA TIB EAS 
         NWSEA NESEA SSEA 
         NAU CAU EAU WSAU ESAU NZE 
         SMED NMED NEU WCE)

indices=(tp t2m) # RR1 RX1day TXx TN20 tp t2m mx2t mn2t
dataset="ERA5-Land"

basedir="/home/netapp-clima-scratch/mda_silv/CORDEX-CORE2/OBS/${dataset}"
maskdir="/home/mda_silv/scratch/CORDEX-CORE2/Masks_AR7"
outdir="/home/netapp-clima-scratch/mda_silv/CORDEX-CORE2/OBS/${dataset}"

maskstore="${outdir}/AR7_masks"
mkdir -p "$maskstore"

for idx in "${indices[@]}"; do

  infile="${basedir}/${idx}/${idx}_${dataset}_1970-2024.nc"
  tmpdir="${outdir}/${idx}_tmp"
  tsdir="${outdir}/${idx}_ts"

  mkdir -p "$tmpdir"
  mkdir -p "$tsdir"

  for reg in "${regions[@]}"; do
    echo "Processing region: ${reg}"

    mask_global="${maskdir}/${reg}_mask.nc"
    mask_cpc="${maskstore}/${reg}_mask_cpc.nc"
    tmpgrid="${maskstore}/grid_${reg}.txt"
    mask_fixed="${maskstore}/${reg}_fixed.nc"

    if [ ! -f "$mask_cpc" ]; then

      CDO griddes "$mask_global" > "$tmpgrid"
      sed -i 's/generic/lonlat/' "$tmpgrid"

      CDO setgrid,"$tmpgrid" "$mask_global" "$mask_fixed" 
      CDO remapnn,"$infile" "$mask_fixed" "$mask_cpc"
      
    fi

    maskedfile="${tmpdir}/${idx}_${reg}_masked.nc"
    CDO ifthen "$mask_cpc" "$infile" "$maskedfile"

    outfile="${tsdir}/${idx}_${reg}_ts.nc"
    CDO -O fldmean -selyear,1970/2024 "$maskedfile" "$outfile"

  done

done

echo "Done"
