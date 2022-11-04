"""CLI for comparison plots within Ecal Validation"""

import argparse
import os
import re
import matplotlib as mpl
mpl.use('Agg')
from _differ import Differ
import time

import matplotlib.pyplot as plt
import mplhep
plt.style.use(mplhep.style.ROOT)

def extract_parameters(fn) :
    l = fn.replace('.root','').split('_')
    if 'rereco' == l[0] :
        l = l[1:]
    return l[0], { l[i] : l[i+1] for i in range((len(l)-1)) if i%2 == 1 }

# guard incase someone imports this somehow
if __name__ == '__main__' :
    parser = argparse.ArgumentParser(
        description="""
        Make comparison plots between different geometries.

        We assume that the input files are written out in the
        format of the configs in this repository so we can
        deduce the parameters from their names.
        """
        )

    parser.add_argument('dev',help='directory of event and histogram files from new developments')
    parser.add_argument('--label',help='label for developments, defaults to dev directory name')
    parser.add_argument('--out-dir',help='directory to which to print plots. defaults to input data dev dir')
    parser.add_argument('--last-valid',help='Diretory with event and histogram files from last major validation')
    parser.add_argument('--last-valid-name', help='Name of last major validation (defaults to directory name)')
    parser.add_argument('--do-histos',help='Do already-written histograms in histo files',action='store_true')

    arg = parser.parse_args()

    dev = arg.dev
    if dev.endswith('/') :
        dev = dev[:-1]
    print(dev)

    label = os.path.basename(dev)
    if arg.label is not None :
        label = arg.label

    out_dir = dev
    if arg.out_dir is not None :
        out_dir = arg.out_dir

    def generate_colmod(fp) :
        if fp.startswith('rereco') :
            def colmod(c) :
                return c.replace('valid','rereco')
            return colmod
        else :
            return None

    root_files = [ 
        (os.path.join(dev,f), extract_parameters(f)) 
        for f in os.listdir(dev) if f.endswith('.root') 
        ]

    last_valid_files = []
    last_valid = arg.last_valid
    if last_valid is not None :
        if last_valid.endswith('/') :
            last_valid = last_valid[:-1]
        last_valid_name = os.path.basename(last_valid)
        if arg.last_valid_name is not None :
            last_valid_name = arg.last_valid_name

        last_valid_files = [
            (os.path.join(last_valid,f), extract_parameters(f))
            for f in os.listdir(last_valid) if f.endswith('.root')
            ]

    if arg.do_histos :
        histo_files = [ (fp, params['geometry']) for fp, (t, params) in root_files if t == 'histos' ]
        histo_files.extend(
            [ (fp, last_valid_name+' '+params['geometry']) for fp, (t, params) in last_valid_files if t == 'histos' ])
    
        hd = Differ(label, *histo_files)
    
        shower_feats = [
            ('EcalShowerFeatures/EcalShowerFeatures_deepest_layer_hit', 'Deepest Layer Hit'),
            ('EcalShowerFeatures/EcalShowerFeatures_num_readout_hits', 'N Readout Hits'),
            ('EcalShowerFeatures/EcalShowerFeatures_summed_det', 'Total Rec Energy [MeV]'),
            ('EcalShowerFeatures/EcalShowerFeatures_summed_iso', 'Total Isolated Energy [MeV]'),
            ('EcalShowerFeatures/EcalShowerFeatures_summed_back', 'Total Back Energy [MeV]'),
            ('EcalShowerFeatures/EcalShowerFeatures_max_cell_dep', 'Max Cell Dep [MeV]'),
            ('EcalShowerFeatures/EcalShowerFeatures_shower_rms', 'Shower RMS [mm]'),
            ('EcalShowerFeatures/EcalShowerFeatures_x_std', 'X Standard Deviation [mm]'),
            ('EcalShowerFeatures/EcalShowerFeatures_y_std', 'Y Standard Deviation [mm]'),
            ('EcalShowerFeatures/EcalShowerFeatures_avg_layer_hit', 'Avg Layer Hit'),
            ('EcalShowerFeatures/EcalShowerFeatures_std_layer_hit', 'Std Dev Layer Hit')
            ]
        histo_draw_times = []
        for path, name in shower_feats :
            start = time.time()
            hd.plot1d(path, name, 
                      file_name = re.sub(r'^.*/','',path),
                      out_dir = out_dir)
            histo_draw_times.append(time.time() - start)

        print('Histos:', sum(histo_draw_times)/len(histo_draw_times))

    event_files = [ 
        (fp, params['geometry'] + (' rereco' if 'rereco' in fp else ''), generate_colmod(fp)) 
        for fp, (t, params) in root_files if t == 'events' ]
    event_files.extend([ 
      (fp, last_valid_name+' '+params['geometry']) 
      for fp, (t, params) in last_valid_files if t == 'events' ])
    ed = Differ(arg.label, *event_files)
    event_draw_times = []

    shower_feats = [
        ('LDMX_Events/EcalVeto_valid/nReadoutHits_', 'N Readout Hits', dict(bins=100,range=(0,300))),
        ('LDMX_Events/EcalVeto_valid/deepestLayerHit_', 'Deepest Layer Hit', dict(bins=40,range=(0,40))),
        ('LDMX_Events/EcalVeto_valid/summedDet_', 'Total Rec Energy [MeV]', dict(bins=800,range=(0,8000))),
        ('LDMX_Events/EcalVeto_valid/summedTightIso_', 'Total Isolated Energy [MeV]', dict(bins=400,range=(0,4000))),
        ('LDMX_Events/EcalVeto_valid/maxCellDep_', 'Max Single-Cell Energy Dep [MeV]', dict(bins=100,range=(0,1000))),
        ('LDMX_Events/EcalVeto_valid/showerRMS_', 'Transverse Shower RMS [mm]', dict(bins=200,range=(0,200))),
        ('LDMX_Events/EcalVeto_valid/xStd_', 'X Std Deviation [mm]', dict(bins=200,range=(0,200))),
        ('LDMX_Events/EcalVeto_valid/yStd_', 'Y Std Deviation [mm]', dict(bins=200,range=(0,200))),
        ('LDMX_Events/EcalVeto_valid/avgLayerHit_', 'Avg Layer Hit', dict(bins=40,range=(0,40))),
        ('LDMX_Events/EcalVeto_valid/stdLayerHit_', 'Std Dev Layer Hit', dict(bins=20,range=(0,20)))
        ]
    for path, name, kw in shower_feats :
        start = time.time()
        ed.plot1d(path, name, **kw,
                  file_name = re.sub(r'^.*/','',path),
                  out_dir = out_dir)
        event_draw_times.append(time.time() - start)

    print('Events:', sum(event_draw_times)/len(event_draw_times))
