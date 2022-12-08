"""Ecal-focused simulation script"""

import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('--n-events',default=10,type=int,help='number of events to simulate')
parser.add_argument('--run',default=1,help='run number (controls random number seeding)')
parser.add_argument('--out-dir',default=os.getcwd(),help='directory to put output file into')
parser.add_argument('--energy',default=4.,help='energy of incident electron in GeV')
# TODO: add arguments for incident angle (theta,phi) and position (x,y)

arg = parser.parse_args()

from LDMX.Framework import ldmxcfg

if not os.path.isdir(arg.out_dir) :
    raise KeyError(f'Need to create output directory {arg.out_dir}')

full_out_dir = os.path.join(arg.out_dir, arg.sim)
os.makedirs(full_out_dir, exist_ok=True)

p = ldmxcfg.Process( "valid" )
p.run = arg.run
p.maxEvents = arg.n_events
p.maxTriesPerEvent = 10000
file_stub = f'energy_{arg.energy}_geometry_v14_events_{arg.n_events}_run_{arg.run}.root'
p.outputFiles = [ full_out_dir+'/type_events_'+file_stub ]
p.histogramFile = full_out_dir+'/type_histos_'+file_stub

# we want to see every event
p.logFrequency = 1000
p.termLogLevel = 0

from LDMX.SimCore import simulator
from LDMX.SimCore import generators
import LDMX.Ecal.EcalGeometry
import LDMX.Ecal.ecal_hardcoded_conditions
import LDMX.Hcal.HcalGeometry
from LDMX.DQM import dqm
import LDMX.Ecal.digi as ecal_digi
import LDMX.Ecal.vetos as ecal_vetos

electrons = generators.gun('ecal-electrons')
electrons.particle = 'e-'
electrons.energy = arg.energy
electrons.direction = [0., 0., 1.]
electrons.position = [0.,0.,220.] #mm - in front of ECal, skip tracker/trig scint

validator = simulator.simulator('plain')
validator.setDetector(f'ldmx-det-v14', False)
validator.description = 'Electrons straight into ECal for ECal geometry testing'
validator.generators = [electrons]

reco = ecal_digi.EcalRecProducer()
veto = ecal_vetos.EcalVetoProcessor()
digi = ecal_digi.EcalDigiProducer()

p.sequence = [ validator, digi, reco, veto ] + dqm.ecal_dqm
