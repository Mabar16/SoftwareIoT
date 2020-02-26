import pycom
import time
import machine
from pysense import Pysense
from LTR329ALS01 import LTR329ALS01

pycom.heartbeat(False)
py = Pysense()
lt = LTR329ALS01(pysense = py, sda = 'P22', scl = 'P21', rate=LTR329ALS01.ALS_RATE_50)
light = lt.light()
while True: 
    pycom.rgbled(0x550000)
    #print(light)
    light2=lt.light() 
    if (light != light2):
        print('change')
        light = light2
