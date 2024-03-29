from ableton.v2.control_surface import ControlSurface
from ableton.v2.base import listens
import math

def calculate_value(ms):
    a = 0.5
    b = 250
    parameter = (math.log(ms/a))/(math.log(b/a))
    return parameter

class SyncReverbMode(ControlSurface):
    def __init__(self, *a, **k):
        super(SyncReverbMode, self).__init__(*a, **k)
        self._song = self.song
        self._on_tempo_changed.subject = self._song
        self._on_tracks_changed.subject = self._song
        self._on_return_tracks_changed.subject = self._song
        self._all_mode = False  
        self._initial_reverbs = self.get_reverbs()
        self.update_reverb_pre_delay()
        for track in self._song.tracks:
            self._on_devices_changed.subject = track
            track.add_devices_listener(self._on_devices_changed)
        for track in self._song.return_tracks:
            self._on_devices_changed.subject = track
            track.add_devices_listener(self._on_devices_changed)
        self._on_devices_changed()
        
    @listens('tracks')
    def _on_tracks_changed(self):
        for track in self._song.tracks:
            self._on_devices_changed.subject = track
            for device in track.devices:
                if device.class_name == 'Reverb':
                    self.schedule_message(0, self.update_reverb_pre_delay, device)
        self._on_devices_changed()

    @listens('return_tracks')
    def _on_return_tracks_changed(self):
        for track in self._song.return_tracks:
            self._on_devices_changed.subject = track
            if not track.devices_has_listener(self._on_devices_changed):
                track.add_devices_listener(self._on_devices_changed)
            for device in track.devices:
                if device.class_name == 'Reverb':
                    self.schedule_message(0, self.update_reverb_pre_delay, device)
        self._on_devices_changed()
        
    def get_reverbs(self):
        tracks_and_returns = list(self._song.tracks) + list(self._song.return_tracks)
        return [device for track in tracks_and_returns for device in track.devices if device.class_name == 'Reverb']

    def switch_mode(self):
        self._all_mode = not self._all_mode

    @listens('tempo')
    def _on_tempo_changed(self):
        self.schedule_message(0, self.update_reverb_pre_delay)
    
    @listens('devices')
    def _on_devices_changed(self):
        tracks_and_returns = list(self._song.tracks) + list(self._song.return_tracks)
        for track in tracks_and_returns:
            for device in track.devices:
                if device.class_name == 'Reverb':
                    self.schedule_message(0, self.update_reverb_pre_delay, device)

    def update_reverb_pre_delay(self, reverb=None):
        reverbs = [reverb] if reverb else self.get_reverbs()
        for reverb in reverbs:
            if self._all_mode or reverb not in self._initial_reverbs:
                pre_delay_parameter = next((p for p in reverb.parameters if p.name == 'Predelay'), None)
                if pre_delay_parameter is not None:
                    new_pre_delay = 60000 / (self._song.tempo) * 4 / 32
                    while new_pre_delay < 0.5:
                        new_pre_delay *= 2
                    while new_pre_delay > 250:
                        new_pre_delay /= 2
                    normalized_pre_delay = calculate_value(new_pre_delay)
                    pre_delay_parameter.value = normalized_pre_delay

    def disconnect(self):
        self._on_tempo_changed.subject = None
        super(SyncReverbMode, self).disconnect()
