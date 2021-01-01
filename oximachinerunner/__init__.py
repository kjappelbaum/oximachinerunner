# -*- coding: utf-8 -*-
# pylint:disable=wrong-import-position
"""Implements methods to use oximachine as part of a Python package"""
import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)
from collections import OrderedDict
from typing import Dict, List, Tuple, Union

import joblib
import numpy as np
from ase import Atoms
from oximachine_featurizer import featurize
from oximachine_featurizer.featurize import get_feature_names
from pymatgen import Structure
from pymatgen.io.ase import AseAtomsAdaptor

import oximachinerunner.learnmofox as learnmofox

from ._version import get_versions
from .config import MODEL_CONFIG, MODEL_DEFAULT_MAPPING
from .utils import download_model, mode_std_predict_dropout, model_exists

__version__ = get_versions()["version"]
del get_versions
sys.modules["learnmofox"] = learnmofox

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def _load_file(
    path, md5: str, url: str, automatic_download: bool = True, keras_model: bool = False
) -> object:  # pylint:disable=inconsistent-return-statements
    """[summary]

    Args:
        path (str, PathLike): Path of the model file
        md5 (str): md5 hash of the model file
        url (str): url to download the file from
        automatic_download (bool): If true, it automatically downloads
            the file if it is not available
        keras_model (bool): If true, it assumes that the model is a keras model

    Raises:
        FileNotFoundError: If automatic_download is not enabled and the file
            is not on the disk

    Returns:
        model, typically a sklearn estimator object
    """
    if model_exists(path, md5):  # pylint:disable=no-else-return

        if keras_model:
            import zipfile  # pylint:disable=import-outside-toplevel

            from tensorflow import keras  # pylint:disable=import-outside-toplevel

            extract_dir = Path(path).parents[0]
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
                extracted = zip_ref.namelist()
                extracted_file = os.path.join(extract_dir, extracted[0])
            model = keras.models.load_model(extracted_file)
        else:
            model = joblib.load(path)
        return model
    else:
        if not automatic_download:
            raise FileNotFoundError(
                "The model does not exist and you didn't allow automatic download.\
                Probably you did not download it yet. You can either enable automatic downloads\
                (automatic_download=True) or use the download functions from the utils module\
                to download the files"
            )
        download_model(url, path, md5)
        return _load_file(path, md5, url, automatic_download, keras_model)


