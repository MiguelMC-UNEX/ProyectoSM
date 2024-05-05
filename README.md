# Audio Analyzer

Audio Analyzer es una aplicación de escritorio basada en PyQt5 para analizar y procesar archivos de audio. La aplicación permite cargar archivos de audio, visualizar formas de onda y espectros, aplicar filtros y compresión, y guardar los archivos procesados.

## Características

- **Cargar archivos de audio**: Soporte para formatos WAV y MP3.
- **Visualización**: Muestra la forma de onda del audio y su espectro de frecuencia.
- **Procesamiento de audio**: Incluye la conversión a mono o estéreo, aplicación de filtros de paso bajo y paso alto, y compresión de audio.
- **Guardar archivos procesados**: Guarda el audio procesado en formatos WAV o FLAC.

## Requisitos
Para ejecutar Audio Analyzer, necesitamos importar el `enviroment.yml`.

Para ello, utiliza el siguiente comando en la terminal:

```bash
conda env create -f environment.yml  
```


## Uso


Para ejecutar la aplicación haga lo siguiente:


- **Haga git clone del repositorio**:
  ```bash 
  git clone https://github.com/MiguelMC-UNEX/ProyectoSM.git
  ```

- **Vaya al directorio clonado remotamente**:
 ```bash
 cd ProyectoSM
 ```

 - **Carge el entorno conda `audio_env`**:

 ```bash
 conda activate audio_env
 ```

 - **Ejecute la aplicación**:
 ```bash
 python main.py
 ```



# Explicación del Código de Audio Analyzer

Audio Analyzer es una aplicación desarrollada en Python utilizando PyQt5 para la interfaz gráfica, junto con librosa, numpy, soundfile, scipy y matplotlib para el procesamiento y visualización de audio. El proyecto se divide principalmente en dos clases: `MainWindow` y `PlotWindow`.

## MainWindow

### Descripción General
`MainWindow` es la ventana principal de la aplicación, encargada de la interacción con el usuario. Desde aquí, los usuarios pueden cargar archivos de audio, aplicar diferentes procesamientos y guardar el audio modificado.

### Componentes Clave
- **Botones para cargar y guardar archivos**: Utilizan `QFileDialog` para abrir y guardar archivos de audio.
```python
self.load_button.clicked.connect(self.load_audio)
self.save_button.clicked.connect(self.save_audio)
```

- **Visualización de información del audio**: Muestra detalles como la tasa de muestreo, duración y número de canales.
```python
self.label_info.setText(f"Loaded {path}\nSample Rate: {self.sr} Hz\nDuration: {self.num_samples / self.sr:.2f} seconds\nChannels: {self.num_channels}")
```

- **Selección de acciones**: Un `QComboBox` permite elegir entre convertir audio a mono o estéreo, aplicar filtros de paso bajo o paso alto, y aplicar compresión de audio.
```python
self.action_type.addItem("Convert to Mono")
self.action_type.addItem("Convert to Stereo")
```

- **Aplicación de efectos y procesamiento**: Al seleccionar una acción y pulsar el botón de aplicar, se procesa el audio cargado según la elección.

### Métodos Importantes
- `load_audio()`: Carga el archivo de audio seleccionado y actualiza la interfaz con la información del archivo.
- `apply_action()`: Aplica el efecto o procesamiento seleccionado al archivo de audio.
- `save_audio()`: Guarda el archivo procesado en el formato deseado.

## PlotWindow

### Descripción General
`PlotWindow` se utiliza para visualizar el audio en términos de su forma de onda y espectro de frecuencia.

### Componentes Clave
- **Canvas de Matplotlib**: Se utilizan `Figure` y `FigureCanvasQTAgg` para dibujar las gráficas de audio.
```python
self.figure = Figure()
self.canvas = FigureCanvas(self.figure)
layout.addWidget(self.canvas)
```

- **Visualización de forma de onda y espectro**: Muestra la forma de onda del audio y un espectro de frecuencia, permitiendo una inspección detallada del audio.
```python
ax_waveform.plot(t, self.audio_data[i], label=f"Channel {i+1}")
ax_spectrum.plot(xf, np.abs(yf), label=f"Channel {i+1}")
```


### Funciones de Visualización
- `plot_waveform()`: Dibuja la forma de onda del audio en el tiempo.
- `plot_spectrum()`: Calcula y muestra el espectro de frecuencia del audio.

## Consideraciones Adicionales

El código también incluye tratamiento de excepciones básico y ajustes de la interfaz gráfica para mejorar la experiencia del usuario. La aplicación es capaz de manejar diferentes formatos de audio y puede ser extendida con más funcionalidades como filtros adicionales o análisis más detallados.



