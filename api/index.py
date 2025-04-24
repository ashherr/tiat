from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Redirect to main page
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()
        return 