from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>TIAT Recovery Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                .container { max-width: 800px; margin: 0 auto; }
                .status { padding: 20px; background-color: #f0f0f0; border-radius: 5px; }
                .success { background-color: #d4edda; color: #155724; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>TIAT Recovery Page</h1>
                <div class="status success">
                    <h2>Server Status: Online</h2>
                    <p>This minimal page is working. The Vercel function is responding correctly.</p>
                </div>
                <div>
                    <h2>Next Steps</h2>
                    <p>Once this page loads successfully, you can begin restoring the full application.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())
        return 