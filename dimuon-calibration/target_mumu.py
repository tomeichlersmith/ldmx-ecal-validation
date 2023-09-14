import argparse
import sys
from pathlib import Path

def nfmt(n):
    """format an integer n with a nice suffix"""
    for suffix in ['','k','M']:
        if n < 1000:
            return f'{n}{suffix}'
        n //= 1000
    return f'{n}B'

parser = argparse.ArgumentParser(
    'ldmx fire '+sys.argv[0],
    formatter_class = argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('--run', type=int, default=1, help='run number to change random seed')
parser.add_argument('--n-events', type=int, default=1000000, help='number of events to throw')
parser.add_argument('--beam', choices=['4','8'], default='4', help='beam energy to study')
parser.add_argument('--out-dir', type=Path, default=Path.cwd(), help='directory to write output file to')
args = parser.parse_args()

from LDMX.Framework import ldmxcfg
from LDMX.SimCore import generators
from LDMX.SimCore import simulator
from LDMX.SimCore import bias_operators
from LDMX.Biasing import filters
from LDMX.Biasing import util
from LDMX.Biasing import include as includeBiasing

p = ldmxcfg.Process('target_mumu')

includeBiasing.library()
import LDMX.Ecal.EcalGeometry
import LDMX.Hcal.HcalGeometry

detector, beam, energy = None, None, None
if args.beam == '4':
    detector = 'ldmx-det-v14'
    beam = generators.single_4gev_e_upstream_tagger()
    energy = 4000. #MeV
elif args.beam == '8':
    detector = 'ldmx-det-v14-8gev'
    beam = generators.single_8gev_e_upstream_tagger()
    energy = 8000. #MeV
else:
    raise ValueError('--beam is not "4" or "8"! (probably bug in this config script)')

if not args.out_dir.is_dir():
    raise ValueError(f'--out-dir {args.out_dir} does not exist (or it cant be seen in the container)')

sim = simulator.simulator("target_gammamumu")

# Set the path to the detector to use.
#   Also tell the simulator to include scoring planes
sim.setDetector( detector , True )

# Set run parameters
sim.description = "gamma -> mu+ mu- in target region"
sim.beamSpotSmear = [20., 80., 0.]
sim.generators = [beam]

min_photon_energy = 0.625*energy

# Enable and configure the biasing
sim.biasing_operators = [ 
    bias_operators.GammaToMuPair('target', 1e6, min_photon_energy)
]

# Configure the sequence in which user actions should be called.
sim.actions.extend([
        # Only consider events where a hard brem occurs
        filters.TaggerVetoFilter(thresh = 0.95*energy),
        filters.TargetBremFilter(recoil_max_p = energy - min_photon_energy, brem_min_e = min_photon_energy),
        filters.TargetGammaMuMuFilter(),
        util.TrackProcessFilter.gamma_mumu()
])

p.run = args.run
p.sequence = [ sim ]
p.maxEvents = args.n_events
p.maxTriesPerEvent = 1
p.termLogLevel = 1
p.logFrequency = args.n_events // 100
p.outputFiles = [ 
    str(args.out_dir / f'target_dimuon_beam_{args.beam}GeV_Nevents_{nfmt(args.n_events)}_run_{args.run}.root')
]
