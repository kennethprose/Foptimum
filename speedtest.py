import json
import subprocess


# Run speedtest
# Specify json output
# Pipe output of subprocess to variable
speedtest_results = subprocess.Popen(['speedtest.exe', '-f', 'json'], stdout=subprocess.PIPE).communicate()[0]
json_results = json.loads(speedtest_results)

# Scrape relevant data
avg_latency = json_results['ping']['latency']
download_speed = json_results['download']['bandwidth']
upload_speed = json_results['upload']['bandwidth']
packet_loss = json_results['packetLoss']