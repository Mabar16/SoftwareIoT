import machine
from machine import Pin
import pycom
import time
import wifiHandler as handler
from pysense import Pysense
from LTR329ALS01 import LTR329ALS01
import utime


pycom.heartbeat(False)

# Setup Connection
wifi = handler.WifiHandler()
wifi.connect()

# Setup temperature sensor
p_out = Pin('P19', mode=Pin.OUT)
p_out.value(1)
adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P16')   # create an analog pin on P16

# Setup Light sensor
py = Pysense()
lt = LTR329ALS01(pysense = py, sda = 'P22', scl = 'P21',gain = LTR329ALS01.ALS_GAIN_96X,  rate=LTR329ALS01.ALS_RATE_1000, integration = LTR329ALS01.ALS_INT_50)


count = 0                       # Number of transmissions
while True:
    temperature = apin()        # read an analog value
    lightValue = lt.light()     # Read the light value, format: (a, b)
    lightAvg = (lightValue[0] + lightValue[1]) / 2
    pycom.rgbled(0x020502)      # LED OFF
    timestamp = utime.ticks_cpu()
    payload = "%s,%s,%s,%s" % (str(temperature), str(lightAvg), str(count), str(timestamp))
    if not wifi.is_connected():
        pycom.rgbled(0xFF0000)
        wifi.connect()
    wifi.send(payload)
    count += 1
    time.sleep(1)
    