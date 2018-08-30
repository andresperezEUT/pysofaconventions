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
#   @file   test_SOFAEmitter.py
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

    # EmitterUp exists, but not EmitterView
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    emitterUp = rootgrp.createVariable('EmitterUp', 'f8', ())
    rootgrp.close()

    with pytest.raises(SOFAError) as e:
        SOFAEmitter(None,emitterUp,None) # Internally calls checkOptionalVariables()
    assert e.match('EmitterUp exists but not EmitterView')
    os.remove(path)


    # EmitterView exists, but not EmitterUp
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    emitterView = rootgrp.createVariable('EmitterView', 'f8', ())
    rootgrp.close()

    with pytest.raises(SOFAError) as e:
        SOFAEmitter(None,None,emitterView) # Internally calls checkOptionalVariables()
    assert e.match('EmitterView exists but not EmitterUp')
    os.remove(path)


    # None of them exists
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert SOFAEmitter(None,None,None).checkOptionalVariables()


    # Both of them exist
    rootgrp = Dataset(path, 'a')
    emitterUp = rootgrp.createVariable('EmitterUp', 'f8', ())
    emitterView = rootgrp.createVariable('EmitterView', 'f8', ())
    rootgrp.close()
    assert SOFAEmitter(None, emitterUp, emitterView).checkOptionalVariables()

    os.remove(path)



def test_hasValidDimensions():

    i = 1
    e = 2
    c = 3
    m = 4

    # EmitterPosition not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('E',e)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        SOFAEmitter(None,None,None).hasValidDimensions(e,c,i,m)
    assert error.match('EmitterPosition Variable not found!')

    # Invalid EmitterPosition dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('EmitterPosition', 'f8', ('M','C','E'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        emitterPosition = sofafile.getVariableInstance('EmitterPosition')
        SOFAEmitter(emitterPosition,None,None).hasValidDimensions(e,c,i,m)
    assert error.match('Invalid EmitterPosition Dimensions')

    sofafile.close()
    os.remove(path)

    # Invalid EmitterUp dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('E', e)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('EmitterPosition', 'f8', ('E', 'C', 'I'))
    rootgrp.createVariable('EmitterUp', 'f8', ('E', 'C', 'E'))
    rootgrp.createVariable('EmitterView', 'f8', ('E', 'C', 'I'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        emitterPosition = sofafile.getVariableInstance('EmitterPosition')
        emitterUp = sofafile.getVariableInstance('EmitterUp')
        emitterView = sofafile.getVariableInstance('EmitterView')
        SOFAEmitter(emitterPosition,emitterUp,emitterView).hasValidDimensions(e,c,i,m)
    assert error.match('Invalid EmitterUp Dimensions')

    sofafile.close()
    os.remove(path)

    # Invalid EmitterView dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('E', e)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('EmitterPosition', 'f8', ('E', 'C', 'I'))
    rootgrp.createVariable('EmitterUp', 'f8', ('E', 'C', 'I'))
    rootgrp.createVariable('EmitterView', 'f8', ('E', 'C', 'E'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        emitterPosition = sofafile.getVariableInstance('EmitterPosition')
        emitterUp = sofafile.getVariableInstance('EmitterUp')
        emitterView = sofafile.getVariableInstance('EmitterView')
        SOFAEmitter(emitterPosition, emitterUp, emitterView).hasValidDimensions(e, c, i, m)
    assert error.match('Invalid EmitterView Dimensions')

    sofafile.close()
    os.remove(path)
    
    # Valid dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('E', e)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('EmitterPosition', 'f8', ('E', 'C', 'I'))
    rootgrp.createVariable('EmitterUp', 'f8', ('E', 'C', 'I'))
    rootgrp.createVariable('EmitterView', 'f8', ('E', 'C', 'I'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    emitterPosition = sofafile.getVariableInstance('EmitterPosition')
    emitterUp = sofafile.getVariableInstance('EmitterUp')
    emitterView = sofafile.getVariableInstance('EmitterView')
    assert SOFAEmitter(emitterPosition, emitterUp, emitterView).hasValidDimensions(e, c, i, m)

    sofafile.close()
    os.remove(path)

def test_emitterPositionHasDimensions():

    i = 1
    e = 2
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('E',e)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('EmitterPosition', 'f8', ('M','C','E'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    emitterPosition = sofafile.getVariableInstance('EmitterPosition')
    sofaEmitter = SOFAEmitter(emitterPosition,None,None)

    # Dimensions do not match
    assert not sofaEmitter.emitterPositionHasDimensions(i,e,c)

    # Dimensions match
    assert sofaEmitter.emitterPositionHasDimensions(m, c, e)

    sofafile.close()
    os.remove(path)


def test_emitterUpHasDimensions():

    i = 1
    e = 2
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('E',e)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('EmitterUp', 'f8', ('M','C','E'))
    rootgrp.createVariable('EmitterView', 'f8', ('M','C','E'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    emitterUp = sofafile.getVariableInstance('EmitterUp')
    emitterView = sofafile.getVariableInstance('EmitterView')
    sofaEmitter = SOFAEmitter(None,emitterUp,emitterView)

    # Dimensions do not match
    assert not sofaEmitter.emitterUpHasDimensions(i,e,c)

    # Dimensions match
    assert sofaEmitter.emitterUpHasDimensions(m, c, e)

    sofafile.close()
    os.remove(path)


def test_emitterViewHasDimensions():

    i = 1
    e = 2
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('E',e)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('EmitterUp', 'f8', ('M','C','E'))
    rootgrp.createVariable('EmitterView', 'f8', ('M','C','E'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    emitterUp = sofafile.getVariableInstance('EmitterUp')
    emitterView = sofafile.getVariableInstance('EmitterView')
    sofaEmitter = SOFAEmitter(None,emitterUp,emitterView)

    # Dimensions do not match
    assert not sofaEmitter.emitterViewHasDimensions(i,e,c)

    # Dimensions match
    assert sofaEmitter.emitterViewHasDimensions(m, c, e)

    sofafile.close()
    os.remove(path)


def test_hasEmitterUp():

    i = 1
    e = 2
    c = 3
    m = 4

    # Do not have
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('E', e)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaEmitter = SOFAEmitter(None, None, None)
    assert not sofaEmitter.hasEmitterUp()
    sofafile.close()

    # Do have
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('EmitterUp', 'f8', ('M', 'C', 'E'))
    rootgrp.createVariable('EmitterView', 'f8', ('M', 'C', 'E'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    emitterUp = sofafile.getVariableInstance('EmitterUp')
    emitterView = sofafile.getVariableInstance('EmitterView')
    sofaEmitter = SOFAEmitter(None, emitterUp, emitterView)
    assert sofaEmitter.hasEmitterUp()

    sofafile.close()
    os.remove(path)


def test_hasEmitterView():

    i = 1
    e = 2
    c = 3
    m = 4

    # Do not have
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('E', e)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaEmitter = SOFAEmitter(None, None, None)
    assert not sofaEmitter.hasEmitterView()
    sofafile.close()

    # Do have
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('EmitterUp', 'f8', ('M', 'C', 'E'))
    rootgrp.createVariable('EmitterView', 'f8', ('M', 'C', 'E'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    emitterUp = sofafile.getVariableInstance('EmitterUp')
    emitterView = sofafile.getVariableInstance('EmitterView')
    sofaEmitter = SOFAEmitter(None, emitterUp, emitterView)
    assert sofaEmitter.hasEmitterView()

    sofafile.close()
    os.remove(path)
