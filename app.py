from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime, timedelta
import os
import traceback
import requests
import json
import sys
from dotenv import load_dotenv
# Import Google Calendar integration
import gcal_integration

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

# Print environment info for debugging
print(f"Python version: {sys.version}")
print(f"Environment variables: {list(os.environ.keys())}")
print(f"ENABLE_GCAL set to: {os.getenv('ENABLE_GCAL')}")
print(f"GOOGLE_CALENDAR_ID set to: {os.getenv('GOOGLE_CALENDAR_ID', 'Not set')}")
print(f"GOOGLE_SERVICE_ACCOUNT_EMAIL present: {'Yes' if os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL') else 'No'}")

# Set the database URI based on environment
if is_production:
    # For production, we'll use SQLite as a placeholder but not actually use it
    # Instead, we'll use Supabase REST API for database operations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    print(f"Environment: Production (Using Supabase REST API)")
else:
    # Use SQLite for local development with explicit path to the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/events.db'
    print(f"Environment: Development (SQLite - Database Path: {app.config['SQLALCHEMY_DATABASE_URI']})")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Models for SQLite (local development)
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)  # Changed to nullable=False
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    event_link = db.Column(db.String(500), nullable=False)
    tags = db.Column(db.String(500), nullable=False)
    is_starred = db.Column(db.Boolean, default=False)
    organizer_email = db.Column(db.String(200), nullable=False)  # Changed to nullable=False
    calendar_event_id = db.Column(db.String(200), nullable=True)  # New field to store Google Calendar event ID

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
    
    # Print detailed request info for debugging
    print(f"Supabase Request URL: {url}")
    print(f"Supabase Request Headers: {headers}")
    print(f"Supabase Request Params: {query_params}")
    
    response = requests.get(url, headers=headers, params=query_params)
    
    # Print response status and headers for debugging
    print(f"Supabase Response Status: {response.status_code}")
    print(f"Supabase Response Headers: {response.headers}")
    
    if response.status_code != 200:
        print(f"Supabase API Error: {response.status_code} - {response.text}")
        raise Exception(f"Supabase API Error: {response.status_code} - {response.text}")
    
    try:
        data = response.json()
        print(f"Supabase Response Data Count: {len(data)}")
        return data
    except Exception as e:
        print(f"Error parsing Supabase response: {str(e)}")
        print(f"Response Content: {response.text[:200]}...")  # Show first 200 chars
        raise Exception(f"Error parsing Supabase response: {str(e)}")

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

@app.route('/calendar')
def calendar():
    """Show calendar subscription information."""
    try:
        calendar_info = gcal_integration.get_calendar_info()
        
        return render_template('calendar.html',
                            calendar_id=calendar_info['calendar_id'],
                            google_url=calendar_info['html_link'],
                            ical_url=calendar_info['ical_url'],
                            embed_html=calendar_info['embed_html'])
    except Exception as e:
        print(f"Error loading calendar info: {str(e)}")
        # Return an error page instead of crashing
        return render_template('error.html', 
                              error="Calendar integration is currently unavailable", 
                              description="Please try again later or contact the administrator.")

