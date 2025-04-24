import os
import datetime
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# Configuration
CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials/service_account.json')
CALENDAR_ID = os.getenv('GOOGLE_CALENDAR_ID', 'primary')  # Calendar ID to add events to

def create_service():
    """Create a Google Calendar API service."""
    try:
        # Check for service account key in environment variables first
        service_account_email = os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL')
        service_account_private_key = os.getenv('GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY')
        
        if service_account_email and service_account_private_key:
            print("Using Google service account from environment variables")
            
            # Replace newline placeholders with actual newlines if needed
            if "\\n" in service_account_private_key:
                service_account_private_key = service_account_private_key.replace("\\n", "\n")
            
            # Create service account info dictionary
            credentials_info = {
                "type": "service_account",
                "project_id": os.getenv('GOOGLE_PROJECT_ID', ''),
                "private_key_id": os.getenv('GOOGLE_PRIVATE_KEY_ID', ''),
                "private_key": service_account_private_key,
                "client_email": service_account_email,
                "client_id": os.getenv('GOOGLE_CLIENT_ID', ''),
                "auth_uri": os.getenv('GOOGLE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth'),
                "token_uri": os.getenv('GOOGLE_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
                "auth_provider_x509_cert_url": os.getenv('GOOGLE_AUTH_PROVIDER_X509_CERT_URL', 'https://www.googleapis.com/oauth2/v1/certs'),
                "client_x509_cert_url": os.getenv('GOOGLE_CLIENT_X509_CERT_URL', '')
            }
            
            # Create credentials from dictionary
            try:
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info,
                    scopes=['https://www.googleapis.com/auth/calendar']
                )
            except Exception as e:
                print(f"Error creating credentials from environment variables: {e}")
                print("Falling back to credentials file...")
                credentials = None
                
            if credentials:
                service = build('calendar', 'v3', credentials=credentials)
                return service
                
        # Fall back to file-based credentials if environment variables didn't work
        if os.path.exists(CREDENTIALS_FILE):
            print(f"Using Google credentials from file: {CREDENTIALS_FILE}")
            try:
                credentials = service_account.Credentials.from_service_account_file(
                    CREDENTIALS_FILE, 
                    scopes=['https://www.googleapis.com/auth/calendar']
                )
                service = build('calendar', 'v3', credentials=credentials)
                return service
            except Exception as e:
                print(f"Error creating credentials from file: {e}")
                return None
        
        # No valid credentials available
        print("No valid Google credentials available. Calendar features will be disabled.")
        return None
            
    except Exception as e:
        print(f"Error creating Google Calendar service: {e}")
        print(f"Error details: {traceback.format_exc()}")
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