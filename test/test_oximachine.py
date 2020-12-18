# -*- coding: utf-8 -*-
# pylint:disable=missing-module-docstring, missing-function-docstring
import os

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
    assert len(output) == 5
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
    assert len(output) == 5
    assert output["prediction"] == [2, 2]
    assert output["metal_indices"] == [0, 1]
    assert output["metal_symbols"] == ["Fe", "Fe"]
    assert output["base_predictions"] == [[2, 2, 2, 2], [2, 2, 2, 2]]

    assert isinstance(runner.feature_names, list)
