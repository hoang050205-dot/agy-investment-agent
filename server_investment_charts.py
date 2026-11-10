"""
Local HTTP Server for Investment Interactive Charts (Port 8888)
Serves files from outputs/investment:
- http://localhost:8888/chart_scenario_VND.html
- http://localhost:8888/chart_scenario_interactive_MASTER.html
- http://localhost:8888/ (redirects to VND interactive chart)
"""

import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8888
# Robust directory resolution: works whether executed from root or inside outputs/investment
_curr = os.path.abspath(os.path.dirname(__file__))
if os.path.basename(_curr).lower() == "investment":
    SERVE_DIR = _curr
else:
    SERVE_DIR = os.path.abspath(os.path.join(_curr, "outputs", "investment"))

class ChartHTTPHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)

    def do_GET(self):
        # Default root redirect to VND chart
        if self.path in ["/", "/index.html"]:
            self.send_response(302)
            self.send_header("Location", "/chart_scenario_VND.html")
            self.end_headers()
            return
        return super().do_GET()

    def end_headers(self):
        # Enable CORS and disable cache for smooth dev experience
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        # Suppress noisy request logs
        sys.stderr.write(f"[{self.log_date_time_string()}] {args[0]}\n")

def run():
    os.chdir(SERVE_DIR)
    server_address = ("127.0.0.1", PORT)
    try:
        httpd = HTTPServer(server_address, ChartHTTPHandler)
        print(f"[SUCCESS] Investment Chart Server running at: http://localhost:{PORT}/")
        print(f"  • VND Chart:    http://localhost:{PORT}/chart_scenario_VND.html")
        print(f"  • Master Chart: http://localhost:{PORT}/chart_scenario_interactive_MASTER.html")
        sys.stdout.flush()
        httpd.serve_forever()
    except OSError as e:
        if e.errno == 10048: # Port already in use
            print(f"[INFO] Port {PORT} is already in use by an active server. Ready to serve!")
        else:
            raise

if __name__ == "__main__":
    run()

