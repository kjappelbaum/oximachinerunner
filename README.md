# oximachinerunner

[![Actions Status](https://github.com/kjappelbaum/oximachinerunner/workflows/Python%20package/badge.svg)](https://github.com/kjappelbaum/oximachinerunner/actions)

_oximachine for AiiDA lab_: Core functionalities of oximachine with stripped dependencies.

_**Warning:** This model works excellent on a test set but it might give fully unphysical predictions in some cases when it is used outside the domain of applicability (structures similar to the ones in the MOF subset of the CSD). This is currently estimated with an uncertainty vote. Consider it in alpha phase_

## assets

- `votingclassifier.joblib` is the model that is currently deployed. It is a voting classifier with four different base estimators
- `scaler.joblib` is the standard scaler
- `KAJZIH_freeONLY.cif` and `ACODAA.cif` are some test structures.
