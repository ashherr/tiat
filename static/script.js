document.addEventListener('DOMContentLoaded', function() {
  // Image collections from the original script
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

  // Get all event headings
  const eventHeadings = document.querySelectorAll('.event-heading');
  
  // Setup each event heading with images and cycling functionality
  eventHeadings.forEach(heading => {
    const imageElement = heading.querySelector('.event-image');
    const headingData = heading.getAttribute('data-heading');
    const imageUrls = imageUrlsByHeading[headingData];
    
    // Skip if no images for this heading
    if (!imageUrls || imageUrls.length === 0) return;
    
    let currentIndex = 0;
    let intervalId;
    
    // Set initial image
    imageElement.src = imageUrls[0];
    
    // Function to cycle through images
    function cycleImages() {
      imageElement.src = imageUrls[currentIndex];
      currentIndex = (currentIndex + 1) % imageUrls.length;
    }
    
    // Add hover event listeners
    heading.addEventListener('mouseover', () => {
      imageElement.style.display = 'block';
      // Only set interval if there are multiple images
      if (imageUrls.length > 1) {
        intervalId = setInterval(cycleImages, 800); // Change image every 0.8 seconds
      }
    });
    
    heading.addEventListener('mouseout', () => {
      imageElement.style.display = 'none';
      clearInterval(intervalId); // Stop the image cycling
    });
  });
}); 