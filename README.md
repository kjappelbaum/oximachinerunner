# oximachinerunner

[![Actions Status](https://github.com/kjappelbaum/oximachinerunner/workflows/Python%20package/badge.svg)](https://github.com/kjappelbaum/oximachinerunner/actions)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kjappelbaum/oximachinerunner/master?filepath=examples%2Fexample.ipynb)

_oximachine for AiiDA lab_: Core functionalities of oximachine with stripped dependencies.

_**Warning:** This model works excellent on a test set but it might give fully unphysical predictions in some cases when it is used outside the domain of applicability (structures similar to the ones in the MOF subset of the CSD). This is currently estimated with an uncertainty vote. Consider it in alpha phase_

## Installation

### Latest, development, version

```(bash)
pip install git+git@github.com:kjappelbaum/oximachinerunner.git
```

### Latest stable release

```(bash)
pip install oximachinerunner
```

## Usage

```(python)
from oximachinerunner import run_oximachine
run_oximachine('oximachinerunner/assets/ACODAA.cif')
```

Will return a tuple with three elements:

- A list of oxidation states
- A list of indices of the metal sites
- Strings indicating the metal

## assets

Currently, served directly in the package. In the future might be fetched from an external storage.

- `votingclassifier.joblib` is the model that is currently deployed. It is a voting classifier with four different base estimators
- `scaler.joblib` is the standard scaler
- `KAJZIH_freeONLY.cif` and `ACODAA.cif` are some test structures.
