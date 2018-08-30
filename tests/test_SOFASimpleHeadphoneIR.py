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
#   @file   test_SOFASimpleHeadphoneIR.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
import os
import tempfile
import time
from netCDF4 import Dataset
from pysofaconventions import *


def test_getConventionVersion():

    assert SOFASimpleHeadphoneIR.getConventionVersion() == "0.2"


def test_isValid():

    fd, path = tempfile.mkstemp()

    def raiseWarning(warningString):
        simpleHeadphoneIR = SOFASimpleHeadphoneIR(path, 'r')
        with pytest.warns(SOFAWarning) as record:
            assert not simpleHeadphoneIR.isValid()
        assert warningString in str(record[-1].message)
        simpleHeadphoneIR.close()


    ## Validity of SOFAFile

    # File not valid
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    rootgrp.close()
    raiseWarning('Missing required attribute: APIName')
    os.remove(path)

    # SOFA File valid
    rootgrp = Dataset(path, 'w', format='NETCDF4')
    # Attributes
    rootgrp.Conventions = 'SOFA'
    rootgrp.Version = '1.0'
    rootgrp.SOFAConventions = 'GeneralFIRE'
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
    # Dimensions
    rootgrp.createDimension('I', 1)
    rootgrp.createDimension('N', 2)
    rootgrp.createDimension('C', 3)
    rootgrp.createDimension('M', 4)
    rootgrp.createDimension('R', 5)
    rootgrp.createDimension('E', 6)
    # Variables
    sr = rootgrp.createVariable('Data.SamplingRate', 'f8', ('I',))
    sr.Units = 'hertz'
    rootgrp.createVariable('Data.Delay', 'f8', ('M', 'R', 'E'))
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'E', 'N'))
    listenerPositionVar = rootgrp.createVariable('ListenerPosition', 'f8', ('I', 'C'))
    listenerPositionVar.Units = 'metre'
    listenerPositionVar.Type = 'cartesian'
    sourcePositionVar = rootgrp.createVariable('SourcePosition', 'f8', ('I', 'C'))
    sourcePositionVar.Units = 'metre'
    sourcePositionVar.Type = 'cartesian'
    receiverPositionVar = rootgrp.createVariable('ReceiverPosition', 'f8', ('R', 'C', 'I'))
    receiverPositionVar.Units = 'metre'
    receiverPositionVar.Type = 'cartesian'
    emitterPositionVar = rootgrp.createVariable('EmitterPosition', 'f8', ('E', 'C', 'M'))
    emitterPositionVar.Units = 'metre'
    emitterPositionVar.Type = 'cartesian'
    rootgrp.close()

    ## Specific validity

    # Data type should be FIR
    raiseWarning('DataType is not FIR')
    # Adjust data type and required variables to change
    rootgrp = Dataset(path, 'a')
    rootgrp.DataType = 'FIR'
    rootgrp.renameVariable('Data.Delay',"OLD_Data.Delay")
    rootgrp.createVariable('Data.Delay', 'f8', ('M', 'R'))
    rootgrp.renameVariable('Data.IR','OLD_Data.IR')
    rootgrp.createVariable('Data.IR', 'f8', ('M', 'R', 'N'))
    rootgrp.close()

    # SOFAConventions should be SimpleHeadphoneIR
    raiseWarning('SOFAConventions is not SimpleHeadphoneIR')
    rootgrp = Dataset(path, 'a')
    rootgrp.SOFAConventions = 'SimpleHeadphoneIR'
    rootgrp.close()

    # Global Attribute RoomType should be 'free field
    raiseWarning('RoomType is not "free field"')
    rootgrp = Dataset(path, 'a')
    rootgrp.RoomType = 'free field'
    rootgrp.close()

    # Mandatory Global Attribute ListenerShortName
    raiseWarning('Missing required Global Attribute "ListenerShortName"')
    rootgrp = Dataset(path, 'a')
    rootgrp.ListenerShortName = 'AmazinglyShortName'
    rootgrp.close()


    # Mandatory Global Attribute ListenerDescription
    raiseWarning('Missing required Global Attribute "ListenerDescription"')
    rootgrp = Dataset(path, 'a')
    rootgrp.ListenerDescription = 'the best listener'
    rootgrp.close()

    # Mandatory Global Attribute SourceDescription
    raiseWarning('Missing required Global Attribute "SourceDescription"')
    rootgrp = Dataset(path, 'a')
    rootgrp.SourceDescription = 'source is not as godo'
    rootgrp.close()

    # Mandatory Global Attribute EmitterDescription
    raiseWarning('Missing required Global Attribute "EmitterDescription"')
    rootgrp = Dataset(path, 'a')
    rootgrp.EmitterDescription = 'I like this emitter'
    rootgrp.close()

    # Mandatory Global Attribute DatabaseName
    raiseWarning('Missing required Global Attribute "DatabaseName"')
    rootgrp = Dataset(path, 'a')
    rootgrp.DatabaseName = 'IncredibleDatabase'
    rootgrp.close()

    # Mandatory Global Attribute SourceModel
    raiseWarning('Missing required Global Attribute "SourceModel"')
    rootgrp = Dataset(path, 'a')
    rootgrp.SourceModel = 'this is the source model'
    rootgrp.close()

    # Mandatory Global Attribute SourceManufacturer
    raiseWarning('Missing required Global Attribute "SourceManufacturer"')
    rootgrp = Dataset(path, 'a')
    rootgrp.SourceManufacturer = 'INGSOC'
    rootgrp.close()

    # Mandatory Global Attribute SourceURI
    raiseWarning('Missing required Global Attribute "SourceURI"')
    rootgrp = Dataset(path, 'a')
    rootgrp.SourceURI = 'www.com'
    rootgrp.close()

    # Dimension E should match dimension R
    raiseWarning('Number of emitters (E) and number of receivers (R) should match')
    rootgrp = Dataset(path, 'a')
    rootgrp.renameDimension('E','OLD_E')
    rootgrp.createDimension('E',5)
    rootgrp.renameVariable('EmitterPosition','OLD_EmitterPosition')
    emitterPositionVar = rootgrp.createVariable('EmitterPosition', 'f8', ('E', 'C', 'M'))
    emitterPositionVar.Units = 'metre'
    emitterPositionVar.Type = 'cartesian'
    rootgrp.close()

    # All right
    simpleHeadphoneIR = SOFASimpleHeadphoneIR(path, 'r')
    assert simpleHeadphoneIR.isValid()
    simpleHeadphoneIR.close()
    os.remove(path)