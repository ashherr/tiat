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
  ]
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
