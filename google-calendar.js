// Google Calendar Integration
const GOOGLE_CALENDAR_ID = '1cec5ca26c8f4a7bb306b18e1c024a7c5370fe7f7813ddbfa12723bf5455d06b@group.calendar.google.com';
const CLIENT_ID = '736097547055-f9vr8rbmq6mkfn88hmgl73l5ln1nn0nd.apps.googleusercontent.com';
const SCOPES = 'https://www.googleapis.com/auth/calendar.events';

let auth2 = null;

// Initialize the Google Calendar API
async function initGoogleCalendar() {
  console.log('Initializing Google Calendar API...');
  try {
    // Load the auth2 library
    console.log('Loading auth2 library...');
    await new Promise((resolve, reject) => {
      gapi.load('client:auth2', {
        callback: async () => {
          console.log('Google API loaded, initializing...');
          try {
            await gapi.client.init({
              clientId: CLIENT_ID,
              scope: SCOPES,
              discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest'],
              ux_mode: 'popup'  // Use popup instead of iframe
            });
            
            auth2 = gapi.auth2.getAuthInstance();
            console.log('Auth2 initialized successfully');
            
            // Listen for sign-in state changes
            auth2.isSignedIn.listen(updateSigninStatus);
            // Handle the initial sign-in state
            updateSigninStatus(auth2.isSignedIn.get());
            
            resolve();
          } catch (initError) {
            console.error('Error in client.init:', initError);
            console.error('Error details:', {
              message: initError.message,
              stack: initError.stack,
              details: initError.details
            });
            reject(initError);
          }
        },
        onerror: (error) => {
          console.error('Error loading Google API:', error);
          console.error('Error details:', {
            message: error.message,
            stack: error.stack,
            details: error.details
          });
          reject(error);
        }
      });
    });
    
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
    const googleUser = await auth2.signIn({
      prompt: 'select_account'  // Force account selection
    });
    console.log('Sign in successful', googleUser);
    return googleUser;
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