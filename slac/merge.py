import os
import pickle as pkl

working = '/sdf/group/ldmx/users/eichl008/valid-scratch/binned'

histos = {}
for f in os.listdir(working) :
    geo = 'v12' if 'v12' in f else 'v14'
    with open(os.path.join(working,f),'rb') as f :
        h = pkl.load(f)
    if geo in histos :
        for k, (v, b) in h.items() :
            og = histos[geo][k]
            histos[geo][k] = (og[0]+v, og[1])
    else :
        histos[geo] = h

with open(os.path.join(working,'merged.pkl'),'wb') as f :
    pkl.dump(histos,f)
