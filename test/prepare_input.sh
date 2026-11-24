#!/bin/bash

outdir="/home/mda_silv/scratch/CORDEX-CORE2/CMIP5/input"
basedir="/home/esp-shared-a/GlobalModels/CMIP5/daily"

vars=("tasmin" "tasmax" "tas" "pr")

models=(
"CCCma-CanESM2_r1"
#"CNRM-CERFACS-CNRM-CM5_r1"
#"ICHEC-EC-EARTH_r12"
#"ICHEC-EC-EARTH_r1"
#"ICHEC-EC-EARTH_r3"
#"IPSL-IPSL-CM5A-LR_r1"
#"IPSL-IPSL-CM5A-MR_r1"
#"MIROC-MIROC5_r1"
#"MOHC-HadGEM2-ES_r1"
#"MPI-M-MPI-ESM-LR_r1"
#"MPI-M-MPI-ESM-LR_r2"
#"MPI-M-MPI-ESM-LR_r3"
#"NCC-NorESM1-M_r1"
#"NOAA-GFDL-GFDL-ESM2M_r1"
)

year_start=1970
year_end=2024

for var in "${vars[@]}"; do

    mkdir -p "${outdir}/${var}"

    for model in "${models[@]}"; do

        member=$(echo $model | cut -d'_' -f2)

        case $model in
            CCCma-CanESM2_*) gcm="CanESM2" ;;
            CNRM-CERFACS-CNRM-CM5_*) gcm="CNRM-CM5" ;;
            ICHEC-EC-EARTH_*) gcm="EC-EARTH" ;;
            IPSL-IPSL-CM5A-LR_*) gcm="IPSL-CM5A-LR" ;;
            IPSL-IPSL-CM5A-MR_*) gcm="IPSL-CM5A-MR" ;;
            MIROC-MIROC5_*) gcm="MIROC5" ;;
            MOHC-HadGEM2-ES_*) gcm="HadGEM2-ES" ;;
            MPI-M-MPI-ESM-LR_*) gcm="MPI-ESM-LR" ;;
            NCC-NorESM1-M_*) gcm="NorESM1-M" ;;
            NOAA-GFDL-GFDL-ESM2M_*) gcm="GFDL-ESM2M" ;;
        esac

        member_full="${member}i1p1"
        out_file="${outdir}/${var}/${var}_${model}_${year_start}-${year_end}.nc"
        tmpdir=$(mktemp -d "${outdir}/${var}/tmp_${model}_XXXX")

        echo "Processing $var $model (GCM: $gcm)"

        # Pastas por experimento 
        hist_dir="${basedir}/historical/${gcm}"
        rcp_dir="${basedir}/rcp8.5/${gcm}"

        # Lista de arquivos 
        mapfile -t hist_files < <(find "$hist_dir" -type f -name "${var}_day_${gcm}_historical_${member_full}_*.nc" | sort)
        mapfile -t rcp_files  < <(find "$rcp_dir"  -type f -name "${var}_day_${gcm}_rcp85_${member_full}_*.nc" | sort)

        if [ ${#hist_files[@]} -eq 0 ] || [ ${#rcp_files[@]} -eq 0 ]; then
            echo "  AVISO: arquivos nao encontrados (hist=${#hist_files[@]}, rcp=${#rcp_files[@]}). Pulando."
            #rmdir "$tmpdir"
            continue
        fi

        # Merge de todos os anos
        cdo mergetime "${hist_files[@]}" "${tmpdir}/hist_merged.nc"
        cdo mergetime "${rcp_files[@]}"  "${tmpdir}/rcp_merged.nc"

        # Merge dos dois experimentos 
        cdo selyear,${year_start}/${year_end} -mergetime "${tmpdir}/hist_merged.nc" "${tmpdir}/rcp_merged.nc" "$out_file"

        #rm -rf "$tmpdir"
        echo "  OK -> $out_file"

    done

done
