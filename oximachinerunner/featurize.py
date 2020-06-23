# -*- coding: utf-8 -*-
# pylint:disable=invalid-name, logging-format-interpolation, logging-fstring-interpolation, line-too-long, dangerous-default-value, too-many-lines, anomalous-backslash-in-string
"""Featurization functions for the oxidation state mining project. Wrapper around matminer"""
from __future__ import absolute_import, print_function

import logging
import os
import pickle
import warnings
from glob import glob
from pathlib import Path
# from collections import defaultdict
from typing import List, Tuple, Union

import numpy as np
import pandas as pd
from ase.io import read
from matminer.featurizers.base import BaseFeaturizer, MultipleFeaturizer
from matminer.featurizers.site import CrystalNNFingerprint, GaussianSymmFunc
from matminer.utils.caching import get_nearest_neighbors
from matminer.utils.data import MagpieData
from pymatgen.analysis.local_env import VoronoiNN
from pymatgen.core import Element
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.cif import CifParser

from .utils import diff_to_18e, read_pickle

PathType = Union[str, bytes, os.PathLike]

warnings.simplefilter('ignore')

extra_test_set: List = []

collectorlogger = logging.getLogger('FeatureCollector')
collectorlogger.setLevel(logging.INFO)
logging.basicConfig(format='%(filename)s: %(message)s', level=logging.DEBUG)

FEATURE_RANGES_DICT = {
    'crystal_nn_fingerprint': [(0, 61)],
    'crystal_nn_no_steinhardt': [(0, 33), (36, 37), (40, 41), (44, 46), (49, 61)],
    'local_property_stats': [(61, 121)],
    'column_differences': [(62, 63), (77, 78), (92, 93), (107, 108)],
    'row_differences': [(63, 64), (78, 79), (93, 94), (108, 109)],
    'electronegativity_differences': [(64, 65), (79, 80), (94, 95), (109, 110)],
    'valence_differences': [(69, 70), (84, 85), (99, 100), (114, 115)],
    'unfilled_differences': [(74, 75), (89, 90), (104, 105), (119, 120)],
    'nsvalence_differences': [(65, 66), (79, 80), (95, 96), (110, 111)],
    'behler_parinello': [(121, 129)],
    'number': [(129, 130)],
    'row': [(130, 131)],
    'column': [(131, 132)],
    'valenceelectrons': [(132, 133)],
    'diffto18electrons': [(133, 134)],
    'sunfilled': [(134, 135)],
    'punfilled': [(135, 136)],
    'dunfilled': [(136, 137)],
    'random_column': [(137, 138)],
    'optimized_feature_set': [
        (0, 33),
        (36, 37),
        (40, 41),
        (44, 46),
        (49, 61),
        (130, 131),
        (131, 132),
        (76, 90),
    ],
}

