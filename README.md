# LDMX ECal Simulated Geometry Validation

This repository is focused on storing configuration scripts for `fire` and python-based analyses
related to validating the simulated geometry of the ECal.

## Running the Simulation
The simulation is run via `ldmx fire` with the [config script](simulation.py) in this repository.
Generally, you want to simulate both the v12 and v14 geometries, which would require two runs.
```
ldmx fire simulation.py --geometry 12 --n-events <n-events> --out-dir <out-dir>
ldmx fire simulation.py --geometry 14 --n-events <n-events> --out-dir <out-dir>
```
In order to roughly parallelize this, a [bash script](run.sh) was written to be run within the container.
```
ldmx ./run.sh -o <out-dir> -N <n-events>
```

### Full Procedure
This is a reference on the procedure for getting the simulation up and running.
We assume that ldmx-sw has already be `git clone`d onto your computer.

Enter the ldmx-sw environment
```
source ldmx-sw/scripts/ldmx-env.sh
```

**Only if needed**, recompile ldmx-sw. This is only necessary if you `git pull`d
changes to the ldmx-sw source code.
```
cd ldmx-sw/build
ldmx make install
```

Determine the version of ldmx-sw you are running.
```
cd ldmx-sw
git describe --tags
```

Create a directory for the simulated data pertaining to the version of the
simulation you are running.
```
cd ecal-validation
mkdir -p data/<specific-version-name>
```

Run the simulation.
```
ldmx ./run.sh -o data/<specific-version-name> -N <n-events>
```

## Running the Analysis
The analysis code largely consists of filling and drawing histograms.

### Installing the Validation Module
We have a python module in development that was originally here but has been moved to ldmx-sw
so that we can share it more broadly. Right now, it resides on a specific branch of ldmx-sw.
```
cd ldmx-sw
git checkout iss1114
python3 -m pip install Validation/
```
If you are going to make changes to the code in the Validation module, it is advised
to use an "editable" install inside of a virtual environment.
```
# in this directory
python3 -m venv .venv --prompt valid
source .venv/bin/activate
cd ../ldmx-sw
python3 -m pip install -e Validation
```
Then in subsequent sessions, you just need to `source .venv/bin/activate` from this
directory so that you can start using the Validation module that is in the source
directory. **Note**: This means if you switch to a branch that does not have the Validation
files, the module will not be available to be used.

## Table of Contents
- run.sh : a helper script for roughly parallelizing the two geometry runs
- simulation.py : the config to run the simulations
- rereco.py : a config to re-run the reconstruction if only reco-level changes were made
- test.ipynb : testing the Validation module and other scratch work
- [characterize](characterize) the ECal's performance in simulation
- [dimuon calibration](dimuon-calibration) studying how frequently a given cell has a muon pass through it for calibration purposes
