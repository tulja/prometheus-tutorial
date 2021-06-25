import http.server
import random
import time
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge


REQUESTS = Counter('hello_worlds_total','Hello Worlds requested.')
INPROGRESS = Gauge('hello_worlds_inprogress', 'Number of Hello Worlds in progress.')


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
    	start = time.time()
    	INPROGRESS.inc()
    	REQUESTS.inc()
    	self.send_response(200)
    	self.end_headers()
    	self.wfile.write(b"Hello World")
    	INPROGRESS.dec()


if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()