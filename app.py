from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import traceback
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
project_id = supabase_url.replace('https://', '').split('.')[0] if supabase_url else ''

# Set the database URI based on environment
if is_production:
    # For Vercel deployment with Supabase PostgreSQL
    # Use direct connection to the Supabase PostgreSQL database
    db_password = os.getenv('SUPABASE_KEY', '')
    
    # Construct PostgreSQL connection string for Supabase
    # Format: postgresql://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres
    db_url = f"postgresql://postgres:{db_password}@db.{project_id}.supabase.co:5432/postgres"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    
    # Log connection info (without password) for debugging
    print(f"Connecting to Supabase PostgreSQL: db.{project_id}.supabase.co:5432/postgres")
    print(f"Project ID: {project_id}")
    print(f"Environment: Production")
else:
    # Use SQLite for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
    print("Environment: Development (SQLite)")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Models
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
            event = Event(
                title=request.form['title'],
                start_time=datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M'),
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
        query = Event.query.filter(Event.start_time >= datetime.now())
        if tag:
            query = query.filter(Event.tags.contains(tag))
        events = query.order_by(Event.start_time).all()
        
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

# Add a diagnostic route to check database connection
@app.route('/db-test')
def db_test():
    try:
        # Try to make a simple query to test the database connection
        db.session.execute("SELECT 1").fetchone()
        return jsonify({
            "status": "success", 
            "message": "Database connection successful",
            "config": {
                "db_host": f"db.{project_id}.supabase.co" if is_production else "sqlite",
                "is_production": is_production,
                "project_id": project_id
            }
        })
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Database connection error: {str(e)}\n{error_traceback}")
        return jsonify({
            "status": "error", 
            "message": str(e),
            "traceback": error_traceback,
            "config": {
                "db_host": f"db.{project_id}.supabase.co" if is_production else "sqlite",
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