def load_model(
    modelname: str, automatic_download: bool = True, keras_model: bool = False
) -> Tuple:
    """Orchestrates the loading of the model and the scaler

    Args:
        modelname (str): name of the model
        automatic_download (bool): if true,
            it will attempt to automatically download the model
        keras_model (bool): If true, it assumes that the model is a keras model

    Raises:
        ValueError: if the modelname is not defined in the configuration

    Returns:
        model, scaler, featurenames
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Check if one default model was selected

        try:
            modelname = MODEL_DEFAULT_MAPPING[modelname]
        except KeyError:
            pass

        if modelname not in MODEL_CONFIG.keys():
            raise ValueError(
                "A model with name {} does not exist in the configuration.".format(
                    modelname
                )
            )

        modelpath = MODEL_CONFIG[modelname]["classifier"]["path"]
        modelmd5 = MODEL_CONFIG[modelname]["classifier"]["md5"]
        modelurl = MODEL_CONFIG[modelname]["classifier"]["url"]

        scalerpath = MODEL_CONFIG[modelname]["scaler"]["path"]
        scalermd5 = MODEL_CONFIG[modelname]["scaler"]["md5"]
        scalerurl = MODEL_CONFIG[modelname]["scaler"]["url"]

        model = _load_file(
            modelpath, modelmd5, modelurl, automatic_download, keras_model
        )
        scaler = _load_file(scalerpath, scalermd5, scalerurl, automatic_download)
        featureset = MODEL_CONFIG[modelname]["features"]

    return model, scaler, featureset


class OximachineRunner:
    """Loads a model and then runs the prediction"""

    def __init__(self, modelname: str = "all", automatic_download: bool = True):
        """

        Args:
            modelname (str, optional): [description]. Defaults to 'all'.
                Use it to specifiy a model. You can view all available models with
                the .available_models property
            automatic_download (bool, optional): [description]. Defaults to True.
        """
        self.modelname = modelname
        self._automatic_download = automatic_download
        self.md5 = MODEL_CONFIG[MODEL_DEFAULT_MAPPING[modelname]]["classifier"]["md5"]
        self._model_dict = {}
        self._is_voting_ensemble = True
        self._is_nn_model = False

    @property
    def model(self):
        """Return the model object with `.predict` method"""
        return self._get("model")

    @property
    def scaler(self):
        """Return the scaler object with `.transform` method"""
        return self._get("scaler")

    @property
    def featureset(self) -> List[str]:
        """Return the list of feature names"""
        return self._get("featureset")

    def _get(self, key: str):
        try:
            return self._model_dict[key]
        except KeyError:
            self._load_model()
            return self._get(key)

    def _load_model(self):

        if "dense" in self.modelname or self.modelname == "nn":
            self._is_voting_ensemble = False
            self._is_nn_model = True

        (
            self._model_dict["model"],
            self._model_dict["scaler"],
            self._model_dict["featureset"],
        ) = load_model(self.modelname, self._automatic_download, self._is_nn_model)

    def load_model(self):
        """Load the model and populate the namespace with the model objects."""
        self._load_model()

    @property
    def available_models(self) -> List[str]:
        """List all the available models."""
        return sorted(list(MODEL_CONFIG.keys()) + list(MODEL_DEFAULT_MAPPING.keys()))

    @property
    def feature_names(self) -> List[str]:
        """Get a list of feature names"""
        return get_feature_names(self.featureset)

    @property
    def default_mapping(self) -> Dict[str, str]:
        """Return the default mapping between model name and filename"""
        return MODEL_DEFAULT_MAPPING

    def __repr__(self):
        return "OximachineRunner (version: {}) with model {} (md5: {})".format(
            __version__, self.modelname, self.md5
        )

    def _make_predictions(  # pylint:disable=invalid-name
        self, feature_matrix: np.ndarray, num_samples: int = 100
    ) -> OrderedDict:
        """Makes predictions for a set of metal sites.
        Applies the scaler to the feature matrix.

        Args:
            feature_matrix (np.ndarray): feature matrix (two dimensional,
            metal sites in rows and features in columns)
            num_samples (int): Number of samples used for Dropout Monte-Carlo
                uncertainty estimation. Can only be used in Keras models with
                Dropout layers

        Returns:
            OrderedDict: predictions (this is the vote of the four base estimators),
                maximum probabilities of the base estimators, the prediction of each
                base estimator, standard deviation of the base predictions/dropout
                inference
        """
        feature_matrix_scaled = self.scaler.transform(feature_matrix)

        base_predictions = []
        max_probas = []
        std = []

        if self._is_nn_model:

            model_predictions = mode_std_predict_dropout(
                feature_matrix_scaled, self.model, num_samples
            )

            prediction = (model_predictions["prediction"] - 1).tolist()
            max_probas = self.model.predict_proba(feature_matrix_scaled)
            std = model_predictions["std"]
        if self._is_voting_ensemble:
            prediction = self.model.predict(feature_matrix_scaled).tolist()
            max_probas = np.max(self.model.predict_proba(feature_matrix_scaled), axis=1)
            _base_predictions = self.model._predict(  # pylint:disable=protected-access
                feature_matrix_scaled
            )

            for pred in _base_predictions:
                base_predictions.append(
                    [self.model.classes[prediction_index] for prediction_index in pred]
                )
            base_predictions = np.vstack(base_predictions)
            std = base_predictions.std(0)
            base_predictions = base_predictions.tolist()
        return OrderedDict(
            [
                ("prediction", prediction),
                ("max_probas", list(max_probas)),
                ("base_predictions", base_predictions),
                ("std", list(std)),
            ]
        )

    def _featurize_single(self, structure: Structure) -> Tuple[np.array, list, list]:
        """Finds metals in the structure, featurizes the metal sites and collects the features

        Args:
            structure (pymatgen.Structure): Structure to featurize

        Returns:
            Tuple[np.array, list, list]: Feature array, metal indices, metal symbols
        """
        feature_matrix, metal_indices, metals = featurize(structure, self.featureset)
        return feature_matrix, metal_indices, metals

    def run_oximachine(
        self,
        structure: Union[str, os.PathLike, Structure, Atoms],
        num_samples: int = 10,
    ) -> OrderedDict:
        """Runs oximachine after attempting to guess what structure is

        Args:
            structure (Union[str, os.PathLike, Structure, Atoms]):
                can be a `pymatgen.Structure`, `ase.Atoms` or a filepath as `str` or
                `os.PathLike`, which we then attempt to parse with pymatgen.
            num_samples (int): Number of samples used for Dropout Monte-Carlo
                uncertainty estimation. Can only be used in Keras models with
                Dropout layers
        Raises:
            ValueError: In case the format of structure is not implemented

        Returns:
            OrderedDict: with the keys metal_indices, metal_symbols,
                prediction, max_probas, base_predictions, std
        """

        if isinstance(structure, Structure):  # pylint:disable=no-else-return
            return self._run_oximachine(structure, num_samples)
        elif isinstance(structure, Atoms):
            pymatgen_structure = AseAtomsAdaptor.get_structure(structure)
            return self._run_oximachine(pymatgen_structure, num_samples)
        elif isinstance(structure, str):
            pymatgen_structure = Structure.from_file(structure)
            return self._run_oximachine(pymatgen_structure, num_samples)
        elif isinstance(structure, os.PathLike):
            pymatgen_structure = Structure.from_file(structure)
            return self._run_oximachine(pymatgen_structure, num_samples)
        else:
            raise ValueError(
                "Could not recognize structure! I can read Pymatgen structure objects,\
                ASE atom objects and a filepath in a fileformat that can be read by ase"
            )

    def _run_oximachine(
        self, structure: Structure, num_samples: int = 100
    ) -> OrderedDict:
        """Run the oximachine on one structure

        Args:
            structure (Structure): pymatgen Structure object
            num_samples (int): Number of samples used for Dropout Monte-Carlo
                uncertainty estimation. Can only be used in Keras models with
                Dropout layers

        Returns:
            OrderedDict: with the keys metal_indices, metal_symbols,
                prediction, max_probas, base_predictions, std
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            (
                feature_matrix,
                metal_indices,
                metal_symbols,
            ) = self._featurize_single(  # pylint:disable=protected-access
                structure
            )

            result = self._make_predictions(  # pylint:disable=protected-access
                feature_matrix, num_samples
            )

        return OrderedDict(
            [
                ("metal_indices", metal_indices),
                ("metal_symbols", metal_symbols),
                ("prediction", result["prediction"]),
                ("max_probas", result["max_probas"]),
                ("base_predictions", result["base_predictions"]),
                ("std", result["std"]),
            ]
        )
