# Bay Area Creative Tech Events

A minimal, fast-performing website for aggregating creative technology events in the Bay Area.

## Features

- Google Sign-in authentication
- Event submission for authenticated users
- Minimal, text-based event listing
- Hover to preview event details and images
- Tag-based filtering
- Admin dashboard for event moderation
- Star system for featured events

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

3. Create a `.env` file with the following variables:
```
SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
```

4. Initialize the database:
```bash
flask run
```

5. To make a user an admin, use the Flask shell:
```bash
flask shell
>>> from app import db, User
>>> user = User.query.filter_by(email='admin@example.com').first()
>>> user.is_admin = True
>>> db.session.commit()
```

## Development

The application uses:
- Flask for the backend
- SQLite for the database
- Google Sign-In for authentication
- Minimal HTML/JavaScript for the frontend

## License

MIT 