FEATURE_LABELS_ALL = [
    'wt CN_1',
    'sgl_bd CN_1',
    'wt CN_2',
    'L-shaped CN_2',
    'water-like CN_2',
    'bent 120 degrees CN_2',
    'bent 150 degrees CN_2',
    'linear CN_2',
    'wt CN_3',
    'trigonal planar CN_3',
    'trigonal non-coplanar CN_3',
    'T-shaped CN_3',
    'wt CN_4',
    'square co-planar CN_4',
    'tetrahedral CN_4',
    'rectangular see-saw-like CN_4',
    'see-saw-like CN_4',
    'trigonal pyramidal CN_4',
    'wt CN_5',
    'pentagonal planar CN_5',
    'square pyramidal CN_5',
    'trigonal bipyramidal CN_5',
    'wt CN_6',
    'hexagonal planar CN_6',
    'octahedral CN_6',
    'pentagonal pyramidal CN_6',
    'wt CN_7',
    'hexagonal pyramidal CN_7',
    'pentagonal bipyramidal CN_7',
    'wt CN_8',
    'body-centered cubic CN_8',
    'hexagonal bipyramidal CN_8',
    'wt CN_9',
    'q2 CN_9',
    'q4 CN_9',
    'q6 CN_9',
    'wt CN_10',
    'q2 CN_10',
    'q4 CN_10',
    'q6 CN_10',
    'wt CN_11',
    'q2 CN_11',
    'q4 CN_11',
    'q6 CN_11',
    'wt CN_12',
    'cuboctahedral CN_12',
    'q2 CN_12',
    'q4 CN_12',
    'q6 CN_12',
    'wt CN_13',
    'wt CN_14',
    'wt CN_15',
    'wt CN_16',
    'wt CN_17',
    'wt CN_18',
    'wt CN_19',
    'wt CN_20',
    'wt CN_21',
    'wt CN_22',
    'wt CN_23',
    'wt CN_24',
    'local difference in MendeleevNumber',
    'local difference in Column',
    'local difference in Row',
    'local difference in Electronegativity',
    'local difference in NsValence',
    'local difference in NpValence',
    'local difference in NdValence',
    'local difference in NfValence',
    'local difference in NValence',
    'local difference in NsUnfilled',
    'local difference in NpUnfilled',
    'local difference in NdUnfilled',
    'local difference in NfUnfilled',
    'local difference in NUnfilled',
    'local difference in GSbandgap',
    'local signed difference in MendeleevNumber',
    'local signed difference in Column',
    'local signed difference in Row',
    'local signed difference in Electronegativity',
    'local signed difference in NsValence',
    'local signed difference in NpValence',
    'local signed difference in NdValence',
    'local signed difference in NfValence',
    'local signed difference in NValence',
    'local signed difference in NsUnfilled',
    'local signed difference in NpUnfilled',
    'local signed difference in NdUnfilled',
    'local signed difference in NfUnfilled',
    'local signed difference in NUnfilled',
    'local signed difference in GSbandgap',
    'maximum local difference in MendeleevNumber',
    'maximum local difference in Column',
    'maximum local difference in Row',
    'maximum local difference in Electronegativity',
    'maximum local difference in NsValence',
    'maximum local difference in NpValence',
    'maximum local difference in NdValence',
    'maximum local difference in NfValence',
    'maximum local difference in NValence',
    'maximum local difference in NsUnfilled',
    'maximum local difference in NpUnfilled',
    'maximum local difference in NdUnfilled',
    'maximum local difference in NfUnfilled',
    'maximum local difference in NUnfilled',
    'maximum local difference in GSbandgap',
    'mimum local difference in MendeleevNumber',
    'mimum local difference in Column',
    'mimum local difference in Row',
    'mimum local difference in Electronegativity',
    'mimum local difference in NsValence',
    'mimum local difference in NpValence',
    'mimum local difference in NdValence',
    'mimum local difference in NfValence',
    'mimum local difference in NValence',
    'mimum local difference in NsUnfilled',
    'mimum local difference in NpUnfilled',
    'mimum local difference in NdUnfilled',
    'mimum local difference in NfUnfilled',
    'mimum local difference in NUnfilled',
    'mimum local difference in GSbandgap',
    'G2_0.05',
    'G2_4.0',
    'G2_20.0',
    'G2_80.0',
    'G4_0.005_1.0_1.0',
    'G4_0.005_1.0_-1.0',
    'G4_0.005_4.0_1.0',
    'G4_0.005_4.0_-1.0',
    'number',
    'row',
    'column',
    'valenceelectrons',
    'diffto18electrons',
    'sunfilled',
    'punfilled',
    'dunfilled',
    'random_column',
]

SELECTED_RACS = [
    'D_mc-I-0-all',
    'D_mc-I-1-all',
    'D_mc-I-2-all',
    'D_mc-I-3-all',
    'D_mc-S-0-all',
    'D_mc-S-1-all',
    'D_mc-S-2-all',
    'D_mc-S-3-all',
    'D_mc-T-0-all',
    'D_mc-T-1-all',
    'D_mc-T-2-all',
    'D_mc-T-3-all',
    'D_mc-Z-0-all',
    'D_mc-Z-1-all',
    'D_mc-Z-2-all',
    'D_mc-Z-3-all',
    'D_mc-chi-0-all',
    'D_mc-chi-1-all',
    'D_mc-chi-2-all',
    'D_mc-chi-3-all',
    'mc-I-0-all',
    'mc-I-1-all',
    'mc-I-2-all',
    'mc-I-3-all',
    'mc-S-0-all',
    'mc-S-1-all',
    'mc-S-2-all',
    'mc-S-3-all',
    'mc-T-0-all',
    'mc-T-1-all',
    'mc-T-2-all',
    'mc-T-3-all',
    'mc-Z-0-all',
    'mc-Z-1-all',
    'mc-Z-2-all',
    'mc-Z-3-all',
    'mc-chi-0-all',
    'mc-chi-1-all',
    'mc-chi-2-all',
    'mc-chi-3-all',
]


