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
import uos as os
_lock = _thread.allocate_lock()

def unix_time_nanos(dt, seconds):
    microsecs = seconds * 1000000 + dt[6]
    nanos = microsecs * 1000
    return nanos

if 'comfortrange.txt' in os.listdir():    
    try:
        with open('comfortrange.txt', 'r') as datafile:
            text = datafile.readline()
            comfortrange_min = int(text.split(' ')[0])
            comfortrange_max = int(text.split(' ')[1])
    except:
        comfortrange_min = 10
        comfortrange_max = 30
else:
    comfortrange_min = 10
    comfortrange_max = 30

if 'messagecount.txt' in os.listdir():    
    try:
        with open('messagecount.txt', 'r') as datafile:
            text = datafile.readline()
            transmissionCount = int(text)
    except:
        transmissionCount = 0
else:
    transmissionCount = 0


deviceid = config.deviceid

py = Pytrack()
acc = LIS2HH12()

# Setup temperature sensor
p_out = Pin('P19', mode=Pin.OUT)
p_out.value(1)
adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P16', attn=adc.ATTN_2_5DB)   # create an analog pin on P16

pycom.heartbeat(False)

# Setup Connection
wifi = handler.WifiHandler()
wifi.connect()

rtc = RTC()
rtc.ntp_sync("dk.pool.ntp.org")

rtcerrorcount = 0
# Wait for the NTP sync
while( not rtc.synced()):
    time.sleep(1)
    rtcerrorcount += 1
    if(rtcerrorcount > 60):
        pycom.rgbled(0xFF0000)
        running = False
        machine.reset()

from geoposition import geolocate

ssid_ = config.wifi_ssid 						
google_api_key = config.google_api_key			# from google
geo_locate = geolocate(google_api_key, ssid_)	#geo_locate object

valid, location = geo_locate.get_location()
if(valid):
	print("The geo position results: " + geo_locate.get_location_string())

client = MQTTClient(deviceid, config.mqttBrokerIP,user="your_username", password="your_api_key", port=1883)
client.connect()

running = True

def setComfortRange(min, max):
    with _lock:
        print('changing comfort range')
        global comfortrange_max
        comfortrange_max = int(max)
        global comfortrange_min
        comfortrange_min = int(min)

        with open('comfortrange.txt', 'w') as datafile:            
            datafile.write(str(min) + ' ' + str(max))


def handleMQTTMessage(topic, message):
    topic = topic.decode("utf8")
    payload = ujson.loads(message.decode("utf8"))
    if "device/"+deviceid+"/comfortrange/updates" == topic:
        setComfortRange(payload['newmin'], payload['newmax'])


client.set_callback(handleMQTTMessage)
client.subscribe("device/"+deviceid+"/comfortrange/updates")
#client.subscribe("device/"+deviceid+"/location/request") #do we still use this? 
def reconnectMQTT():
  #  wifi.connect()
    client.connect()
    client.subscribe("device/"+deviceid+"/comfortrange/updates")

def listenForUpdates():
    global running
    errorcount = 0
    while running:
        if errorcount > 5:
            pycom.rgbled(0xFF0000)  # Red Error = Receive MQTT Error
            running = False
            machine.reset()
        
        if errorcount > 2:
            try:
                pycom.rgbled(0xFF0000)
                print("reconnecing")
                reconnectMQTT()
                time.sleep(10)
                print("reconnec?")
            except:
                machine.reset()

        try:
            client.check_msg()
            errorcount = 0
        except OSError as e:
            print(e)
            if(e == "[Errno 113] ECONNABORTED"):
                reconnectMQTT()
            errorcount += 1
        
            
        time.sleep_ms(100)

_thread.start_new_thread(listenForUpdates, tuple() )

lastTemp = 0
def getTemperatureColor(tempReading):
    with _lock:
        if (tempReading > comfortrange_max):
            return 0xFF5500
        elif tempReading < comfortrange_min:
            return 0x000088
        else:
            return 0x008800

def mean(alist):
    total = 0
    for item in alist:
        total += item
    return total / len(alist)

def median(alist):
    sortedlist = sorted(alist)
    if (len(alist) ==2):
        return (sortedlist[0] + sortedlist[1])/2
    elif(len(sortedlist) % 2 == 0):
        indexa = len(sortedlist)// 2
        indexb = len(sortedlist)// 2 +1
        return (sortedlist[indexa] + sortedlist[indexb])/2
    else:
        return sortedlist[len(sortedlist)// 2]

buffer = []
def readTemp():
    global buffer
    reading = apin()
    volts = (reading/4096) * 1.4669
    temp = (volts-0.5) /0.01
    buffer.append(temp)
    if(len(buffer) > config.temperatureBufferLength):
        buffer = buffer[1:]
    return median(buffer)

def makeLocationUpdateMessage():
    try:
        valid, location = geo_locate.get_location()
        if(valid):
            geostring = geo_locate.get_location_string()
            if geostring != None and not "error" in geostring:
                geolist = geostring.split(',')
                message = {
                "latitude": geolist[0],
                "longitude":geolist[1],
                "accuracy":geolist[2],
                "deviceid": deviceid}
                client.publish(topic="clevercup/location", msg=ujson.dumps(message), retain=True)
                #print(message) 
    except:
        pycom.rgbled(0xFF00FF)  # Magenta Error = Location Error

def locationUpdates():
    while running:
        try:
            makeLocationUpdateMessage()
        except:
            pass
        time.sleep(config.locationUpdateInterval_s)
        
_thread.start_new_thread(locationUpdates, tuple() )

def sampleTemperature():
    
    meantemperature = readTemp()

    pycom.rgbled(getTemperatureColor(meantemperature))
   

    return meantemperature

def sendTemperatureUpdate(temperature):
    try:
        global transmissionCount
        timestamp = unix_time_nanos(rtc.now(), time.time())
        message = {"deviceid" : deviceid,
            "temperature":temperature,
            "pycomtime":timestamp,
            "count":transmissionCount }

        client.publish(topic="clevercup/temperature", msg=ujson.dumps(message))

        transmissionCount+=1
        with open('messagecount.txt', 'w') as datafile:            
            datafile.write(str(transmissionCount))
            #print(message)
    except OSError as e:
        #   pass
        print(e)
        pycom.rgbled(0xFFFFFF)  # White Error = Send MQTT Temp Error
        raise e

def temperatureUpdates():
    global running
    errorcount = 0
    temperaturesamples = 0
    while running:
        if errorcount > 5:
            pycom.rgbled(0xFF0000)  # Red Error = Receive MQTT Error
            running = False
            machine.reset()
        
        if errorcount > 2:
            try:
                pycom.rgbled(0xFF0000)
                print("reconnecing")
                reconnectMQTT()
                time.sleep(10)
                print("reconnec?")
            except:
                machine.reset()
        try:
            temperature = sampleTemperature()
            temperaturesamples += 1
            if temperaturesamples >= config.temperatureBufferLength/2:
                sendTemperatureUpdate(temperature)
                temperaturesamples = 0
        except OSError as e:
         #   pass
            print(e)
            errorcount += 1
            pycom.rgbled(0xFFFFFF)  # White Error = Send MQTT Temp Error
        time.sleep_ms(config.temperatureUpdateInterval_ms)

_thread.start_new_thread(temperatureUpdates, tuple() )

while running:
    #pitch = acc.pitch()
    #roll = acc.roll()
    time.sleep(1)

pycom.rgbled(0xa200ff) # Purple Error = Some other error?