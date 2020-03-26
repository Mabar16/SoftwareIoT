
import socket
import time
import sys
import select

HOST = ''  # Symbolic name, meaning all available interfaces
PORT = 8000  # Arbitrary non-privileged port

with open('log.csv', 'a') as file_object:
    file_object.write("temp,light,count,pycomtime,laptoptime    \n")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# Bind socket to local host and port
try:
    server.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + msg + ' Message ' + str(msg))
    sys.exit()

server.listen(10)

input = [server, ]  # a list of all connections we want to check for data
# each time we call select.select()

running = 1  # set running to zero to close the server
while running:
    inputready, outputready, exceptready = select.select(input, [], [])

    for s in inputready:  # check each socket that select() said has available data

        if s == server:  # if select returns our server socket, there is a new
                        # remote socket trying to connect
            client, address = server.accept()
            # add it to the socket list so we can check it now
            input.append(client)
            print('new client added%s' % str(address))

        else:
            # select has indicated that these sockets have data available to recv
            data = s.recv(1024)
            if data:
                string = str(data) # read data
                string = string[2:-1] # remove b'...'
                print('%s received from %s' % (string, s.getsockname()))
                with open('log.csv', 'a') as file_object:
                    timeAfter = time.time_ns()
                    file_object.write((string+"," + str(timeAfter)+"\n"))

server.close()
