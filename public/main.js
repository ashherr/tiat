document.addEventListener('DOMContentLoaded', function() {
  // Find all elements with event-heading class
  const eventHeadings = document.querySelectorAll('.event-heading');
  
  // Add click event listeners to each heading
  eventHeadings.forEach(heading => {
    heading.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Find the associated table within the section
      const section = this.closest('section');
      if (section) {
        const table = section.querySelector('table');
        if (table) {
          // Toggle the display property
          if (table.style.display === 'none' || table.style.display === '') {
            table.style.display = 'table';
            this.classList.add('active');
          } else {
            table.style.display = 'none';
            this.classList.remove('active');
          }
        }
      }
    });

    // Add hover effect
    heading.addEventListener('mouseenter', function() {
      this.style.textDecoration = 'underline';
    });
    
    heading.addEventListener('mouseleave', function() {
      this.style.textDecoration = 'none';
    });
  });
}); 