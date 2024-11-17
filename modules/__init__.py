# modules/__init__.py
"""
This module initializes the components of the Jhagmag LED Controller.
Modules:
    SerialConnection: Manages the serial connection for the LED controller.
    AudioVisualizer: Handles the audio visualization for the LED controller.
    ScreenResponsive: Manages the screen responsiveness for the LED controller.
__all__:
    A list of public objects of this module, as interpreted by `import *`.
"""

from .serial_connection import SerialConnection
from .audio_visualizer import AudioVisualizer
from .screen_responsive import ScreenResponsive

__all__ = ["SerialConnection", "AudioVisualizer", "ScreenResponsive"]
