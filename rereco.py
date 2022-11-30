"""Ecal-focused simulation script"""

import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('input_files',nargs='+',help='already simulated files to re-run reco on')
parser.add_argument('--out-dir',help='directory to put output file into (default: same as first input file)')

arg = parser.parse_args()

from LDMX.Framework import ldmxcfg

p = ldmxcfg.Process('rereco')

p.inputFiles = arg.input_files

file_stub = os.path.basename(p.inputFiles[0])
out_dir = os.path.dirname(p.inputFiles[0]) if arg.out_dir is None else arg.out_dir

p.outputFiles = [ os.path.join(out_dir,'rereco_'+file_stub) ]

# we want to see every event
p.logFrequency = 1000
p.termLogLevel = 0

import LDMX.Ecal.EcalGeometry
import LDMX.Ecal.ecal_hardcoded_conditions
import LDMX.Hcal.HcalGeometry
from LDMX.DQM import dqm
import LDMX.Ecal.digi as ecal_digi
import LDMX.Ecal.vetos as ecal_vetos

reco = ecal_digi.EcalRecProducer()
reco.digiPassName = 'rereco'
veto = ecal_vetos.EcalVetoProcessor()
veto.rec_pass_name = 'rereco'

if 'v12' in p.inputFiles[0] :
    reco.v12()
    digi = ecal_digi.EcalDigiProducer(si_thickness = 0.5)
else :
    digi = ecal_digi.EcalDigiProducer()
    


p.sequence = [ digi, reco, veto ]
