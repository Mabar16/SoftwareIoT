from __future__ import absolute_import
import serial
import time
file_object = open('log.csv', 'a')

ser = serial.Serial('COM7', 115200)
while True:
    timeBefore=time.time()
    line = str(ser.readline())
    timeAfter=time.time()
    file_object.write(str(str(timeBefore)+","+line+","+str(timeAfter)+"\n")
# Close the file
file_object.close()