import uproot
import pickle as pkl
import sys
import numpy as np
import os

input_file = sys.argv[1]

out_dir = '/sdf/group/ldmx/users/eichl008/valid-scratch/binned/'

hist_spec = [
    ('nReadoutHits_', dict(range=(0,200),bins=50)),
    ('deepestLayerHit_', dict(range=(0,34),bins=34)),
    ('summedDet_', dict(range=(0,10000),bins=1000)),
    ('summedTightIso_', dict(range=(0,5000), bins=500)),
    ('maxCellDep_', dict(range=(0,500),bins=50)),
    ('showerRMS_', dict(range=(0,200),bins=50)),
    ('xStd_', dict(range=(0,200),bins=50)),
    ('yStd_', dict(range=(0,200),bins=50)),
    ('avgLayerHit_', dict(range=(0,34),bins=34)),
    ('stdLayerHit_', dict(range=(0,17),bins=17)),
    ('ecalBackEnergy_',dict(range=(0,5000),bins=500)),
    ('nStraightTracks_',dict(range=(0,30),bins=30)),
    ('nLinregTracks_',dict(range=(0,10),bins=10))
    ]

with uproot.open(input_file) as f :
    b = f['LDMX_Events/EcalVeto_rereco']
    histos = {
        k : np.histogram(b[k].array(library='np'), **bins)
        for k, bins in hist_spec 
        }
    with open(out_dir+os.path.basename(input_file).replace('root','pkl'),'wb') as f :
        pkl.dump(histos, f)
        
