# oximachinerunner

[![Actions Status](https://github.com/kjappelbaum/oximachinerunner/workflows/Python%20package/badge.svg)](https://github.com/kjappelbaum/oximachinerunner/actions)

_oximachine for AiiDA lab_: Core functionalities of oximachine with stripped dependencies.

_**Warning:** This model works excellent on a test set but it might give fully unphysical predictions in some cases. Consider it in alpha phase_

- It is good to know where it fails
- We work on improving the model by training it on a larger subset of the CSD with a new architecture

- The featurization can be slow in some cases. In practice, it is best to get the smallest possible cell of a clean structure.
- There is still one dependency on one of my forks of a well-known package.
- The package is slow
- For compatability and reproducibility we need to pin an old scikit-learn version

## features not deployed for AiIDA lab

- Feature importance (slow as it has to integrate the dataset. Also, it is quite likely that we will break the API here in the future when we add new features)
- Most similar structures in training set (is typically fast though, as it uses a KDtree)
- Uncertainity estimate (not sure how the best way to use this in a workchain?)

## assets

- `votingclassifier.joblib` is the model that is currently deployed. It is a voting classifier with four different base estimators
- `scaler.joblib` is the standard scaler
- `KAJZIH_freeONLY.cif` and `ACODAA.cif` are some test structures.