class LocalPropertyStats(BaseFeaturizer):
    """
    Differences, minima and maxima in elemental properties between site and its neighboring sites.

    Uses the Voronoi tessellation of the structure to determine the
    neighbors of the site, and assigns each neighbor (:math:`n`) a
    weight (:math:`A_n`) that corresponds to the area of the facet
    on the tessellation corresponding to that neighbor.
    The local property difference is then computed by
    :math:`\\frac{\sum_n {A_n |p_n - p_0|}}{\sum_n {A_n}}`
    where :math:`p_n` is the property (e.g., atomic number) of a neighbor
    and :math:`p_0` is the property of a site. If signed parameter is assigned
    True, signed difference of the properties is returned instead of absolute
    difference.

    Features:
        - "local property stat in [property]"

    References:
         `Ward et al. _PRB_ 2017 <http://link.aps.org/doi/10.1103/PhysRevB.96.024104>`_
    """

    def __init__(self, data_source=MagpieData(), weight='area', properties=('Electronegativity',)):
        """ Initialize the featurizer

        Args:
            data_source (AbstractData) - Class from which to retrieve
                elemental properties
            weight (str) - What aspect of each voronoi facet to use to
                weigh each neighbor (see VoronoiNN)
            properties ([str]) - List of properties to use (default=['Electronegativity'])
            signed (bool) - whether to return absolute difference or signed difference of
                            properties(default=False (absolute difference))
        """
        self.data_source = data_source
        self.properties = properties
        self.weight = weight

    @staticmethod
    def from_preset(preset):
        """
        Create a new LocalPropertyStats class according to a preset

        Args:
            preset (str) - Name of preset
        """

        if preset == 'interpretable':  # pylint:disable=no-else-return
            return LocalPropertyStats(
                data_source=MagpieData(),
                properties=[
                    'MendeleevNumber',
                    'Column',
                    'Row',
                    'Electronegativity',
                    'NsValence',
                    'NpValence',
                    'NdValence',
                    'NfValence',
                    'NValence',
                    'NsUnfilled',
                    'NpUnfilled',
                    'NdUnfilled',
                    'NfUnfilled',
                    'NUnfilled',
                    'GSbandgap',
                ],
            )
        else:
            raise ValueError('Unrecognized preset: ' + preset)

    def featurize(self, strc, idx):  # pylint:disable=arguments-differ
        # Get the targeted site
        my_site = strc[idx]

        # Get the tessellation of a site
        nn = get_nearest_neighbors(VoronoiNN(weight=self.weight), strc, idx)

        # Get the element and weight of each site
        elems = [n['site'].specie for n in nn]
        weights = [n['weight'] for n in nn]

        # Compute the difference for each property
        output = np.zeros((len(self.properties),))
        output_signed = np.zeros((len(self.properties),))
        output_max = np.zeros((len(self.properties),))
        output_min = np.zeros((len(self.properties),))

        total_weight = np.sum(weights)
        for i, p in enumerate(self.properties):
            my_prop = self.data_source.get_elemental_property(my_site.specie, p)
            n_props = self.data_source.get_elemental_properties(elems, p)
            output[i] = (np.dot(weights, np.abs(np.subtract(n_props, my_prop))) / total_weight)
            output_signed[i] = (np.dot(weights, np.subtract(n_props, my_prop)) / total_weight)
            output_max[i] = np.max(np.subtract(n_props, my_prop))
            output_min[i] = np.min(np.subtract(n_props, my_prop))
        return np.hstack([output, output_signed, output_max, output_min])

    def feature_labels(self):

        return (['local difference in ' + p for p in self.properties] +
                ['local signed difference in ' + p for p in self.properties] +
                ['maximum local difference in ' + p for p in self.properties] +
                ['minimum local difference in ' + p for p in self.properties])

    def citations(self):
        return [
            '@article{Ward2017,'
            'author = {Ward, Logan and Liu, Ruoqian '
            'and Krishna, Amar and Hegde, Vinay I. '
            'and Agrawal, Ankit and Choudhary, Alok '
            'and Wolverton, Chris},'
            'doi = {10.1103/PhysRevB.96.024104},'
            'journal = {Physical Review B},'
            'pages = {024104},'
            'title = {{Including crystal structure attributes '
            'in machine learning models of formation energies '
            'via Voronoi tessellations}},'
            'url = {http://link.aps.org/doi/10.1103/PhysRevB.96.014107},'
            'volume = {96},year = {2017}}',
            '@article{jong_chen_notestine_persson_ceder_jain_asta_gamst_2016,'
            'title={A Statistical Learning Framework for Materials Science: '
            'Application to Elastic Moduli of k-nary Inorganic Polycrystalline Compounds}, '
            'volume={6}, DOI={10.1038/srep34256}, number={1}, journal={Scientific Reports}, '
            'author={Jong, Maarten De and Chen, Wei and Notestine, Randy and Persson, '
            'Kristin and Ceder, Gerbrand and Jain, Anubhav and Asta, Mark and Gamst, Anthony}, '
            'year={2016}, month={Mar}}',
        ]

    def implementors(self):
        return ['Kevin Jablonka']


