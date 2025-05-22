// Google Calendar Integration
const GOOGLE_CALENDAR_ID = '1cec5ca26c8f4a7bb306b18e1c024a7c5370fe7f7813ddbfa12723bf5455d06b@group.calendar.google.com';
const CLIENT_ID = '736097547055-f9vr8rbmq6mkfn88hmgl73l5ln1nn0nd.apps.googleusercontent.com';

let isInitialized = false;

// Initialize Google Calendar API
async function initGoogleCalendar() {
  if (isInitialized) return;

  try {
    await new Promise((resolve, reject) => {
      gapi.load('client:auth2', {
        callback: async () => {
          try {
            await gapi.client.init({
              clientId: CLIENT_ID,
              scope: 'https://www.googleapis.com/auth/calendar',
              discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest']
            });
            console.log('Google Calendar API initialized');
            isInitialized = true;
            resolve();
          } catch (error) {
            console.error('Error in gapi.client.init:', error);
            reject(error);
          }
        },
        onerror: (error) => {
          console.error('Error loading gapi:', error);
          reject(error);
        }
      });
    });
  } catch (error) {
    console.error('Error initializing Google Calendar API:', error);
    throw error;
  }
}

// Add an event to Google Calendar
async function addEventToGoogleCalendar(event) {
  try {
    // Ensure API is initialized
    if (!isInitialized) {
      await initGoogleCalendar();
    }

    // Check if user is signed in
    const auth2 = gapi.auth2.getAuthInstance();
    if (!auth2.isSignedIn.get()) {
      console.log('User not signed in, initiating sign in...');
      await auth2.signIn();
    }

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

    console.log('Adding event to calendar:', calendarEvent);

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

// Export functions
window.googleCalendar = {
  addEventToGoogleCalendar,
  initGoogleCalendar
}; 