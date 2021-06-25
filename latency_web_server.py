import http.server
import random
import time
from prometheus_client import Gauge
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Summary

REQUESTS = Counter('hello_worlds_total','Hello Worlds requested.')
INPROGRESS = Gauge('hello_worlds_inprogress', 'Number of Hello Worlds in progress.')
LATENCY = Summary('hello_world_latency_seconds','Time for a request Hello World.')
LAST = Gauge('hello_world_last_time_seconds', 'The last time a Hello World was served.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
    	start = time.time()
    	INPROGRESS.inc()
    	REQUESTS.inc()
    	self.send_response(200)
    	self.end_headers()
    	self.wfile.write(b"Hello World")
    	LAST.set(time.time())
    	INPROGRESS.dec()
    	LATENCY.observe(time.time() - start)
    

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()
