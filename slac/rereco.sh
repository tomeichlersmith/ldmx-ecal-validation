#!/bin/bash
#
#SBATCH --partition=shared
#SBATCH --ntasks=1
#SBATCH --output=valid-scratch/slurm/%A-%a.out
#
# Filename Pattern Quick Ref:
#   %J - job id number (universal)
#   %a - array number
#   %A - master number for arrays
#
#SBATCH --job-name=ldmx-valid
#
# there are 150 files in both geometry samples
#  and the --array parameter INCLUDES both limits
#SBATCH --array=0-299

LDMX_DATA=/sdf/group/ldmx/data
LDMX_BASE=/sdf/group/ldmx/users/eichl008

input_files=(${LDMX_DATA}/validation/v12/4.0GeV/v3.2.0_ecalPN/* ${LDMX_DATA}/validation/v14/4.0GeV/v3.2.0_ecalPN-v14/*)

srun singularity run --no-home \
  --cleanenv --env LDMX_BASE=${LDMX_BASE} \
  --bind ${LDMX_BASE},${LDMX_DATA} \
  ${LDMX_BASE}/ldmx_dev_latest.sif . \
  fire ${LDMX_BASE}/rereco.py \
  --out-dir ${LDMX_BASE}/valid-scratch/rereco ${input_files[${SLURM_ARRAY_TASK_ID}]}
