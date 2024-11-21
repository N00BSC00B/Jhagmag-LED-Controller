# Jhagmag LED Controller

**Jhagmag** is an Arduino-based LED controller that uses an HC-05 Bluetooth module and push-button support to control various LED patterns and effects. The project includes a Python GUI built with PyQt6, enabling users to control LED patterns, colors, and settings via serial connection or by using a push button to swap patterns. The hardware is assembled on a dot matrix board and housed in a custom box for portability and durability.

## Table of Contents

- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Project Structure](#project-structure)
- [Pictures](#Pictures)
- [Videos](#videos)
- [Arduino Schematic](#arduino-schematic)
- [Contributors](#contributors)
- [License](#license)

## Features

- Control LED patterns and colors via Bluetooth using an HC-05 module or through a push button for offline pattern swapping.
- Multiple LED patterns including:
  - Solid
  - Fade
  - Cycle
  - Rainbow Cycle
  - Breathing
  - Random
- Real-time audio visualization with LED response.
- Screen color detection and LED response.
- GUI application built with PyQt6 and Tkinter for easy control.
- Settings window to configure serial connection parameters.
- Push-button support for pattern swapping without Bluetooth connection.
- Enclosure built using a dot matrix board and custom box design.

## Hardware Requirements

- **Arduino board** (e.g., Arduino Uno)
- **HC-05 Bluetooth module**
- **RGB LED strip**
- **Push button** for pattern swapping
- **Resistors**:
  - 3 x 200Ω resistors (for current limiting)
  - 3 x 10kΩ resistors (for MOSFET gate pull-down)
- **MOSFETs**:
  - 3 x IRFZ44N (to control LED strip channels)
- **Indicator LED**:
  - Blue LED for power/on indication
- **Dot Matrix Board**: For sturdy and permanent circuit assembly
- **Custom Box Enclosure**: For housing the board and components

## Software Requirements

- Python 3.6+
- [PyQt6](https://pypi.org/project/PyQt6/)
- [PyAudio](https://pypi.org/project/PyAudio/)
- [Librosa](https://librosa.org/)
- [Matplotlib](https://matplotlib.org/)
- [scikit-learn](https://scikit-learn.org/)
- [Pillow](https://pillow.readthedocs.io/)
- [PySerial](https://pypi.org/project/pyserial/)

## Project Structure

```
jhagmag-led-controller/
├── Jhagmag/
│   ├── Jhagmag.ino                   # Arduino sketch for LED control
├── modules/
│   ├── serial_connection.py          # Serial connection handling
│   ├── audio_visualizer.py           # Audio visualization logic
│   ├── screen_responsive.py          # Screen color detection logic
├── main.py                           # Main PyQt6 GUI application
├── style.qss                         # Stylesheet for the PyQt6 application
└── README.md                         # Project documentation
```

### Key Files

- **[Jhagmag.ino](Jhagmag/Jhagmag.ino)**: Arduino sketch for controlling LED patterns, handling Bluetooth communication, and managing push-button input.
- **[main.py](main.py)**: Main PyQt6 GUI application.
- **[audio_visualizer.py](modules/audio_visualizer.py)**: Audio visualization logic.
- **[screen_responsive.py](modules/screen_responsive.py)**: Screen color detection logic.
- **[serial_connection.py](modules/serial_connection.py)**: Serial connection handling.
- **[style.qss](style.qss)**: Stylesheet for the PyQt6 application.

## Pictures

<details>
  <summary>Click to expand screenshots</summary>
  <div style="display: flex; flex-wrap: wrap;">
    <img src="assets/images/Solid.png" alt="Solid Screen" width="240" style="margin: 5px;">
    <img src="assets/images/Color Picker.png" alt="Color Picker" width="240" style="margin: 5px;">
    <img src="assets/images/Patterns.png" alt="Patterns Screen" width="240" style="margin: 5px;">
    <img src="assets/images/Audio Reactive.png" alt="Audio Reactive Screen" width="240" style="margin: 5px;">
    <img src="assets/images/Screen Reactive.png" alt="Screen Reactive Screen" width="240" style="margin: 5px;">
    <img src="assets/images/Development.jpg" alt="Development Kit" width="240" style="margin: 5px;">
    <img src="assets/images/Connection.jpg" alt="Final Kit" width="240" style="margin: 5px;">
  </div>
</details>

## Videos

<a href="https://streamable.com/wcu6o5">
  <img src="assets/images/Thumbnail.png" alt="Video Thumbnail" width="500">
</a>

## Arduino Schematic

The schematic should include:

- **HC-05 Bluetooth module** connections to the Arduino for wireless control.
- **Push button** wiring for pattern swapping when Bluetooth is not in use.
- **RGB LED strip** wiring through three IRFZ44N MOSFETs for color control:
  - Connect each RGB channel to a separate IRFZ44N MOSFET.
  - Use 200Ω resistors for current limiting and 10kΩ resistors as pull-downs for the MOSFET gates.
- **Blue LED** as an indicator light to signal power/on status.

You can download the full schematic in Fritzing format [here](assets/schematics/jhagmag.fzz).

<img src="assets/images/Schematic.png" alt="Video Thumbnail" width="500">

## Contributors

- [Sayan Barma](https://github.com/N00BSC00B)
- [Anirban Saha](https://github.com/TheFastest599)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
