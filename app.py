from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'

db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    event_link = db.Column(db.String(500), nullable=False)
    tags = db.Column(db.String(500), nullable=False)  # Stored as comma-separated values
    is_starred = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/salons')
def salons():
    return render_template('salons.html')

@app.route('/salon')
def salon():
    return redirect(url_for('salons'))  # Redirect /salon to /salons

@app.route('/submit', methods=['GET', 'POST'])
def submit_event():
    if request.method == 'POST':
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

# Serve static files from the root directory if needed
@app.route('/salons.html')
def salons_static():
    return redirect(url_for('salons'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 