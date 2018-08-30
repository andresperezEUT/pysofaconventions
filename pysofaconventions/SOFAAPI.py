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
#   @file   SOFAAPI.py
#   @author Andrés Pérez-López
#   @date   29/08/2018
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from .SOFAVersion import SOFAVersion

class SOFAAPI:

    APIName = 'pysofaconventions'
    copyrightString = "Copyright (c) 2018 Eurecat / UPF\n All rights reserved"

    @classmethod
    def getAPIName(cls):
        """
        Get the name of this API
        :return:    API name string
        """
        return cls.APIName

    @classmethod
    def getAPIVersion(cls):
        """
        Get the version of this API in the format major.minor.release
        :return:    Version string
        """
        versionString = str(SOFAVersion.SOFAVersionMajor) \
                        + "." + str(SOFAVersion.SOFAVersionMinor) \
                        + "." + str(SOFAVersion.SOFAVersionRelease)

        return versionString

    @classmethod
    def getAPIVersionMajor(cls):
        """
        Get the major version of this API
        :return:    Major version integer
        """
        return SOFAVersion.SOFAVersionMajor

    @classmethod
    def getAPIVersionMinor(cls):
        """
        Get the minor version of this API
        :return:    Minor version integer
        """
        return SOFAVersion.SOFAVersionMinor

    @classmethod
    def getAPIVersionRelease(cls):
        """
         Get the release version of this API
         :return:    Release version integer
         """
        return SOFAVersion.SOFAVersionRelease

    @classmethod
    def getAPICopyright(cls):
        """
        Get the copyright disclaimer for this API
        :return:    Copyright string
        """
        return cls.copyrightString

    @classmethod
    def getSpecificationsVersion(cls):
        """
        Get the SOFA specifications version in the format major.minor
        :return:    Version string
        """
        versionString = str(SOFAVersion.SOFASpecificationsMajor) \
                        + "." + str(SOFAVersion.SOFASpecificationsMinor)

        return versionString

    @classmethod
    def getSpecificationsVersionMajor(cls):
        """
        Get the major version of SOFA specification
        :return:    Major version integer
        """
        return SOFAVersion.SOFASpecificationsMajor

    @classmethod
    def getSpecificationsVersionMinor(cls):
        """
        Get the minor version of the SOFA specification
        :return:    Minor version integer
        """
        return SOFAVersion.SOFASpecificationsMinor