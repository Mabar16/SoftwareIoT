import time
from machine import UART
import pycom

uart = UART(0, 115200)                         # init with given baudrate
uart.init(115200, bits=8, parity=None, stop=1) # init with given parameters

pycom.heartbeat(False)
while(True):
    data = uart.read(1)
    if data != None:
        if data[0] == 1:
            pycom.rgbled(0xFFFFFF)
        else:
            pycom.rgbled(0)
        