import random
from unittest import TestCase
from AudioApi.audio_api import AudioApi


class TestAudioApi(TestCase):
    def setUp(self):
        self.api = AudioApi()


class TestRetrieveAudioDevices(TestAudioApi):
    def test_current_input_audio_device(self):
        device = self.api.default_input_device()
        print("Current Input:", device)
        self.assertRegex(device, ".+")

    def test_current_output_audio_device(self):
        device = self.api.default_output_device()
        print("Current Output:", device)
        self.assertRegex(device, ".+")

    def test_list_input_audio_devices(self):
        devices = self.api.list_input_devices()
        print("All Inputs:", devices)
        self.assertGreater(len(devices), 0)

    def test_list_output_audio_devices(self):
        devices = self.api.list_output_devices()
        print("All Outputs:", devices)
        self.assertGreater(len(devices), 0)


class TestSetAudioDevice(TestAudioApi):
    def test_select_input_audio_device(self):
        default_device = self.api.default_input_device()
        print("Current Input:", default_device)
        new_device = random.choice([dev for dev in self.api.list_input_devices() if dev != default_device])
        self.api.select_input_device(new_device)
        new_device = self.api.default_input_device()
        print("New Input:", new_device)
        self.assertNotEqual(default_device, new_device)
        self.api.select_input_device(default_device)

    def test_select_output_audio_device(self):
        default_device = self.api.default_output_device()
        print("Current Output:", default_device)
        new_device = random.choice([dev for dev in self.api.list_output_devices() if dev != default_device])
        self.api.select_output_device(new_device)
        new_device = self.api.default_output_device()
        print("New Output:", new_device)
        self.assertNotEqual(default_device, new_device)
        self.api.select_output_device(default_device)
