# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Copyright (c) 2018, Eurecat / UPF
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   @file   test_SOFANcFile.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
import os
import tempfile
from netCDF4 import Dataset
import numpy as np
from pysofaconventions import *
from collections import OrderedDict

def test_close():

    # Open the file and assert it
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    assert rootgrp.isopen()

    # Close the file and assert it
    rootgrp.close()
    assert not rootgrp.isopen()

    # Open the file through a SofaNetCDFile instance
    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.file.isopen()

    # Close it and assert it
    sofaNcFile.close()
    assert not sofaNcFile.file.isopen()

    os.remove(path)

def test_getGobalAttributesAsDict():

    targetDict = {
        'attr1': 'attrValue1',
        'attr2': 'attrValue2',
    }

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.attr1 = 'attrValue1'
    rootgrp.attr2 = 'attrValue2'
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.getGlobalAttributesAsDict() == targetDict

    sofafile.close()
    os.remove(path)


def test_getGlobalAttributeValue():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        sofaNcFile = sofafile.ncfile
        with pytest.raises(SOFAError) as e:
            sofaNcFile.getGlobalAttributeValue('attr1')
        assert e.match(errorString)
        sofafile.close()

    # Attribute not found error
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Attribute not found')

    # Attribute correctly found
    rootgrp = Dataset(path, 'a')
    rootgrp.attr1 = 'attrValue1'
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.getGlobalAttributeValue('attr1') == 'attrValue1'

    sofafile.close()
    os.remove(path)


def test_getDimensionsAsDict():

    # Empty dictionary
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()

    emptyDict = {}
    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.getDimensionsAsDict() == emptyDict
    sofafile.close()

    # Non-empty dictionary
    rootgrp = Dataset(path, 'a')
    dimA = rootgrp.createDimension('A',1)
    dimB = rootgrp.createDimension('B',2)
    rootgrp.close()

    targetDict = OrderedDict([
        ('A',dimA),
        ('B',dimB)
    ])

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile

    # Assert dimension names are equal
    for k1, k2 in zip(targetDict.keys(), sofaNcFile.getDimensionsAsDict().keys()):
        assert k1 == k2
    # Assert dimension instances (value and name) are equal
    for v1, v2 in zip(targetDict.values(), sofaNcFile.getDimensionsAsDict().values()):
        assert v1.name == v2.name
        assert v1.size == v2.size


    sofafile.close()
    os.remove(path)


def test_getDimension():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        sofaNcFile = sofafile.ncfile
        with pytest.raises(SOFAError) as e:
            sofaNcFile.getDimension('A')
        assert e.match(errorString)
        sofafile.close()

    # Dimension not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Dimension not found')

    # Dimension found
    rootgrp = Dataset(path, 'a')
    dimA = rootgrp.createDimension('A', 1)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.getDimension('A') == sofaNcFile.getDimensionsAsDict()['A']

    sofafile.close()
    os.remove(path)


def test_getDimensionSize():

    variableName = 'A'

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        sofaNcFile = sofafile.ncfile
        with pytest.raises(SOFAError) as e:
            sofaNcFile.getDimensionSize(variableName)
        assert e.match(errorString)
        sofafile.close()

    # Dimension not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Dimension not found')

    # Dimension found
    rootgrp = Dataset(path, 'a')
    dimA = rootgrp.createDimension(variableName, 1)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.getDimensionSize(variableName) == sofaNcFile.getDimensionsAsDict()[variableName].size

    sofafile.close()
    os.remove(path)


def test_getVariablesAsDict():

    variableName1 = 'CoolVariable1'
    variableName2 = 'CoolVariable2'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createVariable(variableName1, 'f8', ())
    rootgrp.createVariable(variableName2, 'f8', ())
    variableDict = OrderedDict(rootgrp.variables)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile

    # Assert variable names are equal
    for k1, k2 in zip(variableDict.keys(), sofaNcFile.getVariablesAsDict().keys()):
        assert k1 == k2
    # Assert variable instances are equal (through internal dict)
    for v1, v2 in zip(variableDict.values(), sofaNcFile.getVariablesAsDict().values()):
        assert v1.__dict__ == v2.__dict__

    sofafile.close()
    os.remove(path)


def test_getVariableInstance():

    variableName = 'A'

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        sofaNcFile = sofafile.ncfile
        with pytest.raises(SOFAError) as e:
            sofaNcFile.getVariableInstance(variableName)
        assert e.match(errorString)
        sofafile.close()

    # Variable not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Variable not found')

    # Variable found
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable(variableName, 'f8', ())
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.getVariableInstance('A') == sofaNcFile.getVariablesAsDict()['A']

    sofafile.close()
    os.remove(path)


def test_getVariableShape():

    variableName = 'A'

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        sofaNcFile = sofafile.ncfile
        with pytest.raises(SOFAError) as e:
            sofaNcFile.getVariableShape(variableName)
        assert e.match(errorString)
        sofafile.close()

    # Dimension not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Variable not found')

    # Dimension found
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable(variableName, 'f8', ())
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.getVariableShape(variableName) == sofaNcFile.getVariablesAsDict()[variableName].shape

    sofafile.close()
    os.remove(path)


def test_getVariableValues():

    variableName = 'A'
    variableDim = 3
    variableValue = np.random.rand(variableDim)

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        sofaNcFile = sofafile.ncfile
        with pytest.raises(SOFAError) as e:
            sofaNcFile.getVariableValues(variableName)
        assert e.match(errorString)
        sofafile.close()

    # Dimension not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Variable not found')

    # Dimension found
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('D1',variableDim)
    var = rootgrp.createVariable(variableName, 'f8', ('D1',))
    var[:] = variableValue
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert np.array_equal(sofaNcFile.getVariableValues(variableName), variableValue)

    sofafile.close()
    os.remove(path)


