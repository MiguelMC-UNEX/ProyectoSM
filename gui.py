import librosa
import numpy as np
import soundfile as sf
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QComboBox
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Analyzer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.load_button = QPushButton("Load Audio File")
        self.load_button.clicked.connect(self.load_audio)
        layout.addWidget(self.load_button)

        self.label_info = QLabel("Audio Information Will Appear Here")
        layout.addWidget(self.label_info)

        self.conversion_type = QComboBox()
        self.conversion_type.addItem("Convert to Mono")
        self.conversion_type.addItem("Convert to Stereo")
        layout.addWidget(self.conversion_type)

        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_audio)
        layout.addWidget(self.convert_button)

        self.save_button = QPushButton("Save Audio File")
        self.save_button.clicked.connect(self.save_audio)
        layout.addWidget(self.save_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.audio_path = None
        self.audio_data = None
        self.sr = None
        self.num_channels = None
        self.num_samples = None

    def load_audio(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.mp3)")
        if path:
            self.audio_path = path
            self.audio_data, self.sr = librosa.load(path, sr=None, mono=False)
            if self.audio_data.ndim == 1:
                self.audio_data = self.audio_data[np.newaxis, :]
            self.num_channels = self.audio_data.shape[0]
            self.num_samples = self.audio_data.shape[1]
            self.label_info.setText(f"Loaded {path}\nSample Rate: {self.sr} Hz\nDuration: {self.num_samples / self.sr:.2f} seconds\nChannels: {self.num_channels}\nSamples: {self.num_samples}")
            self.update_plot()

    def convert_audio(self):
        if self.audio_data is not None:
            selection = self.conversion_type.currentText()
            if selection == "Convert to Mono" and self.num_channels > 1:
                self.audio_data = np.mean(self.audio_data, axis=0, keepdims=True)
                self.num_channels = 1
            elif selection == "Convert to Stereo" and self.num_channels == 1:
                self.audio_data = np.tile(self.audio_data, (2, 1))
                self.num_channels = 2
            self.label_info.setText(f"Conversion Applied: {selection}\nSample Rate: {self.sr} Hz\nDuration: {self.num_samples / self.sr:.2f} seconds\nChannels: {self.num_channels}\nSamples: {self.num_samples}")
            self.update_plot()

    def save_audio(self):
        if self.audio_data is not None:
            path, _ = QFileDialog.getSaveFileName(self, "Save Audio File", "", "Audio Files (*.wav *.flac)")
            if path:
                sf.write(path, self.audio_data.T, self.sr)
                self.label_info.setText(f"File saved as: {path}")

    def update_plot(self):
        fig = make_subplots(rows=2, cols=1, subplot_titles=("Time Domain", "Frequency Domain"))

        # Time domain plot
        if self.num_channels > 1:
            for i in range(self.num_channels):
                fig.add_trace(go.Scatter(y=self.audio_data[i], mode='lines', name=f'Channel {i+1}'), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(y=self.audio_data.squeeze(), mode='lines', name='Mono'), row=1, col=1)

        # Frequency domain plot
        N = len(self.audio_data[0])
        T = 1.0 / self.sr
        yf = np.fft.rfft(self.audio_data[0])
        xf = np.fft.rfftfreq(N, T)

        fig.add_trace(go.Scatter(x=xf, y=np.abs(yf), mode='lines', name='Spectrum'), row=2, col=1)

        fig.update_layout(height=800, width=700)
        pyo.plot(fig, filename='audio_waveform.html', auto_open=True)
