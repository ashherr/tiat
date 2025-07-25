/* Control background image as user scrolls through sections */
// const sections = document.querySelectorAll('section');
// const backgroundImage = document.getElementById('background-image');

// Removed background image logic since the element no longer exists
// backgroundImage.style.opacity = '.5';  // 50% opacity (50% transparent)

// Use a single imageUrlsByHeading definition for both background and salon image logic
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
  "Demos from event 11": [
    "https://i.postimg.cc/X7t13H4B/IMG-5118.jpg",
    "https://i.postimg.cc/9fYLdcTy/IMG-5138.jpg",
    "https://i.postimg.cc/cLY9JRL9/IMG-5108.jpg"
  ],
};

// Track currently visible section and image cycling
let currentVisibleSection = null;
let cycleIntervalId = null;
let currentImageIndex = 0;

// Intersection Observer to detect when sections are in view (background image logic)
const observerOptions = {
  root: null,
  rootMargin: '0px',
  threshold: 0.5 // At least 50% of the section visible to trigger
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const section = entry.target;
    const eventHeading = section.querySelector('.event-heading');
    if (!eventHeading) return;
    const heading = eventHeading.getAttribute('data-heading');
    const imageUrls = imageUrlsByHeading[heading];
    if (!imageUrls) return;
    if (entry.isIntersecting) {
      // Stop any existing image cycling
      if (cycleIntervalId) {
        clearInterval(cycleIntervalId);
      }
      // Update current visible section
      currentVisibleSection = section;
      currentImageIndex = 0;
      // Set initial image
      // backgroundImage.src = imageUrls[0];
      // backgroundImage.style.opacity = '.5';  // 50% opacity
      // Start cycling images without fade transition
      cycleIntervalId = setInterval(() => {
        currentImageIndex = (currentImageIndex + 1) % imageUrls.length;
        // backgroundImage.src = imageUrls[currentImageIndex];
        // backgroundImage.style.opacity = '.5';  // Keep opacity consistent
      }, 3000);
    } else if (section === currentVisibleSection && !entry.isIntersecting) {
      // If the current section is no longer visible
      if (cycleIntervalId) {
        clearInterval(cycleIntervalId);
        cycleIntervalId = null;
      }
      currentVisibleSection = null;
    }
  });
}, observerOptions);

// Start observing each section
// sections.forEach(section => {
//   observer.observe(section);
// });

// --- Sidebar Navigation Logic ---
const navItems = document.querySelectorAll('.nav-item');
const contentSections = document.querySelectorAll('.content-section');
const salonImageBox = document.getElementById('image-box');
const salonImage = document.getElementById('salon-image');

function showSection(page) {
  contentSections.forEach(section => {
    section.classList.remove('active');
  });
  const activeSection = document.getElementById(`${page}-content`);
  if (activeSection) activeSection.classList.add('active');

  navItems.forEach(item => {
    item.classList.toggle('active', item.dataset.page === page);
  });

  // Clean up any existing observers and intervals
  if (window.salonSectionObserver) {
    window.salonSectionObserver.disconnect();
  }
  if (window.workshopSectionObserver) {
    window.workshopSectionObserver.disconnect();
  }
  if (window.exhibitionSectionObserver) {
    window.exhibitionSectionObserver.disconnect();
  }
  if (window.salonCycleIntervalId) {
    clearInterval(window.salonCycleIntervalId);
    window.salonCycleIntervalId = null;
  }
  if (window.workshopCycleIntervalId) {
    clearInterval(window.workshopCycleIntervalId);
    window.workshopCycleIntervalId = null;
  }
  if (window.exhibitionCycleIntervalId) {
    clearInterval(window.exhibitionCycleIntervalId);
    window.exhibitionCycleIntervalId = null;
  }

  // Show/hide image box and set up appropriate image cycling
  if (page === 'salons') {
    salonImageBox.style.display = '';
    updateSalonImageOnScroll();
  } else if (page === 'workshops') {
    salonImageBox.style.display = '';
    updateWorkshopImageOnScroll();
  } else if (page === 'exhibitions') {
    salonImageBox.style.display = '';
    updateExhibitionImageOnScroll();
  } else {
    salonImageBox.style.display = 'none';
    if (salonImage) salonImage.src = '';
  }
}

