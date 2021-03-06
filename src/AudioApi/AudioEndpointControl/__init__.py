__all__ = (b"AudioEndpoints", b"Render", b"Capture", b"All",
           b"mmdeviceapiPath", b"DEVICE_STATE_ACTIVE",
           b"DEVICE_STATE_DISABLED", b"DEVICE_STATE_NOTPRESENT",
           b"DEVICE_STATE_UNPLUGGED", b"DEVICE_STATEMASK_ALL",
           b"Device_FriendlyName", b"Device_DeviceDesc",
           b"DeviceInterface_FriendlyName")
__version__ = '0.2a4'
__author__ = 'Joni Borén'

import os
from zipfile import ZipFile
kPackageSuffix = '.keypirinha-package'

try:
    import MMDeviceAPILib
except ImportError:
    mmdeviceapiPath = "mmdeviceapi.tlb"
    directory = os.path.dirname(os.path.abspath(__file__))
    if kPackageSuffix in directory:
        keypirinhaPackage = directory[:directory.index(kPackageSuffix) + len(kPackageSuffix)]
        packageDirectory = os.path.dirname(keypirinhaPackage)
        with ZipFile(keypirinhaPackage, 'r') as zipObj:
            for file in zipObj.infolist():
                if file.filename.endswith('/mmdeviceapi.tlb'):
                    file.filename = 'AudioSwitcher.mmdeviceapi.tlb'
                    zipObj.extract(file, packageDirectory)
        mmdeviceapiPath = os.path.normpath(os.path.join(directory, "../../../AudioSwitcher.mmdeviceapi.tlb"))

from .AudioEndpoints import AudioEndpoints
# DataFlow enumeration: The DataFlow enumeration defines constants that
# indicate the direction in which audio data flows between an audio endpoint
# device and an application.
from .MMConstants import Render, Capture, All
# Role enumeration: The Role enumeration defines constants that indicate the
# role that the system has assigned to an audio endpoint device.
from .MMConstants import Console, Multimedia, Communications
# DEVICE_STATE_XXX Constants: The DEVICE_STATE_XXX constants indicate the
# current state of an audio endpoint device.
from .MMConstants import (
    DEVICE_STATE_ACTIVE,
    DEVICE_STATE_DISABLED,
    DEVICE_STATE_NOTPRESENT,
    DEVICE_STATE_UNPLUGGED,
    DEVICE_STATEMASK_ALL
)
# Each PKEY_Xxx property identifier in the following list is a constant of type
# PROPERTYKEY that is defined in header file Functiondiscoverykeys_devpkey.h.
# All audio endpoint devices have these three device properties.
from .MMConstants import (
    Device_FriendlyName,
    Device_DeviceDesc,
    DeviceInterface_FriendlyName
)
