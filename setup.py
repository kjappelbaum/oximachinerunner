#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name, missing-docstring
import io
import os

from setuptools import find_packages, setup

import versioneer

# Package meta-data.
NAME = "oximachinerunner"
DESCRIPTION = "Run the oximachine"
URL = "https://github.com/kjappelbaum/oximachinerunner"
EMAIL = "kevin.jablonka@epfl.ch"
AUTHOR = "Kevin M. Jablonka, Daniele Ongari, Mohamad Moosavi, Berend Smit"
REQUIRES_PYTHON = ">=3.7,<3.9"

# What packages are required for this module to be executed?
with open("requirements.txt", "r") as fh:
    requirements = [line.strip() for line in fh]  # pylint:disable=invalid-name

# What packages are optional?
EXTRAS = {
    "dev": [
        "pre-commit~=2.6.0",
        "pylint~=2.5.3",
        "pytest~=6.0.1",
        "versioneer~=0.18",
        "isort~=4.3.21",
        "black",
    ],
    "docs": [
        "sphinx~=3.3.1",
        "sphinx-book-theme~=0.0.39",
        "sphinx-autodoc-typehints~=1.11.1",
        "sphinx-copybutton~=0.3.1",
    ],
}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=requirements,
    extras_require=EXTRAS,
    packages=find_packages(include=["oximachinerunner*"]),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
