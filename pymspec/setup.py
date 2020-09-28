# -*- coding: utf-8 -*- 
"""
---------------------------------------------------------------------
Copyright 2013 Alexandre Drouin

This file is part of pymspec.

pymspec is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pymspec is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pymspec.  If not, see <http://www.gnu.org/licenses/>.
---------------------------------------------------------------------
"""
from setuptools import setup, find_packages
from Cython.Build import cythonize


setup(
    name="pymspec",
    version="0.1",
    author="Alexandre Drouin",
    author_email="alexandre.drouin.8@ulaval.ca",
    description='A python framework for playing with mass get_spectra',
    license="GPL",
    keywords="mass, spectrometry, spectrum, get_spectra, kernel, proteomics",
    url="",
    packages=find_packages(), requires=['numpy', 'xlrd']
)
