# -*- coding: utf-8 -*-
# pylint:disable=missing-module-docstring, missing-function-docstring
import os

from oximachinerunner import OximachineRunner

THIS_DIR = os.path.dirname(os.path.realpath(__file__))


def test_oximachine():
    runner = OximachineRunner()
    output = runner.run_oximachine(os.path.join(THIS_DIR, '..', 'oximachinerunner/assets/ACODAA.cif'))
    assert len(output) == 3
    assert output[0] == [2, 2]
    assert output[1] == [0, 1]
    assert output[2] == ['Fe', 'Fe']

    output = runner.run_oximachine(os.path.join(THIS_DIR, '..', 'examples/guvzee.cif'))
    assert output[0] == [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

    output = runner.run_oximachine(os.path.join(THIS_DIR, '..', 'examples/GUVZII_clean.cif'))
    assert output[0] == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

    output = runner.run_oximachine(os.path.join(THIS_DIR, '..', 'examples/IDIWOH_clean.cif'))
    assert output[0] == [4, 4, 4, 4]

    output = runner.run_oximachine(os.path.join(THIS_DIR, '..', 'examples/IDIWIB_clean.cif'))
    assert output[0] == [3, 3, 3, 3]
