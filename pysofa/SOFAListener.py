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
#   @file   SOFAListener.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .SOFAError import SOFAError
from .SOFAPositionVariable import SOFAPositionVariable

class SOFAListener(object):

    def __init__(self, listenerPosition, listenerUp, listenerView):

        # Those are variables
        self.listenerPosition = SOFAPositionVariable(listenerPosition)
        self.listenerUp = SOFAPositionVariable(listenerUp)
        self.listenerView = SOFAPositionVariable(listenerView)

        self.checkOptionalVariables()


    def checkOptionalVariables(self):
        """
        ListenerUp and ListenerView are optional, but if one is present the other should be present as well
        
        :raises:    SOFAError only one exists
        :return:    True if both exist, or if both does not exist
        """
        if self.hasListenerUp() and not self.hasListenerView():
            raise SOFAError("ListenerUp exists but not ListenerView")

        if self.hasListenerView() and not self.hasListenerUp():
            raise SOFAError("ListenerView exists but not ListenerUp")

        return True


    def hasValidDimensions(self, i, c, m):
        """
        Check if the current instance has the given dimensions

        :param i:   dimension value I
        :param c:   dimension value C
        :param m:   dimension value M
        :raises:    SOFAError if dimensions are not valid
        :return:    True if dimensions are valid
        """

        # ListenerPosition is mandatory
        if self.listenerPosition.isNull():
            raise SOFAError("ListenerPosition Variable not found!")

        # Check if ListenerPosition variables are fine
        if not (self.listenerPositionHasDimensions(i, c) or self.listenerPositionHasDimensions(m, c)):
            raise SOFAError("Invalid ListenerPosition Dimensions (should be [I,C] or [M,C]): ", self.listenerPosition.getDimensions())

        # check if ListenerUp, and in this case if dimensions are fine
        if self.hasListenerUp():
            if not (self.listenerUpHasDimensions(i, c) or self.listenerUpHasDimensions(m, c)):
                raise SOFAError("Invalid ListenerUp Dimensions (should be [I,C] or [M,C]): ", self.listenerPosition.getDimensions())

        # check if ListenerView, and in this case if dimensions are fine
        if self.hasListenerView():
            if not (self.listenerViewHasDimensions(i, c) or self.listenerViewHasDimensions(m, c)):
                raise SOFAError("Invalid ListenerView Dimensions (should be [I,C] or [M,C]): ", self.listenerPosition.getDimensions())
            
        return True


    def listenerPositionHasDimensions(self,dim1,dim2):
        """
        Check if the ListenerPosition variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :return:        Boolean
        """
        return self.listenerPosition.hasDimensions(dim1,dim2)

    def listenerUpHasDimensions(self,dim1,dim2):
        """
        Check if the ListenerUp variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :return:        Boolean
        """
        return self.listenerUp.hasDimensions(dim1, dim2)

    def listenerViewHasDimensions(self,dim1,dim2):
        """
         Check if the ListenerView variable has the given dimensions

         :param dim1:    first dimension
         :param dim2:    second dimension
         :return:        Boolean
         """
        return self.listenerView.hasDimensions(dim1, dim2)

    def hasListenerUp(self):
        """
        Check if the current instance has ListenerUp

        :return:    Boolean
        """
        return not self.listenerUp.isNull()

    def hasListenerView(self):
        """
        Check if the current instance has ListenerView

        :return:    Boolean
        """
        return not self.listenerView.isNull()