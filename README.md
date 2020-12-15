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
conda create -n test_oximachine_runner python=3.7
```

Confirm with `y` when asked to do so, then activate with `conda activate test_oximachine_runner`.

### Latest, development, version

```bash
pip install git+https://github.com/kjappelbaum/oximachinerunner.git
```

### Latest stable release

```bash
pip install oximachinerunner
```

Note that the installation will require significant (>500 MB) storage space since the ensembles use k-nearest neighbors models.

## Usage

Note that since version 1 the models are no longer shipped with the PyPi package.
There is a dedicated function to download the models, which has to be run before the first use. Also, in contrast to version 0, the interface is now object-oriented

```python
from oximachinerunner import OximachineRunner
runner = OximachineRunner()
runner.run_oximachine('oximachinerunner/assets/ACODAA.cif')
```

The function will print for how many sites it will run the model.

It will return a `OrderedDict` with:

- A list of oxidation state predictions
- A list of indices of the metal sites
- Strings indicating the metal
- The predictions of the base estimators
- The estimated probabilites

The `OximachineRunner` can be initialized with a modelname. To view which models are available in the current release, use `runner.available_models`. By default, models will be automatically downloaded if there are not yet in the correct folder. You should output as follows

```
/Users/kevinmaikjablonka/opt/miniconda3/envs/test_oximachine_runner/lib/python3.7/site-packages/oximachinerunner/assets/all_202000830/classifier.joblib are not exist or md5 is wrong.
Download file from https://www.dropbox.com/s/lc2z4abaycjbbe1/classifier.joblib?dl=1
2.9% of 527.44M
```

If you want to turn this behavior of, you can set `OximachineRunner(automatic_download=False)`. If you then need a model, you can manually download it using a function from the `utils` module.

The `run_oximachine` function accepts `pymatgen.Structure`, `ase.Atoms` and `str` as well as `os.PathLike`. Latter two are expected to be filepaths to a file that is then parsed with `pymatgen`.

## Reference

Jablonka, Kevin Maik; Ongari, Daniele; Moosavi, Seyed Mohamad; Smit, Berend (2020): Using Collective Knowledge to Assign Oxidation States. ChemRxiv. Preprint. https://doi.org/10.26434/chemrxiv.11604129.v1
