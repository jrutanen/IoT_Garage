---
generator: 'pdoc 0.5.3'
title: Battery API documentation
viewport: 'width=device-width, initial-scale=1, minimum-scale=1'
---

<div id="section-intro" class="section">

Source code
    from SerialDevice import *

    class Battery (SerialDevice):
        """Battery device
        This class is used for devices that report battery voltage
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
            """Reads data from serial port

            Returns:
            string: String that was received from serial connection
           """
            voltage =\
                self.serial_conn.readline().decode().replace('\r\n', '')
            return voltage

        def set_alarm_severity(self, value):
            """Sets alarm value for the device.
            
            Parameters:
            value (string): raw data from the serial port as string
           """
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
            """Sends update to ThingSpeak server for battery level. Update
            is sent only of the value has changed more than diff or minimum
            update frequency is met.
            
            Parameters:
            value (string): raw data from the serial port as string
            """
            #Check if we should send the update
            if self.publish_battery_data(value):
                #ThingSpeak connection
                thing_speak = ThingSpeak()
                thing_speak.publish(self.thing_speak_field, value)
                self.time_published = datetime.datetime.now()

        def publish_battery_data(self, value):
            """Checks if
            A: We have not sent any update to ThingSpeak previosly
            B: If the value has changed more than diff
            C: More than min_update_freq seconds is passed
            D: Less than max_update_freq seconds is passed
            
            Parameters:
            value (string): raw data from the serial port as string

            Returns:
            boolean: True is A, B or C, False otherwise
            """
            #Case A
            if self.time_published is None:
                return True
            #Case B
            #Check that we have previous measurement
            if len(self.measurements) > 1:
                #value is already added to the end of the measurements so
                #comparison is between the current value and the second last
                #value in the measurements list
                change = abs(float(value) - float(self.measurements[-2]))
                if (change > self.diff):
                    return True
            else:
                #No previous measurement
                return True

            #Case C & D
            time_after_publish = \
                (datetime.datetime.now()\
                - self.time_published).total_seconds()

            if time_after_publish > self.min_publish_freq:
                return True

            if time_after_publish < self.max_publish_freq:
                return False

            #Just in case none of the above conditions are met
            return False

</div>

<div class="section">

</div>

<div class="section">

</div>

<div class="section">

</div>

<div class="section">

Classes {#header-classes .section-title}
-------

` class Battery (ancestors: SerialDevice.SerialDevice)`{.flex .name .class}

:   <div class="section desc">

    Battery device This class is used for devices that report battery
    voltage

    </div>

    Source code

        class Battery (SerialDevice):
            """Battery device
            This class is used for devices that report battery voltage
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
                """Reads data from serial port

                Returns:
                string: String that was received from serial connection
               """
                voltage =\
                    self.serial_conn.readline().decode().replace('\r\n', '')
                return voltage

            def set_alarm_severity(self, value):
                """Sets alarm value for the device.
                
                Parameters:
                value (string): raw data from the serial port as string
               """
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
                """Sends update to ThingSpeak server for battery level. Update
                is sent only of the value has changed more than diff or minimum
                update frequency is met.
                
                Parameters:
                value (string): raw data from the serial port as string
                """
                #Check if we should send the update
                if self.publish_battery_data(value):
                    #ThingSpeak connection
                    thing_speak = ThingSpeak()
                    thing_speak.publish(self.thing_speak_field, value)
                    self.time_published = datetime.datetime.now()

            def publish_battery_data(self, value):
                """Checks if
                A: We have not sent any update to ThingSpeak previosly
                B: If the value has changed more than diff
                C: More than min_update_freq seconds is passed
                D: Less than max_update_freq seconds is passed
                
                Parameters:
                value (string): raw data from the serial port as string

                Returns:
                boolean: True is A, B or C, False otherwise
                """
                #Case A
                if self.time_published is None:
                    return True
                #Case B
                #Check that we have previous measurement
                if len(self.measurements) > 1:
                    #value is already added to the end of the measurements so
                    #comparison is between the current value and the second last
                    #value in the measurements list
                    change = abs(float(value) - float(self.measurements[-2]))
                    if (change > self.diff):
                        return True
                else:
                    #No previous measurement
                    return True

                #Case C & D
                time_after_publish = \
                    (datetime.datetime.now()\
                    - self.time_published).total_seconds()

                if time_after_publish > self.min_publish_freq:
                    return True

                if time_after_publish < self.max_publish_freq:
                    return False

                #Just in case none of the above conditions are met
                return False

    ### Class variables

    `var diff`{.name}

    :   <div class="section desc">

        </div>

    `var max_publish_freq`{.name}

    :   <div class="section desc">

        </div>

    `var max_voltage`{.name}

    :   <div class="section desc">

        </div>

    `var min_publish_freq`{.name}

    :   <div class="section desc">

        </div>

    `var time_published`{.name}

    :   <div class="section desc">

        </div>

    `var voltage`{.name}

    :   <div class="section desc">

        </div>

    ### Methods

    ` def __init__(self, max_voltage, **kwds)`{.name .flex}

    :   <div class="section desc">

        Initialize self. See help(type(self)) for accurate signature.

        </div>

        Source code

            def __init__(self, max_voltage, **kwds):
                super(Battery, self).__init__(**kwds)
                self.max_voltage = max_voltage

    ` def publish(self, value)`{.name .flex}

    :   <div class="section desc">

        Sends update to ThingSpeak server for battery level. Update is
        sent only of the value has changed more than diff or minimum
        update frequency is met.

        Parameters: value (string): raw data from the serial port as
        string

        </div>

        Source code

            def publish(self, value):
                """Sends update to ThingSpeak server for battery level. Update
                is sent only of the value has changed more than diff or minimum
                update frequency is met.
                
                Parameters:
                value (string): raw data from the serial port as string
                """
                #Check if we should send the update
                if self.publish_battery_data(value):
                    #ThingSpeak connection
                    thing_speak = ThingSpeak()
                    thing_speak.publish(self.thing_speak_field, value)
                    self.time_published = datetime.datetime.now()

    ` def publish_battery_data(self, value)`{.name .flex}

    :   <div class="section desc">

        Checks if\
        **`A`** : `We` `have` `not` `sent` `any` `update` `to` `ThingSpeak` `previosly`
        :    

        **`B`** : `If` `the` `value` `has` `changed` `more` `than` `diff`
        :    

        **`C`** : `More` `than` `min_update_freq` `seconds` `is` `passed`
        :    

        **`D`** : `Less` `than` `max_update_freq` `seconds` `is` `passed`
        :    

        Parameters: value (string): raw data from the serial port as
        string

        Returns:\
        **`boolean`** : `True` `is` `A`, `B` or `C`, `False` `otherwise`
        :    

        </div>

        Source code

            def publish_battery_data(self, value):
                """Checks if
                A: We have not sent any update to ThingSpeak previosly
                B: If the value has changed more than diff
                C: More than min_update_freq seconds is passed
                D: Less than max_update_freq seconds is passed
                
                Parameters:
                value (string): raw data from the serial port as string

                Returns:
                boolean: True is A, B or C, False otherwise
                """
                #Case A
                if self.time_published is None:
                    return True
                #Case B
                #Check that we have previous measurement
                if len(self.measurements) > 1:
                    #value is already added to the end of the measurements so
                    #comparison is between the current value and the second last
                    #value in the measurements list
                    change = abs(float(value) - float(self.measurements[-2]))
                    if (change > self.diff):
                        return True
                else:
                    #No previous measurement
                    return True

                #Case C & D
                time_after_publish = \
                    (datetime.datetime.now()\
                    - self.time_published).total_seconds()

                if time_after_publish > self.min_publish_freq:
                    return True

                if time_after_publish < self.max_publish_freq:
                    return False

                #Just in case none of the above conditions are met
                return False

    ` def read(self)`{.name .flex}

    :   <div class="section desc">

        Reads data from serial port

        Returns:\
        **`string`** : `String` `that` `was` `received` `from` `serial` `connection`
        :    

        </div>

        Source code

            def read(self):
                """Reads data from serial port

                Returns:
                string: String that was received from serial connection
               """
                voltage =\
                    self.serial_conn.readline().decode().replace('\r\n', '')
                return voltage

    ` def set_alarm_severity(self, value)`{.name .flex}

    :   <div class="section desc">

        Sets alarm value for the device.

        Parameters: value (string): raw data from the serial port as
        string

        </div>

        Source code

            def set_alarm_severity(self, value):
                """Sets alarm value for the device.
                
                Parameters:
                value (string): raw data from the serial port as string
               """
                value = float(value.split(";")[0])
                if value > 0.95*self.max_voltage:
                    self.alarm_severity = ALARM_NONE
                elif value > 0.94*self.max_voltage:
                    self.alarm_severity = ALARM_MINOR
                elif value > 0.93*self.max_voltage:
                    self.alarm_severity = ALARM_MAJOR
                else:
                    self.alarm_severity = ALARM_CRITICAL

</div>

Index
=====

<div class="toc">

</div>

-   ### [Classes](#header-classes) {#classes}

    -   #### `Battery`

        -   `__init__`
        -   `diff`
        -   `max_publish_freq`
        -   `max_voltage`
        -   `min_publish_freq`
        -   `publish`
        -   `publish_battery_data`
        -   `read`
        -   `set_alarm_severity`
        -   `time_published`
        -   `voltage`

Generated by [pdoc 0.5.3](https://pdoc3.github.io/pdoc).
