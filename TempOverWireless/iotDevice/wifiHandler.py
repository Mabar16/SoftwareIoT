import network
import time
import socket
import ssl
import uselect as select

class WifiHandler:

    def connect(self):
        # setup as a station
        wlan = network.WLAN(mode=network.WLAN.STA)
        wlan.connect('be7528-2.4GHz', auth=(network.WLAN.WPA2, '283444193'))
        while not wlan.isconnected():
            time.sleep_ms(50)
        print(wlan.ifconfig())

        # (address, port)
        s= socket.socket()
        s.setblocking(False)
     #   s = ssl.wrap_socket(s)
        try:
            s.connect(('192.168.0.13', 9999))
        except OSError as e:
            if str(e) == '[Errno 119] EINPROGRESS': # For non-Blocking sockets 119 is EINPROGRESS
                print("In Progress")
            else:
                raise e
        
        url= 'http://micropython.org/ks/test.html'
        _, _, host, path = url.split('/', 3)
        addr = socket.getaddrinfo(host, 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
        while True:
            data = s.recv(100)
            if data:
                print(str(data, 'utf8'), end='')
            else:
                break
        s.close()
        
       # s.send(b"A")