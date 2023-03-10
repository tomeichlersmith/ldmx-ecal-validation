# ECal Characteristic Plots
Studying how the ECal design performs under a variety of controlled scenarios
using a set of "standard" plots.

We cannot expect a perfect measurement where we always measure the true value without any error.
Besides the quantum fundamentals preventing this, there are many detector effects that cause
normally-distributed random fluctuations (e.g. electronic noise, sampling losses). Still, we
hope to understand how these fluctuations affect the measurements our detector makes.

Essentially, we want to know the ECal's [resolution](resolution.md) in energy and position
after varying the incident electron's energy, angle, and position. This can help us characterize
how the ECal will perform within the experiment.

There are a few different types of [averages](averages.md) that we will use as well.

## Running Task List
- [x] run simulations of varying energies
- [x] load measured energy and plot histograms of accuracy samples
- [x] calculate energy resolution and accuracy and plot various beam energies to show trends (including error bars to reflect statistical uncertainty)
- [ ] imbue code with more structure with `pandas.DataFrame` so that it can be more flexible
- [ ] use `mplhep` to make plots look more familiar to ROOT users

## Tools
- jupyter lab
- scipy
- numpy
- uproot
- matplotlib
- mplhep
- pandas
