// Google Calendar Integration
const GOOGLE_CALENDAR_ID = '1cec5ca26c8f4a7bb306b18e1c024a7c5370fe7f7813ddbfa12723bf5455d06b@group.calendar.google.com';
const CLIENT_ID = '736097547055-f9vr8rbmq6mkfn88hmgl73l5ln1nn0nd.apps.googleusercontent.com'; // Replace with your OAuth 2.0 Client ID
const SCOPES = 'https://www.googleapis.com/auth/calendar.events';

let auth2 = null;

// Initialize the Google Calendar API
async function initGoogleCalendar() {
  console.log('Initializing Google Calendar API...');
  try {
    // Load the auth2 library
    console.log('Loading auth2 library...');
    await new Promise((resolve, reject) => {
      gapi.load('auth2', {
        callback: () => {
          console.log('Auth2 library loaded, initializing...');
          try {
            gapi.auth2.init({
              client_id: CLIENT_ID,
              scope: SCOPES
            }).then((auth) => {
              console.log('Auth2 initialized successfully');
              auth2 = auth;
              resolve();
            }).catch((error) => {
              console.error('Error initializing auth2:', error);
              console.error('Error details:', {
                message: error.message,
                stack: error.stack,
                details: error.details
              });
              reject(error);
            });
          } catch (initError) {
            console.error('Error in auth2.init:', initError);
            console.error('Error details:', {
              message: initError.message,
              stack: initError.stack,
              details: initError.details
            });
            reject(initError);
          }
        },
        onerror: (error) => {
          console.error('Error loading auth2 library:', error);
          console.error('Error details:', {
            message: error.message,
            stack: error.stack,
            details: error.details
          });
          reject(error);
        }
      });
    });

    // Load the calendar API
    console.log('Loading calendar API...');
    try {
      await gapi.client.init({
        discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest']
      });
      console.log('Calendar API loaded');
    } catch (clientError) {
      console.error('Error loading calendar API:', clientError);
      console.error('Error details:', {
        message: clientError.message,
        stack: clientError.stack,
        details: clientError.details
      });
      throw clientError;
    }

    // Listen for sign-in state changes
    auth2.isSignedIn.listen(updateSigninStatus);
    // Handle the initial sign-in state
    updateSigninStatus(auth2.isSignedIn.get());
    
    console.log('Google Calendar API initialization complete');
  } catch (error) {
    console.error('Error initializing Google Calendar API:', error);
    console.error('Error details:', {
      message: error.message,
      stack: error.stack,
      details: error.details
    });
    throw error;
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
  console.log('handleAuthClick called');
  try {
    if (!auth2) {
      console.error('Auth2 not initialized');
      throw new Error('Auth2 not initialized');
    }
    console.log('Attempting to sign in...');
    await auth2.signIn();
    console.log('Sign in successful');
  } catch (error) {
    console.error('Error signing in:', error);
    console.error('Error details:', {
      message: error.message,
      stack: error.stack,
      details: error.details
    });
    throw error;
  }
}

// Add an event to Google Calendar
async function addEventToGoogleCalendar(event) {
  try {
    if (!auth2) {
      throw new Error('Auth2 not initialized');
    }

    // Check if user is signed in
    if (!auth2.isSignedIn.get()) {
      throw new Error('User must be signed in to add events');
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