#!/usr/bin/python3

"""
MQTT topics must start with: EricssonONE/esignum/
Example: "EricssonONE/edallam/MQTT_Display/text"
"""

from urllib.request import urlopen
import sys
from time import sleep
import json 
import datetime
# For MQTT
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from personal import *
from Battery import *
from ThingSpeak import *


#the callback function
def on_connect(client, userdata, flags, rc):
     print("PUBLISH: Connected With Result Code {}".format(rc))
     client.publish(topic = "edallam/mmsi/boat/status", payload="Online", qos=0, retain=True) # TODO change to a publish that is with "auth"

def on_disconnect(client, userdata, rc):
     client.publish(topic = "edallam/MQTT_Display/text", payload = "This is a test Message")
     print("PUBLISH: Disconnected From Broker")
     client.publish(topic = "edallam/mmsi/boat/status", payload="Offline - Disconnected", qos=0, retain=True) # TODO change to a publish that is with "auth"


# States and Global variables
# BATTERY1
battery1_lastReportedValue = 0.0
# BATTERY2
battery2_lastReportedValue = 0.0
# SOLAR
solar_lastReportedValue    = 0.0
# DOOR
door_lastReportedValue     = 0
# WATER
water_lastReportedValue    = 0

def startit():
    global ThingSpeak_reportingCounter

    global door_lastReportedValue

    client = mqtt.Client()

    config = getConfig()

    #Assigning the object attribute to the Callback Function
    client.will_set("edallam/mmsi/boat/status", payload="Offline - Will", qos=0, retain=True)
    client.username_pw_set(username = config.MQTT_auth['username'], password = config.MQTT_auth['username'])
    client.on_connect = on_connect
    

    client.on_disconnect = on_disconnect

    client.connect(config.broker_address, config.broker_portno)



    while True:
        #try:
        for device in device_list:
            line = device.read()
            print(line)
            send2ThingSpeak()      
            ThingSpeak_reportingCounter += 1

##################################################################
# Functions below
##################################################################


def publishMqttDisplay(topic, payload):
    config = getConfig()
    egarageTopic = "EricssonONE/egarage/{}".format(topic)

    publish.single(\
    topic = egarageTopic, \
    payload = payload, \
    hostname = config.broker_address, \
    client_id ="", \
    keepalive = 60, \
    will = None, \
    auth = config.MQTT_auth, \
    tls = None, \
    protocol = mqtt.MQTTv311, \
    transport = "tcp")

    print("Publish topic: {} payload: {}".format(egarageTopic,payload))
    
##################################################################
# Main battery 
def signalk_battery1(data):
    diff = 0.1
    src_str = "115"
    pgn_str= "128267"
    path_str = "electrical.batteries.0.voltage"

    now = str(datetime.datetime.now())

    delta_message = json.loads(' { "updates":[ \
                    { \
                    "source": { \
                      "device": "/dev/arduino", \
                      "src": "'+ src_str +'", "pgn": "'+ pgn_str +'"}, \
                    "timestamp" : "'+ str(now[:10] +'-'+ now[11:]) +'", \
                    "values": [ \
                       { \
                       "path" : "'+ path_str +' ",  "value" : '+ str(data) +' \
                       } ] \
                    }  \
                    ] }')
    print(delta_message)
    


def publish_display(name, data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global solar_lastReportedValue
    global field4_str
    print("data: {} lastValue: {}".format(data, solar_lastReportedValue))
    if abs(data - solar_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        solar_lastReportedValue = data
        data = '%.2f' % data
        field4_str = '&field4=%s' % (data)
        topic = "Water"
        topic = "MQTT_Display/text"
        publishMqttDisplay(topic, name + ": " + data);        
        
##################################################################
# Solar panel
def decode_solar(line):
    data = float(line[7:])
    if isinstance(data, float):
        return data
    else:
        return float(0.0) // Error

def publish_solar(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global solar_lastReportedValue
    global field4_str
    print("data: {} lastValue: {}".format(data, solar_lastReportedValue))
    if abs(data - solar_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        solar_lastReportedValue = data
        data = '%.2f' % data
        field4_str = '&field4=%s' % (data)
        topic = "Water"
        topic = "MQTT_Display/text"
        publishMqttDisplay(topic, "Solar" + data);




##################################################################
# Water 
def decode_water(line):
    data = int(line[18:])
    if isinstance(data, int):
        return data
    else:
        return 2 // Error

def decode_input(line):
    name, data = line.split(": ")
    data = float(data)
    if isinstance(data, float):
        return data
    else:
        return 2 // Error


def publish_water(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global water_lastReportedValue
    global field5_str
    if abs(data-water_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        water_lastReportedValue = data
        data = '%.2f' % data
        field5_str = '&field5=%s' % (data)

##################################################################
# Door
def decode_door(line):
    data = int(line[6:])
    if isinstance(data, int):
        return data
    else:
        return 2 // Error

def publish_door(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global door_lastReportedValue
    global field6_str
    if abs(data-door_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        door_lastReportedValue = data
        data = '%.2f' % data
        field6_str = '&field6=%s' % (data)
        publishMqttDisplay("The Door on your boat just opened!")

##################################################################
if __name__ == "__main__":
    #TODO: Create factory for creating device objects?
    #Create Two Battery Devices and start them
    battery_one = Battery(name="one", field="field1", max_voltage=12.80)
    battery_one.set_serial_conn(
        conn_port='/dev/ttyUSB0', conn_baudrate=9600, conn_timeout=100)
    battery_one.start()
    battery_two = Battery(name="two", field="field2", max_voltage=12.00)
    battery_two.set_serial_conn(
        conn_port='/dev/ttyUSB1', conn_baudrate=9600, conn_timeout=100)
    battery_two.start()
    sleep(240)
    battery_one.stop()
    battery_two.stop()
