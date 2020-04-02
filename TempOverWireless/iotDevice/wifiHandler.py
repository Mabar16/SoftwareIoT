import network
import time
import socket
import ssl
import uselect as select

class WifiHandler:
    
    def connect(self):
        # setup as a station
        self.wlan = network.WLAN(mode=network.WLAN.STA)
        ssid = ''
        password = ''
        self.wlan.connect(ssid, auth=(network.WLAN.WPA2, password)) 
        while not self.wlan.isconnected():
            time.sleep_ms(50)
        print(self.wlan.ifconfig())

        # (address, port)
        s= socket.socket()
        s.setblocking(True)
     #   s = ssl.wrap_socket(s)
        try:
            s.connect(('52.57.73.53', 8000))
        except OSError as e:
            if str(e) == '[Errno 119] EINPROGRESS': # For non-Blocking sockets 119 is EINPROGRESS
                print("In Progress")
            else:
                raise e

        
        self.sock = s

    def send(self,data):
        #print(data)
        bytess = bytes(str(data),"utf8")
        print(bytess)
        self.sock.send(bytess)

    def is_connected(self):
        return self.wlan.isconnected()

