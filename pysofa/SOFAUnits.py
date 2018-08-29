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
#   @file   SOFAUnits.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .SOFAError import SOFAError
import inspect

class SOFAUnits(object):

    class UnitTypes:
        Meter           = 0
        CubicMeter      = 1
        Hertz           = 2
        Samples         = 3
        SphericalUnits  = 4
        Kelvin          = 5

    @classmethod
    def getTypeMap(cls):

        return {
            'metres'                    : cls.UnitTypes.Meter,
            'meters'                    : cls.UnitTypes.Meter,
            'metre'                     : cls.UnitTypes.Meter,
            'meter'                     : cls.UnitTypes.Meter,

            'cubic meter'               : cls.UnitTypes.CubicMeter,
            'cubic meters'              : cls.UnitTypes.CubicMeter,
            'cubic metre'               : cls.UnitTypes.CubicMeter,
            'cubic metres'              : cls.UnitTypes.CubicMeter,

            'hertz'                     : cls.UnitTypes.Hertz,
            'samples'                   : cls.UnitTypes.Samples,

            'degree, degree, meter'     : cls.UnitTypes.SphericalUnits,
            'degree, degree, metre'     : cls.UnitTypes.SphericalUnits,
            'degree, degree, metres'    : cls.UnitTypes.SphericalUnits,
            'degree, degree, meters'    : cls.UnitTypes.SphericalUnits,
            'degrees, degrees, meter'   : cls.UnitTypes.SphericalUnits,
            'degrees, degrees, metre'   : cls.UnitTypes.SphericalUnits,
            'degrees, degrees, metres'  : cls.UnitTypes.SphericalUnits,
            'degrees, degrees, meters'  : cls.UnitTypes.SphericalUnits,

            'degree,degree,meter'       : cls.UnitTypes.SphericalUnits,
            'degree,degree,metre'       : cls.UnitTypes.SphericalUnits,
            'degree,degree,metres'      : cls.UnitTypes.SphericalUnits,
            'degree,degree,meters'      : cls.UnitTypes.SphericalUnits,
            'degrees,degrees,meter'     : cls.UnitTypes.SphericalUnits,
            'degrees,degrees,metre'     : cls.UnitTypes.SphericalUnits,
            'degrees,degrees,metres'    : cls.UnitTypes.SphericalUnits,
            'degrees,degrees,meters'    : cls.UnitTypes.SphericalUnits,

            'degree degree meter'       : cls.UnitTypes.SphericalUnits,
            'degree degree metre'       : cls.UnitTypes.SphericalUnits,
            'degree degree metres'      : cls.UnitTypes.SphericalUnits,
            'degree degree meters'      : cls.UnitTypes.SphericalUnits,
            'degrees degrees meter'     : cls.UnitTypes.SphericalUnits,
            'degrees degrees metre'     : cls.UnitTypes.SphericalUnits,
            'degrees degrees metres'    : cls.UnitTypes.SphericalUnits,
            'degrees degrees meters'    : cls.UnitTypes.SphericalUnits,

            'kelvin'                    : cls.UnitTypes.Kelvin,
            'Kelvin'                    : cls.UnitTypes.Kelvin,
            'degree Kelvin'             : cls.UnitTypes.Kelvin,
            'degrees Kelvin'            : cls.UnitTypes.Kelvin,
            'degree kelvin'             : cls.UnitTypes.Kelvin,
            'degrees kelvin'            : cls.UnitTypes.Kelvin,
        }

    @classmethod
    def getType(cls,name):
        """
        Get the UnitType of a given type string

        :param name:    the name of the unit being queried
        :return:        an instance of UniType
        :raises:        SOFAError if the name does not correspond with a valid Unit Type
        """
        typeMap = cls.getTypeMap()
        try:
            return typeMap[name.lower()]
        except KeyError:
            raise SOFAError(str('Unit name not known: ' + name))


    @classmethod
    def isValid(cls,name):
        """
        Answer if a given name string corresponds with a valid Unit Type

        :param name:    the name of the unit being queried
        :return:        a Boolean
        """

        typeMap = cls.getTypeMap()

        if name.lower() in typeMap:
            return True
        else:
            return False


    @classmethod
    def isDistanceUnit(cls,unitName):
        """
        Check if a given unit type is of Distance kind

        :param unitName:    a unit name string
        :return:            a Boolean
        :raise:             SOFAError, if the name string does not correspond with a unit type
        """
        try:
            if cls.getType(unitName) == cls.UnitTypes.Meter:
                return True
            else:
                return False
        except SOFAError as e:
            raise e

    @classmethod
    def isFrequencyUnit(cls, unitName):
        """
        Check if a given unit type is of Frequency kind

        :param unitName:    a unit name string
        :return:            a Boolean
        :raise:             SOFAError, if the name string does not correspond with a unit type
        """
        try:
            if cls.getType(unitName) == cls.UnitTypes.Hertz:
                return True
            else:
                return False
        except SOFAError as e:
            raise e

    @classmethod
    def isTimeUnit(cls, unitName):
        """
        Check if a given unit type is of Time kind

        :param unitName:    a unit name string
        :return:           a Boolean
        :raise:             SOFAError, if the name string does not correspond with a unit type
        """
        try:
            if cls.getType(unitName) == cls.UnitTypes.Samples:
                return True
            else:
                return False
        except SOFAError as e:
            raise e