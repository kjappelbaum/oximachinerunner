# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""
Some general utility functions for the oxidation state mining project
"""
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import os
import warnings
from pathlib import Path
import json
import pickle
from collections.abc import Iterable
from tqdm import tqdm
from pymatgen.core import Element
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler
import numpy as np
from apricot import FacilityLocationSelection


def read_pickle(filepath: str):
    """Does what it says. Nothing more and nothing less. Takes a pickle file path and unpickles it"""
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


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def diff_to_18e(nvalence):
    """The number of electrons to donate to achieve 18 electrons might be an interesting descriptor,
    though there are more stable electron configurations"""
    return min(np.abs(nvalence - 18), nvalence)


def apricot_select(data, k, standardize=True, chunksize=20000):
    """Does 'farthest point sampling' with apricot.
    For memory limitation reasons it is chunked with a hardcoded chunksize. """
    if standardize:
        print("standardizing data")
        data = StandardScaler().fit_transform(data)

    data = data.astype(np.float64)

    num_chunks = int(data.shape[0] / chunksize)

    if num_chunks > 1:
        chunksize = int(data.shape[0] / num_chunks)
    else:
        num_chunks = 1
        chunksize = len(data)

    # This assumes shuffled data and is used to make stuff a bit less
    # memory intensive
    chunklist = []

    to_select = int(k / num_chunks)

    print(("Will use {} chunks of size {}".format(num_chunks, chunksize)))
    num_except = 0

    for d_ in tqdm(chunks(data, chunksize)):
        print(("Current chunk has size {}".format(len(d_))))
        if len(d_) > to_select:  # otherwise it makes no sense to select something
            try:
                X_subset = FacilityLocationSelection(to_select).fit_transform(d_)
                chunklist.append(X_subset)
            except Exception:  # pylint:disable=broad-except
                num_except += 1
                if num_except > 1:  # pylint:disable=no-else-return
                    warnings.warn(
                        "Could not perform diverse set selection for two attempts, will perform random choice")
                    return np.random.choice(len(data), k, replace=False)
                else:
                    print("will use greedy select now")
                    X_subset = _greedy_loop(d_, to_select, "euclidean")
                    chunklist.append(X_subset)
    greedy_indices = []
    subset = np.vstack(chunklist)

    print((subset.shape))
    for d in subset:
        index = np.where(np.all(data == d, axis=1))[0][0]
        greedy_indices.append(index)

    del data
    del subset

    output = list(set(greedy_indices))
    print((len(output)))
    return output


def _greedy_loop(remaining, k, metric):
    """Doing it chunked"""
    greedy_data = np.zeros((k, remaining.shape[1]))

    greedy_index = np.random.randint(0, len(remaining))
    greedy_data[0] = remaining[greedy_index]
    remaining = np.delete(remaining, greedy_index, 0)

    for i in range(int(k) - 1):
        dist = distance.cdist(remaining, greedy_data, metric)
        greedy_index = np.argmax(np.argmax(np.min(dist, axis=0)))

        greedy_data[i + 1] = remaining[greedy_index]
        remaining = np.delete(remaining, greedy_index, 0)

    return greedy_data


def _greedy_farthest_point_samples_non_chunked(data,
                                               k: int,
                                               metric: str = "euclidean",
                                               standardize: bool = True) -> list:
    """
        Args:
            data (np.array)
            k (int)
            metric (string): metric to use for the distance, can be one from
                https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
                defaults to euclidean
            standardize (bool): flag that indicates whether features are standardized prior to sampling
        Returns:
            list with the sampled names
            list of indices
    """

    data = data.astype(np.float32)

    if standardize:
        data = StandardScaler().fit_transform(data)

    greedy_data = []

    index = np.random.randint(0, len(data) - 1)
    greedy_data.append(data[index])
    remaining = np.delete(data, index, 0)

    _greedy_loop(remaining, k, metric)

    greedy_indices = []
    for d in greedy_data:
        greedy_indices.append(np.array(np.where(np.all(data == d, axis=1)))[0])

    greedy_indices = np.concatenate(greedy_indices).ravel()

    return list(flatten(greedy_indices))


def greedy_farthest_point_samples(
    data,
    k: int,
    metric: str = "euclidean",
    standardize: bool = True,
    chunked: bool = False,
) -> list:
    """
        Args:
            data (np.array)
            k (int)
            metric (string): metric to use for the distance, can be one from
                https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
                defaults to euclidean
            standardize (bool): flag that indicates whether features are standardized prior to sampling
        Returns:
            list with the sampled names
            list of indices
    """
    if chunked:
        result = _greedy_farthest_point_samples_chunked(data, k, metric, standardize)

    else:
        result = _greedy_farthest_point_samples_non_chunked(data, k, metric, standardize)

    return result


def _greedy_farthest_point_samples_chunked(data, k: int, metric: str = "euclidean", standardize: bool = True) -> list:
    """
        Args:
            data (np.array)
            k (int)
            metric (string): metric to use for the distance, can be one from
                https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html
                defaults to euclidean
            standardize (bool): flag that indicates whether features are standardized prior to sampling
        Returns:
            list with the sampled names
            list of indices
    """

    data = data.astype(np.float32)

    if standardize:
        data = StandardScaler().fit_transform(data)

    greedy_data = []

    num_chunks = int(data.shape[0] * data.shape[1] / 100000)
    chunksize = int(data.shape[0] / num_chunks)

    # This assumes shuffled data and is used to make stuff a bit less
    # memory intensive
    i = 0
    for d_ in chunks(data, chunksize):
        print(("chunk {} out of {}".format(i, num_chunks)))
        d = d_
        if len(d) > 2:
            index = np.random.randint(0, len(d) - 1)
            greedy_data.append(d[index])
            remaining = np.delete(d, index, 0)

            for _ in range(int(k / num_chunks) - 1):
                dist = distance.cdist(remaining, greedy_data, metric)
                greedy_index = np.argmax(np.argmax(np.min(dist, axis=0)))
                greedy_data.append(remaining[greedy_index])
                remaining = np.delete(remaining, greedy_index, 0)
        else:
            greedy_data.append(d)

        i += 1
    greedy_indices = []

    for d in greedy_data:
        greedy_indices.append(np.array(np.where(np.all(data == d, axis=1)))[0])

    greedy_indices = np.concatenate(greedy_indices).ravel()

    return list(flatten(greedy_indices))


class SymbolNameDict:
    """
    Parses the periodic table json and returns  a dictionary with symbol: longname
    """

    def __init__(self):
        with open(
                os.path.join(Path(__file__).absolute().parent, "assets", "periodic_table.json"),
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
