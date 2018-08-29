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
#   @file   SOFAEmitter.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .SOFAError import SOFAError
from .SOFAPositionVariable import SOFAPositionVariable

class SOFAEmitter(object):

    def __init__(self, emitterPosition, emitterUp, emitterView):

        # Those are variables
        self.emitterPosition = SOFAPositionVariable(emitterPosition)
        self.emitterUp = SOFAPositionVariable(emitterUp)
        self.emitterView = SOFAPositionVariable(emitterView)

        self.checkOptionalVariables()


    def checkOptionalVariables(self):
        """
        EmitterUp and EmitterView are optional, but if one is present the other should be present as well

        :raises:    SOFAError only one exists
        :return:    True if both exist, or if both does not exist
        """
        if self.hasEmitterUp() and not self.hasEmitterView():
            raise SOFAError("EmitterUp exists but not EmitterView")

        if self.hasEmitterView() and not self.hasEmitterUp():
            raise SOFAError("EmitterView exists but not EmitterUp")

        return True


    def hasValidDimensions(self, e, c, i, m):
        """
        Check if the current instance has the given dimensions

        :param e:   dimension value E
        :param c:   dimension value C
        :param i:   dimension value I
        :param m:   dimension value E
        :raises:    SOFAError if dimensions are not valid
        :return:    True if dimensions are valid
        """

        # EmitterPosition is mandatory
        if self.emitterPosition.isNull():
            raise SOFAError("EmitterPosition Variable not found!")

        # Check if EmitterPosition dimensions are fine
        if not (self.emitterPositionHasDimensions(e, c, i) or self.emitterPositionHasDimensions(e, c, m)):
            raise SOFAError("Invalid EmitterPosition Dimensions (should be [E,C,I] or [E,C,M]): ", self.emitterPosition.getDimensions())

        # check if EmitterUp, and in this case if dimensions are fine
        if self.hasEmitterUp():
            if not (self.emitterUpHasDimensions(e, c, i) or self.emitterUpHasDimensions(e, c, m)):
                raise SOFAError("Invalid EmitterUp Dimensions (should be [E,C,I] or [E,C,M]): ", self.emitterPosition.getDimensions())

        # check if EmitterView, and in this case if dimensions are fine
        if self.hasEmitterView():
            if not (self.emitterViewHasDimensions(e, c, i) or self.emitterViewHasDimensions(e, c, m)):
                raise SOFAError("Invalid EmitterView Dimensions (should be [E,C,I] or [E,C,M]): ", self.emitterPosition.getDimensions())

        return True


    def emitterPositionHasDimensions(self,dim1,dim2,dim3):
        """
        Check if the EmitterPosition variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :param dim3:    third dimension
        :return:        Boolean
        """
        return self.emitterPosition.hasDimensions(dim1,dim2,dim3)

    def emitterUpHasDimensions(self,dim1,dim2,dim3):
        """
        Check if the EmitterUp variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :param dim3:    third dimension
        :return:        Boolean
        """
        return self.emitterUp.hasDimensions(dim1,dim2,dim3)

    def emitterViewHasDimensions(self,dim1,dim2,dim3):
        """
        Check if the EmitterView variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :param dim3:    third dimension
        :return:        Boolean
        """
        return self.emitterView.hasDimensions(dim1,dim2,dim3)

    def hasEmitterUp(self):
        """
        Check if the current instance has EmitterUp

        :return:    Boolean
        """
        return not self.emitterUp.isNull()

    def hasEmitterView(self):
        """
        Check if the current instance has EmitterView

        :return:    Boolean
        """
        return not self.emitterView.isNull()