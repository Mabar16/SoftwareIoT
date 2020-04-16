import machine
from machine import Pin
import pycom
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
import time
import wifiHandler as handler
from umqttsimple import MQTTClient
import ujson
import config
import _thread

comfortrange_max = 10
comfortrange_min = 0
deviceid = "vicPycom"

py = Pytrack()
acc = LIS2HH12()

# Setup temperature sensor
p_out = Pin('P19', mode=Pin.OUT)
p_out.value(1)
adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P16')   # create an analog pin on P16

pycom.heartbeat(False)

# Setup Connection
wifi = handler.WifiHandler()
wifi.connect()

from geoposition import geolocate

ssid_ = "Network2GHz" 							                                #usually defined in your boot.py file
google_api_key = config.google_api_key					  	#get from google
geo_locate = geolocate(google_api_key, ssid_)	#geo_locate object

# valid, location = geo_locate.get_location()
# if(valid):
# 	print("The geo position results: " + geo_locate.get_location_string())

client = MQTTClient(deviceid, "3.126.242.230",user="your_username", password="your_api_key", port=1883)
client.connect()


def setComfortRange(min, max):
    print('changing comfort range')
    global comfortrange_max
    comfortrange_max = int(max)
    global comfortrange_min
    comfortrange_min = int(min)

def handleMQTTMessage(topic, message):
    topic = topic.decode("utf8")
    payload = ujson.loads(message.decode("utf8"))
    if "device/"+deviceid+"/comfortrange/updates" == topic:
        setComfortRange(payload['newmin'], payload['newmax'])

client.set_callback(handleMQTTMessage)
client.subscribe("device/"+deviceid+"/comfortrange/updates")

def listenForUpdates():
    while True:
        client.check_msg()
        time.sleep_ms(10)

_thread.start_new_thread(listenForUpdates, tuple() )


def isWithinTempInterval(tempReading):
    if (tempReading > comfortrange_max or tempReading < comfortrange_min):
        return False
    else:
        return True

def mean(alist):
    total = 0
    for item in alist:
        total += item
    return total / len(alist)

buffer = []
def readTemp():
    global buffer
    reading = apin()
    volts = (reading/4095) * 1.1
    temp = (volts-0.5) /0.01
    buffer.append(temp)
    if(len(buffer) > 10):
        buffer = buffer[1:]
    return mean(buffer)

while True:
    pitch = acc.pitch()
    roll = acc.roll()

    temperature = readTemp()
    #print(str(pitch) + " | " + str(roll))
    if isWithinTempInterval(temperature):
        pycom.rgbled(0x005500)#Green
    else:
        pycom.rgbled(0x555500)#Yellow
    
    message = {"deviceid" : deviceid,
        "temperature":temperature }

    client.publish(topic="clevercup/temperature", msg=ujson.dumps(message))
   
    valid, location = geo_locate.get_location()
    geostring = geo_locate.get_location_string()
    if geostring != None and not "error" in geostring:
        geolist = geostring.split(',')
        message = {"deviceid" : deviceid,
        "latitude": geolist[0],
        "longitude":geolist[1],
        "accuracy":geolist[2]}
        client.publish(topic="clevercup/geolocation", msg=ujson.dumps(message))
    else: 
        print('error')
        
    time.sleep_ms(500)