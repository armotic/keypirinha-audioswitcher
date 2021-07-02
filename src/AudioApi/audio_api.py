from .AudioEndpointControl import AudioEndpoints
from .AudioEndpointControl.MMConstants import (Render, Capture)
from comtypes import GUID


class AudioApi:
    app_uuid = GUID('{302d46f8-b9fa-4235-a6d2-912bdfb1db6e}')

    def default_input_device(self):
        return AudioEndpoints(EventContext=self.app_uuid, dataFlow=Capture).GetDefault().getName()

    def default_output_device(self):
        return AudioEndpoints(EventContext=self.app_uuid, dataFlow=Render).GetDefault().getName()

    def select_input_device(self, name):
        endpoints = [d for d in AudioEndpoints(EventContext=self.app_uuid, dataFlow=Capture) if d.getName() == name]
        if len(endpoints) > 0:
            AudioEndpoints(EventContext=self.app_uuid, dataFlow=Capture).SetDefault(endpoints[0])

    def select_output_device(self, name):
        endpoints = [d for d in AudioEndpoints(EventContext=self.app_uuid, dataFlow=Render) if d.getName() == name]
        if len(endpoints) > 0:
            AudioEndpoints(EventContext=self.app_uuid, dataFlow=Render).SetDefault(endpoints[0])

    def list_input_devices(self, exclude_default=False):
        return [endpoint.getName() for endpoint in AudioEndpoints(EventContext=self.app_uuid, dataFlow=Capture)
                if not exclude_default or not endpoint.isDefault(dataFlow=Capture)]

    def list_output_devices(self, exclude_default=False):
        return [endpoint.getName() for endpoint in AudioEndpoints(EventContext=self.app_uuid, dataFlow=Render)
                if not exclude_default or not endpoint.isDefault(dataFlow=Render)]
