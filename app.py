from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import traceback
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Determine if we're in production (Vercel deployment)
is_production = os.environ.get('VERCEL', False)

# Get Supabase info for both db connection and diagnostics
supabase_url = os.getenv('SUPABASE_URL', '')
supabase_key = os.getenv('SUPABASE_KEY', '')
project_id = supabase_url.replace('https://', '').split('.')[0] if supabase_url else ''

# Set the database URI based on environment
if is_production:
    # For production, we'll use SQLite as a placeholder but not actually use it
    # Instead, we'll use Supabase REST API for database operations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    print(f"Environment: Production (Using Supabase REST API)")
else:
    # Use SQLite for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
    print("Environment: Development (SQLite)")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Models for SQLite (local development)
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    event_link = db.Column(db.String(500), nullable=False)
    tags = db.Column(db.String(500), nullable=False)
    is_starred = db.Column(db.Boolean, default=False)

# Supabase API helper functions
def supabase_insert(table, data):
    """Insert data into Supabase using REST API"""
    if not is_production:
        return None
    
    # Use service role key for bypassing RLS
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    # Direct insert bypassing RLS using service role
    url = f"{supabase_url}/rest/v1/{table}"
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code not in (200, 201):
        # Print detailed error info
        print(f"Supabase API Error: {response.status_code} - {response.text}")
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Data: {data}")
        raise Exception(f"Supabase API Error: {response.status_code} - {response.text}")
    
    return response.json()

def supabase_select(table, query_params=None):
    """Select data from Supabase using REST API"""
    if not is_production:
        return None
    
    # Use service role key for bypassing RLS
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}"
    }
    
    url = f"{supabase_url}/rest/v1/{table}"
    response = requests.get(url, headers=headers, params=query_params)
    
    if response.status_code != 200:
        print(f"Supabase API Error: {response.status_code} - {response.text}")
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Params: {query_params}")
        raise Exception(f"Supabase API Error: {response.status_code} - {response.text}")
    
    return response.json()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salons')
def salons():
    return render_template('salons.html')

@app.route('/salon')
def salon():
    return redirect(url_for('salons'))

@app.route('/submit', methods=['GET', 'POST'])
def submit_event():
    if request.method == 'POST':
        try:
            # Format date for API
            start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
            start_time_iso = start_time.isoformat()
            
            # Prepare event data
            event_data = {
                "title": request.form['title'],
                "start_time": start_time_iso,
                "location": request.form['location'],
                "description": request.form['description'],
                "image_url": request.form['image_url'],
                "event_link": request.form['event_link'],
                "tags": ','.join(request.form.getlist('tags')),
                "is_starred": False
            }
            
            print(f"Attempting to insert event: {event_data}")
            
            if is_production:
                # Use Supabase REST API in production
                result = supabase_insert("events", event_data)
                print(f"Insert successful: {result}")
            else:
                # Use SQLAlchemy in development
                event = Event(
                    title=request.form['title'],
                    start_time=start_time,
                    location=request.form['location'],
                    description=request.form['description'],
                    image_url=request.form['image_url'],
                    event_link=request.form['event_link'],
                    tags=','.join(request.form.getlist('tags'))
                )
                db.session.add(event)
                db.session.commit()
                
            return redirect(url_for('index'))
        except Exception as e:
            # Log the error with traceback for better debugging
            error_traceback = traceback.format_exc()
            print(f"Error submitting event: {str(e)}\n{error_traceback}")
            
            # Return a more helpful error page
            return render_template('error.html', error=f"{str(e)}\n\nTraceback:\n{error_traceback}"), 500
    return render_template('submit.html')

@app.route('/api/events')
def get_events():
    tag = request.args.get('tag')
    
    try:
        if is_production:
            # Use Supabase REST API in production
            now = datetime.now().isoformat()
            query_params = {
                "select": "*",
                "start_time": f"gte.{now}",
                "order": "start_time"
            }
            
            if tag:
                # Filter by tag - use cs (contains) for comma-separated values
                query_params["tags"] = f"cs.{tag}"
                
            events_data = supabase_select("events", query_params)
            
            # Format the response
            return jsonify([{
                'id': event['id'],
                'title': event['title'],
                'start_time': event['start_time'],
                'location': event['location'],
                'description': event['description'],
                'image_url': event['image_url'],
                'event_link': event['event_link'],
                'tags': event['tags'].split(',') if event['tags'] else [],
                'is_starred': event['is_starred']
            } for event in events_data])
        else:
            # Use SQLAlchemy in development
            query = Event.query.filter(Event.start_time >= datetime.now())
            
            if tag:
                # Ensure proper tag filtering for SQLite
                # For comma-separated tags, we need to use LIKE with wildcards
                tag_pattern = f"%{tag}%"
                query = query.filter(Event.tags.like(tag_pattern))
                
            events = query.order_by(Event.start_time).all()
            
            # Log the SQL query for debugging
            print(f"SQL Query: {str(query)}")
            print(f"Events found: {len(events)}")
            
            return jsonify([{
                'id': event.id,
                'title': event.title,
                'start_time': event.start_time.isoformat(),
                'location': event.location,
                'description': event.description,
                'image_url': event.image_url,
                'event_link': event.event_link,
                'tags': event.tags.split(',') if event.tags else [],
                'is_starred': event.is_starred
            } for event in events])
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Error fetching events: {str(e)}\n{error_traceback}")
        return jsonify({"error": str(e), "traceback": error_traceback}), 500

# Add a diagnostic route to check Supabase API connection
@app.route('/api-test')
def api_test():
    try:
        # Test Supabase API connection
        headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}"
        }
        
        url = f"{supabase_url}/rest/v1/events?limit=1"
        response = requests.get(url, headers=headers)
        
        status_code = response.status_code
        
        # Test table creation permission
        create_test = None
        create_error = None
        try:
            test_headers = {
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            test_url = f"{supabase_url}/rest/v1/events"
            test_data = {"title": "API Test", "start_time": datetime.now().isoformat(), 
                        "location": "Test", "description": "Test", "image_url": "https://example.com/test.jpg",
                        "event_link": "https://example.com", "tags": "test"}
            test_response = requests.post(test_url, headers=test_headers, data=json.dumps(test_data))
            create_test = {
                "status_code": test_response.status_code,
                "response": test_response.text
            }
        except Exception as e:
            create_error = str(e)
        
        return jsonify({
            "status": "success" if status_code == 200 else "error",
            "status_code": status_code,
            "message": "Supabase API connection successful" if status_code == 200 else f"Error: {response.text}",
            "create_test": create_test,
            "create_error": create_error,
            "config": {
                "supabase_url": supabase_url,
                "is_production": is_production,
                "project_id": project_id
            }
        })
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"API connection error: {str(e)}\n{error_traceback}")
        return jsonify({
            "status": "error", 
            "message": str(e),
            "traceback": error_traceback,
            "config": {
                "supabase_url": supabase_url,
                "is_production": is_production,
                "project_id": project_id
            }
        }), 500

# Redirect for static files
@app.route('/salons.html')
def salons_static():
    return redirect(url_for('salons'))

@app.route('/submit.html')
def submit_static():
    return redirect(url_for('submit_event'))

# For Vercel deployment
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False) 

