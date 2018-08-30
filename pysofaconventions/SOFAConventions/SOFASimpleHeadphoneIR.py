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
#   @file   SOFASimpleHeadphoneIR.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofaconventions import SOFAFile, SOFAWarning
import warnings

class SOFASimpleHeadphoneIR(SOFAFile):

    conventionVersionMajor = 0
    conventionVersionMinor = 2

    def isValid(self):
        """
        Check for convention consistency
        It ensures general file consistency, and also specifics for this convention.
        - 'DataType' == 'FIR'
        - 'SOFAConventions' == 'SimpleHeadphoneIR'
        - 'RoomType' == 'free field'
        - Mandatory attribute 'ListenerShortName'
        - Mandatory attribute 'ListenerDescription'
        - Mandatory attribute 'SourceDescription'
        - Mandatory attribute 'EmitterDescription'
        - Mandatory attribute 'DatabaseName'
        - Mandatory attribute 'SourceModel'
        - Mandatory attribute 'SourceManufacturer'
        - Mandatory attribute 'SourceURI'
        - E == R

        :return:    Boolean
        :raises:    SOFAWarning with error description, in case
        """

        # Check general file validity
        if not SOFAFile.isValid(self):
            return False


        # Ensure specifics of this convention

        ## Attributes
        if not self.isFIRDataType():
            warnings.warn('DataType is not FIR', SOFAWarning)
            return False

        if not self.getGlobalAttributeValue('SOFAConventions') == 'SimpleHeadphoneIR':
            warnings.warn('SOFAConventions is not SimpleHeadphoneIR', SOFAWarning)
            return False

        if not self.getGlobalAttributeValue('RoomType') == 'free field':
            warnings.warn('RoomType is not "free field"', SOFAWarning)
            return False

        if not self.hasGlobalAttribute('ListenerShortName'):
            warnings.warn('Missing required Global Attribute "ListenerShortName"', SOFAWarning)
            return False

        if not self.hasGlobalAttribute('ListenerDescription'):
            warnings.warn('Missing required Global Attribute "ListenerDescription"', SOFAWarning)
            return False

        if not self.hasGlobalAttribute('SourceDescription'):
            warnings.warn('Missing required Global Attribute "SourceDescription"', SOFAWarning)
            return False

        if not self.hasGlobalAttribute('EmitterDescription'):
            warnings.warn('Missing required Global Attribute "EmitterDescription"', SOFAWarning)
            return False

        if not self.hasGlobalAttribute('DatabaseName'):
            warnings.warn('Missing required Global Attribute "DatabaseName"', SOFAWarning)
            return False

        if not self.hasGlobalAttribute('SourceModel'):
            warnings.warn('Missing required Global Attribute "SourceModel"', SOFAWarning)
            return False

        if not self.hasGlobalAttribute('SourceManufacturer'):
            warnings.warn('Missing required Global Attribute "SourceManufacturer"', SOFAWarning)
            return False

        if not self.hasGlobalAttribute('SourceURI'):
            warnings.warn('Missing required Global Attribute "SourceURI"', SOFAWarning)
            return False

        ## Dimensions
        if not self.getDimensionSize('E') == self.getDimensionSize('R'):
            warnings.warn('Number of emitters (E) and number of receivers (R) should match, got  '
                          +str(self.getDimensionSize('E')) + ","
                          +str(self.getDimensionSize('R')), SOFAWarning)
            return False


        return True
