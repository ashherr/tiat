from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import traceback
import sys

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Determine if we're in production (Vercel deployment)
is_production = os.environ.get('VERCEL', False)

# Set the database URI based on environment
if is_production:
    # For production we'll use SQLite in memory
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    print(f"Environment: Production (Using in-memory SQLite)")
else:
    # Use SQLite for local development with explicit path to the database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/events.db'
    print(f"Environment: Development (SQLite - Database Path: {app.config['SQLALCHEMY_DATABASE_URI']})")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Models for SQLite
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    event_link = db.Column(db.String(500), nullable=False)
    tags = db.Column(db.String(500), nullable=False)
    is_starred = db.Column(db.Boolean, default=False)
    organizer_email = db.Column(db.String(200), nullable=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salons')
def salons():
    return render_template('salons.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit_event():
    if request.method == 'POST':
        try:
            # Format date for API
            start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
            
            # In production, just return a success message for now
            if is_production:
                return render_template('error.html', 
                                      error="Success! (Test Mode)", 
                                      description="The event submission feature is currently in test mode. Your event was not actually saved.")
            
            # For local development, save to SQLite
            event = Event(
                title=request.form['title'],
                start_time=start_time,
                end_time=end_time,
                location=request.form['location'],
                description=request.form['description'],
                image_url=request.form['image_url'],
                event_link=request.form['event_link'],
                tags=','.join(request.form.getlist('tags')),
                organizer_email=request.form['organizer_email']
            )
            db.session.add(event)
            db.session.commit()
                
            return redirect(url_for('index'))
        except Exception as e:
            error_traceback = traceback.format_exc()
            print(f"Error submitting event: {str(e)}\n{error_traceback}")
            return render_template('error.html', 
                                 error="Error Submitting Event", 
                                 description=f"There was an error processing your submission: {str(e)}")
    return render_template('submit.html')

@app.route('/api/events')
def get_events():
    try:
        if is_production:
            # Return sample data in production for now
            sample_events = [{
                'id': 1,
                'title': 'Sample Event',
                'start_time': datetime.now().isoformat(),
                'location': 'San Francisco',
                'description': 'This is a sample event for testing.',
                'image_url': 'https://via.placeholder.com/300',
                'event_link': 'https://example.com',
                'tags': ['art', 'tech'],
                'is_starred': False
            }]
            return jsonify(sample_events)
        else:
            # Use SQLAlchemy in development
            events = Event.query.filter(Event.start_time >= datetime.now()).order_by(Event.start_time).all()
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
        print(f"Error fetching events: {str(e)}")
        # Return empty list instead of error for better user experience
        return jsonify([]), 200

# Add a debug route
@app.route('/debug')
def debug():
    env_vars = {k: ("REDACTED" if k.lower().startswith(('key', 'secret', 'password', 'token')) else v) 
               for k, v in os.environ.items()}
    
    return jsonify({
        "environment": "Production" if is_production else "Development",
        "python_version": sys.version,
        "available_env_vars": list(env_vars.keys()),
        "env_vars_sample": env_vars
    })

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

# For Vercel deployment
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000) 