import network
import time
import socket
import ssl
import uselect as select

class WifiHandler:
    
    def connect(self):
        # setup as a station
        wlan = network.WLAN(mode=network.WLAN.STA)
        wlan.connect('Network2GHz', auth=(network.WLAN.WPA2, 'kalenderlys'))
        while not wlan.isconnected():
            time.sleep_ms(50)
        print(wlan.ifconfig())

        # (address, port)
        s= socket.socket()
        s.setblocking(True)
     #   s = ssl.wrap_socket(s)
        try:
            s.connect(('192.168.0.13', 8000))
        except OSError as e:
            if str(e) == '[Errno 119] EINPROGRESS': # For non-Blocking sockets 119 is EINPROGRESS
                print("In Progress")
            else:
                raise e

        
        self.sock = s

    def send(self,data):
        print(data)
        bytess = bytes(str(data),"utf8")
        print(bytess)
        self.sock.send(bytess)