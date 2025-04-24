from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World! The minimal app is working."

@app.route('/info')
def info():
    import sys
    import os
    
    return jsonify({
        "python_version": sys.version,
        "working": True,
        "env_count": len(os.environ)
    })

# Required for Vercel
from http.server import BaseHTTPRequestHandler

# Vercel serverless function handler
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run(debug=True) 