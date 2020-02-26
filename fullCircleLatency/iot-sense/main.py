import pycom
import time
import machine
from pysense import Pysense
from LTR329ALS01 import LTR329ALS01

pycom.heartbeat(False)
py = Pysense()
lt = LTR329ALS01(pysense = py, sda = 'P22', scl = 'P21',gain = LTR329ALS01.ALS_GAIN_96X,  rate=LTR329ALS01.ALS_RATE_50, integration = LTR329ALS01.ALS_INT_50)
light = lt.light()[0]
while True: 
    pycom.rgbled(0x0000FF)
    #print(light)
    light2=lt.light()[0] 
    if (abs(light- light2) > 0): #Maybe add threshold?
        print('1')
        light = light2
    else:
        print('0')
