from __future__ import absolute_import
import serial
import time
file_object = open('log.csv', 'a')

ser = serial.Serial('COM7', 115200)
while True:
    line = str(ser.readline())
    file_object.write(line+","+str(time.time())+"\n")
# Close the file
file_object.close()