import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QLabel,
    QFrame, QCheckBox, QSpinBox, QSlider, QColorDialog, QPushButton,
    QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QIcon, QAction

from modules import SerialConnection, AudioVisualizer, ScreenResponsive


class LEDControllerUI(QMainWindow):

    """
    A class to represent the main UI for the LED Controller application.
    Attributes
    ----------
    R : int
        Red color value (0-255).
    G : int
        Green color value (0-255).
    B : int
        Blue color value (0-255).
    pattern_buttons : list
        List of pattern buttons.
    selected_button : QPushButton or None
        Currently selected pattern button.
    music : bool
        Flag to indicate if music mode is enabled.
    FPS : int
        Frames per second for screen reactive mode.
    last_update_time : float
        Timestamp of the last update.
    conn : SerialConnection
        Serial connection to the LED controller.
    screen_responsive : ScreenResponsive
        Screen responsive handler.
    settings_window : SettingsWindow
        Settings window instance.
    Methods
    -------
    __init__():
        Initialize the main UI for the LED Controller.
    open_settings_window():
        Open the settings window.
    connect_conn():
        Connect to the serial connection.
    disconnect_conn():
        Disconnect from the serial connection.
    reconnect_conn():
        Reconnect to the serial connection.
    update_menu_actions():
        Update the state of menu actions based on connection status.
    on_tab_changed(index):
        Handle tab change events.
    unactiveTab():
        Deactivate the current tab.
    create_solid_tab():
        Create the Solid tab.
    create_pattern_tab():
        Create the Pattern tab.
    create_audio_reactive_tab():
        Create the Audio Reactive tab.
    create_screen_reactive_tab():
        Create the Screen Reactive tab.
    toggle_rgb_controls(state, value_box, slider, color):
        Enable or disable RGB controls based on checkbox state.
    value_box_control(sl, value, color):
        Sync the value box and slider values.
    slider_control(vb, value):
        Sync the slider and value box values.
    update_color(value, color):
        Update the color values and send to the connection.
    open_color_picker():
        Open the color picker dialog.
    select_pattern():
        Select a pattern from the pattern tab.
    open_screen_dimension_selector():
        Open the screen dimension selector.
    update_capturing_label(x1, y1, x2, y2):
        Update the capturing label with the selected dimensions.
    clear_capturing_label():
        Clear the capturing label.
    update_fps(value):
        Update the FPS value.
    start_screen_capture():
        Start the screen capture.
    stop_screen_capture():
        Stop the screen capture.
    """

    def __init__(self):

        """
        Initialize the main UI for the LED Controller.
        This method sets up the main window, initializes variables, and
        creates the main layout with tabs and an options menu.
        It also connects actions to their respective functions.
        Attributes:
            R (int): Red color value.
            G (int): Green color value.
            B (int): Blue color value.
            pattern_buttons (list): List of pattern buttons.
            selected_button (QPushButton): Currently selected button.
            music (bool): Flag to indicate if music mode is active.
            FPS (int): Frames per second for updates.
            last_update_time (float): Timestamp of the last update.
            conn (SerialConnection): Serial connection object.
            screen_responsive (ScreenResponsive): Screen responsive object.
            settings_window (SettingsWindow): Settings window object.
        """

        super().__init__()
        self.setWindowTitle("Jhagmag")
        self.setFixedSize(500, 400)
        self.setWindowIcon(QIcon("icon.ico"))

        # Variables
        self.R = 0
        self.G = 0
        self.B = 0
        self.pattern_buttons = []
        self.selected_button = None
        self.music = False
        self.FPS = 10
        self.last_update_time = time.time()
        self.conn = SerialConnection(port="COM11")
        self.screen_responsive = ScreenResponsive(self.conn)
        self.settings_window = SettingsWindow(self.conn)

        # Main layout
        main_layout = QVBoxLayout()

        # Title Label and Gear Icon
        # label = QLabel("Jhagmag")
        # main_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Tabs setup
        tabs = QTabWidget()
        tabs.addTab(self.create_solid_tab(), "Solid")
        tabs.addTab(self.create_pattern_tab(), "Pattern")
        tabs.addTab(self.create_audio_reactive_tab(), "Audio Reactive")
        tabs.addTab(self.create_screen_reactive_tab(), "Screen Reactive")
        tabs.currentChanged.connect(self.on_tab_changed)
        main_layout.addWidget(tabs)

        # Options menu
        options_menu = self.menuBar().addMenu("Options")
        self.connect_action = QAction("Connect", self)
        self.disconnect_action = QAction("Disconnect", self)
        self.reconnect_action = QAction("Reconnect", self)
        self.settings_action = QAction("Settings", self)

        # Connect actions to functions
        self.connect_action.triggered.connect(self.connect_conn)
        self.disconnect_action.triggered.connect(self.disconnect_conn)
        self.reconnect_action.triggered.connect(self.reconnect_conn)
        self.settings_action.triggered.connect(self.open_settings_window)

        options_menu.addAction(self.connect_action)
        options_menu.addAction(self.disconnect_action)
        options_menu.addAction(self.reconnect_action)
        options_menu.addAction(self.settings_action)

        # Set initial states
        self.update_menu_actions()

        # Main widget and layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_settings_window(self):

        """
        Open the settings window and position it at the center of the main
        window. This method checks if the settings window is not already
        visible, calculates the center position relative to the main window,
        and moves the settings window to that position. It also sets the
        window modality to application modal and ensures the settings window
        stays on top and behaves as a dialog. Finally, it shows, raises, and
        activates the settings window.
        """

        if not self.settings_window.isVisible():
            # Calculate the center position
            main_window_rect = self.geometry()
            settings_window_rect = self.settings_window.geometry()
            center_x = main_window_rect.x() + (
                (main_window_rect.width()
                 - settings_window_rect.width()) // 2
            )
            center_y = main_window_rect.y() + (
                (main_window_rect.height()
                 - settings_window_rect.height()) // 2
            )
            self.settings_window.move(center_x, center_y)

        self.settings_window.setWindowModality(
            Qt.WindowModality.ApplicationModal
        )
        self.settings_window.setWindowFlags(
            self.settings_window.windowFlags()
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Dialog
        )
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def connect_conn(self):

        """
        Establish a connection to the serial device.

        This method attempts to connect to the serial device using the
        connection object stored in `self.conn`. Once the connection is
        established, it updates the menu actions to reflect the new state.

        Raises:
            SerialException: If the connection to the serial device fails.
        """

        self.conn.connect()
        self.update_menu_actions()

    def disconnect_conn(self):

        """
        Disconnect from the serial connection.

        This method disconnects the current serial connection and updates
        the menu actions to reflect the disconnection status.
        """

        self.conn.disconnect()
        self.update_menu_actions()

    def reconnect_conn(self):

        """
        Reconnect to the serial connection.

        This method attempts to re-establish the serial connection by calling
        the `reconnect` method on the `conn` attribute. After successfully
        reconnecting, it updates the menu actions to reflect the current state
        of the connection.
        """

        self.conn.reconnect()
        self.update_menu_actions()

    def update_menu_actions(self):

        """
        Update the state of menu actions based on the connection status.

        This method enables or disables the connect, disconnect, and reconnect
        actions in the menu based on whether the Arduino connection is open or
        not. If the Arduino is connected and the connection is open, the
        connect action is disabled, and the disconnect and reconnect actions
        are enabled. If the Arduino is not connected or the connection is
        closed, the connect action is enabled, and the disconnect and
        reconnect actions are disabled.
        """

        if self.conn.arduino and self.conn.arduino.is_open:
            self.connect_action.setEnabled(False)
            self.disconnect_action.setEnabled(True)
            self.reconnect_action.setEnabled(True)
        else:
            self.connect_action.setEnabled(True)
            self.disconnect_action.setEnabled(False)
            self.reconnect_action.setEnabled(False)

    def on_tab_changed(self, index):

        """
        Handle tab change events.
        This method is called when the tab is changed. It performs different
        actions based on the index of the selected tab:
        - If the index is 0, it disables the timeout and sends the current
            color values.
        - If the index is 1, it disables the timeout and sets the mode based
            on the selected button's text.
        - If the index is 2, it enables the timeout and starts the visualizer.
        Args:
            index (int): The index of the selected tab.
        """

        self.unactiveTab()

        if index == 0:
            self.conn.send_timeout(False)
            self.conn.send_color(self.R, self.G, self.B)
        elif index == 1:
            self.conn.send_timeout(False)
            if self.selected_button:
                self.conn.set_mode(self.selected_button.text())
        elif index == 2:
            self.conn.send_timeout(True)
            self.visualizer.start()

    def unactiveTab(self):

        """
        Deactivate the current tab by setting the connection mode to "OFF" and
        stopping any running visualizer or screen responsiveness processes.

        This method performs the following actions:
        1. Sets the connection mode to "OFF".
        2. Stops the visualizer if it is running.
        3. Stops the screen responsiveness process if it is running.
        """

        self.conn.set_mode("OFF")
        if hasattr(self, 'visualizer') and self.visualizer.is_running():
            self.visualizer.stop()
        if hasattr(self, 'screen_responsive') \
                and self.screen_responsive.is_running():
            self.screen_responsive.stop()

    def create_solid_tab(self):

        """
        Create the Solid tab with RGB color controls and a color picker button.
        This method creates a tab containing:
        - Three sets of checkboxes, spin boxes, and sliders for controlling
            the Red, Green, and Blue color values.
        - A color picker button to open a color selection dialog.
        Each color control set includes:
        - A checkbox to enable/disable the corresponding color controls.
        - A spin box to display and set the color value (0-255).
        - A slider to adjust the color value (0-255).
        The spin box and slider values are synchronized, and their enabled
            state is controlled by the checkbox.
        Returns:
            QFrame: A frame containing the layout with all the color controls
                and the color picker button.
        """

        frame = QFrame()
        layout = QVBoxLayout()

        # Color Sliders and Checkboxes
        for color in ["Red", "Green", "Blue"]:
            checkbox = QCheckBox(color)
            value_box = QSpinBox()
            value_box.setRange(0, 255)
            value_box.setValue(128)
            value_box.setEnabled(False)  # Initially disabled
            value_box.setFixedWidth(100)

            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 255)
            slider.setValue(128)
            slider.setEnabled(False)  # Initially disabled
            slider.setFixedWidth(250)

            # Sync the value box and slider values
            value_box.valueChanged.connect(
                lambda val,
                sl=slider,
                color=color: self.value_box_control(sl, val, color)
            )
            slider.sliderReleased.connect(
                lambda vb=value_box,
                sl=slider: self.slider_control(vb, sl.value())
            )

            # Enable/disable the slider and value box based on checkbox state
            checkbox.stateChanged.connect(
                lambda state,
                vb=value_box,
                sl=slider,
                color=color: self.toggle_rgb_controls(state, vb, sl, color)
            )

            # Add widgets to layout
            hlayout = QHBoxLayout()
            hlayout.addWidget(checkbox)
            hlayout.addWidget(value_box)
            hlayout.addWidget(slider)
            layout.addLayout(hlayout)

        # Color Picker
        color_picker_button = QPushButton("Color Picker")
        color_picker_button.clicked.connect(self.open_color_picker)
        layout.addWidget(color_picker_button)

        frame.setLayout(layout)
        return frame

    def create_pattern_tab(self):

        """
        Create the Pattern tab with buttons for different LED patterns.
        This method creates a new QFrame and sets up a QVBoxLayout. It then
        creates a series of QPushButton widgets for each pattern in the
        predefined list of patterns. Each button is made checkable and
        connected to the select_pattern method. The buttons are added to the
        layout, which is then set on the frame.
        Returns:
            QFrame: The frame containing the layout with pattern buttons.
        """

        frame = QFrame()
        layout = QVBoxLayout()

        # Pattern Buttons
        patterns = ["Fade", "Cycle", "Rainbow Cycle", "Breathing", "Random"]
        for pattern in patterns:
            button = QPushButton(pattern)
            button.setCheckable(True)
            button.clicked.connect(self.select_pattern)
            self.pattern_buttons.append(button)
            layout.addWidget(button)

        frame.setLayout(layout)
        return frame

    def create_audio_reactive_tab(self):

        """
        Create the Audio Reactive tab.

        This method initializes a new QFrame and sets up a QVBoxLayout for it.
        It then creates an instance of AudioVisualizer with the specified
        layout, connection, and type, and assigns it to the visualizer
        attribute. Finally, it sets the layout to the frame and returns the
        frame.

        Returns:
            QFrame: The frame containing the audio reactive tab layout.
        """

        frame = QFrame()
        layout = QVBoxLayout()
        self.visualizer = AudioVisualizer(layout, self.conn, type="qt")
        frame.setLayout(layout)
        return frame

    def create_screen_reactive_tab(self):

        """
        Create the Screen Reactive tab.
        This method sets up the UI components for the Screen Reactive tab,
        including:
        - A frame and main vertical layout.
        - FPS setting with a label and spin box.
        - A label to display the capturing status.
        - A button to select screen dimensions.
        - A button to clear the capturing label.
        - Buttons to start and stop screen capture.
        - Horizontal layouts for organizing the buttons.
        Returns:
            QFrame: The frame containing the Screen Reactive tab UI components.
        """

        frame = QFrame()
        layout = QVBoxLayout()

        # FPS Setting
        fps_label = QLabel("FPS:")
        fps_box = QSpinBox()
        fps_box.setRange(1, 15)
        fps_box.setValue(self.FPS)
        fps_box.valueChanged.connect(self.update_fps)

        # Add a horizontal layout for FPS setting
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(fps_label)
        fps_layout.addWidget(fps_box)

        # Add a label for capturing status
        self.capturing_label = QLabel("Capturing: Full Screen")
        self.capturing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a button to select screen dimensions
        select_dimensions_button = QPushButton("Select Screen Dimensions")
        select_dimensions_button.clicked.connect(
            self.open_screen_dimension_selector
        )
        clear_snapshot_button = QPushButton("Clear Snapshot")
        clear_snapshot_button.clicked.connect(self.clear_capturing_label)

        # Add a button to start screen capture
        start_button = QPushButton("Start Screen Capture")
        start_button.clicked.connect(self.start_screen_capture)

        # Add a button to stop screen capture
        stop_button = QPushButton("Stop Screen Capture")
        stop_button.clicked.connect(self.stop_screen_capture)

        # Add a horizontal layout for start and stop buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(start_button)
        button_layout.addWidget(stop_button)

        # Add a horizontal layout for clear snapshot button
        clear_snapshot_layout = QHBoxLayout()
        clear_snapshot_layout.addWidget(select_dimensions_button)
        clear_snapshot_layout.addWidget(clear_snapshot_button)

        # Add all widgets to the main layout
        layout.addLayout(fps_layout)
        layout.addWidget(
            self.capturing_label, alignment=Qt.AlignmentFlag.AlignCenter
        )
        layout.addLayout(clear_snapshot_layout)
        layout.addLayout(button_layout)

        frame.setLayout(layout)
        return frame

    # Solic Tab Functions
    def toggle_rgb_controls(self, state, value_box, slider, color):

        """
        Enable or disable RGB controls based on checkbox state.
        Parameters:
        state (int): The state of the checkbox
            (0 for unchecked, non-zero for checked).
        value_box (QSpinBox): The spin box widget for the RGB value.
        slider (QSlider): The slider widget for the RGB value.
        color (str): The color to be controlled ("Red", "Green", or "Blue").
        Returns:
        None
        """

        enabled = state != 0

        if color == "Red":
            self.R = 0 if not enabled else value_box.value()
        elif color == "Green":
            self.G = 0 if not enabled else value_box.value()
        elif color == "Blue":
            self.B = 0 if not enabled else value_box.value()

        self.conn.send_color(self.R, self.G, self.B)

        value_box.setEnabled(enabled)
        slider.setEnabled(enabled)

    def value_box_control(self, sl, value, color):

        """
        Sync the value box and slider values.

        Parameters:
        sl (QSlider): The slider widget to update.
        value (int): The value to set on the slider.
        color (str): The color to update in the value box.

        Returns:
        None
        """

        sl.setValue(value)
        self.update_color(value, color)

    def slider_control(self, vb, value):

        """
        Sync the slider and value box values.

        Parameters:
            vb (QWidget): The value box widget to be updated.
            value (int): The value to set in the value box.
        """

        vb.setValue(value)

    def update_color(self, value, color):
        """
        Update the color values and send to the connection.
        Args:
            value (int): The new value for the specified color.
            color (str): The color to update.
                Should be one of "Red", "Green", or "Blue".
        Raises:
            ValueError: If the color is not one of "Red", "Green", or "Blue".
        """

        if color == "Red":
            self.R = value
        elif color == "Green":
            self.G = value
        elif color == "Blue":
            self.B = value

        self.conn.send_color(self.R, self.G, self.B)

    def open_color_picker(self):

        """
        Opens a color picker dialog for the user to select a color.

        If a valid color is selected, the RGB values are extracted and sent
        to the connected device.

        Attributes:
            self.R (int): Red component of the selected color.
            self.G (int): Green component of the selected color.
            self.B (int): Blue component of the selected color.
        """

        color = QColorDialog.getColor()
        if color.isValid():
            self.R, self.G, self.B = color.red(), color.green(), color.blue()
            self.conn.send_color(self.R, self.G, self.B)

    # Pattern Tab Functions
    def select_pattern(self):

        """
        Handles the selection of a pattern from the pattern tab.
        This method is triggered when a pattern button is clicked. It checks
        if the clicked button is the same as the currently selected button.
        If it is, the button remains checked and the method returns. If a
        different button is clicked, the previously selected button is
        unchecked, and the clicked button is marked as the new selected button.
        The mode is then set based on the text of the clicked button.
        Returns:
            None
        """

        clicked_button = self.sender()

        if clicked_button == self.selected_button:
            clicked_button.setChecked(True)
            return

        if self.selected_button:
            self.selected_button.setChecked(False)

        # Mark the clicked button as the selected one
        self.selected_button = clicked_button \
            if clicked_button.isChecked() else None

        self.conn.set_mode(clicked_button.text())

    # Screen Reactive Tab Functions
    def open_screen_dimension_selector(self):

        """
        Open the screen dimension selector.

        This method initializes the ScreenDimensionSelector, sets the callback
        function for when the selection is complete, and displays the selector
        to the user.
        """

        self.selector = ScreenDimensionSelector()
        self.selector.selection_complete_callback = self.update_capturing_label
        self.selector.show()

    def update_capturing_label(self, x1, y1, x2, y2):

        """
        Update the capturing label with the selected dimensions.

        Args:
            x1 (int): The x-coordinate of the top-left corner of the selected
                portion.
            y1 (int): The y-coordinate of the top-left corner of the selected
                portion.
            x2 (int): The x-coordinate of the bottom-right corner of the
                selected portion.
            y2 (int): The y-coordinate of the bottom-right corner of the
                selected portion.

        Returns:
            None
        """

        self.capturing_label.setText(
            f"Capturing: Portion ({x1}, {y1}) to ({x2}, {y2})"
        )
        self.screen_responsive.select_snapshot(x1, y1, x2 - x1, y2 - y1)

    def clear_capturing_label(self):

        """
        Clear the capturing label by resetting its text to
        "Capturing: Full Screen" and clearing the snapshot from the
        screen_responsive object.
        """

        self.capturing_label.setText("Capturing: Full Screen")
        self.screen_responsive.clear_snapshot()

    def update_fps(self, value):

        """
        Update the FPS (frames per second) value.

        Args:
            value (int): The new FPS value to set.
        """

        self.FPS = value
        self.screen_responsive.update_fps(value)

    def start_screen_capture(self):

        """
        Start the screen capture process.

        This method initiates the screen capture by starting the
        screen_responsive thread or process. It is intended to be called when
        the screen capture functionality needs to be activated.
        """

        self.screen_responsive.start()

    def stop_screen_capture(self):

        """
        Stop the screen capture process.

        This method stops the screen capture by calling the `stop` method on
        the `screen_responsive` attribute of the instance.

        Raises:
            AttributeError: If `screen_responsive` attribute is not set.
        """

        self.screen_responsive.stop()


