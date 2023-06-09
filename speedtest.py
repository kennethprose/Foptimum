import json
import os
import subprocess
import threading
import logging
from time import sleep
from prometheus_client import Gauge, Counter, start_http_server

logging.basicConfig(filename='app.log',
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Read environment variables to get settings
speedtest_interval = int(os.environ['SPEEDTEST_INTERVAL'])
ping_interval = int(os.environ['PING_INTERVAL'])
server_list = os.environ['SERVER_LIST'].split(',')

# Init prometheus server to post metrics
start_http_server(9191)

# Init prometheus gauges for each data point
prom_latency = Gauge('speedtest_latency',
                     'Latency of the connection to the test server')
prom_download = Gauge('speedtest_download',
                      'Download speed in bytes of the internet connection')
prom_upload = Gauge('speedtest_upload',
                    'Upload speed in bytes of the internet connection')
prom_ping_currently_failing = Gauge(
    'ping_currently_failing', 'A true/false value. True when pings are currently in a failing state')
prom_ping_success = Counter('ping_success', 'Number of successful pings')
prom_ping_fails = Counter('ping_fails', 'Number of failed pings')


def speedtest():

    while True:

        # Run speedtest
        # Specify json output
        # Pipe output of subprocess to variable
        speedtest_results = subprocess.Popen(
            ['./speedtest', "--accept-license", "--accept-gdpr", '-f', 'json'], stdout=subprocess.PIPE).communicate()[0]

        if str(speedtest_results) != "b''":

            json_results = json.loads(speedtest_results)

            # Scrape and post relevant data
            prom_latency.set(json_results['ping']['latency'])
            prom_download.set(json_results['download']['bandwidth'])
            prom_upload.set(json_results['upload']['bandwidth'])

        else:

            prom_latency.set('0')
            prom_download.set('0')
            prom_upload.set('0')

            logging.warning('Speed test failed')

        sleep(speedtest_interval)


def ping_test():

    prom_ping_currently_failing.set(0)

    while True:

        for server in server_list:

            # Send a single ping to the current server and capture result by piping output
            ping_result = subprocess.Popen(
                ['ping', '-c', '1', server], stdout=subprocess.PIPE).communicate()[0]

            if ' 0% packet loss' in str(ping_result):
                prom_ping_success.inc()
                prom_ping_currently_failing.set(0)
            else:
                prom_ping_fails.inc()
                prom_ping_currently_failing.set(1)
                logging.warning(server + ' ping failed')

        sleep(ping_interval)


ping_thread = threading.Thread(target=ping_test)
speedtest_thread = threading.Thread(target=speedtest)

ping_thread.start()
speedtest_thread.start()

ping_thread.join()
speedtest_thread.join()
