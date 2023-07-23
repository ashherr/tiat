/* Cycle through a few pics per event heading */
const eventHeadings = document.querySelectorAll('.event-heading');

const imageUrlsByHeading = {
  "Demos from event 1": [
    "https://pbs.twimg.com/media/F1tXV5YaAAAKMdH?format=jpg&name=large"
  ],
  "Demos from event 2": [
    "https://pbs.twimg.com/media/F1tWiH0aAAIoO4t?format=jpg&name=4096x4096",
    "https://pbs.twimg.com/media/F1tWjm1aYAcbXuM?format=jpg&name=4096x4096"
  ],
  "Demos from event 3": [
    "https://pbs.twimg.com/media/F1tSkOeaMAAZWoH?format=jpg&name=4096x4096",
    "https://pbs.twimg.com/media/F1tSkOdaYAIqWPf?format=jpg&name=4096x4096",
    "https://pbs.twimg.com/media/F1tSkOhakAIa3iF?format=jpg&name=4096x4096",
    "https://pbs.twimg.com/media/F1tSkOhaYAA-TK_?format=jpg&name=4096x4096"
  ],
  "Demos from event 4": [
    " ",
    " ",
    " ",
    " "
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