# Jhagmag LED Controller

_Jhagmag_ is an Arduino-based LED controller designed for vibrant, customizable lighting effects. Utilizing an HC-05 Bluetooth module and optional push-button functionality, it offers control over a variety of LED patterns and effects. A Python GUI, developed with PyQt6, provides an intuitive interface for adjusting patterns, colors, and settings. For enhanced portability and durability, the hardware is assembled on a dot matrix board and enclosed in a custom housing.

## Table of Contents

-   [Features](#features)
-   [Hardware Requirements](#hardware-requirements)
-   [Software Requirements](#software-requirements)
-   [Project Structure](#project-structure)
-   [Pictures](#pictures)
-   [Videos](#videos)
-   [Arduino Schematic](#arduino-schematic)
-   [Contributors](#contributors)
-   [Acknowledgments](#acknowledgments)
-   [License](#license)

---

## Features

-   _Control Mechanisms_:
    -   _Bluetooth Control_: Adjust patterns and settings via an HC-05 Bluetooth module.
    -   _Push Button_: Offline pattern swapping without Bluetooth connectivity.
-   _LED Patterns_:
    -   Solid
    -   Fade
    -   Cycle
    -   Rainbow Cycle
    -   Breathing
    -   Random
-   _Advanced Features_:
    -   Real-time _audio visualization_ with LEDs responding dynamically to sound.
    -   _Screen color detection_: Sync LEDs with the predominant screen color.
-   _Graphical Interface_:
    -   Built with _PyQt6_ for cross-platform compatibility and intuitive controls.
    -   Integrated _settings window_ for serial connection configuration.
-   _Compact Design_:
    -   Circuit assembled on a _dot matrix board_ for reliability.
    -   Enclosed in a _custom housing_ for a polished, portable setup.

---

## Hardware Requirements

-   _Core Components_:
    -   Arduino board (e.g., Arduino Uno)
    -   HC-05 Bluetooth module
    -   RGB LED strip
    -   Push button (for pattern swapping)
-   _Electronics_:
    -   Resistors:
        -   3 x 200Ω (current limiting for LED channels)
        -   3 x 10kΩ (MOSFET gate pull-downs)
    -   3 x IRFZ44N MOSFETs (to control RGB LED channels)
    -   Blue LED (power/on indicator)
-   _Assembly_:
    -   Dot matrix board for permanent wiring.
    -   Custom box enclosure for protection and portability.

---

## Software Requirements

Ensure the following dependencies are installed before running the software:

-   Python 3.6+
-   [PyQt6](https://pypi.org/project/PyQt6/) (GUI development)
-   [PyAudio](https://pypi.org/project/PyAudio/) (audio processing)
-   [Librosa](https://librosa.org/) (audio analysis)
-   [Matplotlib](https://matplotlib.org/) (visualization)
-   [scikit-learn](https://scikit-learn.org/) (machine learning utilities)
-   [Pillow](https://pillow.readthedocs.io/) (image processing)
-   [PySerial](https://pypi.org/project/pyserial/) (serial communication)

---

## Project Structure

jhagmag-led-controller/
├── Jhagmag/
│ ├── Jhagmag.ino # Arduino sketch for LED control
├── modules/
│ ├── **init**.py
│ ├── serial_connection.py # Serial connection handling
│ ├── audio_visualizer.py # Audio visualization logic
│ ├── screen_responsive.py # Screen color detection logic
├── main.py # Main PyQt6 GUI application
├── style.qss # Stylesheet for the PyQt6 application
└── README.md # Project documentation

---

## Pictures

<div style="display: flex; flex-wrap: wrap;">
  <img src="assets/images/Solid.png" alt="Solid Pattern" width="240" style="margin: 5px;">
  <img src="assets/images/Color Picker.png" alt="Color Picker" width="240" style="margin: 5px;">
  <img src="assets/images/Patterns.png" alt="Patterns Screen" width="240" style="margin: 5px;">
  <img src="assets/images/Audio Reactive.png" alt="Audio Reactive" width="240" style="margin: 5px;">
  <img src="assets/images/Screen Reactive.png" alt="Screen Reactive" width="240" style="margin: 5px;">
  <img src="assets/images/Development.jpg" alt="Development Kit" width="240" style="margin: 5px;">
  <img src="assets/images/Connection.jpg" alt="Final Kit" width="240" style="margin: 5px;">
</div>

---

## Videos

<a href="https://youtu.be/UNQXKmhpDMk" target="_blank">
  <img src="assets/images/Thumbnail.png" alt="Video Thumbnail" width="500">
</a>

> _Note_: Right-click and select "Open link in new tab" for better viewing.

---

## Arduino Schematic

The schematic details the connections between the HC-05 Bluetooth module, push button, RGB LED strip, and MOSFETs. Resistors ensure proper operation and safety, while the blue LED serves as an indicator.

-   _Fritzing File_: Download the complete schematic in Fritzing format [here](assets/schematics/jhagmag.fzz).

<img src="assets/images/Schematic.png" alt="Arduino Schematic" width="500">

---

Here's the updated _Contributors_ section with specific roles for hardware and software parts:

---

## Contributors

Thanks to these wonderful contributors for their efforts in making this project a success:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/N00BSC00B">
        <img src="https://avatars.githubusercontent.com/N00BSC00B" width="100px;" alt=""/>
        <br />
        <sub><b>Sayan Barma</b></sub>
      </a>
      <br />
      <b>Software Development</b><br />
      (Software and GUI Development)
    </td>
    <td align="center">
      <a href="https://github.com/TheFastest599">
        <img src="https://avatars.githubusercontent.com/TheFastest599" width="100px;" alt=""/>
        <br />
        <sub><b>Anirban Saha</b></sub>
      </a>
      <br />
      <b>Hardware Design</b><br />
      (Hardware Design and Assembly)
    </td>
  </tr>
</table>

---

## Acknowledgments

Special thanks to open-source communities and contributors for tools and libraries like PyQt6, Librosa, and Fritzing.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
