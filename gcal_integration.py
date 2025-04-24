import os
import datetime
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials/service_account.json')
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'primary')  # Calendar ID to add events to

def create_service():
    """Create a Google Calendar API service."""
    try:
        # Check if credentials file exists
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"Credentials file not found: {CREDENTIALS_FILE}")
            return None
            
        # Create credentials using service account
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, 
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        
        # Build the service
        service = build('calendar', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print(f"Error creating Google Calendar service: {e}")
        return None

def add_event_to_calendar(event_data):
    """
    Add an event to Google Calendar.
    
    Args:
        event_data: Dictionary containing event details (title, start_time, end_time, location, description)
    
    Returns:
        event_id: ID of created event, or None if failed
    """
    service = create_service()
    if not service:
        print("Failed to create Google Calendar service")
        return None
    
    try:
        # Parse start and end times
        start_time = event_data.get('start_time')
        # If no end time provided, make event 2 hours long by default
        end_time = event_data.get('end_time', 
                                 (datetime.datetime.fromisoformat(start_time) + 
                                  datetime.timedelta(hours=2)).isoformat())
        
        # Create event object
        event = {
            'summary': event_data.get('title'),
            'location': event_data.get('location', ''),
            'description': event_data.get('description', '') + f"\nEvent Link: {event_data.get('event_link', '')}",
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Los_Angeles',
            },
        }
        
        # Add organizer if provided
        if event_data.get('organizer_email'):
            event['organizer'] = {
                'email': event_data.get('organizer_email')
            }
        
        # Add event to calendar
        created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"Event created: {created_event.get('htmlLink')}")
        
        return created_event.get('id')
    
    except HttpError as error:
        print(f"Google Calendar API error: {error}")
        return None
    except Exception as e:
        print(f"Error adding event to calendar: {e}")
        return None

def get_calendar_subscribe_url():
    """Get the URL for subscribing to the calendar."""
    # Format: webcal://calendar.google.com/calendar/ical/{calendar_id}/public/basic.ics
    # Remove the @ and replace with %40 for proper URL format
    formatted_id = CALENDAR_ID.replace('@', '%40')
    return f"https://calendar.google.com/calendar/u/0?cid={formatted_id}"

def get_calendar_embed_html(width=800, height=600):
    """Get HTML for embedding the calendar."""
    return f"""
    <iframe src="https://calendar.google.com/calendar/embed?src={CALENDAR_ID}&ctz=America%2FLos_Angeles" 
    style="border: 0" width="{width}" height="{height}" frameborder="0" scrolling="no"></iframe>
    """

def get_calendar_info():
    """Get calendar information for sharing."""
    return {
        'calendar_id': CALENDAR_ID,
        'subscribe_url': get_calendar_subscribe_url(),
        'embed_html': get_calendar_embed_html(),
        'ical_url': f"https://calendar.google.com/calendar/ical/{CALENDAR_ID.replace('@', '%40')}/public/basic.ics",
        'html_link': f"https://calendar.google.com/calendar/u/0?cid={CALENDAR_ID.replace('@', '%40')}"
    } 