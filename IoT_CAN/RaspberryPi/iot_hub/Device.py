from serial import Serial

class Device:
    """Super Class for iot device and all devices should be
    inherited from this class
    """

    #Topic is used to identify the device in MQTT network
    topic = None
    #Fields to be used with ThingSpeak
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
    #serial port for the device
    serial_conn = None
    id = ""
    input = ""
    last_read_value = ""

    def __init__(self, name):
        self.id = name

    def set_serial_conn(self, conn_port, conn_speed, conn_timeout):
        self.serial_conn = Serial(port=conn_port,
                                  baudrate=conn_speed,
                                  timeout=conn_timeout)

    def read(self):
        return ""

    def write(self, user_input):
        self.input = user_input

    def warning(self):
        return 0

    def info(self):
        return id + "is alive"