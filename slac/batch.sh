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
#SBATCH --array=0-299

LDMX_BASE=/sdf/group/ldmx/users/eichl008

#input_files=(/sdf/group/ldmx/data/validation/v12/4.0GeV/v3.2.0_ecalPN/* /sdf/group/ldmx/data/validation/v14/4.0GeV/v3.2.0_ecalPN-v14/*)
input_files=(${LDMX_BASE}/valid-scratch/rereco/*)

srun python3 ${LDMX_BASE}/ecal-validation/slac/fill.py ${input_files[${SLURM_ARRAY_TASK_ID}]}
