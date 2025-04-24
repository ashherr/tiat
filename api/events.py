from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Sample events data
        events = [
            {
                'id': 1,
                'title': 'Gray Area Festival',
                'start_time': '2023-10-20T10:00:00',
                'end_time': '2023-10-22T18:00:00',
                'location': 'San Francisco',
                'description': 'Annual festival of art, technology, and culture featuring performances, installations, and talks.',
                'image_url': 'https://via.placeholder.com/300',
                'event_link': 'https://grayarea.org',
                'tags': ['festival', 'art', 'tech'],
                'is_starred': True
            },
            {
                'id': 2,
                'title': 'Digital Art Exhibition',
                'start_time': '2023-11-05T09:00:00',
                'end_time': '2023-11-05T17:00:00',
                'location': 'San Jose',
                'description': 'Exhibition showcasing works from digital artists pushing the boundaries of technology in art.',
                'image_url': 'https://via.placeholder.com/300',
                'event_link': 'https://example.com/digital-art',
                'tags': ['exhibition', 'digital-art'],
                'is_starred': False
            },
            {
                'id': 3,
                'title': 'Creative Coding Workshop',
                'start_time': '2023-11-12T13:00:00',
                'end_time': '2023-11-12T16:00:00',
                'location': 'Berkeley',
                'description': 'Learn the basics of creative coding with p5.js in this beginner-friendly workshop.',
                'image_url': 'https://via.placeholder.com/300',
                'event_link': 'https://example.com/coding-workshop',
                'tags': ['workshop', 'coding', 'p5js'],
                'is_starred': False
            }
        ]
        
        # Filter by tag if provided in query string
        tag = None
        if '?' in self.path:
            query = self.path.split('?')[1]
            params = query.split('&')
            for param in params:
                if param.startswith('tag='):
                    tag = param.split('=')[1]
        
        if tag:
            filtered_events = [event for event in events if tag in event['tags']]
        else:
            filtered_events = events
        
        self.wfile.write(json.dumps(filtered_events).encode()) 