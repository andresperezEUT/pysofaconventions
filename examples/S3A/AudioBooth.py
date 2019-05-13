# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   AudioBooth.py
#
#   Implementation of conversion from the S3A dataset
#
#   (C) Andrés Pérez-López - Eurecat / UPF
#   01/10/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofaconventions import *
from netCDF4 import Dataset
import time
import numpy as np
import soundfile as sf

#----------Create it----------#

filePath = "/Volumes/Dinge/SOFA/S3A/AudioBooth.sofa"
rootgrp = Dataset(filePath, 'w', format='NETCDF4')


#----------Required Attributes----------#

rootgrp.Conventions = 'SOFA'
rootgrp.Version = SOFAAPI.getAPIVersion()
rootgrp.SOFAConventions = 'AmbisonicsDRIR'
rootgrp.SOFAConventionsVersion = SOFAAmbisonicsDRIR.getConventionVersion()
rootgrp.APIName = 'pysofaconventions'
rootgrp.APIVersion = SOFAAPI.getAPIVersion()
rootgrp.AuthorContact = 'andres.perez@eurecat.org'
rootgrp.Organization = 'Eurecat - UPF'
rootgrp.License = 'Please ask authors for permission'
rootgrp.DataType = 'FIRE'
rootgrp.RoomType = 'reverberant'
rootgrp.DateCreated = time.ctime(time.time())
rootgrp.DateModified = time.ctime(time.time())
rootgrp.Title = 'AudioBooth'
rootgrp.AmbisonicsOrder = '1'


#----------Required Dimensions----------#

M = 1
N = 65536
R = 4
E = 17
I = 1
C = 3
rootgrp.createDimension('M', M)
rootgrp.createDimension('N', N)
rootgrp.createDimension('R', R)
rootgrp.createDimension('E', E)
rootgrp.createDimension('I', I)
rootgrp.createDimension('C', C)


#----------Required Variables----------#

# Listener at the center
listenerPositionVar = rootgrp.createVariable('ListenerPosition',    'f8',   ('I','C'))
listenerPositionVar.Units   = 'metre'
listenerPositionVar.Type    = 'cartesian'
listenerPositionVar[:] = np.zeros(C)

# ListenerUp in the +Z axis
listenerUpVar       = rootgrp.createVariable('ListenerUp',          'f8',   ('I','C'))
listenerUpVar.Units         = 'metre'
listenerUpVar.Type          = 'cartesian'
listenerUpVar[:]    = np.asarray([0,0,1])

# Listener looking to the left (+Y axis)
listenerViewVar     = rootgrp.createVariable('ListenerView',        'f8',   ('I','C'))
listenerViewVar.Units       = 'metre'
listenerViewVar.Type        = 'cartesian'
listenerViewVar[:]  = np.asarray([0,1,0])


# Source at the center
sourcePositionVar = rootgrp.createVariable('SourcePosition',        'f8',   ('I','C'))
sourcePositionVar.Units   = 'metre'
sourcePositionVar.Type    = 'cartesian'
sourcePositionVar[:]      = np.zeros(C)

sourceUpVar       = rootgrp.createVariable('SourceUp',              'f8',   ('I','C'))
sourceUpVar.Units         = 'metre'
sourceUpVar.Type          = 'cartesian'
sourceUpVar[:]    = np.asarray([0,0,1])

sourceViewVar     = rootgrp.createVariable('SourceView',            'f8',   ('I','C'))
sourceViewVar.Units       = 'metre'
sourceViewVar.Type        = 'cartesian'
sourceViewVar[:]  = np.asarray([1,0,0])


# Emitter: From the specs... (cartesian)
emitterPositionVar  = rootgrp.createVariable('EmitterPosition',     'f8',   ('E','C','I'))
emitterPositionVar.Units   = 'metre'
emitterPositionVar.Type    = 'cartesian'
emitterPositions =\
    [[0,1.68000000000000,0],
    [0.987479223851355,1.35914855054991,0],
    [1.59777494737586,0.519148550549912,0],
    [1.59777494737586,-0.519148550549912,0],
    [0.762704039562439,-1.49689096063646,0],
    [-0.762704039562439,-1.49689096063646,0],
    [-1.59777494737586,-0.519148550549912,0],
    [-1.59777494737586,0.519148550549912,0],
    [-0.987479223851355,1.35914855054991,0],
    [0.745260030511565,1.02576243204591,1.10217916870405],
    [1.20585605982450,-0.391806384658784,1.10217916870405],
    [-1.20585605982450,-0.391806384658784,1.10217916870405],
    [-0.745260030511565,1.02576243204591,1.10217916870405],
    [0.855182093564614,1.17705717229302,-0.840000000000000],
    [1.38371369395784,-0.449595833114093,-0.840000000000000],
    [-1.38371369395784,-0.449595833114093,-0.840000000000000],
    [-0.855182093564614,1.17705717229302,-0.840000000000000]]

for e in range(E):
    emitterPositionVar[e, :, :] = np.asarray(emitterPositions[e])

# Receiver
receiverPositionVar = rootgrp.createVariable('ReceiverPosition',  'f8',   ('R','C','I'))
receiverPositionVar.Units   = 'metre'
receiverPositionVar.Type    = 'cartesian'
receiverPositionVar[:]      = np.zeros((R,C))

# From specs
samplingRateVar =   rootgrp.createVariable('Data.SamplingRate', 'f8',   ('I'))
samplingRateVar.Units = 'hertz'
samplingRateVar[:] = 48000

# No delay found
delayVar        =   rootgrp.createVariable('Data.Delay',        'f8',   ('I','R','E'))
delay = np.zeros((I,R,E))
delayVar[:,:,:] = delay

# Parse the audio files...
dataIRVar =         rootgrp.createVariable('Data.IR', 'f8', ('M','R','E','N'))
dataIRVar.ChannelOrdering   = 'fuma'
dataIRVar.Normalization     = 'fuma'

audioFilesPath = '/Volumes/Dinge/audio/S3A_original/AudioBooth/Soundfield/'
for e in range(E):

    fileIdx = e+1 # Numeration starts at 1
    fileName = 'ls' + str(fileIdx) + '.wav'

    # Open the audio file
    data, samplerate = sf.read(audioFilesPath + fileName)
    assert samplerate == 48000
    assert np.shape(data) == (65536,4)

    dataIRVar[:,:,e,:] = data

#----------Close it----------#

rootgrp.close()