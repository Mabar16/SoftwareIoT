from __future__ import absolute_import
import serial
import time
with open('log.csv', 'a') as file_object:
    file_object.write("msg,before,after\n")
    print("hell")
    ser = serial.Serial('COM7', 115200,timeout=2)
    while True:
        timeBefore=time.time()
        line = str(ser.readline())
        timeAfter=time.time()
        if(line != None and line != ""):
            file_object.write((line+"," +str(timeBefore)+","+str(timeAfter)+"\n"))