navItems.forEach(item => {
  item.addEventListener('click', () => {
    const page = item.dataset.page;
    showSection(page);
    window.history.pushState({ page }, '', page === 'salons' ? '/' : `/${page}`);
  });
});

window.addEventListener('popstate', (e) => {
  const page = (e.state && e.state.page) || (window.location.pathname.replace('/', '') || 'salons');
  showSection(page);
});

// --- Salon Image Scroll Logic ---
const salonSections = document.querySelectorAll('#salons-content section');
let currentSalonSection = null;
let salonCycleIntervalId = null;
let salonCurrentImageIndex = 0;

function fadeToImage(url) {
  if (!salonImage) return;
  salonImage.src = url;
}

function updateSalonImageOnScroll() {
  if (!salonImage) return;
  // Remove any previous observer/interval
  if (window.salonSectionObserver) {
    window.salonSectionObserver.disconnect();
  }
  if (window.salonCycleIntervalId) {
    clearInterval(window.salonCycleIntervalId);
    window.salonCycleIntervalId = null;
  }
  
  // Set up observer with viewport as root for consistent behavior
  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };
  
  window.salonSectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const section = entry.target;
      const eventHeading = section.querySelector('.event-heading');
      if (!eventHeading) return;
      const heading = eventHeading.getAttribute('data-heading');
      const imageUrls = imageUrlsByHeading[heading];
      if (!imageUrls) return;
      if (entry.isIntersecting) {
        // Stop any existing image cycling
        if (window.salonCycleIntervalId) clearInterval(window.salonCycleIntervalId);
        currentSalonSection = section;
        salonCurrentImageIndex = 0;
        fadeToImage(imageUrls[0]);
        // Start cycling images
        if (imageUrls.length > 1) {
          window.salonCycleIntervalId = setInterval(() => {
            salonCurrentImageIndex = (salonCurrentImageIndex + 1) % imageUrls.length;
            fadeToImage(imageUrls[salonCurrentImageIndex]);
          }, 1000);
        }
      } else if (section === currentSalonSection && !entry.isIntersecting) {
        if (window.salonCycleIntervalId) {
          clearInterval(window.salonCycleIntervalId);
          window.salonCycleIntervalId = null;
        }
        currentSalonSection = null;
      }
    });
  }, observerOptions);
  
  salonSections.forEach(section => {
    window.salonSectionObserver.observe(section);
  });
}

// Workshop data and functionality
let workshopsData = null;
const workshopImageUrlsByHeading = {};

// Exhibition data and functionality
let exhibitionsData = null;
const exhibitionImageUrlsByHeading = {};

// Load workshop data
async function loadWorkshopData() {
  try {
    const response = await fetch('/workshops.json');
    workshopsData = await response.json();
    
    // Build image URLs mapping for workshops
    workshopsData.upcoming.forEach(workshop => {
      workshopImageUrlsByHeading[`Workshop: ${workshop.title}`] = [workshop.flyer, ...workshop.images];
    });
    
    workshopsData.past.forEach(workshop => {
      // For past workshops, only use the images array (not the flyer)
      workshopImageUrlsByHeading[`Workshop: ${workshop.title}`] = workshop.images;
    });
    
    // Merge with existing image URLs
    Object.assign(imageUrlsByHeading, workshopImageUrlsByHeading);
    
    renderWorkshops();
  } catch (error) {
    console.error('Error loading workshop data:', error);
  }
}

// Load exhibition data
async function loadExhibitionData() {
  try {
    const response = await fetch('/exhibitions.json');
    exhibitionsData = await response.json();
    
    // Build image URLs mapping for exhibitions
    exhibitionsData.upcoming.forEach(exhibition => {
      exhibitionImageUrlsByHeading[`Exhibition: ${exhibition.title}`] = [exhibition.flyer, ...exhibition.images];
    });
    
    exhibitionsData.past.forEach(exhibition => {
      // For past exhibitions, only use the images array (not the flyer)
      exhibitionImageUrlsByHeading[`Exhibition: ${exhibition.title}`] = exhibition.images;
    });
    
    // Merge with existing image URLs
    Object.assign(imageUrlsByHeading, exhibitionImageUrlsByHeading);
    
    renderExhibitions();
  } catch (error) {
    console.error('Error loading exhibition data:', error);
  }
}

