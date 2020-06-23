# -*- coding: utf-8 -*-
"""ipywidget to run the oxiMACHINE on AiiDA lab"""
import ipywidgets as ipw
from ase import Atoms
from pymatgen.io.ase import AseAtomsAdaptor
from traitlets import Dict, Instance

from oximachinerunner import _featurize_single, _make_predictions


class OxiMachineWidget(ipw.VBox):
    """Widget that allows for the basic structure editing."""
    structure = Instance(Atoms, allow_none=True)
    oxidation_states = Dict(allow_none=True)

    def __init__(self, title=''):
        self.title = title
        button_runoximachine = ipw.Button(description='Find oxidation states')
        button_runoximachine.on_click(self.run_oximachine)
        self.tolerance = ipw.FloatSlider(
            value=1.0,
            min=0.1,
            max=2.0,
            step=0.1,
            description='Tolerance',
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
        )

        self.output = ipw.HTML('')
        super().__init__(children=[button_runoximachine, self.output])

    def run_oximachine(self, _=None):
        """Call the oxiMACHINE and save prediction to self.oxidation_states it possible"""
        self.output.value = """<i class="fa fa-spinner fa-pulse" style="color:red;" ></i>"""
        try:
            atoms_adaptor = AseAtomsAdaptor()
            structure = atoms_adaptor.get_structure(self.structure)
            X, metal_indices, _ = _featurize_single(structure)  # pylint:disable=invalid-name
            predictions = _make_predictions(X)
        except Exception:  # pylint:disable=broad-except
            self.output.value = 'Could not determine the oxidation states'
        else:
            self.output.value = ''
            results = dict(zip(metal_indices, predictions))
            self.oxidation_states = results
