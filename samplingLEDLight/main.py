import pycom
import time

pycom.heartbeat(False)

while True:
    pycom.rgbled(0xFFFFFF)  # White
    time.sleep(1/10)
    pycom.rgbled(0) # Off
    time.sleep(1/10)

