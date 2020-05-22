import os
from typing import Union
from learnmofox import utils
from pymatgen import Structure
from .featurize import GetFeatures, FeatureCollector
from .utils import read_pickle
import numpy as np
import joblib
import sys


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL = joblib.load(os.path.join(THIS_DIR, "assets", "votingclassifier.joblib"))
SCALER = joblib.load(os.path.join(THIS_DIR, , "assets","scaler_0.joblib"))

# this is dirty but needed due to the way in which I wrote my model class and saved it.
# I can save it more clever in the future, but it works for now
sys.modules["utils"] = utils

# those global vars are for now hard coded for this model
METAL_CENTER_FEATURES = [
    "column",
    "row",
    "valenceelectrons",
    "diffto18electrons",
    "sunfilled",
    "punfilled",
    "dunfilled",
]
GEOMETRY_FEATURES = ["crystal_nn_fingerprint", "behler_parinello"]
CHEMISTRY_FEATURES = ["local_property_stats"]
FEATURES = CHEMISTRY_FEATURES + METAL_CENTER_FEATURES + ["crystal_nn_no_steinhardt"]


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


def _featurize_single(
    structure: pymatgen.Structure, feature_dir: str = ""
) -> Union[np.array, list, list]:
    """Finds metals in the structure, featurizes the metal sites and collects the features

    Args:
        structure (pymatgen.Structure): Structure to featurize
        feature_dir (str, optional): Directory to which features should be saved, can be useful if features should be reused. Defaults to "".

    Returns:
        Union[np.array, list, list]: [description]
    """
    gf = GetFeatures(structure, feature_dir)
    features = gf.return_features()
    metal_indices = gf.metal_indices
    X = []
    rl = FeatureCollector.create_dict_for_feature_table_from_dict(features)
    for f in rl:
        X.append(f["feature"])
    X = np.vstack(X)
    X, names = FeatureCollector._select_features_return_names(FEATURES, X)
    metals = [site.species_string for site in gf.metal_sites]
    return X, metal_indices, metals


def run_oximachine(cif: str) -> Union[list, list, list]:
    """Run the oximachine on one structure

    Args:
        cif (str): Filepath to cif 

    Returns:
        Union[list, list, list]: list of oxidation states, list of metal indices, 
        list of metal symbols
    """
    s = Structure.from_file(cif)
    X, metal_indices, metal_symbols = _featurize_single(cif)
    prediction = _make_predictions(X)

    return prediction, metal_indices, metal_symbols
