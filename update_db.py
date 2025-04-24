from app import app, db
import traceback

"""
Script to update the database schema with new fields for Google Calendar integration.
This will add:
- end_time (DateTime)
- organizer_email (String)
- calendar_event_id (String)
"""

def update_schema():
    try:
        with app.app_context():
            # Check if we're using SQLite (development)
            if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
                # Add columns to existing table
                print("Adding new columns to SQLite database...")
                db.engine.execute('ALTER TABLE event ADD COLUMN end_time DATETIME')
                db.engine.execute('ALTER TABLE event ADD COLUMN organizer_email VARCHAR(200)')
                db.engine.execute('ALTER TABLE event ADD COLUMN calendar_event_id VARCHAR(200)')
                print("Schema update complete for SQLite!")
            else:
                print("You're using Supabase in production. Please update your Supabase schema manually:")
                print("ALTER TABLE events ADD COLUMN end_time TIMESTAMPTZ;")
                print("ALTER TABLE events ADD COLUMN organizer_email VARCHAR(200);")
                print("ALTER TABLE events ADD COLUMN calendar_event_id VARCHAR(200);")
                
    except Exception as e:
        error_traceback = traceback.format_exc()
        print(f"Error updating schema: {str(e)}\n{error_traceback}")
        print("Note: If you get 'duplicate column' errors, the columns may already exist.")

if __name__ == "__main__":
    update_schema()
    print("Database update script completed.") 