import machine
from machine import Pin
import pycom
import time
import wifiHandler as handler
from pysense import Pysense
from LTR329ALS01 import LTR329ALS01
from machine import RTC

def unix_time_nanos(dt):
    # Hardcoded reference point:
    my_epoch = 1585699200 # 2020-04-01 00:00:00
    my_epoch_nanos = my_epoch * 1000000000
    days = dt[2] - 1
    seconds = days * 24 * 3600  + dt[3] * 3600 + dt[4] * 60 + dt[5]
    microsecs = seconds * 1000000 + dt[6]
    return microsecs * 1000 + my_epoch_nanos

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

rtc = RTC()
rtc.ntp_sync("dk.pool.ntp.org")
print(unix_time_nanos(rtc.now()))
count = 0                       # Number of transmissions
while True:
    temperature = apin()        # read an analog value
    lightValue = lt.light()     # Read the light value, format: (a, b)
    lightAvg = (lightValue[0] + lightValue[1]) / 2
    pycom.rgbled(0x020502)      # LED OFF
    timestamp = unix_time_nanos(rtc.now())
    payload = "%s,%s,%s,%s" % (str(temperature), str(lightAvg), str(count), str(timestamp))
    if not wifi.is_connected():
        pycom.rgbled(0xFF0000)
        wifi.connect()
    wifi.send(payload)
    count += 1
    time.sleep(.500)
    