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
#   @file   test_SOFASource.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
import os
import tempfile
from netCDF4 import Dataset
from pysofaconventions import *


def test_checkOptionalVariables():

    # SourceUp exists, but not SourceView
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    sourceUp = rootgrp.createVariable('SourceUp', 'f8', ())
    rootgrp.close()

    with pytest.raises(SOFAError) as e:
        SOFASource(None,sourceUp,None) # Internally calls checkOptionalVariables()
    assert e.match('SourceUp exists but not SourceView')
    os.remove(path)


    # SourceView exists, but not SourceUp
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    sourceView = rootgrp.createVariable('SourceView', 'f8', ())
    rootgrp.close()

    with pytest.raises(SOFAError) as e:
        SOFASource(None,None,sourceView) # Internally calls checkOptionalVariables()
    assert e.match('SourceView exists but not SourceUp')
    os.remove(path)


    # None of them exists
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert SOFASource(None,None,None).checkOptionalVariables()


    # Both of them exist
    rootgrp = Dataset(path, 'a')
    sourceUp = rootgrp.createVariable('SourceUp', 'f8', ())
    sourceView = rootgrp.createVariable('SourceView', 'f8', ())
    rootgrp.close()
    assert SOFASource(None, sourceUp, sourceView).checkOptionalVariables()

    os.remove(path)



def test_hasValidDimensions():

    i = 1
    c = 3
    m = 4

    # SourcePosition not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        SOFASource(None,None,None).hasValidDimensions(i,c,m)
    assert error.match('SourcePosition Variable not found!')

    # Invalid SourcePosition dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('SourcePosition', 'f8', ('C','M'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        sourcePosition = sofafile.getVariableInstance('SourcePosition')
        SOFASource(sourcePosition,None,None).hasValidDimensions(i,c,m)
    assert error.match('Invalid SourcePosition Dimensions')

    sofafile.close()
    os.remove(path)

    # Invalid SourceUp dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('SourcePosition', 'f8', ('I', 'C'))
    rootgrp.createVariable('SourceUp', 'f8', ('C','M'))
    rootgrp.createVariable('SourceView', 'f8', ('I', 'C'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        sourcePosition = sofafile.getVariableInstance('SourcePosition')
        sourceUp = sofafile.getVariableInstance('SourceUp')
        sourceView = sofafile.getVariableInstance('SourceView')
        SOFASource(sourcePosition,sourceUp,sourceView).hasValidDimensions(i,c,m)
    assert error.match('Invalid SourceUp Dimensions')

    sofafile.close()
    os.remove(path)

    # Invalid SourceView dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('SourcePosition', 'f8', ('I', 'C'))
    rootgrp.createVariable('SourceUp', 'f8', ('I', 'C'))
    rootgrp.createVariable('SourceView', 'f8', ('C','M'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        sourcePosition = sofafile.getVariableInstance('SourcePosition')
        sourceUp = sofafile.getVariableInstance('SourceUp')
        sourceView = sofafile.getVariableInstance('SourceView')
        SOFASource(sourcePosition, sourceUp, sourceView).hasValidDimensions(i,c,m)
    assert error.match('Invalid SourceView Dimensions')

    sofafile.close()
    os.remove(path)

    # Valid dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('SourcePosition', 'f8', ('I', 'C'))
    rootgrp.createVariable('SourceUp', 'f8', ('I', 'C'))
    rootgrp.createVariable('SourceView', 'f8', ('I', 'C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sourcePosition = sofafile.getVariableInstance('SourcePosition')
    sourceUp = sofafile.getVariableInstance('SourceUp')
    sourceView = sofafile.getVariableInstance('SourceView')
    assert SOFASource(sourcePosition, sourceUp, sourceView).hasValidDimensions(i,c,m)

    sofafile.close()
    os.remove(path)


def test_sourcePositionHasDimensions():

    i = 1
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('SourcePosition', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sourcePosition = sofafile.getVariableInstance('SourcePosition')
    sofaSource = SOFASource(sourcePosition,None,None)

    # Dimensions do not match
    assert not sofaSource.sourcePositionHasDimensions(i,m)

    # Dimensions match
    assert sofaSource.sourcePositionHasDimensions(i,c)

    sofafile.close()
    os.remove(path)


def test_sourceUpHasDimensions():

    i = 1
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('SourceUp', 'f8', ('I','C'))
    rootgrp.createVariable('SourceView', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sourceUp = sofafile.getVariableInstance('SourceUp')
    sourceView = sofafile.getVariableInstance('SourceView')
    sofaSource = SOFASource(None,sourceUp,sourceView)

    # Dimensions do not match
    assert not sofaSource.sourceUpHasDimensions(i,m)

    # Dimensions match
    assert sofaSource.sourceUpHasDimensions(i,c)

    sofafile.close()
    os.remove(path)


def test_sourceViewHasDimensions():

    i = 1
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('SourceUp', 'f8', ('I','C'))
    rootgrp.createVariable('SourceView', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sourceUp = sofafile.getVariableInstance('SourceUp')
    sourceView = sofafile.getVariableInstance('SourceView')
    sofaSource = SOFASource(None,sourceUp,sourceView)

    # Dimensions do not match
    assert not sofaSource.sourceViewHasDimensions(i,m)

    # Dimensions match
    assert sofaSource.sourceViewHasDimensions(i,c)

    sofafile.close()
    os.remove(path)


def test_hasSourceUp():

    i = 1
    c = 3
    m = 4

    # Do not have
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaSource = SOFASource(None, None, None)
    assert not sofaSource.hasSourceUp()
    sofafile.close()

    # Do have
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('SourceUp', 'f8', ('I','C'))
    rootgrp.createVariable('SourceView', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sourceUp = sofafile.getVariableInstance('SourceUp')
    sourceView = sofafile.getVariableInstance('SourceView')
    sofaSource = SOFASource(None, sourceUp, sourceView)
    assert sofaSource.hasSourceUp()

    sofafile.close()
    os.remove(path)


def test_hasSourceView():

    i = 1
    c = 3
    m = 4

    # Do not have
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaSource = SOFASource(None, None, None)
    assert not sofaSource.hasSourceView()
    sofafile.close()

    # Do have
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('SourceUp', 'f8', ('I','C'))
    rootgrp.createVariable('SourceView', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sourceUp = sofafile.getVariableInstance('SourceUp')
    sourceView = sofafile.getVariableInstance('SourceView')
    sofaSource = SOFASource(None, sourceUp, sourceView)
    assert sofaSource.hasSourceView()

    sofafile.close()
    os.remove(path)
