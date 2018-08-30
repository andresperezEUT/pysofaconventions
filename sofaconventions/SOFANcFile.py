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
#   @file   SOFANcFile.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import netCDF4
from .SOFAError import SOFAError

class SOFANetCDFFile(object):

    def __init__(self,path,mode):
        self.file = netCDF4.Dataset(path,mode)
        self.filename = path

    def close(self):
        '''
        Close the NetCDFile
        '''
        self.file.close()

    def getGlobalAttributesAsDict(self):
        '''
        Get all Global Attributes as a dictionary

        :return:    a Dictionary
        '''
        return self.file.__dict__

    def getGlobalAttributeValue(self,attr):
        """
        Get the value of an attribute

        :param attr:    the queried attribute name
        :return:        the attribute value
        :raise:         SOFAError if the attribute does not exist
        """
        try:
            return getattr(self.file, attr)
        except AttributeError:
            raise SOFAError('Attribute not found: '+attr)

    def getDimensionsAsDict(self):
        '''
        Get a dictionary with the pairs (dimensionName, netCDF4.Dimension instance)

        :return:    a Dictionary
        '''
        return self.file.dimensions

    def getDimension(self,dimName):
        """
        Return a netCDF4.Dimension instance given a dimensions name

        :param dimName:     the queried dimension name
        :return:            a netCDF4.Dimension instance
        :raise:             SOFAError if dimension does not exist
        """
        try:
            return self.getDimensionsAsDict()[dimName]
        except KeyError:
            raise SOFAError("Dimension not found: "+dimName)

    def getDimensionSize(self,dimName):
        """
        Return the size of a given dimension

        :param dimName:     the queried dimension name
        :return:            the dimension size
        :raise:             SOFAError if dimension does not exist
        """
        try:
            return self.getDimensionsAsDict()[dimName].size
        except KeyError:
            raise SOFAError("Dimension not found: "+dimName)

    def getVariablesAsDict(self):
        """
        Get the file variable instances as a dictionary

        :return:    Dictionary containing the file variables instances
        """
        return self.file.variables

    def getVariableInstance(self,varName):
        """
        Return a netCDF4.Variable instance given a variable name name

        :param dimName:     the queried variable name
        :return:            a netCDF4.Variable instance
        :raise:             SOFAError if variable does not exist
        """
        try:
            return self.file.variables[varName]
        except KeyError:
            raise SOFAError("Variable not found: "+varName)

    def getVariableShape(self,varName):
        """
        Return the shape of a variable given then name

        :param dimName:     the queried variable name
        :return:            the shape of the variable
        :raise:             SOFAError if variable does not exist
        """
        try:
            return self.file.variables[varName].shape
        except KeyError:
            raise SOFAError("Variable not found: " + varName)

    def getVariableValues(self,varName):
        try:
            var = self.getVariableInstance(varName)
        except SOFAError:
            raise SOFAError('Variable not found: ' + varName )

        return var[:]

    def getVariableAttributeFromName(self, varName, attrName):
        """
        Get the value of a variable attribute

        :param varInstance: a variable name
        :param attrName:    the name of the queried attribute
        :return:            the value of the attribute, or None if not found
        """
        varInstance = self.getVariableInstance(varName)
        return  self.getVariableAttributeFromInstance(varInstance,attrName)

    def getVariableDimensionsFromName(self, varName):
        """
        Get the dimensions of a variable

        :param varInstance: a variable name
        :return:            a tuple with the variable dimensions
        """
        varInstance = self.getVariableInstance(varName)
        return self.getVariableDimensionsFromInstance(varInstance)

    def getVariableDimensionalityFromName(self, varName):
        """
        Get the number of dimensions from a variable name

        :param varInstance: a variable name
        :return:            the number of different dimensions
        """
        varInstance = self.getVariableInstance(varName)
        return self.getVariableDimensionalityFromInstance(varInstance)

    #
    #  Following methods operate on the variable instances themselves
    # (no need for retrieve the variable instance from the variable name),
    # so they can be called from outside a class withouth a `file` reference
    # (for example, SOFAPositionVariable)
    #

    @classmethod
    def variableHasDimensions(cls, varInstance, dims):
        """
        Check if the variable dimensions match the given ones

        :param varInstance: an instance of a variable
        :param dims:        a tuple with the dimension values
        :return:            Boolean
        """

        # Check that the number of dimensions match
        if cls.getVariableDimensionalityFromInstance(varInstance) != len(dims):
            return False
        else:
            # Check that the variable dimensions _orderedly_ match with the provided ones
            if cls.getVariableDimensionsFromInstance(varInstance) == dims:
                return True
            else:
                return False

    @classmethod
    def variableHasAttribute(cls, varInstance, attrName):
        """
        Check if the given variable has the attribute with attrName

        :param varInstance: an instance of a variable
        :param attrName:    the name of the queried attribute
        :return:            Boolean
        """
        attributes = varInstance.__dict__

        if attrName in attributes:
            return True
        else:
            return False

    @classmethod
    def getVariableAttributeFromInstance(cls, varInstance, attrName):
        """
        Get the value of a variable attribute

        :param varInstance: an instance of variable
        :param attrName:    the name of the queried attribute
        :return:            the value of the attribute, or None if not found
        """
        if cls.variableHasAttribute(varInstance,attrName):
            a = getattr(varInstance,attrName)
            return a
        else:
            return None

    @classmethod
    def getVariableDimensionsFromInstance(cls, varInstance):
        """
        Get the dimensions from a variable instance

        :param varInstance: a variable instance
        :return:            a tuple with the variable dimensions
        """
        return varInstance.shape

    @classmethod
    def getVariableDimensionalityFromInstance(cls, varInstance):
        """
        Get the number of dimensions from a variable instance

        :param varInstance: a variable instance
        :return:            the number of different dimensions
        """
        return len(varInstance.dimensions)