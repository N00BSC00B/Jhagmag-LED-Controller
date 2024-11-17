from PIL import ImageGrab, ImageEnhance
import time
from sklearn.cluster import KMeans
import numpy as np
import threading


class ScreenResponsive:

    """
    A class to handle screen responsiveness and send the dominant color over a
    serial connection.
    Attributes:
        conn: The serial connection object.
        running (bool): Indicates if the process is running.
        fps (int): Frames per second (default is 10).
        frame_interval (float): Time per frame in seconds.
        snapshot (tuple): Snapshot region (x, y, width, height).
    Methods:
        `calculate_bounding_box()`:
            Calculates the bounding box for the active window.
        `get_dominant_color()`:
            Gets the dominant color of the screen or snapshot region using
            KMeans clustering.
        `core()`:
            Core function to continuously get the dominant color and send it
            over the serial connection.
        `start()`:
            Starts the process of sending the dominant color over the serial
            connection.
        `stop()`:
            Stops the process.
        `update_fps(new_fps)`:
            Updates the frames per second (FPS) dynamically.
        `select_snapshot(x, y, width, height)`:
            Selects a snapshot region for the screen.
        `clear_snapshot()`:
            Clears the snapshot region.
        `is_running()`:
            Checks if the process is running.
    """

    def __init__(self, conn, fps=10):

        """
        Initializes the screen responsive module.

        Args:
            conn: The connection object to communicate with the screen.
            fps (int, optional): Frames per second. Defaults to 10.

        Attributes:
            conn: Stores the connection object.
            running (bool): Indicates if the screen responsive module is
                running.
            fps (int): Frames per second.
            frame_interval (float): Time per frame in seconds.
            snapshot (tuple or None): Snapshot region defined by
                (x, y, width, height).
        """

        self.conn = conn
        self.running = False
        self.fps = fps  # Frames per second (default 10)
        self.frame_interval = 1.0 / self.fps  # Time per frame in seconds
        self.snapshot = None  # Snapshot region (x, y, width, height)

    # Dynamic bounding box calculation for active window
    def calculate_bounding_box(self):

        """
        Calculate the bounding box of the screen.

        This method captures the current screen size using the ImageGrab module
        and returns a tuple representing the bounding box coordinates.

        Returns:
            tuple: A tuple containing four integers (0, 0, screenX, screenY)
                   representing the bounding box of the screen.
        """

        screensize = ImageGrab.grab().size
        screenX, screenY = screensize
        return (0, 0, screenX, screenY)

    # Function to get the dominant color using KMeans
    def get_dominant_color(self):

        """
        Get the dominant color from a screen snapshot.
        This method captures a snapshot of the screen or a specified region of
        the screen, enhances the color saturation, resizes the image for faster
        processing, and then uses KMeans clustering to determine the dominant
        color in the image.
        Returns:
            tuple: A tuple representing the RGB values of the dominant color.
        Raises:
            Exception: If an error occurs during the process, it prints the
                    error message and returns (0, 0, 0) as the default color.
        """

        try:
            if self.snapshot:
                x, y, width, height = self.snapshot
                image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            else:
                image = ImageGrab.grab()

            converter = ImageEnhance.Color(image)
            image2 = converter.enhance(3)  # Optional: Enhance color saturation

            # Resize the image for faster processing
            image_resized = image2.resize((100, 100))

            # Convert image to numpy array
            image_np = np.array(image_resized)
            image_np = image_np.reshape((-1, 3))  # Reshape to (pixels, RGB)

            # KMeans clustering for dominant color
            kmeans = KMeans(n_clusters=1, random_state=0)
            kmeans.fit(image_np)

            # Get the dominant color (cluster center)
            dominant_color = tuple(map(int, kmeans.cluster_centers_[0]))

            return dominant_color

        except Exception as e:
            print(f"Error: {e}")
            return (0, 0, 0)

    def core(self):

        """
        Core loop that continuously gets the dominant color from the screen
        and sends the RGB values over a serial connection.
        This method runs in a loop while `self.running` is True.
        It performs the following steps:
        1. Gets the dominant color from the screen.
        2. Extracts the RGB values from the dominant color.
        3. Sends the RGB values over a serial connection.
        4. Sleeps for a duration defined by `self.frame_interval` to maintain
        the set FPS rate. If an exception occurs during the execution of the
        loop, it is caught and ignored.
        Attributes:
            self.running (bool): A flag to control the execution of the loop.
            self.frame_interval (float): The interval (in seconds) to sleep
                between iterations to control the FPS rate.
            self.conn (object): The connection object used to send RGB data
                over serial.
        """

        self.running = True
        try:
            while self.running:
                # Get the dominant color
                dominant_color = self.get_dominant_color()
                r, g, b = dominant_color
                # Send RGB data over serial
                self.conn.send_color(r, g, b)
                # print(f"Sent RGB: {r},{g},{b}")

                # Sleep to maintain the set FPS rate
                time.sleep(self.frame_interval)

        except Exception:
            pass

    def start(self):

        """
        Starts the core function in a new thread.

        This method creates and starts a new thread that runs the `core
        method. It allows the `core` method to execute asynchronously.
        """

        threading.Thread(target=self.core).start()

    def stop(self):

        """
        Stops the LED controller by setting its mode to "OFF" and updating the
        running status.

        This method sends a command to the LED controller to switch its mode
        to "OFF" and sets the running` attribute to `False` to indicate that
        the controller is no longer active.
        """

        self.conn.set_mode("OFF")
        self.running = False

    def update_fps(self, new_fps):

        """
        Update the frames per second (FPS) value and recalculate the frame
        interval.

        Args:
            new_fps (float): The new FPS value to set.

        """

        self.fps = new_fps
        self.frame_interval = 1.0 / self.fps

    def select_snapshot(self, x, y, width, height):

        """
        Selects a snapshot region with the specified coordinates and
        dimensions.

        Args:
            x (int): The x-coordinate of the top-left corner of the snapshot
                region.
            y (int): The y-coordinate of the top-left corner of the snapshot
                region.
            width (int): The width of the snapshot region.
            height (int): The height of the snapshot region.
        """

        self.snapshot = (x, y, width, height)

    def clear_snapshot(self):

        """
        Clears the current snapshot.

        This method sets the snapshot attribute to None, effectively clearing
        any stored snapshot data.
        """

        self.snapshot = None

    def is_running(self):

        """
        Check if the screen is currently running.

        Returns:
            bool: True if the screen is running, False otherwise.
        """

        return self.running


# Example usage:
if __name__ == "__main__":
    from serial_connection import SerialConnection

    conn = SerialConnection()
    color_detector = ScreenResponsive(fps=10, conn=conn)
    # color_detector.select_snapshot(100, 100, 300, 200)
    color_detector.start()
