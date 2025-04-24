from http.server import BaseHTTPRequestHandler
import json
import sys
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Collect status information
        status_info = {
            "status": "online",
            "python_version": sys.version,
            "env_vars_count": len(os.environ),
            "flask_app_enabled": True,
            "templates_directory": os.path.exists("templates"),
            "static_directory": os.path.exists("static")
        }
        
        self.wfile.write(json.dumps(status_info, indent=2).encode())
        return 