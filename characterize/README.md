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

### Helpful Plots
For studying the resolution of measurement X, there are many helpful plots we can make.
- Distribution of X (for making sure it is normal)
  - If the distribution of X is not-normal, there is something else going on that we need to understand.
- Distribution of X divided by the true value (for comparing multiple different true values)
- Mean of X divided by true value vs true value (for seeing how accuracy changes with true value)
- Resolution of X vs true value (for seeing how resolution changes with true value)

## Getting Started
For a lot of reasons, measuring the energy is the simplest place to start.
We will start with a [configuration script](simulation.py) that fires a single electron
directly into the ECal. This allows us to use the total reconstructed energy in the entire
ECal as the measurement of the incident electron's energy.

In the output file holding the events, the measurements of total reconstructed energy are
located at `LDMX_Events/EcalVeto_valid/EcalVeto_valid/summedDet_` inside the file where
there is one measurement for each event.

**First Task**: Load the measurements into Jupyter Lab and create a histogram of them.
Plot a normal distribution on top with the mean and standard deviation of these measurements
so we can make sure they are normally distributed.

## Tools
- jupyter lab
- scipy
- numpy
- uproot
- matplotlib
