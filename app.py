from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Determine if we're in production (Vercel deployment)
is_production = os.environ.get('VERCEL', False)

# Set the database URI based on environment
if is_production:
    # For Vercel deployment with Supabase PostgreSQL
    # The direct connection string approach wasn't working due to socket issues
    # Instead, use a connection string that works with Vercel and Supabase
    supabase_url = os.getenv('SUPABASE_URL', '').replace('https://', '')
    db_password = os.getenv('SUPABASE_KEY', '')
    
    # Connection string format for Supabase from Vercel
    # Use the hostname without db. prefix to avoid socket address family issues
    # Separate the project ID from the hostname
    project_id = supabase_url.split('.')[0]
    
    # PostgreSQL connection string for Supabase
    db_url = f"postgresql://postgres:{db_password}@aws-0-{os.getenv('VERCEL_REGION', 'us-east-1')}.pooler.supabase.com:5432/postgres"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    # Use SQLite for local development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'

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
            # Log the error (in production this would go to your logging system)
            print(f"Error submitting event: {str(e)}")
            # Return a more helpful error page
            return render_template('error.html', error=str(e)), 500
    return render_template('submit.html')

@app.route('/api/events')
def get_events():
    tag = request.args.get('tag')
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

