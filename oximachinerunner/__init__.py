# -*- coding: utf-8 -*-
# pylint:disable=invalid-name
"""Implements methods to use oximachine as part of a Python package"""
import os
import sys
import warnings
from typing import Union

import joblib
import numpy as np
from ase import Atoms
from oximachine_featurizer.featurize import FeatureCollector, GetFeatures
from pymatgen import Structure
from pymatgen.io.ase import AseAtomsAdaptor

import oximachinerunner.learnmofox as learnmofox

from ._version import get_versions
from .config import MODEL_CONFIG, MODEL_DEFAULT_MAPPING
from .utils import download_model, model_exists, read_pickle

__version__ = get_versions()['version']
del get_versions
sys.modules['learnmofox'] = learnmofox

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def _load_file(path, md5, url, automatic_download):  # pylint:disable=inconsistent-return-statements
    if model_exists(path, md5):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            model = joblib.load(path)
        return model
    else:  # pylint:disable=no-else-return
        if not automatic_download:
            raise FileNotFoundError("The model does not exist and you didn't allow automatic download.\
                Probably you did not download it yet. You can either enable automatic downloads\
                (automatic_download=True) or use the download functions from the utils module\
                to download the files")
        else:  # pylint:disable=no-else-return
            download_model(url, path, md5)
            _load_file(path, md5, url, automatic_download)


def load_model(modelname, automatic_download):
    # Check if one default model was selected
    if modelname == 'all':
        modelname = MODEL_DEFAULT_MAPPING['all']
    if modelname == 'mof':
        modelname = MODEL_DEFAULT_MAPPING['mof']

    if modelname not in MODEL_CONFIG.keys():
        raise ValueError('A model with name {} does not exist in the configuration.'.format(modelname))

    modelpath = MODEL_CONFIG[modelname]['classifier']['path']
    modelmd5 = MODEL_CONFIG[modelname]['classifier']['md5']
    modelurl = MODEL_CONFIG[modelname]['classifier']['url']

    scalerpath = MODEL_CONFIG[modelname]['scaler']['path']
    scalermd5 = MODEL_CONFIG[modelname]['scaler']['md5']
    scalerurl = MODEL_CONFIG[modelname]['scaler']['url']

    model = _load_file(modelpath, modelmd5, modelurl, automatic_download)
    scaler = _load_file(scalerpath, scalermd5, scalerurl, automatic_download)
    featureset = MODEL_CONFIG[modelname]['features']

    return model, scaler, featureset


class OximachineRunner:

    def __init__(self, modelname: str = 'all', automatic_download: bool = True):
        model, scaler, featureset = load_model(modelname, automatic_download)
        self.modelname = modelname
        self.model = model
        self.scaler = scaler
        self.featureset = featureset

    def __repr__(self):
        return 'OximachineRunner (version: {}) with model {}'.format(__version__, self.modelname)

    def _make_predictions(self, X: np.array) -> list:
        """Makes predictions for a set of metal sites.
        Applies the scaler to the feature matrix.

        Args:
            X (np.array): feature matrix

        Returns:
            list: predictions (this is the vote of the four base estimators)
        """
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)

        return list(prediction)

    def _featurize_single(self, structure: Structure) -> Union[np.array, list, list]:
        """Finds metals in the structure, featurizes the metal sites and collects the features

        Args:
            structure (pymatgen.Structure): Structure to featurize

        Returns:
            Union[np.array, list, list]: [description]
        """
        get_feat = GetFeatures(structure, '')
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
            self.featureset, X)

        metals = [site.species_string for site in get_feat.metal_sites]
        return X, metal_indices, metals

    def run_oximachine(self, structure):
        if isinstance(structure, Structure):
            self._run_oximachine(structure)
        elif isinstance(structure, Atoms):
            s = AseAtomsAdaptor.get_structure(structure)
            self._run_oximachine(s)
        elif isinstance(structure, str):
            # ToDo: Potentially replace the parser with c2x\ 
            # --- but it is unclear how to achieve Mac/Windows/Linux compatibility here
            s = Structure.from_file(structure)
            self._run_oximachine(s)
        else:
            raise ValueError('Could not recognize structure! I can read Pymatgen structure objects,\
                 ASE atom objects and a filepath in a fileformat that can be read by ase')

    def _run_oximachine(self, structure: Structure) -> Union[list, list, list]:
        """Run the oximachine on one structure

        Args:
            structure (Structure): pymatgen Structure object

        Returns:
            Union[list, list, list]: list of oxidation states, list of metal indices,
            list of metal symbols
        """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            X, metal_indices, metal_symbols = self._featurize_single(structure)  # pylint:disable=protected-access

            prediction = self._make_predictions(X)  # pylint:disable=protected-access

        return prediction, metal_indices, metal_symbols
