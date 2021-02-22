Getting Started
================

Installation
---------------

We recommend installing oximachinerunner in a clean virtual environment environment (e.g., a `conda environment <https://docs.conda.io/projects/conda/en/latest/index.html>`_). On macOS you need to run `brew install libomp` first to enable multithreading for the `XGBoost` library.

You can install the latest stable release from PyPi using

.. code-block:: bash

    pip install oximachinerunner


or the latest development version using

.. code-block:: bash

    pip install git+https://github.com/kjappelbaum/oximachinerunner.git


Note that the installation will take significant (>500 MB) hard drive storage as the models contain a k-nearest neighbors esimator that basically stores the complete training set.

Some parts of the code are accelerated using just-in-time compilation (jit) using numba. This can benefit from `threading layers <https://numba.pydata.org/numba-doc/latest/user/threading-layer.html>`_. You can enable this using :code:`pip install tbb`. If you do not do so, you might see warnings like :code:`The TBB threading layer requires TBB version 2019.5 or later`.

Running Inference
---------------------

The most common use case for oximachinerunner is to estimate the oxidation states for metal cation in a crystal structure. To do so, you only need the following lines of code

.. code-block:: python

    from oximachinerunner import OximachineRunner

    oximachine_instance = OximachineRunner()
    results = oximachine_instance.run_oximachine(<structure>)

In the code snippet above, :code:`structure` can be a :code:`pymatgen.Structure`, :code:`ase.Atoms` object or a filepath to a `cif`.
The output of the run will be a `OrderedDict` with:

- A list of oxidation state predictions
- A list of indices of the metal sites
- Strings indicating the metal
- The predictions of the base estimators
- The estimated probabilites


Models
------------

When you create an instance of the :code:`OximachineRunner` class you can choose which model you want to use. Currently, we provide a model that was trained only on MOFs and another one that was trained on all chemistry deposited in the Cambridge Crystallographic Database (CSD) plus additional structures from the Crystallographic Open Database (COD). By default, oximachinerunner uses latter model. You can list all availabel models using the :py:attr:`~OximachineRunner.available_models` attribute.

If you use the package for the first time, it will automatically download the models. You can turn this behavior off by setting :code:`automatic_download=False` in the class initialization.

Exceptions
-----------

- *No metal in structure*: `OximachineRunner` can only be used to predict oxidation states of metals. If a input structure does not contain a metal, we will raise a :py:class:`~oximachinerunner.errors.NoMetalError` execption.
- *Parsing error*: Internally, we will convert all inputs into a pymatgen structure object. This only works if pymatgen can parse the structure. Note that a pymatgen Structure is a periodic object, hence we need some information about the cell. Also, there might be issues in case the `CIF` is formatted in a way pymatgen cannot handle (e.g., using `_atom_site_Cartn_x` instead of `_atom_site_fract_x`). In all these cases, we will raise a :py:class:`~oximachinerunner.errors.ParsingError` execption.
- *Featurization error*: In some cases the featurization might fail. Then, we will raise a :py:class:`~oximachinerunner.errors.FeaturizationError` exception.
- *Prediction error*: In some cases the prediction might fail. Then, we will rasie a :py:class:`~oximachinerunner.errors.PredictionError` execption.

All errors are subclasses of :py:class:`~oximachinerunner.errors.OximachineRunnerException`. Hence, in principle, you can just catch with exception class to catch all aforementioned error types.


Graphical user interface
-------------------------

If you want to have a graphical user interface for this application, you can use the `oximachinetool <https://github.com/kjappelbaum/oximachinetool>`_.  You can try this application `online <http://go.epfl.ch/oximachine>`_.

Caveats
-------------

This model works excellent on a test set but it might give fully unphysical predictions in some cases when it is used outside the domain of applicability (structures similar to the ones in the MOF subset of the CSD). This is currently estimated with an uncertainty vote.
