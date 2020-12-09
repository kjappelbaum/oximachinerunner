Getting Started
================

Installation
---------------

We recommend installing oximachinerunner in a clean virtual environment environment (e.g., a `conda environment <https://docs.conda.io/projects/conda/en/latest/index.html>`_)

You can install the latest stable release from PyPi using

.. code-block:: bash

    pip install oximachinerunner


or the latest development version using

.. code-block:: bash

    pip install git+https://github.com/kjappelbaum/oximachinerunner.git



Running Inference
---------------------

The most common use case for oximachinerunner is to estimate the oxidation states for metal cation in a crystal structure. To do so, you only need the following lines of code

.. code-block:: python

    from oximachinerunner import OximachineRunner

    oximachine_instance = OximachineRunner()
    oxidation_states, metal_indices, metal_symbols = oximachine_instance.run_oximachine(<structure>)

In the code snippet above, :code:`structure` can be a :code:`pymatgen.Structure`, :code:`ase.Atoms` object or a filepath to a `cif`.
The output of the run will be three lists of identical length: One contains the oxidationstates, the second one contains the indices of the metals, and the third one contains the elemental symbols of the metals.

Models
------------

When you create an instance of the :code:`OximachineRunner` class you can choose which model you want to use. Currently, we provide a model that was trained only on MOFs and another one that was trained on all chemistry deposited in the Cambridge Crystallographic Database (CSD) plus additional structures from the Crystallographic Open Database (COD). By default, oximachinerunner uses latter model. You can list all availabel models using the :py:attr:`~OximachineRunner.available_models` attribute.

If you use the package for the first time, it will automatically download the models. You can turn this behavior off by setting :code:`automatic_download=False` in the class initialization.


Additional information
-----------------------------

ipython widget
--------------------



Caveats
-------------

This model works excellent on a test set but it might give fully unphysical predictions in some cases when it is used outside the domain of applicability (structures similar to the ones in the MOF subset of the CSD). This is currently estimated with an uncertainty vote.
