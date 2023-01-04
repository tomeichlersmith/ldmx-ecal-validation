#!/bin/bash
#
#SBATCH --partition=shared
#SBATCH --ntasks=1
#SBATCH --output=/sdf/group/ldmx/users/eichl008/valid-scratch/slurm/%A-%a.out
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
#SBATCH --array=0-199

LDMX_DATA=/sdf/group/ldmx/data/validation
LDMX_BASE=/sdf/group/ldmx/users/eichl008

# 300 files
#sample_name="1e-ecal-pn"
#input_files=(${LDMX_DATA}/v12/4.0GeV/v3.2.0_ecalPN/* ${LDMX_DATA}/v14/4.0GeV/v3.2.0_ecalPN-v14/*)

# 200 files
#sample_name="1e-inclusive"
#input_files=(${LDMX_DATA}/v12/4.0GeV/v3.2.0-1e-v12/* ${LDMX_DATA}/v14/4.0GeV/v3.2.0-1e-v14/*)

# 200 files
sample_name="2e-inclusive"
input_files=(${LDMX_DATA}/v12/4.0GeV/v3.2.0-2e-v12/* ${LDMX_DATA}/v14/4.0GeV/v3.2.0-2e-v14/*)

# 300 files
#sample_name="ecal-pn-overlay"
#input_files=(${LDMX_DATA}/v12/4.0GeV/v3.2.0_overlayEcalPN_v12/* ${LDMX_DATA}/v14/4.0GeV/v3.2.0_overlayEcalPN_v14/*)

srun singularity run --no-home \
  --cleanenv --env LDMX_BASE=${LDMX_BASE} \
  --bind ${LDMX_BASE},${LDMX_DATA} \
  ${LDMX_BASE}/ldmx_dev_latest.sif . \
  fire ${LDMX_BASE}/ecal-validation/slac/rereco.py \
  --out-dir ${LDMX_BASE}/valid-scratch/rereco/${sample_name} \
  ${input_files[${SLURM_ARRAY_TASK_ID}]}
