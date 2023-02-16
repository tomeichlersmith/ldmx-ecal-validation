"""draw the histograms in the pickled dictionary"""

import pickle
import os
import sys
from PyPDF2 import PdfMerger

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import mplhep
plt.style.use(mplhep.style.ROOT)

working = '/sdf/group/ldmx/users/eichl008/valid-scratch'

def plt_hist(ax, np_hist, **kwargs) :
    if 'histtype' not in kwargs :
        kwargs['histtype'] = 'step'
    if 'linewidth' not in kwargs :
        kwargs['linewidth'] = 2
    ax.hist(np_hist[1][1:], bins=np_hist[1], weights=np_hist[0], **kwargs)
    
def main() :
    with open(os.path.join(working,'binned/merged.pkl'), 'rb') as f :
        h = pickle.load(f)

    style = [
        ('nReadoutHits_', 'N Reco Hits'),
        ('deepestLayerHit_', 'Deepest Layer Hit'),
        ('summedDet_', 'Total Reco Energy [MeV]'),
        ('summedTightIso_', 'Total Isolated Energy [MeV]'),
        ('maxCellDep_', 'Maximum Cell E Dep [MeV]'),
        ('showerRMS_', 'Shower RMS [mm]'),
        ('xStd_', 'X std dev [mm]'),
        ('yStd_', 'Y std dev [mm]'),
        ('avgLayerHit_', 'Avg Layer Hit'),
        ('stdLayerHit_', 'Std Layer Hit'),
        ('ecalBackEnergy_', 'Total Back Energy [MeV]'),
        ('nStraightTracks_', 'N Straight Tracks'),
        ('nLinregTracks_', 'N Lin Reg Tracks')
    ]

    merger = PdfMerger()

    for feat, xlabel in style :
        fig = plt.figure('valid')
        ax = fig.subplots()
        print(feat, end=' ')
        for geo in ['v12','v14'] :
            plt_hist(ax, h[geo][feat], label=geo)
            print(geo, h[geo][feat][0].sum(), end=' ')
        print()
        ax.set_xlabel(xlabel)
        ax.set_ylabel('Events')
        ax.set_yscale('log')
        ax.legend()
        ax.set_title('1e ECal PN')
        fig.savefig(working+'/drawn/'+feat+'.pdf',bbox_inches='tight')
        fig.clf()
        merger.append(working+'/drawn/'+feat+'.pdf')

    merger.write('ecal_pn_1e_shower_feats.pdf')
    merger.close()

if __name__ == '__main__' :
    main()
