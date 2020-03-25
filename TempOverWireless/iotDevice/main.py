import machine
from machine import Pin
import pycom
import time
import wifiHandler as handler

pycom.heartbeat(False)

wifi = handler.WifiHandler()
wifi.connect()

p_out = Pin('P19', mode=Pin.OUT)
p_out.value(1)

adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P16')   # create an analog pin on P16

while True:
    val = apin()                    # read an analog value
    pycom.rgbled(0x556633)  # Red
    wifi.send(val)
    time.sleep(1)
    #pycom.rgbled(0x005500)  # Green
    #time.sleep(1)
    #pycom.rgbled(0x000055)  # Blue
    #time.sleep(1)
    