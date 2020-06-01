# pysofaconventions

[![PyPI](https://img.shields.io/pypi/v/pysofaconventions.svg)](https://pypi.python.org/pypi/pysofaconventions)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Build Status](https://travis-ci.org/andresperezlopez/pysofaconventions.svg?branch=master)](https://travis-ci.org/andresperezlopez/pysofaconventions)
[![Coverage Status](https://coveralls.io/repos/github/andresperezlopez/pysofaconventions/badge.svg?branch=master)](https://coveralls.io/github/andresperezlopez/pysofaconventions?branch=master)
[![PyPI](https://img.shields.io/badge/python-3.6-blue.svg)]()

Python implementation of the SOFA Specification
www.sofaconventions.org

Adapted from [API_Cpp](https://github.com/sofacoustics/API_Cpp), the C++ implementation by Thibaut Carpentier.
Based on the [fork by andresperezlopez](https://github.com/andresperezlopez/API_Cpp) which implements the [AmbisonicsDRIR Convention](https://zenodo.org/record/1299894) v0.1.


## installation

### automatic installation

`sudo pip install pysofaconventions`


### manual installation

Clone the sources from github:
```
git clone https://github.com/andresperezlopez/pysofaconventions.git
```

Then enter the source folder and install using pip to handle python dependencies:
```
cd pysofaconventions
sudo pip install -e .
```


## dependencies

- netCDF4


## examples

Check the /examples folder to see some reference implementations.


## changelog

Version 0.1.5, 18/05/2019
- SourceUp.Units and SourceUp.Coordinates are not mandatory
- SingleRoomDRIR: ListenerView.Units and SourceView.Units are not mandatory

Version 0.1.4, 13/05/2019
- ListenerUp.Units and ListenerUp.Coordinates are not mandatory
- SimpleFreeFieldHRIR: mandatory R=2
- Updated to netCDF4-1.5.1.2
- Removed remote build version 3.4 (netcdf4 lib incompatibility)
