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
#   @file   test_SOFAUnits.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pytest
from pysofaconventions import *


def test_getType():

    # Type not found
    with pytest.raises(SOFAError) as e:
        SOFAUnits.getType("FakeType")
    assert e.match('Unit name not known')
    # Type found
    assert  SOFAUnits.getType("Meter") == SOFAUnits.UnitTypes.Meter
    assert  SOFAUnits.getType("degrees Kelvin") == SOFAUnits.UnitTypes.Kelvin


def test_isValid():

    # Not Valid
    assert not SOFAUnits.isValid("FakeType")

    # Valid
    assert SOFAUnits.isValid("cubic meters")
    assert SOFAUnits.isValid("degree degree meter")


def test_isDistanceUnit():

    # Not instance
    assert not SOFAUnits.isDistanceUnit("kelvin")
    # Instance
    assert SOFAUnits.isDistanceUnit("meter")
    assert SOFAUnits.isDistanceUnit("metre")

    #@ SOFAError: unit string not known
    with pytest.raises(SOFAError) as e:
        SOFAUnits.isDistanceUnit("fakeUnitString")
    assert e.match('Unit name not known')


def test_isFrequencyUnit():

    # Not instance
    assert not SOFAUnits.isFrequencyUnit("kelvin")
    # Instance
    assert SOFAUnits.isFrequencyUnit("hertz")
    assert SOFAUnits.isFrequencyUnit("Hertz")

    #@ SOFAError: unit string not known
    with pytest.raises(SOFAError) as e:
        SOFAUnits.isFrequencyUnit("fakeUnitString")
    assert e.match('Unit name not known')


def test_isTimeUnit():

    # Not instance
    assert not SOFAUnits.isTimeUnit("kelvin")
    # Instance
    assert SOFAUnits.isTimeUnit("samples")
    assert SOFAUnits.isTimeUnit("Samples")

    #@ SOFAError: unit string not known
    with pytest.raises(SOFAError) as e:
        SOFAUnits.isTimeUnit("fakeUnitString")
    assert e.match('Unit name not known')