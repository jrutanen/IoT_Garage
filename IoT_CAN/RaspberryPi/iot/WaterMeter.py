from SerialDevice import *

class WaterMeter (SerialDevice):
    """Battery device
    This class is used for devices that report battery voltage
    """

    water_depth = 0
    time_published = None
    #ThingSpeak won't be updated until min_publish_freq seconds has
    #passed but will be updated latest every max_publish_feq
    min_publish_freq = 30
    max_publish_freq = 15

    def __init__(self, **kwds):
        super(WaterMeter, self).__init__(**kwds)

    def read(self):
        """Reads data from serial port

        Returns:
        string: String that was received from serial connection
       """
        water_depth =\
            self.serial_conn.readline().decode().replace('\r\n', '')
        return water_depth

    def set_alarm_severity(self, value):
        """Sets alarm value for the device.
        
        Parameters:
        value (string): raw data from the serial port as string
        """
        depth = int(value)
        if depth > 2:
            self.alarm_severity = ALARM_CRITICAL
        elif depth > 0:
            self.alarm_severity = ALARM_MAJOR
        else:
            self.alarm_severity = ALARM_NONE