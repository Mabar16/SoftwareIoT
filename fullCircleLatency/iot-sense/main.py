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
    pycom.rgbled(0x000000)
    #print(light)
    light2=lt.light()[0] 
    if (abs(light- light2) > 10000): #Maybe add threshold?
        if(light2 > 10000):
            print('1')
        else:
            print('0')
        light = light2
        #print("LUX:"+str(light2))
