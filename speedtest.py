import json
import subprocess
import threading
from time import sleep
from prometheus_client import Gauge, Counter, start_http_server

# Init prometheus server to post metrics
start_http_server(9191)

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

        sleep(60)


def ping_test(servers):

    global kill_threads

    while not kill_threads:

        for server in servers:

            # Send a single ping to the current server and capture result by piping output
            ping_result = subprocess.Popen(['ping', '/n', '1', server], stdout=subprocess.PIPE).communicate()[0]
            
            if 'Received = 1' in str(ping_result):
                prom_ping_success.inc()
            else:
                prom_ping_fails.inc()

        sleep(10)


ping_thread = threading.Thread(target=ping_test, args=(['1.1.1.1','8.8.8.8'],))
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