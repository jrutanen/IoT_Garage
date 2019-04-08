from SerialDevice import *

class TrashCan (SerialDevice):
    """TrashCan device
    This class is used for TrashCan devices that report temperature,
    how much room trash can has and if the door is locked or not.
    Each sensor sends a separate serial message for the reading.
    """
    def __init__(self, **kwds):
        super(TrashCan, self).__init__(**kwds)

    def read_data(self):
        """Process to continuously read data from serial port. This
        process will update measurments list with new values. Check for
        alarms and publish data.
        """
        while True:
            value = self.read()
            self.measurements.append(value)
            sensor = value[0]
            data = value[1]
            self.set_alarm_severity(sensor, data)
            current_time = datetime.datetime.now()
            if self.time_of_last_measurement is None:
                self.time_of_last_measurement = current_time
            time_diff = (current_time-self.time_of_last_measurement)\
                        .total_seconds()
            if time_diff == 0\
                or time_diff >= self.reporting_freq\
                or self.alarm_severity == ALARM_CRITICAL: 
                self.callback(\
                    type(self), self.id, value, self.alarm_severity,\
                    self.thing_speak_field, self.topic)
                self.time_of_last_measurement = current_time

    def read(self):
        """Reads data from serial port

        Returns:
        string: String that was received from serial connection
       """
        data =\
            self.serial_conn.readline().decode().replace('\r\n', '')
        value = self.decode_data(data)
        return value

    def set_alarm_severity(self, sensor, data):
        """Sets alarm value for the device.
        
        Parameters:
        value (string): raw data from the serial port as string
        """
        if sensor == "Temp":
            self.alarm_severity =\
                self.set_alarm_severity_temperature(data)
        if sensor == "Distance":
            self.alarm_severity =\
                self.set_alarm_severity_distance(data)
        if sensor == "Lock":
            self.alarm_severity =\
                self.set_alarm_severity_lock(data)

    def set_alarm_severity_temperature(self, value):
        value = float(value)
        if value > 0:
            return ALARM_NONE
        return ALARM_CRITICAL

    def set_alarm_severity_distance(self, value):
        value = int(value)
        if value > 90:
            return ALARM_CRITICAL
        elif value > 80:
            return ALARM_MAJOR
        else:
            return ALARM_NONE

    def set_alarm_severity_lock(self, value):
        value = int(value)
        if value == 1:
            return ALARM_CRITICAL
        else:
            return ALARM_NONE


    def decode_data(self, data):
        sensor = ""
        #This device has three sensors connected to it
        #Temperature 'ejacsve/Temp: '
        #Distance 'egebant/Distance: '
        #Lock (0/1) 'erohsat/lock: !state'
        if 'Temp' in data:
            sensor = "Temp"
        elif 'Distance' in data:
            sensor = "Distance"
        elif 'lock' in data:
            sensor = "Lock"
        else:
            print("Unknown sensor type: " + str(data))
            sensor = "Unkown"

        value = (data[data.find(':')+1 :]).strip()

        return (sensor, value)