function renderWorkshops() {
  if (!workshopsData) return;
  
  const upcomingContainer = document.getElementById('upcoming-workshops');
  const pastContainer = document.getElementById('past-workshops');
  
  if (upcomingContainer) {
    upcomingContainer.innerHTML = workshopsData.upcoming.map(workshop => `
      <div class="workshop-item" data-workshop-id="${workshop.id}">
        <a href="${workshop.link || 'javascript:void(0)'}" class="workshop-heading" data-heading="Workshop: ${workshop.title}" ${workshop.link ? 'target="_blank"' : ''}>
          <div class="workshop-header">
            <img src="${workshop.flyer}" alt="${workshop.title}" class="workshop-flyer" />
            <div class="workshop-info">
              <h3>${workshop.title}</h3>
              <p>${workshop.description}</p>
              <div class="workshop-date">
                <span>${workshop.date === 'TBD' ? 'TBD' : formatDate(workshop.date)}</span>
                <span>${workshop.time === 'TBD' ? '' : workshop.time}</span>
              </div>
            </div>
          </div>
        </a>
      </div>
    `).join('');
  }
  
  if (pastContainer) {
    pastContainer.innerHTML = workshopsData.past.map(workshop => `
      <div class="workshop-item" data-workshop-id="${workshop.id}">
        <a href="${workshop.link || 'javascript:void(0)'}" class="workshop-heading" data-heading="Workshop: ${workshop.title}" ${workshop.link ? 'target="_blank"' : ''}>
          <div class="workshop-header">
            <img src="${workshop.flyer}" alt="${workshop.title}" class="workshop-flyer" />
            <div class="workshop-info">
              <h3>${workshop.title}</h3>
              <p>${workshop.description}</p>
            </div>
          </div>
        </a>
      </div>
    `).join('');
  }
  
  // If we're on the workshops page, set up image cycling
  if (document.getElementById('workshops-content').classList.contains('active')) {
    updateWorkshopImageOnScroll();
  }
}

