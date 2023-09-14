import argparse
import sys
from pathlib import Path

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
p = ldmxcfg.Process('target_mumu')
from LDMX.Biasing import target
from LDMX.SimCore import generators
import LDMX.Ecal.EcalGeometry
import LDMX.Hcal.HcalGeometry

detector, beam = None, None
if args.beam == '4':
    detector = 'ldmx-det-v14'
    beam = generators.single_4gev_e_upstream_tagger()
elif args.beam == '8':
    detector = 'ldmx-det-v14-8gev'
    beam = generators.single_8gev_e_upstream_tagger()
else:
    raise ValueError('--beam is not "4" or "8"! (probably bug in this config script)')

if not args.out_dir.is_dir():
    raise ValueError(f'--out-dir {args.out_dir} does not exist (or it cant be seen in the container)')

def nfmt(n):
    """format an integer n with a nice suffix"""
    for suffix in ['','k','M']:
        if n < 1000:
            return f'{n}{suffix}'
        n //= 1000
    return f'{n}B'

p.run = args.run
p.sequence = [ target.gamma_mumu(detector, beam) ]
p.maxEvents = args.n_events
p.maxTriesPerEvent = 1
p.termLogLevel = 1
p.logFrequency = args.n_events // 100
p.outputFiles = [ 
    str(args.out_dir / f'target_dimuon_beam_{args.beam}GeV_Nevents_{nfmt(args.n_events)}_run_{args.run}.root')
]