@app.route('/submit', methods=['GET', 'POST'])
def submit_event():
    if request.method == 'POST':
        try:
            # Format date for API
            start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
            start_time_iso = start_time.isoformat()
            
            # Handle end time - now required
            end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
            end_time_iso = end_time.isoformat()
            
            # Prepare event data
            event_data = {
                "title": request.form['title'],
                "start_time": start_time_iso,
                "end_time": end_time_iso,
                "location": request.form['location'],
                "description": request.form['description'],
                "image_url": request.form['image_url'],
                "event_link": request.form['event_link'],
                "tags": ','.join(request.form.getlist('tags')),
                "is_starred": False,
                "organizer_email": request.form['organizer_email']  # Now required field
            }
            
            print(f"Attempting to insert event: {event_data}")
            
            # Add to Google Calendar if enabled
            calendar_event_id = None
            if os.getenv('ENABLE_GCAL', 'false').lower() == 'true':
                try:
                    print("Adding event to Google Calendar...")
                    calendar_event_id = gcal_integration.add_event_to_calendar(event_data)
                    if calendar_event_id:
                        event_data["calendar_event_id"] = calendar_event_id
                        print(f"Event added to Google Calendar with ID: {calendar_event_id}")
                    else:
                        print("Failed to add event to Google Calendar")
                except Exception as cal_error:
                    print(f"Error adding to Google Calendar: {str(cal_error)}")
                    # Continue with submission even if calendar fails
            
            if is_production:
                # Use Supabase REST API in production
                result = supabase_insert("events", event_data)
                print(f"Insert successful: {result}")
            else:
                # Use SQLAlchemy in development
                event = Event(
                    title=request.form['title'],
                    start_time=start_time,
                    end_time=end_time,
                    location=request.form['location'],
                    description=request.form['description'],
                    image_url=request.form['image_url'],
                    event_link=request.form['event_link'],
                    tags=','.join(request.form.getlist('tags')),
                    organizer_email=request.form['organizer_email'], # Now directly use required field
                    calendar_event_id=calendar_event_id
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
            
            # Print for debugging
            print(f"Production API call - filtering by tag: '{tag}'")
            print(f"Using Supabase URL: {supabase_url}")
            
            # Basic query parameters
            query_params = {
                "select": "*",
                "start_time": f"gte.{now}",
                "order": "start_time"
            }
            
            if tag:
                # Simply use the tag as provided in Supabase query
                # For Supabase, the correct format for filtering on a comma-separated list is ilike
                query_params["tags"] = f"ilike.%{tag}%"
                print(f"Supabase query params: {query_params}")
            
            try:
                events_data = supabase_select("events", query_params)
                print(f"Supabase returned {len(events_data)} events")
                
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
            except Exception as supabase_error:
                print(f"Supabase API error: {str(supabase_error)}")
                # Fallback: return empty list instead of error
                print("Returning empty list as fallback")
                return jsonify([])
        else:
            # Use SQLAlchemy in development
            query = Event.query.filter(Event.start_time >= datetime.now())
            
            if tag:
                # Print for debugging
                print(f"Filtering by tag: '{tag}'")
                
                # For SQLite, simple pattern matching should work
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
        # Return empty list instead of error for better user experience
        return jsonify([]), 200

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

# Add a global error handler
@app.errorhandler(500)
def server_error(e):
    error_traceback = traceback.format_exc()
    print(f"500 error: {str(e)}\n{error_traceback}")
    return render_template('error.html', 
                          error="Internal Server Error", 
                          description="The server encountered an internal error. Please try accessing /debug for more information."), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', 
                          error="Page Not Found", 
                          description="The requested page does not exist."), 404

# Fallback index route for when other routes fail
@app.route('/minimal-index')
def minimal_index():
    """Minimal index page that doesn't rely on database or external services"""
    return """
    <html><body>
    <h1>TIAT Minimal Mode</h1>
    <p>The site is running in minimal mode due to configuration issues.</p>
    <p><a href="/debug">View debug information</a></p>
    </body></html>
    """

# Redirect for static files
@app.route('/salons.html')
def salons_static():
    return redirect(url_for('salons'))

@app.route('/submit.html')
def submit_static():
    return redirect(url_for('submit_event'))

# Add a debug route for Vercel troubleshooting
@app.route('/debug')
def debug():
    """Route to help debug Vercel deployment issues"""
    env_vars = {k: (v if not k.lower().startswith('google_service_account_private') else '[REDACTED]') 
               for k, v in os.environ.items()}
    
    # Test Google Calendar credentials separately
    gcal_test = None
    gcal_error = None
    try:
        if os.getenv('ENABLE_GCAL', 'false').lower() == 'true':
            service = gcal_integration.create_service()
            if service:
                gcal_test = "Google Calendar service created successfully"
            else:
                gcal_test = "Failed to create Google Calendar service"
        else:
            gcal_test = "Google Calendar integration is disabled"
    except Exception as e:
        gcal_error = f"Error testing Google Calendar integration: {str(e)}"
    
    # Test Supabase connectivity
    supabase_test = None
    supabase_error = None
    try:
        if is_production:
            headers = {
                "apikey": supabase_key,
                "Authorization": f"Bearer {supabase_key}"
            }
            url = f"{supabase_url}/rest/v1/events?limit=1"
            response = requests.get(url, headers=headers)
            supabase_test = f"Supabase API response: {response.status_code}"
        else:
            supabase_test = "Not in production, Supabase not tested"
    except Exception as e:
        supabase_error = f"Error testing Supabase connection: {str(e)}"
    
    return jsonify({
        "environment": "Production" if is_production else "Development",
        "python_version": sys.version,
        "available_env_vars": list(env_vars.keys()),
        "key_env_vars": {
            "ENABLE_GCAL": os.getenv('ENABLE_GCAL'),
            "GOOGLE_CALENDAR_ID": os.getenv('GOOGLE_CALENDAR_ID'),
            "GOOGLE_SERVICE_ACCOUNT_EMAIL": os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL'),
            "SUPABASE_URL": supabase_url,
            "Project ID": project_id,
        },
        "gcal_test": gcal_test,
        "gcal_error": gcal_error,
        "supabase_test": supabase_test,
        "supabase_error": supabase_error
    })

# For Vercel deployment
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run the Bay Area Creative Tech Events app')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the app on')
    args = parser.parse_args()
    
    with app.app_context():
        db.create_all()
    app.run(debug=False, port=args.port) 

