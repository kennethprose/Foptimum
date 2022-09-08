import json
import subprocess
import threading
from time import sleep
from configparser import ConfigParser
from prometheus_client import Gauge, Counter, start_http_server

config = ConfigParser()
config.read('config.ini')

server_port = int(config['DEFAULT']['Server_Port'])
speedtest_interval = int(config['DEFAULT']['Speedtest_Interval'])
ping_interval = int(config['DEFAULT']['Ping_Interval'])
server_list = config['DEFAULT']['Server_List'].split(',')

# Init prometheus server to post metrics
start_http_server(server_port)

# Init prometheus gauges for each data point
prom_latency = Gauge('speedtest_latency', 'Latency of the connection to the test server')
prom_download = Gauge('speedtest_download', 'Download speed in bytes of the internet connection')
prom_upload = Gauge('speedtest_upload', 'Upload speed in bytes of the internet connection')
prom_ping_success = Counter('ping_success', 'Number of successful pings')
prom_ping_fails = Counter('ping_fails', 'Number of failed pings')


def speedtest():

    global kill_threads

    while not kill_threads:
        
        # Run speedtest
        # Specify json output
        # Pipe output of subprocess to variable
        speedtest_results = subprocess.Popen(['speedtest.exe', '-f', 'json'], stdout=subprocess.PIPE).communicate()[0]
        json_results = json.loads(speedtest_results)

        # Scrape and post relevant data
        prom_latency.set(json_results['ping']['latency'])
        prom_download.set(json_results['download']['bandwidth'])
        prom_upload.set(json_results['upload']['bandwidth'])

        sleep(speedtest_interval)


def ping_test():

    global kill_threads

    while not kill_threads:

        for server in server_list:

            # Send a single ping to the current server and capture result by piping output
            ping_result = subprocess.Popen(['ping', '/n', '1', server], stdout=subprocess.PIPE).communicate()[0]
            
            if 'Received = 1' in str(ping_result):
                prom_ping_success.inc()
            else:
                prom_ping_fails.inc()

        sleep(ping_interval)


ping_thread = threading.Thread(target=ping_test)
speedtest_thread = threading.Thread(target=speedtest)

kill_threads = False

ping_thread.start()
speedtest_thread.start()

# Used to detect CTRL-C and terminate the threads
try:
    while True:
        pass
except KeyboardInterrupt:
    kill_threads = True

ping_thread.join()
speedtest_thread.join()