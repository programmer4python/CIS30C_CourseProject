from signal import signal, SIGINT
from sys import exit

import socket
import logging
import time
import datetime

logging.basicConfig(format='%(asctime)s %(message)s', filename='server.log', level=logging.INFO)
logging.info('server started')
server_started=datetime.datetime.now()
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
seconds = time.time()
local_time = time.ctime(seconds)
mySocket.bind(('localhost', 8080))

mySocket.listen(5)

def exiting():
    logging.warning('server down')
    server_ended=datetime.datetime.now()
    difference = server_ended - server_started
    total_seconds = difference.total_seconds()
    print('Server was up for: ', total_seconds, 'seconds')
    logging.info("Server was up for {0:f}s".format(total_seconds))
    exit(0)

print(local_time,'Waiting for connections')

while True:
    try:
        (recvSocket, address) = mySocket.accept()
    except KeyboardInterrupt:
        exiting()
    except OSError as error:
        print(error)
        logging.error(error)
    except Exception as e:
        print(e)
        logging.error(e)

    print('Request received')
    try:
        recvSocket.recv(1024)
        recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n <html><body><h1>Server is acknowledging</h1></body></html> \r\n",'utf-8'))    
        recvSocket.close()
        logging.error('ConnectionResetError')
    except ConnectionResetError:
        pass


