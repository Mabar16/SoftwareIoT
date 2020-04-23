import network
import time
import socket
import ssl
import uselect as select
import config

class WifiHandler:

    def connect(self):
        # setup as a station
        self.wlan = network.WLAN(mode=network.WLAN.STA)
        ssid = config.wifi_ssid
        password = config.wifi_password
        self.wlan.connect(ssid, auth=(network.WLAN.WPA2, password)) 
        while not self.wlan.isconnected():
            time.sleep_ms(50)
        print(self.wlan.ifconfig())

        
      

    def send(self,data):
        print(data)
        bytess = bytes(str(data),"utf8")
        #print(bytess)
        self.sock.send(bytess)

    def is_connected(self):
        return self.wlan.isconnected()

