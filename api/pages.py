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
            
            <!-- Interactive features for salon listings -->
            <script>
              document.addEventListener("DOMContentLoaded", function() {{
                // Add event listeners for salon headings
                const eventHeadings = document.querySelectorAll('.event-heading');
                
                eventHeadings.forEach(heading => {{
                  heading.addEventListener('click', function() {{
                    const headingText = this.getAttribute('data-heading');
                    console.log(`Clicked on: ${{headingText}}`);
                    
                    // Find and toggle the table following this heading
                    const section = this.closest('section');
                    const table = section.querySelector('table');
                    if (table) {{
                      table.style.display = table.style.display === 'none' ? 'table' : 'none';
                    }}
                  }});
                }});
                
                // Smooth scrolling for anchor links
                document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                  anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    
                    const targetId = this.getAttribute('href');
                    if (targetId === '#') return;
                    
                    const targetElement = document.querySelector(targetId);
                    if (targetElement) {{
                      targetElement.scrollIntoView({{
                        behavior: 'smooth'
                      }});
                    }}
                  }});
                }});
              }});
            </script>
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
            <link rel="stylesheet" href="/static/style.css">
            
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
            
            <!-- Interactive features -->
            <script src="/static/main.js"></script>
            <script src="/static/images.js"></script>
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
                        <img src="" alt="Images from event 11" class="event-image" />
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

                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 7"
                    >
                      <h2>tiat 7</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 7" class="event-image" />
                      </div>
                    </a>

                    <table>
                      <colgroup>
                        <col style="width: 45%;">
                        <col style="width: 55%;">
                      </colgroup>
                      <tr>
                        <td>vent</td>
                        <td>ash herr</td>
                      </tr>
                      <tr>
                        <td>ratio</td>
                        <td>​johan ismael / david grunzweig</td>
                      </tr>
                      <tr>
                        <td>fred again app</td>
                        <td>claire wang</td>
                      </tr>
                      <tr>
                        <td>everything interface</td>
                        <td>alessio grancini</td>
                      </tr>
                      <tr>
                        <td>qigong, magic wave</td>
                        <td>koi ren</td>
                      </tr>
                      <tr>
                        <td>hotvinebhotline</td>
                        <td>taylor tabb</td>
                      </tr>
                    </table>
                </section>

                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 6"
                    >
                      <h2>tiat 6</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 6" class="event-image" />
                      </div>
                    </a>

                    <table>
                      <colgroup>
                        <col style="width: 45%;">
                        <col style="width: 55%;">
                      </colgroup>
                      <tr>
                        <td>diffusion grown card decks</td>
                        <td>marisa lu</td>
                      </tr>
                      <tr>
                        <td>garden of ancients</td>
                        <td>jeffrey yip</td>
                      </tr>
                      <tr>
                        <td>breathe together</td>
                        <td>megan van weilie</td>
                      </tr>
                      <tr>
                        <td>data sensing toolkit</td>
                        <td>scott kildall</td>
                      </tr>
                      <tr>
                        <td>GPT-me</td>
                        <td>avital meshi</td>
                      </tr>
                      <tr>
                        <td>dataset butoh</td>
                        <td>noah aust</td>
                      </tr>
                      <tr>
                        <td>fluid sculpture</td>
                        <td>danny so-haeg</td>
                      </tr>
                      <tr>
                        <td>synesthetic perceptions</td>
                        <td>amanda yeh</td>
                      </tr>
                      <tr>
                        <td>last seen online</td>
                        <td>henry tran</td>
                      </tr>
                      <tr>
                        <td>body output digital interface</td>
                        <td>taylor tabb</td>
                      </tr>
                      <tr>
                        <td>cyber taoism dream - zhuangzi's butterfly inception</td>
                        <td>lin xinye</td>
                      </tr>
                      <tr>
                        <td>call this # now</td>
                        <td>cole ryder</td>
                      </tr>
                    </table>
                </section>

                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 5"
                    >
                      <h2>tiat 5</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 5" class="event-image" />
                      </div>
                    </a>

                    <table>
                      <tr>
                        <td>you're never lonely on wikipedia</td>
                        <td>ash herr</td>
                      </tr>
                      <tr>
                        <td>improv</td>
                        <td>joe baker</td>
                      </tr>
                      <tr>
                        <td>flow fields</td>
                        <td>rishi pandey</td>
                      </tr>
                      <tr>
                        <td>dis//continuity</td>
                        <td>joey verbeke</td>
                      </tr>
                      <tr>
                        <td>reVerb</td>
                        <td>sara</td>
                      </tr>
                      <tr>
                        <td>shapes at play</td>
                        <td>bonnie pham</td>
                      </tr>
                      <tr>
                        <td>elevator pitch</td>
                        <td>marc</td>
                      </tr>
                      <tr>
                        <td>ai drawing experiments</td>
                        <td>james hurlburt</td>
                      </tr>
                      <tr>
                        <td>visual synth experiments</td>
                        <td>koven kawandeep</td>
                      </tr>
                      <tr>
                        <td>the healing room</td>
                        <td>mingzhu heseri</td>
                      </tr>
                      <tr>
                        <td>church of GPT</td>
                        <td>zain shah</td>
                      </tr>
                      <tr>
                        <td>mid conversation</td>
                        <td>leia chang</td>
                      </tr>
                    </table>
                </section>

                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 4"
                    >
                      <h2>tiat 4</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 4" class="event-image" />
                      </div>
                    </a>

                    <table>
                      <tr>
                        <td>resonant frequency</td>
                        <td>joe baker</td>
                      </tr>
                      <tr>
                        <td>spider trap</td>
                        <td>sri</td>
                      </tr>
                      <tr>
                        <td>overruled</td>
                        <td>cody</td>
                      </tr>
                      <tr>
                        <td>dawn</td>
                        <td>ritwik</td>
                      </tr>
                      <tr>
                        <td>lumi</td>
                        <td>vignesh rajmohan</td>
                      </tr>
                      <tr>
                        <td>candle !holder</td>
                        <td>leia chang</td>
                      </tr>
                      <tr>
                        <td>memory, love, and the handmade</td>
                        <td>alexa ann bonomo</td>
                      </tr>
                      <tr>
                        <td>bespoke</td>
                        <td>evan dorsky</td>
                      </tr>
                      <tr>
                        <td>sound werkshop</td>
                        <td>chris guichet</td>
                      </tr>
                    </table>
                </section>

                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 3"
                    >
                      <h2>tiat 3</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 3" class="event-image" />
                      </div>
                    </a>

                    <table>
                      <tr>
                        <td>simulated validation</td>
                        <td>henry tran</td>
                      </tr>
                      <tr>
                        <td>bitcube</td>
                        <td>justine sun dela cruz</td>
                      </tr>
                      <tr>
                        <td>musai</td>
                        <td>jake mclain</td>
                      </tr>
                      <tr>
                        <td>letters from a stranger</td>
                        <td>mylene tu</td>
                      </tr>
                      <tr>
                        <td>light + code experiments</td>
                        <td>dan gorelick</td>
                      </tr>
                      <tr>
                        <td>light it up</td>
                        <td>marisa lu</td>
                      </tr>
                    </table>
                </section>

                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 2"
                    >
                      <h2>tiat 2</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 2" class="event-image" />
                      </div>
                    </a>

                    <table>
                      <tr>
                        <td>dataviz</td>
                        <td>ara</td>
                      </tr>
                      <tr>
                        <td>huddler</td>
                        <td>jordan</td>
                      </tr>
                      <tr>
                        <td>break</td>
                        <td>eric lum</td>
                      </tr>
                      <tr>
                        <td>impulse</td>
                        <td>daniel</td>
                      </tr>
                      <tr>
                        <td>wide views</td>
                        <td>gray crawford</td>
                      </tr>
                      <tr>
                        <td>acrylic</td>
                        <td>celeste</td>
                      </tr>
                      <tr>
                        <td>projects</td>
                        <td>mitch chaiet</td>
                      </tr>
                    </table>
                </section>

                <section>
                    <a
                      href="javascript:void(0)"
                      class="event-heading"
                      data-heading="Demos from event 1"
                    >
                      <h2>tiat 1</h2>
                      <div class="image-container">
                        <img src="" alt="Images from event 1" class="event-image" />
                      </div>
                    </a>

                    <table>
                      <tr>
                        <td>coffee sada</td>
                        <td>ali</td>
                      </tr>
                      <tr>
                        <td>dating gpt</td>
                        <td>henry tran</td>
                      </tr>
                      <tr>
                        <td>streamwork</td>
                        <td>jared hsu</td>
                      </tr>
                      <tr>
                        <td>dial gpt</td>
                        <td>george</td>
                      </tr>
                      <tr>
                        <td>mit: regressions</td>
                        <td>luke igel</td>
                      </tr>
                      <tr>
                        <td>latent expressionism</td>
                        <td>nicholas bardy</td>
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
            <div id="cursor-chat-layer">
              <input type="text" id="cursor-chat-box" />
            </div>
            <!-- install playhtml -->
            <script type="module" src="https://unpkg.com/playhtml"></script>
            <link rel="stylesheet" href="https://unpkg.com/playhtml/dist/style.css" />
            <!-- install cursor chat -->
            <script type="module">
              import { initCursorChat } from "https://esm.sh/cursor-chat";
              initCursorChat(window.location.href);
            </script>
            <link
              rel="stylesheet"
              type="text/css"
              href="https://unpkg.com/cursor-chat/dist/style.css"
            />
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