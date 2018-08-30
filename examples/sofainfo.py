# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   sofainfo.py
#
#   Print information about a given SOFA file
#
#   (C) Andrés Pérez-López - Eurecat / UPF
#   24/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from sofaconventions import *

def printLine():
    print("-----------------------------------------------------------------------\n")

def printBlankLine():
    print("")


# Set here your SOFA file path
path = "/Volumes/Dinge/SOFA/testpysofa.sofa"

# Open the file for reading
file = SOFAFile(path,"r")

# Check validity
if file.isValid():
    print(path + " is a valid SOFA file")
else:
    print(path + " is _NOT_ a valid SOFA file")
    exit()


# Print attributes
printLine()
print("GLOBAL ATTRIBUTES")
file.printSOFAGlobalAttributes()


# Print dimensions
printLine()
print("DIMENSIONS")
file.printSOFADimensions()


# Print variable dimensions
printLine()
print("VARIABLE DIMENSIONS")
file.printSOFAVariables()


# Check SOFAConvention
printLine()
print("CONVENTIONS")
convention = file.getGlobalAttributeValue("SOFAConventions")
print(convention)

if convention == 'AmbisonicsDRIR':
    conventionFile = SOFAAmbisonicsDRIR(path,"r")
elif convention == 'GeneralFIR':
    conventionFile = SOFAGeneralFIR(path,"r")
elif convention == 'GeneralFIRE':
    conventionFile = SOFAGeneralFIRE(path,"r")
elif convention == 'GeneralTF':
    conventionFile = SOFAGeneralTF(path,"r")
elif convention == 'MultiSpeakerBRIR':
    conventionFile = SOFAMultiSpeakerBRIR(path,"r")
elif convention == 'SimpleFreeFieldHRIR':
    conventionFile = SOFASimpleFreeFieldHRIR(path,"r")
elif convention == 'SimpleFreeFieldSOS':
    conventionFile = SOFASimpleFreeFieldSOS(path,"r")
elif convention == 'SimpleHeadphoneIR':
    conventionFile = SOFASimpleHeadphoneIR(path,"r")
elif convention == 'SingleRoomDRIR':
    conventionFile = SOFASingleRoomDRIR(path,"r")
else:
    print(convention + " is _NOT_ a valid SOFA convention type")
    exit()

if conventionFile.isValid():
    print(path + " is a valid " + convention + " SOFA file")
else:
    print(path + " is _NOT_ a valid " + convention + " SOFA file")
    exit()

# Print Variable dimensions
printLine()
print("VARIABLE VALUES")

samplingRate = conventionFile.getSamplingRate()
samplingRateUnits = conventionFile.getSamplingRateUnits()
print("- Data.SamplingRate = " + str(samplingRate))
print("- Data.SamplingRate:Units = " + str(samplingRateUnits))
printBlankLine()

# Listener

listenerPosUnits, listenerPosCoordinates = conventionFile.getListenerPositionInfo()
listenerPos = conventionFile.getListenerPositionValues()
print("- ListenerPosition:Type = " + listenerPosCoordinates)
print("- ListenerPosition:Units = " + listenerPosUnits)
print("- ListenerPosition = " + str(listenerPos))
printBlankLine()

if conventionFile.hasListenerView():
    listenerViewUnits, listenerViewCoordinates = conventionFile.getListenerViewInfo()
    listenerView = conventionFile.getListenerViewValues()
    if listenerViewCoordinates is not None:
        print("- ListenerView:Type = " + listenerViewCoordinates)
    if listenerViewUnits is not None:
        print("- ListenerView:Units = " + listenerViewUnits)
    print("- ListenerView = " + str(listenerView))
    printBlankLine()

if conventionFile.hasListenerUp():
    listenerUpUnits, listenerUpCoordinates = conventionFile.getListenerUpInfo()
    listenerUp = conventionFile.getListenerUpValues()
    if listenerUpCoordinates is not None:
        print("- ListenerUp:Type = " + listenerUpCoordinates)
    if listenerUpUnits is not None:
        print("- ListenerUp:Units = " + listenerUpUnits)
    print("- ListenerUp = " + str(listenerUp))
    printBlankLine()