class GetFeatures:
    """Featurizer"""

    def __init__(self, structure, outpath):
        """Generates features for a list of structures

        Args:
            structure
            outpath (str): path to which the features will be dumped

        Returns:

        """
        featurizelogger = logging.getLogger('Featurize')
        featurizelogger.setLevel(logging.INFO)
        logging.basicConfig(
            # filename="featurize.log",
            format='%(filename)s: %(message)s',
            level=logging.INFO,
        )

        self.outpath = outpath
        self.logger = featurizelogger
        self.path = None
        self.structure = structure
        self.metal_sites = []
        self.metal_indices = []
        self.features = []
        if self.path is not None:
            self.outname = os.path.join(self.outpath, ''.join([Path(self.path).stem, '.pkl']))
        else:
            self.outname = os.path.join(
                self.outpath,
                ''.join([self.structure.formula.replace(' ', '_'), '.pkl']),
            )
        self.featurizer = MultipleFeaturizer([
            CrystalNNFingerprint.from_preset('ops'),
            LocalPropertyStats.from_preset('interpretable'),
            GaussianSymmFunc(),
        ])

    @classmethod
    def from_file(cls, structurepath, outpath):
        """
        Construct a featurizer class from path to structure and an output path
        """
        s = GetFeatures.read_safe(structurepath)
        featureclass = cls(s, outpath)
        featureclass.path = structurepath
        featureclass.outname = os.path.join(featureclass.outpath, ''.join([Path(featureclass.path).stem, '.pkl']))
        return featureclass

    @classmethod
    def from_string(cls, structurestring, outpath):
        """
        Constructure for the webapp
        """

        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            try:
                cp = CifParser.from_string(structurestring)
                s = cp.get_structures()[0]
            except Exception:
                raise ValueError('Pymatgen could not parse ciffile')
            else:
                return cls(s, outpath)

    @staticmethod
    def read_safe(path):
        """Fail early

        Returns:
            bool: True if check ok (if pymatgen can load structure)

        """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            try:
                atoms = read(path)
                structure = AseAtomsAdaptor.get_structure(atoms)  # ase parser is a bit more robust
                return structure
            except Exception:  # pylint: disable=broad-except
                raise ValueError('Could not read structure')

    def get_metal_sites(self):
        """Stores all metal sites of structure  to list"""
        for idx, site in enumerate(self.structure):
            if site.species.elements[0].is_metal:
                self.metal_sites.append(site)
                self.metal_indices.append(idx)

    def get_feature_vectors(self, site):
        """Runs matminer on one site"""

        X = self.featurizer.featurize(self.structure, site)

        return X

    def dump_features(self):
        """Dumps all the features into one pickle file"""
        with open(self.outname, 'wb') as filehandle:
            pickle.dump(list(self.features), filehandle)

    def return_features(self):
        """Runs featurization and return np array with features.
        """
        self.get_metal_sites()
        try:
            self.logger.debug('iterating over {} metal sites'.format(len(self.metal_sites)))
            for idx, metal_site in enumerate(self.metal_sites):
                self.features.append({
                    'metal': metal_site.species_string,
                    'feature': self.get_feature_vectors(self.metal_indices[idx]),
                    'coords': metal_site.coords,
                })
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error('could not featurize because of {}'.format(e))

        return self.features

    def run_featurization(self):
        """loops over sites if check ok"""
        self.get_metal_sites()
        try:
            self.logger.debug('iterating over {} metal sites'.format(len(self.metal_sites)))
            for idx, metal_site in enumerate(self.metal_sites):
                self.features.append({
                    'metal': metal_site.species_string,
                    'feature': self.get_feature_vectors(self.metal_indices[idx]),
                    'coords': metal_site.coords,
                })
            self.dump_features()
        except Exception as e:  # pylint: disable=broad-except
            self.logger.error('could not featurize {} because of {}'.format(self.path, e))


