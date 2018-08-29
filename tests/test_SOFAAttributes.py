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
#   @file   test_SOFAAttributes.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofa import *

def test_isRequired() :

    # Required
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.Conventions)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.Version)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.SOFAConventions)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.SOFAConventionsVersion)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.APIName)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.APIVersion)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.AuthorContact)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.Organization)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.License)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.DataType)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.RoomType)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.DateCreated)
    assert SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.DateModified)

    # Not required
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.ApplicationName)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.ApplicationVersion)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.Comment)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.History)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.References)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.Origin)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.RoomShortName)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.RoomDescription)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.RoomLocation)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.ListenerShortName)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.ListenerDescription)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.SourceShortName)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.SourceDescription)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.ReceiverShortName)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.ReceiverDescription)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.EmitterShortName)
    assert not SOFAAttributes.isRequired(SOFAAttributes.AttributeTypes.EmitterDescription)


def test_isReadOnly():
    
    # Read-only
    assert SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.Conventions)
    assert SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.Version)
    assert SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.SOFAConventions)
    assert SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.SOFAConventionsVersion)
    assert SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.APIName)
    assert SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.APIVersion)

    # Not read-only
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.ApplicationName)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.ApplicationVersion)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.AuthorContact)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.Organization)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.License)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.Comment)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.History)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.References)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.DataType)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.RoomType)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.Origin)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.DateCreated)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.DateModified)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.Title)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.RoomShortName)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.RoomDescription)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.RoomLocation)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.ListenerShortName)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.ListenerDescription)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.SourceShortName)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.SourceDescription)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.ReceiverShortName)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.ReceiverDescription)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.EmitterShortName)
    assert not SOFAAttributes.isReadOnly(SOFAAttributes.AttributeTypes.EmitterDescription)


def test_hasDefaultValue():

    # Default value
    assert SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.Conventions)
    assert SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.Version)
    assert SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.DataType)
    assert SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.SOFAConventions)
    assert SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.SOFAConventionsVersion)
    assert SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.APIName)
    assert SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.APIVersion)
    assert SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.License)
    assert SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.RoomType)

    # No default value
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.ApplicationName)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.ApplicationVersion)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.AuthorContact)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.Organization)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.Comment)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.History)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.References)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.Origin)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.DateCreated)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.DateModified)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.Title)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.RoomShortName)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.RoomDescription)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.RoomLocation)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.ListenerShortName)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.ListenerDescription)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.SourceShortName)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.SourceDescription)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.ReceiverShortName)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.ReceiverDescription)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.EmitterShortName)
    assert not SOFAAttributes.hasDefaultValue(SOFAAttributes.AttributeTypes.EmitterDescription)


def test_getDefaultAttributeValue():

    # Default value
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.Conventions)               \
           == 'SOFA'
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.Version)                   \
           == SOFAAPI.getSpecificationsVersion()
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.DataType)                  \
           == 'FIR'
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.SOFAConventions)           \
           == 'SimpleFreeFieldHRIR'
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.SOFAConventionsVersion)    \
           == ''
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.APIName)                   \
           == SOFAAPI.getAPIName()
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.APIVersion)                \
           == SOFAAPI.getAPIVersion()
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.License)                   \
           == 'No license provided, ask the author for permission.'
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.RoomType)                  \
           == 'free field'

    # No default value
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.ApplicationName)       == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.ApplicationVersion)    == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.AuthorContact)         == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.Organization)          == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.Comment)               == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.History)               == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.References)            == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.Origin)                == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.DateCreated)           == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.DateModified)          == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.Title)                 == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.RoomShortName)         == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.RoomDescription)       == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.RoomLocation)          == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.ListenerShortName)     == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.ListenerDescription)   == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.SourceShortName)       == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.SourceDescription)     == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.ReceiverShortName)     == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.ReceiverDescription)   == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.EmitterShortName)      == ""
    assert SOFAAttributes.getDefaultAttributeValue(SOFAAttributes.AttributeTypes.EmitterDescription)    == ""