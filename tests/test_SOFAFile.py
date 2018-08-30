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
#   @file   test_SOFAFile.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
import os
import tempfile
from netCDF4 import Dataset
import time
from pysofaconventions import *
import sys
import numpy as np
from collections import OrderedDict


def test_isValid():

    def raiseWarning(warningString):
        sofafile = SOFAFile(path, 'r')
        with pytest.warns(SOFAWarning) as record:
            assert not sofafile.isValid()
        assert warningString in str(record[-1].message)
        sofafile.close()

    # Missing Global Attributes
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    raiseWarning('Missing required attribute')
    sofafile.close()

    # All required attributes, but Invalid SOFA convention
    rootgrp = Dataset(path, 'a')
    rootgrp.Conventions = 'NOT_SOFA'
    rootgrp.Version = '1.0'
    rootgrp.SOFAConventions = 'AmbisonicsDRIR'
    rootgrp.SOFAConventionsVersion = '0.1'
    rootgrp.APIName = 'pysofaconventions'
    rootgrp.APIVersion = '0.1'
    rootgrp.APIVersion = '0.1'
    rootgrp.AuthorContact = 'andres.perez@eurecat.org'
    rootgrp.Organization = 'Eurecat - UPF'
    rootgrp.License = 'WTFPL - Do What the Fuck You Want to Public License'
    rootgrp.DataType = 'FIRE'
    rootgrp.RoomType = 'reverberant'
    rootgrp.DateCreated = time.ctime(time.time())
    rootgrp.DateModified = time.ctime(time.time())
    rootgrp.Title = 'testpysofaconventions'
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    raiseWarning('File convention is not SOFA')
    sofafile.close()

    # Valid convention, but missing dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.Conventions = 'SOFA'
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    raiseWarning('Dimension not found: M')
    sofafile.close()

    # Add required dimensions, missing Listener Variables
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('M', 4)
    rootgrp.createDimension('R', 5)
    rootgrp.createDimension('E', 6)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    raiseWarning('Missing Variable: ListenerPosition')
    sofafile.close()

    # Missing Source Variables
    rootgrp = Dataset(path, 'a')
    listenerPositionVar = rootgrp.createVariable('ListenerPosition', 'f8', ('I', 'C'))
    listenerPositionVar.Units = 'metre'
    listenerPositionVar.Type = 'cartesian'
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    raiseWarning('Missing Variable: SourcePosition')
    sofafile.close()

    # Missing Receiver Variables
    rootgrp = Dataset(path, 'a')
    sourcePositionVar = rootgrp.createVariable('SourcePosition', 'f8', ('I', 'C'))
    sourcePositionVar.Units = 'metre'
    sourcePositionVar.Type = 'cartesian'
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    raiseWarning('Missing Variable: ReceiverPosition')
    sofafile.close()

    # Missing Emitter Variables
    rootgrp = Dataset(path, 'a')
    receiverPositionVar = rootgrp.createVariable('ReceiverPosition', 'f8', ('R', 'C', 'I'))
    receiverPositionVar.Units = 'metre'
    receiverPositionVar.Type = 'cartesian'
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    raiseWarning('Missing Variable: EmitterPosition')
    sofafile.close()

    # Missing Data
    rootgrp = Dataset(path, 'a')
    emitterPositionVar = rootgrp.createVariable('EmitterPosition', 'f8', ('E', 'C', 'I'))
    emitterPositionVar.Units = 'metre'
    emitterPositionVar.Type = 'cartesian'
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    raiseWarning('Missing Data.IR Variable')
    sofafile.close()

    # # Now it should be fine
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'E', 'N'))
    sr = rootgrp.createVariable('Data.SamplingRate', 'f8', ('I',))
    sr.Units = 'hertz'
    rootgrp.createVariable('Data.Delay', 'f8', ('I','R', 'E'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.isValid()
    sofafile.close()

    os.remove(path)

def test_getFile():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getFile().__dict__ == rootgrp.__dict__
    sofafile.close()

    os.remove(path)


def test_getFilename():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getFilename() == path
    sofafile.close()

    os.remove(path)


def test_hasGlobalAttribute():

    attributeName = 'bestAttribute'

    # Attribute does not exist
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert not sofafile.hasGlobalAttribute(attributeName)
    sofafile.close()

    # Attribute exists
    rootgrp = Dataset(path, 'a')
    rootgrp.bestAttribute = 'yeah'
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.hasGlobalAttribute(attributeName)
    sofafile.close()

    os.remove(path)


def test_getGlobalAttributesAsDict():

    attrValue1 = 'attrValue1'
    attrValue2 = 'attrValue2'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.attr1 = attrValue1
    rootgrp.attr2 = attrValue2
    attrNameList = rootgrp.ncattrs()

    # Compare attribute names
    assert attrNameList ==  ['attr1','attr2']

    # Compare attribute values
    attrValueList = [getattr(rootgrp,attrName) for attrName in attrNameList]
    assert attrValueList == [attrValue1, attrValue2]

    rootgrp.close()
    os.remove(path)


def test_getGlobalAttributeValue():

    attrValue = 'A'

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.getGlobalAttributeValue('attr1')
        assert e.match(errorString)
        sofafile.close()

    # Attribute not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Attribute not found')

    # Attribute Found
    rootgrp = Dataset(path, 'a')
    rootgrp.attr1 = attrValue
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getGlobalAttributeValue('attr1') == attrValue

    os.remove(path)


def test_getDimensionsAsDict():

        # Empty dictionary
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()

    emptyDict = {}
    sofafile = SOFAFile(path, 'r')
    assert sofafile.getDimensionsAsDict() == emptyDict
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
    # Assert dimension names are equal
    for k1, k2 in zip(targetDict.keys(), sofafile.getDimensionsAsDict().keys()):
        assert k1 == k2
    # Assert dimension instances (value and name) are equal
    for v1, v2 in zip(targetDict.values(), sofafile.getDimensionsAsDict().values()):
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
    assert sofafile.getDimension('A') == sofafile.getDimensionsAsDict()['A']

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
    assert sofafile.getDimensionSize(variableName) == sofafile.getDimensionsAsDict()[variableName].size

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
    # Assert variable names are equal
    for k1, k2 in zip(variableDict.keys(), sofafile.getVariablesAsDict().keys()):
        assert k1 == k2
    # Assert variable instances are equal (through internal dict)
    for v1, v2 in zip(variableDict.values(), sofafile.getVariablesAsDict().values()):
        assert v1.__dict__ == v2.__dict__


    sofafile.close()

    os.remove(path)


def test_hasVariable():

    variableName = 'CoolVariable'

    # Variable does not exist
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert not sofafile.hasVariable(variableName)
    sofafile.close()

    # Variable exists
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable(variableName, 'f8', ())
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.hasVariable(variableName)
    sofafile.close()

    os.remove(path)


def test_getVariableShape():

    variableName = 'CoolVariable'
    dimensions = {'DIM1':1,'DIM2':2,'DIM3':3}
    numDimensions = len(dimensions)

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.getVariableShape(variableName)
        assert e.match(errorString)
        sofafile.close()

    # No such variable: SOFAError
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Variable not found')

    # Variable exists
    rootgrp = Dataset(path, 'a')
    for name, value in zip(dimensions.keys(), dimensions.values()):
        rootgrp.createDimension(name, value)
    var = rootgrp.createVariable(variableName, 'f8', tuple(dimensions.keys()))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getVariableShape(variableName) == tuple(dimensions.values())
    sofafile.close()

    os.remove(path)


def test_getVariableDimensionality():

    variableName = 'CoolVariable'
    dimensions = {'DIM1':1,'DIM2':2}
    numDimensions = len(dimensions)

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.getVariableDimensionality(variableName)
        assert e.match(errorString)
        sofafile.close()

    # No such variable: SOFAError
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Variable not found')

    # Variable exists
    rootgrp = Dataset(path, 'a')
    for name, value in zip(dimensions.keys(), dimensions.values()):
        rootgrp.createDimension(name, value)
    var = rootgrp.createVariable(variableName, 'f8', tuple(dimensions.keys()))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getVariableDimensionality(variableName) == numDimensions
    sofafile.close()

    os.remove(path)


def test_getVariableValue():

    variableName = 'CoolVariable'
    variableDim = 1
    variableValue = np.random.rand(variableDim)

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.getVariableValue(variableName)
        assert e.match(errorString)
        sofafile.close()

    # No such variable: SOFAError
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Variable not found')

    # Variable exists
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('I', variableDim)
    var = rootgrp.createVariable(variableName, 'f8', ('I'))
    var[:] = variableValue
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert np.array_equal(sofafile.getVariableValue(variableName), variableValue)
    sofafile.close()

    os.remove(path)


def test_getVariableInstance():

    variableName = 'CoolVariable'

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.getVariableInstance(variableName)
        assert e.match(errorString)
        sofafile.close()

    # No such variable: SOFAError
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Variable not found')

    # Variable exists
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable(variableName, 'f8', ())
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getVariableInstance(variableName).__dict__ == rootgrp[variableName].__dict__
    sofafile.close()

    os.remove(path)


def test_getVariableAttributeValue():

    variableName = 'CoolVariable'
    attributeValue = 'coolAttributeValue'

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.getVariableAttributeValue(variableName,'coolAttribute')
        assert e.match(errorString)
        sofafile.close()


    # No such variable: SOFAError
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Variable not found')

    # Variable exists, but not the attribute: None
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable(variableName, 'f8', ())
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getVariableAttributeValue(variableName,'coolAttribute') == None
    sofafile.close()

    # Both variable and attribute exist
    rootgrp = Dataset(path, 'a')
    var = rootgrp.variables[variableName]
    var.coolAttribute = attributeValue
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getVariableAttributeValue(variableName,'coolAttribute') == attributeValue
    sofafile.close()

    os.remove(path)


def test_getPositionVariableInfo():

    variableName = 'CoolVariable'
    unitsVar =  'myUnits'
    typeVar = 'greatType'

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.getPositionVariableInfo(variableName)
        assert e.match(errorString)
        sofafile.close()

    # No such variable: SOFAError
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Variable not found')

    # Variable exists, but not the attributes: None
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable(variableName, 'f8', ())
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getPositionVariableInfo(variableName) == (None, None)
    sofafile.close()

    # Both variable and attributes exist
    rootgrp = Dataset(path, 'a')
    var = rootgrp.variables[variableName]
    var.Units = unitsVar
    var.Type = typeVar
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    assert sofafile.getPositionVariableInfo(variableName) == (unitsVar, typeVar)
    sofafile.close()

    os.remove(path)

def test_hasListenerView():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert not SOFAFile(path, 'r').hasListenerView()

    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ListenerView', 'f8', ())
    rootgrp.close()
    assert SOFAFile(path, 'r').hasListenerView()

    os.remove(path)

def test_hasListenerUp():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert not SOFAFile(path, 'r').hasListenerUp()

    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ListenerUp', 'f8', ())
    rootgrp.close()
    assert SOFAFile(path, 'r').hasListenerUp()

    os.remove(path)


def test_hasSourceView():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert not SOFAFile(path, 'r').hasSourceView()

    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('SourceView', 'f8', ())
    rootgrp.close()
    assert SOFAFile(path, 'r').hasSourceView()

    os.remove(path)

def test_hasSourceUp():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert not SOFAFile(path, 'r').hasSourceUp()

    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('SourceUp', 'f8', ())
    rootgrp.close()
    assert SOFAFile(path, 'r').hasSourceUp()

    os.remove(path)


def test_hasReceiverView():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert not SOFAFile(path, 'r').hasReceiverView()

    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ReceiverView', 'f8', ())
    rootgrp.close()
    assert SOFAFile(path, 'r').hasReceiverView()

    os.remove(path)

def test_hasReceiverUp():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert not SOFAFile(path, 'r').hasReceiverUp()

    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ReceiverUp', 'f8', ())
    rootgrp.close()
    assert SOFAFile(path, 'r').hasReceiverUp()

    os.remove(path)


def test_hasEmitterView():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert not SOFAFile(path, 'r').hasEmitterView()

    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('EmitterView', 'f8', ())
    rootgrp.close()
    assert SOFAFile(path, 'r').hasEmitterView()

    os.remove(path)

def test_hasEmitterUp():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert not SOFAFile(path, 'r').hasEmitterUp()

    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('EmitterUp', 'f8', ())
    rootgrp.close()
    assert SOFAFile(path, 'r').hasEmitterUp()

    os.remove(path)


def test_getListenerPositionInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('ListenerPosition', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getListenerPositionInfo() ==  targetTuple
    os.remove(path)

def test_getListenerUpInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('ListenerUp', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getListenerUpInfo() ==  targetTuple
    os.remove(path)

def test_getListenerViewInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('ListenerView', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getListenerViewInfo() ==  targetTuple
    os.remove(path)


def test_getSourcePositionInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('SourcePosition', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getSourcePositionInfo() ==  targetTuple
    os.remove(path)

def test_getSourceUpInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('SourceUp', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getSourceUpInfo() ==  targetTuple
    os.remove(path)

def test_getSourceViewInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('SourceView', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getSourceViewInfo() ==  targetTuple
    os.remove(path)


def test_getReceiverPositionInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('ReceiverPosition', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getReceiverPositionInfo() ==  targetTuple
    os.remove(path)

def test_getReceiverUpInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('ReceiverUp', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getReceiverUpInfo() ==  targetTuple
    os.remove(path)

def test_getReceiverViewInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('ReceiverView', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getReceiverViewInfo() ==  targetTuple
    os.remove(path)


def test_getEmitterPositionInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('EmitterPosition', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getEmitterPositionInfo() ==  targetTuple
    os.remove(path)

def test_getEmitterUpInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('EmitterUp', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getEmitterUpInfo() ==  targetTuple
    os.remove(path)

def test_getEmitterViewInfo():

    units = 'Unit'
    type = 'Type'
    targetTuple = (units, type)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    var = rootgrp.createVariable('EmitterView', 'f8', ())
    var.Units = units
    var.Type = type
    rootgrp.close()

    assert SOFAFile(path, 'r').getEmitterViewInfo() ==  targetTuple
    os.remove(path)


def test_getListenerPositionValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('ListenerPosition', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getListenerPositionValues(), targetArray)
    os.remove(path)

def test_getListenerUpValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('ListenerUp', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getListenerUpValues(), targetArray)
    os.remove(path)

def test_getListenerViewValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('ListenerView', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getListenerViewValues(), targetArray)
    os.remove(path)

def test_getSourcePositionValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('SourcePosition', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getSourcePositionValues(), targetArray)
    os.remove(path)

def test_getSourceUpValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('SourceUp', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getSourceUpValues(), targetArray)
    os.remove(path)

def test_getSourceViewValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('SourceView', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getSourceViewValues(), targetArray)
    os.remove(path)

def test_getReceiverPositionValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('ReceiverPosition', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getReceiverPositionValues(), targetArray)
    os.remove(path)

def test_getReceiverUpValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('ReceiverUp', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getReceiverUpValues(), targetArray)
    os.remove(path)

def test_getReceiverViewValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('ReceiverView', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getReceiverViewValues(), targetArray)
    os.remove(path)

def test_getEmitterPositionValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('EmitterPosition', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getEmitterPositionValues(), targetArray)
    os.remove(path)

def test_getEmitterUpValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('EmitterUp', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getEmitterUpValues(), targetArray)
    os.remove(path)

def test_getEmitterViewValues():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    var = rootgrp.createVariable('EmitterView', 'f8', ('DIM1','DIM2'))
    var[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getEmitterViewValues(), targetArray)
    os.remove(path)


def test_getDataIR():

    dim1 = 2
    dim2 = 5
    targetArray = np.random.rand(dim1,dim2)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    rootgrp.createDimension('DIM2', dim2)
    ir = rootgrp.createVariable('Data.IR', 'f8', ('DIM1','DIM2'))
    ir[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getDataIR(), targetArray)
    os.remove(path)

def test_getDataDelay():

    dim1 = 2
    targetArray = np.random.rand(dim1)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    delay = rootgrp.createVariable('Data.Delay', 'f8', ('DIM1'))
    delay[:] = targetArray
    rootgrp.close()

    assert np.array_equal(SOFAFile(path, 'r').getDataDelay(), targetArray)
    os.remove(path)

def test_getSamplingRate():

    dim1 = 2
    targetArray = np.random.rand(dim1)

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    sr = rootgrp.createVariable('Data.SamplingRate', 'f8', ('DIM1'))
    sr[:] = targetArray

    assert np.array_equal(SOFAFile(path, 'r').getSamplingRate(), targetArray)
    os.remove(path)

def test_getSamplingRateUnits():

    dim1 = 2
    targetString = 'Kelvin'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    sr = rootgrp.createVariable('Data.SamplingRate', 'f8', ('DIM1'))
    sr.Units = targetString
    rootgrp.close()

    assert SOFAFile(path, 'r').getSamplingRateUnits() == targetString
    os.remove(path)

def test_getDataIRChannelOrdering():

    dim1 = 2
    targetString = 'incredibleChannelOrdering'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    ir = rootgrp.createVariable('Data.IR', 'f8', ('DIM1'))
    ir.ChannelOrdering = targetString
    rootgrp.close()

    assert SOFAFile(path, 'r').getDataIRChannelOrdering() == targetString
    os.remove(path)

def test_getDataIRNormalization():

    dim1 = 2
    targetString = 'amazingNormalization'

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('DIM1', dim1)
    ir = rootgrp.createVariable('Data.IR', 'f8', ('DIM1'))
    ir.Normalization = targetString
    rootgrp.close()

    assert SOFAFile(path, 'r').getDataIRNormalization() == targetString
    os.remove(path)


# Custom class for print asserts
class MyOutput(object):
    def __init__(self):
        self.data = []

    def write(self, s):
        self.data.append(s)

    def __str__(self):
        return "".join(self.data)


def test_printSOFAGlobalAttributes():

    # Replace sys out by our out to compare the strings
    stdout_org = sys.stdout
    my_stdout = MyOutput()

    # Create custom file with attributes
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.A = 'a'
    rootgrp.B = 'b'
    rootgrp.close()

    # This should be the output
    targetString = "- A\n\ta\n- B\n\tb\n"

    # Produce some output
    try:
        sys.stdout = my_stdout
        SOFAFile(path, 'r').printSOFAGlobalAttributes()
        os.remove(path)
    finally:
        sys.stdout = stdout_org

    # Assert
    assert str(my_stdout) == targetString


def test_printSOFADimensions():

    # Replace sys out by our out to compare the strings
    stdout_org = sys.stdout
    my_stdout = MyOutput()

    # Create custom file with dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('A', 1)
    rootgrp.createDimension('B', 2)
    rootgrp.close()

    # This should be the output
    targetString = "- A : 1\n- B : 2\n"

    # Produce some output
    try:
        sys.stdout = my_stdout
        SOFAFile(path, 'r').printSOFADimensions()
        os.remove(path)
    finally:
        sys.stdout = stdout_org

    # Assert
    assert str(my_stdout) == targetString


def test_printSOFAVariables():

    # Replace sys out by our out to compare the strings
    stdout_org = sys.stdout
    my_stdout = MyOutput()

    # Create custom file with variables
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('A', 1)
    rootgrp.createDimension('B', 2)
    rootgrp.createVariable('CoolVariable', 'f8', ('A'))
    rootgrp.createVariable('UltraVariable', 'f8', ('A', 'B'))
    rootgrp.close()

    # This should be the output
    targetString = "- CoolVariable = (1,)\n- UltraVariable = (1, 2)\n"

    # Produce some output
    try:
        sys.stdout = my_stdout
        SOFAFile(path, 'r').printSOFAVariables()
        os.remove(path)
    finally:
        sys.stdout = stdout_org

    # Assert
    assert str(my_stdout) == targetString


def test_getSOFADimensionStrings():

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 1)
    rootgrp.createDimension('A', 2)
    rootgrp.close()

    # Explanatory string for known variables
    targetString = "Number of measurements (M)"
    assert SOFAFile(path, 'r').getSOFADimensionStrings('M') == targetString

    # Return symbol for unknown variables
    targetString = "A"
    assert SOFAFile(path, 'r').getSOFADimensionStrings('A') == targetString

    os.remove(path)

def test_getConventionVersion():

    # This should be the output for base SOFAFile
    targetString = "None.None"

    assert SOFAFile.getConventionVersion() == targetString


def test_checkSOFARequiredAttributes():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkSOFARequiredAttributes()
        assert e.match(errorString)
        sofafile.close()

    # SOFA file with missing attributes
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Missing required attribute: APIName')


    # Assert all attributes
    rootgrp = Dataset(path, 'a')
    rootgrp.Conventions = 'SOFA'
    rootgrp.Version = '1.0'
    rootgrp.SOFAConventions = 'AmbisonicsDRIR'
    rootgrp.SOFAConventionsVersion = '0.1'
    rootgrp.APIName = 'pysofaconventions'
    rootgrp.APIVersion = '0.1'
    rootgrp.APIVersion = '0.1'
    rootgrp.AuthorContact = 'andres.perez@eurecat.org'
    rootgrp.Organization = 'Eurecat - UPF'
    rootgrp.License = 'WTFPL - Do What the Fuck You Want to Public License'
    rootgrp.DataType = 'FIRE'
    rootgrp.RoomType = 'reverberant'
    rootgrp.DateCreated = time.ctime(time.time())
    rootgrp.DateModified = time.ctime(time.time())
    rootgrp.Title = 'testpysofaconventions'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkSOFARequiredAttributes()
    os.remove(path)


def test_checkSOFAConvention():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkSOFAConvention()
        assert e.match(errorString)
        sofafile.close()

    # Incorrect Conventions string
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.Conventions = 'Incorrect_string'
    rootgrp.close()
    raiseError('File convention is not SOFA')

    # Correct string
    rootgrp = Dataset(path, 'a')
    rootgrp.Conventions = 'SOFA'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkSOFAConvention()
    os.remove(path)


def test_checkSOFADimensionsAreValid():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkSOFADimensionsAreValid()
        assert e.match(errorString)
        sofafile.close()

    ## MISSING DIMENSIONS

    # Missing M
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Dimension not found: M')

    # Missing N
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('M', 1)
    rootgrp.close()
    raiseError('Dimension not found: N')

    # Missing R
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('N', 1)
    rootgrp.close()
    raiseError('Dimension not found: R')

    # Missing E
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('R', 1)
    rootgrp.close()
    raiseError('Dimension not found: E')

    # Missing I
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('E', 1)
    rootgrp.close()
    raiseError('Dimension not found: I')

    # Missing C
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('I', 1)
    rootgrp.close()
    raiseError('Dimension not found: C')

    os.remove(path)


    ## INCORRECT VALUES FOR DIMENSIONS

    # M < 1
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 0)
    rootgrp.createDimension('N', 1)
    rootgrp.createDimension('R', 1)
    rootgrp.createDimension('E', 1)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.close()
    raiseError('Incorrect dimension size for M')
    os.remove(path)

    # N < 1
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 1)
    rootgrp.createDimension('N', 0)
    rootgrp.createDimension('R', 1)
    rootgrp.createDimension('E', 1)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.close()
    raiseError('Incorrect dimension size for N')
    os.remove(path)

    # R < 1
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 1)
    rootgrp.createDimension('N', 1)
    rootgrp.createDimension('R', 0)
    rootgrp.createDimension('E', 1)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.close()
    raiseError('Incorrect dimension size for R')
    os.remove(path)

    # E < 1
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 1)
    rootgrp.createDimension('N', 1)
    rootgrp.createDimension('R', 1)
    rootgrp.createDimension('E', 0)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.close()
    raiseError('Incorrect dimension size for E')
    os.remove(path)

    # I != 1
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 1)
    rootgrp.createDimension('N', 1)
    rootgrp.createDimension('R', 1)
    rootgrp.createDimension('E', 1)
    rootgrp.createDimension('I', 2)
    rootgrp.createDimension('C', 3)
    rootgrp.close()
    raiseError('Incorrect dimension size for I')
    os.remove(path)

    # C != 3
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 1)
    rootgrp.createDimension('N', 1)
    rootgrp.createDimension('R', 1)
    rootgrp.createDimension('E', 1)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 4)
    rootgrp.close()
    raiseError('Incorrect dimension size for C')
    os.remove(path)

    # All fine
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 1)
    rootgrp.createDimension('N', 1)
    rootgrp.createDimension('R', 1)
    rootgrp.createDimension('E', 1)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.close()
    assert SOFAFile(path, 'r').checkSOFADimensionsAreValid()
    os.remove(path)


def test_checkListenerVariables():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkListenerVariables()
        assert e.match(errorString)
        sofafile.close()

    # Missing ListenerPosition Variable
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Missing Variable: ListenerPosition')

    # Missing ListenerPosition.Units
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('M', 2)
    rootgrp.createVariable('ListenerPosition', 'f8', ('I', 'C'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: ListenerPosition.Units')

    # Missing ListenerPosition.Coordinates
    rootgrp = Dataset(path, 'a')
    listenerPositionVar = rootgrp.variables['ListenerPosition']
    listenerPositionVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: ListenerPosition.Coordinates')

    # Add ListenerPosition.Coordinates, now it should be fine
    rootgrp = Dataset(path, 'a')
    listenerPositionVar = rootgrp.variables['ListenerPosition']
    listenerPositionVar.Type = 'cartesian'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkListenerVariables()
    os.remove(path)


    # Add ListenerUp, missing Units
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('M', 1)
    listenerPositionVar = rootgrp.createVariable('ListenerPosition', 'f8', ('I', 'C'))
    listenerPositionVar.Units = 'metre'
    listenerPositionVar.Type = 'cartesian'
    rootgrp.createVariable('ListenerUp', 'f8', ('I', 'C'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: ListenerUp.Units')

    # Missing ListenerUp.Coordinates
    rootgrp = Dataset(path, 'a')
    listenerUpVar = rootgrp.variables['ListenerUp']
    listenerUpVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: ListenerUp.Coordinates')

    # Add ListenerView, missing Units
    rootgrp = Dataset(path, 'a')
    listenerUpVar = rootgrp.variables['ListenerUp']
    listenerUpVar.Type = 'cartesian'
    rootgrp.createVariable('ListenerView', 'f8', ('I', 'C'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: ListenerView.Units')

    # Missing ListenerView.Coordinates
    rootgrp = Dataset(path, 'a')
    listenerViewVar = rootgrp.variables['ListenerView']
    listenerViewVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: ListenerView.Coordinates')

    # Add ListenerUp, now it's all fine
    rootgrp = Dataset(path, 'a')
    listenerViewVar = rootgrp.variables['ListenerView']
    listenerViewVar.Type = 'cartesian'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkListenerVariables()
    os.remove(path)



def test_checkSourceVariables():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkSourceVariables()
        assert e.match(errorString)
        sofafile.close()

    # Missing SourcePosition Variable
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Missing Variable: SourcePosition')

    # Missing SourcePosition.Units
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('M', 2)
    rootgrp.createVariable('SourcePosition', 'f8', ('I', 'C'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: SourcePosition.Units')

    # Missing SourcePosition.Coordinates
    rootgrp = Dataset(path, 'a')
    sourcePositionVar = rootgrp.variables['SourcePosition']
    sourcePositionVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: SourcePosition.Coordinates')

    # Add SourcePosition.Coordinates, now it should be fine
    rootgrp = Dataset(path, 'a')
    sourcePositionVar = rootgrp.variables['SourcePosition']
    sourcePositionVar.Type = 'cartesian'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkSourceVariables()
    os.remove(path)


    # Add SourceUp, missing Units
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('M', 1)
    sourcePositionVar = rootgrp.createVariable('SourcePosition', 'f8', ('I', 'C'))
    sourcePositionVar.Units = 'metre'
    sourcePositionVar.Type = 'cartesian'
    rootgrp.createVariable('SourceUp', 'f8', ('I', 'C'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: SourceUp.Units')

    # Missing SourceUp.Coordinates
    rootgrp = Dataset(path, 'a')
    sourceUpVar = rootgrp.variables['SourceUp']
    sourceUpVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: SourceUp.Coordinates')

    # Add SourceView, missing Units
    rootgrp = Dataset(path, 'a')
    sourceUpVar = rootgrp.variables['SourceUp']
    sourceUpVar.Type = 'cartesian'
    rootgrp.createVariable('SourceView', 'f8', ('I', 'C'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: SourceView.Units')

    # Missing SourceView.Coordinates
    rootgrp = Dataset(path, 'a')
    sourceViewVar = rootgrp.variables['SourceView']
    sourceViewVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: SourceView.Coordinates')

    # Add SourceUp, now it's all fine
    rootgrp = Dataset(path, 'a')
    sourceViewVar = rootgrp.variables['SourceView']
    sourceViewVar.Type = 'cartesian'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkSourceVariables()
    os.remove(path)



def test_checkReceiverVariables():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkReceiverVariables()
        assert e.match(errorString)
        sofafile.close()

    # Missing ReceiverPosition Variable
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Missing Variable: ReceiverPosition')

    # Missing ReceiverPosition.Units
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('R', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('M', 2)
    rootgrp.createVariable('ReceiverPosition', 'f8', ('R', 'C', 'I'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: ReceiverPosition.Units')

    # Missing ReceiverPosition.Coordinates
    rootgrp = Dataset(path, 'a')
    receiverPositionVar = rootgrp.variables['ReceiverPosition']
    receiverPositionVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: ReceiverPosition.Coordinates')

    # Add ReceiverPosition.Coordinates, now it should be fine
    rootgrp = Dataset(path, 'a')
    receiverPositionVar = rootgrp.variables['ReceiverPosition']
    receiverPositionVar.Type = 'cartesian'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkReceiverVariables()
    os.remove(path)


    # Add ReceiverUp, missing Units
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('R', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('M', 1)
    receiverPositionVar = rootgrp.createVariable('ReceiverPosition', 'f8', ('R', 'C', 'I'))
    receiverPositionVar.Units = 'metre'
    receiverPositionVar.Type = 'cartesian'
    rootgrp.createVariable('ReceiverUp', 'f8', ('R', 'C', 'I'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: ReceiverUp.Units')

    # Missing ReceiverUp.Coordinates
    rootgrp = Dataset(path, 'a')
    receiverUpVar = rootgrp.variables['ReceiverUp']
    receiverUpVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: ReceiverUp.Coordinates')

    # Add ReceiverView, missing Units
    rootgrp = Dataset(path, 'a')
    receiverUpVar = rootgrp.variables['ReceiverUp']
    receiverUpVar.Type = 'cartesian'
    rootgrp.createVariable('ReceiverView', 'f8', ('R', 'C', 'I'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: ReceiverView.Units')

    # Missing ReceiverView.Coordinates
    rootgrp = Dataset(path, 'a')
    receiverViewVar = rootgrp.variables['ReceiverView']
    receiverViewVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: ReceiverView.Coordinates')

    # Add ReceiverUp, now it's all fine
    rootgrp = Dataset(path, 'a')
    receiverViewVar = rootgrp.variables['ReceiverView']
    receiverViewVar.Type = 'cartesian'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkReceiverVariables()
    os.remove(path)


def test_checkEmitterVariables():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkEmitterVariables()
        assert e.match(errorString)
        sofafile.close()

    # Missing EmitterPosition Variable
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Missing Variable: EmitterPosition')

    # Missing EmitterPosition.Units
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('E', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('M', 2)
    rootgrp.createVariable('EmitterPosition', 'f8', ('E', 'C', 'I'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: EmitterPosition.Units')

    # Missing EmitterPosition.Coordinates
    rootgrp = Dataset(path, 'a')
    emitterPositionVar = rootgrp.variables['EmitterPosition']
    emitterPositionVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: EmitterPosition.Coordinates')

    # Add EmitterPosition.Coordinates, now it should be fine
    rootgrp = Dataset(path, 'a')
    emitterPositionVar = rootgrp.variables['EmitterPosition']
    emitterPositionVar.Type = 'cartesian'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkEmitterVariables()
    os.remove(path)


    # Add EmitterUp, missing Units
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('E', 1)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('M', 1)
    emitterPositionVar = rootgrp.createVariable('EmitterPosition', 'f8', ('E', 'C', 'I'))
    emitterPositionVar.Units = 'metre'
    emitterPositionVar.Type = 'cartesian'
    rootgrp.createVariable('EmitterUp', 'f8', ('E', 'C', 'I'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: EmitterUp.Units')

    # Missing EmitterUp.Coordinates
    rootgrp = Dataset(path, 'a')
    emitterUpVar = rootgrp.variables['EmitterUp']
    emitterUpVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: EmitterUp.Coordinates')

    # Add EmitterView, missing Units
    rootgrp = Dataset(path, 'a')
    emitterUpVar = rootgrp.variables['EmitterUp']
    emitterUpVar.Type = 'cartesian'
    rootgrp.createVariable('EmitterView', 'f8', ('E', 'C', 'I'))
    rootgrp.close()
    raiseError('Missing Variable Attribute: EmitterView.Units')

    # Missing EmitterView.Coordinates
    rootgrp = Dataset(path, 'a')
    emitterViewVar = rootgrp.variables['EmitterView']
    emitterViewVar.Units = 'metre'
    rootgrp.close()
    raiseError('Missing Variable Attribute: EmitterView.Coordinates')

    # Add EmitterUp, now it's all fine
    rootgrp = Dataset(path, 'a')
    emitterViewVar = rootgrp.variables['EmitterView']
    emitterViewVar.Type = 'cartesian'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkEmitterVariables()
    os.remove(path)


def test_checkDataVariable():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkDataVariable()
        assert e.match(errorString)
        sofafile.close()

    # Missing GLOBAL.DataType attribute
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('No DataType attribute')

    # DataType not known
    rootgrp = Dataset(path, 'a')
    rootgrp.DataType = 'FAKE'
    rootgrp.close()
    raiseError('DataType not known')

    # Assert correct Data
    rootgrp = Dataset(path, 'a')
    rootgrp.DataType = 'FIR'
    rootgrp.createDimension('M', 1)
    rootgrp.createDimension('N', 1)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 1)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'I'))
    sr = rootgrp.createVariable('Data.SamplingRate', 'f8', ('I',))
    sr.Units = 'hertz'
    rootgrp.createVariable('Data.Delay', 'f8', ('I','R'))
    rootgrp.close()
    assert SOFAFile(path, 'r').checkDataVariable()
    os.remove(path)

def test_isFIRDataType():

    # Assert proper data type assignment
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.DataType = 'FIR'
    rootgrp.close()
    assert SOFAFile(path, 'r').isFIRDataType()
    os.remove(path)

def test_isFIREDataType():

    # Assert proper data type assignment
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.DataType = 'FIRE'
    rootgrp.close()
    assert SOFAFile(path, 'r').isFIREDataType()
    os.remove(path)

def test_isSOSDataType():

    # Assert proper data type assignment
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.DataType = 'SOS'
    rootgrp.close()
    assert SOFAFile(path, 'r').isSOSDataType()
    os.remove(path)

def test_isTFDataType():

    # Assert proper data type assignment
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.DataType = 'TF'
    rootgrp.close()
    assert SOFAFile(path, 'r').isTFDataType()
    os.remove(path)



def test_checkFIRDataType():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkFIRDataType()
        assert e.match(errorString)
        sofafile.close()

    # Missing M
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Dimension not found: M')

    # Missing N
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('M', 3)
    rootgrp.close()
    raiseError('Dimension not found: N')

    # Missing I
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('N', 2)
    rootgrp.close()
    raiseError('Dimension not found: I')

    # Missing R
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('I', 1)
    rootgrp.close()
    raiseError('Dimension not found: R')

    # Missing Data.IR
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('R', 4)
    rootgrp.close()
    raiseError('Missing Data.IR Variable')

    # Incorrect Data.IR dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.IR', 'f8', ('N', 'M', 'R'))
    rootgrp.close()
    raiseError('Incorrect Data.IR dimensions:')
    os.remove(path)


    # Missing Data.SamplingRate
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'N'))
    rootgrp.close()
    raiseError('Missing Data.SamplingRate Variable')

    # Incorrect Data.SamplingRate dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.SamplingRate', 'f8', ('N', 'M', 'R'))
    rootgrp.close()
    raiseError('Incorrect Data.SamplingRate dimensions:')
    os.remove(path)

    # Missing Data.SamplingRate.Units
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'N'))
    rootgrp.createVariable('Data.SamplingRate', 'f8', ('I',))
    rootgrp.close()
    raiseError('Missing Attribute Data.SamplingRate.Units')

    # Add Data.SamplingRate.Units, incorrect Type
    rootgrp = Dataset(path, 'a')
    sr = rootgrp.variables['Data.SamplingRate']
    sr.Units = 'Kelvin'
    rootgrp.close()
    raiseError('Attribute Data.SamplingRate.Units is not a frequency unit')

    # Fix Type. Missing Data.Delay variable
    rootgrp = Dataset(path, 'a')
    sr = rootgrp.variables['Data.SamplingRate']
    sr.Units = 'hertz'
    rootgrp.close()
    raiseError('Missing Data.Delay Variable')

    # Add Data.Delay, incorrect dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.Delay', 'f8', ('R', 'N'))
    rootgrp.close()
    raiseError('Incorrect Data.Delay dimensions')
    os.remove(path)

    # Assert everything is correct
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'N'))
    sr = rootgrp.createVariable('Data.SamplingRate', 'f8', ('I',))
    sr.Units = 'hertz'
    rootgrp.createVariable('Data.Delay', 'f8', ('I', 'R'))
    rootgrp.close()
    assert SOFAFile(path, 'r').checkFIRDataType()
    os.remove(path)


def test_checkFIREDataType():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkFIREDataType()
        assert e.match(errorString)
        sofafile.close()

    # Missing M
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Dimension not found: M')

    # Missing N
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('M', 3)
    rootgrp.close()
    raiseError('Dimension not found: N')

    # Missing I
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('N', 2)
    rootgrp.close()
    raiseError('Dimension not found: I')

    # Missing R
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('I', 1)
    rootgrp.close()
    raiseError('Dimension not found: R')

    # Missing E
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('R', 4)
    rootgrp.close()
    raiseError('Dimension not found: E')

    # Missing Data.IR
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('E', 5)
    rootgrp.close()
    raiseError('Missing Data.IR Variable')

    # Incorrect Data.IR dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.IR', 'f8', ('N', 'E', 'M', 'R'))
    rootgrp.close()
    raiseError('Incorrect Data.IR dimensions:')
    os.remove(path)


    # Missing Data.SamplingRate
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createDimension('E', 5)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'E', 'N'))
    rootgrp.close()
    raiseError('Missing Data.SamplingRate Variable')

    # Incorrect Data.SamplingRate dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.SamplingRate', 'f8', ('N', 'M', 'R'))
    rootgrp.close()
    raiseError('Incorrect Data.SamplingRate dimensions:')
    os.remove(path)

    # Missing Data.SamplingRate.Units
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createDimension('E', 5)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'E', 'N'))
    rootgrp.createVariable('Data.SamplingRate', 'f8', ('I',))
    rootgrp.close()
    raiseError('Missing Attribute Data.SamplingRate.Units')

    # Add Data.SamplingRate.Units, incorrect Type
    rootgrp = Dataset(path, 'a')
    sr = rootgrp.variables['Data.SamplingRate']
    sr.Units = 'Kelvin'
    rootgrp.close()
    raiseError('Attribute Data.SamplingRate.Units is not a frequency unit')

    # Fix Type. Missing Data.Delay variable
    rootgrp = Dataset(path, 'a')
    sr = rootgrp.variables['Data.SamplingRate']
    sr.Units = 'hertz'
    rootgrp.close()
    raiseError('Missing Data.Delay Variable')

    # Add Data.Delay, incorrect dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.Delay', 'f8', ('R', 'N'))
    rootgrp.close()
    raiseError('Incorrect Data.Delay dimensions')
    os.remove(path)

    # Assert everything is correct
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createDimension('E', 5)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'E', 'N'))
    sr = rootgrp.createVariable('Data.SamplingRate', 'f8', ('I',))
    sr.Units = 'hertz'
    rootgrp.createVariable('Data.Delay', 'f8', ('I', 'R', 'E'))
    rootgrp.close()
    assert SOFAFile(path, 'r').checkFIREDataType()
    os.remove(path)



def test_checkSOSDataType():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkSOSDataType()
        assert e.match(errorString)
        sofafile.close()

    # Missing M
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Dimension not found: M')

    # Missing N
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('M', 3)
    rootgrp.close()
    raiseError('Dimension not found: N')

    # Missing I
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('N', 2)
    rootgrp.close()
    raiseError('Dimension not found: I')

    # Missing R
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('I', 1)
    rootgrp.close()
    raiseError('Dimension not found: R')

    # Missing Data.IR
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('R', 4)
    rootgrp.close()
    raiseError('Missing Data.IR Variable')

    # Incorrect Data.IR dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.IR', 'f8', ('N', 'M', 'R'))
    rootgrp.close()
    raiseError('Incorrect Data.IR dimensions:')
    os.remove(path)


    # Missing Data.SamplingRate
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'N'))
    rootgrp.close()
    raiseError('Missing Data.SamplingRate Variable')

    # Incorrect Data.SamplingRate dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.SamplingRate', 'f8', ('N', 'M', 'R'))
    rootgrp.close()
    raiseError('Incorrect Data.SamplingRate dimensions:')
    os.remove(path)

    # Missing Data.SamplingRate.Units
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'N'))
    rootgrp.createVariable('Data.SamplingRate', 'f8', ('I',))
    rootgrp.close()
    raiseError('Missing Attribute Data.SamplingRate.Units')

    # Add Data.SamplingRate.Units, incorrect Type
    rootgrp = Dataset(path, 'a')
    sr = rootgrp.variables['Data.SamplingRate']
    sr.Units = 'Kelvin'
    rootgrp.close()
    raiseError('Attribute Data.SamplingRate.Units is not a frequency unit')

    # Fix Type. Missing Data.Delay variable
    rootgrp = Dataset(path, 'a')
    sr = rootgrp.variables['Data.SamplingRate']
    sr.Units = 'hertz'
    rootgrp.close()
    raiseError('Missing Data.Delay Variable')

    # Add Data.Delay, incorrect dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.Delay', 'f8', ('R', 'N'))
    rootgrp.close()
    raiseError('Incorrect Data.Delay dimensions')
    os.remove(path)

    # Assert everything is correct
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'N'))
    sr = rootgrp.createVariable('Data.SamplingRate', 'f8', ('I',))
    sr.Units = 'hertz'
    rootgrp.createVariable('Data.Delay', 'f8', ('I', 'R'))
    rootgrp.close()
    assert SOFAFile(path, 'r').checkSOSDataType()
    os.remove(path)


def test_checkTFDataType():

    def raiseError(errorString):
        sofafile = SOFAFile(path, 'r')
        with pytest.raises(SOFAError) as e:
            sofafile.checkTFDataType()
        assert e.match(errorString)
        sofafile.close()

    # Missing M
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseError('Dimension not found: M')

    # Missing N
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('M', 3)
    rootgrp.close()
    raiseError('Dimension not found: N')

    # Missing I
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('N', 2)
    rootgrp.close()
    raiseError('Dimension not found: I')

    # Missing R
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('I', 1)
    rootgrp.close()
    raiseError('Dimension not found: R')

    # Missing Data.Real
    rootgrp = Dataset(path, 'a')
    rootgrp.createDimension('R', 4)
    rootgrp.close()
    raiseError('Missing Data.Real Variable')

    # Incorrect Data.Real dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.Real', 'f8', ('N', 'M', 'R'))
    rootgrp.close()
    raiseError('Incorrect Data.Real dimensions:')
    os.remove(path)

    # Missing Data.Imag
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createVariable('Data.Real', 'f8', ('M', 'R', 'N'))
    rootgrp.close()
    raiseError('Missing Data.Imag Variable')

    # Incorrect Data.Imag dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('Data.Imag', 'f8', ('N', 'M', 'R'))
    rootgrp.close()
    raiseError('Incorrect Data.Imag dimensions:')
    os.remove(path)

    # Missing N
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createVariable('Data.Real', 'f8', ('M', 'R', 'N'))
    rootgrp.createVariable('Data.Imag', 'f8', ('M', 'R', 'N'))
    rootgrp.close()
    raiseError('Missing N Variable')

    # Incorrect N dimension
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('N', 'f8', ('R',))
    rootgrp.close()
    raiseError('Incorrect N dimensions')
    os.remove(path)


    # Missing N.Units
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('M', 3)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('R', 4)
    rootgrp.createVariable('Data.Real', 'f8', ('M', 'R', 'N'))
    rootgrp.createVariable('Data.Imag', 'f8', ('M', 'R', 'N'))
    rootgrp.createVariable('N', 'f8', ('N',))
    rootgrp.close()
    raiseError('Missing Attribute N.Units')

    # Add N.Units, incorrect Type
    rootgrp = Dataset(path, 'a')
    sr = rootgrp.variables['N']
    sr.Units = 'Kelvin'
    rootgrp.close()
    raiseError('Attribute N.Units is not a frequency unit')


    # Assert everything is correct
    rootgrp = Dataset(path, 'a')
    n = rootgrp.variables['N']
    n.Units = 'hertz'
    rootgrp.close()
    assert SOFAFile(path, 'r').checkTFDataType()
    os.remove(path)