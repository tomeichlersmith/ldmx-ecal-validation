
### Re-Reco
If reco parameters need to be updated relative to what was included in the simulation.
```
sbatch rereco.sh
```
This runs the config `rereco.py` over all the validation files.

### Fill Histograms
```
sbatch batch.sh
```
This runs the python script `fill.py` over the ROOT data files.

### Merge Histograms
```
python3 merge.py
```
This opens all the pickled histograms and adds them together.

### Draw Histograms
```
python3 draw valid-scratch/binned/merged.pkl
```
This draws the merged histograms comparing the two different geometries.
