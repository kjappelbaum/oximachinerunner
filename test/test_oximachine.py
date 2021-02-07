# -*- coding: utf-8 -*-
# pylint:disable=missing-module-docstring, missing-function-docstring
import os

from ase.io import read
from pymatgen import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from oximachinerunner import OximachineRunner

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def test_model_dict():
    runner = OximachineRunner()
    assert isinstance(runner.featureset, list)


def test_oximachine():
    runner = OximachineRunner()
    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "oximachinerunner/assets/ACODAA.cif")
    )
    assert len(output) == 6
    assert output["prediction"] == [2, 2]
    assert output["metal_indices"] == [0, 1]
    assert output["metal_symbols"] == ["Fe", "Fe"]
    assert output["base_predictions"] == [[2, 1, 2, 2], [2, 1, 2, 2]]

    output = runner.run_oximachine(os.path.join(THIS_DIR, "..", "examples/guvzee.cif"))
    assert output["prediction"] == [
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
    ]

    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "examples/GUVZII_clean.cif")
    )
    assert output["prediction"] == [
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
    ]

    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "examples/IDIWOH_clean.cif")
    )
    assert output["prediction"] == [4, 4, 4, 4]

    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "examples/IDIWIB_clean.cif")
    )
    assert output["prediction"] == [3, 3, 3, 3]

    # testing the MOF model
    runner = OximachineRunner(modelname="mof")
    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "examples/IDIWIB_clean.cif")
    )
    assert output["prediction"] == [3, 3, 3, 3]

    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "examples/IDIWOH_clean.cif")
    )
    assert output["prediction"] == [4, 4, 4, 4]

    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "oximachinerunner/assets/ACODAA.cif")
    )
    assert len(output) == 6
    assert output["prediction"] == [2, 2]
    assert output["metal_indices"] == [0, 1]
    assert output["metal_symbols"] == ["Fe", "Fe"]
    assert output["base_predictions"] == [[2, 2, 2, 2], [2, 2, 2, 2]]

    assert isinstance(runner.feature_names, list)

    runner = OximachineRunner()
    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "oximachinerunner/assets/Mg_MOF_74.cif")
    )
    assert len(output["prediction"]) == 6
    assert output["metal_indices"][0] == 0
    assert output["metal_indices"][5] == 5

    runner = OximachineRunner()
    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "structure_data", "RSM0027.cif")
    )

    assert output["prediction"] == [3, 3]

    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "structure_data", "RSM0099.cif")
    )

    assert output["prediction"] == [3, 3, 3]

    # test independence on reader
    pymatgen_structure = Structure.from_file(
        os.path.join(THIS_DIR, "structure_data", "RSM0027.cif")
    )

    atoms = read(os.path.join(THIS_DIR, "structure_data", "RSM0027.cif"))

    output = runner.run_oximachine(pymatgen_structure)

    assert output["prediction"] == [3, 3]

    output = runner.run_oximachine(atoms)

    assert output["prediction"] == [3, 3]

    # Now, transform the cell

    space_group_analyzer = SpacegroupAnalyzer(pymatgen_structure)

    output = runner.run_oximachine(
        space_group_analyzer.get_conventional_standard_structure()
    )

    assert output["prediction"] == [3, 3, 3, 3]

    output = runner.run_oximachine(
        space_group_analyzer.get_primitive_standard_structure()
    )

    assert output["prediction"] == [3, 3]

    runner = OximachineRunner(modelname="nn")
    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "oximachinerunner/assets/Mg_MOF_74.cif")
    )
    assert len(output["prediction"]) == 6
    assert output["prediction"] == [2, 2, 2, 2, 2, 2]
    assert output["metal_indices"][0] == 0
    assert output["metal_indices"][5] == 5

    output = runner.run_oximachine(
        os.path.join(THIS_DIR, "..", "oximachinerunner/assets/ACODAA.cif")
    )
    assert len(output) == 6
    assert output["prediction"] == [2, 2]
    assert output["metal_indices"] == [0, 1]
    assert output["metal_symbols"] == ["Fe", "Fe"]
    assert len(output["std"]) == 2
    assert output["std"][0] >= 0
    assert output["std"][1] >= 0
