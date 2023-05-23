# When Shower Starts

We've been talking a lot about qualitatively understanding when a shower starts and now we want to look at 
_quantitatively_ calculating a variable that can tell us precisely when a shower is beginning.

### X% of Energy
We want to calculate the percentage of the total reconstructed energy in an event deposited in a given layer
and all layers in front of it. I see this as four separate calculations
1. Calculate the energy in a given layer in a given event
2. Calculate the energy in a given event
3. Calculate the percent of the energy in a given layer in a given event (combine 1 and 2)
4. Cumulatively sum these percentages so that the value of a specific layer includes the percent 
    deposited in earlier (lower layer number) layers

I've been able to deduce a possible solution.
```python
# df is a multi-index dataframe where 'number' is the event number, 'layer' is the layer number for a hit,
#    and 'energy' is the energy for a hit
energy_per_layer_per_event = df.groupby(['number','layer'])['energy'].sum()
energy_per_event = energy_per_layer_per_event.groupby(['number']).sum()
percent_energy_per_layer_per_event = energy_per_layer_per_event / energy_per_event
cumulative_percent_energy_per_layer_per_Event = percent_energy_per_layer_per_event.groupby(['number']).cumsum()
```
This is actually a bit of an oversimplification compared to the actual shape of our data,
but hopefully it is an illustrative example. Below I've dumped some code that I used to
test this procedure with an actual file written by ldmx-sw. 
```python
import pandas as pd
import uproot
import awkward as ak
# with the ROOT file open, we parse the arrays we need into a pandas dataframe
# we need the event number for grouping by event, the ID to get the layer, and the hit energy
# you may need to install additional python packages for this call of 'arrays' to work
#   python3 -m pip install --user awkward-pandas
with uproot.open('data.root') as f:
    df = f['LDMX_Events'].arrays(
        filter_name=['EventHeader/eventNumber_','EcalRecHits_eat.id_','EcalRecHits_eat.energy_'],
        library='pd' # need to specify 'pd' for library for pandas
    )
# we need to convert the awkward data into python lists so we can explode them into their own columns
#   this is the part that takes the longest and I can't find a better solution right now
for m in ['id','energy']:
    df[f'EcalRecHits_eat.{m}_'] = df[f'EcalRecHits_eat.{m}_'].apply(ak.to_list)
# explode the columns that previously had a list as each entry so that a new row is
#    created for each element of that list
df = df.explode([f'EcalRecHits_eat.{m}_' for m in ['id','energy']])
# inform the dataframe the types of our columns
#    as a relic of the 'ak.to_list' we used earlier, we lost the datatype
df['EcalRecHits_eat.id_'] = df['EcalRecHits_eat.id_'].astype(int)
df['EcalRecHits_eat.energy_'] = df['EcalRecHits_eat.energy_'].astype(float)
# calculate the layer of each hit
df['layer'] = (df['EcalRecHits_eat.id_'].to_numpy() >> 17) & 0x3f
# now we can go through with the calculation described above

energy_per_layer_per_event = df.groupby(['eventNumber_','layer'])['EcalRecHits_eat.energy_'].sum()

(energy_per_layer_per_event / energy_per_layer_per_event.groupby('eventNumber_').sum()).groupby('eventNumber_').cumsum()
```
