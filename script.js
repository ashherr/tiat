/* Cycle through a few pics per event heading */
const eventHeadings = document.querySelectorAll('.event-heading');

const imageUrlsByHeading = {
  "Demos from event 1": [
    "https://i.postimg.cc/QMdPQRzg/tiat1.png"
  ],
  "Demos from event 2": [
    "https://i.postimg.cc/L5p3TPXd/IMG-6906.jpg",
    "https://i.postimg.cc/ry1Jpfnq/IMG-6898.jpg"
  ],
  "Demos from event 3": [
    "https://i.postimg.cc/1txGmFDg/IMG-7331.jpg",
    "https://i.postimg.cc/85hhjCbZ/IMG-7300.jpg",
    "https://i.postimg.cc/D06LPYHs/IMG-7314.jpg"
  ],
  "Demos from event 4": [
    "https://i.postimg.cc/jd9LYbH2/IMG-7706.jpg",
    "https://i.postimg.cc/VNPv5WHc/IMG-7734.jpg",
    "https://i.postimg.cc/Gmy9c5KQ/IMG-7720.jpg",
    "https://i.postimg.cc/rpGm4RvR/IMG-7749.jpg"
  ],
  "Demos from event 5": [
    "https://i.postimg.cc/50n27d9x/Full-Size-Render.jpg"
  ],
  "Demos from event 6": [
    "https://i.postimg.cc/dQZ0RXPK/4e034a1e-f135-4161-b970-124cc462.jpg",
    "https://i.postimg.cc/mrqstLr1/IMG-0520.jpg"
  ],
  "Demos from event 7": [
    "https://i.postimg.cc/8CPz38S7/tiat7-1.png",
    "https://i.postimg.cc/PJw6jrDK/tiat7-2.png",
    "https://i.postimg.cc/76C93YKD/tiat7-3.png"
  ],
  "Demos from event 8": [
    "https://i.postimg.cc/kgD0dBJD/tiat-ia-intro-2.jpg",
    "https://i.postimg.cc/L6xc7zMr/tiat-ia-aud-1.jpg",
    "https://i.postimg.cc/R0H2NynB/tiat-ia-sharon-3.jpg",
    "https://i.postimg.cc/dVXzQw36/tiat-ia-dan-1.jpg"
  ],
  "Demos from event 9": [
    "https://i.postimg.cc/pL2GcmSG/IMG-1283.jpg",
    "https://i.postimg.cc/1zDjM8wv/IMG-1331.jpg",
    "https://i.postimg.cc/52nPhxdx/IMG-1260.jpg"
  ],
  "Demos from event 10": [
    "https://i.postimg.cc/g0nBNdh0/IMG-8479-preview.jpg",
    "https://i.postimg.cc/T3k4VhpS/IMG-3170.jpg",
    "https://i.postimg.cc/mZMJvb5z/IMG-8471-preview.jpg"
  ],
};

eventHeadings.forEach((eventHeading) => {
  const eventImage = eventHeading.querySelector('.event-image');
  const heading = eventHeading.getAttribute('data-heading');
  const imageUrls = imageUrlsByHeading[heading];

  let currentIndex = 0;
  let intervalId;

  eventHeading.addEventListener('mouseover', () => {
    eventImage.style.display = 'block';
    intervalId = setInterval(cycleImages, 500); // Change image every 1 second (adjust the interval as needed)
  });

  eventHeading.addEventListener('mouseout', () => {
    eventImage.style.display = 'none';
    clearInterval(intervalId); // Stop the image cycling
  });

  function cycleImages() {
    eventImage.src = imageUrls[currentIndex];
    currentIndex = (currentIndex + 1) % imageUrls.length;
  }

  // Set initial image
  eventImage.src = imageUrls[0];
});

// For GitHub Pages static version
function loadEventsStatic() {
    // Example static data - you would need to replace this with your actual event data
    const staticEvents = [
        {
            id: 1,
            title: "Example Art Event",
            start_time: "2023-12-25T19:00:00",
            location: "San Francisco Museum of Modern Art",
            description: "An exciting exhibition of digital art and technology.",
            image_url: "https://via.placeholder.com/400x300",
            event_link: "https://example.com/event1",
            tags: ["AI / ML", "generative"],
            is_starred: true
        },
        {
            id: 2,
            title: "Tech Art Workshop",
            start_time: "2023-12-26T14:00:00",
            location: "Gray Area Foundation",
            description: "Learn how to create interactive art with technology.",
            image_url: "https://via.placeholder.com/400x300",
            event_link: "https://example.com/event2",
            tags: ["hardware", "installation"],
            is_starred: false
        }
    ];
    
    return staticEvents;
}

// Modified function to work both with API and static data
function loadEvents(tag = null) {
    // Check if we're running on GitHub Pages (no backend)
    const isGitHubPages = window.location.hostname.includes('github.io');
    
    if (isGitHubPages) {
        // Use static data for GitHub Pages
        let events = loadEventsStatic();
        
        // Filter by tag if provided
        if (tag) {
            events = events.filter(event => event.tags.includes(tag));
        }
        
        displayEvents(events);
    } else {
        // Use API for local development
        let url = '/api/events';
        if (tag) {
            url += `?tag=${tag}`;
        }
        
        fetch(url)
            .then(response => response.json())
            .then(events => {
                displayEvents(events);
            });
    }
}

function displayEvents(events) {
    const eventsDiv = document.getElementById('events');
    eventsDiv.innerHTML = '';
    let currentDate = null;
    
    events.forEach(event => {
        const date = new Date(event.start_time).toLocaleDateString();
        if (date !== currentDate) {
            currentDate = date;
            const dateDiv = document.createElement('div');
            dateDiv.className = 'date';
            dateDiv.textContent = date;
            eventsDiv.appendChild(dateDiv);
        }
        
        const eventLink = document.createElement('a');
        eventLink.className = 'event';
        eventLink.href = event.event_link;
        eventLink.target = "_blank";
        eventLink.innerHTML = `
            ${event.is_starred ? '<span class="star">★</span>' : ''}
            ${new Date(event.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - ${event.title} - ${event.location}
        `;
        
        eventLink.onmouseover = () => {
            const preview = document.getElementById('preview');
            preview.innerHTML = `
                <img src="${event.image_url}" alt="${event.title}">
                <p>${event.description}</p>
            `;
            preview.style.display = 'block';
        };
        
        eventLink.onmouseout = () => {
            document.getElementById('preview').style.display = 'none';
        };
        
        eventsDiv.appendChild(eventLink);
    });
}