class SettingsWindow(QMainWindow):

    """
    A QMainWindow subclass that provides a settings window for configuring
    the connection port and baud rate.
    Attributes:
        conn (Connection): The connection object used to get available ports
                           and update settings.
        port_dropdown (QComboBox): Dropdown for selecting the connection port.
        baud_dropdown (QComboBox): Dropdown for selecting the baud rate.
    Methods:
        __init__(conn):
            Initializes the settings window with the given connection object.
        update_settings():
            Updates the connection settings based on user selection.
    """

    def __init__(self, conn):

        """
        Initialize the settings window.
        Args:
            conn: A connection object that provides access to available ports.
        Attributes:
            conn: Stores the connection object.
            port_dropdown (QComboBox): Dropdown menu for selecting the port.
            baud_dropdown (QComboBox): Dropdown menu for selecting the baud
                rate.
        Methods:
            update_settings: Updates the settings when the dropdown selection
                changes.
        """

        super().__init__()
        self.conn = conn
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon("icon.ico"))

        # Main layout
        layout = QVBoxLayout()

        # Port dropdown
        port_label = QLabel("PORT:")
        self.port_dropdown = QComboBox()
        ports = self.conn.get_ports()
        for port in ports:
            self.port_dropdown.addItem(ports[port], port)
        self.port_dropdown.setCurrentText(ports[self.conn.port])

        port_layout = QHBoxLayout()
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_dropdown)

        # Baud rate dropdown
        baud_label = QLabel("Baud Rate:")
        self.baud_dropdown = QComboBox()
        baud_rates = [9600, 19200, 38400, 57600, 115200]
        for rate in baud_rates:
            self.baud_dropdown.addItem(str(rate))

        baud_layout = QHBoxLayout()
        baud_layout.addWidget(baud_label)
        baud_layout.addWidget(self.baud_dropdown)

        # on change update settings
        self.port_dropdown.currentIndexChanged.connect(self.update_settings)
        self.baud_dropdown.currentIndexChanged.connect(self.update_settings)

        # Add widgets to layout
        layout.addLayout(port_layout)
        layout.addLayout(baud_layout)

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.show()
        self.close()

    def update_settings(self):

        """
        Update the settings based on user selection.

        This method retrieves the selected port and baud rate from the
        dropdown menus and updates the connection settings accordingly.

        Raises:
            ValueError: If the baud rate is not a valid integer.
        """

        port = self.port_dropdown.currentData()
        baudrate = int(self.baud_dropdown.currentText())
        self.conn.update_settings(port, baudrate)


