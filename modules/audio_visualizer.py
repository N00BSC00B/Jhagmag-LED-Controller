import numpy as np
import pyaudio
import librosa
import matplotlib.animation as animation
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class AudioVisualizer:

    """
    A class to visualize audio data in real-time and control LED colors based
    on audio frequencies.
    Attributes:
        serial_conn (Serial): The serial connection to send RGB values.
        running (bool): Indicates if the visualizer is running.
        CHUNK (int): The number of audio frames per buffer.
        RATE (int): The sampling rate of the audio stream.
        CHANNELS (int): The number of audio channels.
        FORMAT (int): The format of the audio stream.
        audio (pyaudio.PyAudio): The PyAudio instance.
        stream (pyaudio.Stream): The audio input stream.
        fig (matplotlib.figure.Figure): The Matplotlib figure for plotting.
        ax (matplotlib.axes.Axes): The axes of the Matplotlib figure.
        bars (matplotlib.container.BarContainer): The bar container for the
            frequency bands.
        current_bass (float): The current bass level.
        current_mid (float): The current mid level.
        current_treble (float): The current treble level.
        max_bass (float): The maximum observed bass level.
        max_mid (float): The maximum observed mid level.
        max_treble (float): The maximum observed treble level.
        FADE_THRESHOLD (float): The threshold for fading the LED colors.
        NOISE_GATE_THRESHOLD (float): The threshold for ignoring noise.
        DECAY_TIME (float): The time for the audio levels to decay.
    Methods:
        `get_canvas()`:
            Returns the canvas widget for embedding in a GUI.
        `get_frequency_indices(freq_range, n_fft, rate)`:
            Returns the indices of the frequencies within the specified range.
        `nextpow2(n)`:
            Returns the next power of 2 greater than or equal to n.
        `update(frame)`:
            Updates the audio visualization and sends RGB values via serial.
        `audio_to_rgb(bass_level, mid_level, treble_level)`:
            Converts audio levels to RGB values.
        `start()`:
            Starts the audio visualizer.
        `stop()`:
            Stops the audio visualizer.
        `is_running()`:
            Returns whether the visualizer is running.
    """

    def __init__(self, master, serial_conn, chunk=1024, rate=44100, type='tk'):

        """
        Initializes the AudioVisualizer class.

        Parameters:
            master (Tk or QWidget): Parent widget for embedding the matplotlib
                figure.
            serial_conn (serial.Serial): Serial connection object.
            chunk (int, optional): Frames per buffer. Default is 1024.
            rate (int, optional): Sampling rate. Default is 44100.
            type (str, optional): GUI framework type
                ('tk' for Tkinter, 'qt' for PyQt). Default is 'tk'.

        Attributes:
            serial_conn (serial.Serial): Serial connection object.
            running (bool): Visualizer running status.
            CHUNK (int): Frames per buffer.
            RATE (int): Sampling rate.
            CHANNELS (int): Number of audio channels.
            FORMAT (int): Audio stream format.
            audio (pyaudio.PyAudio): PyAudio instance.
            stream (pyaudio.Stream): Audio input stream.
            fig (matplotlib.figure.Figure): Matplotlib figure.
            ax (matplotlib.axes._subplots.AxesSubplot): Matplotlib axes.
            bars (matplotlib.container.BarContainer): Bar container for audio
                levels.
            current_bass (float): Current bass level.
            current_mid (float): Current mid level.
            current_treble (float): Current treble level.
            max_bass (float): Maximum bass level.
            max_mid (float): Maximum mid level.
            max_treble (float): Maximum treble level.
            FADE_THRESHOLD (float): Threshold for fading effect.
            NOISE_GATE_THRESHOLD (float): Threshold for noise gate.
            DECAY_TIME (float): Decay time for audio levels.
            canvas (FigureCanvasTkAgg or FigureCanvasQTAgg): Canvas for
                embedding the matplotlib figure.
            ani (matplotlib.animation.FuncAnimation): Animation object for
                updating the plot.
        """

        # Serial connection
        self.serial_conn = serial_conn
        self.running = False

        # PyAudio parameters
        self.CHUNK = chunk
        self.RATE = rate
        self.CHANNELS = 1
        self.FORMAT = pyaudio.paFloat32

        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        # Matplotlib figure for embedding in GUI
        self.fig, self.ax = plt.subplots(figsize=(480/100, 280/100), dpi=100)
        self.fig.patch.set_facecolor('#2c2f33')  # Figure background color
        self.ax.set_facecolor('#2c2f33')  # Axis background color
        self.fig.patch.set_linewidth(2)

        self.ax.spines['right'].set_color('#2c2f33')  # Right border (spine)
        self.ax.spines['bottom'].set_color('#2c2f33')  # Bottom border (spine)
        self.ax.spines['left'].set_color('#2c2f33')  # Left border (spine)
        self.ax.spines['top'].set_color('#2c2f33')  # Top border (spine)

        # Set axis labels color to white
        self.ax.tick_params(axis='both', colors='#ffffff')  # Axis ticks color
        self.ax.xaxis.label.set_color('#ffffff')  # X axis label color
        self.ax.yaxis.label.set_color('#ffffff')  # Y axis label color

        # Set title color to white
        self.ax.set_title('Audio Reactive Plot', color='#ffffff')
        self.bars = self.ax.barh(
            ['Bass', 'Mid', 'Treble'],
            [0, 0, 0],
            color=['#ff4c4c', '#4caf50', '#42aaff'],
            edgecolor='none',
            height=0.5,
            linewidth=0,
            capsize=20
        )
        self.ax.set_xlim(0, 1)

        # Other variables
        self.current_bass = 0
        self.current_mid = 0
        self.current_treble = 0
        self.max_bass = 1
        self.max_mid = 1
        self.max_treble = 1
        self.FADE_THRESHOLD = 0.05
        self.NOISE_GATE_THRESHOLD = 0.02
        self.DECAY_TIME = 1

        if type == 'tk':
            self.canvas = FigureCanvasTkAgg(self.fig, master)
            self.canvas.get_tk_widget().pack()
        else:
            self.canvas = FigureCanvasQTAgg(self.fig)
            master.addWidget(self.canvas)

        # Animation setup
        self.ani = animation.FuncAnimation(
            self.fig, self.update, interval=50, cache_frame_data=False
        )

    def get_canvas(self):

        """
        Retrieve the current canvas.

        Returns:
            object: The current canvas object.
        """

        return self.canvas

    def get_frequency_indices(self, freq_range, n_fft, rate):

        """
        Get the indices of the frequency bins that fall within a specified
        frequency range.

        Parameters:
        freq_range (tuple): A tuple containing the lower and upper bounds of
            the frequency range (in Hz).
        n_fft (int): The number of FFT points.
        rate (float): The sampling rate of the audio signal (in Hz).

        Returns:
        numpy.ndarray: An array of indices corresponding to the frequency bins
            within the specified range.
        """
        freqs = np.fft.rfftfreq(n_fft, 1.0 / rate)
        return np.where((freqs >= freq_range[0]) & (freqs <= freq_range[1]))[0]

    def nextpow2(self, n):

        """
        Calculate the next power of 2 greater than or equal to the given
        number.

        Parameters:
        n (int): The input number.

        Returns:
        int: The next power of 2 greater than or equal to n.
        """

        return 2 ** int(np.ceil(np.log2(n)))

    def update(self, frame):

        """
        Update the audio visualizer with the latest audio frame.
        This method processes the audio data from the stream, computes the
        Short-Time Fourier Transform (STFT), and updates the visualizer's
        levels for bass, mid, and treble frequencies. It also applies a noise
        gate, decay, normalization, and dynamic range compression before
        sending the RGB values via serial communication and updating the
        visual representation.
        Parameters:
            frame (int): The current frame number (not used in the method but
                required by the animation function).
        Returns:
            None
        """

        data = np.frombuffer(
            self.stream.read(self.CHUNK, exception_on_overflow=False),
            dtype=np.float32
        )

        # Compute the STFT for the chunk, setting n_fft equal to CHUNK
        stft = np.abs(librosa.stft(
            data,
            n_fft=self.nextpow2(self.CHUNK),
            hop_length=self.CHUNK,
            center=False
        ))

        bass_idx = self.get_frequency_indices(
            [20, 250], self.CHUNK, self.RATE
        )
        mid_idx = self.get_frequency_indices(
            [250, 4000], self.CHUNK, self.RATE
        )
        treble_idx = self.get_frequency_indices(
            [4000, 20000], self.CHUNK, self.RATE
        )

        # Compute average amplitude for each frequency band
        bass_level = np.mean(stft[bass_idx])
        mid_level = np.mean(stft[mid_idx])
        treble_level = np.mean(stft[treble_idx])

        # Calculate the decay rate per frame based on the desired decay time
        decay_rate = 1 - (1 / (self.RATE * self.DECAY_TIME))

        # Update the levels only if they exceed the noise gate threshold
        if bass_level > self.NOISE_GATE_THRESHOLD:
            self.current_bass = bass_level
            self.max_bass = max(self.max_bass, bass_level)
        else:
            self.current_bass = max(self.current_bass - decay_rate, 0)

        if mid_level > self.NOISE_GATE_THRESHOLD:
            self.current_mid = mid_level
            self.max_mid = max(self.max_mid, mid_level)
        else:
            self.current_mid = max(self.current_mid - decay_rate, 0)

        if treble_level > self.NOISE_GATE_THRESHOLD:
            self.current_treble = treble_level
            self.max_treble = max(self.max_treble, treble_level)
        else:
            self.current_treble = max(self.current_treble - decay_rate, 0)

        # Normalize the levels relative to their maximum observed values
        normalized_bass = self.current_bass / self.max_bass
        normalized_mid = self.current_mid / self.max_mid
        normalized_treble = self.current_treble / self.max_treble

        # Apply dynamic range compression for mid and treble
        compressed_mid = min(normalized_mid * 1.2, 1.0)
        compressed_treble = min(normalized_treble * 1.5, 1.0)

        # Send RGB values via serial only if above the threshold
        if (
            normalized_bass > self.FADE_THRESHOLD or
            compressed_mid > self.FADE_THRESHOLD or
            compressed_treble > self.FADE_THRESHOLD
        ):
            red, green, blue = self.audio_to_rgb(
                normalized_bass, compressed_mid, compressed_treble
            )
            self.serial_conn.send_color(red, green, blue)

        # Update bar widths in the plot instead of heights
        self.bars[0].set_width(normalized_bass)
        self.bars[1].set_width(normalized_mid)
        self.bars[2].set_width(normalized_treble)
        self.canvas.draw()

    def audio_to_rgb(self, bass_level, mid_level, treble_level):

        """
        Converts audio levels to RGB values.
        This function takes in bass, mid, and treble audio levels and converts
        them to corresponding RGB values. The conversion is done by mapping
        the audio levels to the RGB color space.
        Args:
            bass_level (float): The bass level of the audio, expected to be
                between 0 and 1.
            mid_level (float): The mid level of the audio, expected to be
                between 0 and 1.
            treble_level (float): The treble level of the audio, expected to
                be between 0 and 1.
        Returns:
            tuple: A tuple containing the RGB values (red, green, blue)
                as integers ranging from 0 to 255.
        """

        def amplitude_to_rgb(level, multiplier=1, min_rgb=25):
            if level <= 0.05:
                return 0
            rgb_value = int(min_rgb + ((255 - min_rgb) * level * multiplier))
            return max(0, min(255, rgb_value))

        red = amplitude_to_rgb(bass_level, 1.2)
        green = amplitude_to_rgb(mid_level)
        blue = amplitude_to_rgb(treble_level)

        return red, green, blue

    def start(self):

        """
        Starts the audio visualizer.

        This method sets the running flag to True, resumes the animation,
        and starts the audio stream if it is not already active.
        """

        self.running = True
        # Resume the animation
        self.ani.event_source.start()
        if not self.stream.is_active():
            self.stream.start_stream()

    def stop(self):

        """
        Stops the audio visualizer.

        This method sets the running flag to False, pauses the animation,
        and stops the audio stream if it is active.
        """

        self.running = False
        # Pause the animation and the stream
        self.ani.event_source.stop()
        if self.stream.is_active():
            self.stream.stop_stream()

    def is_running(self):

        """
        Check if the audio visualizer is currently running.

        Returns:
            bool: True if the visualizer is running, False otherwise.
        """

        return self.running


if __name__ == "__main__":
    import tkinter as tk
    from serial_connection import SerialConnection
    import time

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Audio Visualizer")
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())

    # Create a SerialConnection instance
    conn = SerialConnection(port='COM8', baudrate=9600)
    time.sleep(1)
    conn.send_timeout(True)

    # Create an AudioVisualizer instance
    visualizer = AudioVisualizer(root, conn)

    # Start the animation
    visualizer.start()

    # Run the Tkinter main loop
    root.mainloop()
