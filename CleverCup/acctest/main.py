from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
import time

py = Pytrack()
acc = LIS2HH12()

while True:
    pitch = acc.pitch()
    roll = acc.roll()
    print(str(pitch) + " | " + str(roll))
    time.sleep_ms(100)