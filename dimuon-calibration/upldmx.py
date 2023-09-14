"""load event files output by ldmx-sw into awkward array

currently, we do not do any fancy lazy-loading or caching
and so this can easily overload the memory of the running
computer if one attempts to load too large (many GB) datafile
at once.

Supported ldmx-sw event types:
- SimParticle
- SimTrackerHit
- SimCalorimeterHit
- EventHeader
"""

from pathlib import Path

import uproot
import awkward as ak
import numpy as np
import vector
vector.register_awkward()


def sim_tracker_hit(events, coll):
    def subbranch(member):
        return events[f'{coll}.{member}_']
    the_dict = {
        m : subbranch(m)
        for m in [
            'id', 'layerID', 'moduleID',
            'edep', 'time', 'pathLength', 'trackID', 'pdgID'
        ]
    }
    the_dict.update({
        'momentum' : ak.zip({c : subbranch(c) for c in ['px','py','pz','energy']}, with_name='Momentum4D'),
        'position' : ak.zip({c : subbranch(c) for c in ['x','y','z']}, with_name='Vector3D')
    })
    return ak.zip(the_dict, with_name='SimTrackerHit')



def sim_particle(events, coll):
    def subbranch(member):
        return events[f'{coll}.second.{member}_']
    the_dict = {
        m : subbranch(m)
        for m in [
            'pdgID', 'genStatus', 'mass', 'charge',
            'daughters', 'parents', 'processType', 'vertexVolume'
        ]
    }
    the_dict.update({
        'track_id' : events[f'{coll}.first'],
        'momentum' : ak.zip({c : subbranch(c) for c in ['px','py','pz','energy']}, with_name='Momentum4D'),
        'position' : ak.zip({c : subbranch(c) for c in ['x','y','z','time']}, with_name='Vector4D'),
        'end_momentum' : ak.zip({c : subbranch(f'end{c}') for c in ['px','py','pz']}, with_name='Momentum3D'),
        'end_position' : ak.zip({c : subbranch(f'end{c.upper()}') for c in ['x','y','z']}, with_name='Vector3D')
    })
    return ak.zip(the_dict, with_name='SimParticle', depth_limit=2)


def sim_cal_hit(events, coll):
    def subbranch(member):
        return events[f'{coll}.{member}_']
    the_dict = {
        m : subbranch(m)
        for m in [
            'id', 'edep',
            # dropping pre/post step and velocity information
        ]
    }
    the_dict.update({
        'contrib' : ak.zip({
            'track_id' : subbranch('trackIDContribs'),
            'incident_id' : subbranch('incidentIDContribs'),
            'pdg_id' : subbranch('pdgCodeContribs'),
            'edep' : subbranch('edepContribs'),
            'time' : subbranch('timeContribs')
        }),
        'position' : ak.zip(
            {c : subbranch(c) for c in ['x','y','z','time']},
            with_name='Vector4D'
        )
    })
    return ak.zip(the_dict, with_name='SimCalorimeterHit', depth_limit=2)


def header(events):
    def subbranch(member):
        return events[f'{member}_']
    
    # easy members who don't need to be rezipped
    header_reformat = {
        key : subbranch(key)
        for key in [
            'eventNumber', 'run', 
            #'timestamp_.fSec', 'timestamp_.fNanoSec',
            'weight', 'isRealData'
        ]
    }
    
    # hard members who do need to be rezipped
    to_drop = {'eventSeed'}
    for param_type in ['float','int','string']:
        for key in np.unique(ak.flatten(events[f'{param_type}Parameters_.first']).to_numpy()):
            if key in to_drop:
                continue
            header_reformat[key] = ak.flatten(
                events[f'{param_type}Parameters_.second'][
                    events[f'{param_type}Parameters_.first']==key
                ]
            )
    return ak.zip(header_reformat, with_name='EventHeader')


def reformat(events, passname = 'target_mumu'):
    event_dict = {
        'EventHeader' : header(events),
        'SimParticles' : sim_particle(events, f'SimParticles_{passname}')
    }
    event_dict.update({
        collection : sim_cal_hit(events, f'{collection}_{passname}')
        for collection in [
            'HcalSimHits', 'EcalSimHits', 'TargetSimHits',
            'TriggerPad1SimHits','TriggerPad2SimHits','TriggerPad3SimHits'
        ]
    })
    event_dict.update({
        collection : sim_tracker_hit(events, f'{collection}_{passname}')
        for collection in [
            'RecoilSimHits','TaggerSimHits'
            # dropping scoring planes
        ]
    })
    return ak.zip(event_dict, depth_limit=1)


def load(f: str | Path):
    with uproot.open(f) as rf:
        return reformat(rf['LDMX_Events'].arrays())