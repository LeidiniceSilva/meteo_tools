#!/bin/bash

domains=(SEA-22)
#domains=(AFR-22 AUS-22 CAM-22 EAS-22 EUR-11 NAM-22 SEA-22 SAM-22 WAS-22)
indices=(pr tas)

basedir=/home/mda_silv/scratch/CORDEX-CORE2/CORDEX-CORE
maskdir=/home/mda_silv/scratch/CORDEX-CORE2/CORDEX-CORE/Masks_AR7
outdir=/home/mda_silv/scratch/CORDEX-CORE2/CORDEX-CORE

for dom in "${domains[@]}"; do

echo "==== DOMAIN $dom ===="

[[ $dom = NAM-22 ]] && subregs="ALA ANA NWN NEN CWN WSN CNA CEN SEN ESN WSN"  
[[ $dom = CAM-22 ]] && subregs="CAM CAR"
[[ $dom = SAM-22 ]] && subregs="NWS NSA SAM NES SES SWS SSA"
[[ $dom = AFR-22 ]] && subregs="NWSH NCSH NESH SWSH SCSH SESH WAF NCAF NEAF SEAF ARP SCAF WSAF ESAF MDG"
[[ $dom = WAS-22 ]] && subregs="WCA SAS" 
[[ $dom = EAS-22 ]] && subregs="ESB RFE ECA TIB EAS"
[[ $dom = SEA-22 ]] && subregs="NWSEA NESEA SSEA"
[[ $dom = AUS-22 ]] && subregs="NAU CAU EAU WSAU ESAU NZE"
[[ $dom = EUR-11 ]] && subregs="SMED NMED NEU WCE"

for idx in "${indices[@]}"; do

indir=${basedir}/${dom}/${idx}
outts=${outdir}/${dom}/${idx}_ts
maskstore=${outdir}/${dom}/AR7_masks
tmpdir=${outdir}/${dom}/${idx}_tmp

mkdir -p "$outts"
mkdir -p "$maskstore"
mkdir -p "$tmpdir"

for infile in ${indir}/${idx}_*_1980-2024_lm_yr.nc; do

file=$(basename "$infile")
member=${file#${idx}_}
member=${member%_1980-2024_lm_yr.nc}

# Extract RCM name (3rd field)
rcm=$(echo $member | cut -d'_' -f4)

echo "Member: $member"
echo "RCM grid: $rcm"

for reg in $subregs; do

	mask_global=${maskdir}/${reg}_mask.nc
	mask_rcm=${maskstore}/${reg}_${rcm}.nc

	# ------------------------------------------------
	# Create remapped mask only if it doesn't exist
	# ------------------------------------------------
	if [[ ! -f $mask_rcm ]]; then

		echo "Creating mask for $reg on grid $rcm"

		tmpgrid=${maskstore}/grid_${reg}.txt
		mask_fixed=${maskstore}/${reg}_fixed.nc

		cdo griddes $mask_global > $tmpgrid
		sed -i 's/generic/lonlat/' $tmpgrid

		cdo -O setgrid,$tmpgrid $mask_global $mask_fixed
		cdo -O remapnn,$infile $mask_fixed $mask_rcm

		rm -f $tmpgrid $mask_fixed

	fi
        tmpfile=${tmpdir}/${idx}_${member}_${reg}_masked.nc
	outfile=${outts}/${idx}_${member}_${reg}_ts.nc

	echo "Processing: $idx | $member | $reg"

	#cdo -O fldmean -selyear,1970/2020 -setctomiss,1e20 -ifthen $mask_rcm $infile $outfile
	#create masked field
	cdo -O -setctomiss,1e20 -ifthen $mask_rcm $infile $tmpfile

	# compute regional mean
	cdo -O fldmean -selyear,1980/2024 $tmpfile $outfile

	done
done
done
done

echo "==== COMPLETE ===="
