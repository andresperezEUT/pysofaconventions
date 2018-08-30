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
#   @file   SOFAAmbisonicsDRIR.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofaconventions import SOFAFile, SOFAWarning
import warnings

class SOFAAmbisonicsDRIR(SOFAFile):

    conventionVersionMajor = 0
    conventionVersionMinor = 1

    def isValid(self):
        """
        Check for convention consistency
        It ensures general file consistency, and also specifics for this convention.
        - 'DataType' == 'FIRE'
        - 'SOFAConventions' == 'AmbisonicsDRIR'
        - Mandatory global attribute 'AmbisonicsOrder'
        - Mandatory Data.IR attributes 'ChannelOrdering' and 'Normalization'
        - ListenerUp and ListenerView are mandatory
        - EmitterUp and EmitterView are mandatory

        :return:    Boolean
        :raises:    SOFAWarning with error description, in case
        """

        # Check general file validity
        if not SOFAFile.isValid(self):
            return False


        # Ensure specifics of this convention

        ## Attributes
        if not self.isFIREDataType():
            warnings.warn('DataType is not FIRE', SOFAWarning)
            return False

        if not self.getGlobalAttributeValue('SOFAConventions') == 'AmbisonicsDRIR':
            warnings.warn('SOFAConventions is not AmbisonicsDRIR', SOFAWarning)
            return False

        if 'AmbisonicsOrder' not in self.getGlobalAttributesAsDict():
            warnings.warn('Global Attribute AmbisonicsOrder not found', SOFAWarning)
            return False

        if self.getVariableAttributeValue('Data.IR','ChannelOrdering') is None:
            warnings.warn('Data.IR Attribute ChannelOrdering not found', SOFAWarning)
            return False

        if self.getVariableAttributeValue('Data.IR','Normalization') is None:
            warnings.warn('Data.IR Attribute Normalization not found', SOFAWarning)
            return False


        ##  Variables
        if not self.hasListenerUp() or not self.hasListenerView():
            warnings.warn('Mandatory Variables ListenerUp and ListenerView not found', SOFAWarning)
            return False

        if not self.hasEmitterUp() or not self.hasEmitterView():
            warnings.warn('Mandatory Variables EmitterUp and EmitterView not found', SOFAWarning)
            return False


        return True