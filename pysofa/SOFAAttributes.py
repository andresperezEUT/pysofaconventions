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
#   @file   SOFAAttributes.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum
from .SOFAAPI import SOFAAPI

class SOFAAttributes:

    @classmethod
    def isRequired(self,attribute):
        """
        Query if the attribute is required

        :param attribute:   The attribute
        :return:            True if required, False otherwise
        """
        return self.requiredAttributes[attribute]

    @classmethod
    def isReadOnly(self,attribute):
        """
        Query if the attribute is read only
        :param attribute: The attribute
        :return: True if read only, False otherwise
        """
        return self.readOnlyAttributes[attribute]

    @classmethod
    def hasDefaultValue(self,attribute):
        """
        Query if the attribute has a default value
        :param attribute: The attribute
        :return: True if there is default value, False otherwise
        """
        return self.hasDefaultValueAttributes[attribute]

    @classmethod
    def getDefaultAttributeValue(self,attributeType):
        """
        Get the default value for the given attribute, or empty string if there is no default value

        :param attributeType:   an attribute type
        :return:                the default attribute value, or empty string if not found
        """
        if self.hasDefaultValueAttributes[attributeType]:
            return self.defaultAttributeValues[attributeType]
        else:
            return ""



    class AttributeTypes(Enum):
        Conventions            = 0     # Specifies the netCDF file as a set of AES-X212 SOFAConventions.
        Version                = 1     # Version of the AES-X212 specifications. The version is in the form x.y, where x is the version major and y the version minor
        SOFAConventions        = 2     # Name of the AES-X212 convention.
        SOFAConventionsVersion = 3     # Version of the AES-X212 convention. The version is in the form x.y, where x is the version major and y the version minor.
        DataType               = 4     # Specifies the data type
        RoomType               = 5     # Specifies the room type.
        Title                  = 6     # A succinct description of what is in the file.
        DateCreated            = 7     # Date and time of the creation of the file in ISO 8601 format: 'yyyy-mm-dd HH:MM:SS'. This field is updated each time a new file is created
        DateModified           = 8     # Date and time of the last file modification in ISO 8601 format: 'yyyy-mm-dd HH:MM:SS'. This field is updated each time when saving a file
        APIName                = 9     # Name of the API that created/edited the file
        APIVersion             = 10    # Version of the API that created/edited the file. The version is in the form x.y, where x is the version major and y the version minor.
        AuthorContact          = 11    # Contact information (for example, email) of the author
        Organization           = 12    # Legal name of the organization of the author. Use author's name for private authors
        License                = 13    # Legal license under which the data are provided
        ApplicationName        = 14    # Name of the application that created/edited the file
        ApplicationVersion     = 15    # Version of the application that created/edited the file
        Comment                = 16    # Miscellaneous information about the data or methods used to produce the date/file
        History                = 17    # Audit trail for modifications to the original data
        References             = 18    # Published or web-based references that describe the data or methods used to produce the data
        Origin                 = 19    # The method used for creating the original data. In case of model-generated data, origin should name the model and its version. In case of observed/measured data, source should characterize the data.
        RoomShortName          = 20    # Short Name of the room
        RoomDescription        = 21    # Informal verbal description of the room
        RoomLocation           = 22    # Location of the room
        ListenerShortName      = 23    # Short name of the listener
        ListenerDescription    = 24    # Description of the listener
        SourceShortName        = 25    # Short name of the source
        SourceDescription      = 26    # Description of the source
        ReceiverShortName      = 27    # Short name of the receiver
        ReceiverDescription    = 28    # Description of the receiver
        EmitterShortName       = 29    # Short name of the emitter
        EmitterDescription     = 30    # Description of the emitter


    requiredAttributes = {
        AttributeTypes.Conventions:             True,
        AttributeTypes.Version:                 True,
        AttributeTypes.SOFAConventions:         True,
        AttributeTypes.SOFAConventionsVersion:  True,
        AttributeTypes.APIName:                 True,
        AttributeTypes.APIVersion:              True,
        AttributeTypes.ApplicationName:         False,
        AttributeTypes.ApplicationVersion:      False,
        AttributeTypes.AuthorContact:           True,
        AttributeTypes.Organization:            True,
        AttributeTypes.License:                 True,
        AttributeTypes.Comment:                 False,
        AttributeTypes.History:                 False,
        AttributeTypes.References:              False,
        AttributeTypes.DataType:                True,
        AttributeTypes.RoomType:                True,
        AttributeTypes.Origin:                  False,
        AttributeTypes.DateCreated:             True,
        AttributeTypes.DateModified:            True,
        AttributeTypes.Title:                   True,
        AttributeTypes.RoomShortName:           False,
        AttributeTypes.RoomDescription:         False,
        AttributeTypes.RoomLocation:            False,
        AttributeTypes.ListenerShortName:       False,
        AttributeTypes.ListenerDescription:     False,
        AttributeTypes.SourceShortName:         False,
        AttributeTypes.SourceDescription:       False,
        AttributeTypes.ReceiverShortName:       False,
        AttributeTypes.ReceiverDescription:     False,
        AttributeTypes.EmitterShortName:        False,
        AttributeTypes.EmitterDescription:      False,
    }

    readOnlyAttributes = {
        AttributeTypes.Conventions:             True,
        AttributeTypes.Version:                 True,
        AttributeTypes.SOFAConventions:         True,
        AttributeTypes.SOFAConventionsVersion:  True,
        AttributeTypes.APIName:                 True,
        AttributeTypes.APIVersion:              True,
        AttributeTypes.ApplicationName:         False,
        AttributeTypes.ApplicationVersion:      False,
        AttributeTypes.AuthorContact:           False,
        AttributeTypes.Organization:            False,
        AttributeTypes.License:                 False,
        AttributeTypes.Comment:                 False,
        AttributeTypes.History:                 False,
        AttributeTypes.References:              False,
        AttributeTypes.DataType:                False,
        AttributeTypes.RoomType:                False,
        AttributeTypes.Origin:                  False,
        AttributeTypes.DateCreated:             False,
        AttributeTypes.DateModified:            False,
        AttributeTypes.Title:                   False,
        AttributeTypes.RoomShortName:           False,
        AttributeTypes.RoomDescription:         False,
        AttributeTypes.RoomLocation:            False,
        AttributeTypes.ListenerShortName:       False,
        AttributeTypes.ListenerDescription:     False,
        AttributeTypes.SourceShortName:         False,
        AttributeTypes.SourceDescription:       False,
        AttributeTypes.ReceiverShortName:       False,
        AttributeTypes.ReceiverDescription:     False,
        AttributeTypes.EmitterShortName:        False,
        AttributeTypes.EmitterDescription:      False,
    }

    hasDefaultValueAttributes = {
        AttributeTypes.Conventions:             True,
        AttributeTypes.Version:                 True,
        AttributeTypes.SOFAConventions:         True,
        AttributeTypes.SOFAConventionsVersion:  True,
        AttributeTypes.APIName:                 True,
        AttributeTypes.APIVersion:              True,
        AttributeTypes.ApplicationName:         False,
        AttributeTypes.ApplicationVersion:      False,
        AttributeTypes.AuthorContact:           False,
        AttributeTypes.Organization:            False,
        AttributeTypes.License:                 True,
        AttributeTypes.Comment:                 False,
        AttributeTypes.History:                 False,
        AttributeTypes.References:              False,
        AttributeTypes.DataType:                True,
        AttributeTypes.RoomType:                True,
        AttributeTypes.Origin:                  False,
        AttributeTypes.DateCreated:             False,
        AttributeTypes.DateModified:            False,
        AttributeTypes.Title:                   False,
        AttributeTypes.RoomShortName:           False,
        AttributeTypes.RoomDescription:         False,
        AttributeTypes.RoomLocation:            False,
        AttributeTypes.ListenerShortName:       False,
        AttributeTypes.ListenerDescription:     False,
        AttributeTypes.SourceShortName:         False,
        AttributeTypes.SourceDescription:       False,
        AttributeTypes.ReceiverShortName:       False,
        AttributeTypes.ReceiverDescription:     False,
        AttributeTypes.EmitterShortName:        False,
        AttributeTypes.EmitterDescription:      False,
    }

    defaultAttributeValues = {
        AttributeTypes.Conventions: 'SOFA',
        AttributeTypes.Version: SOFAAPI.getSpecificationsVersion(),
        AttributeTypes.DataType: 'FIR',
        AttributeTypes.SOFAConventions: 'SimpleFreeFieldHRIR',
        # TODO: importing SimpleFreeFieldHRIR causes multiple circular dependency errors to happen
        # AttributeTypes.SOFAConventionsVersion: 'SimpleFreeFieldHRIR::GetConventionVersion()',
        AttributeTypes.SOFAConventionsVersion: '',
        AttributeTypes.APIName: SOFAAPI.getAPIName(),
        AttributeTypes.APIVersion: SOFAAPI.getAPIVersion(),
        AttributeTypes.License: 'No license provided, ask the author for permission.',
        AttributeTypes.RoomType: 'free field'
    }