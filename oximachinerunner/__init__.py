# -*- coding: utf-8 -*-
# pylint:disable=wrong-import-position
"""Implements methods to use oximachine as part of a Python package"""
import os
import sys
import warnings

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
from .errors import FeaturizationError, ParsingError, PredictionError
from .utils import download_model, has_metal_sites, model_exists

__version__ = get_versions()["version"]
del get_versions
sys.modules["learnmofox"] = learnmofox

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

__all__ = ["OximachineRunner"]


EMPTY_PREDICTION = OrderedDict(
    [
        ("metal_indices", []),
        ("metal_symbols", []),
        ("prediction", []),
        ("max_probas", []),
        ("base_predictions", []),
    ]
)


def _load_file(
    path, md5: str, url: str, automatic_download: bool = True
) -> object:  # pylint:disable=inconsistent-return-statements
    """[summary]

    Args:
        path (str, PathLike): Path of the model file
        md5 (str): md5 hash of the model file
        url (str): url to download the file from
        automatic_download (bool): If true, it automatically downloads
            the file if it is not available

    Raises:
        FileNotFoundError: If automatic_download is not enabled and the file
            is not on the disk

    Returns:
        model, typically a sklearn estimator object
    """
    if model_exists(path, md5):  # pylint:disable=no-else-return

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
        return _load_file(path, md5, url, automatic_download)


def load_model(modelname: str, automatic_download: bool = True) -> Tuple:
    """Orchestrates the loading of the model and the scaler

    Args:
        modelname (str): name of the model
        automatic_download (bool): if true,
            it will attempt to automatically download the model

    Raises:
        ValueError: if the modelname is not defined in the configuration

    Returns:
        model, scaler, featurenames
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Check if one default model was selected
        if modelname == "all":
            modelname = MODEL_DEFAULT_MAPPING["all"]
        if modelname == "mof":
            modelname = MODEL_DEFAULT_MAPPING["mof"]

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

        model = _load_file(modelpath, modelmd5, modelurl, automatic_download)
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
        (
            self._model_dict["model"],
            self._model_dict["scaler"],
            self._model_dict["featureset"],
        ) = load_model(self.modelname, self._automatic_download)

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
        self, feature_matrix: np.ndarray
    ) -> Tuple[list, list, list]:
        """Makes predictions for a set of metal sites.
        Applies the scaler to the feature matrix.

        Args:
            feature_matrix (np.ndarray): feature matrix (two dimensional,
            metal sites in rows and features in columns)

        Raises:
            PredictionError: For possible exceptions when running the model.

        Returns:
            Tuple[list, list, list]: predictions (this is the vote of the four base estimators),
                maximum probabilities of the base estimators, the prediction of each
                base estimator
        """
        try:
            feature_matrix_scaled = self.scaler.transform(feature_matrix)
            prediction = self.model.predict(feature_matrix_scaled)

            max_probas = np.max(self.model.predict_proba(feature_matrix_scaled), axis=1)
            _base_predictions = self.model._predict(  # pylint:disable=protected-access
                feature_matrix_scaled
            )

            base_predictions = []
            for pred in _base_predictions:
                base_predictions.append(
                    [self.model.classes[prediction_index] for prediction_index in pred]
                )
            return list(prediction), list(max_probas), list(base_predictions)
        except Exception as exception:
            raise PredictionError(
                "Could not make predictions for structure."
            ) from exception

    def _featurize_single(self, structure: Structure) -> Tuple[np.array, list, list]:
        """Finds metals in the structure, featurizes the metal sites and collects the features

        Args:
            structure (pymatgen.Structure): Structure to featurize

        Raises:
            FeaturizationError: Raised for all kinds of errors that might occurr when
                featurizing the structure

        Returns:
            Tuple[np.array, list, list]: Feature array, metal indices, metal symbols
        """
        try:
            feature_matrix, metal_indices, metals = featurize(
                structure, self.featureset
            )
            return feature_matrix, metal_indices, metals
        except Exception as exception:
            raise FeaturizationError("Could not featurize structure.") from exception

    def run_oximachine(
        self, structure: Union[str, os.PathLike, Structure, Atoms]
    ) -> OrderedDict:
        """Runs oximachine after attempting to guess what structure is

        Args:
            structure (Union[str, os.PathLike, Structure, Atoms]):
            can be a `pymatgen.Structure`, `ase.Atoms` or a filepath as `str` or
            `os.PathLike`, which we then attempt to parse with pymatgen.

        Raises:
            ParsingError: In case the format of structure is not implemented or in
                case we cannot convert the input into a pymatgen Structure object.
            FeaturizationError: In case the featurization fails.
            PredictionError: In case the prediction fails.

        Returns:
            OrderedDict: with the keys metal_indices, metal_symbols,
                prediction, max_probas, base_predictions
        """

        if isinstance(structure, Structure):  # pylint:disable=no-else-return
            return self._run_oximachine(structure)
        elif isinstance(structure, Atoms):
            try:
                pymatgen_structure = AseAtomsAdaptor.get_structure(structure)
            except Exception as exception:
                raise ParsingError(
                    "Could not convert structure into a pymatgen Structure object."
                ) from exception
            return self._run_oximachine(pymatgen_structure)
        elif isinstance(structure, str):
            try:
                pymatgen_structure = Structure.from_file(structure)
            except Exception as exception:
                raise ParsingError(
                    "Could not convert structure into a pymatgen Structure object."
                ) from exception
            return self._run_oximachine(pymatgen_structure)
        elif isinstance(structure, os.PathLike):
            try:
                pymatgen_structure = Structure.from_file(structure)
            except Exception as exception:
                raise ParsingError(
                    "Could not convert structure into a pymatgen Structure object."
                ) from exception
            return self._run_oximachine(pymatgen_structure)
        else:
            raise ParsingError(
                "Could not recognize structure! I can read Pymatgen structure objects,\
                ASE atom objects and a filepath in a file format that can be read by ase"
            )

    def _run_oximachine(self, structure: Structure) -> OrderedDict:
        """Run the oximachine on one structure

        Args:
            structure (Structure): pymatgen Structure object

        Returns:
            OrderedDict: with the keys metal_indices, metal_symbols,
                prediction, max_probas, base_predictions
        """
        if not has_metal_sites(structure):
            warnings.warn(
                "Oximachine can only predict oxidation states of metals. \
                    This structure contains no metals."
            )
            return EMPTY_PREDICTION

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            (
                feature_matrix,
                metal_indices,
                metal_symbols,
            ) = self._featurize_single(  # pylint:disable=protected-access
                structure
            )

            (
                prediction,
                max_probas,
                base_predictions,
            ) = self._make_predictions(  # pylint:disable=protected-access
                feature_matrix
            )

        return OrderedDict(
            [
                ("metal_indices", metal_indices),
                ("metal_symbols", metal_symbols),
                ("prediction", prediction),
                ("max_probas", max_probas),
                ("base_predictions", base_predictions),
            ]
        )
