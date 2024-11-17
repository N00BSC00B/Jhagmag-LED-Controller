import serial
import serial.tools.list_ports
import time
import threading


class SerialConnection:

    """
    A class to manage the serial connection to an Arduino for controlling LED
    modes and colors.
    Attributes:
        port (str): The serial port to connect to.
        baudrate (int): The baud rate for the serial connection.
        debug (bool): Flag to enable debug messages.
        arduino (serial.Serial): The serial connection object.
        stop_thread (bool): Flag to control the thread for printing serial
            data.
    Methods:
        `send_timeout(enabled: bool = False)`:
            Enable or disable the timeout feature on the Arduino.
        `set_mode(mode: str)`:
            Set the mode on the Arduino by sending a specific command code.
        `send_color(red: int, green: int, blue: int)`:
            Send RGB color values with a header to indicate color update.
        `print_serial()`:
            Continuously print serial data from the Arduino until stopped.
        `get_ports()` -> dict:
            Get a dictionary of available serial ports and their descriptions.
        `start_thread()`:
            Start the thread to print serial data from the Arduino.
        `update_settings(port: str, baudrate: int)`:
            Update the serial port and baud rate settings.
        `connect()`:
            Establish the serial connection to the Arduino.
        `disconnect()`:
            Close the serial connection to the Arduino.
        `reconnect()`:
            Re-establish the serial connection to the Arduino.
        `close()`:
            Stop the thread and close the serial connection.
    """

    def __init__(self, port, baudrate=9600, debug=False):

        """
        Initializes the serial connection to the Arduino.

        Args:
            port (str): The port to which the Arduino is connected.
            baudrate (int, optional): The baud rate for the serial
                communication. Defaults to 9600.
            debug (bool, optional): Flag to enable or disable debug mode.
                Defaults to False.
        """

        self.arduino = None
        self.port = port
        self.baudrate = baudrate
        self.stop_thread = False  # Flag to control the thread
        self.debug = debug

    def send_timeout(self, enabled: bool = False):

        """
        Sends a timeout setting to the Arduino.

        Args:
            enabled (bool): If True, enables the timeout. If False, disables
                the timeout.

        Returns:
            None
        """

        if not self.arduino or not self.arduino.is_open:
            return
        val = 1 if enabled else 0
        if self.debug:
            print(f"Setting timeout: {'Enabled' if enabled else 'Disabled'}")
        self.arduino.write(bytes([0x01, val]))

    def set_mode(self, mode):

        """
        Set the mode on the Arduino by sending a specific command code.

        Parameters:
        mode (str): The mode to set on the Arduino. Valid modes are:
            - "OFF"
            - "Solid"
            - "Fade"
            - "Cycle"
            - "Rainbow Cycle"
            - "Breathing"
            - "Random"

        Returns:
        None
        """

        if not self.arduino or not self.arduino.is_open:
            return
        modes = {
            "OFF": 0,
            "Solid": 0,
            "Fade": 1,
            "Cycle": 2,
            "Rainbow Cycle": 3,
            "Breathing": 4,
            "Random": 5
        }
        if mode in modes:
            if self.debug:
                print(f"Setting mode: {mode}")
            self.arduino.write(bytes([0x02, modes[mode]]))
        else:
            print(f"Unknown mode: {mode}")

    def send_color(self, red, green, blue):

        """
        Sends RGB color values to the connected Arduino.

        Parameters:
        red (int): The red color value (0-255).
        green (int): The green color value (0-255).
        blue (int): The blue color value (0-255).

        Returns:
        None
        """

        if not self.arduino or not self.arduino.is_open:
            return
        if self.debug:
            print(f"Sending RGB: {red}, {green}, {blue}")
        self.arduino.write(bytes([0x03, red, green, blue]))

    def print_serial(self):

        """
        Continuously print serial data from the Arduino until stopped.

        This method runs in a loop, checking if there is any data available
        to read from the Arduino. If data is available, it reads the data,
        decodes it using UTF-8 encoding (ignoring errors), and prints it to
        the console. If a UnicodeDecodeError occurs during decoding, it
        catches the exception and prints an error message.

        The loop continues to run until the `stop_thread` attribute is set
        to True. A small delay is added at the end of each loop iteration
        to prevent high CPU usage.

        Attributes:
            stop_thread (bool): A flag to stop the loop when set to True.
            arduino (serial.Serial): The serial connection to the Arduino.
        """

        while not self.stop_thread:
            if self.arduino.in_waiting > 0:
                try:
                    data = self.arduino.readline().decode(
                        'utf-8', errors='ignore'
                    ).strip()
                    print("Serial Print: " + data)
                except UnicodeDecodeError as e:
                    print(f"Error decoding data: {e}")
            time.sleep(0.1)  # Small delay to prevent high CPU usage

    def get_ports(self):

        """
        Retrieves a dictionary of available serial ports and their
            descriptions.

        Returns:
            dict: A dictionary where the keys are the device names of the
                  serial ports and the values are their descriptions.
        """

        return {
            port.device: port.description
            for port in serial.tools.list_ports.comports()
        }

    def start_thread(self):

        """
        Starts a new thread to handle serial communication if the Arduino is
        connected and the thread is not already running.

        This method checks if the Arduino is connected and if the serial port
        is open. If both conditions are met and there is no existing active
        thread, it creates and starts a new thread to handle serial
        communication by calling the `print_serial` method.

        Attributes:
            arduino (serial.Serial): The serial connection to the Arduino.
            thread (threading.Thread): The thread handling serial
                communication.
            stop_thread (bool): A flag to indicate whether the thread should
                be stopped.
            debug (bool): A flag to indicate whether debug messages should be
                printed.

        Returns:
            None
        """

        if not self.arduino or not self.arduino.is_open:
            return
        if not hasattr(self, 'thread') or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.print_serial)
            self.stop_thread = False
            if self.debug:
                print("Starting thread")
            self.thread.start()

    def update_settings(self, port, baudrate):

        """
        Update the serial connection settings and reconnect.

        Parameters:
        port (str): The serial port to connect to.
        baudrate (int): The baud rate for the serial connection.

        Returns:
        None
        """

        self.port = port
        self.baudrate = baudrate
        self.reconnect()

    def connect(self):

        """
        Establishes a serial connection to the Arduino.

        This method attempts to open a serial connection to the Arduino using
        the specified port and baud rate. If the connection is already open,
        it does nothing. If the connection is not open, it initializes the
        connection and waits for 2 seconds to allow the Arduino to reset.

        Raises:
            serial.SerialException: If there is an error opening the serial
                connection.
        """

        if not self.arduino or not self.arduino.is_open:
            self.arduino = serial.Serial(self.port, self.baudrate)
            time.sleep(2)  # Allow time for the Arduino to reset

    def disconnect(self):

        """
        Disconnects the Arduino if it is currently connected and open.

        This method checks if the Arduino instance exists and if the serial
        connection is open. If both conditions are met, it closes the serial
        connection to the Arduino.
        """

        if self.arduino and self.arduino.is_open:
            self.arduino.close()

    def reconnect(self):

        """
        Reconnects the serial connection by first disconnecting, waiting for 2
        seconds, and then reconnecting.

        This method ensures that the serial connection is properly reset by
        performing a disconnect and connect sequence.
        """

        self.disconnect()
        time.sleep(2)
        self.connect()

    def close(self):

        """
        Stop the running thread and close the serial connection.

        This method sets the `stop_thread` flag to True, waits for the thread
        to finish execution using `join()`, and then closes the serial
        connection to the Arduino.
        It also deletes the singleton instance of the SerialConnection
        class to allow the creation of new instances if needed.
        """

        self.stop_thread = True
        self.thread.join()
        self.arduino.close()
        del SerialConnection._instance  # Allow new instances if needed


# Usage example:
if __name__ == "__main__":
    conn = SerialConnection(port='COM11', baudrate=9600)
    time.sleep(1)
    timeout = False

    while True:
        user = input("Enter the Type: ")
        if user == "timeout":
            conn.send_timeout(not timeout)
        elif user == "mode":
            mode = input("Enter the mode: ")
            conn.set_mode(mode)
        elif user == "color":
            red = int(input("Enter the red value: "))
            green = int(input("Enter the green value: "))
            blue = int(input("Enter the blue value: "))
            conn.send_color(red, green, blue)
        elif user == "exit":
            break
        else:
            print("Invalid Input")
            continue
        time.sleep(1)
