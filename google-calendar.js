// Google Calendar Integration
const GOOGLE_CALENDAR_ID = '1cec5ca26c8f4a7bb306b18e1c024a7c5370fe7f7813ddbfa12723bf5455d06b@group.calendar.google.com';

// Add an event to Google Calendar
async function addEventToGoogleCalendar(event) {
  try {
    const calendarEvent = {
      summary: event.name,
      location: event.location,
      description: event.description,
      start: {
        dateTime: `${event.date}T${event.start_time}:00`,
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      },
      end: {
        dateTime: `${event.date}T${event.end_time}:00`,
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      },
      ...(event.event_url && { htmlLink: event.event_url }),
    };

    // Initialize the Google Calendar API
    await gapi.client.init({
      apiKey: null,
      discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'],
    });

    // Add the event to the calendar
    const response = await gapi.client.calendar.events.insert({
      calendarId: GOOGLE_CALENDAR_ID,
      resource: calendarEvent
    });

    console.log('Event added to Google Calendar:', response.result);
    return response.result;
  } catch (error) {
    console.error('Error adding event to Google Calendar:', error);
    throw error;
  }
}

// Initialize Google Calendar API
async function initGoogleCalendar() {
  try {
    await gapi.load('client', async () => {
      await gapi.client.init({
        apiKey: null,
        discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'],
      });
      console.log('Google Calendar API initialized');
    });
  } catch (error) {
    console.error('Error initializing Google Calendar API:', error);
    throw error;
  }
}

// Export functions
window.googleCalendar = {
  addEventToGoogleCalendar,
  initGoogleCalendar
}; 