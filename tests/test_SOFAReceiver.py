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
#   @file   test_SOFAReceiver.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
import os
import tempfile
from netCDF4 import Dataset
from pysofaconventions import *


def test_checkOptionalVariables():

    # ReceiverUp exists, but not ReceiverView
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    receiverUp = rootgrp.createVariable('ReceiverUp', 'f8', ())
    rootgrp.close()

    with pytest.raises(SOFAError) as e:
        SOFAReceiver(None,receiverUp,None) # Internally calls checkOptionalVariables()
    assert e.match('ReceiverUp exists but not ReceiverView')
    os.remove(path)


    # ReceiverView exists, but not ReceiverUp
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    receiverView = rootgrp.createVariable('ReceiverView', 'f8', ())
    rootgrp.close()

    with pytest.raises(SOFAError) as e:
        SOFAReceiver(None,None,receiverView) # Internally calls checkOptionalVariables()
    assert e.match('ReceiverView exists but not ReceiverUp')
    os.remove(path)


    # None of them exists
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    assert SOFAReceiver(None,None,None).checkOptionalVariables()


    # Both of them exist
    rootgrp = Dataset(path, 'a')
    receiverUp = rootgrp.createVariable('ReceiverUp', 'f8', ())
    receiverView = rootgrp.createVariable('ReceiverView', 'f8', ())
    rootgrp.close()
    assert SOFAReceiver(None, receiverUp, receiverView).checkOptionalVariables()

    os.remove(path)



