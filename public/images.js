document.addEventListener('DOMContentLoaded', function() {
  // Image collections from the original script
  window.imageUrlsByHeading = {
    "Demos from event 11": [
      "https://i.postimg.cc/bvhDJMjW/tiat-future.jpg"
    ],
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

  // Set up image display for each section
  const eventHeadings = document.querySelectorAll('.event-heading');
  
  // 1. Initialize images and image containers
  eventHeadings.forEach(heading => {
    const section = heading.closest('section');
    const imageContainer = section.querySelector('.image-container');
    const headingData = heading.getAttribute('data-heading');
    const imageUrls = window.imageUrlsByHeading[headingData];
    
    // Skip if no images for this heading
    if (!imageUrls || imageUrls.length === 0) return;
    
    // Create image element if it doesn't exist
    let imageElement = section.querySelector('.event-image');
    if (!imageElement && imageContainer) {
      imageElement = document.createElement('img');
      imageElement.className = 'event-image';
      imageElement.alt = 'Image from ' + headingData;
      imageContainer.appendChild(imageElement);
    }
    
    // Set initial image if element exists
    if (imageElement) {
      imageElement.src = imageUrls[0];
    }
  });
  
  // 2. Set up image cycling when tables are visible
  const cyclingSections = new Map(); // Store active intervals
  
  function startImageCycling(heading) {
    const headingData = heading.getAttribute('data-heading');
    if (!headingData) return;
    
    const imageUrls = window.imageUrlsByHeading[headingData];
    if (!imageUrls || imageUrls.length <= 1) return;
    
    const section = heading.closest('section');
    const imageElement = section.querySelector('.event-image');
    if (!imageElement) return;
    
    let currentIndex = 0;
    
    // Clear any existing interval
    if (cyclingSections.has(headingData)) {
      clearInterval(cyclingSections.get(headingData));
    }
    
    // Set up new cycling interval
    const intervalId = setInterval(() => {
      currentIndex = (currentIndex + 1) % imageUrls.length;
      imageElement.src = imageUrls[currentIndex];
    }, 2000); // Every 2 seconds
    
    cyclingSections.set(headingData, intervalId);
  }
  
  function stopImageCycling(heading) {
    const headingData = heading.getAttribute('data-heading');
    if (!headingData) return;
    
    if (cyclingSections.has(headingData)) {
      clearInterval(cyclingSections.get(headingData));
      cyclingSections.delete(headingData);
    }
  }
  
  // 3. Add CSS styles for images
  const styleElement = document.createElement('style');
  styleElement.textContent = `
    .image-container {
      margin: 15px 0;
      text-align: center;
    }
    
    .event-image {
      max-width: 85%;
      height: auto;
      display: block;
      margin: 0 auto;
      border-radius: 4px;
      transition: opacity 0.5s ease;
      opacity: 0.8;
    }
    
    @media screen and (max-width: 768px) {
      .event-image {
        max-width: 80%;
      }
    }
    
    @media screen and (max-width: 480px) {
      .event-image {
        max-width: 75%;
      }
    }
  `;
  document.head.appendChild(styleElement);
  
  // 4. Handle image display when tables are toggled
  eventHeadings.forEach(heading => {
    heading.addEventListener('click', function() {
      const section = this.closest('section');
      const table = section.querySelector('table');
      const imageContainer = section.querySelector('.image-container');
      
      if (table) {
        const isTableVisible = table.style.display === 'table';
        
        // If table is now visible, show images and start cycling
        if (isTableVisible) {
          if (imageContainer) {
            imageContainer.style.display = 'block';
            startImageCycling(this);
          }
        } 
        // If table is now hidden, hide images and stop cycling
        else {
          if (imageContainer) {
            imageContainer.style.display = 'none';
            stopImageCycling(this);
          }
        }
      }
    });
  });
}); 