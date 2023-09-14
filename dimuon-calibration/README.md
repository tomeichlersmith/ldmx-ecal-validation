# Di-Muon Calibration Study

We are going to study how effective using the Di-Muon production process can be
for calibration the LDMX ECal. This directory in this repository will be the main
place where we store our work and notes.

### Helpful Links
- [General LDMX Software Documentation](https://ldmx-software.github.io/)
- [Awkward Array](https://awkward-array.org/doc/main/) - how we hold our data in memory while studying it
- [hist](https://hist.readthedocs.io/en/latest/) - package for filling, manipulating, and plotting histograms
- [UHI Indexing](https://uhi.readthedocs.io/en/latest/indexing.html) - specific page about how `hist` implements pythonic indexing (the stuff between `[` and `]`), helpful reference area

## Table of Contents
- README.md (this file): introduction and explanation
- `upldmx.py`: a python module I wrote to help load ROOT files produced by ldmx-sw into memory
  - It's a pretty small module, mainly focused on "reformatting" the data that is loaded into
    memory by [uproot](https://uproot.readthedocs.io/en/latest/) into a easier-to-use form.
- `target_mumu.py`: a config script to run with `ldmx fire` to generate Di-Muon events.
- [example.ipynb](example.ipynb): an example jupyter notebook showing an imagined workflow
  - I use [jupyter-scikit-hep](https://github.com/tomeichlersmith/jupyter-scikit-hep) to run
    my notebooks which puts jupyter and all the python packages I need into a container because
    I already have a container runner for ldmx-sw, I like having fixed python package versions
    for the different machines I used, and the python installed on our cluster is pretty old.

If you don't want to use the container solution with jupyter (or it doesn't work), you can
install the necessary dependencies with `pip`. In WSL,
```
python3 -m pip install --user --upgrade scikit-hep jupyterlab
```
If this command complains about `python3` not being installed, then you will need to install
that first with
```
sudo apt install python3 python3-pip
```
