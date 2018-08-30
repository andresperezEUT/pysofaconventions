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
#   @file   SOFASource.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .SOFAError import SOFAError
from .SOFAPositionVariable import SOFAPositionVariable

class SOFAReceiver(object):

    def __init__(self, receiverPosition, receiverUp, receiverView):

        # Those are variables
        self.receiverPosition = SOFAPositionVariable(receiverPosition)
        self.receiverUp = SOFAPositionVariable(receiverUp)
        self.receiverView = SOFAPositionVariable(receiverView)

        self.checkOptionalVariables()


    def checkOptionalVariables(self):
        """
        ReceiverUp and ReceiverView are optional, but if one is present the other should be present as well
        
        :raises:    SOFAError only one exists
        :return:    True if both exist, or if both does not exist
        """
        if self.hasReceiverUp() and not self.hasReceiverView():
            raise SOFAError("ReceiverUp exists but not ReceiverView")

        if self.hasReceiverView() and not self.hasReceiverUp():
            raise SOFAError("ReceiverView exists but not ReceiverUp")

        return True


    def hasValidDimensions(self, r, c, i, m):
        """
        Check if the current instance has the given dimensions

        :param r:   dimension value R
        :param c:   dimension value C
        :param i:   dimension value I
        :param m:   dimension value E
        :raises:    SOFAError if dimensions are not valid
        :return:    True if dimensions are valid
        """

        # ReceiverPosition is mandatory
        if self.receiverPosition.isNull():
            raise SOFAError("ReceiverPosition Variable not found!")

        # Check if ReceiverPosition variables are fine
        if not (self.receiverPositionHasDimensions(r, c, i) or self.receiverPositionHasDimensions(r, c, m)):
            raise SOFAError("Invalid ReceiverPosition Dimensions (should be [R,C,I] or [R,C,M]): ", self.receiverPosition.getDimensions())

        # check if ReceiverUp, and in this case if dimensions are fine
        if self.hasReceiverUp():
            if not (self.receiverUpHasDimensions(r, c, i) or self.receiverUpHasDimensions(r, c, m)):
                raise SOFAError("Invalid ReceiverUp Dimensions (should be [R,C,I] or [R,C,M]): ", self.receiverPosition.getDimensions())

        # check if ReceiverView, and in this case if dimensions are fine
        if self.hasReceiverView():
            if not (self.receiverViewHasDimensions(r, c, i) or self.receiverViewHasDimensions(r, c, m)):
                raise SOFAError("Invalid ReceiverView Dimensions (should be [R,C,I] or [R,C,M]): ", self.receiverPosition.getDimensions())
            
        return True


    def receiverPositionHasDimensions(self,dim1,dim2,dim3):
        """
        Check if the ReceiverPosition variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :param dim3:    third dimension
        :return:        Boolean
        """
        return self.receiverPosition.hasDimensions(dim1,dim2,dim3)

    def receiverUpHasDimensions(self,dim1,dim2,dim3):
        """
        Check if the ReceiverUp variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :param dim3:    third dimension
        :return:        Boolean
        """
        return self.receiverUp.hasDimensions(dim1,dim2,dim3)

    def receiverViewHasDimensions(self,dim1,dim2,dim3):
        """
        Check if the ReceiverView variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :param dim3:    third dimension
        :return:        Boolean
        """
        return self.receiverView.hasDimensions(dim1,dim2,dim3)

    def hasReceiverUp(self):
        """
        Check if the current instance has ReceiverUp

        :return:    Boolean
        """
        return not self.receiverUp.isNull()

    def hasReceiverView(self):
        """
        Check if the current instance has ReceiverView

        :return:    Boolean
        """
        return not self.receiverView.isNull()