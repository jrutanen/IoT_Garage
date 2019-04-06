from personal import *
from urllib.request import urlopen

class ThingSpeak:
    thing_speak_reporting_counter = 0
    thing_speak_unreported_change = 0
    update_url = ""

    def __init__(self):
        config = getConfig()
#        self.name = name
#        self.thing_speak_fields = thing_speak_values
        self.update_url = config.ThingSpeak_BaseURL\
                       + 'api_key='\
                       + config.ThingSpeak_Write_API_key\
                       + '&'

    def publish(self, field, value):
        # Sending the data to thingspeak
        url = self.update_url + field +'=' + str(value)
        print(url)
        conn = urlopen(url)
        print('ThingSpeak publish entry: ' + str(conn.read().decode()))
        # Closing the connection
        conn.close()
