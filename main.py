import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget, QSlider, QLabel, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, QTimer
from openai_processor import OpenAIProcessor
from transcription import Transcriber
from audio_processing import AudioProcessor
from settings_dialog import SettingsDialog

logging.basicConfig(level=logging.DEBUG)

class MainWindow(QMainWindow):
    error_signal = pyqtSignal(str)
    transcription_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TaskAI")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.start_button = QPushButton("Start Listening", self)
        self.layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Listening", self)
        self.layout.addWidget(self.stop_button)

        self.is_silent_mode = False

        self.transcriber = Transcriber(self)
        self.processor = OpenAIProcessor(self)

        self.start_button.clicked.connect(self.toggle_listening)
        self.stop_button.clicked.connect(self.stop_listening)

        self.error_signal.connect(self.display_error)
        self.transcription_signal.connect(self.display_transcription)

        self.listening = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_recording_time)

        self.init_ui()
        logging.info("MainWindow initialized successfully")

    def init_ui(self):
        self.settings_button = QPushButton("Settings", self)
        self.layout.addWidget(self.settings_button)
        self.settings_button.clicked.connect(self.open_settings)

    def toggle_listening(self):
        if self.listening:
            self.stop_listening()
        else:
            self.start_listening()

    def start_listening(self):
        self.listening = True
        self.transcriber.start_recording()
        self.timer.start(3000)  # Process audio every 3 seconds
        logging.info("Starting to listen")
    
    def stop_listening(self):
        self.listening = False
        self.transcriber.stop_recording()
        self.timer.stop()
        logging.info("Stopping listening")

    def update_recording_time(self):
        transcription = self.transcriber.transcribe_audio("Low-quality")
        self.transcription_signal.emit(transcription)

    def display_error(self, error_message):
        self.text_edit.append(f"Error: {error_message}")

    def display_transcription(self, transcription):
        self.text_edit.append(f"Transcription: {transcription}")

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
