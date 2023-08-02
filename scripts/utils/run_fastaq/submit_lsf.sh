#!/usr/bin/env bash
set -eux

MEMORY=4000
PROFILE="lsf_bacterial_assembly_pipeline"
LOG_DIR=logs/
JOB_NAME="snakemake_run_fastaq_pipeline."$(date --iso-8601='minutes')

mkdir -p $LOG_DIR

bsub -R "select[mem>$MEMORY] rusage[mem=$MEMORY] span[hosts=1]" \
     -M "$MEMORY" \
     -o "$LOG_DIR"/"$JOB_NAME".o \
     -e "$LOG_DIR"/"$JOB_NAME".e \
     -J "$JOB_NAME" \
     snakemake --profile "$PROFILE" --keep-going --restart-times 0 "$@"

exit 0
