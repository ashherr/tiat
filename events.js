// Store events in localStorage
const EVENTS_STORAGE_KEY = 'tiat_events';
const ADMIN_KEY = 'tiat_admin'; // Simple admin flag for demonstration

// Sample data structure for an event
/*
{
  id: "unique-id", // Generated UUID
  name: "Event Name",
  date: "2023-05-01", // YYYY-MM-DD
  startTime: "17:00", // HH:MM in 24hr format
  endTime: "19:00",
  location: "Location Name",
  description: "Event description...",
  imageUrl: "https://example.com/image.jpg",
  tags: ["generative", "sound"],
  isFeatured: false, // For admin to mark as featured
  timestamp: 1682902800000 // For sorting, combined date and startTime in milliseconds
}
*/

document.addEventListener('DOMContentLoaded', () => {
  // DOM elements
  const eventsContainer = document.getElementById('events-container');
  const tagsContainer = document.getElementById('tags-container');
  const submitButton = document.getElementById('submit-event');
  const submissionForm = document.getElementById('submission-form');
  const eventForm = document.getElementById('event-form');
  const cancelButton = document.getElementById('cancel-submission');

  // Initialize
  loadAndDisplayEvents();
  setupTagFiltering();
  setupEventForm();

  // Event Listeners
  submitButton.addEventListener('click', (e) => {
    e.preventDefault();
    submissionForm.style.display = 'block';
  });

  cancelButton.addEventListener('click', () => {
    submissionForm.style.display = 'none';
    eventForm.reset();
  });

  // Functions
  function loadAndDisplayEvents(filterTag = 'all') {
    const events = getEvents();
    
    // Filter events to only show current and future events
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Beginning of today
    
    const futureEvents = events.filter(event => {
      const eventDate = new Date(event.date);
      eventDate.setHours(0, 0, 0, 0);
      return eventDate >= today;
    });

    // Sort events by date and time
    futureEvents.sort((a, b) => a.timestamp - b.timestamp);

    // Group events by date
    const eventsByDate = groupEventsByDate(futureEvents);

    // Clear events container
    eventsContainer.innerHTML = '';

    // Display events grouped by date
    if (Object.keys(eventsByDate).length === 0) {
      eventsContainer.innerHTML = '<p>No upcoming events. Be the first to submit one!</p>';
      return;
    }

    // Create DOM elements for each date and its events
    Object.keys(eventsByDate).forEach(date => {
      // Format date for display (e.g., "Monday, May 1, 2023")
      const dateObj = new Date(date);
      const formattedDate = dateObj.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });

      // Create date heading
      const dateElement = document.createElement('div');
      dateElement.className = 'date';
      dateElement.textContent = formattedDate;
      eventsContainer.appendChild(dateElement);

      // Filter events by tag if needed
      let eventsToShow = eventsByDate[date];
      if (filterTag !== 'all') {
        eventsToShow = eventsToShow.filter(event => 
          event.tags && event.tags.includes(filterTag)
        );
      }

      // If no events for this date after filtering, skip
      if (eventsToShow.length === 0) {
        const noEvents = document.createElement('div');
        noEvents.className = 'event';
        noEvents.textContent = 'No events matching the selected tag on this date.';
        eventsContainer.appendChild(noEvents);
        return;
      }

      // Create event elements
      eventsToShow.forEach(event => {
        // Format times for display
        const startTime = formatTime(event.startTime);
        const endTime = formatTime(event.endTime);
        
        // Create event element
        const eventElement = document.createElement('div');
        eventElement.className = 'event';
        eventElement.setAttribute('data-id', event.id);
        
        // Star for featured events
        const featuredStar = event.isFeatured ? '★ ' : '';
        
        // Event text: time, title, location
        eventElement.textContent = `${featuredStar}${startTime}-${endTime} ${event.name} @ ${event.location}`;
        
        // Create image element (hidden by default)
        if (event.imageUrl) {
          const imageElement = document.createElement('img');
          imageElement.className = 'event-image';
          imageElement.src = event.imageUrl;
          imageElement.alt = event.name;
          eventElement.appendChild(imageElement);
        }
        
        // Create description element (hidden by default)
        const descriptionElement = document.createElement('div');
        descriptionElement.className = 'event-description';
        descriptionElement.textContent = event.description;
        
        // Add tags to description
        if (event.tags && event.tags.length > 0) {
          const tagsText = document.createElement('div');
          tagsText.textContent = `Tags: ${event.tags.join(', ')}`;
          descriptionElement.appendChild(tagsText);
        }
        
        eventElement.appendChild(descriptionElement);
        
        // Event hover effects
        eventElement.addEventListener('mouseenter', () => {
          const image = eventElement.querySelector('.event-image');
          if (image) image.style.display = 'block';
          eventElement.querySelector('.event-description').style.display = 'block';
        });
        
        eventElement.addEventListener('mouseleave', () => {
          const image = eventElement.querySelector('.event-image');
          if (image) image.style.display = 'none';
          eventElement.querySelector('.event-description').style.display = 'none';
        });
        
        eventsContainer.appendChild(eventElement);
      });
    });
  }

  function setupTagFiltering() {
    const tags = tagsContainer.querySelectorAll('.tag');
    
    tags.forEach(tag => {
      tag.addEventListener('click', () => {
        // Remove active class from all tags
        tags.forEach(t => t.classList.remove('active'));
        
        // Add active class to clicked tag
        tag.classList.add('active');
        
        // Get the tag value and filter events
        const tagValue = tag.getAttribute('data-tag');
        loadAndDisplayEvents(tagValue);
      });
    });
  }

  function setupEventForm() {
    eventForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // Get form values
      const name = document.getElementById('event-name').value;
      const date = document.getElementById('event-date').value;
      const startTime = document.getElementById('event-time').value;
      const endTime = document.getElementById('event-end-time').value;
      const location = document.getElementById('event-location').value;
      const description = document.getElementById('event-description').value;
      const imageUrl = document.getElementById('event-image').value;
      
      // Get selected tags
      const selectedTags = [];
      document.querySelectorAll('input[name="tags"]:checked').forEach(checkbox => {
        selectedTags.push(checkbox.value);
      });
      
      // Create event object
      const newEvent = {
        id: generateId(),
        name,
        date,
        startTime,
        endTime,
        location,
        description,
        imageUrl,
        tags: selectedTags,
        isFeatured: false,
        timestamp: getTimestamp(date, startTime)
      };
      
      // Save event
      saveEvent(newEvent);
      
      // Reset form and hide
      eventForm.reset();
      submissionForm.style.display = 'none';
      
      // Reload events
      loadAndDisplayEvents();
    });
  }

  // Helper Functions
  function getEvents() {
    const eventsJson = localStorage.getItem(EVENTS_STORAGE_KEY);
    return eventsJson ? JSON.parse(eventsJson) : [];
  }

  function saveEvent(event) {
    const events = getEvents();
    events.push(event);
    localStorage.setItem(EVENTS_STORAGE_KEY, JSON.stringify(events));
  }

  function groupEventsByDate(events) {
    return events.reduce((groups, event) => {
      const date = event.date;
      if (!groups[date]) {
        groups[date] = [];
      }
      groups[date].push(event);
      return groups;
    }, {});
  }

  function formatTime(timeString) {
    // Convert 24h format to 12h format
    const [hour, minute] = timeString.split(':');
    const hourNum = parseInt(hour);
    const period = hourNum >= 12 ? 'PM' : 'AM';
    const hour12 = hourNum % 12 || 12;
    return `${hour12}:${minute}${period}`;
  }

  function generateId() {
    // Simple UUID generator
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  function getTimestamp(dateStr, timeStr) {
    const [year, month, day] = dateStr.split('-');
    const [hour, minute] = timeStr.split(':');
    return new Date(year, month - 1, day, hour, minute).getTime();
  }
});

