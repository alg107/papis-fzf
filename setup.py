# -*- coding: utf-8 -*-
from setuptools import setup

from papis_fzf import __version__

with open('README.rst') as fd:
    long_description = fd.read()

setup(
    name='papis-fzf',
    version=__version__,
    author='Alex Goodenbour',
    install_requires=[
        "papis>=0.11",
        "pyfzf",
    ],
    description='fzf based picker for papis',
    long_description=long_description,
    packages=[
        "papis_fzf",
    ],
    entry_points={
        'papis.picker': [
            'fzf=papis_fzf.fzf:Picker'
        ]
    },
    platforms=['linux', 'osx'],
)