class FeatureCollector:  # pylint:disable=too-many-instance-attributes,too-many-locals
    """convert features from a folder of pickle files to three
    pickle files for feature matrix, label vector and names list. """

    def __init__(  # pylint:disable=too-many-arguments
        self,
        inpath: PathType = None,
        labelpath: PathType = None,
        outdir_labels: PathType = 'data/labels',
        outdir_features: PathType = 'data/features',
        outdir_helper: PathType = 'data/helper',
        percentage_holdout: float = 0,
        outdir_holdout: PathType = None,
        forbidden_picklepath: PathType = 'data/helper/two_ox_states.pkl',
        exclude_dir: PathType = '../test_structures/showcases',
        selected_features: list = [
            'crystal_nn_fingerprint',
            'ward_prb',
            'bond_orientational',
            'behler_parinello',
        ],
        old_format: bool = False,
        training_set_size: int = None,
        racsfile: PathType = None,
        selectedracs: list = SELECTED_RACS,
        drop_duplicates: bool = True,
    ):
        """Initializes a feature collector.

        WARNING! The fingerprint selection function assumes that the full feature vector in the
        pickle files has the columns as specified in FEATURE_LABELS_ALL

        Keyword Arguments:
            inpath {PathType} -- path to directory with one pickle file per structure (default: {None})
            labelpath {PathType} -- path to picklefile with labels (default: {None})
            outdir_labels {PathType} -- path to output directory for labelsfile (default: {"data/labels"})
            outdir_features {PathType} -- path to output directory for featuresfile (default: {"data/features"})
            outdir_helper {PathType} -- path to output directory for helper files (feature names, structure names) (default: {"data/helper"})
            percentage_holdout {float} -- precentage of all the data that should be put away as holdout
            outdir_holdout {PathType} -- directory into which the files for the holdout set are written (names, X and y)
            forbidden_picklepath {PathType} -- path to picklefile with list of forbidden CSD names (default: {"/home/kevin/Dropbox/proj62_guess_oxidation_states/machine_learn_oxstates/data/helper/two_ox_states.pkl"})
            exclude_dir {PathType} -- path to directory with structure names are forbidden as well (default: {"/home/kevin/Dropbox (LSMO)/proj62_guess_oxidation_states/test_structures/showcases"})
            selected_features {list} -- list of selected features. Available crystal_nn_fingerprint, cn, ward_prb, bond_orientational, behler_parinello
              (default: {["crystal_nn_fingerprint","ward_prd","bond_orientational","behler_parinello",]})
            old_format {bool} -- if True, it uses the old feature dictionary style (default: {True})
            training_set_size {int} -- if set to an int, it set an upper limit of the number of training points and uses farthest point sampling to select them
            racsfile {PathType} -- path to file with
            selectedracs {list} -- list of selected RACs
        """
        self.inpath = inpath
        self.labelpath = labelpath
        self.outdir_labels = outdir_labels
        self.outdir_features = outdir_features
        self.outdir_helper = outdir_helper
        self.selected_features = selected_features

        for feature in self.selected_features:
            if feature not in list(  # pylint:disable=no-else-raise
                    FEATURE_RANGES_DICT.keys()):
                raise KeyError('Cannot understand {}'.format(feature))
            else:
                collectorlogger.info('will collect %s', feature)

        self.percentage_holdout = percentage_holdout
        self.outdir_holdout = outdir_holdout
        self.outdir_valid = None
        self.old_format = old_format
        self.training_set_size = training_set_size

        self.picklefiles = glob(os.path.join(inpath, '*.pkl'))
        self.forbidden_list = (list(read_pickle(forbidden_picklepath)) if forbidden_picklepath is not None else [])
        self.forbidden_list.append('BOJSUO')  # this is te Re2O7 with dioxan
        clashing = read_pickle('clashing_atoms.pkl')  # clashing atoms as determined by Mohamad
        self.forbidden_list.extend(clashing)

        self.forbidden_list.extend(extra_test_set)
        # just be double sure that we drop the ones we want to test on out
        if exclude_dir is not None:
            all_to_exclude = [Path(p).stem for p in glob(os.path.join(exclude_dir, '*.cif'))]
            self.forbidden_list.extend(all_to_exclude)

        # collectorlogger.info(
        #     f'initialized feature collector: {len(self.forbidden_list)} forbidden structures, {len(self.picklefiles)} files with features'
        # )
        self.x = None
        self.y = None
        self.names = None

        self.x_test = None
        self.y_test = None
        self.names_test = None

        self.x_valid = None
        self.y_valid = None
        self.names_valid = None

        # RACs
        self.racsdf = None
        self.selected_racs = selectedracs
        if (racsfile is not None) and (racsfile.endswith('.csv')):
            collectorlogger.info('Using RACs, now reading them and adding them to the feature names')
            collectorlogger.warning('Be carful, RACs and their implementation in this code are not thoroughly tested!')
            self.racsdf = pd.read_csv(racsfile)
            self.selected_features = list(self.selected_racs) + list(
                self.selected_features)  # to get the correct ordering
            for i, feature in enumerate(self.selected_racs):
                FEATURE_RANGES_DICT[feature] = [(i, i + 1)]

        # If we encode with only metal centre, we cannot drop duplicates
        self.drop_duplicates = drop_duplicates

    @staticmethod
    def _select_features(selected_features, X, outdir_helper=None, offset=0):
        """Selects the feature and dumps the names as pickle in the helper directory.
        Offset to be used if RACs are used"""
        to_hstack = []
        featurenames = []
        # RACs are naturally considered
        for feature in selected_features:
            featureranges = FEATURE_RANGES_DICT[feature]
            for featurerange in featureranges:
                lower, upper = featurerange
                # adding the offset to account for RACS from seperate file
                # that are added at the start of the feature list
                lower += offset
                upper += offset
                to_hstack.append(X[:, lower:upper])
                featurenames.extend(FEATURE_LABELS_ALL[lower:upper])

        collectorlogger.debug('the feature names are %s', featurenames)

        if outdir_helper is not None:
            with open(os.path.join(outdir_helper, 'feature_names.pkl'), 'wb') as fh:
                pickle.dump(featurenames, fh)
        return np.hstack(to_hstack)

    @staticmethod
    def _select_features_return_names(selected_features, X, offset=0):
        """Selects the feature and dumps the names as pickle in the helper directory.
        Offset to be used if RACs are used"""
        to_hstack = []
        featurenames = []
        # RACs are naturally considered
        for feature in selected_features:
            featureranges = FEATURE_RANGES_DICT[feature]
            for featurerange in featureranges:
                lower, upper = featurerange
                # adding the offset to account for RACS from seperate file
                # that are added at the start of the feature list
                lower += offset
                upper += offset
                to_hstack.append(X[:, lower:upper])
                featurenames.extend(FEATURE_LABELS_ALL[lower:upper])

        collectorlogger.debug('the feature names are %s', featurenames)

        return np.hstack(to_hstack), featurenames

    def _featurecollection(self) -> Tuple[np.array, np.array, list]:
        """
        Runs the feature collection workflow.

        Returns:
            Tuple[np.array, np.array, list] -- numpy arrays of features and labels and list of names
        """
        feature_list = FeatureCollector.create_feature_list(self.picklefiles, self.forbidden_list, self.old_format)
        label_raw = read_pickle(self.labelpath)
        # collectorlogger.info(f'found {len(label_raw)} labels')
        label_list = FeatureCollector.make_labels_table(label_raw)
        df = FeatureCollector.create_clean_dataframe(feature_list, label_list, self.drop_duplicates)

        # shuffle dataframe for the next steps to ensure randomization
        df = df.sample(frac=1).reset_index(drop=True)

        # set offset of select features
        offset = 0
        if self.racsdf is not None:
            offset = len(self.selected_racs)
            df = FeatureCollector.merge_racs_frame(df, self.racsdf, self.selected_racs)

        if self.percentage_holdout > 0:  # pylint:disable=no-else-raise
            raise NotImplementedError('Use the full version of minemofox')

        else:  # no seperate holdout set
            x, self.y, self.names = FeatureCollector.get_x_y_names(df)
        if self.training_set_size:  # perform farthest point sampling to selet a fixed number of training points
            raise NotImplementedError('Use the full version of minemofox')

        self.x = FeatureCollector._select_features(self.selected_features, x, self.outdir_helper, offset)

    def dump_featurecollection(self) -> None:
        """Collect features and write features, labels and names to seperate files

        Returns:
            None -- [description]
        """
        self._featurecollection()
        FeatureCollector.write_output(
            self.x,
            self.y,
            self.names,
            self.outdir_labels,
            self.outdir_features,
            self.outdir_helper,
        )
        if self.x_test is not None:
            FeatureCollector.write_output(
                self.x_test,
                self.y_test,
                self.names_test,
                self.outdir_holdout,
                self.outdir_holdout,
                self.outdir_holdout,
            )

        if self.x_valid is not None:
            self.outdir_valid = os.path.join(self.outdir_holdout, 'valid')
            if not os.path.exists(self.outdir_valid):
                os.makedirs(self.outdir_valid)
            FeatureCollector.write_output(
                self.x_valid,
                self.y_valid,
                self.names_valid,
                self.outdir_valid,
                self.outdir_valid,
                self.outdir_valid,
            )

    def return_featurecollection_train(self) -> Tuple[np.array, np.array, list]:
        self._featurecollection()
        return self.x, self.y, self.names

    @staticmethod
    def selectracs(df, columns=SELECTED_RACS):
        """select the RACs columns from the dataframe"""
        selected_columns = columns + [
            'name',
            'metal',
            'coordinate_x',
            'coordinate_y',
            'coordinate_z',
        ]
        return df[selected_columns]

    @staticmethod
    def _partial_match_in_name(name: str, forbidden_list: list) -> bool:
        """Tries to match also partial names, e.g. to ensure that  MAHSUK01 or
        MAHSUK02 is also matched when only MAHSUK is in the forbidden list"""
        return any(name.rstrip('1234567890') in s for s in set(forbidden_list))

    @staticmethod
    def create_feature_list(picklefiles: list, forbidden_list: list, old_format: bool = True) -> list:
        """Reads a list of pickle files into dictionary

        Arguments:
            picklefiles {list} -- list of paths
            forbidden_list {list} -- list of forbidden names (CSD naming convention)

        Returns:
            list -- parsed pickle contents
        """
        collectorlogger.info('reading pickle files with features')
        result_list = []
        if not isinstance(forbidden_list, list):
            forbidden_list = []

        for pickle_file in picklefiles:
            if not FeatureCollector._partial_match_in_name(Path(pickle_file).stem, forbidden_list):
                if not old_format:
                    result_list.extend(FeatureCollector.create_dict_for_feature_table(pickle_file))
                else:
                    result_list.extend(FeatureCollector._create_dict_for_feature_table(pickle_file))
            else:
                collectorlogger.info(
                    '{} is in forbidden list and will not be considered for X, y, names'.format(pickle_file))
        return result_list

    @staticmethod
    def make_labels_table(raw_labels: dict) -> list:
        """Read raw labeling output into a dictionary format that can be used to construct pd.DataFrames

        Warning: assumes that each metal in the structure has the same oxidation states as it takes the first
        list element. Cases in which this is not fulfilled need to be filtered out earlier.

        Arguments:
            raw_labels {dict} -- nested dictionary of {name: {metal: [oxidationstates]}}

        Returns:
            list -- list of dictionaries of the form [{'name':, 'metal':, 'oxidationstate':}]
        """
        collectorlogger.info('converting raw list of features into list of site dictionaries')
        result_list = []
        for key, value in raw_labels.items():
            for metal, oxstate in value.items():
                result_list.append({'name': key, 'metal': metal, 'oxidationstate': oxstate[0]})
        # collectorlogger.info(f'collected {len(result_list)} labels')
        return result_list

    @staticmethod
    def merge_racs_frame(df_features, df_racs, selectedracs):
        """Merges the selected RACs features to the list of features
        """
        collectorlogger.info('Merging RACs into other features')
        df_selected_racs = FeatureCollector.selectracs(df_racs, selectedracs)
        df_selected_racs['coordinate_x'] = df_selected_racs['coordinate_x'].astype(np.int32)
        df_selected_racs['coordinate_y'] = df_selected_racs['coordinate_y'].astype(np.int32)
        df_selected_racs['coordinate_z'] = df_selected_racs['coordinate_z'].astype(np.int32)

        df_features['coordinate_x'] = df_features['coordinate_x'].astype(np.int32)
        df_features['coordinate_y'] = df_features['coordinate_y'].astype(np.int32)
        df_features['coordinate_z'] = df_features['coordinate_z'].astype(np.int32)

        df_merged = pd.merge(
            df_features,
            df_selected_racs,
            left_on=['name', 'metal', 'coordinate_x', 'coordinate_y', 'coordinate_z'],
            right_on=['name', 'metal', 'coordinate_x', 'coordinate_y', 'coordinate_z'],
        )
        df_merged.dropna(inplace=True)

        df_merged = df_merged.loc[df_merged.astype(str).drop_duplicates().index]

        new_feature_columns = []
        print((df_merged.shape))
        for _, row in df_merged.iterrows():
            new_feature_column = row['feature']
            racs = list(row[selectedracs])
            racs.extend(new_feature_column)
            new_feature_columns.append(racs)
        print((len(new_feature_columns)))
        df_merged.drop(columns=['feature'], inplace=True)
        df_merged['feature'] = new_feature_columns

        return df_merged

    @staticmethod
    def create_clean_dataframe(feature_list: list, label_list: list, drop_duplicates: bool = True) -> pd.DataFrame:
        """Merge the features and the labels on names and metals and drop entry rows

        Arguments:
            feature_list {list} --  list of dictionaries of the features, names and metals
            label_list {list} -- list of dicionaries with names, metals and labels
            drop_duplicates {bool} -- drops duplicates if True
        Returns:
            pd.DataFrame -- Dataframe with each row describing a seperate metal site
        """
        pd.options.mode.use_inf_as_na = True
        collectorlogger.info('merging labels and features')
        df_features = pd.DataFrame(feature_list)
        df_labels = pd.DataFrame(label_list)
        df_merged = pd.merge(
            df_features,
            df_labels,
            left_on=['name', 'metal'],
            right_on=['name', 'metal'],
        )

        collectorlogger.info(
            'the length of the feature df is {} the length of the label df is {} and the merged one is {}'.format(
                len(df_features), len(df_labels), len(df_merged)))
        df_merged.dropna(inplace=True)
        if drop_duplicates:
            df_cleaned = df_merged.loc[df_merged.astype(str).drop_duplicates(
            ).index]  # to be sure that we do not accidently have same examples in training and test set
        else:
            df_cleaned = df_merged
        return df_cleaned

    @staticmethod
    def get_x_y_names(df: pd.DataFrame) -> Tuple[np.array, np.array, list]:
        """Splits the columns of a dataframe into features, labels and names

        Arguments:
            df {pd.DataFrame} -- dataframe that in each row contains a full description of
                a metal site with feature, oxidation state, metal  and name

        Returns:
            Tuple[np.array, np.array, list] -- [description]
        """
        names = list(df['name'])
        # ToDo: check why I used this comprehension
        feature_list = [l for l in df['feature']]  # pylint:disable=unnecessary-comprehension
        features = np.array(feature_list)
        labels = np.array(df['oxidationstate'])
        return features, labels, names

    @staticmethod
    def create_dict_for_feature_table(picklefile: PathType) -> list:
        """Reads in a pickle with features and returns a list of dictionaries with one dictionary per metal site.

        Arguments:
            picklefile {PathType} -- path to pickle file

        Returns:
            list -- list of dicionary
        """
        result = read_pickle(picklefile)
        mpd = MagpieData()
        result_list = []
        for site in result:
            e = Element(site['metal'])
            valence_electrons = mpd.get_elemental_properties([e], 'NValence')[0]
            valence_to_donate = diff_to_18e(valence_electrons)
            sunfilled = mpd.get_elemental_properties([e], 'NsUnfilled')[0]
            dunfilled = mpd.get_elemental_properties([e], 'NdUnfilled')[0]
            punfilled = mpd.get_elemental_properties([e], 'NpUnfilled')[0]
            metal_encoding = [
                e.number,
                e.row,
                e.group,
                valence_electrons,
                valence_to_donate,
                sunfilled,
                punfilled,
                dunfilled,
                np.random.randint(1, 18),
            ]
            features = list(site['feature'])
            features.extend(metal_encoding)
            result_dict = {
                'metal': site['metal'],
                'coordinate_x': int(site['coords'][0]),
                'coordinate_y': int(site['coords'][1]),
                'coordinate_z': int(site['coords'][2]),
                'feature': features,
                'name': Path(picklefile).stem,
            }

            if not np.isnan(np.array(features)).any():
                result_list.append(result_dict)

        return result_list

    @staticmethod
    def create_dict_for_feature_table_from_dict(d) -> list:
        """Reads in a pickle with features and returns a list of dictionaries with one dictionary per metal site.

        Arguments:
            d {dict} -- dictionary

        Returns:
            list -- list of dicionary
        """
        mpd = MagpieData()
        result_list = []
        for site in d:
            e = Element(site['metal'])
            valence_electrons = mpd.get_elemental_properties([e], 'NValence')[0]
            valence_to_donate = diff_to_18e(valence_electrons)
            sunfilled = mpd.get_elemental_properties([e], 'NsUnfilled')[0]
            dunfilled = mpd.get_elemental_properties([e], 'NdUnfilled')[0]
            punfilled = mpd.get_elemental_properties([e], 'NpUnfilled')[0]
            metal_encoding = [
                e.number,
                e.row,
                e.group,
                valence_electrons,
                valence_to_donate,
                sunfilled,
                punfilled,
                dunfilled,
                np.random.randint(1, 18),
            ]
            features = list(site['feature'])
            features.extend(metal_encoding)
            result_dict = {  # pylint:disable=unnecessary-comprehension
                'metal': site['metal'],
                'coordinate_x': int(site['coords'][0]),
                'coordinate_y': int(site['coords'][1]),
                'coordinate_z': int(site['coords'][2]),
                'feature': features,
                'name': 'noname',
            }

            if not np.isnan(np.array(features)).any():
                result_list.append(result_dict)

        return result_list

    @staticmethod
    def _create_dict_for_feature_table(picklefile: PathType) -> list:
        """Reads in a pickle with features and returns a list of dictionaries with one dictionary per metal site.

        Arguments:
            picklefile {PathType} -- path to pickle file

        Returns:
            list -- list of dicionary
        """
        # warnings.DeprecationWarning(
        #    "this is method for old feature files will be deprecated. Produce feature files in new format"
        # )
        result = read_pickle(picklefile)

        result_list = []
        for key, value in result.items():
            e = Element(key)

            metal_encoding = [e.number, e.row, e.group, np.random.randint(1, 18)]
            features = list(value['feature'])
            features.extend(metal_encoding)
            result_dict = {
                'metal': key,
                'coords': value['coords'],
                'feature': features,
                'name': Path(picklefile).stem,
            }

            if not np.isnan(np.array(features)).any():
                result_list.append(result_dict)

        return result_list

    @staticmethod
    def write_output(
            x: np.array,
            y: np.array,
            names: list,
            outdir_labels: PathType,
            outdir_features: PathType,
            outdir_helper: PathType,
    ) -> None:
        """writes feature array, label array and name array into output files in outdir/datetime/{x,y}.npy and outdir/datetime/names.pkl

        Arguments:
            x {np.array} -- feature matrix
            y {np.array} -- label vector
            names {list} -- name list (csd  identifiers)
            outdir_labels {PathType} -- directory into which labels are written
            outdir_features {PathType} -- directory into which features are written
            outdir_helper {PathType} -- directory into which names are written

        Returns:
            None --
        """
        # timestr = time.strftime('%Y%m%d-%H%M%S')
        # outpath_base = os.path.join(outdir, timestr)

        np.save(os.path.join(outdir_features, 'features'), x)
        np.save(os.path.join(outdir_labels, 'labels'), y)

        with open(os.path.join(outdir_helper, 'names.pkl'), 'wb') as picklefile:
            pickle.dump(names, picklefile)

        collectorlogger.info('stored features into labels and names into')
