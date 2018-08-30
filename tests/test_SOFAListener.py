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
#   @file   test_SOFAListener.py
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

    # ListenerUp exists, but not ListenerView
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    listenerUp = rootgrp.createVariable('ListenerUp', 'f8', ())
    rootgrp.close()

    with pytest.raises(SOFAError) as e:
        SOFAListener(None,listenerUp,None) # Internally calls checkOptionalVariables()
    assert e.match('ListenerUp exists but not ListenerView')
    os.remove(path)


    # ListenerView exists, but not ListenerUp
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    listenerView = rootgrp.createVariable('ListenerView', 'f8', ())
    rootgrp.close()

    with pytest.raises(SOFAError) as e:
        SOFAListener(None,None,listenerView) # Internally calls checkOptionalVariables()
    assert e.match('ListenerView exists but not ListenerUp')
    os.remove(path)


    # None of them exists
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert SOFAListener(None,None,None).checkOptionalVariables()


    # Both of them exist
    rootgrp = Dataset(path, 'a')
    listenerUp = rootgrp.createVariable('ListenerUp', 'f8', ())
    listenerView = rootgrp.createVariable('ListenerView', 'f8', ())
    rootgrp.close()
    assert SOFAListener(None, listenerUp, listenerView).checkOptionalVariables()

    os.remove(path)



def test_hasValidDimensions():

    i = 1
    c = 3
    m = 4

    # ListenerPosition not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        SOFAListener(None,None,None).hasValidDimensions(i,c,m)
    assert error.match('ListenerPosition Variable not found!')

    # Invalid ListenerPosition dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ListenerPosition', 'f8', ('C','M'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        listenerPosition = sofafile.getVariableInstance('ListenerPosition')
        SOFAListener(listenerPosition,None,None).hasValidDimensions(i,c,m)
    assert error.match('Invalid ListenerPosition Dimensions')

    sofafile.close()
    os.remove(path)

    # Invalid ListenerUp dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('ListenerPosition', 'f8', ('I', 'C'))
    rootgrp.createVariable('ListenerUp', 'f8', ('C','M'))
    rootgrp.createVariable('ListenerView', 'f8', ('I', 'C'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        listenerPosition = sofafile.getVariableInstance('ListenerPosition')
        listenerUp = sofafile.getVariableInstance('ListenerUp')
        listenerView = sofafile.getVariableInstance('ListenerView')
        SOFAListener(listenerPosition,listenerUp,listenerView).hasValidDimensions(i,c,m)
    assert error.match('Invalid ListenerUp Dimensions')

    sofafile.close()
    os.remove(path)

    # Invalid ListenerView dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('ListenerPosition', 'f8', ('I', 'C'))
    rootgrp.createVariable('ListenerUp', 'f8', ('I', 'C'))
    rootgrp.createVariable('ListenerView', 'f8', ('C','M'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        listenerPosition = sofafile.getVariableInstance('ListenerPosition')
        listenerUp = sofafile.getVariableInstance('ListenerUp')
        listenerView = sofafile.getVariableInstance('ListenerView')
        SOFAListener(listenerPosition, listenerUp, listenerView).hasValidDimensions(i,c,m)
    assert error.match('Invalid ListenerView Dimensions')

    sofafile.close()
    os.remove(path)

    # Valid dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('ListenerPosition', 'f8', ('I', 'C'))
    rootgrp.createVariable('ListenerUp', 'f8', ('I', 'C'))
    rootgrp.createVariable('ListenerView', 'f8', ('I', 'C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    listenerPosition = sofafile.getVariableInstance('ListenerPosition')
    listenerUp = sofafile.getVariableInstance('ListenerUp')
    listenerView = sofafile.getVariableInstance('ListenerView')
    assert SOFAListener(listenerPosition, listenerUp, listenerView).hasValidDimensions(i,c,m)

    sofafile.close()
    os.remove(path)


def test_listenerPositionHasDimensions():

    i = 1
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('ListenerPosition', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    listenerPosition = sofafile.getVariableInstance('ListenerPosition')
    sofaListener = SOFAListener(listenerPosition,None,None)

    # Dimensions do not match
    assert not sofaListener.listenerPositionHasDimensions(i,m)

    # Dimensions match
    assert sofaListener.listenerPositionHasDimensions(i,c)

    sofafile.close()
    os.remove(path)


def test_listenerUpHasDimensions():

    i = 1
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('ListenerUp', 'f8', ('I','C'))
    rootgrp.createVariable('ListenerView', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    listenerUp = sofafile.getVariableInstance('ListenerUp')
    listenerView = sofafile.getVariableInstance('ListenerView')
    sofaListener = SOFAListener(None,listenerUp,listenerView)

    # Dimensions do not match
    assert not sofaListener.listenerUpHasDimensions(i,m)

    # Dimensions match
    assert sofaListener.listenerUpHasDimensions(i,c)

    sofafile.close()
    os.remove(path)


def test_listenerViewHasDimensions():

    i = 1
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('ListenerUp', 'f8', ('I','C'))
    rootgrp.createVariable('ListenerView', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    listenerUp = sofafile.getVariableInstance('ListenerUp')
    listenerView = sofafile.getVariableInstance('ListenerView')
    sofaListener = SOFAListener(None,listenerUp,listenerView)

    # Dimensions do not match
    assert not sofaListener.listenerViewHasDimensions(i,m)

    # Dimensions match
    assert sofaListener.listenerViewHasDimensions(i,c)

    sofafile.close()
    os.remove(path)


def test_hasListenerUp():

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
    sofaListener = SOFAListener(None, None, None)
    assert not sofaListener.hasListenerUp()
    sofafile.close()

    # Do have
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ListenerUp', 'f8', ('I','C'))
    rootgrp.createVariable('ListenerView', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    listenerUp = sofafile.getVariableInstance('ListenerUp')
    listenerView = sofafile.getVariableInstance('ListenerView')
    sofaListener = SOFAListener(None, listenerUp, listenerView)
    assert sofaListener.hasListenerUp()

    sofafile.close()
    os.remove(path)


def test_hasListenerView():

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
    sofaListener = SOFAListener(None, None, None)
    assert not sofaListener.hasListenerView()
    sofafile.close()

    # Do have
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ListenerUp', 'f8', ('I','C'))
    rootgrp.createVariable('ListenerView', 'f8', ('I','C'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    listenerUp = sofafile.getVariableInstance('ListenerUp')
    listenerView = sofafile.getVariableInstance('ListenerView')
    sofaListener = SOFAListener(None, listenerUp, listenerView)
    assert sofaListener.hasListenerView()

    sofafile.close()
    os.remove(path)
