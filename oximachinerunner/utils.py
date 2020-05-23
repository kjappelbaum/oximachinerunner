# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
Some general utility functions for the oxidation state mining project
"""
from __future__ import absolute_import, print_function

import json
import os
import pickle
from collections.abc import Iterable
from pathlib import Path

import numpy as np
from pymatgen.core import Element


def read_pickle(filepath: str):
    """Does what it says. Nothing more and nothing less. Takes a pickle file path and unpickles it"""
    with open(filepath, 'rb') as fh:  # pylint: disable=invalid-name
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


class SymbolNameDict:
    """
    Parses the periodic table json and returns  a dictionary with symbol: longname
    """

    def __init__(self):
        with open(
                os.path.join(Path(__file__).absolute().parent, 'assets', 'periodic_table.json'),
                'r',
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
                    self.symbol_name_dict[key] = value['Name'].lower()
            else:
                self.symbol_name_dict[key] = value['Name'].lower()

        return self.symbol_name_dict
