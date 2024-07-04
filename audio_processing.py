import sounddevice as sd
import numpy as np

class AudioProcessor:
    def __init__(self, parent):
        self.parent = parent
        self.samplerate = 16000
        self.duration = 5
        self.recording = False

    def start_recording(self):
        self.recording = True
        self.audio_data = np.zeros((self.duration * self.samplerate, 1))
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.samplerate)
        self.stream.start()

    def stop_recording(self):
        self.recording = False
        self.stream.stop()

    def audio_callback(self, indata, frames, time, status):
        if self.recording:
            self.audio_data = np.append(self.audio_data, indata)
