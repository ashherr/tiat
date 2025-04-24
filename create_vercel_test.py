from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    """Simple test endpoint that doesn't rely on any external services"""
    return """
    <html>
    <head>
        <title>Vercel Test - TIAT</title>
        <style>
            body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        </style>
    </head>
    <body>
        <h1>TIAT Vercel Test</h1>
        <p>If you're seeing this, the basic Vercel deployment is working correctly.</p>
        <p>This is a simple test route that doesn't use any database connections, Google API credentials or other services.</p>
        <p>Once you get this working, you can configure the remaining environment variables for the main app.</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True) 