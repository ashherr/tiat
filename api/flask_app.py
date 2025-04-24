from flask import Flask, Response, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    try:
        # Attempt to render templates if the path matches a route
        if path == '' or path == 'index':
            return render_template('index.html')
        elif path == 'salons':
            return render_template('salons.html')
        elif path == 'submit':
            return render_template('submit.html')
        else:
            # Return a simple text response if template doesn't exist
            return Response(f"TIAT Flask App - Path: /{path}", mimetype="text/plain")
    except Exception as e:
        # If template rendering fails, return error as text
        return Response(f"Error: {str(e)}", mimetype="text/plain")

# API route to return sample events
@app.route('/api/events')
def events():
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

# For Vercel serverless function
def handler(event, context):
    return app(event, context) 