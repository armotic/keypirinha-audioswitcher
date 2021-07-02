# -*- coding: utf-8 -*-
"""Defines the main classes AudioEndpoints, AudioEndpoint"""

from __future__ import print_function, unicode_literals, absolute_import

from . import mmdeviceapiPath
from _ctypes import COMError
from comtypes import CoCreateInstance, CLSCTX_INPROC_SERVER, CLSCTX_ALL, GUID

from .MMConstants import (Render, Console, DEVICE_STATE_ACTIVE,
                          Device_FriendlyName, STGM_READ)

try:
    # Try to import local .MMDeviceAPILib for Python 2.6 compatibility
    from .MMDeviceAPILib import (MMDeviceEnumerator as _MMDeviceEnumerator,
                                 IMMDeviceEnumerator as _IMMDeviceEnumerator,
                                 IMMNotificationClient)
except ImportError:
    # Use comtypes to generate MMDeviceAPILib (Python 2.7+))
    from comtypes.client import GetModule

    GetModule(mmdeviceapiPath)
    from comtypes.gen.MMDeviceAPILib import (
        MMDeviceEnumerator as _MMDeviceEnumerator,
        IMMDeviceEnumerator as _IMMDeviceEnumerator,
        IMMNotificationClient)
from .PolicyConfigAPI import CLSID_CPolicyConfigVistaClient, IPolicyConfigVista

_CLSID_MMDeviceEnumerator = _MMDeviceEnumerator._reg_clsid_


def _GetValue(value):
    # Need to do this in a function as comtypes seems to
    # have a problem if it's in a class.

    # Types for vt defined here:
    # https://msdn.microsoft.com/en-us/library/windows/desktop/aa380072%28v=vs.85%29.aspx
    if value.vt == 0:
        return None
    elif value.vt == 31:
        return value.__MIDL____MIDL_itf_mmdeviceapi_0003_00850001.pwszVal
    return value.__MIDL____MIDL_itf_mmdeviceapi_0003_00850001.cVal

class AudioEndpoint(object):
    """Wrapper for a single COM endpoint."""

    def __init__(self, endpoint, endpoints, PKEY_Device=Device_FriendlyName,
                 EventContext=None):
        """Initializes an endpoint object."""
        self._endpoint = endpoint
        self.endpoints = endpoints
        self.PKEY_Device = PKEY_Device
        self.EventContext = EventContext

    def getName(self):
        """Return an endpoint devices FriendlyName."""
        pStore = self._endpoint.OpenPropertyStore(STGM_READ)
        return _GetValue(pStore.GetValue(self.PKEY_Device))

    def getId(self):
        """Gets a string that identifies the device."""
        return self._endpoint.GetId()

    def getState(self):
        """Gets the current state of the device."""
        return self._endpoint.GetState()

    def isDefault(self, role=Console, dataFlow=Render):
        """Return if endpoint device is default or not."""
        return self == self.endpoints.GetDefault(role, dataFlow)

    def __eq__(self, other):
        """Tests if two endpoint devices are the same."""
        return self.getId() == other.getId()

    def __ne__(self, other):
        """Tests if two endpoint devices are not the same."""
        return self.getId() != other.getId()

    __unicode__ = getName

    def __str__(self):
        return str(self.getName())


class AudioEndpoints(object):
    """The main class to access all endpoints in the system"""

    def __init__(self, DEVICE_STATE=DEVICE_STATE_ACTIVE,
                 PKEY_Device=Device_FriendlyName,
                 dataFlow=Render,
                 EventContext=GUID.create_new()):
        self.DEVICE_STATE = DEVICE_STATE
        self.default_flow = dataFlow
        self.PKEY_Device = PKEY_Device
        self.EventContext = EventContext
        self._DevEnum = CoCreateInstance(_CLSID_MMDeviceEnumerator,
                                         _IMMDeviceEnumerator,
                                         CLSCTX_INPROC_SERVER)
        self._callback = None
        self._PolicyConfig = None

    # TODO: Missing class docstring (missing-docstring)
    def GetDefault(self, role=Console, dataFlow=None):
        return AudioEndpoint(self._DevEnum.GetDefaultAudioEndpoint(
            dataFlow or self.default_flow, role),
            self, self.PKEY_Device, self.EventContext)

    # TODO: Missing class docstring (missing-docstring)
    def SetDefault(self, endpoint, role=Console):
        OldDefault = self.GetDefault(role)

        if self._PolicyConfig is None:
            self._PolicyConfig = CoCreateInstance(
                CLSID_CPolicyConfigVistaClient, IPolicyConfigVista, CLSCTX_ALL)

        hr = self._PolicyConfig.SetDefaultEndpoint(endpoint.getId(), role)
        if hr:
            print('Could not SetDefaultEndpoint:', hr)
        return OldDefault

    def __call__(self, ID):
        try:
            return AudioEndpoint(self._DevEnum.GetDevice(ID), self,
                                 self.PKEY_Device, self.EventContext)
        except COMError:
            for endpoint in self:
                if endpoint.getName() == ID:
                    return endpoint
            raise

    def __str__(self):
        return str([str(endpoint) for endpoint in self])

    # TODO: Missing class docstring (missing-docstring)
    def ChangeFilter(self, DEVICE_STATE=None, PKEY_Device=None):
        if DEVICE_STATE is not None:
            self.DEVICE_STATE = DEVICE_STATE
        if PKEY_Device is not None:
            self.PKEY_Device = PKEY_Device

    def __iter__(self, dataFlow=None):
        pEndpoints = self._DevEnum.EnumAudioEndpoints(dataFlow or self.default_flow,
                                                      self.DEVICE_STATE)
        for i in range(pEndpoints.GetCount()):
            yield AudioEndpoint(pEndpoints.Item(i), self, self.PKEY_Device,
                                self.EventContext)

    # pylint: disable=invalid-length-returned
    def __len__(self):
        return int(self._DevEnum.EnumAudioEndpoints(
            Render, self.DEVICE_STATE).GetCount())