// Admin functionality (basic implementation)
// In a real application, this would be handled server-side with proper authentication
function initAdminInterface() {
  // Check if user is admin
  const isAdmin = localStorage.getItem(ADMIN_KEY) === 'true';
  
  if (isAdmin) {
    // Add admin controls to each event
    document.querySelectorAll('.event').forEach(eventElement => {
      const eventId = eventElement.getAttribute('data-id');
      
      // Feature/unfeature button
      const featureButton = document.createElement('button');
      featureButton.textContent = '★';
      featureButton.style.marginLeft = '10px';
      featureButton.addEventListener('click', () => toggleFeatureEvent(eventId));
      
      // Delete button
      const deleteButton = document.createElement('button');
      deleteButton.textContent = '✕';
      deleteButton.style.marginLeft = '5px';
      deleteButton.addEventListener('click', () => deleteEvent(eventId));
      
      eventElement.appendChild(featureButton);
      eventElement.appendChild(deleteButton);
    });
  }
}

// These admin functions would be called when admin interface is active
function toggleFeatureEvent(eventId) {
  const events = JSON.parse(localStorage.getItem(EVENTS_STORAGE_KEY) || '[]');
  const eventIndex = events.findIndex(e => e.id === eventId);
  
  if (eventIndex >= 0) {
    events[eventIndex].isFeatured = !events[eventIndex].isFeatured;
    localStorage.setItem(EVENTS_STORAGE_KEY, JSON.stringify(events));
    location.reload(); // Refresh to show changes
  }
}

function deleteEvent(eventId) {
  if (confirm('Are you sure you want to delete this event?')) {
    const events = JSON.parse(localStorage.getItem(EVENTS_STORAGE_KEY) || '[]');
    const filteredEvents = events.filter(e => e.id !== eventId);
    localStorage.setItem(EVENTS_STORAGE_KEY, JSON.stringify(filteredEvents));
    location.reload(); // Refresh to show changes
  }
} 