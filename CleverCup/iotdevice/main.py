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
from machine import RTC

_lock = _thread.allocate_lock()

def unix_time_nanos(dt):
    # Hardcoded reference point:
    my_epoch = 1585699200 # 2020-04-01 00:00:00
    my_epoch_nanos = my_epoch * 1000000000
    days = dt[2] - 1
    seconds = days * 24 * 3600  + dt[3] * 3600 + dt[4] * 60 + dt[5]
    microsecs = seconds * 1000000 + dt[6]
    return microsecs * 1000 + my_epoch_nanos

comfortrange_max = 10
comfortrange_min = 0
deviceid = "markusPycom"

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

rtc = RTC()
rtc.ntp_sync("dk.pool.ntp.org")

# Wait 5 secs for the NTP sync
time.sleep(5)
from geoposition import geolocate

ssid_ = "be7528-2.4GHz" 							                                #usually defined in your boot.py file
google_api_key = config.google_api_key					  	#get from google
geo_locate = geolocate(google_api_key, ssid_)	#geo_locate object

valid, location = geo_locate.get_location()
if(valid):
	print("The geo position results: " + geo_locate.get_location_string())

client = MQTTClient(deviceid, "3.127.128.243",user="your_username", password="your_api_key", port=1883)
client.connect()

def setComfortRange(min, max):
    with _lock:
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
client.subscribe("device/"+deviceid+"/location/request")

def listenForUpdates():
    while True:
        client.check_msg()
        time.sleep_ms(10)

_thread.start_new_thread(listenForUpdates, tuple() )

lastTemp = 0
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
    return buffer

lasttimelocation = 0

def makeLocationUpdateMessage():
    valid, location = geo_locate.get_location()
    if(valid):
        geostring = geo_locate.get_location_string()
        if geostring != None and not "error" in geostring:
            geolist = geostring.split(',')
            message = {
            "latitude": geolist[0],
            "longitude":geolist[1],
            "accuracy":geolist[2]}
            client.publish(topic="device/"+deviceid+"/location/update", msg=ujson.dumps(message))
            print(message) 

def locationUpdates():
    while True:
        try:
            makeLocationUpdateMessage()
        except:
            pass
        time.sleep(30)
        
_thread.start_new_thread(locationUpdates, tuple() )

def makeTempeatureUpdates():
    global lastTemp
    temperature = lastTemp
    readTemp()
    global buffer

    if isWithinTempInterval(temperature):
        pycom.rgbled(0x005500)#Green
    else:
        pycom.rgbled(0x555500)#Yellow

    if (len(buffer) > 50):
        temperature = mean(buffer)
        buffer = []
        lastTemp = temperature
        #print(str(pitch) + " | " + str(roll))
        
        
        timestamp = unix_time_nanos(rtc.now())
        message = {"deviceid" : deviceid,
            "temperature":temperature,
            "pycomtime":timestamp }

        client.publish(topic="clevercup/temperature", msg=ujson.dumps(message))
        #print(message)

def temperatureUpdates():
    while True:
        try:
            makeTempeatureUpdates()
        except:
            pass
        time.sleep_ms(10)

_thread.start_new_thread(temperatureUpdates(), tuple() )

while True:
    #pitch = acc.pitch()
    #roll = acc.roll()
    time.sleep(1)