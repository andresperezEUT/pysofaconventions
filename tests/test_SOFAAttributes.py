# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Copyright (c') 2018, Eurecat / UPF
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
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION') HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE') ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   @file   test_SOFAAttributes.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofaconventions import *

def test_isRequired() :

    # Required
    assert SOFAAttributes.isRequired('Conventions')
    assert SOFAAttributes.isRequired('Version')
    assert SOFAAttributes.isRequired('SOFAConventions')
    assert SOFAAttributes.isRequired('SOFAConventionsVersion')
    assert SOFAAttributes.isRequired('APIName')
    assert SOFAAttributes.isRequired('APIVersion')
    assert SOFAAttributes.isRequired('AuthorContact')
    assert SOFAAttributes.isRequired('Organization')
    assert SOFAAttributes.isRequired('License')
    assert SOFAAttributes.isRequired('DataType')
    assert SOFAAttributes.isRequired('RoomType')
    assert SOFAAttributes.isRequired('DateCreated')
    assert SOFAAttributes.isRequired('DateModified')

    # Not required
    assert not SOFAAttributes.isRequired('ApplicationName')
    assert not SOFAAttributes.isRequired('ApplicationVersion')
    assert not SOFAAttributes.isRequired('Comment')
    assert not SOFAAttributes.isRequired('History')
    assert not SOFAAttributes.isRequired('References')
    assert not SOFAAttributes.isRequired('Origin')
    assert not SOFAAttributes.isRequired('RoomShortName')
    assert not SOFAAttributes.isRequired('RoomDescription')
    assert not SOFAAttributes.isRequired('RoomLocation')
    assert not SOFAAttributes.isRequired('ListenerShortName')
    assert not SOFAAttributes.isRequired('ListenerDescription')
    assert not SOFAAttributes.isRequired('SourceShortName')
    assert not SOFAAttributes.isRequired('SourceDescription')
    assert not SOFAAttributes.isRequired('ReceiverShortName')
    assert not SOFAAttributes.isRequired('ReceiverDescription')
    assert not SOFAAttributes.isRequired('EmitterShortName')
    assert not SOFAAttributes.isRequired('EmitterDescription')


def test_isReadOnly():
    
    # Read-only
    assert SOFAAttributes.isReadOnly('Conventions')
    assert SOFAAttributes.isReadOnly('Version')
    assert SOFAAttributes.isReadOnly('SOFAConventions')
    assert SOFAAttributes.isReadOnly('SOFAConventionsVersion')
    assert SOFAAttributes.isReadOnly('APIName')
    assert SOFAAttributes.isReadOnly('APIVersion')

    # Not read-only
    assert not SOFAAttributes.isReadOnly('ApplicationName')
    assert not SOFAAttributes.isReadOnly('ApplicationVersion')
    assert not SOFAAttributes.isReadOnly('AuthorContact')
    assert not SOFAAttributes.isReadOnly('Organization')
    assert not SOFAAttributes.isReadOnly('License')
    assert not SOFAAttributes.isReadOnly('Comment')
    assert not SOFAAttributes.isReadOnly('History')
    assert not SOFAAttributes.isReadOnly('References')
    assert not SOFAAttributes.isReadOnly('DataType')
    assert not SOFAAttributes.isReadOnly('RoomType')
    assert not SOFAAttributes.isReadOnly('Origin')
    assert not SOFAAttributes.isReadOnly('DateCreated')
    assert not SOFAAttributes.isReadOnly('DateModified')
    assert not SOFAAttributes.isReadOnly('Title')
    assert not SOFAAttributes.isReadOnly('RoomShortName')
    assert not SOFAAttributes.isReadOnly('RoomDescription')
    assert not SOFAAttributes.isReadOnly('RoomLocation')
    assert not SOFAAttributes.isReadOnly('ListenerShortName')
    assert not SOFAAttributes.isReadOnly('ListenerDescription')
    assert not SOFAAttributes.isReadOnly('SourceShortName')
    assert not SOFAAttributes.isReadOnly('SourceDescription')
    assert not SOFAAttributes.isReadOnly('ReceiverShortName')
    assert not SOFAAttributes.isReadOnly('ReceiverDescription')
    assert not SOFAAttributes.isReadOnly('EmitterShortName')
    assert not SOFAAttributes.isReadOnly('EmitterDescription')


