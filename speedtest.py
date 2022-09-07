import json
import subprocess
from time import sleep
from prometheus_client import Gauge, start_http_server

# Init prometheus server to post metrics
start_http_server(9191)

# Init prometheus gauges for each data point
prom_latency = Gauge('speedtest_latency', 'Latency of the connection to the test server')
prom_download = Gauge('speedtest_download', 'Download speed in bytes of the internet connection')
prom_upload = Gauge('speedtest_upload', 'Upload speed in bytes of the internet connection')

while True:
    
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