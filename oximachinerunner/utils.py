# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
Some general utility functions for the oxidation state mining project
"""

import hashlib
import json
import os
import pickle
import urllib
from collections.abc import Iterable
from functools import partial
from pathlib import Path
from typing import Union

import numpy as np
from pymatgen.core import Element

from .config import MODEL_CONFIG


def md5sum(filename: Union[str, Path]):
    """Gets the md5 hash of a file"""
    with open(filename, "rb") as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b""):
            d.update(buf)
    return d.hexdigest()


def model_exists(path: Union[Path, str], md5: str):
    """Checks whether a model if the expected md5 hash
    exists at the path"""
    is_exist = False
    if os.path.exists(path):
        this_file_md5 = md5sum(path)
        if this_file_md5 == md5:
            is_exist = True

    return is_exist


def cbk_for_urlretrieve(a, b, c):
    """
    Callback function for showing process
    """
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print("\r%.1f%% of %.2fM" % (per, c / (1024 * 1024)), end="")


def download_model(url: str, destination: Union[Path, str], md5: str):
    """Downloads file from url to destination
        and checks md5 hash

    Args:
        url (str): URL
        destination (Union[Path, str]): Path to which the downloaded file
            will be saved
        md5 (str): Expected md5 hash

    Raises:
        Exception: [description]
        Exception: [description]
    """
    if not model_exists(destination, md5):
        print("{} does not exist or md5 is wrong.".format(destination))
        print("Download file from {}".format(url))
        try:
            basedir = Path(destination).parent
            if not os.path.exists(basedir):
                os.makedirs(basedir)
            urllib.request.urlretrieve(url, destination, cbk_for_urlretrieve)
            this_file_md5 = md5sum(destination)
            if this_file_md5 == md5:
                print("\nDownload {} file successfully.".format(destination))
            else:
                raise Exception("Md5 wrong.")
        except Exception as error:
            infos = "[Error]: Download from {} failed due to {}".format(url, error)
            raise Exception(infos) from error


def download_all():
    """Download model and scaler"""
    for _, v in MODEL_CONFIG.items():
        download_model(v["scaler"]["url"], v["scaler"]["path"], v["scaler"]["md5"])
        download_model(
            v["classifier"]["url"], v["classifier"]["path"], v["classifier"]["md5"]
        )


def read_pickle(filepath: str):
    """Does what it says. Nothing more and nothing less.
    Takes a pickle file path and unpickles it"""
    with open(filepath, "rb") as fh:  # pylint: disable=invalid-name
        result = pickle.load(fh)  # pylint: disable=invalid-name
    return result


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


def diff_to_18e(nvalence):
    """The number of electrons to donate to achieve 18 electrons might be an interesting descriptor,
    though there are more stable electron configurations"""
    return min(np.abs(nvalence - 18), nvalence)


class SymbolNameDict:  # pylint: disable=too-few-public-methods
    """Parses the periodic table json and returns a dictionary with symbol: longname"""

    def __init__(self):
        with open(
            os.path.join(
                Path(__file__).absolute().parent, "assets", "periodic_table.json"
            ),
            "r",
        ) as periodic_table_file:
            self.pt_data = json.load(periodic_table_file)
        self.symbol_name_dict = {}

    def get_symbol_name_dict(self, only_metal=True):
        """
        Iterates over keys and returns the symbol: name dict.
        """
        for key, value in self.pt_data.items():
            if only_metal:
                if Element(key).is_metal:
                    self.symbol_name_dict[key] = value["Name"].lower()
            else:
                self.symbol_name_dict[key] = value["Name"].lower()

        return self.symbol_name_dict


def has_metal_sites(structure):
    """Returns True if there is a metal in the structure."""
    metal_sites = []
    for _, site in enumerate(structure):
        if site.species.elements[0].is_metal:
            metal_sites.append(site)

    return len(metal_sites) > 0
