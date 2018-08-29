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
#   @file   SOFAPositionVariable.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .SOFANcFile import SOFANetCDFFile

class SOFAPositionVariable(object):


    def __init__(self,var):
        self.variable = var

    def isNull(self):
        if self.variable == None:
            return True
        else:
            return False

    def getDimensions(self):
        return SOFANetCDFFile.getVariableDimensionsFromInstance(self.variable)

    def hasDimensions(self, *dims):
        return SOFANetCDFFile.variableHasDimensions(self.variable, dims)

    def getUnits(self):
        attrUnits = SOFANetCDFFile.getVariableAttributeFromInstance(self.variable, 'Units')

        if attrUnits is not None:
            return attrUnits
        else:
            return None

    def getCoordinates(self):
        attrUnits = SOFANetCDFFile.getVariableAttributeFromInstance(self.variable, 'Type')

        if attrUnits is not None:
            return attrUnits
        else:
            return None