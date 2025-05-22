# TIAT
the intersection of art &amp; technology

[TIAT](https://ashherr.github.io/tiat/) is a salon series in San Francisco for creative technologists to share personal projects.

put on by [ash](https://imempowa.com/)

# tiat.place Events System

A lightweight events listing and submission system for [tiat.place](http://tiat.place), a home for creative technology.

## Features

- View events organized by date
- Filter events by tags
- Submit new events with details and images
- Built with Supabase for better performance and reliability

## Setup Instructions

### 1. Supabase Setup

1. Create a new project on [Supabase](https://supabase.com/)
2. Get your project URL and anon key from the API settings
3. Run the database schema setup:
   - Navigate to the SQL Editor in your Supabase dashboard
   - Paste and run the contents of `supabase_schema.sql`

### 2. Configure the Front-end

1. Open `events.html` and update the Supabase credentials:
   ```javascript
   const supabaseUrl = 'YOUR_SUPABASE_URL';
   const supabaseKey = 'YOUR_SUPABASE_ANON_KEY';
   ```

### 3. Deploy

1. Upload the following files to your web server:
   - `index.html` (with the link to events.html)
   - `events.html`
   - Other site assets (CSS, images, etc.)

## File Structure

- `index.html` - Main site with link to events page
- `events.html` - Public events listing and submission page
- `supabase_schema.sql` - SQL schema for Supabase setup
- `README.md` - This file

## Customization

Feel free to customize the styling to better match your site's aesthetics. The current design is intentionally minimal for fast performance.

## Database Schema

The events are stored in a `events` table with the following structure:

- `id` - UUID, primary key
- `name` - Event name
- `date` - Event date
- `start_time` - Event start time
- `end_time` - Event end time
- `location` - Event location
- `description` - Event description
- `image_url` - URL to event image
- `tags` - Array of tags
- `is_featured` - Boolean flag for featured events (reserved for future use)
- `created_at` - Timestamp of creation
- `updated_at` - Timestamp of last update

## Future Improvements

- Add admin functionality for event management
- Implement server-side authentication
- Add image uploads to Supabase Storage
- Add event editing functionality
- Implement email notifications for new event submissions

# TIAT Calendar

## Google Calendar Integration Setup

1. Create a Google Cloud Project and enable the Google Calendar API
2. Create a service account and download the credentials
3. Rename the downloaded credentials file to `service-account.json` and place it in the root directory
4. Share your Google Calendar with the service account email address
5. Add the following environment variables to your Vercel project:
   - `GOOGLE_CALENDAR_ID`: Your Google Calendar ID
   - `GOOGLE_SERVICE_ACCOUNT_EMAIL`: The service account email
   - `GOOGLE_PRIVATE_KEY`: The private key from your service account
   - `GOOGLE_PROJECT_ID`: Your Google Cloud project ID

## Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `service-account.json` file based on the template:
   ```bash
   cp service-account.template.json service-account.json
   ```

3. Fill in your service account credentials in `service-account.json`

4. Start the development server:
   ```bash
   npm run dev
   ```

## Deployment

This project is configured to deploy to Vercel. Make sure to add all required environment variables in your Vercel project settings.
