from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip('/')
        
        # Set response headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Serve the appropriate page based on path
        if path == '' or path == 'index' or path == 'home':
            content = self.get_home_page()
        elif path == 'events':
            content = self.get_events_page()
        elif path == 'submit':
            content = self.get_submit_page()
        else:
            content = self.get_not_found_page(path)
        
        self.wfile.write(content.encode())
        return
    
    def get_common_head(self, title):
        """Generate the common head section for all pages"""
        return f"""
        <head>
            <title>TIAT - {title}</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    line-height: 1.6; 
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                header {{ 
                    background-color: #f8f9fa;
                    border-bottom: 1px solid #e9ecef;
                    padding: 15px 0;
                    text-align: center;
                }}
                h1, h2, h3 {{ color: #333; margin-top: 0; }}
                .notice {{ 
                    padding: 15px; 
                    border-radius: 5px; 
                    margin-bottom: 20px; 
                    text-align: center;
                }}
                .success {{ background-color: #d4edda; color: #155724; }}
                .warning {{ background-color: #fff3cd; color: #856404; }}
                nav {{ 
                    display: flex; 
                    justify-content: center;
                    margin: 15px 0;
                }}
                nav a {{ 
                    margin: 0 10px; 
                    text-decoration: none; 
                    padding: 8px 16px; 
                    background: #f1f1f1; 
                    border-radius: 4px;
                    color: #333;
                    font-weight: bold;
                }}
                nav a:hover {{ background-color: #e0e0e0; }}
                .salon {{ 
                    background-color: #f9f9f9;
                    padding: 20px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                    border-left: 4px solid #6c757d;
                }}
                .event-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                    gap: 20px;
                }}
                .event-card {{
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .event-image {{
                    width: 100%;
                    height: 180px;
                    background-color: #f1f1f1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .event-details {{
                    padding: 15px;
                }}
                .form-group {{
                    margin-bottom: 15px;
                }}
                label {{
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                }}
                input, textarea, select {{
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    box-sizing: border-box;
                }}
                button {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }}
                footer {{
                    text-align: center;
                    padding: 20px;
                    border-top: 1px solid #e9ecef;
                    margin-top: 40px;
                }}
            </style>
        </head>
        """
    
    def get_header(self):
        """Generate the common header with navigation"""
        return """
        <header>
            <div class="container">
                <h1>Technology in Art (TIAT)</h1>
                <div class="notice success">
                    <strong>Recovery Mode:</strong> The site is running with limited functionality while we rebuild.
                </div>
                <nav>
                    <a href="/">Salons</a>
                    <a href="/events">Events</a>
                    <a href="/submit">Submit Event</a>
                    <a href="/recovery">Status</a>
                </nav>
            </div>
        </header>
        """
    
    def get_footer(self):
        """Generate the common footer"""
        return """
        <footer>
            <div class="container">
                <p>TIAT - Technology in Art | <a href="/status">Status</a> | <a href="/recovery">Recovery Info</a></p>
            </div>
        </footer>
        """
    
    def get_home_page(self):
        """Generate the home page with salons"""
        return f"""
        <!DOCTYPE html>
        <html>
        {self.get_common_head("Salons")}
        <body>
            {self.get_header()}
            
            <div class="container">
                <h2>Upcoming Salons</h2>
                <p>Technology in Art Salons (TIAT) are hosted gatherings where artists, technologists, and creators come together to share ideas, collaborate, and explore the intersection of technology and art.</p>
                
                <div class="salon">
                    <h3>AI in Visual Arts</h3>
                    <p><strong>Date:</strong> November 15, 2023</p>
                    <p><strong>Location:</strong> San Francisco - Gallery 16</p>
                    <p>Join us for a discussion on how artificial intelligence is transforming visual arts. Artists will share their experiences working with AI tools like DALL-E, Midjourney, and Stable Diffusion.</p>
                </div>
                
                <div class="salon">
                    <h3>Interactive Installations Workshop</h3>
                    <p><strong>Date:</strong> December 3, 2023</p>
                    <p><strong>Location:</strong> Berkeley - The Annex</p>
                    <p>A hands-on workshop exploring the creation of interactive art installations using sensors, microcontrollers, and projection mapping techniques.</p>
                </div>
                
                <div class="salon">
                    <h3>NFTs and Digital Ownership</h3>
                    <p><strong>Date:</strong> December 18, 2023</p>
                    <p><strong>Location:</strong> Oakland - Tech Hub</p>
                    <p>A panel discussion on the current state of NFTs and digital ownership in the art world. What's working, what's not, and where do we go from here?</p>
                </div>
                
                <div class="notice warning">
                    <p>Want to host a salon? <a href="/submit">Submit your proposal here</a>.</p>
                </div>
            </div>
            
            {self.get_footer()}
        </body>
        </html>
        """
    
    def get_events_page(self):
        """Generate the events page"""
        return f"""
        <!DOCTYPE html>
        <html>
        {self.get_common_head("Events")}
        <body>
            {self.get_header()}
            
            <div class="container">
                <h2>Upcoming Events</h2>
                <p>Discover art and technology events happening in the Bay Area. From exhibitions to workshops, performances to hackathons - find events at the intersection of creativity and technology.</p>
                
                <div class="event-grid">
                    <div class="event-card">
                        <div class="event-image">
                            <img src="https://via.placeholder.com/300" alt="Gray Area Festival" style="max-width:100%;">
                        </div>
                        <div class="event-details">
                            <h3>Gray Area Festival</h3>
                            <p><strong>Date:</strong> October 20-22, 2023</p>
                            <p><strong>Location:</strong> San Francisco</p>
                            <p>Annual festival of art, technology, and culture featuring performances, installations, and talks.</p>
                        </div>
                    </div>
                    
                    <div class="event-card">
                        <div class="event-image">
                            <img src="https://via.placeholder.com/300" alt="Digital Art Exhibition" style="max-width:100%;">
                        </div>
                        <div class="event-details">
                            <h3>Digital Art Exhibition</h3>
                            <p><strong>Date:</strong> November 5, 2023</p>
                            <p><strong>Location:</strong> San Jose</p>
                            <p>Exhibition showcasing works from digital artists pushing the boundaries of technology in art.</p>
                        </div>
                    </div>
                    
                    <div class="event-card">
                        <div class="event-image">
                            <img src="https://via.placeholder.com/300" alt="Creative Coding Workshop" style="max-width:100%;">
                        </div>
                        <div class="event-details">
                            <h3>Creative Coding Workshop</h3>
                            <p><strong>Date:</strong> November 12, 2023</p>
                            <p><strong>Location:</strong> Berkeley</p>
                            <p>Learn the basics of creative coding with p5.js in this beginner-friendly workshop.</p>
                        </div>
                    </div>
                </div>
                
                <div class="notice warning">
                    <p>Have an event to share? <a href="/submit">Submit it here</a>.</p>
                </div>
            </div>
            
            {self.get_footer()}
        </body>
        </html>
        """
    
    def get_submit_page(self):
        """Generate the submit event/salon page"""
        return f"""
        <!DOCTYPE html>
        <html>
        {self.get_common_head("Submit")}
        <body>
            {self.get_header()}
            
            <div class="container">
                <h2>Submit an Event or Salon</h2>
                
                <div class="notice warning">
                    <strong>Note:</strong> Submission is currently disabled during recovery mode. This form is for display purposes only.
                </div>
                
                <form action="#" method="post" style="max-width: 600px; margin: 0 auto;">
                    <div class="form-group">
                        <label for="type">Submission Type</label>
                        <select id="type" name="type" required disabled>
                            <option value="">Select type...</option>
                            <option value="event">Event</option>
                            <option value="salon">Salon</option>
                        </select>
                    </div>
                
                    <div class="form-group">
                        <label for="title">Title</label>
                        <input type="text" id="title" name="title" required disabled>
                    </div>
                    
                    <div class="form-group">
                        <label for="start_time">Start Time</label>
                        <input type="datetime-local" id="start_time" name="start_time" required disabled>
                    </div>
                    
                    <div class="form-group">
                        <label for="end_time">End Time</label>
                        <input type="datetime-local" id="end_time" name="end_time" required disabled>
                    </div>
                    
                    <div class="form-group">
                        <label for="location">Location</label>
                        <input type="text" id="location" name="location" required disabled>
                    </div>
                    
                    <div class="form-group">
                        <label for="description">Description</label>
                        <textarea id="description" name="description" rows="4" required disabled></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="image_url">Image URL</label>
                        <input type="url" id="image_url" name="image_url" disabled>
                    </div>
                    
                    <div class="form-group">
                        <label for="event_link">Website/Event Link</label>
                        <input type="url" id="event_link" name="event_link" disabled>
                    </div>
                    
                    <div class="form-group">
                        <label for="organizer_email">Organizer Email</label>
                        <input type="email" id="organizer_email" name="organizer_email" required disabled>
                    </div>
                    
                    <button type="submit" disabled>Submit</button>
                </form>
            </div>
            
            {self.get_footer()}
        </body>
        </html>
        """
    
    def get_not_found_page(self, path):
        """Generate a 404 page"""
        return f"""
        <!DOCTYPE html>
        <html>
        {self.get_common_head("Page Not Found")}
        <body>
            {self.get_header()}
            
            <div class="container" style="text-align: center; padding: 50px 0;">
                <h2>Page Not Found</h2>
                <p>The page you're looking for <strong>/{path}</strong> doesn't exist.</p>
                <p>Please use the navigation menu to find what you're looking for.</p>
            </div>
            
            {self.get_footer()}
        </body>
        </html>
        """ 