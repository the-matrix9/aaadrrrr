from http.server import BaseHTTPRequestHandler
import requests
import urllib.parse

API_KEY = "@DARKxERA"
BASE_URL = "http://167.71.235.17:3000/search-aadhaar"


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        key = params.get("key", [None])[0]
        name = params.get("name", [None])[0]
        aadhaar = params.get("aadhaar", [None])[0]

        # API key check
        if key != API_KEY:
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"success":false,"message":"Invalid API key"}')
            return

        if not name or not aadhaar:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"success":false,"message":"Missing params"}')
            return

        try:
            r = requests.get(
                BASE_URL,
                params={"search": name, "aadhaar": aadhaar},
                timeout=25
            )

            # 🔥 ORIGINAL JSON EXACT forward
            self.send_response(r.status_code)
            self.send_header(
                "Content-Type",
                r.headers.get("Content-Type", "application/json")
            )
            self.end_headers()
            self.wfile.write(r.content)

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(str(e).encode())
