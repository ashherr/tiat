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
        """Generate the home page with salons based on the original salons.html"""
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>the intersection of art & technology</title>
            <style>
                body {{
                    font-family: 'Kosugi', sans-serif;
                    margin: 20px;
                    font-size: 14px;
                    line-height: 1.5;
                }}
                h1 {{ 
                    font-size: 26px; 
                    margin-top: 30px;
                }}
                h2 {{
                    font-size: 18px;
                    margin-top: 30px;
                }}
                main {{
                    max-width: 800px;
                    margin: 0 auto;
                }}
                table {{
                    margin-top: 15px;
                    border-collapse: collapse;
                    width: 100%;
                }}
                table td {{
                    padding: 5px 10px;
                    vertical-align: top;
                }}
                section {{
                    margin-bottom: 40px;
                }}
                .event-heading {{
                    text-decoration: none;
                    color: black;
                }}
                a {{
                    color: #000;
                }}
                
                /* Recovery notice */
                .recovery-notice {{
                    background-color: #d4edda;
                    color: #155724;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                    text-align: center;
                }}
                
                /* Navigation */
                .nav {{
                    display: flex;
                    margin: 20px 0;
                }}
                .nav a {{
                    margin-right: 15px;
                    text-decoration: none;
                    padding: 5px 10px;
                    background: #f1f1f1;
                    border-radius: 3px;
                }}
            </style>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Kosugi&display=swap" rel="stylesheet">
            
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id=G-MCCV52KT3X"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){{dataLayer.push(arguments);}}
              gtag('js', new Date());
            
              gtag('config', 'G-MCCV52KT3X');
            </script>
        </head>

        <body>
            <main>
                <div class="header"></div>
                <br> <br>
                
                <h1>tiat salons</h1>
                
                <div class="recovery-notice">
                    <strong>Recovery Mode:</strong> The site is being rebuilt with a new structure. Salons are now on the home page.
                </div>
                
                <div class="nav">
                    <a href="/">Salons</a>
                    <a href="/events">Events</a>
                    <a href="/submit">Submit</a>
                    <a href="/recovery">Status</a>
                </div>
                
                <p>
                    art demos for the creative technologists in sf. 
                </p>
                
                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 11"
                    >
                      <h2> tiat 11</h2>
                      <div class="image-container">
                        
                      </div>
                    </a>

                    <p>the next tiat is on May 4th, 2025 at 7pm. <a href="https://lu.ma/w2xi3u4p">RSVP here</a></p>
                </section>

                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 10"
                    >
                      <h2> tiat 10</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 10" class="event-image" />
                      </div>
                    </a>

                    <p><a href="https://www.youtube.com/watch?v=brfgTr0PJvg">watch the recording</a></p>

                    <table>
                      <colgroup>
                        <col style="width: 45%;">
                        <col style="width: 55%;">
                      </colgroup>
                      <tr>
                        <td>latent fields</td>
                        <td>​rishi pandey</td>
                      </tr>
                      <tr>
                        <td>music explorer / little guy</td>
                        <td>daniel kuntz</td>
                      </tr>
                      <tr>
                        <td>rat dating simulator</td>
                        <td>connie ye</td>
                      </tr>
                      <tr>
                        <td>a poem</td>
                        <td>alicia guo</td>
                      </tr>
                      <tr>
                        <td>roombavision</td>
                        <td>taylor tabb & adnan aga</td>
                      </tr>
                      <tr>
                        <td>square powder claw</td>
                        <td>halim madi</td>
                      </tr>
                      <tr>
                        <td>vocoder</td>
                        <td>julip</td>
                      </tr>
                      <tr>
                        <td>latent space image variation</td>
                        <td>gray crawford</td>
                      </tr>
                      <tr>
                        <td>kiko</td>
                        <td>kyt</td>
                      </tr>
                      <tr></tr>
                        <td>lasers are the message</td>
                        <td>brendan luu</td>
                      </tr>
                    </table>
                </section>

                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 9"
                    >
                      <h2> tiat 9</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 9" class="event-image" />
                      </div>
                    </a>

                    <p><a href="https://www.youtube.com/watch?v=Y0HBiyo3W48">watch the recording</a></p>

                    <table>
                      <colgroup>
                        <col style="width: 45%;">
                        <col style="width: 55%;">
                      </colgroup>
                      <tr>
                        <td>body language</td>
                        <td>ash herr</td>
                      </tr>
                      <tr>
                        <td>AcknowledgeNET</td>
                        <td>spencer chang</td>
                      </tr>
                      <tr>
                        <td>knit soundscape/memory</td>
                        <td>jessica kim</td>
                      </tr>
                      <tr>
                        <td>bop spotter</td>
                        <td>riley walz</td>
                      </tr>
                      <tr>
                        <td>ratatouille irl</td>
                        <td>athena leong</td>
                      </tr>
                      <tr>
                        <td>strange loops</td>
                        <td>ninon hollanderski </td>
                      </tr>
                      <tr>
                        <td>advice line proj</td>
                        <td>danielle egan</td>
                      </tr>
                      <tr>
                        <td>duump site</td>
                        <td>ven qiu</td>
                      </tr>
                      <tr>
                        <td>daily sketching</td>
                        <td>zach lieberman</td>
                      </tr>
                      <tr></tr>
                        <td>himala (miracle)</td>
                        <td>chia amisola</td>
                      </tr>
                    </table>
                </section>
                
                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 8"
                    >
                      <h2> tiat 8</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 8" class="event-image" />
                      </div>
                    </a>

                    <p><a href="https://www.youtube.com/watch?v=dBErFlHfc8w">watch the recording</a></p>

                    <table>
                      <colgroup>
                        <col style="width: 45%;">
                        <col style="width: 55%;">
                      </colgroup>
                      <tr>
                        <td>anti-aging software</td>
                        <td>ash herr</td>
                      </tr>
                      <tr>
                        <td>music millennium</td>
                        <td>melisa seah</td>
                      </tr>
                      <tr>
                        <td>UR-AURA</td>
                        <td>sharon zheng</td>
                      </tr>
                      <tr>
                        <td>we called us poetry</td>
                        <td>halim madi</td>
                      </tr>
                      <tr>
                        <td>chinese cyberfeminism archive</td>
                        <td>crassula shang</td>
                      </tr>
                      <tr>
                        <td>biotopy</td>
                        <td>​​darren zhu</td>
                      </tr>
                      <tr>
                        <td>random drums</td>
                        <td>​jeanette andrews</td>
                      </tr>
                      <tr>
                        <td>1-bit halftone thermal printing</td>
                        <td>evan sirchuk</td>
                      </tr>
                      <tr>
                        <td>binaural tuner</td>
                        <td>dan gorelick</td>
                      </tr>
                      <tr>
                        <td>and you'll miss it</td>
                        <td>henry tran</td>
                      </tr>
                    </table>
                </section>

                <footer>
                    <br><br><br><br>
                    <p>
                      questions? reach out to
                      <a href="https://imempowa.com/">ash</a>
                    </p>
                </footer>
            </main>
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