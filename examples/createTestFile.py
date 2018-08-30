# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#   createTestFile.py
#
#   Reference implementation for SOFA file creation with sofaconventions
#
#   (C) Andrés Pérez-López - Eurecat / UPF
#   24/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from sofaconventions import *
from netCDF4 import Dataset
import time
import numpy as np

#----------Create it----------#

filePath = "/Volumes/Dinge/SOFA/testpysofa.sofa"
rootgrp = Dataset(filePath, 'w', format='NETCDF4')


#----------Required Attributes----------#

rootgrp.Conventions = 'SOFA'
rootgrp.Version = '1.0'
rootgrp.SOFAConventions = 'AmbisonicsDRIR'
rootgrp.SOFAConventionsVersion = '0.1'
rootgrp.APIName = 'sofaconventions'
rootgrp.APIVersion = '0.1'
rootgrp.APIVersion = '0.1'
rootgrp.AuthorContact = 'andres.perez@eurecat.org'
rootgrp.Organization = 'Eurecat - UPF'
rootgrp.License = 'WTFPL - Do What the Fuck You Want to Public License'
rootgrp.DataType = 'FIRE'
rootgrp.RoomType = 'reverberant'
rootgrp.DateCreated = time.ctime(time.time())
rootgrp.DateModified = time.ctime(time.time())
rootgrp.Title = 'testpysofa'
rootgrp.AmbisonicsOrder = '1'


#----------Required Dimensions----------#

m = 3
n = 48000
r = 4
e = 1
i = 1
c = 3
rootgrp.createDimension('M', m)
rootgrp.createDimension('N', n)
rootgrp.createDimension('R', r)
rootgrp.createDimension('E', e)
rootgrp.createDimension('I', i)
rootgrp.createDimension('C', c)


#----------Required Variables----------#
listenerPositionVar = rootgrp.createVariable('ListenerPosition',    'f8',   ('I','C'))
listenerPositionVar.Units   = 'metre'
listenerPositionVar.Type    = 'cartesian'
listenerPositionVar[:] = np.zeros(c)

listenerUpVar       = rootgrp.createVariable('ListenerUp',          'f8',   ('I','C'))
listenerUpVar.Units         = 'metre'
listenerUpVar.Type          = 'cartesian'
listenerUpVar[:]    = np.zeros(c)

listenerViewVar     = rootgrp.createVariable('ListenerView',        'f8',   ('I','C'))
listenerViewVar.Units       = 'metre'
listenerViewVar.Type        = 'cartesian'
listenerViewVar[:]  = np.zeros(c)

emitterPositionVar  = rootgrp.createVariable('EmitterPosition',     'f8',   ('E','C','I'))
emitterPositionVar.Units   = 'metre'
emitterPositionVar.Type    = 'cartesian'
emitterPositionVar[:] = np.asarray([1,0,0])

emitterUpVar        = rootgrp.createVariable('EmitterUp',           'f8',   ('E','C','I'))
emitterUpVar.Units         = 'metre'
emitterUpVar.Type          = 'cartesian'
emitterUpVar[:]     = np.zeros(c)

emitterViewVar      = rootgrp.createVariable('EmitterView',         'f8',   ('E','C','I'))
emitterViewVar.Units       = 'metre'
emitterViewVar.Type        = 'cartesian'
emitterViewVar[:]   = np.zeros(c)

sourcePositionVar = rootgrp.createVariable('SourcePosition',    'f8',   ('I','C'))
sourcePositionVar.Units   = 'metre'
sourcePositionVar.Type    = 'cartesian'
sourcePositionVar[:]      = np.zeros(c)

receiverPositionVar = rootgrp.createVariable('ReceiverPosition',  'f8',   ('R','C','I'))
receiverPositionVar.Units   = 'metre'
receiverPositionVar.Type    = 'cartesian'
receiverPositionVar[:]      = np.zeros((r,c))

samplingRateVar =   rootgrp.createVariable('Data.SamplingRate', 'f8',   ('I'))
samplingRateVar.Units = 'hertz'
samplingRateVar[:] = 48000

delayVar        =   rootgrp.createVariable('Data.Delay',        'f8',   ('I','R','E'))
delay = np.zeros(r)
delayVar[:,:,:] = delay

dataIRVar =         rootgrp.createVariable('Data.IR', 'f8', ('M','R','E','N'))
dataIRVar.ChannelOrdering   = 'acn'
dataIRVar.Normalization     = 'sn3d'
dataIRVar[:] = np.random.rand(m,r,e,n)

#----------Close it----------#

rootgrp.close()