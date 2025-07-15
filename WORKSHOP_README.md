# Workshop System Documentation

## Overview

The workshop system allows you to manage upcoming and past workshops on the tiat website. It includes:

- A dynamic workshop page with upcoming and past sections
- Image cycling when scrolling through workshops
- An admin interface for managing workshop data
- JSON-based data storage

## Features

### Workshop Page (`/workshops`)
- **Upcoming Workshops**: Shows workshops with dates and times
- **Past Workshops**: Shows completed workshops without time information
- **Image Cycling**: When you scroll through workshops, the right sidebar shows workshop images
- **Responsive Design**: Works on desktop and mobile

### Data Management
- Direct JSON editing of `workshops.json`
- Simple file-based storage
- No authentication required

## Setup

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Start the Server**:
   ```bash
   npm start
   ```

3. **Edit Workshop Data**:
   - Edit `workshops.json` directly in your code editor
   - Restart the server to see changes

## Data Structure

Workshops are stored in `workshops.json` with this structure:

```json
{
  "upcoming": [
    {
      "id": "workshop-1",
      "title": "Workshop Title",
      "description": "Workshop description",
      "date": "2024-09-15",
      "time": "2:00 PM - 5:00 PM",
      "flyer": "https://example.com/flyer.png",
      "images": [
        "https://example.com/image1.png",
        "https://example.com/image2.png"
      ]
    }
  ],
  "past": [
    {
      "id": "workshop-past-1",
      "title": "Past Workshop",
      "description": "Description",
      "date": "2024-08-10",
      "flyer": "https://example.com/flyer.png",
      "images": [
        "https://example.com/image1.png"
      ]
    }
  ]
}
```

## Adding Workshops

### Via JSON File
1. Edit `workshops.json` directly in your code editor
2. Add workshop objects to the appropriate array (`upcoming` or `past`)
3. Ensure proper JSON formatting
4. Restart the server to see changes

## Image Requirements

- **Flyer**: Main workshop image (120x120px display)
- **Additional Images**: Extra photos from the workshop
- **Format**: Any web-accessible image URL
- **Recommended**: Use image hosting services like Postimg, Imgur, etc.

## Navigation

- **Main Site**: `http://localhost:3000`
- **Workshop Page**: Click "tiat workshops" in navigation

## Styling

The workshop system uses the same styling as the main site:
- Yellow highlight color: `#EEFF42`
- Font: Barlow Condensed
- Responsive design for mobile and desktop

## Troubleshooting

### Images Not Loading
- Check that image URLs are accessible
- Ensure URLs are complete (include `https://`)
- Try different image hosting services

### Workshop Page Not Loading
- Make sure the server is running (`npm start`)
- Check browser console for errors
- Verify `workshops.json` exists and is valid JSON

### Workshop Page Not Updating
- Clear browser cache
- Check that `workshops.json` is being served correctly
- Verify JavaScript console for errors

## File Structure

```
tiat/
├── index.html          # Main site with workshop page
├── script.js           # JavaScript with workshop logic
├── style.css           # CSS with workshop styles
├── workshops.json      # Workshop data
├── server.js           # Express server
└── package.json        # Dependencies
``` 