def test_hasDefaultValue():

    # Default value
    assert SOFAAttributes.hasDefaultValue('Conventions')
    assert SOFAAttributes.hasDefaultValue('Version')
    assert SOFAAttributes.hasDefaultValue('DataType')
    assert SOFAAttributes.hasDefaultValue('SOFAConventions')
    assert SOFAAttributes.hasDefaultValue('SOFAConventionsVersion')
    assert SOFAAttributes.hasDefaultValue('APIName')
    assert SOFAAttributes.hasDefaultValue('APIVersion')
    assert SOFAAttributes.hasDefaultValue('License')
    assert SOFAAttributes.hasDefaultValue('RoomType')

    # No default value
    assert not SOFAAttributes.hasDefaultValue('ApplicationName')
    assert not SOFAAttributes.hasDefaultValue('ApplicationVersion')
    assert not SOFAAttributes.hasDefaultValue('AuthorContact')
    assert not SOFAAttributes.hasDefaultValue('Organization')
    assert not SOFAAttributes.hasDefaultValue('Comment')
    assert not SOFAAttributes.hasDefaultValue('History')
    assert not SOFAAttributes.hasDefaultValue('References')
    assert not SOFAAttributes.hasDefaultValue('Origin')
    assert not SOFAAttributes.hasDefaultValue('DateCreated')
    assert not SOFAAttributes.hasDefaultValue('DateModified')
    assert not SOFAAttributes.hasDefaultValue('Title')
    assert not SOFAAttributes.hasDefaultValue('RoomShortName')
    assert not SOFAAttributes.hasDefaultValue('RoomDescription')
    assert not SOFAAttributes.hasDefaultValue('RoomLocation')
    assert not SOFAAttributes.hasDefaultValue('ListenerShortName')
    assert not SOFAAttributes.hasDefaultValue('ListenerDescription')
    assert not SOFAAttributes.hasDefaultValue('SourceShortName')
    assert not SOFAAttributes.hasDefaultValue('SourceDescription')
    assert not SOFAAttributes.hasDefaultValue('ReceiverShortName')
    assert not SOFAAttributes.hasDefaultValue('ReceiverDescription')
    assert not SOFAAttributes.hasDefaultValue('EmitterShortName')
    assert not SOFAAttributes.hasDefaultValue('EmitterDescription')


def test_getDefaultAttributeValue():

    # Default value
    assert SOFAAttributes.getDefaultAttributeValue('Conventions')               \
           == 'SOFA'
    assert SOFAAttributes.getDefaultAttributeValue('Version')                   \
           == SOFAAPI.getSpecificationsVersion()
    assert SOFAAttributes.getDefaultAttributeValue('DataType')                  \
           == 'FIR'
    assert SOFAAttributes.getDefaultAttributeValue('SOFAConventions')           \
           == 'SimpleFreeFieldHRIR'
    assert SOFAAttributes.getDefaultAttributeValue('SOFAConventionsVersion')    \
           == ''
    assert SOFAAttributes.getDefaultAttributeValue('APIName')                   \
           == SOFAAPI.getAPIName()
    assert SOFAAttributes.getDefaultAttributeValue('APIVersion')                \
           == SOFAAPI.getAPIVersion()
    assert SOFAAttributes.getDefaultAttributeValue('License')                   \
           == 'No license provided, ask the author for permission.'
    assert SOFAAttributes.getDefaultAttributeValue('RoomType')                  \
           == 'free field'

    # No default value
    assert SOFAAttributes.getDefaultAttributeValue('ApplicationName')       == ""
    assert SOFAAttributes.getDefaultAttributeValue('ApplicationVersion')    == ""
    assert SOFAAttributes.getDefaultAttributeValue('AuthorContact')         == ""
    assert SOFAAttributes.getDefaultAttributeValue('Organization')          == ""
    assert SOFAAttributes.getDefaultAttributeValue('Comment')               == ""
    assert SOFAAttributes.getDefaultAttributeValue('History')               == ""
    assert SOFAAttributes.getDefaultAttributeValue('References')            == ""
    assert SOFAAttributes.getDefaultAttributeValue('Origin')                == ""
    assert SOFAAttributes.getDefaultAttributeValue('DateCreated')           == ""
    assert SOFAAttributes.getDefaultAttributeValue('DateModified')          == ""
    assert SOFAAttributes.getDefaultAttributeValue('Title')                 == ""
    assert SOFAAttributes.getDefaultAttributeValue('RoomShortName')         == ""
    assert SOFAAttributes.getDefaultAttributeValue('RoomDescription')       == ""
    assert SOFAAttributes.getDefaultAttributeValue('RoomLocation')          == ""
    assert SOFAAttributes.getDefaultAttributeValue('ListenerShortName')     == ""
    assert SOFAAttributes.getDefaultAttributeValue('ListenerDescription')   == ""
    assert SOFAAttributes.getDefaultAttributeValue('SourceShortName')       == ""
    assert SOFAAttributes.getDefaultAttributeValue('SourceDescription')     == ""
    assert SOFAAttributes.getDefaultAttributeValue('ReceiverShortName')     == ""
    assert SOFAAttributes.getDefaultAttributeValue('ReceiverDescription')   == ""
    assert SOFAAttributes.getDefaultAttributeValue('EmitterShortName')      == ""
    assert SOFAAttributes.getDefaultAttributeValue('EmitterDescription')    == ""