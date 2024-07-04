import logging
import sounddevice as sd
import numpy as np
import openai

class Transcriber:
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

    def transcribe_audio(self, quality):
        try:
            if quality == "High-quality":
                logging.info("Transcribing audio using method: High-quality")
                response = openai.Audio.transcribe("whisper-1", self.audio_data)
            else:
                logging.info("Transcribing audio using method: Low-quality")
                response = openai.Audio.transcribe("whisper-1", self.audio_data)

            transcription = response['text']
            logging.info(f"Transcription result: {transcription}")
            return transcription
        except Exception as e:
            error_message = f"Error during transcription: {str(e)}"
            logging.error(error_message)
            self.parent.error_signal.emit(error_message)
            return ""
