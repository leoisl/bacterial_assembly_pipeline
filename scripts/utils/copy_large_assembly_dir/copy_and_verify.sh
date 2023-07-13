#!/usr/bin/env bash

function copy_and_check {
    input_file=$1
    output_file=$2

    rsync -aq $input_file $output_file

    orig_checksum=$(md5sum $input_file | awk '{print $1}')
    copied_checksum=$(md5sum $output_file | awk '{print $1}')

    if [ "$orig_checksum" != "$copied_checksum" ]; then
        echo "Checksums do not match for file $input_file!"
        exit 1
    fi
}

copy_and_check "${snakemake_input[input_assembly_file]}" "${snakemake_output[output_assembly_file]}"
copy_and_check "${snakemake_input[input_metadata_file]}" "${snakemake_output[output_metadata_file]}"
touch "${snakemake_output[flag]}"
