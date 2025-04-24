document.addEventListener('DOMContentLoaded', function() {
    // Remove mobile-only check, apply to all devices
    
    // Get all sections in the salon page
    const sections = document.querySelectorAll('section');
    
    // Initialize Intersection Observer for each section
    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const section = entry.target;
            const heading = section.querySelector('.event-heading');
            const imageContainer = section.querySelector('.image-container');
            const imageElement = section.querySelector('.event-image');
            
            if (entry.isIntersecting) {
                // Section is in view, show the image
                if (imageElement && imageElement.src) {
                    imageContainer.style.display = 'block';
                    imageElement.style.display = 'block';
                    
                    // Start image cycling if needed
                    startImageCycling(heading);
                }
            } else {
                // Section is out of view, hide the image
                if (imageContainer) {
                    imageContainer.style.display = 'none';
                }
                if (imageElement) {
                    imageElement.style.display = 'none';
                }
                
                // Stop image cycling
                stopImageCycling(heading);
            }
        });
    }, {
        root: null, // Use viewport as root
        rootMargin: '0px',
        threshold: 0.4 // 40% of the section needs to be visible
    });
    
    // Observe each section
    sections.forEach(section => {
        sectionObserver.observe(section);
    });
    
    // Image cycling functionality
    const cyclingSections = new Map(); // Store active intervals
    
    function startImageCycling(heading) {
        const headingData = heading.getAttribute('data-heading');
        if (!headingData) return;
        
        // Get the image URLs from the main script's data
        let imageUrls;
        if (window.imageUrlsByHeading) {
            imageUrls = window.imageUrlsByHeading[headingData];
        } else {
            // Fallback if the main script's data isn't accessible
            const mainScript = document.querySelector('script[src*="script.js"]');
            if (mainScript) {
                // Wait for the main script to finish loading
                mainScript.onload = function() {
                    if (window.imageUrlsByHeading) {
                        imageUrls = window.imageUrlsByHeading[headingData];
                        setupCycling();
                    }
                };
                return;
            }
        }
        
        setupCycling();
        
        function setupCycling() {
            if (!imageUrls || imageUrls.length <= 1) return;
            
            const imageElement = heading.querySelector('.event-image');
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
    }
    
    function stopImageCycling(heading) {
        const headingData = heading.getAttribute('data-heading');
        if (!headingData) return;
        
        if (cyclingSections.has(headingData)) {
            clearInterval(cyclingSections.get(headingData));
            cyclingSections.delete(headingData);
        }
    }
    
    // Add CSS to style the images for all devices
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        .image-container {
            display: none;
            margin: 15px 0;
            text-align: center;
        }
        
        .event-image {
            max-width: 90%;
            height: auto;
            display: block;
            margin: 0 auto;
        }
        
        /* Remove hover styles completely */
        .event-heading:hover .image-container,
        .event-heading:hover .event-image {
            display: none;
        }
        
        /* Additional mobile-specific styles */
        @media screen and (max-width: 768px) {
            .event-image {
                max-width: 85%;
            }
        }
        
        /* Extra small devices */
        @media screen and (max-width: 480px) {
            .event-image {
                max-width: 80%;
            }
        }
    `;
    document.head.appendChild(styleElement);
    
    // Make the image URLs accessible to this script
    window.addEventListener('load', function() {
        // Attempt to access the imageUrlsByHeading from the main script
        if (typeof imageUrlsByHeading !== 'undefined') {
            window.imageUrlsByHeading = imageUrlsByHeading;
        }
    });
}); 