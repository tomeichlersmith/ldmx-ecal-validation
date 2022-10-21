"""CLI for comparison plots within Ecal Validation"""

import argparse
import os
from _differ import Differ

# guard incase someone imports this somehow
if __name__ == '__main__' :
    parser = argparse.ArgumentParser()

    parser.add_argument('v12',help='v12 simulation')
    parser.add_argument('v14',help='v14 simulation')

    args = parser.parse_args()


    d = Differ('v3.2.0-alpha',(args.v12,'v12'),(args.v14,'v14'))

    d.plot1d('EcalSimHits_valid/EcalSimHits_valid.edep_',
             'Sim Energy Dep [MeV]',
             file_name = 'edep',
             out_dir = os.getcwd())