def test_hasValidDimensions():

    i = 1
    r = 2
    c = 3
    m = 4

    # ReceiverPosition not found
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('R',r)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        SOFAReceiver(None,None,None).hasValidDimensions(r,c,i,m)
    assert error.match('ReceiverPosition Variable not found!')

    # Invalid ReceiverPosition dimensions
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ReceiverPosition', 'f8', ('M','C','R'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        receiverPosition = sofafile.getVariableInstance('ReceiverPosition')
        SOFAReceiver(receiverPosition,None,None).hasValidDimensions(r,c,i,m)
    assert error.match('Invalid ReceiverPosition Dimensions')

    sofafile.close()
    os.remove(path)

    # Invalid ReceiverUp dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('R', r)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('ReceiverPosition', 'f8', ('R', 'C', 'I'))
    rootgrp.createVariable('ReceiverUp', 'f8', ('R', 'C', 'R'))
    rootgrp.createVariable('ReceiverView', 'f8', ('R', 'C', 'I'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        receiverPosition = sofafile.getVariableInstance('ReceiverPosition')
        receiverUp = sofafile.getVariableInstance('ReceiverUp')
        receiverView = sofafile.getVariableInstance('ReceiverView')
        SOFAReceiver(receiverPosition,receiverUp,receiverView).hasValidDimensions(r,c,i,m)
    assert error.match('Invalid ReceiverUp Dimensions')

    sofafile.close()
    os.remove(path)

    # Invalid ReceiverView dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('R', r)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('ReceiverPosition', 'f8', ('R', 'C', 'I'))
    rootgrp.createVariable('ReceiverUp', 'f8', ('R', 'C', 'I'))
    rootgrp.createVariable('ReceiverView', 'f8', ('R', 'C', 'R'))
    rootgrp.close()

    with pytest.raises(SOFAError) as error:
        sofafile = SOFAFile(path, 'r')
        receiverPosition = sofafile.getVariableInstance('ReceiverPosition')
        receiverUp = sofafile.getVariableInstance('ReceiverUp')
        receiverView = sofafile.getVariableInstance('ReceiverView')
        SOFAReceiver(receiverPosition, receiverUp, receiverView).hasValidDimensions(r, c, i, m)
    assert error.match('Invalid ReceiverView Dimensions')

    sofafile.close()
    os.remove(path)

    # Valid dimensions
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('R', r)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.createVariable('ReceiverPosition', 'f8', ('R', 'C', 'I'))
    rootgrp.createVariable('ReceiverUp', 'f8', ('R', 'C', 'I'))
    rootgrp.createVariable('ReceiverView', 'f8', ('R', 'C', 'I'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    receiverPosition = sofafile.getVariableInstance('ReceiverPosition')
    receiverUp = sofafile.getVariableInstance('ReceiverUp')
    receiverView = sofafile.getVariableInstance('ReceiverView')
    assert SOFAReceiver(receiverPosition, receiverUp, receiverView).hasValidDimensions(r, c, i, m)

    sofafile.close()
    os.remove(path)


def test_receiverPositionHasDimensions():

    i = 1
    r = 2
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('R',r)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('ReceiverPosition', 'f8', ('M','C','R'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    receiverPosition = sofafile.getVariableInstance('ReceiverPosition')
    sofaReceiver = SOFAReceiver(receiverPosition,None,None)

    # Dimensions do not match
    assert not sofaReceiver.receiverPositionHasDimensions(i,r,c)

    # Dimensions match
    assert sofaReceiver.receiverPositionHasDimensions(m, c, r)

    sofafile.close()
    os.remove(path)


def test_receiverUpHasDimensions():

    i = 1
    r = 2
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('R',r)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('ReceiverUp', 'f8', ('M','C','R'))
    rootgrp.createVariable('ReceiverView', 'f8', ('M','C','R'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    receiverUp = sofafile.getVariableInstance('ReceiverUp')
    receiverView = sofafile.getVariableInstance('ReceiverView')
    sofaReceiver = SOFAReceiver(None,receiverUp,receiverView)

    # Dimensions do not match
    assert not sofaReceiver.receiverUpHasDimensions(i,r,c)

    # Dimensions match
    assert sofaReceiver.receiverUpHasDimensions(m, c, r)

    sofafile.close()
    os.remove(path)


def test_receiverViewHasDimensions():

    i = 1
    r = 2
    c = 3
    m = 4

    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I',i)
    rootgrp.createDimension('R',r)
    rootgrp.createDimension('C',c)
    rootgrp.createDimension('M',m)
    rootgrp.createVariable('ReceiverUp', 'f8', ('M','C','R'))
    rootgrp.createVariable('ReceiverView', 'f8', ('M','C','R'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    receiverUp = sofafile.getVariableInstance('ReceiverUp')
    receiverView = sofafile.getVariableInstance('ReceiverView')
    sofaReceiver = SOFAReceiver(None,receiverUp,receiverView)

    # Dimensions do not match
    assert not sofaReceiver.receiverViewHasDimensions(i,r,c)

    # Dimensions match
    assert sofaReceiver.receiverViewHasDimensions(m, c, r)

    sofafile.close()
    os.remove(path)


def test_hasReceiverUp():

    i = 1
    r = 2
    c = 3
    m = 4

    # Do not have
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('R', r)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaReceiver = SOFAReceiver(None, None, None)
    assert not sofaReceiver.hasReceiverUp()
    sofafile.close()

    # Do have
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ReceiverUp', 'f8', ('M', 'C', 'R'))
    rootgrp.createVariable('ReceiverView', 'f8', ('M', 'C', 'R'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    receiverUp = sofafile.getVariableInstance('ReceiverUp')
    receiverView = sofafile.getVariableInstance('ReceiverView')
    sofaReceiver = SOFAReceiver(None, receiverUp, receiverView)
    assert sofaReceiver.hasReceiverUp()

    sofafile.close()
    os.remove(path)


def test_hasReceiverView():

    i = 1
    r = 2
    c = 3
    m = 4

    # Do not have
    fd, path = tempfile.mkstemp()
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.createDimension('I', i)
    rootgrp.createDimension('R', r)
    rootgrp.createDimension('C', c)
    rootgrp.createDimension('M', m)
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    sofaReceiver = SOFAReceiver(None, None, None)
    assert not sofaReceiver.hasReceiverView()
    sofafile.close()

    # Do have
    rootgrp = Dataset(path, 'a')
    rootgrp.createVariable('ReceiverUp', 'f8', ('M', 'C', 'R'))
    rootgrp.createVariable('ReceiverView', 'f8', ('M', 'C', 'R'))
    rootgrp.close()

    sofafile = SOFAFile(path, 'r')
    receiverUp = sofafile.getVariableInstance('ReceiverUp')
    receiverView = sofafile.getVariableInstance('ReceiverView')
    sofaReceiver = SOFAReceiver(None, receiverUp, receiverView)
    assert sofaReceiver.hasReceiverView()

    sofafile.close()
    os.remove(path)
