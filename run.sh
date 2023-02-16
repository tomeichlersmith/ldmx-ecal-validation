#!/bin/bash
# run.sh 
#   run four simulations within container

__usage__() {
  cat <<HELP
 USAGE:
  ldmx ./run.sh [-o|--out-dir OUT_DIR] [-N|--n-events NUM_EVENTS]
                [-s|--sim SIM]

 OPTIONS:
  -o, --out-dir  : Base output directory for data files
  -N, --n-events : Number of events per geometry to simulate (default: 10k)
  -s, --sim      : Simulation to run (options: 'plain', 'ecalpn')

HELP
}

__main__() {
  if [ -z ${LDMX_BASE} ]; then
    echo "ERROR: Need to be in ldmx environment."
    echo "  source the ldmx-env.sh script in ldmx-sw."
    return 1
  fi
  local _output_dir=$(cd data && pwd -P)/dev
  local _n_events=10000
  local _sim="plain"
  while [ $# -gt 0 ]; do
    case $1 in
      -o|--out-dir|-N|--n-events|-s|--sim)
        if [ -z $2 ]; then
          echo "ERROR: '$1' requires an argument."
          return 1
        fi
        case $1 in
          -o|--out-dir) _output_dir=$2;;
          -N|--n-events) 
            if ! [[ $2 =~ '^[0-9]+$' ]]; then
              echo "ERROR: '$2' is not a number."
              return 1
            fi
            _n_events=$2;;
          -s|--sim) 
            case $2 in
              plain|ecalpn)
                _sim=$2
                ;;
              *)
                echo "ERROR: Unrecognized simulation '$2'"
                return 1
                ;;
            esac
            ;;
        esac
        shift
        ;;
      -h|--help|-?)
        __usage__
        return 0
        ;;
      *)
        echo "ERROR: Unrecognized option '$1'."
        return 1
        ;;
    esac
    shift
  done
  
  if ! mkdir -p ${_output_dir}; then
    echo "ERROR: Could not create output directory ${_output_dir}"
    return $?
  fi

  for g in 12 14; do
    fire simulation.py \
      --n-events ${_n_events} \
      --out-dir ${_output_dir} \
      --sim ${_sim} \
      --geometry ${g} \
      &> ${_output_dir}/sim_${_sim}_v${g}.log &
  done
  wait
}

__main__ $@ 
