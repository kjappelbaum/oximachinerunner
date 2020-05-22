#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name, missing-docstring

from __future__ import absolute_import
import io
import os
import sys
import subprocess

from setuptools import setup
import versioneer

git_matminer = 'git+https://github.com/kjappelbaum/matminer.git@localpropertystats'

try:
    import matminer  # pylint:disable=unused-import
except Exception:  # pylint:disable=broad-except
    if '--user' in sys.argv:
        subprocess.run(
            [
                sys.executable,
                '-m',
                'pip',
                'install',
                '--upgrade',
                '--user',
                git_matminer,
            ],
            check=False,
        )
    else:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--upgrade', git_matminer],
            check=False,
        )

# Package meta-data.
NAME = 'oximachinerunner'
DESCRIPTION = 'Run the oximachine'
URL = 'https://github.com/kjappelbaum/oximachinerunner'
EMAIL = 'kevin.jablonka@epfl.ch'
AUTHOR = 'Kevin M. Jablonka, Daniele Ongari, Mohamad Moosavi, Berend Smit'
REQUIRES_PYTHON = '>=3.5.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'pymatgen',
    'ase',
    'apricot-select',
    'tqdm',
    'pandas',
    'scikit-learn==0.22',
    'scikit-multilearn',
]

# What packages are optional?
EXTRAS = {
    'dev': ['prospector', 'pre-commit', 'pylint', 'pytest', 'versioneer'],
}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='GPL',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
