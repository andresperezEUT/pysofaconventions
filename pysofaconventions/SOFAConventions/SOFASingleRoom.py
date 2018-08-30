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
#   @file   SOFASingleRoom.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofaconventions import SOFAFile, SOFAWarning
import warnings

class SOFASingleRoomDRIR(SOFAFile):

    conventionVersionMajor = 0
    conventionVersionMinor = 3

    def isValid(self):
        """
        Check for convention consistency
        It ensures general file consistency, and also specifics for this convention.
        - 'DataType' == 'FIR'
        - 'SOFAConventions' == 'SingleRoomDRIR'
        - 'RoomType' == 'reverberant'
        - Mandatory attribute 'RoomDescription'
        - ListenerUp and ListenerView are mandatory
        - E == 1

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

        if not self.getGlobalAttributeValue('SOFAConventions') == 'SingleRoomDRIR':
            warnings.warn('SOFAConventions is not SingleRoomDRIR', SOFAWarning)
            return False

        if not self.getGlobalAttributeValue('RoomType') == 'reverberant':
            warnings.warn('RoomType is not "reverberant, got: "'
                          +self.getGlobalAttributeValue('RoomType'), SOFAWarning)
            return False

        if not self.hasGlobalAttribute('RoomDescription'):
            warnings.warn('Missing required Global Attribute "RoomDescription"', SOFAWarning)
            return False


        ##  Variables
        if not self.hasListenerUp() or not self.hasListenerView():
            warnings.warn('Mandatory Variables ListenerUp and ListenerView not found', SOFAWarning)
            return False


        ## Dimensions
        if not self.getDimensionSize('E') == 1:
            warnings.warn('Number of emitters (E) should be 1, got '
                          +str(self.getDimensionSize('E')), SOFAWarning)
            return False

        return True