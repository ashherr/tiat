import { google } from 'googleapis';

// Load service account credentials from environment variable
const credentials = JSON.parse(process.env.GOOGLE_SERVICE_ACCOUNT);

// Initialize auth
const auth = new google.auth.JWT(
  credentials.client_email,
  null,
  credentials.private_key,
  ['https://www.googleapis.com/auth/calendar']
);

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { calendarId, event } = req.body;
    
    const calendar = google.calendar('v3');
    const response = await calendar.events.insert({
      auth,
      calendarId,
      resource: event
    });
    
    return res.status(200).json(response.data);
  } catch (error) {
    console.error('Error adding event:', error);
    return res.status(500).json({ error: error.message });
  }
} 