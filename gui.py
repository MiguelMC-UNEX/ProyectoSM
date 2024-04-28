import librosa
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel
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

            # Verificar el número de canales después de cargar el audio
            self.num_channels = self.audio_data.shape[0] if len(self.audio_data.shape) > 1 else 1

            # Verificar el número de muestras del audio
            self.num_samples = self.audio_data.shape[1] if len(self.audio_data.shape) > 1 else self.audio_data.shape[0]

            # Imprimir información adicional para depuración
            print(f"Loaded {path}")
            print(f"Sample Rate: {self.sr} Hz")
            print(f"Duration: {self.num_samples / self.sr:.2f} seconds")
            print(f"Number of Channels: {self.num_channels}")
            print(f"Number of Samples: {self.num_samples}")

            self.label_info.setText(f"Loaded {path}\nSample Rate: {self.sr} Hz\nDuration: {self.num_samples / self.sr:.2f} seconds\nChannels: {self.num_channels}\nSamples: {self.num_samples}")

            # Visualización interactiva
            fig = make_subplots(rows=1, cols=1)
            if self.num_channels > 1:
                for i in range(self.num_channels):
                    fig.add_trace(go.Scatter(y=self.audio_data[i], mode='lines'), row=1, col=1)
            else:
                fig.add_trace(go.Scatter(y=self.audio_data, mode='lines'), row=1, col=1)
            fig.update_layout(height=400, width=700, title_text="Audio Waveform")
            pyo.plot(fig, filename='audio_waveform.html')
