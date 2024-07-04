from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSlider, QCheckBox

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")

        layout = QVBoxLayout()

        self.api_key_label = QLabel("OpenAI API Key:")
        layout.addWidget(self.api_key_label)
        self.api_key_input = QLineEdit(self)
        layout.addWidget(self.api_key_input)

        self.response_interval_label = QLabel("Response Interval (seconds):")
        layout.addWidget(self.response_interval_label)
        self.response_interval_slider = QSlider(self)
        layout.addWidget(self.response_interval_slider)

        self.silent_mode_checkbox = QCheckBox("Silent Mode", self)
        layout.addWidget(self.silent_mode_checkbox)

        self.save_button = QPushButton("Save", self)
        layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.save_settings)

        self.setLayout(layout)

    def save_settings(self):
        api_key = self.api_key_input.text()
        response_interval = self.response_interval_slider.value()
        silent_mode = self.silent_mode_checkbox.isChecked()

        # Save these settings as needed
        # For example, use QSettings to save to a file or update the parent directly
        self.parent().processor.api_key = api_key
        self.parent().response_interval = response_interval
        self.parent().is_silent_mode = silent_mode

        self.accept()
