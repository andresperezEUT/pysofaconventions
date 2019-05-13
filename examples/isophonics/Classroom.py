# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   AudioBooth.py
#
#   Implementation of conversion from the isophonics dataset
#
#   (C) Andrés Pérez-López - Eurecat / UPF
#   02/10/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pysofaconventions import *
from netCDF4 import Dataset
import time
import numpy as np
import soundfile as sf

#----------Create it----------#

filePath = "/Volumes/Dinge/SOFA/isophonics/Classroom.sofa"
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
rootgrp.Title = 'Classroom'
rootgrp.AmbisonicsOrder = '1'


#----------Required Dimensions----------#

X = 13
Y = 10

M = X*Y
N = 96000*2
R = 4
E = 1
I = 1
C = 3
rootgrp.createDimension('M', M)
rootgrp.createDimension('N', N)
rootgrp.createDimension('R', R)
rootgrp.createDimension('E', E)
rootgrp.createDimension('I', I)
rootgrp.createDimension('C', C)


#----------Required Variables----------#

dataIRVar = rootgrp.createVariable('Data.IR', 'f8', ('M','R','E','N'))
dataIRVar.ChannelOrdering   = 'fuma'
dataIRVar.Normalization     = 'fuma'

audioFolderPath = '/Volumes/Dinge/isophonics/Classroom/'



# Listener: compute positions and open files at the same time...
listenerPositionVar = rootgrp.createVariable('ListenerPosition',    'f8',   ('M','C'))
listenerPositionVar.Units   = 'metre'
listenerPositionVar.Type    = 'cartesian'

d = 0.5 # Distance between listener positions
x_offset = 3
y_offset = 2

# X and Y here are in the diagram coordinate system
for x in range(X):
    x_pos =  (d*x) - x_offset
    x_str = '0' + str(int(x * d * 10)) if x < 2 else str(int(x * d * 10))

    for y in range(Y):
        y_pos = (d*y) + y_offset
        y_str = '0' + str(int(y*d*10)) if y < 2 else str(int(y*d*10))

        m = x*Y + y
        filename = x_str + 'x' + y_str + 'y' + '.wav'

        # print (x_pos,y_pos)
        # print (filename)
        # print('---')

        # Here coordinate system is shifted 90 degree
        # sofa x = diagram y; sofa y = diagram -x
        x_pos_sofa = y_pos
        y_pos_sofa = -x_pos
        z_pos_sofa = 0
        listenerPositionVar[m,:] = np.asarray([x_pos_sofa,y_pos_sofa,z_pos_sofa])

        print('m',m)
        print ('Emitter position: ' + str([x_pos_sofa,y_pos_sofa,z_pos_sofa]))
        print ('Filename: ' + filename )
        print('---')

        # Open audio files and get the stuff
        for ch_idx, ch in enumerate(['W','X','Y','Z']):

            data, samplerate = sf.read(audioFolderPath + ch +'/' + ch + filename)
            assert samplerate == 96000
            assert np.shape(data) == (96000*2,)

            dataIRVar[m, ch_idx, :, :] = data

dataIRVar.ChannelOrdering = 'fuma'
dataIRVar.Normalization = 'fuma'


# ListenerUp in the +Z axis
listenerUpVar       = rootgrp.createVariable('ListenerUp',          'f8',   ('I','C'))
listenerUpVar.Units         = 'metre'
listenerUpVar.Type          = 'cartesian'
listenerUpVar[:]    = np.asarray([0,0,1])

# Listener looking to the front (+X axis)
listenerViewVar     = rootgrp.createVariable('ListenerView',        'f8',   ('I','C'))
listenerViewVar.Units       = 'metre'
listenerViewVar.Type        = 'cartesian'
listenerViewVar[:]  = np.asarray([1,0,0])


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


# Emitter: same as source
emitterPositionVar  = rootgrp.createVariable('EmitterPosition',     'f8',   ('E','C','I'))
emitterPositionVar.Units   = 'metre'
emitterPositionVar.Type    = 'cartesian'
emitterPositionVar[:]      = np.zeros((E,C))

# Receiver
receiverPositionVar = rootgrp.createVariable('ReceiverPosition',  'f8',   ('R','C','I'))
receiverPositionVar.Units   = 'metre'
receiverPositionVar.Type    = 'cartesian'
receiverPositionVar[:]      = np.zeros((R,C))

# From specs
samplingRateVar =   rootgrp.createVariable('Data.SamplingRate', 'f8',   ('I'))
samplingRateVar.Units = 'hertz'
samplingRateVar[:] = 96000

# No delay found
delayVar        =   rootgrp.createVariable('Data.Delay',        'f8',   ('I','R','E'))
delay = np.zeros((I,R,E))
delayVar[:,:,:] = delay



#----------Close it----------#

rootgrp.close()