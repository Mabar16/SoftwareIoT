from __future__ import absolute_import
import serial
import time
file_object = open('outTimes.csv', 'a')
file_object.write("Before_send,After_send,Message\n")
ser = serial.Serial('COM5', 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)

def send_message(message):
    t1 = time.time()
    bytess = message.to_bytes(1,"big")
    ser.write(bytess)
    t2 = time.time()
    line = str(t1) + "," + str(t2) +","+ str(message) + "," + "\n"
    file_object.write(line)

while True:
    send_message(1)
    time.sleep(1)
    send_message(0)
    time.sleep(1)
