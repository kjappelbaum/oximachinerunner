# -*- coding: utf-8 -*-
# pylint:disable=invalid-name
"""Implements methods to use oximachine as part of a Python package"""
from __future__ import absolute_import

import os
import sys
import warnings
from typing import Union

import joblib
import numpy as np
from oximachine_featurizer.featurize import FeatureCollector, GetFeatures
from pymatgen import Structure

import oximachinerunner.learnmofox as learnmofox

from ._version import get_versions
from .utils import read_pickle

__version__ = get_versions()['version']
del get_versions
sys.modules['learnmofox'] = learnmofox

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    MODEL_MOF = joblib.load(os.path.join(THIS_DIR, 'assets', 'votingclassifier.joblib'))
    SCALER_MOF = joblib.load(os.path.join(THIS_DIR, 'assets', 'scaler_0.joblib'))

    # MODEL_ALL = joblib.load(os.path.join(THIS_DIR, 'assets', '20200823-161001_ensemble_0.joblib'))
    # SCALER_ALL = joblib.load(os.path.join(THIS_DIR, 'assets', '20200822-151455_scaler.joblib'))
    # VT_ALL = joblib.load(os.path.join(THIS_DIR, 'assets', '20200822-151455_vt.joblib'))

# those global vars are for now hard coded for this model

FEATURES_MOF = ['local_property_stats'] + [
    'column',
    'row',
    'valenceelectrons',
    'diffto18electrons',
    'sunfilled',
    'punfilled',
    'dunfilled',
] + ['crystal_nn_no_steinhardt']

METAL_CENTER_FEATURES = [
    'column',
    'row',
    'valenceelectrons',
    'diffto18electrons',
    'sunfilled',
    'punfilled',
    'dunfilled',
]
GEOMETRY_FEATURES = ['crystal_nn_fingerprint', 'behler_parinello']
CHEMISTRY_FEATURES = ['local_property_stats']

FEATURES_ALL = CHEMISTRY_FEATURES + METAL_CENTER_FEATURES + ['crystal_nn_fingerprint', 'behler_parinello']


def _make_predictions(X: np.array, model: str = 'mof') -> list:
    """Makes predictions for a set of metal sites.
    Applies the scaler to the feature matrix.

    Args:
        X (np.array): feature matrix
        model (str): can be used to toggle between the model trained only on MOFs ("mof")
            and the model trained on all the CSD + COD ("all"). Defaults to "mof"

    Returns:
        list: predictions (this is the vote of the four base estimators)
    """
    if model == 'all':
        X = VT_ALL.transform(X)
        X_scaled = SCALER_ALL.transform(X)
        prediction = MODEL_ALL.predict(X_scaled)
    elif model == 'mof':
        X_scaled = SCALER_MOF.transform(X)
        prediction = MODEL_MOF.predict(X_scaled)
    else:
        X_scaled = SCALER_MOF.transform(X)
        prediction = MODEL_MOF.predict(X_scaled)
    return list(prediction)


def _featurize_single(structure: Structure, model: str = 'mof', feature_dir: str = '') -> Union[np.array, list, list]:
    """Finds metals in the structure, featurizes the metal sites and collects the features

    Args:
        structure (pymatgen.Structure): Structure to featurize
        model (str): can be used to toggle between the model trained only on MOFs ("mof")
            and the model trained on all the CSD + COD ("all"). Defaults to "mof"
        feature_dir (str, optional): Directory to which features should be saved,
        can be useful if features should be reused. Defaults to "".

    Returns:
        Union[np.array, list, list]: [description]
    """
    get_feat = GetFeatures(structure, feature_dir)
    features = get_feat.return_features()
    metal_indices = get_feat.metal_indices
    X = []
    feat_dict_list = FeatureCollector.create_dict_for_feature_table_from_dict(features)
    for feat_dict in feat_dict_list:
        X.append(feat_dict['feature'])

    if model == 'mof':
        X = np.vstack(X)
        (
            X,
            _,
        ) = FeatureCollector._select_features_return_names(  # pylint:disable=protected-access
            FEATURES_MOF, X)
    elif model == 'all':
        X = np.vstack(X)
        (
            X,
            _,
        ) = FeatureCollector._select_features_return_names(  # pylint:disable=protected-access
            FEATURES_ALL, X)

    metals = [site.species_string for site in get_feat.metal_sites]
    return X, metal_indices, metals


def run_oximachine(cif: str, model='mof') -> Union[list, list, list]:
    """Run the oximachine on one structure

    Args:
        cif (str): Filepath to cif
        model (str): can be used to toggle between the model trained only on MOFs ("mof")
            and the model trained on all the CSD + COD ("all"). Defaults to "mof"

    Returns:
        Union[list, list, list]: list of oxidation states, list of metal indices,
        list of metal symbols
    """
    if model == 'all': 
        raise NotImplementedError('The model trained on all structures of the CSD is not available in this release')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        structure = Structure.from_file(cif)
        X, metal_indices, metal_symbols = _featurize_single(structure, model=model)  # pylint:disable=protected-access

        prediction = _make_predictions(X, model=model)  # pylint:disable=protected-access

    return prediction, metal_indices, metal_symbols
