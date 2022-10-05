"""Ecal-focused simulation script"""

import argparse
import os

parser = argparse.ArgumentParser()

parser.add_argument('--n-events',default=10,help='number of events to simulate')
parser.add_argument('--geometry',default=12,choices=[12,13,14],help='version of geometry to simulate')
parser.add_argument('--run',default=1,help='run number (controls random number seeding)')
parser.add_argument('--out-dir',default=os.getcwd(),help='directory to put output file into')

arg = parser.parse_args()

from LDMX.Framework import ldmxcfg

p = ldmxcfg.Process( "valid" )
p.run = arg.run
p.maxEvents = arg.n_events
p.outputFiles = [ f'{arg.out_dir}/simulation_geometry_v{arg.geometry}_events_{arg.n_events}_run_{arg.run}.root' ]

# we want to see every event
p.logFrequency = 1
p.termLogLevel = 0

from LDMX.SimCore import simulator
from LDMX.SimCore import generators
import LDMX.Ecal.EcalGeometry
import LDMX.Hcal.HcalGeometry

electrons = generators.gun('ecal-electrons')
electrons.particle = 'e-'
electrons.energy = 4.0 # GeV
electrons.direction = [0., 0., 1.]
electrons.position = [0.,0.,220.] #mm - in front of ECal, skip tracker/trig scint

validator = simulator.simulator('ecal-validator')
validator.setDetector(f'ldmx-det-v{arg.geometry}', True)
validator.description = 'Electrons straight into ECal for ECal geometry testing'
validator.generators = [electrons]

p.sequence = [ validator ]
