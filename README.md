# Bay Area Creative Tech Events

A minimal, fast-performing website for aggregating creative technology events in the Bay Area.

## Features

- Event submission for anyone
- Minimal, text-based event listing
- Hover to preview event details and images
- Tag-based filtering
- Google Calendar integration for events
- Star system for featured events
- Mobile responsive design

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file by copying the example:
```bash
cp env.example .env
```
Then edit the `.env` file with your configuration values.

4. Initialize the database:
```bash
python init_db.py
```

5. Start the app:
```bash
flask run
```

## Google Calendar Integration

To enable Google Calendar integration:

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Google Calendar API
3. Create a service account with Calendar API permissions
4. You have two options for credentials management:

   **Option 1: Environment Variables (RECOMMENDED for security):**
   - Get the credentials JSON and extract the values into environment variables in your `.env` file:
   ```
   ENABLE_GCAL=true
   GOOGLE_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret-here
   GOOGLE_PROJECT_ID=your-project-id
   GOOGLE_CALENDAR_ID=your-calendar-id@group.calendar.google.com
   ```

   **Option 2: Service Account JSON File (less secure):**
   - Download the service account credentials JSON file and save it to `credentials/service_account.json`
   - Add this file to your `.gitignore` to prevent accidental exposure
   - Update the `.env` file with:
   ```
   ENABLE_GCAL=true
   GOOGLE_CREDENTIALS_FILE=credentials/service_account.json
   GOOGLE_CALENDAR_ID=your-calendar-id@group.calendar.google.com
   ```

5. Share your Google Calendar with the service account email

Users can subscribe to your public calendar by visiting the `/calendar` page.

## Security Best Practices

- Never commit credentials or API keys to your repository
- Use environment variables for secrets rather than files
- Make sure `.env` and other credentials files are in your `.gitignore`
- If you accidentally commit sensitive information, follow GitHub's guide to [remove sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## Database Schema Updates

After updating the database schema, run the update script:
```bash
python update_db.py
```

For production (Supabase), run the SQL commands manually as specified in `supabase_table.sql`.

## Development

The application uses:
- Flask for the backend
- SQLite for development, Supabase PostgreSQL for production
- Minimal HTML/CSS/JavaScript for the frontend
- Google Calendar API for event synchronization

## License

MIT 