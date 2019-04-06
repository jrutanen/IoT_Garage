from SerialDevice import *

class Battery (SerialDevice):
    """Battery device
    """

    voltage = 0
    max_voltage = 12.80
    time_published = None
    #ThingSpeak won't be updated until min_publish_freq seconds has
    #passed but will be updated latest every max_publish_feq
    min_publish_freq = 30
    max_publish_freq = 15
    diff = 0.1

    def __init__(self, max_voltage, **kwds):
        super(Battery, self).__init__(**kwds)
        self.max_voltage = max_voltage

    def read(self):
        voltage =\
            self.serial_conn.readline().decode().replace('\r\n', '')
        return voltage

    def write(self, user_input):
        self.input = user_input

    def set_alarm_severity(self, value):
        value = float(value.split(";")[0])
        if value > 0.95*self.max_voltage:
            self.alarm_severity = ALARM_NONE
        elif value > 0.94*self.max_voltage:
            self.alarm_severity = ALARM_MINOR
        elif value > 0.93*self.max_voltage:
            self.alarm_severity = ALARM_MAJOR
        else:
            self.alarm_severity = ALARM_CRITICAL

    def publish(self, value):
        #Battery will publish data to thingSpeak if values have changed
        #or last update is more than 1 minute old
        if self.publish_battery_data(value):
            #ThingSpeak connection
            thing_speak = ThingSpeak()
            thing_speak.publish(self.thing_speak_field, value)
            self.time_published = datetime.datetime.now()

    def publish_battery_data(self, value):
        if self.time_published is None:
            return True
        #current value is not the same as last measurement
        if len(self.measurements) > 1:
            change = abs(float(value) - float(self.measurements[-2]))
            value_changed = (change > self.diff) 
        else:
            value_changed = True

        #check if it's long time since last publish
        time_after_publish = \
            (datetime.datetime.now()\
            - self.time_published).total_seconds()

        if time_after_publish < self.max_publish_freq:
            return False

        old_data =  (time_after_publish > self.min_publish_freq)

        #if value is changed or timer has expired
        if value_changed or old_data:
            return True

        return False
