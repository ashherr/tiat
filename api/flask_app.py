from flask import Flask, Response, jsonify
import os
import sys
import json

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        # Simplified text response instead of template rendering
        if path == '':
            return Response("TIAT - Home Page (Recovery Mode)", mimetype="text/html")
        elif path == 'salons':
            return Response("TIAT - Salons Page (Recovery Mode)", mimetype="text/html")
        elif path == 'submit':
            return Response("TIAT - Submit Event Page (Recovery Mode)", mimetype="text/html")
        else:
            return Response(f"TIAT - Unknown Page: /{path} (Recovery Mode)", mimetype="text/html")
    except Exception as e:
        # Return error as text
        return Response(f"Error: {str(e)}", mimetype="text/plain")

# API route to return system info for debugging
@app.route('/debug')
def debug():
    try:
        info = {
            'python_version': sys.version,
            'env_vars': list(os.environ.keys()),
            'app_name': 'TIAT',
            'mode': 'Recovery'
        }
        return jsonify(info)
    except Exception as e:
        return Response(f"Debug Error: {str(e)}", mimetype="text/plain")

# API route to return sample events
@app.route('/api/events')
def events():
    try:
        sample_events = [{
            'id': 1,
            'title': 'Sample Event',
            'start_time': '2023-10-15T18:00:00',
            'location': 'San Francisco',
            'description': 'This is a sample event for testing.',
            'image_url': 'https://via.placeholder.com/300',
            'event_link': 'https://example.com',
            'tags': ['art', 'tech'],
            'is_starred': False
        }]
        return jsonify(sample_events)
    except Exception as e:
        return Response(f"Events API Error: {str(e)}", mimetype="text/plain")

def handler(event, context):
    return app(event, context) 