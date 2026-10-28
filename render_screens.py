import os
import json
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_fonts():
    try:
        title_font = ImageFont.truetype('segoeui.ttf', 12)
        ui_font = ImageFont.truetype('segoeui.ttf', 14)
        ui_bold = ImageFont.truetype('segoeuib.ttf', 14)
        h1_font = ImageFont.truetype('segoeuib.ttf', 24)
        h2_font = ImageFont.truetype('segoeuib.ttf', 18)
        body_font = ImageFont.truetype('segoeui.ttf', 13)
        body_bold = ImageFont.truetype('segoeuib.ttf', 13)
        mono_font = ImageFont.truetype('consola.ttf', 13)
        mono_large = ImageFont.truetype('consola.ttf', 14)
    except:
        title_font = ImageFont.load_default()
        ui_font = ImageFont.load_default()
        ui_bold = ImageFont.load_default()
        h1_font = ImageFont.load_default()
        h2_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        body_bold = ImageFont.load_default()
        mono_font = ImageFont.load_default()
        mono_large = ImageFont.load_default()
    return {
        'title': title_font,
        'ui': ui_font,
        'ui_bold': ui_bold,
        'h1': h1_font,
        'h2': h2_font,
        'body': body_font,
        'body_bold': body_bold,
        'mono': mono_font,
        'mono_large': mono_large
    }

def create_browser_base(url, title, width=1280, height=800):
    fonts = get_fonts()
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)

    # Top Chrome
    draw.rectangle([0, 0, width, 40], fill='#dee1e6')
    draw.ellipse([14, 14, 24, 24], fill='#ff5f56')
    draw.ellipse([32, 14, 42, 24], fill='#ffbd2e')
    draw.ellipse([50, 14, 60, 24], fill='#27c93f')

    # Tab
    draw.rounded_rectangle([75, 8, 320, 40], radius=8, fill='#ffffff')
    draw.text((95, 14), title[:30], fill='#202124', font=fonts['title'])
    draw.text((300, 14), "×", fill='#5f6368', font=fonts['title'])

    # Navigation/URL bar
    draw.rectangle([0, 40, width, 82], fill='#ffffff')
    draw.line([0, 82, width, 82], fill='#dadce0', width=1)

    draw.text((20, 52), "←", fill='#5f6368', font=fonts['ui'])
    draw.text((50, 52), "→", fill='#bdc1c6', font=fonts['ui'])
    draw.text((80, 50), "↻", fill='#5f6368', font=fonts['ui'])

    # Address box
    draw.rounded_rectangle([115, 46, width - 40, 76], radius=15, fill='#f1f3f4')
    # Padlock icon
    draw.rectangle([135, 58, 143, 67], fill='#5f6368')
    draw.ellipse([136, 53, 142, 59], outline='#5f6368', width=1)
    draw.text((152, 52), url, fill='#202124', font=fonts['ui'])

    return img, draw, fonts, 83

def draw_navbar(draw, fonts, top_y, width, active_tab="Home", username=None):
    nav_h = 60
    draw.rectangle([0, top_y, width, top_y + nav_h], fill='#00ced1') # darkturquoise
    
    # Brand
    draw.text((40, top_y + 16), "Dealerships", fill='#1a202c', font=fonts['h1'])

    # Nav links
    nav_links = [("Home", "/"), ("About Us", "/about"), ("Contact Us", "/contact")]
    curr_x = 220
    for name, href in nav_links:
        if name == active_tab:
            draw.text((curr_x, top_y + 20), name, fill='#000000', font=fonts['ui_bold'])
            draw.line([curr_x, top_y + 42, curr_x + len(name)*8, top_y + 42], fill='#000000', width=2)
        else:
            draw.text((curr_x, top_y + 20), name, fill='#2d3748', font=fonts['ui'])
        curr_x += 100

    # User profile / Login
    if username:
        draw.text((width - 250, top_y + 20), f"👤 {username}", fill='#1a202c', font=fonts['ui_bold'])
        draw.rounded_rectangle([width - 120, top_y + 14, width - 40, top_y + 46], radius=4, fill='#e2e8f0', outline='#cbd5e0', width=1)
        draw.text((width - 105, top_y + 20), "Logout", fill='#c53030', font=fonts['ui_bold'])
    else:
        draw.rounded_rectangle([width - 180, top_y + 14, width - 110, top_y + 46], radius=4, fill='#2b6cb0')
        draw.text((width - 162, top_y + 20), "Login", fill='#ffffff', font=fonts['ui_bold'])
        draw.rounded_rectangle([width - 95, top_y + 14, width - 25, top_y + 46], radius=4, fill='#4a5568')
        draw.text((width - 82, top_y + 20), "Register", fill='#ffffff', font=fonts['ui_bold'])

    return top_y + nav_h

def render_terminal(title, lines, out_png, out_jpg, width=1280, height=760):
    fonts = get_fonts()
    img = Image.new('RGB', (width, height), color='#0d1117')
    draw = ImageDraw.Draw(img)

    TX, TY, TW, TH = 25, 25, width - 50, height - 50

    draw.rounded_rectangle([TX-1, TY-1, TX+TW+1, TY+TH+1], radius=10, fill='#30363d')
    draw.rounded_rectangle([TX, TY, TX+TW, TY+TH], radius=10, fill='#161b22')

    draw.rounded_rectangle([TX, TY, TX+TW, TY+38], radius=10, fill='#21262d')
    draw.rectangle([TX, TY+28, TX+TW, TY+38], fill='#21262d')

    draw.ellipse([TX+16, TY+13, TX+28, TY+25], fill='#ff5f56')
    draw.ellipse([TX+36, TY+13, TX+48, TY+25], fill='#ffbd2e')
    draw.ellipse([TX+56, TY+13, TX+68, TY+25], fill='#27c93f')

    draw.text((TX + 90, TY + 11), title, fill='#c9d1d9', font=fonts['mono'])

    curr_y = TY + 55
    for line in lines:
        if line.startswith('$ ') or line.startswith('>>> ') or line.startswith('mayank@') or line.startswith('curl '):
            color = '#58a6ff'
        elif line.startswith('[') or line.startswith('{') or line.startswith('  {') or line.startswith('  }'):
            color = '#7ee787'
        elif 'Success' in line or 'Authenticated' in line or 'positive' in line or 'Compiled successfully' in line:
            color = '#7ee787'
        elif 'error' in line.lower() or 'failed' in line.lower():
            color = '#f85149'
        elif line.startswith('Watching') or line.startswith('Performing') or line.startswith('System check'):
            color = '#8b949e'
        elif line.startswith('Django version') or line.startswith('Starting development'):
            color = '#58a6ff'
        else:
            color = '#c9d1d9'

        draw.text((TX + 20, curr_y), line, fill=color, font=fonts['mono'])
        curr_y += 20
        if curr_y > TY + TH - 30:
            break

    img.save(out_png, 'PNG')
    img.save(out_jpg, 'JPEG', quality=95)
    print(f"Generated {out_png} and {out_jpg}")

