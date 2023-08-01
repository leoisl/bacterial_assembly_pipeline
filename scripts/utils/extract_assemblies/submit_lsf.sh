#!/usr/bin/env bash
set -eux

MEMORY=1000
PROFILE="lsf_bacterial_assembly_pipeline"
LOG_DIR=logs/
JOB_NAME="snakemake_extract_assemblies_pipeline."$(date --iso-8601='minutes')

mkdir -p $LOG_DIR

bsub -R "select[mem>$MEMORY] rusage[mem=$MEMORY] span[hosts=1]" \
     -M "$MEMORY" \
     -o "$LOG_DIR"/"$JOB_NAME".o \
     -e "$LOG_DIR"/"$JOB_NAME".e \
     -J "$JOB_NAME" \
     snakemake --profile "$PROFILE" --keep-going "$@"

exit 0