# Receiver
printBlankLine()
receiverPosUnits, receiverPosCoordinates = conventionFile.getReceiverPositionInfo()
receiverPos = conventionFile.getReceiverPositionValues()
print("- ReceiverPosition:Type = " + receiverPosCoordinates)
print("- ReceiverPosition:Units = " + receiverPosUnits)
print("- ReceiverPosition = " + str(receiverPos))

if conventionFile.hasReceiverView():
    receiverViewUnits, receiverViewCoordinates = conventionFile.getReceiverViewInfo()
    receiverView = conventionFile.getReceiverViewValues()
    print("- ReceiverView:Type = " + receiverViewCoordinates)
    print("- ReceiverView:Units = " + receiverViewUnits)
    print("- ReceiverView = " + str(receiverView))
    printBlankLine()

if conventionFile.hasReceiverUp():
    receiverUpUnits, receiverUpCoordinates = conventionFile.getReceiverUpInfo()
    receiverUp = conventionFile.getReceiverUpValues()
    print("- ReceiverUp:Type = " + receiverUpCoordinates)
    print("- ReceiverUp:Units = " + receiverUpUnits)
    print("- ReceiverUp = " + str(receiverUp))
    printBlankLine()


# Source
printBlankLine()
sourcePosUnits, sourcePosCoordinates = conventionFile.getSourcePositionInfo()
sourcePos = conventionFile.getSourcePositionValues()
print("- SourcePosition:Type = " + sourcePosCoordinates)
print("- SourcePosition:Units = " + sourcePosUnits)
print("- SourcePosition = " + str(sourcePos))

if conventionFile.hasSourceView():
    sourceViewUnits, sourceViewCoordinates = conventionFile.getSourceViewInfo()
    sourceView = conventionFile.getSourceViewValues()
    print("- SourceView:Type = " + sourceViewCoordinates)
    print("- SourceView:Units = " + sourceViewUnits)
    print("- SourceView = " + str(sourceView))
    printBlankLine()

if conventionFile.hasSourceUp():
    sourceUpUnits, sourceUpCoordinates = conventionFile.getSourceUpInfo()
    sourceUp = conventionFile.getSourceUpValues()
    print("- SourceUp:Type = " + sourceUpCoordinates)
    print("- SourceUp:Units = " + sourceUpUnits)
    print("- SourceUp = " + str(sourceUp))
    printBlankLine()


# Emitter
printBlankLine()
emitterPosUnits, emitterPosCoordinates = conventionFile.getEmitterPositionInfo()
emitterPos = conventionFile.getEmitterPositionValues()
print("- EmitterPosition:Type = " + emitterPosCoordinates)
print("- EmitterPosition:Units = " + emitterPosUnits)
print("- EmitterPosition = " + str(emitterPos))

if conventionFile.hasEmitterView():
    emitterViewUnits, emitterViewCoordinates = conventionFile.getEmitterViewInfo()
    emitterView = conventionFile.getEmitterViewValues()
    print("- EmitterView:Type = " + emitterViewCoordinates)
    print("- EmitterView:Units = " + emitterViewUnits)
    print("- EmitterView = " + str(emitterView))
    printBlankLine()

if conventionFile.hasEmitterUp():
    emitterUpUnits, emitterUpCoordinates = conventionFile.getEmitterUpInfo()
    emitterUp = conventionFile.getEmitterUpValues()
    print("- EmitterUp:Type = " + emitterUpCoordinates)
    print("- EmitterUp:Units = " + emitterUpUnits)
    print("- EmitterUp = " + str(emitterUp))
    printBlankLine()


# Ambisonics stuff
if convention == 'AmbisonicsDRIR':
    print("- GLOBAL:AmbisonicsOrder = " + conventionFile.getGlobalAttributeValue('AmbisonicsOrder'))
    print("- Data.IR:ChannelOrdering = " + conventionFile.getDataIRChannelOrdering())
    print("- Data.IR:Normalization = " + conventionFile.getDataIRNormalization())