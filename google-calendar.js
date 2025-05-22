// Google Calendar Integration
const GOOGLE_CALENDAR_ID = '1cec5ca26c8f4a7bb306b18e1c024a7c5370fe7f7813ddbfa12723bf5455d06b@group.calendar.google.com';
const CLIENT_ID = '736097547055-f9vr8rbmq6mkfn88hmgl73l5ln1nn0nd.apps.googleusercontent.com'; // Replace with your OAuth 2.0 Client ID
const SCOPES = 'https://www.googleapis.com/auth/calendar.events';

// Initialize the Google Calendar API
async function initGoogleCalendar() {
  try {
    // Load the auth2 library
    await new Promise((resolve, reject) => {
      gapi.load('auth2', {
        callback: resolve,
        onerror: reject
      });
    });

    // Initialize the auth2 library
    await gapi.auth2.init({
      client_id: CLIENT_ID,
      scope: SCOPES
    });

    // Load the calendar API
    await gapi.client.init({
      discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest']
    });

    // Listen for sign-in state changes
    gapi.auth2.getAuthInstance().isSignedIn.listen(updateSigninStatus);
    // Handle the initial sign-in state
    updateSigninStatus(gapi.auth2.getAuthInstance().isSignedIn.get());
    
    console.log('Google Calendar API initialized');
  } catch (error) {
    console.error('Error initializing Google Calendar API:', error);
  }
}

// Update UI based on sign-in status
function updateSigninStatus(isSignedIn) {
  if (isSignedIn) {
    console.log('User is signed in');
  } else {
    console.log('User is not signed in');
  }
}

// Handle sign-in
async function handleAuthClick() {
  try {
    await gapi.auth2.getAuthInstance().signIn();
  } catch (error) {
    console.error('Error signing in:', error);
  }
}

// Add an event to Google Calendar
async function addEventToGoogleCalendar(event) {
  try {
    // Check if user is signed in
    if (!gapi.auth2.getAuthInstance().isSignedIn.get()) {
      await handleAuthClick();
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

    const response = await gapi.client.calendar.events.insert({
      calendarId: GOOGLE_CALENDAR_ID,
      resource: calendarEvent,
    });

    console.log('Event added to Google Calendar:', response);
    return response;
  } catch (error) {
    console.error('Error adding event to Google Calendar:', error);
    throw error;
  }
}

// Export functions
window.googleCalendar = {
  initGoogleCalendar,
  addEventToGoogleCalendar,
  handleAuthClick,
}; 