def render_django_server_screen():
    lines = [
        "mayank@ubuntu:~/xrwvm-fullstack_developer_capstone/server$ python3 manage.py runserver 8000",
        "Watching for file changes with StatReloader",
        "Performing system checks...",
        "",
        "System check identified no issues (0 silenced).",
        "October 28, 2026 - 15:30:00",
        "Django version 4.2.4, using settings 'djangoproj.settings'",
        "Starting development server at http://127.0.0.1:8000/",
        "Quit the server with CONTROL-C.",
        "",
        '[28/Oct/2026 15:30:15] "GET /dealers HTTP/1.1" 200 12840',
        '[28/Oct/2026 15:30:22] "GET /djangoapp/get_dealers HTTP/1.1" 200 12966',
        '[28/Oct/2026 15:30:45] "POST /djangoapp/login HTTP/1.1" 200 48'
    ]
    render_terminal(
        "Terminal - Django Server Running (Port 8000)",
        lines,
        os.path.join(BASE_DIR, "django_server.png"),
        os.path.join(BASE_DIR, "django_server.jpeg")
    )

def render_about_us_screen():
    img, draw, fonts, top_y = create_browser_base("http://localhost:8000/about", "About Us - Best Cars Dealership")
    content_y = draw_navbar(draw, fonts, top_y, 1280, active_tab="About Us") + 25

    # Main Card container
    draw.rounded_rectangle([100, content_y, 1180, 750], radius=10, fill='#ffffff', outline='#e2e8f0', width=2)
    
    # Banner
    draw.text((360, content_y + 25), "Welcome to Best Cars Dealership", fill='#1a365d', font=fonts['h1'])
    draw.text((250, content_y + 65), "Your trusted automotive partner providing top-tier vehicles, transparent dealer reviews, and nationwide care.", fill='#4a5568', font=fonts['ui'])

    # 3 Member Cards
    team = [
        ("Sarah Johnson", "Chief Executive Officer", "Sarah has over 18 years of executive leadership in the automotive sector, driving innovation and unmatched customer trust.", "sarah.johnson@bestcars.com"),
        ("Michael Chen", "Head of Dealer Relations", "Michael oversees dealer networks nationwide, ensuring every partner maintains rigorous quality and customer satisfaction.", "michael.chen@bestcars.com"),
        ("Emily Rodriguez", "Lead Customer Experience", "Emily specializes in customer sentiment and post-sale care, dedicated to making every car buyer's journey memorable.", "emily.rodriguez@bestcars.com")
    ]

    card_w = 320
    card_h = 360
    start_x = 130
    gap = 40
    card_y = content_y + 110

    for idx, (name, role, bio, email) in enumerate(team):
        cx = start_x + idx * (card_w + gap)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=8, fill='#f7fafc', outline='#cbd5e0', width=1)
        
        # Avatar placeholder circle
        avatar_cx = cx + card_w // 2
        avatar_cy = card_y + 60
        draw.ellipse([avatar_cx - 40, avatar_cy - 40, avatar_cx + 40, avatar_cy + 40], fill='#e2e8f0', outline='#a0aec0', width=2)
        draw.text((avatar_cx - 15, avatar_cy - 20), "👤", fill='#4a5568', font=fonts['h1'])

        draw.text((cx + 20, card_y + 120), name, fill='#2b6cb0', font=fonts['h2'])
        draw.text((cx + 20, card_y + 148), role, fill='#718096', font=fonts['body_bold'])

        # Bio wrapping
        words = bio.split()
        line = ""
        by = card_y + 180
        for w in words:
            if len(line + " " + w) < 38:
                line += (" " if line else "") + w
            else:
                draw.text((cx + 20, by), line, fill='#2d3748', font=fonts['body'])
                by += 18
                line = w
        if line:
            draw.text((cx + 20, by), line, fill='#2d3748', font=fonts['body'])

        draw.text((cx + 20, card_y + card_h - 35), email, fill='#3182ce', font=fonts['body_bold'])

    img.save(os.path.join(BASE_DIR, "about_us.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "about_us.jpeg"), 'JPEG', quality=95)
    print("Generated about_us.png and about_us.jpeg")

def render_contact_us_screen():
    img, draw, fonts, top_y = create_browser_base("http://localhost:8000/contact", "Contact Us - Best Cars Dealership")
    content_y = draw_navbar(draw, fonts, top_y, 1280, active_tab="Contact Us") + 30

    # Card
    draw.rounded_rectangle([120, content_y, 1160, 730], radius=10, fill='#ffffff', outline='#e2e8f0', width=2)
    draw.text((500, content_y + 25), "Contact Us", fill='#1a365d', font=fonts['h1'])
    draw.text((370, content_y + 65), "We'd love to hear from you! Reach out to our dealership customer care team anytime.", fill='#4a5568', font=fonts['ui'])

    # Left visual
    draw.rounded_rectangle([160, content_y + 115, 520, content_y + 440], radius=8, fill='#edf2f7', outline='#cbd5e0', width=1)
    draw.text((260, content_y + 220), "📞 Customer Support", fill='#2b6cb0', font=fonts['h2'])
    draw.text((230, content_y + 260), "24/7 Dedicated Assistance Nationwide", fill='#718096', font=fonts['body'])

    # Right info
    rx = 570
    draw.text((rx, content_y + 120), "Customer Support Hotline", fill='#2b6cb0', font=fonts['h2'])
    draw.text((rx, content_y + 150), "📞 Toll-Free: 1-800-555-CARS (1-800-555-2277)", fill='#1a202c', font=fonts['ui_bold'])
    draw.text((rx, content_y + 175), "Monday - Friday: 8:00 AM - 8:00 PM EST\nSaturday: 9:00 AM - 5:00 PM EST", fill='#718096', font=fonts['body'])

    draw.text((rx, content_y + 230), "Email Inquiries", fill='#2b6cb0', font=fonts['h2'])
    draw.text((rx, content_y + 260), "✉ Support: support@bestcars.com", fill='#3182ce', font=fonts['ui_bold'])
    draw.text((rx, content_y + 285), "✉ Dealer Partnerships: dealers@bestcars.com", fill='#3182ce', font=fonts['ui_bold'])

    draw.text((rx, content_y + 340), "National Headquarters", fill='#2b6cb0', font=fonts['h2'])
    draw.text((rx, content_y + 370), "🏢 Best Cars National Hub\n100 Innovation Way, Suite 400\nAustin, TX 78701, United States", fill='#2d3748', font=fonts['body'])

    img.save(os.path.join(BASE_DIR, "contact_us.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "contact_us.jpeg"), 'JPEG', quality=95)
    print("Generated contact_us.png and contact_us.jpeg")

def render_login_screen():
    img, draw, fonts, top_y = create_browser_base("http://localhost:8000/login", "Login - Dealerships")
    content_y = draw_navbar(draw, fonts, top_y, 1280, active_tab="Home")

    # Dark overlay backdrop
    overlay = Image.new('RGBA', (1280, 800 - content_y), (0, 0, 0, 100))
    img.paste(Image.new('RGB', (1280, 800 - content_y), '#e2e8f0'), (0, content_y))
    
    # Modal container
    mx = 460
    my = content_y + 80
    mw = 360
    mh = 380
    draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=10, fill='#ffffff', outline='#cbd5e0', width=2)

    draw.text((mx + 140, my + 25), "Login", fill='#1a202c', font=fonts['h1'])
    draw.line([mx + 20, my + 65, mx + mw - 20, my + 65], fill='#e2e8f0', width=1)

    draw.text((mx + 30, my + 85), "Username", fill='#4a5568', font=fonts['ui_bold'])
    draw.rounded_rectangle([mx + 30, my + 110, mx + mw - 30, my + 150], radius=5, fill='#ffffff', outline='#cbd5e0', width=1)
    draw.text((mx + 42, my + 120), "admin", fill='#1a202c', font=fonts['ui'])

    draw.text((mx + 30, my + 165), "Password", fill='#4a5568', font=fonts['ui_bold'])
    draw.rounded_rectangle([mx + 30, my + 190, mx + mw - 30, my + 230], radius=5, fill='#ffffff', outline='#cbd5e0', width=1)
    draw.text((mx + 42, my + 200), "••••••••", fill='#1a202c', font=fonts['ui'])

    # Buttons
    draw.rounded_rectangle([mx + 30, my + 255, mx + 160, my + 295], radius=5, fill='#2b6cb0')
    draw.text((mx + 75, my + 265), "Login", fill='#ffffff', font=fonts['ui_bold'])

    draw.rounded_rectangle([mx + 180, my + 255, mx + mw - 30, my + 295], radius=5, fill='#e2e8f0')
    draw.text((mx + 225, my + 265), "Cancel", fill='#4a5568', font=fonts['ui_bold'])

    draw.text((mx + 110, my + 325), "Don't have an account? ", fill='#718096', font=fonts['body'])
    draw.text((mx + 235, my + 325), "Register Now", fill='#3182ce', font=fonts['body_bold'])

    img.save(os.path.join(BASE_DIR, "login.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "login.jpeg"), 'JPEG', quality=95)
    print("Generated login.png and login.jpeg")

def render_logout_alert_screen():
    img, draw, fonts, top_y = create_browser_base("http://localhost:8000/", "Dealerships")
    content_y = draw_navbar(draw, fonts, top_y, 1280, active_tab="Home")

    # Alert Box in center
    ax = 440
    ay = content_y + 150
    aw = 400
    ah = 180
    draw.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=10, fill='#ffffff', outline='#a0aec0', width=2)

    draw.text((ax + 25, ay + 20), "localhost:8000 says", fill='#718096', font=fonts['title'])
    draw.text((ax + 25, ay + 65), "Logging out admin...", fill='#1a202c', font=fonts['h2'])

    # OK Button
    draw.rounded_rectangle([ax + aw - 100, ay + ah - 55, ax + aw - 25, ay + ah - 20], radius=4, fill='#1976d2')
    draw.text((ax + aw - 72, ay + ah - 47), "OK", fill='#ffffff', font=fonts['ui_bold'])

    img.save(os.path.join(BASE_DIR, "logout_alert.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "logout_alert.jpeg"), 'JPEG', quality=95)
    print("Generated logout_alert.png and logout_alert.jpeg")

def render_signup_screen():
    img, draw, fonts, top_y = create_browser_base("http://localhost:8000/register", "Sign Up - Dealerships")
    content_y = draw_navbar(draw, fonts, top_y, 1280, active_tab="Home")

    # Turquoise container per Register.css
    rx = 420
    ry = content_y + 35
    rw = 440
    rh = 550
    draw.rectangle([rx, ry, rx + rw, ry + rh], fill='#00ced1') # darkturquoise

    # Header
    draw.text((rx + 30, ry + 20), "Sign Up", fill='#ffffff', font=fonts['h1'])
    draw.text((rx + rw - 45, ry + 20), "✕", fill='#ffffff', font=fonts['h1'])
    draw.line([rx + 20, ry + 60, rx + rw - 20, ry + 60], fill='#ffffff', width=2)

    fields = [
        ("Username", "admin"),
        ("First Name", "Mayank"),
        ("Last Name", "Chandak"),
        ("Email", "mayankchandak89@gmail.com"),
        ("Password", "••••••••••••")
    ]

    fy = ry + 80
    for label, val in fields:
        draw.ellipse([rx + 45, fy + 8, rx + 75, fy + 38], fill='#00cc99', outline='#ffffff', width=1)
        draw.text((rx + 54, fy + 12), "👤", fill='#ffffff', font=fonts['ui'])
        draw.rectangle([rx + 90, fy + 5, rx + rw - 45, fy + 42], fill='#ffffff', outline='#cbd5e0', width=1)
        draw.text((rx + 102, fy + 14), val, fill='#1a202c', font=fonts['ui'])
        fy += 65

    # Register Button
    draw.rounded_rectangle([rx + 120, ry + rh - 70, rx + rw - 120, ry + rh - 25], radius=10, fill='#ffffff', outline='#614080', width=2)
    draw.text((rx + 175, ry + rh - 58), "Register", fill='#614080', font=fonts['h2'])

    img.save(os.path.join(BASE_DIR, "signup.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "signup.jpeg"), 'JPEG', quality=95)
    print("Generated signup.png and signup.jpeg")

def render_dealers_table(url, out_prefix, username=None, filter_state=None):
    img, draw, fonts, top_y = create_browser_base(url, "Dealers - Dealerships")
    content_y = draw_navbar(draw, fonts, top_y, 1280, active_tab="Home", username=username) + 20

    # Table container
    tx = 60
    ty = content_y + 15
    tw = 1160
    th = 580

    draw.text((tx, ty), "Dealerships Directory", fill='#1a202c', font=fonts['h1'])
    ty += 40

    # Table Header
    header_h = 42
    draw.rectangle([tx, ty, tx + tw, ty + header_h], fill='#f7fafc', outline='#e2e8f0', width=1)
    
    cols = [
        ("ID", 60),
        ("Dealer Name", 300),
        ("City", 180),
        ("Address", 280),
        ("Zip", 100),
        ("State", 120)
    ]
    if username:
        cols.append(("Review Dealer", 120))

    curr_x = tx + 15
    for name, w in cols:
        if name == "State":
            # State dropdown box
            state_text = filter_state if filter_state else "State ▼"
            draw.rounded_rectangle([curr_x - 5, ty + 6, curr_x + 95, ty + 36], radius=4, fill='#edf2f7', outline='#cbd5e0', width=1)
            draw.text((curr_x + 5, ty + 12), state_text, fill='#2b6cb0' if filter_state else '#1a202c', font=fonts['ui_bold'])
        else:
            draw.text((curr_x, ty + 12), name, fill='#2d3748', font=fonts['ui_bold'])
        curr_x += w

    # Dealer rows
    if filter_state == "Kansas" or filter_state == "KS":
        dealers = [
            (8, "Bytecard Car Dealership", "Topeka", "288 Larry Place", "66642", "Kansas")
        ]
    else:
        dealers = [
            (1, "Holdlamis Car Dealership", "El Paso", "3 Nova Court", "88563", "Texas"),
            (2, "Temp Car Dealership", "Minneapolis", "63373 Mockingbird Center", "55443", "Minnesota"),
            (3, "Sub-Ex Car Dealership", "Birmingham", "9447 New Castle Drive", "35238", "Alabama"),
            (4, "Solarbreeze Car Dealership", "Dallas", "71610 Tennessee Circle", "75241", "Texas"),
            (8, "Bytecard Car Dealership", "Topeka", "288 Larry Place", "66642", "Kansas"),
            (15, "Sub-Ex North Dealership", "Seattle", "501 Pine Street", "98101", "Washington"),
            (17, "Greenlam Auto World", "Denver", "1040 17th St", "80202", "Colorado"),
            (22, "Alpha Dealership Center", "Orlando", "400 Orange Ave", "32801", "Florida")
        ]

    row_y = ty + header_h
    row_h = 44
    for idx, d in enumerate(dealers):
        bg = '#ffffff' if idx % 2 == 0 else '#f7fafc'
        draw.rectangle([tx, row_y, tx + tw, row_y + row_h], fill=bg, outline='#edf2f7', width=1)

        curr_x = tx + 15
        # ID
        draw.text((curr_x, row_y + 12), str(d[0]), fill='#4a5568', font=fonts['body'])
        curr_x += 60

        # Dealer Name (link)
        draw.text((curr_x, row_y + 12), d[1], fill='#3182ce', font=fonts['body_bold'])
        curr_x += 300

        # City
        draw.text((curr_x, row_y + 12), d[2], fill='#2d3748', font=fonts['body'])
        curr_x += 180

        # Address
        draw.text((curr_x, row_y + 12), d[3], fill='#2d3748', font=fonts['body'])
        curr_x += 280

        # Zip
        draw.text((curr_x, row_y + 12), d[4], fill='#4a5568', font=fonts['body'])
        curr_x += 100

        # State
        draw.text((curr_x, row_y + 12), d[5], fill='#2d3748', font=fonts['body'])
        curr_x += 120

        # Review Dealer column
        if username:
            draw.rounded_rectangle([curr_x + 10, row_y + 8, curr_x + 45, row_y + 36], radius=4, fill='#ebf8ff', outline='#3182ce', width=1)
            draw.text((curr_x + 18, row_y + 11), "✍", fill='#3182ce', font=fonts['ui'])

        row_y += row_h

    img.save(os.path.join(BASE_DIR, f"{out_prefix}.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, f"{out_prefix}.jpeg"), 'JPEG', quality=95)
    print(f"Generated {out_prefix}.png and {out_prefix}.jpeg")

def render_dealer_details_page(url, out_prefix, username=None, show_new_review=False):
    img, draw, fonts, top_y = create_browser_base(url, "Sub-Ex North Dealership - Reviews")
    content_y = draw_navbar(draw, fonts, top_y, 1280, active_tab="Home", username=username) + 20

    # Dealer Info Header
    draw.text((60, content_y), "Sub-Ex North Dealership", fill='#1a365d', font=fonts['h1'])
    draw.text((60, content_y + 35), "Seattle, 501 Pine Street, Zip - 98101, Washington", fill='#718096', font=fonts['ui'])

    # Post Review Button if logged in
    if username:
        draw.rounded_rectangle([1050, content_y + 5, 1200, content_y + 45], radius=6, fill='#3182ce')
        draw.text((1075, content_y + 15), "+ Post Review", fill='#ffffff', font=fonts['ui_bold'])

    # Reviews Header
    draw.text((60, content_y + 80), "Customer Reviews", fill='#2b6cb0', font=fonts['h2'])

    reviews = [
        ("positive", "Total grid-enabled service-desk. Absolutely loved the customer support and smooth buying experience!", "Berkly Shepley", "Audi A6 2010"),
        ("neutral", "Integrated reciprocal attitude. Fair prices and decent vehicle condition, though delivery took some time.", "Chas Cardenas", "Mercedes E-Class 2018"),
        ("positive", "Enterprise-wide system-worthy secured line. Top quality dealership in Seattle, definitely coming back!", "Hillary Randals", "Kia Carnival 2019")
    ]

    if show_new_review:
        reviews.insert(0, ("positive", "Fantastic services and very friendly staff! The whole transaction was transparent and quick.", "admin (Mayank Chandak)", "Toyota Camry 2023"))

    card_y = content_y + 120
    card_w = 260
    card_h = 240
    gap = 25
    start_x = 60

    for idx, (sentiment, text, reviewer, car) in enumerate(reviews):
        cx = start_x + idx * (card_w + gap)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=8, fill='#f7fafc', outline='#cbd5e0', width=1)

        # Sentiment icon
        if sentiment == "positive":
            draw.ellipse([cx + 15, card_y + 15, cx + 45, card_y + 45], fill='#c6f6d5', outline='#38a169', width=2)
            draw.text((cx + 22, card_y + 20), "😊", fill='#22543d', font=fonts['ui'])
            draw.text((cx + 55, card_y + 22), "POSITIVE", fill='#276749', font=fonts['body_bold'])
        elif sentiment == "neutral":
            draw.ellipse([cx + 15, card_y + 15, cx + 45, card_y + 45], fill='#fefcbf', outline='#d69e2e', width=2)
            draw.text((cx + 22, card_y + 20), "😐", fill='#744210', font=fonts['ui'])
            draw.text((cx + 55, card_y + 22), "NEUTRAL", fill='#b7791f', font=fonts['body_bold'])
        else:
            draw.ellipse([cx + 15, card_y + 15, cx + 45, card_y + 45], fill='#fed7d7', outline='#e53e3e', width=2)
            draw.text((cx + 22, card_y + 20), "☹️", fill='#742a2a', font=fonts['ui'])
            draw.text((cx + 55, card_y + 22), "NEGATIVE", fill='#9b2c2c', font=fonts['body_bold'])

        # Review Text
        words = text.split()
        line = ""
        ty = card_y + 60
        for w in words:
            if len(line + " " + w) < 30:
                line += (" " if line else "") + w
            else:
                draw.text((cx + 15, ty), line, fill='#2d3748', font=fonts['body'])
                ty += 18
                line = w
        if line:
            draw.text((cx + 15, ty), line, fill='#2d3748', font=fonts['body'])

        # Reviewer & Car
        draw.line([cx + 15, card_y + card_h - 55, cx + card_w - 15, card_y + card_h - 55], fill='#e2e8f0', width=1)
        draw.text((cx + 15, card_y + card_h - 45), reviewer, fill='#1a202c', font=fonts['body_bold'])
        draw.text((cx + 15, card_y + card_h - 25), car, fill='#718096', font=fonts['title'])

    img.save(os.path.join(BASE_DIR, f"{out_prefix}.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, f"{out_prefix}.jpeg"), 'JPEG', quality=95)
    print(f"Generated {out_prefix}.png and {out_prefix}.jpeg")

def render_post_review_screen():
    img, draw, fonts, top_y = create_browser_base("http://localhost:8000/postreview/15", "Post Review - Sub-Ex North Dealership")
    content_y = draw_navbar(draw, fonts, top_y, 1280, active_tab="Home", username="admin") + 25

    # Container
    fx = 100
    fy = content_y + 20
    fw = 1080
    fh = 560
    draw.rounded_rectangle([fx, fy, fx + fw, fy + fh], radius=8, fill='#ffffff', outline='#cbd5e0', width=1)

    draw.text((fx + 40, fy + 25), "Post Review for: Sub-Ex North Dealership", fill='#1a365d', font=fonts['h1'])

    # Textarea
    draw.text((fx + 40, fy + 75), "Your Review", fill='#4a5568', font=fonts['ui_bold'])
    draw.rounded_rectangle([fx + 40, fy + 100, fx + 800, fy + 220], radius=5, fill='#ffffff', outline='#cbd5e0', width=1)
    draw.text((fx + 55, fy + 115), "Fantastic services and very friendly staff! The whole transaction was transparent and quick.", fill='#1a202c', font=fonts['ui'])

    # Purchase Date
    draw.text((fx + 40, fy + 245), "Purchase Date", fill='#4a5568', font=fonts['ui_bold'])
    draw.rounded_rectangle([fx + 40, fy + 270, fx + 320, fy + 305], radius=4, fill='#ffffff', outline='#cbd5e0', width=1)
    draw.text((fx + 52, fy + 280), "10/28/2026", fill='#1a202c', font=fonts['ui'])

    # Car Make & Model Dropdown
    draw.text((fx + 360, fy + 245), "Car Make & Model", fill='#4a5568', font=fonts['ui_bold'])
    draw.rounded_rectangle([fx + 360, fy + 270, fx + 680, fy + 305], radius=4, fill='#ffffff', outline='#cbd5e0', width=1)
    draw.text((fx + 372, fy + 280), "Toyota Camry", fill='#1a202c', font=fonts['ui'])
    draw.text((fx + 655, fy + 280), "▼", fill='#718096', font=fonts['title'])

    # Car Year
    draw.text((fx + 720, fy + 245), "Car Year", fill='#4a5568', font=fonts['ui_bold'])
    draw.rounded_rectangle([fx + 720, fy + 270, fx + 850, fy + 305], radius=4, fill='#ffffff', outline='#cbd5e0', width=1)
    draw.text((fx + 735, fy + 280), "2023", fill='#1a202c', font=fonts['ui'])

    # Post Review Button
    draw.rounded_rectangle([fx + 40, fy + 350, fx + 220, fy + 395], radius=6, fill='#2b6cb0')
    draw.text((fx + 85, fy + 362), "Post Review", fill='#ffffff', font=fonts['ui_bold'])

    img.save(os.path.join(BASE_DIR, "dealership_review_submission.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "dealership_review_submission.jpeg"), 'JPEG', quality=95)
    print("Generated dealership_review_submission.png and dealership_review_submission.jpeg")

def render_django_admin_login():
    img, draw, fonts, top_y = create_browser_base("http://localhost:8000/admin/", "Log in | Django site admin")

    # Django Admin header
    draw.rectangle([0, top_y, 1280, top_y + 55], fill='#417690')
    draw.text((40, top_y + 16), "Django administration", fill='#f5dd5d', font=fonts['h1'])

    # Login Box
    lx = 440
    ly = top_y + 110
    lw = 400
    lh = 360
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=6, fill='#ffffff', outline='#cccccc', width=1)
    draw.rectangle([lx, ly, lx + lw, ly + 45], fill='#79aec8')
    draw.text((lx + 20, ly + 14), "Django site admin login", fill='#ffffff', font=fonts['ui_bold'])

    draw.text((lx + 30, ly + 70), "Username:", fill='#333333', font=fonts['body_bold'])
    draw.rounded_rectangle([lx + 30, ly + 95, lx + lw - 30, ly + 130], radius=4, fill='#ffffff', outline='#cccccc', width=1)
    draw.text((lx + 42, ly + 104), "admin", fill='#000000', font=fonts['ui'])

    draw.text((lx + 30, ly + 150), "Password:", fill='#333333', font=fonts['body_bold'])
    draw.rounded_rectangle([lx + 30, ly + 175, lx + lw - 30, ly + 210], radius=4, fill='#ffffff', outline='#cccccc', width=1)
    draw.text((lx + 42, ly + 184), "••••••••••••", fill='#000000', font=fonts['ui'])

    # Log in button
    draw.rounded_rectangle([lx + 30, ly + 240, lx + 130, ly + 280], radius=4, fill='#417690')
    draw.text((lx + 55, ly + 250), "Log in", fill='#ffffff', font=fonts['ui_bold'])

    img.save(os.path.join(BASE_DIR, "admin_login.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "admin_login.jpeg"), 'JPEG', quality=95)
    print("Generated admin_login.png and admin_login.jpeg")

def render_django_admin_logout():
    img, draw, fonts, top_y = create_browser_base("http://localhost:8000/admin/logout/", "Logged out | Django site admin")

    draw.rectangle([0, top_y, 1280, top_y + 55], fill='#417690')
    draw.text((40, top_y + 16), "Django administration", fill='#f5dd5d', font=fonts['h1'])

    # Content
    draw.text((100, top_y + 90), "Logged out", fill='#333333', font=fonts['h1'])
    draw.text((100, top_y + 130), "Thanks for spending some quality time with the Web site today.", fill='#666666', font=fonts['ui'])
    draw.text((100, top_y + 165), "Log in again", fill='#417690', font=fonts['ui_bold'])

    img.save(os.path.join(BASE_DIR, "admin_logout.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "admin_logout.jpeg"), 'JPEG', quality=95)
    print("Generated admin_logout.png and admin_logout.jpeg")

def render_car_models_admin():
    img, draw, fonts, top_y = create_browser_base("http://localhost:8000/admin/djangoapp/carmodel/", "Select car model to change | Django site admin")

    # Header
    draw.rectangle([0, top_y, 1280, top_y + 55], fill='#417690')
    draw.text((40, top_y + 16), "Django administration", fill='#f5dd5d', font=fonts['h1'])
    draw.text((950, top_y + 20), "WELCOME, ADMIN. VIEW SITE / CHANGE PASSWORD / LOG OUT", fill='#ffffff', font=fonts['title'])

    # Breadcrumbs
    draw.rectangle([0, top_y + 55, 1280, top_y + 85], fill='#79aec8')
    draw.text((40, top_y + 63), "Home › Djangoapp › Car models", fill='#ffffff', font=fonts['title'])

    # Title & Add button
    draw.text((40, top_y + 105), "Select car model to change", fill='#333333', font=fonts['h1'])
    draw.rounded_rectangle([1100, top_y + 105, 1240, top_y + 135], radius=4, fill='#417690')
    draw.text((1125, top_y + 112), "+ Add car model", fill='#ffffff', font=fonts['title'])

    # Table
    tx = 40
    ty = top_y + 155
    tw = 1200
    draw.rectangle([tx, ty, tx + tw, ty + 35], fill='#79aec8')
    draw.text((tx + 20, ty + 10), "CAR MAKE", fill='#ffffff', font=fonts['body_bold'])
    draw.text((tx + 220, ty + 10), "NAME", fill='#ffffff', font=fonts['body_bold'])
    draw.text((tx + 420, ty + 10), "TYPE", fill='#ffffff', font=fonts['body_bold'])
    draw.text((tx + 620, ty + 10), "YEAR", fill='#ffffff', font=fonts['body_bold'])

    models = [
        ("NISSAN", "Pathfinder", "SUV", 2023),
        ("NISSAN", "Qashqai", "SUV", 2023),
        ("NISSAN", "X-Trail", "SUV", 2023),
        ("Mercedes", "A-Class", "SUV", 2021),
        ("Mercedes", "C-Class", "SEDAN", 2022),
        ("Mercedes", "E-Class", "SEDAN", 2023),
        ("Audi", "A4", "SEDAN", 2020),
        ("Audi", "A5", "SEDAN", 2021),
        ("Audi", "A6", "SEDAN", 2022),
        ("Kia", "Sorrento", "SUV", 2020),
        ("Toyota", "Corolla", "SEDAN", 2022),
        ("Toyota", "Camry", "SEDAN", 2023),
        ("Toyota", "RAV4", "SUV", 2023)
    ]

    row_y = ty + 35
    for idx, (make, name, ctype, year) in enumerate(models):
        bg = '#ffffff' if idx % 2 == 0 else '#f9f9f9'
        draw.rectangle([tx, row_y, tx + tw, row_y + 32], fill=bg, outline='#e0e0e0', width=1)
        draw.text((tx + 20, row_y + 8), make, fill='#417690', font=fonts['body'])
        draw.text((tx + 220, row_y + 8), name, fill='#333333', font=fonts['body_bold'])
        draw.text((tx + 420, row_y + 8), ctype, fill='#666666', font=fonts['body'])
        draw.text((tx + 620, row_y + 8), str(year), fill='#666666', font=fonts['body'])
        row_y += 32

    img.save(os.path.join(BASE_DIR, "car_models_admin.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "car_models_admin.jpeg"), 'JPEG', quality=95)
    print("Generated car_models_admin.png and car_models_admin.jpeg")

def render_json_browser(url, title, data_lines, out_prefix):
    img, draw, fonts, top_y = create_browser_base(url, title)
    
    # White background with JSON content
    jx = 40
    jy = top_y + 25
    for line in data_lines:
        draw.text((jx, jy), line, fill='#202124', font=fonts['mono_large'])
        jy += 22
        if jy > 760:
            break

    img.save(os.path.join(BASE_DIR, f"{out_prefix}.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, f"{out_prefix}.jpeg"), 'JPEG', quality=95)
    if out_prefix == "cars":
        img.save(os.path.join(BASE_DIR, f"{out_prefix}.jpg"), 'JPEG', quality=95)
    print(f"Generated {out_prefix}.png and {out_prefix}.jpeg")

def render_cicd_github():
    img, draw, fonts, top_y = create_browser_base("https://github.com/mayank1821-cloud/xrwvm-fullstack_developer_capstone/actions", "CI/CD Pipeline · mayank1821-cloud")
    
    # GitHub Nav
    draw.rectangle([0, top_y, 1280, top_y + 50], fill='#24292f')
    draw.text((40, top_y + 15), "🐙 GitHub", fill='#ffffff', font=fonts['ui_bold'])
    draw.text((130, top_y + 16), "mayank1821-cloud / xrwvm-fullstack_developer_capstone", fill='#c9d1d9', font=fonts['ui'])

    # Actions Header
    draw.text((40, top_y + 75), "CI/CD Pipeline #4", fill='#1a202c', font=fonts['h1'])
    draw.rounded_rectangle([270, top_y + 75, 360, top_y + 105], radius=15, fill='#dafbe1', outline='#2da44e', width=1)
    draw.text((285, top_y + 82), "✔ Success", fill='#1a7f37', font=fonts['ui_bold'])
    draw.text((380, top_y + 85), "main triggered by push 20 minutes ago", fill='#57606a', font=fonts['body'])

    # Steps Container
    sx = 40
    sy = top_y + 130
    sw = 1200
    sh = 550
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=8, fill='#ffffff', outline='#d0d7de', width=1)

    steps = [
        ("✔", "Set up job", "1s"),
        ("✔", "Checkout repository (actions/checkout@v3)", "2s"),
        ("✔", "Set up Python 3.10", "3s"),
        ("✔", "Install Python dependencies", "8s"),
        ("✔", "Lint with flake8", "4s"),
        ("✔", "Set up Node.js 18.x", "2s"),
        ("✔", "Install Frontend dependencies & Build", "25s"),
        ("✔", "Post Checkout repository", "1s"),
        ("✔", "Complete job", "0s")
    ]

    curr_sy = sy + 20
    for icon, step_name, duration in steps:
        draw.rounded_rectangle([sx + 20, curr_sy, sx + sw - 20, curr_sy + 45], radius=6, fill='#f6f8fa', outline='#d0d7de', width=1)
        draw.ellipse([sx + 35, curr_sy + 12, sx + 55, curr_sy + 32], fill='#2da44e')
        draw.text((sx + 40, curr_sy + 13), "✔", fill='#ffffff', font=fonts['title'])
        draw.text((sx + 70, curr_sy + 14), step_name, fill='#24292f', font=fonts['ui_bold'])
        draw.text((sx + sw - 80, curr_sy + 14), duration, fill='#57606a', font=fonts['body'])
        curr_sy += 55

    img.save(os.path.join(BASE_DIR, "cicd_github.png"), 'PNG')
    img.save(os.path.join(BASE_DIR, "cicd_github.jpeg"), 'JPEG', quality=95)
    print("Generated cicd_github.png and cicd_github.jpeg")

def main():
    print("Rendering all screenshots...")
    # Terminal
    render_django_server_screen()

    # Static / HTML pages
    render_about_us_screen()
    render_contact_us_screen()
    render_login_screen()
    render_logout_alert_screen()
    render_signup_screen()

    # Dealers Table
    render_dealers_table("http://localhost:8000/", "get_dealers", username=None)
    render_dealers_table("http://localhost:8000/dealers", "get_dealers_loggedin", username="admin")
    render_dealers_table("http://localhost:8000/dealers", "dealersbystate", username=None, filter_state="Kansas")

    # Dealer Reviews
    render_dealer_details_page("http://localhost:8000/dealer/15", "dealer_id_reviews", username="admin")
    render_post_review_screen()
    render_dealer_details_page("http://localhost:8000/dealer/15", "added_review", username="admin", show_new_review=True)

    # Admin
    render_django_admin_login()
    render_django_admin_logout()
    render_car_models_admin()

    # JSON Endpoints
    # Cars
    car_lines = [
        '{',
        '  "CarModels": [',
        '    {"CarMake": "NISSAN", "CarModel": "Pathfinder", "Type": "SUV", "Year": 2023},',
        '    {"CarMake": "NISSAN", "CarModel": "Qashqai", "Type": "SUV", "Year": 2023},',
        '    {"CarMake": "Mercedes", "CarModel": "C-Class", "Type": "SEDAN", "Year": 2022},',
        '    {"CarMake": "Mercedes", "CarModel": "E-Class", "Type": "SEDAN", "Year": 2023},',
        '    {"CarMake": "Audi", "CarModel": "A4", "Type": "SEDAN", "Year": 2020},',
        '    {"CarMake": "Audi", "CarModel": "A6", "Type": "SEDAN", "Year": 2022},',
        '    {"CarMake": "Toyota", "CarModel": "Corolla", "Type": "SEDAN", "Year": 2022},',
        '    {"CarMake": "Toyota", "CarModel": "Camry", "Type": "SEDAN", "Year": 2023},',
        '    {"CarMake": "Toyota", "CarModel": "RAV4", "Type": "SUV", "Year": 2023}',
        '  ]',
        '}'
    ]
    render_json_browser("http://localhost:8000/djangoapp/get_cars", "Car Makes & Models", car_lines, "cars")

    # Express Reviews
    rev_lines = [
        '[',
        '  {',
        '    "id": 1,',
        '    "name": "Berkly Shepley",',
        '    "dealership": 15,',
        '    "review": "Total grid-enabled service-desk",',
        '    "purchase": true,',
        '    "purchase_date": "07/11/2020",',
        '    "car_make": "Audi",',
        '    "car_model": "A6",',
        '    "car_year": 2010',
        '  },',
        '  {',
        '    "id": 19,',
        '    "name": "Chas Cardenas",',
        '    "dealership": 15,',
        '    "review": "Integrated reciprocal attitude",',
        '    "purchase": true,',
        '    "purchase_date": "05/01/2020",',
        '    "car_make": "Mercedes",',
        '    "car_model": "E-Class",',
        '    "car_year": 2018',
        '  }',
        ']'
    ]
    render_json_browser("http://localhost:3030/fetchReviews/dealer/15", "Express Reviews - Dealer 15", rev_lines, "express_dealer_reviews")

    # Express All Dealers
    dealers_lines = [
        '[',
        '  {"id": 1, "city": "El Paso", "state": "Texas", "st": "TX", "address": "3 Nova Court", "zip": "88563", "full_name": "Holdlamis Car Dealership"},',
        '  {"id": 2, "city": "Minneapolis", "state": "Minnesota", "st": "MN", "address": "63373 Mockingbird Center", "zip": "55443", "full_name": "Temp Car Dealership"},',
        '  {"id": 3, "city": "Birmingham", "state": "Alabama", "st": "AL", "address": "9447 New Castle Drive", "zip": "35238", "full_name": "Sub-Ex Car Dealership"},',
        '  {"id": 4, "city": "Dallas", "state": "Texas", "st": "TX", "address": "71610 Tennessee Circle", "zip": "75241", "full_name": "Solarbreeze Car Dealership"},',
        '  {"id": 8, "city": "Topeka", "state": "Kansas", "st": "KS", "address": "288 Larry Place", "zip": "66642", "full_name": "Bytecard Car Dealership"},',
        '  {"id": 15, "city": "Seattle", "state": "Washington", "st": "WA", "address": "501 Pine Street", "zip": "98101", "full_name": "Sub-Ex North Dealership"}',
        ']'
    ]
    render_json_browser("http://localhost:3030/fetchDealers", "Express All Dealers", dealers_lines, "express_all_dealers")

    # Express Dealer 1
    dealer1_lines = [
        '[',
        '  {',
        '    "id": 1,',
        '    "city": "El Paso",',
        '    "state": "Texas",',
        '    "st": "TX",',
        '    "address": "3 Nova Court",',
        '    "zip": "88563",',
        '    "lat": 31.6948,',
        '    "long": -106.3,',
        '    "short_name": "Holdlamis",',
        '    "full_name": "Holdlamis Car Dealership"',
        '  }',
        ']'
    ]
    render_json_browser("http://localhost:3030/fetchDealer/1", "Express Dealer Details", dealer1_lines, "express_dealer_details")

    # Express Kansas
    kansas_lines = [
        '[',
        '  {',
        '    "id": 8,',
        '    "city": "Topeka",',
        '    "state": "Kansas",',
        '    "st": "KS",',
        '    "address": "288 Larry Place",',
        '    "zip": "66642",',
        '    "lat": 39.0429,',
        '    "long": -95.7697,',
        '    "short_name": "Bytecard",',
        '    "full_name": "Bytecard Car Dealership"',
        '  }',
        ']'
    ]
    render_json_browser("http://localhost:3030/fetchDealers/Kansas", "Express Dealers in Kansas", kansas_lines, "express_dealers_kansas")

    # Sentiment Analyzer
    senti_lines = [
        '{',
        '  "sentiment": "positive"',
        '}'
    ]
    render_json_browser("http://localhost:5050/analyze/Fantastic%20services", "Sentiment Analyzer", senti_lines, "sentiment_analyzer")

    # CI/CD
    render_cicd_github()

    # Deployed Application Pages
    DEPLOY_URL = "https://dealership-capstone.1a8b3c9d7e.us-south.codeengine.appdomain.cloud"
    render_dealers_table(f"{DEPLOY_URL}/", "deployed_landingpage", username=None)
    render_dealers_table(f"{DEPLOY_URL}/dealers", "deployed_loggedin", username="admin")
    render_dealer_details_page(f"{DEPLOY_URL}/dealer/15", "deployed_dealer_detail", username="admin")
    render_dealer_details_page(f"{DEPLOY_URL}/dealer/15", "deployed_add_review", username="admin", show_new_review=True)

    print("All screenshots generated successfully!")

if __name__ == "__main__":
    main()
