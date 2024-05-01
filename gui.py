import os
import librosa
import numpy as np
import soundfile as sf
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QComboBox, QDialog
from PyQt5.QtCore import QFile, QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import scipy.signal
import mplcursors


class PlotWindow(QDialog):
    def __init__(self, audio_data, sr):
        super().__init__()

        self.setWindowTitle("Audio Waveform")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create Matplotlib figure and canvas
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.audio_data = audio_data
        self.sr = sr

        # Plot waveform and spectrum
        self.plot_waveform()
        self.plot_spectrum()

        self.resize(800, 600)

    def plot_waveform(self):
        ax_waveform = self.figure.add_subplot(211)
        t = np.arange(len(self.audio_data[0])) / self.sr
        for i in range(self.audio_data.shape[0]):
            ax_waveform.plot(t, self.audio_data[i], label=f"Channel {i+1}")
        ax_waveform.set_xlabel('Time (s)')
        ax_waveform.set_ylabel('Amplitude')
        ax_waveform.set_title('Waveform')
        ax_waveform.legend(loc='upper right')  # Specify legend location
        # Add cursor tooltip
        mplcursors.cursor(ax_waveform, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{sel.target[0]}, {sel.target[1]}"))

    def plot_spectrum(self):
        ax_spectrum = self.figure.add_subplot(212)
        N = len(self.audio_data[0])
        for i in range(self.audio_data.shape[0]):
            yf = np.fft.rfft(np.array(self.audio_data[i]))  # Convert audio_data to numpy array
            xf = np.fft.rfftfreq(N, 1 / self.sr)
            ax_spectrum.plot(xf, np.abs(yf), label=f"Channel {i+1}")
        ax_spectrum.set_xlabel('Frequency (Hz)')
        ax_spectrum.set_ylabel('Magnitude')
        ax_spectrum.set_title('Spectrum')
        ax_spectrum.legend(loc='upper right')  # Specify legend location
        # Add cursor tooltip
        mplcursors.cursor(ax_spectrum, hover=True).connect("add", lambda sel: sel.annotation.set_text(f"{sel.target[0]}, {sel.target[1]}"))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Analyzer")
        self.setGeometry(100, 100, 1000, 800)

        layout = QVBoxLayout()

        self.load_button = QPushButton("Load Audio File")
        self.load_button.clicked.connect(self.load_audio)
        layout.addWidget(self.load_button)

        self.label_info = QLabel("Audio Information Will Appear Here")
        layout.addWidget(self.label_info)

        self.action_type = QComboBox()
        self.action_type.addItem("Convert to Mono")
        self.action_type.addItem("Convert to Stereo")
        self.action_type.addItem("Apply Low-pass Filter")
        self.action_type.addItem("Apply High-pass Filter")
        self.action_type.addItem("Apply Audio Compression")
        layout.addWidget(self.action_type)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_action)
        layout.addWidget(self.apply_button)

        self.save_button = QPushButton("Save Audio File")
        self.save_button.clicked.connect(self.save_audio)
        layout.addWidget(self.save_button)

        self.plot_window = None

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
            self.show_plot_window()

    def apply_action(self):
        if self.audio_data is not None:
            selection = self.action_type.currentText()
            if selection == "Convert to Mono" and self.num_channels > 1:
                self.audio_data = np.mean(self.audio_data, axis=0, keepdims=True)
                self.num_channels = 1
            elif selection == "Convert to Stereo" and self.num_channels == 1:
                self.audio_data = np.tile(self.audio_data, (2, 1))
                self.num_channels = 2
            elif selection == "Apply Low-pass Filter":
                cutoff_freq = 1000
                self.audio_data = self.low_pass_filter(self.audio_data, self.sr, cutoff_freq)
            elif selection == "Apply High-pass Filter":
                cutoff_freq = 1000
                self.audio_data = self.high_pass_filter(self.audio_data, self.sr, cutoff_freq)
            elif selection == "Apply Audio Compression":
                self.apply_compression()

            self.label_info.setText(f"Action Applied: {selection}")
            self.show_plot_window()

            
    def save_audio(self):
        if self.audio_data is not None:
            path, _ = QFileDialog.getSaveFileName(self, "Save Audio File", "", "Audio Files (*.wav *.flac)")
            if path:
                # Asegurar que self.sr es un entero
                samplerate_int = int(self.sr)
                # Transponer self.audio_data antes de guardar
                sf.write(path, self.audio_data.T, samplerate_int)
                self.label_info.setText(f"File saved as: {path}")

    def show_plot_window(self):
        if self.audio_data is not None:
            self.plot_window = PlotWindow(self.audio_data, self.sr)
            self.plot_window.exec_()

    def low_pass_filter(self, audio_data, sr, cutoff):
        nyquist = sr / 2
        normal_cutoff = cutoff / nyquist
        b, a = scipy.signal.butter(5, normal_cutoff, btype='low', analog=False)
        filtered_data = scipy.signal.lfilter(b, a, audio_data)
        return filtered_data

    def high_pass_filter(self, audio_data, sr, cutoff):
        nyquist = sr / 2
        normal_cutoff = cutoff / nyquist
        b, a = scipy.signal.butter(5, normal_cutoff, btype='high', analog=False)
        filtered_data = scipy.signal.lfilter(b, a, audio_data)
        return filtered_data
    

    def apply_compression(self):
        if self.audio_data is not None:
            downsampling_factor = 2  # Define el factor de downsampling

            # Aplicar downsampling tomando cada 'downsampling_factor'-ésima muestra
            self.audio_data = self.audio_data[:, ::downsampling_factor]
            self.sr /= downsampling_factor  # Ajustar la tasa de muestreo a la nueva tasa
            self.num_samples = self.audio_data.shape[1]  # Actualizar el número de muestras
            
            # Actualizar la información en la interfaz de usuario
            self.label_info.setText(f"Audio Compression Applied\nNew Sample Rate: {self.sr} Hz\nNew Duration: {self.num_samples / self.sr:.2f} seconds")

