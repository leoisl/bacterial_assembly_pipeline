#!/usr/bin/env bash
set -eux

MEMORY=1000
PROFILE="lsf_bacterial_assembly_pipeline"
LOG_DIR=logs/
JOB_NAME="snakemake_bacterial_assembly_pipeline."$(date --iso-8601='minutes')

mkdir -p $LOG_DIR

bsub -R "select[mem>$MEMORY] rusage[mem=$MEMORY] span[hosts=1]" \
     -q long \
     -M "$MEMORY" \
     -o "$LOG_DIR"/"$JOB_NAME".o \
     -e "$LOG_DIR"/"$JOB_NAME".e \
     -J "$JOB_NAME" \
     snakemake --profile "$PROFILE" --keep-going --restart-times 1 --rerun-trigger mtime "$@"

exit 0