def test_variableHasDimensions():

    dimensionName1 = 'D1'
    dimensionValue1 = 1
    dimensionName2 = 'D2'
    dimensionValue2 = 2
    variableName = 'V'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension(dimensionName1,dimensionValue1)
    rootgrp.createDimension(dimensionName2,dimensionValue2)
    rootgrp.createVariable(variableName, 'f8', (dimensionName1,dimensionName2))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    variableInstance = sofaNcFile.getVariableInstance(variableName)
    # Dimension shape does not match
    assert not SOFANetCDFFile.variableHasDimensions(variableInstance, (dimensionValue1,))
    # Dimension shape and values match, but not order
    assert not SOFANetCDFFile.variableHasDimensions(variableInstance, (dimensionValue2, dimensionValue1))
    # Both shape and values match
    assert SOFANetCDFFile.variableHasDimensions(variableInstance, (dimensionValue1, dimensionValue2))

    sofafile.close()
    os.remove(path)


def test_variableHasAttribute():

    dimensionName = 'D'
    dimensionValue = 1
    variableName = 'V'
    attributeValue = 'value'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension(dimensionName,dimensionValue)
    var = rootgrp.createVariable(variableName, 'f8', (dimensionName,))
    var.attribute = attributeValue
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    variableInstance = sofaNcFile.getVariableInstance(variableName)
    # Attribute not found
    assert not SOFANetCDFFile.variableHasAttribute(variableInstance, 'notFoundAttribute')
    # Attribute found
    assert SOFANetCDFFile.variableHasAttribute(variableInstance, 'attribute')

    sofafile.close()
    os.remove(path)


def test_getVariableAttributeFromInstance():

    dimensionName = 'D'
    dimensionValue = 1
    variableName = 'V'
    attributeValue = 'value'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension(dimensionName,dimensionValue)
    var = rootgrp.createVariable(variableName, 'f8', (dimensionName,))
    var.attribute = attributeValue
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    variableInstance = sofaNcFile.getVariableInstance(variableName)
    # Attribute not found
    assert SOFANetCDFFile.getVariableAttributeFromInstance(variableInstance, 'notFoundAttribute') == None
    # Attribute found
    assert SOFANetCDFFile.getVariableAttributeFromInstance(variableInstance, 'attribute') == attributeValue

    sofafile.close()
    os.remove(path)


def test_getVariableAttributeFromName():

    dimensionName = 'D'
    dimensionValue = 1
    variableName = 'V'
    attributeValue = 'attrValue'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension(dimensionName,dimensionValue)
    var = rootgrp.createVariable(variableName, 'f8', (dimensionName,))
    var.attribute = attributeValue
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    # Attribute not found
    assert sofaNcFile.getVariableAttributeFromName(variableName, 'notFoundAttribute') == None
    # Attribute found
    assert sofaNcFile.getVariableAttributeFromName(variableName, 'attribute') == attributeValue

    sofafile.close()
    os.remove(path)


def test_getVariableDimensionsFromInstance():

    dimensionName1 = 'D1'
    dimensionValue1 = 1
    dimensionName2 = 'D2'
    dimensionValue2 = 2
    variableName = 'V'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension(dimensionName1,dimensionValue1)
    rootgrp.createDimension(dimensionName2,dimensionValue2)
    rootgrp.createVariable(variableName, 'f8', (dimensionName1,dimensionName2))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    variableInstance = sofaNcFile.getVariableInstance(variableName)
    assert SOFANetCDFFile.getVariableDimensionsFromInstance(variableInstance) == (dimensionValue1,dimensionValue2)

    sofafile.close()
    os.remove(path)


def test_getVariableDimensionsFromName():

    dimensionName1 = 'D1'
    dimensionValue1 = 1
    dimensionName2 = 'D2'
    dimensionValue2 = 2
    variableName = 'V'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension(dimensionName1,dimensionValue1)
    rootgrp.createDimension(dimensionName2,dimensionValue2)
    rootgrp.createVariable(variableName, 'f8', (dimensionName1,dimensionName2))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.getVariableDimensionsFromName(variableName) == (dimensionValue1,dimensionValue2)

    sofafile.close()
    os.remove(path)


def test_getVariableDimensionalityFromInstance():

    dimensionName1 = 'D1'
    dimensionValue1 = 1
    dimensionName2 = 'D2'
    dimensionValue2 = 2
    variableName = 'V'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension(dimensionName1,dimensionValue1)
    rootgrp.createDimension(dimensionName2,dimensionValue2)
    rootgrp.createVariable(variableName, 'f8', (dimensionName1,dimensionName2))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    variableInstance = sofaNcFile.getVariableInstance(variableName)
    assert SOFANetCDFFile.getVariableDimensionalityFromInstance(variableInstance) == 2

    sofafile.close()
    os.remove(path)


def test_getVariableDimensionalityFromName():

    dimensionName1 = 'D1'
    dimensionValue1 = 1
    dimensionName2 = 'D2'
    dimensionValue2 = 2
    variableName = 'V'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension(dimensionName1,dimensionValue1)
    rootgrp.createDimension(dimensionName2,dimensionValue2)
    rootgrp.createVariable(variableName, 'f8', (dimensionName1,dimensionName2))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaNcFile = sofafile.ncfile
    assert sofaNcFile.getVariableDimensionalityFromName(variableName) == 2

    sofafile.close()
    os.remove(path)