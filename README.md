# oximachinerunner

[![Actions Status](https://github.com/kjappelbaum/oximachinerunner/workflows/Python%20package/badge.svg)](https://github.com/kjappelbaum/oximachinerunner/actions)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kjappelbaum/oximachinerunner/master?filepath=examples%2Fexample.ipynb)
[![Documentation Status](https://readthedocs.org/projects/oximachinerunner/badge/?version=latest)](https://oximachinerunner.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/kjappelbaum/pyepal/branch/master/graph/badge.svg?token=BL2CF4HQ06)](https://codecov.io/gh/kjappelbaum/oximachinerunner)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oximachinerunner)

## Installation

On macOS you need to run `brew install libomp` first to enable multithreading for the `XGBoost` library.

Ideally, you install everything in a clean environment, e.g., using conda

```bash
conda create -n test_oximachine_runner python=3.7 -y
```

Then activate with `conda activate test_oximachine_runner`.

### Latest stable release

```bash
pip install oximachinerunner
```

Note that the installation requires significant (>500 MB) storage space since the ensembles use k-nearest neighbors models.

### Development version

```bash
pip install git+https://github.com/kjappelbaum/oximachinerunner.git
```

## Usage

#### Loading the model

```python
from oximachinerunner import OximachineRunner
runner = OximachineRunner()
```

The `OximachineRunner` can be initialized with a modelname from `runner.available_models`.

By default, models will be automatically downloaded (upon first use) if there are not yet in the correct folder:

```
/Users/kevinmaikjablonka/opt/miniconda3/envs/test_oximachine_runner/lib/python3.7/site-packages/oximachinerunner/assets/all_202000830/classifier.joblib are not exist or md5 is wrong.
Download file from https://www.dropbox.com/s/lc2z4abaycjbbe1/classifier.joblib?dl=1
2.9% of 527.44M
```

To disable this behavior of, set `OximachineRunner(automatic_download=False)` and manually download your model, e.g. using a function from the `utils` module.

#### Predicting oxidation states

The `run_oximachine` function accepts `pymatgen.Structure`, `ase.Atoms` and `str` as well as `os.PathLike`.
The latter two are expected to be paths to a file that is then parsed with `pymatgen`.

```python
runner.run_oximachine('oximachinerunner/assets/ACODAA.cif')
```

The function prints for how many sites it will run the model.

```
featurize.py: iterating over 6 metal sites
```

It returns an `OrderedDict` with the fields:

- `metal_indices`: A list of indices of the metal sites
- `metal_symbols`: A list of symbols of the metal atoms
- `prediction`: A list of oxidation state predictions
- `max_probabs`: For each metal site the maximum confidence of all 4 models.
- `base_predictions`: For each metal site a list of the oxidation state predictions for each of the 4 models.

### Development setup

```
git clone https://github.com/kjappelbaum/oximachinerunner
pip install -e .[dev]
```

## Reference

Jablonka, Kevin Maik; Ongari, Daniele; Moosavi, Seyed Mohamad; Smit, Berend (2020): Using Collective Knowledge to Assign Oxidation States. ChemRxiv. Preprint. https://doi.org/10.26434/chemrxiv.11604129.v1
