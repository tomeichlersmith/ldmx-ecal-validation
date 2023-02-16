"""CLI for comparison plots within LDMX Validation"""

# standard
import argparse
import os
import re
import logging

# external
import matplotlib
# this line allows us to run without an X server connected
#    basically telling MPL that it will not open a window
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import mplhep
plt.style.use(mplhep.style.ROOT)

# us
from Validation import Differ, File, ecal

# guard incase someone imports this somehow
if __name__ == '__main__' :
    parser = argparse.ArgumentParser("python3 plot.py",
        description="""
        Make comparison plots between different files within a directory.

        The labels of different plots within the directory is controlled by
        the parameter you choose. The parameters of a file are extracted from
        the file name by splitting the filename into key-val pairs separated 
        by underscores (i.e. key1_val1_key2_val2_..._keyN_valN.root). If no
        parameter is provided, then the first key/val is used.
        """
        )

    parser.add_argument('data',help='directory of event and histogram files')
    parser.add_argument('--label',help='label for grouping of data, defaults to data directory name')
    parser.add_argument('--reference',help='directory with reference event and histogram files')
    parser.add_argument('--reference-label',help='label for histograms from reference directory')
    parser.add_argument('--log',help='logging level',choices=['info','debug','warn','error'], default='warn')
    parser.add_argument('--out-dir',help='directory to which to print plots. defaults to input data directory')

    arg = parser.parse_args()

    numeric_level = getattr(logging, arg.log.upper(), None)
    if not isinstance(numeric_level, int) :
        raise ValueError(f'Invalid log level: {arg.log}')
    logging.basicConfig(level=numeric_level)

    logging.getLogger('matplotlib').setLevel(logging.ERROR)

    logging.debug(f'Parsed Arguments: {arg}')

    data = arg.data
    if data.endswith('/') :
        data = data[:-1]

    label = os.path.basename(data)
    if arg.label is not None :
        # update the raw string literal to intrepret new lines
        label = arg.label.replace(r'\n','\n')

    out_dir = data
    if arg.out_dir is not None :
        out_dir = arg.out_dir

    logging.debug(f'Deduced Args: label = {label} out_dir = {out_dir}')

    root_files = [ File.from_path(os.path.join(data,f), legendlabel_parameter = 'geometry') 
        for f in os.listdir(data) if f.endswith('.root') and '1000000' not in f]

    # make sure v12 geometry is plotted first and then v14
    root_files.sort(key=lambda f : repr(f))

    if arg.reference is not None :
        root_files.extend([
          File(os.path.join(arg.reference,f), hist_kwargs=dict(label=arg.reference_label))
          for f in os.listdir(arg.reference) if f.endswith('.root')
          ])

    logging.debug(f'ROOT Files: {root_files}')

    hd = Differ(label, *[f for f in root_files if not f.is_events()])
    ed = Differ(label, *[f for f in root_files if f.is_events()])

    logging.debug(f'histogram differ = {hd}')
    logging.debug(f'event differ = {ed}')

    logging.info('running shower_feats')
    ecal.shower_feats(hd, out_dir = out_dir)
    logging.info('running sim_hits')
    ecal.sim_hits(ed, out_dir = out_dir)

