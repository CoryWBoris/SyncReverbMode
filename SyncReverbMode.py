from ableton.v2.control_surface import ControlSurface
from ableton.v2.base import listens
import math

def calculate_value(ms):
    # Constants a and b are determined based on the constraints of the parameter in question. Whatever your parameter's range is can be applied here to get the logarithmic parameter mapping function, if you want to apply this logic to other parameters

    # a = 0.5, b = 250
    a = 0.5
    b = 250

    # Calculate the parameter value based on the input milliseconds
    parameter = (math.log(ms/a))/(math.log(b/a))

    return parameter

class SyncReverbMode(ControlSurface):
    def __init__(self, *a, **k):
        super(SyncReverbMode, self).__init__(*a, **k)
        self._song = self.song  # Get a reference to the current song
        self._on_tempo_changed.subject = self._song
        # Start in 'all_mode = False' mode, this applies reverb sync to new instances of native reverb modules named 'Reverb' added only after your set loads, True applies this script to every native module named 'Reverb' no matter if they were loaded or not.
        self._all_mode = False  
        self._initial_reverbs = self.get_reverbs()  # Store the initial reverb modules
        self.update_reverb_pre_delay()
        for track in self._song.tracks:
            self._on_devices_changed.subject = track  # Listen for changes in devices

    def get_reverbs(self):
        return [device for track in self._song.tracks for device in track.devices if device.class_name == 'Reverb']

    def switch_mode(self):
        self._all_mode = not self._all_mode  # Switch the mode

    # Set up the BPM listener
    @listens('tempo')
    def _on_tempo_changed(self):
        self.schedule_message(0, self.update_reverb_pre_delay)
    
    @listens('devices')
    def _on_devices_changed(self):
        for device in self._song.view.selected_track.devices:
            if device.class_name == 'Reverb':
                self.schedule_message(0, self.update_reverb_pre_delay, device)

    def update_reverb_pre_delay(self, reverb=None):
        reverbs = [reverb] if reverb else self.get_reverbs()
        for reverb in reverbs:
            if self._all_mode or reverb not in self._initial_reverbs:
                pre_delay_parameter = next((p for p in reverb.parameters if p.name == 'Predelay'), None)
                if pre_delay_parameter is not None:
                    new_pre_delay = 60000 / (self._song.tempo) * 4 / 32
                    # Ensure the new pre-delay is within the range of 0.5 to 250 ms
                    while new_pre_delay < 0.5:
                        new_pre_delay *= 2
                    while new_pre_delay > 250:
                        new_pre_delay /= 2
                    # Map the new pre-delay time to the normalized range
                    normalized_pre_delay = calculate_value(new_pre_delay)
                    pre_delay_parameter.value = normalized_pre_delay

    def disconnect(self):
        self._on_tempo_changed.subject = None  # Remove the BPM listener
        super(SyncReverbMode, self).disconnect()
