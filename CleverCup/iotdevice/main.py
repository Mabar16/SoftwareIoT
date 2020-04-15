import machine
from machine import Pin
import pycom
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
import time
import wifiHandler as handler

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
google_api_key = 'AIzaSyCw6xEaydc2w2Cccdkid3Xc8U6SE-WFcAU'					  	#get from google
geo_locate = geolocate(google_api_key, ssid_)	#geo_locate object

valid, location = geo_locate.get_location()
if(valid):
	print("The geo position results: " + geo_locate.get_location_string())

def isWithinTempInterval(tempReading):
    tempMax = 28
    tempMin = 24
    if (tempReading > tempMax or tempReading < tempMin):
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
  #  print(str(pitch) + " | " + str(roll))
    if isWithinTempInterval(readTemp()):
        pycom.rgbled(0x005500)#Green
    else:
        pycom.rgbled(0x555500)#Yellow
    
    
    time.sleep_ms(100)