from constants import *
from serial import Serial
import collections
import multiprocessing
import datetime
from ThingSpeak import *

class SerialDevice:
    """Super Class for iot device connected via serial port. All devices
    should be inherited from this class
    """

    #State of the device, STOPPED or RUNNING
    current_state = STOPPED
    #Topic is used to identify the device in MQTT network
    topic = None
    #ThingSpeak field
    thing_speak_field = None
    #serial port for the device
    serial_conn = None
    #Identification for the device
    id = ""
    #List of latest measurement results (max 10)
    measurements =  collections.deque(maxlen=10)
    #Process used to read serial data
    p = None
    #Alarm level
    alarm_severity = ALARM_NONE

    def __init__(self, name, field):
        self.id = name
        self.p = multiprocessing.Process(name=name,
                                         target=self.read_data)
        self.thing_speak_field = field

    def set_serial_conn(self, conn_port, conn_baudrate, conn_timeout):
        """Update serial connection parameters for the device
        
        Parameters:
        conn_port (string): Serial port device is connected to
        conn_baudrate (string): Baudrate for the device
        conn_timeout (string): Connection timeout
        """
        self.serial_conn = Serial(port=conn_port,
                                  baudrate=conn_baudrate,
                                  timeout=conn_timeout)

    def start(self):
        """Starts the device. The device starts a process to poll
        the serial port for data.
        """
        if self.serial_conn is None:
            print("Serial connection not set. Device can't be started.")
        elif self.current_state == RUNNING:
            print("Device has already been started.")
        else:
            print(self.info())
            #set state to RUNNING and start polling process
            self.current_state = RUNNING
            self.p.start()

    def stop(self):
        """Stops the device. Process to poll the serial port is
        terminated and state is set to STOPPED.
        """
        if self.current_state == RUNNING:
            self.current_state == STOPPED
            self.p.terminate()
        else:
            print("Device not started yet. Device can't be stopped.")

    def read_data(self):
        """Process to continuously read data from serial port. This
        process will update measurments list with new values. Check for
        alarms and publish data.
        """
        while True:
            value = self.read()
            self.measurements.append(value)
            self.set_alarm_severity(value)
            self.publish(value)
            print(self.id + ": " + value)

    def read(self):
        """Command to read data from the device. Shall be overriden
        by child class.
        """
        return None

    def write(self, user_input):
        """Command to write data to the device. Shall be overriden
        by child class.

        Parameters:
        user_input (string): value to be sent to the device.
        """
        return None

    def set_alarm_severity(self, value):
        """Command to set alarm severity for the device. Shall be
        overriden by child class.

        Parameters:
        value (string): Alarm severity value to set: ALARM_NONE,
                        ALARM_MINOR, ALARM_MAJOR or ALARM_CRITICAL
        """        
        return None

    def publish(self, value):
        """Command to publish information from the device. Can be MQTT
        or ThingSpeak for example. Shall be overriden by child class.

        Parameters:
        value (string): Value to publish
        """
        return None

    def info(self):
        """Information about the device
        
        Returns:
        string: Information about the device
        """
        return self.id + " is alive"