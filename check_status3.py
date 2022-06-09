import requests
from time import sleep
import time
import datetime
import hashlib
from urllib.request import urlopen, Request
import logging

logging.basicConfig(format='%(asctime)s %(message)s', filename='monitor.log', level=logging.INFO)

start_monitoring = datetime.datetime.now()
logging.info('Monitoring has begun')
print('Monitoring has begun')

def connected(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            print('Server up')
            logging.info('Server up')

        else:
            print('Server unable to process request')
            logging.warning('Server unable to process request')
    except requests.ConnectionError:
        logging.error('ConnectionError')
        return False
    except ChunkedEncodingError:
        logging.error('ChunkedEncodingError')
    else:
        return True

url = "http://127.0.0.1:8080"

while True:

    if connected(url):

        start = time.perf_counter()
        response = requests.post(url, data = {'key':'value'})
        request_time = time.perf_counter() - start
        print("Server response time is ", response.elapsed.total_seconds())
        response_time = response.elapsed.total_seconds()
        logging.info("Server response time is {0:f}s".format(response_time))

        reading = urlopen(url).read()
        hash = hashlib.sha512(reading).hexdigest()
        sleep(10)
        newhash = hashlib.sha512(reading).hexdigest()
        if newhash == hash:
            print('Website is still the same')
            logging.info('Website unchanged')
        else:
            print('Website has been changed')
            logging.warning('Website has been changed')
            reading = urlopen(url).read()
            hash = hashlib.sha512(response).hexdigest()
            sleep(10)
            continue

    else:
        server_down = datetime.datetime.now()
        while not connected(url):
            time.sleep(5)
            print("Server not up")
            logging.warning('Server is not up')
        server_up = datetime.datetime.now()
        difference = server_up - server_down
        total_seconds = difference.total_seconds()
        print("Server was down for ",total_seconds, ' seconds')
        logging.warning("Server was down for {0:f}s".format(total_seconds))