function renderExhibitions() {
  if (!exhibitionsData) return;
  
  const upcomingContainer = document.getElementById('upcoming-exhibitions');
  const pastContainer = document.getElementById('past-exhibitions');
  
  if (upcomingContainer) {
    upcomingContainer.innerHTML = exhibitionsData.upcoming.map(exhibition => `
      <div class="exhibition-item" data-exhibition-id="${exhibition.id}">
        <a href="${exhibition.link || 'javascript:void(0)'}" class="exhibition-heading" data-heading="Exhibition: ${exhibition.title}" ${exhibition.link ? 'target="_blank"' : ''}>
          <div class="exhibition-header">
            <img src="${exhibition.flyer}" alt="${exhibition.title}" class="exhibition-flyer" />
            <div class="exhibition-info">
              <h3>${exhibition.title}</h3>
              <p>${exhibition.description}</p>
              <div class="exhibition-date">
                <span>${exhibition.date === 'TBD' ? 'TBD' : formatDate(exhibition.date)}</span>
                <span>${exhibition.time === 'TBD' ? '' : exhibition.time}</span>
              </div>
            </div>
          </div>
        </a>
      </div>
    `).join('');
  }
  
  if (pastContainer) {
    pastContainer.innerHTML = exhibitionsData.past.map(exhibition => `
      <div class="exhibition-item" data-exhibition-id="${exhibition.id}">
        <a href="${exhibition.link || 'javascript:void(0)'}" class="exhibition-heading" data-heading="Exhibition: ${exhibition.title}" ${exhibition.link ? 'target="_blank"' : ''}>
          <div class="exhibition-header">
            <img src="${exhibition.flyer}" alt="${exhibition.title}" class="exhibition-flyer" />
            <div class="exhibition-info">
              <h3>${exhibition.title}</h3>
              <p>${exhibition.description}</p>
            </div>
          </div>
        </a>
      </div>
    `).join('');
  }
  
  // If we're on the exhibitions page, set up image cycling
  if (document.getElementById('exhibitions-content').classList.contains('active')) {
    updateExhibitionImageOnScroll();
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
}



// Workshop image scroll logic
function updateWorkshopImageOnScroll() {
  if (!salonImage) return;
  
  // Remove any previous observer/interval
  if (window.workshopSectionObserver) {
    window.workshopSectionObserver.disconnect();
  }
  if (window.workshopCycleIntervalId) {
    clearInterval(window.workshopCycleIntervalId);
    window.workshopCycleIntervalId = null;
  }
  
  // Wait a bit for workshops to render, then set up observer
  setTimeout(() => {
    // Only observe past workshops, not upcoming ones
    const pastWorkshopSections = document.querySelectorAll('#past-workshops .workshop-heading');
    console.log('Found past workshop sections:', pastWorkshopSections.length);
    
    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    };
    
    window.workshopSectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const heading = entry.target.getAttribute('data-heading');
        const imageUrls = imageUrlsByHeading[heading];
        console.log('Workshop heading:', heading, 'Image URLs:', imageUrls);
        
        if (!imageUrls) return;
        
        if (entry.isIntersecting) {
          if (window.workshopCycleIntervalId) clearInterval(window.workshopCycleIntervalId);
          salonCurrentImageIndex = 0;
          fadeToImage(imageUrls[0]);
          
          if (imageUrls.length > 1) {
            window.workshopCycleIntervalId = setInterval(() => {
              salonCurrentImageIndex = (salonCurrentImageIndex + 1) % imageUrls.length;
              fadeToImage(imageUrls[salonCurrentImageIndex]);
            }, 1000);
          }
        }
      });
    }, observerOptions);
    
    pastWorkshopSections.forEach(section => {
      window.workshopSectionObserver.observe(section);
    });
  }, 100);
}

// Exhibition image scroll logic
function updateExhibitionImageOnScroll() {
  if (!salonImage) return;
  
  // Remove any previous observer/interval
  if (window.exhibitionSectionObserver) {
    window.exhibitionSectionObserver.disconnect();
  }
  if (window.exhibitionCycleIntervalId) {
    clearInterval(window.exhibitionCycleIntervalId);
    window.exhibitionCycleIntervalId = null;
  }
  
  // Wait a bit for exhibitions to render, then set up observer
  setTimeout(() => {
    // Only observe past exhibitions, not upcoming ones
    const pastExhibitionSections = document.querySelectorAll('#past-exhibitions .exhibition-heading');
    console.log('Found past exhibition sections:', pastExhibitionSections.length);
    
    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    };
    
    window.exhibitionSectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const heading = entry.target.getAttribute('data-heading');
        const imageUrls = imageUrlsByHeading[heading];
        console.log('Exhibition heading:', heading, 'Image URLs:', imageUrls);
        
        if (!imageUrls) return;
        
        if (entry.isIntersecting) {
          if (window.exhibitionCycleIntervalId) clearInterval(window.exhibitionCycleIntervalId);
          salonCurrentImageIndex = 0;
          fadeToImage(imageUrls[0]);
          
          if (imageUrls.length > 1) {
            window.exhibitionCycleIntervalId = setInterval(() => {
              salonCurrentImageIndex = (salonCurrentImageIndex + 1) % imageUrls.length;
              fadeToImage(imageUrls[salonCurrentImageIndex]);
            }, 1000);
          }
        }
      });
    }, observerOptions);
    
    pastExhibitionSections.forEach(section => {
      window.exhibitionSectionObserver.observe(section);
    });
  }, 100);
}

// On load, show the correct section based on URL
(function initPageFromUrl() {
  const path = window.location.pathname.replace('/', '') || 'salons';
  showSection(path);
  loadWorkshopData();
  loadExhibitionData();
})();
