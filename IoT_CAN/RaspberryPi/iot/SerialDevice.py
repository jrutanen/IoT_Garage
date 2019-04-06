from constants import *
from serial import Serial
import collections
import multiprocessing
import datetime
from ThingSpeak import *

class SerialDevice:
    """Super Class for iot device and all devices should be
    inherited from this class
    """

    #State of the device, "STOPPED" or state_stopped
    current_state = STOPPED
    #Topic is used to identify the device in MQTT network
    topic = None
    #ThingSpeak field
    thing_speak_field = None
    #serial port for the device
    serial_conn = None
    #Name or id for the device
    id = ""
    #List of last measurement results (max 10)
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
        self.serial_conn = Serial(port=conn_port,
                                  baudrate=conn_baudrate,
                                  timeout=conn_timeout)

    def start(self):
        if self.serial_conn is None:
            print("Serial connection not set. Device can't be started.")
        elif self.current_state == RUNNING:
            print("Device has already been started.")
        else:
            print(self.info())
            self.current_state = RUNNING
            self.p.start()

    def stop(self):
        if self.current_state == RUNNING:
            self.current_state == STOPPED
            self.p.terminate()
        else:
            print("Device not started yet. Device can't be stopped.")

    def read_data(self):
        while True:
            value = self.read()
            self.measurements.append(value)
            self.set_alarm_severity(value)
            self.publish(value)
            print(self.id + ": " + value)

    def read(self):
        return ""

    def write(self, user_input):
        self.input = user_input

    def set_alarm_severity(self, value):
        return 0

    def publish(self, value):
        return 0

    def info(self):
        return self.id + " is alive"