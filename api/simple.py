from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip('/')
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TIAT - Ultra Minimal</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1 {{ color: #333; }}
                .notice {{ background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .success {{ background-color: #d4edda; color: #155724; }}
                nav {{ margin: 20px 0; }}
                nav a {{ margin-right: 15px; text-decoration: none; padding: 5px 10px; background: #f1f1f1; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <h1>TIAT - Ultra Minimal Recovery</h1>
            
            <div class="notice success">
                <strong>Working!</strong> The site is now responding in ultra-minimal mode.
                <p>Current path: /{path}</p>
            </div>
            
            <nav>
                <a href="/">Home</a>
                <a href="/salons">Salons</a>
                <a href="/submit">Submit</a>
                <a href="/status">Status</a>
                <a href="/recovery">Recovery</a>
            </nav>
            
            <div>
                <h2>Next Steps</h2>
                <p>This ultra-minimal version is working! You can now gradually restore functionality.</p>
            </div>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())
        return 