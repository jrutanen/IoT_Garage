from Device import *

class Battery (Device):
    """Battery device
    """

    voltage = 0
    max_voltage = 12.80
    # Fields to be used with ThingSpeak
    thing_speak_fields = {
        "field1": "",
        "field2": "",
        "field3": "",
        "field4": "",
        "field5": "",
        "field6": "",
        "field7": "",
        "field8": ""
    }

    def __init__(self, max_voltage, **kwds):
        super(Battery, self).__init__(**kwds)
        self.max_voltage = max_voltage

    def read(self):
        voltage = self.serial_conn.readline().decode().replace('\r\n', '')
        return voltage

    def write(self, user_input):
        self.input = user_input

    def warning(self):
        warning_level = 0
        if self.voltage > 0.95*self.max_voltage:
            warning_level = 0
        elif self.voltage > 0.94*self.max_voltage:
            warning_level = 1
        elif self.voltage > 0.93*self.max_voltage:
            warning_level = 2
        else:
            warning_level = 3
        return warning_level

    def info(self):
        return id + "is alive"