class ScreenDimensionSelector(QWidget):

    """
    ScreenDimensionSelector is a QWidget subclass that allows users to select
    a rectangular screen area by clicking and dragging the mouse. The
    selection is confirmed or discarded using on-screen buttons.
    Attributes:
        start_pos (QPoint): The starting position of the selection rectangle.
        end_pos (QPoint): The ending position of the selection rectangle.
        selection_complete_flag (bool): A flag indicating whether the
            selection is complete.
        selection_complete_callback (function): A callback function to be
            called when the selection is complete.
        confirm_button (QPushButton): A button to confirm the selection.
        discard_button (QPushButton): A button to discard the selection.
    Methods:
        `mousePressEvent(event)`:
            Handles mouse press events to start the selection.
        `mouseMoveEvent(event)`:
            Handles mouse move events to update the selection rectangle.
        `mouseReleaseEvent(event)`:
            Handles mouse release events to complete the selection.
        `paintEvent(event)`:
            Handles paint events to draw the selection rectangle.
        `keyPressEvent(event)`:
            Handles key press events to close the widget on pressing the
            Escape key.
        `confirm_selection()`:
            Confirms the selection and closes the widget.
        `discard_selection()`:
            Discards the selection and resets the widget.
        `selection_complete()`:
            Calls the selection_complete_callback with the coordinates of the
            selected rectangle.
    """

    def __init__(self):

        """
        Initializes the main window for the Jhagmag LED Controller application.
        This method sets up the main window with the following properties:
        - Frameless window with 90% opacity.
        - Translucent background.
        - Fullscreen mode.
        - Mouse tracking enabled.
        - Initializes start and end positions for selection.
        - Initializes a flag to indicate if the selection is complete.
        - Adds confirm and discard buttons for selection with respective
            styles and click event handlers.
        Attributes:
            start_pos (QPoint): The starting position of the selection.
            end_pos (QPoint): The ending position of the selection.
            selection_complete_flag (bool): Flag to indicate if the selection
                is complete.
            selection_complete_callback (callable): Callback function to be
                called when selection is complete.
            confirm_button (QPushButton): Button to confirm the selection.
            discard_button (QPushButton): Button to discard the selection.
        """

        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint
        )
        self.setWindowOpacity(0.9)  # Adjust opacity for better visibility
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.start_pos = None
        self.end_pos = None
        self.selection_complete_flag = False
        self.setMouseTracking(True)
        self.selection_complete_callback = None

        # Add confirm and discard buttons
        self.confirm_button = QPushButton("✔", self)
        self.confirm_button.setStyleSheet("font-size: 24px; color: green;")
        self.confirm_button.clicked.connect(self.confirm_selection)
        self.confirm_button.hide()

        self.discard_button = QPushButton("✖", self)
        self.discard_button.setStyleSheet("font-size: 24px; color: red;")
        self.discard_button.clicked.connect(self.discard_selection)
        self.discard_button.hide()

    def mousePressEvent(self, event):

        """
        Handle mouse press events.

        This method is triggered when a mouse press event occurs. If the
        selection is not complete, it records the starting position of the
        mouse press and hides the confirm and discard buttons.

        Args:
            event (QMouseEvent): The mouse event that triggered this method.
        """

        if not self.selection_complete_flag:
            self.start_pos = event.pos()
            self.confirm_button.hide()
            self.discard_button.hide()

    def mouseMoveEvent(self, event):

        """
        Handle mouse move events.

        This method is called whenever the mouse is moved within the widget.
        It updates the end position of the selection and triggers a repaint
        if the selection is not yet complete.

        Args:
            event (QMouseEvent): The mouse event containing information about
                                 the mouse movement.
        """

        if not self.selection_complete_flag:
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):

        """
        Handle mouse release events to finalize a selection area.

        This method is triggered when the mouse button is released. It marks
        the end position of the selection, sets the selection complete flag,
        updates the display, and positions the confirm and discard buttons
        near the selection area.

        Args:
            event (QMouseEvent): The mouse event containing the position where
                                 the mouse button was released.
        """

        if not self.selection_complete_flag:
            self.end_pos = event.pos()
            self.selection_complete_flag = True
            self.update()
            self.confirm_button.move(
                self.end_pos.x() - 50, self.end_pos.y() + 10
            )
            self.discard_button.move(
                self.end_pos.x() + 10, self.end_pos.y() + 10
            )
            self.confirm_button.show()
            self.discard_button.show()

    def paintEvent(self, event):

        """
        Handle paint events to draw on the widget.
        This method is called whenever the widget needs to be repainted.
        It uses QPainter to draw a semi-transparent background and, if start
        and end positions are defined, it draws a rectangle from start_pos to
        end_pos.
        Args:
            event (QPaintEvent): The paint event that triggers this method.
        """

        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.PenStyle.SolidLine))
        painter.setBrush(QBrush(QColor(0, 0, 0, 50)))
        painter.drawRect(self.rect())  # Draw the semi-transparent background

        if self.start_pos and self.end_pos:
            rect = QRect(self.start_pos, self.end_pos)
            painter.setBrush(QBrush(Qt.GlobalColor.transparent))
            painter.drawRect(rect)

    def keyPressEvent(self, event):

        """
        Handle key press events.

        This method is called whenever a key is pressed while the widget has
        focus. If the Escape key is pressed, the widget will close.

        Args:
            event (QKeyEvent): The key event that triggered this method.
        """

        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def confirm_selection(self):

        """
        Confirm the current selection and proceed with the necessary actions.

        This method finalizes the current selection by calling the
        `selection_complete` method and then closes the current window
        or dialog by calling the `close` method.
        """

        self.selection_complete()
        self.close()

    def discard_selection(self):

        """
        Discard the current selection by resetting the start and end positions,
        marking the selection as incomplete, updating the display, and hiding
        the confirm and discard buttons.
        """

        self.start_pos = None
        self.end_pos = None
        self.selection_complete_flag = False
        self.update()
        self.confirm_button.hide()
        self.discard_button.hide()

    def selection_complete(self):

        """
        Complete the selection process by determining the rectangular area
        defined by the start and end positions. If both positions are set,
        it calculates the top-left and bottom-right coordinates of the
        rectangle and invokes the selection complete callback with these
        coordinates.

        The callback function is called with the following parameters:
        - x1: The minimum x-coordinate of the selection rectangle.
        - y1: The minimum y-coordinate of the selection rectangle.
        - x2: The maximum x-coordinate of the selection rectangle.
        - y2: The maximum y-coordinate of the selection rectangle.
        """

        if self.start_pos and self.end_pos:
            x1, y1 = self.start_pos.x(), self.start_pos.y()
            x2, y2 = self.end_pos.x(), self.end_pos.y()
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            if self.selection_complete_callback:
                self.selection_complete_callback(x1, y1, x2, y2)


def load_stylesheet(app, file_path):

    """
    Loads a stylesheet from a file and applies it to the given application.

    Args:
        app: The application instance to which the stylesheet will be applied.
        file_path (str): The path to the stylesheet file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there is an error reading the file.
    """

    with open(file_path, "r") as f:
        app.setStyleSheet(f.read())


# Main Application Execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LEDControllerUI()

    # Load the stylesheet
    load_stylesheet(app, "style.qss")

    window.show()
    sys.exit(app.exec())
