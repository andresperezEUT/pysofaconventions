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

from .SOFAError import SOFAError
from .SOFAPositionVariable import SOFAPositionVariable

class SOFASource(object):

    def __init__(self, sourcePosition, sourceUp, sourceView):

        # Those are variables
        self.sourcePosition = SOFAPositionVariable(sourcePosition)
        self.sourceUp = SOFAPositionVariable(sourceUp)
        self.sourceView = SOFAPositionVariable(sourceView)

        self.checkOptionalVariables()


    def checkOptionalVariables(self):
        """
        SourceUp and SourceView are optional, but if one is present the other should be present as well

        :raises:    SOFAError only one exists
        :return:    True if both exist, or if both does not exist
        """
        if self.hasSourceUp() and not self.hasSourceView():
            raise SOFAError("SourceUp exists but not SourceView")

        if self.hasSourceView() and not self.hasSourceUp():
            raise SOFAError("SourceView exists but not SourceUp")
        
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

        # SourcePosition is mandatory
        if self.sourcePosition.isNull():
            raise SOFAError("SourcePosition Variable not found!")

        # Check if SourcePosition variables are fine
        if not (self.sourcePositionHasDimensions(i, c) or self.sourcePositionHasDimensions(m, c)):
            raise SOFAError("Invalid SourcePosition Dimensions (should be [I,C] or [M,C]): ", self.sourcePosition.getDimensions())

        # check if SourceUp, and in this case if dimensions are fine
        if self.hasSourceUp():
            if not (self.sourceUpHasDimensions(i, c) or self.sourceUpHasDimensions(m, c)):
                raise SOFAError("Invalid SourceUp Dimensions (should be [I,C] or [M,C]): ", self.sourcePosition.getDimensions())

        # check if SourceView, and in this case if dimensions are fine
        if self.hasSourceView():
            if not (self.sourceViewHasDimensions(i, c) or self.sourceViewHasDimensions(m, c)):
                raise SOFAError("Invalid SourceView Dimensions (should be [I,C] or [M,C]): ", self.sourcePosition.getDimensions())
            
        return True


    def sourcePositionHasDimensions(self,dim1,dim2):
        """
        Check if the SourcePosition variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :return:        Boolean
        """
        return self.sourcePosition.hasDimensions(dim1,dim2)

    def sourceUpHasDimensions(self,dim1,dim2):
        """
        Check if the SourceUp variable has the given dimensions

        :param dim1:    first dimension
        :param dim2:    second dimension
        :return:        Boolean
        """
        return self.sourceUp.hasDimensions(dim1, dim2)

    def sourceViewHasDimensions(self,dim1,dim2):
        """
         Check if the SourceView variable has the given dimensions

         :param dim1:    first dimension
         :param dim2:    second dimension
         :return:        Boolean
         """
        return self.sourceView.hasDimensions(dim1, dim2)

    def hasSourceUp(self):
        """
        Check if the current instance has SourceUp

        :return:    Boolean
        """
        return not self.sourceUp.isNull()

    def hasSourceView(self):
        """
        Check if the current instance has SourceView

        :return:    Boolean
        """
        return not self.sourceView.isNull()