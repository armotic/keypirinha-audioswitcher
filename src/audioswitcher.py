# Keypirinha launcher (keypirinha.com)
import re

import keypirinha as kp

from .AudioApi.audio_api import AudioApi


class AudioSwitcher(kp.Plugin):
    """Audio Switcher Plugin that lets you select your default audio input/output device."""
    api = AudioApi()
    always_suggest = False

    def __init__(self):
        super().__init__()

    def on_start(self):
        self._read_config()

    def on_catalog(self):
        self.set_catalog([
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label="Switch Output Audio",
                short_desc="Change the output audio device",
                target="output_audio",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.NOARGS),
            self.create_item(
                category=kp.ItemCategory.KEYWORD,
                label="Switch Input Audio",
                short_desc="Change the input audio device",
                target="input_audio",
                args_hint=kp.ItemArgsHint.REQUIRED,
                hit_hint=kp.ItemHitHint.NOARGS)])

    def on_suggest(self, user_input, items_chain):
        if items_chain and len(items_chain) > 0:
            target = items_chain[0].target()
        elif self.always_suggest:
            target = 'all'
        else:
            return

        suggestions = []
        if target == 'all' or target == 'output_audio':
            for device in self.api.list_output_devices(exclude_default=True):
                if re.search(user_input, device, re.IGNORECASE):
                    suggestions.append(self.create_item(
                        category=kp.ItemCategory.REFERENCE,
                        label=device,
                        short_desc="Switch to this output audio device",
                        target='output_audio:' + device,
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.IGNORE))
        if target == 'all' or target == 'input_audio':
            for device in self.api.list_input_devices(exclude_default=True):
                if re.search(user_input, device, re.IGNORECASE):
                    suggestions.append(self.create_item(
                        category=kp.ItemCategory.REFERENCE,
                        label=device,
                        short_desc="Switch to this input audio device",
                        target='input_audio:' + device,
                        args_hint=kp.ItemArgsHint.FORBIDDEN,
                        hit_hint=kp.ItemHitHint.IGNORE))
        self.set_suggestions(suggestions, kp.Match.ANY, kp.Sort.NONE)

    def on_execute(self, item, action):
        if item.target().startswith('output_audio:'):
            self.api.select_output_device(item.label())
        else:
            self.api.select_input_device(item.label())

    def on_events(self, flags):
        if flags & kp.Events.PACKCONFIG:
            self._read_config()
            self.on_catalog()

    def _read_config(self):
        settings = self.load_settings()
        self.always_suggest = settings.get_bool("always_suggest", "main", False)
