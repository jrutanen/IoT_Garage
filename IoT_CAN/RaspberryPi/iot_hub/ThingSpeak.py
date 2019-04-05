from personal import *
from urllib.request import urlopen

class ThingSpeak:
    thing_speak_reporting_counter = 0
    thing_speak_unreported_change = 0
    baseURL = ""
    config = None
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


    def __init__(self):
        self.config = getConfig()
        self.name = name
        self.thing_speak_fields = thing_speak_values
        self.baseURL = config.ThingSpeak_BaseURL\
                       + 'api_key='\
                       + config.ThingSpeak_Write_API_key

    def fields_to_string(self):
        field_str = ""
        for field in sorted(self.thing_speak_fields):
            field_str += "&" + field \
                         + "=" \
                         + self.thing_speak_fields[field]
        return field_str

    def publish(self, thing_speak_values):

        # Somethings has to be sent and we did not just send
        # or it was long since we sent something
        if ((self.thing_speak_unreported_change
             and self.thing_speak_reporting_counter >= 100)
             or (self.thing_speak_reporting_counter >= 1 * 36)):
            # Sending the data to thingspeak
            field_str = self.fields_to_string()

            print(self.baseURL + field_str)
            conn = urlopen(self.baseURL + field_str)  # change from str1 to str to publish all
            print('ThingSpeak publish entry: ' + str(conn.read().decode()))
            # Closing the connection
            conn.close()
            self.thing_speak_unreported_change = False
            self.thing_speak_reporting_counter = 0

