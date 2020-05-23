# -*- coding: utf-8 -*-
# pylint:disable=invalid-name
"""Implements methods to use oximachine as part of a Python package"""
from __future__ import absolute_import

import os
import sys
from typing import Union

import joblib
import numpy as np
from pymatgen import Structure

import oximachinerunner.learnmofox as learnmofox

from ._version import get_versions
from .featurize import FeatureCollector, GetFeatures
from .utils import read_pickle

__version__ = get_versions()['version']
del get_versions
sys.modules['learnmofox'] = learnmofox

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL = joblib.load(os.path.join(THIS_DIR, 'assets', 'votingclassifier.joblib'))
SCALER = joblib.load(os.path.join(THIS_DIR, 'assets', 'scaler_0.joblib'))

# those global vars are for now hard coded for this model
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
FEATURES = CHEMISTRY_FEATURES + METAL_CENTER_FEATURES + ['crystal_nn_no_steinhardt']


def _make_predictions(X: np.array) -> list:
    """Makes predictions for a set of metal sites.
    Applies the scaler to the feature matrix.

    Args:
        X (np.array): feature matrix

    Returns:
        list: predictions (this is the vote of the four base estimators)
    """
    X_scaled = SCALER.transform(X)
    prediction = MODEL.predict(X_scaled)
    return list(prediction)


def _featurize_single(structure: Structure, feature_dir: str = '') -> Union[np.array, list, list]:
    """Finds metals in the structure, featurizes the metal sites and collects the features

    Args:
        structure (pymatgen.Structure): Structure to featurize
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
    X = np.vstack(X)
    (
        X,
        _,
    ) = FeatureCollector._select_features_return_names(  # pylint:disable=protected-access
        FEATURES, X)
    metals = [site.species_string for site in get_feat.metal_sites]
    return X, metal_indices, metals


def run_oximachine(cif: str) -> Union[list, list, list]:
    """Run the oximachine on one structure

    Args:
        cif (str): Filepath to cif

    Returns:
        Union[list, list, list]: list of oxidation states, list of metal indices,
        list of metal symbols
    """
    structure = Structure.from_file(cif)
    X, metal_indices, metal_symbols = _featurize_single(structure)  # pylint:disable=protected-access
    prediction = _make_predictions(X)  # pylint:disable=protected-access

    return prediction, metal_indices, metal_symbols
