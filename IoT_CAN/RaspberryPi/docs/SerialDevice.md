---
generator: 'pdoc 0.5.3'
title: SerialDevice API documentation
viewport: 'width=device-width, initial-scale=1, minimum-scale=1'
---

<div id="section-intro" class="section">

Source code
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

` class SerialDevice`{.flex .name .class}

:   <div class="section desc">

    Super Class for iot device connected via serial port. All devices
    should be inherited from this class

    </div>

    Source code

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

    ### Class variables

    `var alarm_severity`{.name}

    :   <div class="section desc">

        </div>

    `var current_state`{.name}

    :   <div class="section desc">

        </div>

    `var id`{.name}

    :   <div class="section desc">

        </div>

    `var measurements`{.name}

    :   <div class="section desc">

        </div>

    `var p`{.name}

    :   <div class="section desc">

        </div>

    `var serial_conn`{.name}

    :   <div class="section desc">

        </div>

    `var thing_speak_field`{.name}

    :   <div class="section desc">

        </div>

    `var topic`{.name}

    :   <div class="section desc">

        </div>

    ### Methods

    ` def __init__(self, name, field)`{.name .flex}

    :   <div class="section desc">

        Initialize self. See help(type(self)) for accurate signature.

        </div>

        Source code

            def __init__(self, name, field):
                self.id = name
                self.p = multiprocessing.Process(name=name,
                                                 target=self.read_data)
                self.thing_speak_field = field

    ` def info(self)`{.name .flex}

    :   <div class="section desc">

        Information about the device

        Returns:\
        **`string`** : `Information` `about` `the` `device`
        :    

        </div>

        Source code

            def info(self):
                """Information about the device
                
                Returns:
                string: Information about the device
                """
                return self.id + " is alive"

    ` def publish(self, value)`{.name .flex}

    :   <div class="section desc">

        Command to publish information from the device. Can be MQTT or
        ThingSpeak for example. Shall be overriden by child class.

        Parameters: value (string): Value to publish

        </div>

        Source code

            def publish(self, value):
                """Command to publish information from the device. Can be MQTT
                or ThingSpeak for example. Shall be overriden by child class.

                Parameters:
                value (string): Value to publish
                """
                return None

    ` def read(self)`{.name .flex}

    :   <div class="section desc">

        Command to read data from the device. Shall be overriden by
        child class.

        </div>

        Source code

            def read(self):
                """Command to read data from the device. Shall be overriden
                by child class.
                """
                return None

    ` def read_data(self)`{.name .flex}

    :   <div class="section desc">

        Process to continuously read data from serial port. This process
        will update measurments list with new values. Check for alarms
        and publish data.

        </div>

        Source code

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

    ` def set_alarm_severity(self, value)`{.name .flex}

    :   <div class="section desc">

        Command to set alarm severity for the device. Shall be overriden
        by child class.

        Parameters: value (string): Alarm severity value to set:
        ALARM\_NONE, ALARM\_MINOR, ALARM\_MAJOR or ALARM\_CRITICAL

        </div>

        Source code

            def set_alarm_severity(self, value):
                """Command to set alarm severity for the device. Shall be
                overriden by child class.

                Parameters:
                value (string): Alarm severity value to set: ALARM_NONE,
                                ALARM_MINOR, ALARM_MAJOR or ALARM_CRITICAL
                """        
                return None

    ` def set_serial_conn(self, conn_port, conn_baudrate, conn_timeout)`{.name .flex}

    :   <div class="section desc">

        Update serial connection parameters for the device

        Parameters: conn\_port (string): Serial port device is connected
        to conn\_baudrate (string): Baudrate for the device
        conn\_timeout (string): Connection timeout

        </div>

        Source code

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

    ` def start(self)`{.name .flex}

    :   <div class="section desc">

        Starts the device. The device starts a process to poll the
        serial port for data.

        </div>

        Source code

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

    ` def stop(self)`{.name .flex}

    :   <div class="section desc">

        Stops the device. Process to poll the serial port is terminated
        and state is set to STOPPED.

        </div>

        Source code

            def stop(self):
                """Stops the device. Process to poll the serial port is
                terminated and state is set to STOPPED.
                """
                if self.current_state == RUNNING:
                    self.current_state == STOPPED
                    self.p.terminate()
                else:
                    print("Device not started yet. Device can't be stopped.")

    ` def write(self, user_input)`{.name .flex}

    :   <div class="section desc">

        Command to write data to the device. Shall be overriden by
        child class.

        Parameters: user\_input (string): value to be sent to
        the device.

        </div>

        Source code

            def write(self, user_input):
                """Command to write data to the device. Shall be overriden
                by child class.

                Parameters:
                user_input (string): value to be sent to the device.
                """
                return None

</div>

Index
=====

<div class="toc">

</div>

-   ### [Classes](#header-classes) {#classes}

    -   #### `SerialDevice`

        -   `__init__`
        -   `alarm_severity`
        -   `current_state`
        -   `id`
        -   `info`
        -   `measurements`
        -   `p`
        -   `publish`
        -   `read`
        -   `read_data`
        -   `serial_conn`
        -   `set_alarm_severity`
        -   `set_serial_conn`
        -   `start`
        -   `stop`
        -   `thing_speak_field`
        -   `topic`
        -   `write`

Generated by [pdoc 0.5.3](https://pdoc3.github.io/pdoc).
