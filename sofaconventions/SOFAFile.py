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
#   @file   SOFAFile.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .SOFAError import SOFAError
from .SOFAWarning import SOFAWarning
from .SOFAAttributes import SOFAAttributes
from .SOFANcFile import SOFANetCDFFile
from .SOFAListener import SOFAListener
from .SOFASource import SOFASource
from .SOFAReceiver import SOFAReceiver
from .SOFAEmitter import SOFAEmitter
from .SOFAUnits import SOFAUnits
from .SOFAPositionVariable import SOFAPositionVariable
import warnings

class SOFAFile(object):

    conventionVersionMajor = None
    conventionVersionMinor = None

    @classmethod
    def getConventionVersion(cls):
        return str(cls.conventionVersionMajor) + "." + str(cls.conventionVersionMinor)

    ###### INIT



    def __init__(self,path,mode):
        self.ncfile = SOFANetCDFFile(path,mode)

    def close(self):
        self.ncfile.close()
        return

    def isValid(self):
        """
        Check file validity in terms of required variables and attributes

        :return:    Boolean
        :raises:    SOFAError with error description, in case
        """
        try:
            self.checkSOFARequiredAttributes()
            self.checkSOFAConvention()
            self.checkSOFADimensionsAreValid()
            self.checkListenerVariables()
            self.checkSourceVariables()
            self.checkReceiverVariables()
            self.checkEmitterVariables()
            self.checkDataVariable()
        except SOFAError as e:
            warnings.warn(str(e),SOFAWarning)
            return False

        return True


    def getFile(self):
        """
        Get the SOFA file instance reference
        :return:    a SOFA file instance reference
        """
        return self.ncfile.file

    def getFilename(self):
        """
        Get the name of the SOFA file
        :return:    the name of the SOFA file
        """
        return self.ncfile.filename

    def hasGlobalAttribute(self,attr):
        """
        Query if the given attribute exists

        :param attr:    The queried attribute
        :return:        True if attribute exists, False otherwise
        """
        attrDict = self.ncfile.getGlobalAttributesAsDict()
        return attr in attrDict

    def getGlobalAttributesAsDict(self):
        """
        Get the global attributes as a dictionary

        :return:    Dictionary containing the global attributes
        """
        return self.ncfile.getGlobalAttributesAsDict()

    def getGlobalAttributeValue(self,attrName):
        """
        Get the value of the given Attribute

        :param attrName:    The queried attribute name
        :return:            The value of the queried attribute
        :raises:            SOFAError if the attribute does not exist
        """
        try:
            return self.ncfile.getGlobalAttributeValue(attrName)
        except SOFAError:
            raise SOFAError('Attribute not found: ' + attrName)

    def getDimensionsAsDict(self):
        """
        Get the dimensions as a dictionary

        :return:    Dictionary containing the file dimensions
        """
        return self.ncfile.getDimensionsAsDict()

    def getDimension(self,dim):
        """
        Get a instance of the queried dimension

        :param dim: Symbol representing the dimension
        :return:    A netCDF4.Dimension instance
        :raises:    SOFAError if the dimension does not exist
        """
        try:
            return self.ncfile.getDimension(dim)
        except SOFAError:
            raise SOFAError('Dimension not found: '+ dim)

    def getDimensionSize(self,dim):
        """
        Get the size of the queried dimension

        :param dim: Symbol representing the dimension
        :return:    Size of the dimension (number)
        :raises:    SOFAError if the dimension does not exist
        """
        try:
            return self.ncfile.getDimensionSize(dim)
        except SOFAError:
            raise SOFAError('Dimension not found: '+ dim)


    def getVariablesAsDict(self):
        """
        Get the file variable instances as a dictionary

        :return:    Dictionary containing the file variables instances
        """
        return self.ncfile.getVariablesAsDict()


    def hasVariable(self,varName):
        """
        Query if the given variable exists

        :param varName: A variable name
        :return:        True if variable exists, False otherwise
        """
        if varName in self.getVariablesAsDict():
            return True
        else:
            return False

    def getVariableShape(self,varName):
        """
        Get the shape of a variable, given its name

        :param varName: A variable name
        :return:        Variable shape as a Tuple
        :raises:        SOFAError if variable does not exist
        """
        try:
            return self.ncfile.getVariableShape(varName)
        except SOFAError:
            raise SOFAError('Variable not found: ' + varName)


    def getVariableDimensionality(self,varName):
        """
        Get the dimensionality of a variable (number of dimensions), given its name

        :param varName:     A variable name
        :return:            The number of dimensions
        :raises:            SOFAError if variable does not exist
        """
        try:
            return self.ncfile.getVariableDimensionalityFromName(varName)
        except SOFAError:
            raise SOFAError('Variable not found: ' + varName)

    def getVariableValue(self,varName):
        """
        Get the values of a variable, given its name

        :param varName: A variable name
        :return:        a numpy array containing the data
        :raises:        SOFAError if variable does not exist
        """
        try:
            return self.ncfile.getVariableValues(varName)
        except SOFAError:
            raise SOFAError('Variable not found: ' + varName)

    def getVariableInstance(self,varName):
        """
        Get the instance of a variable, given its name

        :param varName: A variable name
        :return:        An instance of netCDF4.Variable
        :raises:        SOFAError if variable does not exist
        """
        try:
            return self.ncfile.getVariableInstance(varName)
        except SOFAError:
            raise SOFAError('Variable not found: ' + varName)

    def getVariableAttributeValue(self,varName,attrName):
        """
        Get the instance of a variable, given its name

        :param varName:     A variable name
        :param attrName:    An attribute name
        :return:            The value of the queried attribute, or None if attr does not exist
        :raises:            SOFAError if variable does not exist
        """
        try:
            return self.ncfile.getVariableAttributeFromName(varName, attrName)
        except SOFAError:
            raise SOFAError('Variable not found: ' + varName )




    def getPositionVariableInfo(self,varName):
        """
        Get Units and Coordinates of a position variable

        :param varName: The variable name
        :return:        a Tuple (units,coordinates), with None values if they do not exist
        :raises:        SOFAError if the variable is not found
        """
        try:
            varInstance = self.getVariableInstance(varName)
            positionVariable = SOFAPositionVariable(varInstance)
            return positionVariable.getUnits(), positionVariable.getCoordinates()
        except SOFAError:
            raise SOFAError('Variable not found: ' + varName)


    ################# GET DATA!

    def hasListenerView(self):
        """
        Check if file has ListenerView
        :return: Boolean
        """
        return self.hasVariable('ListenerView')

    def hasListenerUp(self):
        """
        Check if file has ListenerUp
        :return: Boolean
        """
        return self.hasVariable('ListenerUp')

    def hasSourceView(self):
        """
        Check if file has SourceView
        :return: Boolean
        """
        return self.hasVariable('SourceView')

    def hasSourceUp(self):
        """
        Check if file has SourceUp
        :return: Boolean
        """
        return self.hasVariable('SourceUp')

    def hasReceiverView(self):
        """
        Check if file has ReceiverView
        :return: Boolean
        """
        return self.hasVariable('ReceiverView')

    def hasReceiverUp(self):
        """
        Check if file has ReceiverUp
        :return: Boolean
        """
        return self.hasVariable('ReceiverUp')

    def hasEmitterView(self):
        """
        Check if file has EmitterView
        :return: Boolean
        """
        return self.hasVariable('EmitterView')

    def hasEmitterUp(self):
        """
        Check if file has EmitterUp
        :return: Boolean
        """
        return self.hasVariable('EmitterUp')


    def getListenerPositionInfo(self):
        """
        Get Units and Coordinates of ListenerPosition
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('ListenerPosition')

    def getListenerUpInfo(self):
        """
        Get Units and Coordinates of ListenerUp
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('ListenerUp')

    def getListenerViewInfo(self):
        """
        Get Units and Coordinates of ListenerView
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('ListenerView')

    def getSourcePositionInfo(self):
        """
        Get Units and Coordinates of SourcePosition
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('SourcePosition')

    def getSourceUpInfo(self):
        """
        Get Units and Coordinates of SourceUp
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('SourceUp')

    def getSourceViewInfo(self):
        """
        Get Units and Coordinates of SourceView
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('SourceView')


    def getReceiverPositionInfo(self):
        """
        Get Units and Coordinates of ReceiverPosition
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('ReceiverPosition')

    def getReceiverUpInfo(self):
        """
        Get Units and Coordinates of ReceiverUp
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('ReceiverUp')

    def getReceiverViewInfo(self):
        """
        Get Units and Coordinates of ReceiverView
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('ReceiverView')

    def getEmitterPositionInfo(self):
        """
        Get Units and Coordinates of EmitterPosition
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('EmitterPosition')

    def getEmitterUpInfo(self):
        """
        Get Units and Coordinates of EmitterUp

        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('EmitterUp')

    def getEmitterViewInfo(self):
        """
        Get Units and Coordinates of EmitterView
        :return: a Tuple (units,coordinates), with value None if not found
        """
        return self.getPositionVariableInfo('EmitterView')



    def getListenerPositionValues(self):
        """
        Get Values of ListenerPosition
        :return: ndarray with the values
        """
        return self.getVariableValue('ListenerPosition')

    def getListenerUpValues(self):
        """
        Get Values of ListenerUp
        :return: ndarray with the values
        """
        return self.getVariableValue('ListenerUp')

    def getListenerViewValues(self):
        """
        Get Values of ListenerView
        :return: ndarray with the values
        """
        return self.getVariableValue('ListenerView')

    def getSourcePositionValues(self):
        """
        Get Values of SourcePosition
        :return: ndarray with the values
        """
        return self.getVariableValue('SourcePosition')

    def getSourceUpValues(self):
        """
        Get Values of SourceUp
        :return: ndarray with the values
        """
        return self.getVariableValue('SourceUp')

    def getSourceViewValues(self):
        """
        Get Values of SourceView
        :return: ndarray with the values
        """
        return self.getVariableValue('SourceView')

    def getReceiverPositionValues(self):
        """
        Get Values of ReceiverPosition
        :return: ndarray with the values
        """
        return self.getVariableValue('ReceiverPosition')

    def getReceiverUpValues(self):
        """
        Get Values of ReceiverUp
        :return: ndarray with the values
        """
        return self.getVariableValue('ReceiverUp')

    def getReceiverViewValues(self):
        """
        Get Values of ReceiverView
        :return: ndarray with the values
        """
        return self.getVariableValue('ReceiverView')

    def getEmitterPositionValues(self):
        """
        Get Values of EmitterPosition
        :return: ndarray with the values
        """
        return self.getVariableValue('EmitterPosition')

    def getEmitterUpValues(self):
        """
        Get Values of EmitterUp
        :return: ndarray with the values
        """
        return self.getVariableValue('EmitterUp')

    def getEmitterViewValues(self):
        """
        Get Values of EmitterView
        :return: ndarray with the values
        """
        return self.getVariableValue('EmitterView')


    def getDataIR(self):
        """
        Get Values of Data.IR (the actual data)
        :return: ndarray with the values
        """
        return self.getVariableValue('Data.IR')

    def getDataDelay(self):
        """
        Get Values of Data.Delay
        :return: ndarray with the values
        """
        return self.getVariableValue('Data.Delay')

    def getSamplingRate(self):
        """
        Get Values of Data.SamplingRate
        :return: ndarray with the values
        """
        return self.getVariableValue('Data.SamplingRate')


    def getSamplingRateUnits(self):
        """
        Get Units of Data.SamplingRate
        :return: Unit value
        """
        return self.getVariableAttributeValue('Data.SamplingRate','Units')

    def getDataIRChannelOrdering(self):
        """
        Get ChannelOrdering of Data.IR (AmbisonicsDRIR only)
        :return: value string
        """
        return self.getVariableAttributeValue('Data.IR', 'ChannelOrdering')

    def getDataIRNormalization(self):
        """
        Get Normalization of Data.IR (AmbisonicsDRIR only)
        :return: value string
        """
        return self.getVariableAttributeValue('Data.IR', 'Normalization')


    def printSOFAGlobalAttributes(self):
        """
        Print a list of the global attributes with their values
        """
        for attr in self.getGlobalAttributesAsDict():
            print('- ' + attr)
            print('\t' + self.getGlobalAttributeValue(attr))

    def printSOFADimensions(self):
        """
        Print a list of the file dimensions
        """
        for dim in self.getDimensionsAsDict():
            print('- ' + self.getSOFADimensionStrings(dim) + ' : ' + str(self.getDimensionSize(dim)))


    def getSOFADimensionStrings(self,dim):
        """
        Get an explanatory text of a dimension symbol

        :param dim: the queried dimension symbol
        :return:    an explanatory string
        """
        if dim == 'M':      return "Number of measurements (M)"
        elif dim == 'R':    return "Number of receivers (R)"
        elif dim == 'E':    return "Number of emitters (E)"
        elif dim == 'N':    return "Number of data samples (N)"
        # Ignore the rest
        else:               return dim

    def printSOFAVariables(self):
        """
        Print the file variables and their dimensions
        """
        for var in self.getVariablesAsDict():
            print("- " + var + " = " + str(self.getVariableShape(var)))


    ##### check stuff

    def checkSOFARequiredAttributes(self):
        """
        Check if the file has all required attributes.
        Does not check the values.

        :return:    True if all required atributes exist
        :raises:    SOFAError if at least one required attribute is missing
        """
        for attrName in SOFAAttributes.getAttributeNames():
            if SOFAAttributes.isRequired(attrName):
                if attrName not in self.getGlobalAttributesAsDict():
                    raise SOFAError(str('Missing required attribute: '+attrName))

        return True

    def checkSOFAConvention(self):
        """
        Check if the file follows the SOFA data type convention

        :return:    True if the convention is 'SOFA'
        :raises:    SOFAError if the convention is not 'SOFA'
        """
        if self.getGlobalAttributeValue('Conventions') != 'SOFA':
            raise SOFAError('File convention is not SOFA: ' + self.getGlobalAttributeValue('Conventions'))

        return True


    def checkSOFADimensionsAreValid(self):
        """
        Check if the dimensions of the file are valid

        :return:    True if the dimensions are valid
        :raises:    SOFAError if the dimensions or their sizes are not valid
        """
        # Check that required dimensions exist
        self.getDimension('M')
        self.getDimension('N')
        self.getDimension('R')
        self.getDimension('E')
        self.getDimension('I')
        self.getDimension('C')

        # Check that dimension sizes are correct
        if self.getDimensionSize('M') < 1:
            raise SOFAError('Incorrect dimension size for M: '+str(self.getDimensionSize('M')))
        if self.getDimensionSize('N') < 1:
            raise SOFAError('Incorrect dimension size for N: '+str(self.getDimensionSize('N')))
        if self.getDimensionSize('R') < 1:
            raise SOFAError('Incorrect dimension size for R: '+str(self.getDimensionSize('R')))
        if self.getDimensionSize('E') < 1:
            raise SOFAError('Incorrect dimension size for E: '+str(self.getDimensionSize('E')))
        if self.getDimensionSize('I') != 1:
            raise SOFAError('Incorrect dimension size for I: '+str(self.getDimensionSize('I')))
        if self.getDimensionSize('C') != 3:
            raise SOFAError('Incorrect dimension size for C: '+str(self.getDimensionSize('C')))

        return True

    def checkListenerVariables(self):
        """
        Check if Listener is valid

        :return:    True if the Source is valid
        :raises:    SOFAError if the Listener is not valid
        """

        # Check that required Listener variables exist
        try:
            self.getVariableInstance('ListenerPosition')
        except SOFAError:
            raise SOFAError('Missing Variable: ListenerPosition')


        # Check that Listener is consistent
        listenerPosition = self.getVariableInstance('ListenerPosition')
        units, coordinates =  self.getPositionVariableInfo('ListenerPosition')
        if units is None:
            raise SOFAError('Missing Variable Attribute: ListenerPosition.Units')
        if coordinates is None:
            raise SOFAError('Missing Variable Attribute: ListenerPosition.Coordinates')

        if self.hasListenerUp():
            listenerUp = self.getVariableInstance('ListenerUp')
            units, coordinates = self.getPositionVariableInfo('ListenerUp')
            if units is None:
                raise SOFAError('Missing Variable Attribute: ListenerUp.Units')
            if coordinates is None:
                raise SOFAError('Missing Variable Attribute: ListenerUp.Coordinates')
        else:
            listenerUp = None

        if self.hasListenerView():
            listenerView = self.getVariableInstance('ListenerView')
            units, coordinates = self.getPositionVariableInfo('ListenerView')
            if units is None:
                raise SOFAError('Missing Variable Attribute: ListenerView.Units')
            if coordinates is None:
                raise SOFAError('Missing Variable Attribute: ListenerView.Coordinates')
        else:
            listenerView = None

        listener = SOFAListener(listenerPosition, listenerUp, listenerView)
        listener.hasValidDimensions(self.getDimensionSize('I'),
                                    self.getDimensionSize('C'),
                                    self.getDimensionSize('M'))

        return True


    def checkSourceVariables(self):
        """
        Check if Source is valid

        :return:    True if the Source is valid
        :raises:    SOFAError if the Source is not valid
        """

        # Check that required Source variables exist
        try:
            self.getVariableInstance('SourcePosition')
        except SOFAError:
            raise SOFAError('Missing Variable: SourcePosition')


        # Check that Source is consistent
        sourcePosition = self.getVariableInstance('SourcePosition')
        units, coordinates =  self.getPositionVariableInfo('SourcePosition')
        if units is None:
            raise SOFAError('Missing Variable Attribute: SourcePosition.Units')
        if coordinates is None:
            raise SOFAError('Missing Variable Attribute: SourcePosition.Coordinates')

        if self.hasSourceUp():
            sourceUp = self.getVariableInstance('SourceUp')
            units, coordinates = self.getPositionVariableInfo('SourceUp')
            if units is None:
                raise SOFAError('Missing Variable Attribute: SourceUp.Units')
            if coordinates is None:
                raise SOFAError('Missing Variable Attribute: SourceUp.Coordinates')
        else:
            sourceUp = None

        if self.hasSourceView():
            sourceView = self.getVariableInstance('SourceView')
            units, coordinates = self.getPositionVariableInfo('SourceView')
            if units is None:
                raise SOFAError('Missing Variable Attribute: SourceView.Units')
            if coordinates is None:
                raise SOFAError('Missing Variable Attribute: SourceView.Coordinates')
        else:
            sourceView = None

        source = SOFASource(sourcePosition, sourceUp, sourceView)
        source.hasValidDimensions(self.getDimensionSize('I'),
                                  self.getDimensionSize('C'),
                                  self.getDimensionSize('M'))

        return True


    def checkReceiverVariables(self):
        """
        Check if Receiver is valid

        :return:    True if all Emitter variables are valid
        :raises:    SOFAError if the Receiver is not valid
        """

        # Check that required Receiver variables exist
        try:
            self.getVariableInstance('ReceiverPosition')
        except SOFAError:
            raise SOFAError('Missing Variable: ReceiverPosition')


        # Check that Receiver is consistent
        receiverPosition = self.getVariableInstance('ReceiverPosition')
        units, coordinates = self.getPositionVariableInfo('ReceiverPosition')
        if units is None:
            raise SOFAError('Missing Variable Attribute: ReceiverPosition.Units')
        if coordinates is None:
            raise SOFAError('Missing Variable Attribute: ReceiverPosition.Coordinates')

        if self.hasReceiverUp():
            receiverUp = self.getVariableInstance('ReceiverUp')
            units, coordinates = self.getPositionVariableInfo('ReceiverUp')
            if units is None:
                raise SOFAError('Missing Variable Attribute: ReceiverUp.Units')
            if coordinates is None:
                raise SOFAError('Missing Variable Attribute: ReceiverUp.Coordinates')
        else:
            receiverUp = None

        if self.hasReceiverView():
            receiverView = self.getVariableInstance('ReceiverView')
            units, coordinates = self.getPositionVariableInfo('ReceiverView')
            if units is None:
                raise SOFAError('Missing Variable Attribute: ReceiverView.Units')
            if coordinates is None:
                raise SOFAError('Missing Variable Attribute: ReceiverView.Coordinates')
        else:
            receiverView = None

        receiver = SOFAReceiver(receiverPosition, receiverUp, receiverView)
        receiver.hasValidDimensions(self.getDimensionSize('R'),
                                    self.getDimensionSize('C'),
                                    self.getDimensionSize('I'),
                                    self.getDimensionSize('M'))
        return True


    def checkEmitterVariables(self):
        """
        Check if Emitter is valid

        :return:    True if all Emitter variables are valid
        :raises:    SOFAError if the Emitter is not valid
        """

        # Check that required Emitter variables exist
        try:
            self.getVariableInstance('EmitterPosition')
        except SOFAError:
            raise SOFAError('Missing Variable: EmitterPosition')


        # Check that Emitter is consistent
        emitterPosition = self.getVariableInstance('EmitterPosition')
        units, coordinates = self.getPositionVariableInfo('EmitterPosition')
        if units is None:
            raise SOFAError('Missing Variable Attribute: EmitterPosition.Units')
        if coordinates is None:
            raise SOFAError('Missing Variable Attribute: EmitterPosition.Coordinates')

        if self.hasEmitterUp():
            emitterUp = self.getVariableInstance('EmitterUp')
            units, coordinates = self.getPositionVariableInfo('EmitterUp')
            if units is None:
                raise SOFAError('Missing Variable Attribute: EmitterUp.Units')
            if coordinates is None:
                raise SOFAError('Missing Variable Attribute: EmitterUp.Coordinates')
        else:
            emitterUp = None

        if self.hasEmitterView():
            emitterView = self.getVariableInstance('EmitterView')
            units, coordinates = self.getPositionVariableInfo('EmitterView')
            if units is None:
                raise SOFAError('Missing Variable Attribute: EmitterView.Units')
            if coordinates is None:
                raise SOFAError('Missing Variable Attribute: EmitterView.Coordinates')
        else:
            emitterView = None

        emitter = SOFAEmitter(emitterPosition, emitterUp, emitterView)
        emitter.hasValidDimensions(self.getDimensionSize('E'),
                                   self.getDimensionSize('C'),
                                   self.getDimensionSize('I'),
                                   self.getDimensionSize('M'))

        return True

    def checkDataVariable(self):
        """
        Check consistency and availability of Data

        :return:    True if Data is consistent
        :raises:    SOFAError if Data is inconsistent
        """

        try:
            dataType = self.getGlobalAttributeValue('DataType')
        except SOFAError:
            raise SOFAError('No DataType attribute')

        if      self.isFIRDataType():   self.checkFIRDataType()
        elif    self.isFIREDataType():  self.checkFIREDataType()
        elif    self.isSOSDataType():   self.checkSOSDataType()
        elif    self.isTFDataType():    self.checkTFDataType()
        else:
            raise SOFAError('DataType not known: ' + dataType)

        return True


    def isFIRDataType(self):
        return self.getGlobalAttributeValue('DataType') == 'FIR'

    def isFIREDataType(self):
        return self.getGlobalAttributeValue('DataType') == 'FIRE'

    def isSOSDataType(self):
        return self.getGlobalAttributeValue('DataType') == 'SOS'

    def isTFDataType(self):
        return self.getGlobalAttributeValue('DataType') == 'TF'


    def checkFIRDataType(self):
        """
        Data.ir [M,R,N]
        Data.samplingRate [I] or [M]
        Data.delay [I,R] or [M,R]

        :return:    True if Data is consistent
        :raises:    SOFAError if Data is inconsistent
        """

        m = self.getDimensionSize('M')
        n = self.getDimensionSize('N')
        i = self.getDimensionSize('I')
        r = self.getDimensionSize('R')


        # Data.IR variable should exist and have dimension [M,R,N]
        try:
            ir = self.getVariableInstance('Data.IR')
        except SOFAError:
            raise SOFAError('Missing Data.IR Variable')

        if not SOFANetCDFFile.variableHasDimensions(ir, (m, r, n)):
            raise SOFAError('Incorrect Data.IR dimensions: '+str(self.getVariableShape(ir.name))
                            + '. Expected [M,R,N]')


        # Data.SamplingRate variable should exist and have dimension [I] or [R]
        try:
            samplingRate = self.getVariableInstance('Data.SamplingRate')
        except SOFAError:
            raise SOFAError('Missing Data.SamplingRate Variable')

        if not SOFANetCDFFile.variableHasDimensions(samplingRate,(i,)) and not SOFANetCDFFile.variableHasDimensions(samplingRate, (m,)):
            raise SOFAError('Incorrect Data.SamplingRate dimensions: ' + str(self.getVariableShape(samplingRate.name))
                            + '. Expected [I] or [R]')


        # Data.SamplingRate should have Units attribute in Hertzs
        samplingRateUnits = SOFANetCDFFile.getVariableAttributeFromInstance(samplingRate,'Units')

        if samplingRateUnits is None:
            raise SOFAError('Missing Attribute Data.SamplingRate.Units')

        if not SOFAUnits.isFrequencyUnit(samplingRateUnits):
            raise SOFAError('Attribute Data.SamplingRate.Units is not a frequency unit: '+samplingRateUnits)


        # Data.Delay should exist and have dimension [I,R] or [M,R]
        try:
            delay = self.getVariableInstance('Data.Delay')
        except SOFAError:
            raise SOFAError('Missing Data.Delay Variable')

        if not SOFANetCDFFile.variableHasDimensions(delay,(i,r)) and not SOFANetCDFFile.variableHasDimensions(delay, (m,r)):
            raise SOFAError('Incorrect Data.Delay dimensions: ' + str(self.getVariableShape(delay.name))
                            + '. Expected [I,R] or [M,R]')

        return True


    def checkFIREDataType(self):
        """
        Data.ir [M,R,E,N]
        Data.samplingRate [I] or [M]
        Data.delay [I,R,E] or [M,R,E]

        :return:    True if Data is consistent
        :raises:    SOFAError if Data is inconsistent
        """

        m = self.getDimensionSize('M')
        n = self.getDimensionSize('N')
        i = self.getDimensionSize('I')
        r = self.getDimensionSize('R')
        e = self.getDimensionSize('E')

        # Data.IR variable should exist and have dimension [M,R,E,N]
        try:
            ir = self.getVariableInstance('Data.IR')
        except SOFAError:
            raise SOFAError('Missing Data.IR Variable')

        if not SOFANetCDFFile.variableHasDimensions(ir, (m, r, e, n)):
            raise SOFAError('Incorrect Data.IR dimensions: '+str(self.getVariableShape(ir.name))
                            + '. Expected [M,R,E,N]')


        # Data.SamplingRate variable should exist and have dimension [I] or [R]
        try:
            samplingRate = self.getVariableInstance('Data.SamplingRate')
        except SOFAError:
            raise SOFAError('Missing Data.SamplingRate Variable')

        if not SOFANetCDFFile.variableHasDimensions(samplingRate,(i,)) and not SOFANetCDFFile.variableHasDimensions(samplingRate, (m,)):
            raise SOFAError('Incorrect Data.SamplingRate dimensions: ' + str(self.getVariableShape(samplingRate.name))
                            + '. Expected [I] or [R]')


        # Data.SamplingRate should have Units attribute in Hertzs
        samplingRateUnits = SOFANetCDFFile.getVariableAttributeFromInstance(samplingRate,'Units')

        if samplingRateUnits is None:
            raise SOFAError('Missing Attribute Data.SamplingRate.Units')

        if not SOFAUnits.isFrequencyUnit(samplingRateUnits):
            raise SOFAError('Attribute Data.SamplingRate.Units is not a frequency unit: '+samplingRateUnits)


        # Data.Delay should exist and have dimension [I,R,E] or [M,R,E]
        try:
            delay = self.getVariableInstance('Data.Delay')
        except SOFAError:
            raise SOFAError('Missing Data.Delay Variable')

        if not SOFANetCDFFile.variableHasDimensions(delay,(i,r,e)) and not SOFANetCDFFile.variableHasDimensions(delay, (m,r,e)):
            raise SOFAError('Incorrect Data.Delay dimensions: '+str(self.getVariableShape(delay.name))
                            + '. Expected [I,R,E] or [M,R,E]')

        return True



    def checkSOSDataType(self):
        """
        Data.ir [M,R,N]
        Data.samplingRate [I] or [M]
        Data.delay [I,R] or [M,R]

        :return:    True if Data is consistent
        :raises:    SOFAError if Data is inconsistent
        """

        m = self.getDimensionSize('M')
        n = self.getDimensionSize('N')
        i = self.getDimensionSize('I')
        r = self.getDimensionSize('R')

        # Data.IR variable should exist and have dimension [M,R,N]
        try:
            ir = self.getVariableInstance('Data.IR')
        except SOFAError:
            raise SOFAError('Missing Data.IR Variable')

        if not SOFANetCDFFile.variableHasDimensions(ir, (m, r, n)):
            raise SOFAError('Incorrect Data.IR dimensions: ' + str(self.getVariableShape(ir.name))
                            + '. Expected [M,R,N]')

        # Data.SamplingRate variable should exist and have dimension [I] or [R]
        try:
            samplingRate = self.getVariableInstance('Data.SamplingRate')
        except SOFAError:
            raise SOFAError('Missing Data.SamplingRate Variable')

        if not SOFANetCDFFile.variableHasDimensions(samplingRate, (i,)) and not SOFANetCDFFile.variableHasDimensions(samplingRate, (m,)):
            raise SOFAError(
                'Incorrect Data.SamplingRate dimensions: ' + str(self.getVariableShape(samplingRate.name))
                + '. Expected [I] or [R]')

        # Data.SamplingRate should have Units attribute in Hertzs
        samplingRateUnits = SOFANetCDFFile.getVariableAttributeFromInstance(samplingRate, 'Units')

        if samplingRateUnits is None:
            raise SOFAError('Missing Attribute Data.SamplingRate.Units')

        if not SOFAUnits.isFrequencyUnit(samplingRateUnits):
            raise SOFAError('Attribute Data.SamplingRate.Units is not a frequency unit: ' + samplingRateUnits)

        # Data.Delay should exist and have dimension [I,R] or [M,R]
        try:
            delay = self.getVariableInstance('Data.Delay')
        except SOFAError:
            raise SOFAError('Missing Data.Delay Variable')

        if not SOFANetCDFFile.variableHasDimensions(delay, (i, r)) and not SOFANetCDFFile.variableHasDimensions(delay, (m, r)):
            raise SOFAError('Incorrect Data.Delay dimensions: ' + str(self.getVariableShape(delay.name))
                            + '. Expected [I,R] or [M,R]')

        return True


    def checkTFDataType(self):
        """
        Data.Real [M,R,N]
        Data.Imag [M,R,N]
        N  [N] (units:hertzs, longname)

        :raises:    SOFAError if Data is inconsistent
        """

        m = self.getDimensionSize('M')
        n = self.getDimensionSize('N')
        i = self.getDimensionSize('I')
        r = self.getDimensionSize('R')

        # Data.Real
        try:
            varReal = self.getVariableInstance('Data.Real')
        except SOFAError:
            raise SOFAError('Missing Data.Real Variable')

        if not SOFANetCDFFile.variableHasDimensions(varReal, (m, r, n)):
            raise SOFAError('Incorrect Data.Real dimensions: '
                            + str(self.getVariableShape(varReal.name))
                            + '. Expected [M,R,N]')

        # Data.Imag
        try:
            varImag = self.getVariableInstance('Data.Imag')
        except SOFAError:
            raise SOFAError('Missing Data.Imag Variable')

        if not SOFANetCDFFile.variableHasDimensions(varImag, (m, r, n)):
            raise SOFAError('Incorrect Data.Imag dimensions: '
                            + str(self.getVariableShape(varImag.name))
                            + '. Expected [M,R,N]')

        # N
        try:
            varN = self.getVariableInstance('N')
        except SOFAError:
            raise SOFAError('Missing N Variable')

        if not SOFANetCDFFile.variableHasDimensions(varN, (n,)):
            raise SOFAError('Incorrect N dimensions: '
                            + str(self.getVariableShape(varN.name))
                            + '. Expected [N]')

        # N should have Units attribute in Hertzs
        varNUnits = SOFANetCDFFile.getVariableAttributeFromInstance(varN, 'Units')

        if varNUnits is None:
            raise SOFAError('Missing Attribute N.Units')

        if not SOFAUnits.isFrequencyUnit(varNUnits):
            raise SOFAError('Attribute N.Units is not a frequency unit: ' + varNUnits)

        return True