// Main script for TIAT salons page
function handleResponse(res) {
  if (!res.ok) {
    throw new Error(`HTTP error! status: ${res.status}`);
  }
  return res.json();
}

document.addEventListener("DOMContentLoaded", function() {
  // Add event listeners for salon headings
  const eventHeadings = document.querySelectorAll('.event-heading');
  
  eventHeadings.forEach(heading => {
    heading.addEventListener('click', function() {
      const headingText = this.getAttribute('data-heading');
      console.log(`Clicked on: ${headingText}`);
      
      // Toggle visibility of content below the heading
      const content = this.nextElementSibling;
      if (content && content.tagName === 'TABLE') {
        content.style.display = content.style.display === 'none' ? 'table' : 'none';
      }
    });
  });
  
  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });
}); 