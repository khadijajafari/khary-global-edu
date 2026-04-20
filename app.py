from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session, render_template,Response
from datetime import datetime
import sqlite3
import os
from werkzeug.utils import secure_filename
import json
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import time
from datetime import datetime
current_year = datetime.now().year

from functools import wraps

app = Flask(__name__)
app.secret_key = 'khary-global-edu-secret-key-2026'  # Change this to something unique

app.static_folder = 'static'

from security import sanitize_input, validate_email, validate_password, rate_limit

from flask import jsonify

import secrets
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os

import os
import sqlite3

def get_db():
    # Try multiple possible paths
    possible_paths = [
        'applications.db',
        '/opt/render/project/src/applications.db',
        os.path.join(os.getcwd(), 'applications.db'),
        '/data/applications.db'  # if you add disk
    ]
    
    for path in possible_paths:
        try:
            conn = sqlite3.connect(path, timeout=30)
            conn.execute('PRAGMA journal_mode=WAL')
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            continue
    
    # If all fail, create a new database in current directory
    try:
        conn = sqlite3.connect('applications.db', timeout=30)
        conn.execute('PRAGMA journal_mode=WAL')
        conn.row_factory = sqlite3.Row
        # Create tables if needed
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS blog_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, category TEXT, date TEXT, read_time TEXT, content TEXT, published INTEGER DEFAULT 1)''')
        conn.commit()
        return conn
    except Exception as e:
        print(f"Fatal DB error: {e}")
        return None




# ============ ADD SECURITY HEADERS HERE ============
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# ==================== ADD THIS LINE ====================
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
# ======================================================



# ============ LOGIN REQUIRED DECORATOR ============
from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login?next=' + request.url)
        return f(*args, **kwargs)
    return decorated_function


# ================== ADMIN AUTHENTICATION ====================

ADMIN_USERNAME = "khary"
ADMIN_PASSWORD = "khary2024"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect('/admin-login')
        return f(*args, **kwargs)
    return decorated_function

# ==================== EMAIL CONFIGURATION ====================
import os

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# Use environment variables for sensitive data (with fallbacks for local development)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'kharyglobal@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'hdgc xavr ixwq kgaj')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'kharyglobal@gmail.com')

mail = Mail(app)

# Print email config status (without showing password)
print(f"📧 Email configured for: {app.config['MAIL_USERNAME']}")
print(f"📧 Password set: {'Yes' if app.config['MAIL_PASSWORD'] else 'No'}")
mail = Mail(app)

print("📧 Email configured for:", app.config['MAIL_USERNAME'])
# ==================== VERIFICATION EMAIL FUNCTION ====================
def send_verification_email(email, name, code):
    try:
        msg = Message(
            subject="Verify Your Email - KHARY GLOBAL EDU",
            recipients=[email],
            body=f"""
            Dear {name},
            
            Welcome to KHARY GLOBAL EDU!
            
            Please verify your email by clicking the link below:
            http://localhost:5000/verify-email?code={code}&email={email}
            
            If you didn't create an account, please ignore this email.
            
            Best regards,
            KHARY GLOBAL EDU Team
            """
        )
        mail.send(msg)
        print(f"✅ Verification email sent to {email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send verification email to {email}: {e}")
        return False

# ==================== FILE UPLOAD CONFIGURATION ====================
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== STARTUP MESSAGES ====================
print("=" * 50)
print("🚀 KHARY GLOBAL EDU starting up...")
print("=" * 50)
print(f"📂 Upload folder: {UPLOAD_FOLDER}")
print(f"📧 Email: {app.config.get('MAIL_USERNAME', 'Not set')}")
print(f"📁 Upload folder exists: {os.path.exists(UPLOAD_FOLDER)}")
print(f"🔧 Debug mode: {app.debug}")
print("=" * 50)




# ==================== DATABASE SETUP ====================
def init_db():
    """Initialize SQLite database"""
    try:
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        
        # Existing applications table
        c.execute('''CREATE TABLE IF NOT EXISTS applications
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      country TEXT,
                      university TEXT,
                      student_name TEXT,
                      student_email TEXT,
                      student_phone TEXT,
                      program_level TEXT,
                      preferred_program TEXT,
                      message TEXT,
                      application_date TIMESTAMP,
                      status TEXT DEFAULT 'new')''')
        
        # NEW: Users table for student accounts
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      full_name TEXT NOT NULL,
                      email TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL,
                      phone TEXT,
                      country TEXT,
                      education_level TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      last_login TIMESTAMP)''')
        
        # NEW: Saved universities table for comparison
        c.execute('''CREATE TABLE IF NOT EXISTS saved_universities
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      university_id INTEGER,
                      country TEXT,
                      university_name TEXT,
                      saved_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      notes TEXT,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
        
        # NEW: Blog posts table
        c.execute('''CREATE TABLE IF NOT EXISTS blog_posts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      slug TEXT UNIQUE,
                      category TEXT,
                      author_id INTEGER,
                      author_name TEXT,
                      date TEXT,
                      read_time TEXT,
                      views INTEGER DEFAULT 0,
                      likes INTEGER DEFAULT 0,
                      image TEXT,
                      excerpt TEXT,
                      content TEXT,
                      published BOOLEAN DEFAULT 1,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # NEW: Comments table
        c.execute('''CREATE TABLE IF NOT EXISTS comments
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      post_id INTEGER,
                      user_id INTEGER,
                      user_name TEXT,
                      user_email TEXT,
                      comment TEXT,
                      likes INTEGER DEFAULT 0,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (post_id) REFERENCES blog_posts (id),
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
        
        # NEW: Bookmarks table
        c.execute('''CREATE TABLE IF NOT EXISTS bookmarks
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      post_id INTEGER,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      UNIQUE(user_id, post_id),
                      FOREIGN KEY (user_id) REFERENCES users (id),
                      FOREIGN KEY (post_id) REFERENCES blog_posts (id))''')
        
        # NEW: Author profiles table
        c.execute('''CREATE TABLE IF NOT EXISTS authors
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT UNIQUE,
                      bio TEXT,
                      avatar TEXT,
                      role TEXT,
                      articles_count INTEGER DEFAULT 0,
                      followers INTEGER DEFAULT 0,
                      joined_date TEXT,
                      social_facebook TEXT,
                      social_twitter TEXT,
                      social_linkedin TEXT)''')
         # Add this to your existing init_db() function
        c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              full_name TEXT NOT NULL,
              email TEXT UNIQUE NOT NULL,
              password TEXT NOT NULL,
              phone TEXT,
              country TEXT,
              education_level TEXT,
              created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              email_verified INTEGER DEFAULT 0,
              verification_code TEXT)''')
        
         # NEW: Author followers table (MISSING!)
        c.execute('''CREATE TABLE IF NOT EXISTS author_followers
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      author_id INTEGER,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      UNIQUE(user_id, author_id),
                      FOREIGN KEY (user_id) REFERENCES users (id),
                      FOREIGN KEY (author_id) REFERENCES authors (id))''')
        
          

        

        
        conn.commit()
        conn.close()
        print("✅ Database initialized with blog tables")
    except Exception as e:
        print(f"❌ Database error: {e}")


# ==================== BLOG ARTICLES DATA ====================
def init_blog_posts():
    try:
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        
        # Check if posts exist
        c.execute("SELECT COUNT(*) FROM blog_posts")
        count = c.fetchone()[0]
        
        if count == 0:
            # Insert 30 blog posts
            posts = [
                # Article 1 - Tsinghua University
                (1, 'how-to-get-into-tsinghua-university', 'How to Get into Tsinghua University', 'China', 1, 'Khary', 'March 9, 2026', '8 min read',
                 '''<h2>Introduction</h2>
                 <p>Tsinghua University, often called the "MIT of China," is the country's most prestigious institution for engineering and computer science. With an acceptance rate of only 10-15%, getting in requires exceptional preparation.</p>
                 
                 <h2>Admission Requirements</h2>
                 <h3>Academic Requirements</h3>
                 <ul>
                     <li>High School Diploma with 85%+ marks</li>
                     <li>SAT 1400+ or ACT 30+</li>
                     <li>For Chinese-taught programs: HSK Level 4</li>
                     <li>For English-taught programs: IELTS 6.5 (min 6.0) or TOEFL 90+</li>
                 </ul>
                 
                 <h3>Required Documents</h3>
                 <ul>
                     <li>Academic transcripts</li>
                     <li>3 Recommendation Letters</li>
                     <li>Personal Statement</li>
                     <li>Passport copy</li>
                     <li>Portfolio (for architecture/design programs)</li>
                 </ul>
                 
                 <h2>Scholarship Opportunities</h2>
                 <ul>
                     <li><strong>CSC Scholarship:</strong> Full tuition + accommodation + monthly stipend (3,000 RMB)</li>
                     <li><strong>Tsinghua University Scholarship:</strong> 50-100% tuition reduction</li>
                     <li><strong>Beijing Government Scholarship:</strong> 20,000 - 40,000 RMB/year</li>
                 </ul>
                 
                 <h2>Application Timeline</h2>
                 <ul>
                     <li><strong>March 15:</strong> Fall semester deadline</li>
                     <li><strong>October 30:</strong> Spring semester deadline</li>
                     <li><strong>December-March:</strong> Scholarship applications</li>
                 </ul>
                 
                 <h2>Tips from Successful Applicants</h2>
                 <p>1. Start your application at least 6 months before the deadline</p>
                 <p>2. Get strong recommendation letters from teachers who know you well</p>
                 <p>3. Write a personal statement that shows your unique story and passion</p>
                 <p>4. If applying for STEM, highlight your research or project experience</p>
                 <p>5. Apply for multiple scholarships to increase your chances</p>'''),
                
                # Article 2 - Scholarships
                (2, 'top-10-fully-funded-scholarships-asia', 'Top 10 Fully Funded Scholarships in Asia', 'Scholarships', 1, 'Khary', 'March 5, 2026', '10 min read',
                 '''<h2>1. Chinese Government Scholarship (CSC)</h2>
                 <p><strong>Coverage:</strong> Full tuition, accommodation, monthly stipend, health insurance</p>
                 <p><strong>Deadline:</strong> January-March annually</p>
                 <p><strong>Eligibility:</strong> All international students</p>
                 <p><strong>Universities:</strong> Tsinghua, Peking, Fudan, and 280+ others</p>
                 
                 <h2>2. Singapore International Graduate Award (SINGA)</h2>
                 <p><strong>Coverage:</strong> Full tuition, monthly stipend of SGD 2,000, settling-in allowance</p>
                 <p><strong>Deadline:</strong> June 1 & December 1</p>
                 <p><strong>For:</strong> PhD studies in STEM at NTU, NUS, SUTD</p>
                 
                 <h2>3. Japanese Government (MEXT) Scholarship</h2>
                 <p><strong>Coverage:</strong> Full tuition, monthly stipend of ¥143,000-148,000, travel costs</p>
                 <p><strong>Deadline:</strong> April-May (through embassy)</p>
                 <p><strong>For:</strong> Undergraduate, Graduate, PhD, and Training programs</p>
                 
                 <h2>4. Korean Government Scholarship Program (KGSP)</h2>
                 <p><strong>Coverage:</strong> Full tuition, monthly stipend of KRW 900,000, airfare, Korean language training</p>
                 <p><strong>Deadline:</strong> February-March</p>
                 <p><strong>Universities:</strong> SNU, KAIST, Yonsei, Korea University, and 65+ others</p>
                 
                 <h2>5. ASEAN Undergraduate Scholarship (Singapore)</h2>
                 <p><strong>Coverage:</strong> Full tuition + living allowance</p>
                 <p><strong>For:</strong> ASEAN students at NUS, NTU, SMU</p>
                 
                 <h2>6. Taiwan ICDF Scholarship</h2>
                 <p><strong>Coverage:</strong> Full tuition, accommodation, monthly stipend, airfare</p>
                 
                 <h2>7. Hong Kong PhD Fellowship Scheme</h2>
                 <p><strong>Coverage:</strong> HK$331,200/year stipend + conference travel</p>
                 
                 <h2>8. ADB-Japan Scholarship Program</h2>
                 <p><strong>Coverage:</strong> Full tuition, housing, subsistence allowance</p>
                 
                 <h2>9. Malaysia International Scholarship (MIS)</h2>
                 <p><strong>Coverage:</strong> Full tuition + monthly stipend</p>
                 
                 <h2>10. DAAD Scholarships for Asia</h2>
                 <p><strong>Coverage:</strong> Varies by program</p>'''),
                
                # Article 3 - Visa Guide
                (3, 'student-visa-guide-5-asian-countries', 'Student Visa Guide for 5 Asian Countries', 'Visa Guide', 1, 'Khary', 'March 1, 2026', '12 min read',
                 '''<h2>China Student Visa (X Visa)</h2>
                 <p><strong>Requirements:</strong></p>
                 <ul>
                     <li>Valid passport (6+ months validity)</li>
                     <li>JW201/JW202 form from university</li>
                     <li>Admission letter</li>
                     <li>Physical examination record</li>
                     <li>2 passport photos</li>
                     <li>Bank statements (last 3 months)</li>
                 </ul>
                 <p><strong>Processing time:</strong> 4-7 working days</p>
                 <p><strong>Cost:</strong> $140-200</p>
                 
                 <h2>Singapore Student Visa</h2>
                 <p><strong>Requirements:</strong></p>
                 <ul>
                     <li>Valid passport</li>
                     <li>SOLAR registration number</li>
                     <li>Admission letter</li>
                     <li>Financial evidence (SGD 30,000+)</li>
                     <li>Medical report</li>
                 </ul>
                 <p><strong>Processing time:</strong> 2-4 weeks</p>
                 <p><strong>Cost:</strong> SGD 30-90</p>
                 
                 <h2>Malaysia Student Visa</h2>
                 <p><strong>Requirements:</strong></p>
                 <ul>
                     <li>Valid passport</li>
                     <li>VAL (Visa Approval Letter)</li>
                     <li>Medical report</li>
                     <li>Insurance</li>
                     <li>Bank statements</li>
                 </ul>
                 
                 <h2>Japan Student Visa</h2>
                 <p><strong>Requirements:</strong></p>
                 <ul>
                     <li>Valid passport</li>
                     <li>COE (Certificate of Eligibility)</li>
                     <li>Admission letter</li>
                     <li>Bank statements (¥1.5M+)</li>
                 </ul>
                 
                 <h2>Korea Student Visa (D-2)</h2>
                 <p><strong>Requirements:</strong></p>
                 <ul>
                     <li>Valid passport</li>
                     <li>Certificate of Admission</li>
                     <li>Bank statements ($10,000+)</li>
                     <li>Study plan</li>
                     <li>Language proficiency (TOPIK)</li>
                 </ul>'''),
                
                # Article 4 - Mandarin Tips
                (4, 'learning-mandarin-tips-beginners', 'Learning Mandarin: Tips for Beginners', 'China', 1, 'Khary', 'Feb 25, 2026', '6 min read',
                 '''<h2>Best Apps for Learning Mandarin</h2>
                 <ul>
                     <li><strong>Duolingo:</strong> Great for beginners, gamified learning</li>
                     <li><strong>HelloChinese:</strong> Specifically designed for Mandarin learners</li>
                     <li><strong>Pleco:</strong> Essential dictionary app with flashcards</li>
                     <li><strong>Skritter:</strong> Best for learning to write characters</li>
                 </ul>
                 
                 <h2>HSK Exam Guide</h2>
                 <p>The HSK (Hanyu Shuiping Kaoshi) has 6 levels:</p>
                 <ul>
                     <li><strong>HSK 1:</strong> 150 words - Basic daily expressions</li>
                     <li><strong>HSK 2:</strong> 300 words - Simple conversations</li>
                     <li><strong>HSK 3:</strong> 600 words - Basic life and study situations</li>
                     <li><strong>HSK 4:</strong> 1200 words - Fluent conversation on various topics</li>
                     <li><strong>HSK 5:</strong> 2500 words - Reading Chinese media</li>
                     <li><strong>HSK 6:</strong> 5000+ words - Near-native fluency</li>
                 </ul>
                 
                 <h2>Tips from Students Who Mastered Chinese in One Year</h2>
                 <p>1. Practice characters daily - write 10 new characters every day</p>
                 <p>2. Watch Chinese dramas with subtitles</p>
                 <p>3. Use language exchange apps like HelloTalk</p>
                 <p>4. Listen to Chinese podcasts during commute</p>
                 <p>5. Label everything in your room with Chinese names</p>'''),
                
                # Article 5 - Cost of Living
                (5, 'cost-of-living-asian-university-cities', 'Cost of Living in Asian University Cities', 'Student Life', 1, 'Khary', 'Feb 20, 2026', '7 min read',
                 '''<h2>Beijing, China</h2>
                 <p><strong>Monthly costs:</strong></p>
                 <ul>
                     <li>University dormitory: ¥800-1,500</li>
                     <li>Private apartment: ¥2,500-5,000</li>
                     <li>Food: ¥1,500-2,500</li>
                     <li>Transport: ¥200-300</li>
                     <li>Utilities & Internet: ¥300-500</li>
                     <li>Entertainment: ¥500-1,000</li>
                     <li><strong>Total: ¥4,500-8,000/month</strong></li>
                 </ul>
                 
                 <h2>Singapore</h2>
                 <ul>
                     <li>University dormitory: SGD 400-800</li>
                     <li>Private room: SGD 800-2,000</li>
                     <li>Food (hawker centers): SGD 400-600</li>
                     <li>Transport: SGD 100-150</li>
                     <li>Utilities: SGD 100-200</li>
                     <li><strong>Total: SGD 1,500-3,000/month</strong></li>
                 </ul>
                 
                 <h2>Kuala Lumpur, Malaysia</h2>
                 <ul>
                     <li>University dormitory: RM 400-800</li>
                     <li>Private apartment: RM 800-1,500</li>
                     <li>Food: RM 600-900</li>
                     <li>Transport: RM 100-150</li>
                     <li><strong>Total: RM 1,500-2,500/month</strong></li>
                 </ul>
                 
                 <h2>Tokyo, Japan</h2>
                 <ul>
                     <li>University dormitory: ¥30,000-50,000</li>
                     <li>Private apartment: ¥50,000-100,000</li>
                     <li>Food: ¥30,000-50,000</li>
                     <li>Transport: ¥10,000-15,000</li>
                     <li><strong>Total: ¥100,000-180,000/month</strong></li>
                 </ul>
                 
                 <h2>Seoul, Korea</h2>
                 <ul>
                     <li>University dormitory: ₩300,000-500,000</li>
                     <li>Private room: ₩400,000-800,000</li>
                     <li>Food: ₩300,000-500,000</li>
                     <li>Transport: ₩50,000-80,000</li>
                     <li><strong>Total: ₩800,000-1,500,000/month</strong></li>
                 </ul>'''),
                
                # Article 6 - Success Story
                (6, 'from-africa-to-nus-student-journey', 'From Africa to NUS: A Student\'s Journey', 'Success Story', 2, 'Sarah Johnson', 'Feb 15, 2026', '9 min read',
                 '''<h2>My Journey to Singapore</h2>
                 <p>By Sarah Johnson, NUS Computer Science Student</p>
                 
                 <div class="info-box">
                     <h3>Quick Facts</h3>
                     <ul>
                         <li><strong>From:</strong> Nigeria</li>
                         <li><strong>University:</strong> National University of Singapore</li>
                         <li><strong>Program:</strong> Computer Science (Undergraduate)</li>
                         <li><strong>Scholarship:</strong> ASEAN Undergraduate Scholarship</li>
                     </ul>
                 </div>
                 
                 <h2>How I Discovered NUS</h2>
                 <p>Growing up in Lagos, Nigeria, I always dreamed of studying abroad. In my final year of high school, I started researching universities in Asia and discovered that NUS was ranked #1 in Asia. The more I read about their computer science program, the more I knew this was where I wanted to be.</p>
                 
                 <h2>The Application Process</h2>
                 <p>I started my application 8 months before the deadline. The most challenging part was writing the personal statement. I wanted it to truly reflect my passion for technology and my desire to use it to solve problems in Africa.</p>
                 
                 <h3>My Application Timeline:</h3>
                 <ul>
                     <li><strong>July:</strong> Started researching programs</li>
                     <li><strong>August:</strong> Took IELTS (scored 7.5)</li>
                     <li><strong>September:</strong> Requested recommendation letters</li>
                     <li><strong>October:</strong> Wrote and revised personal statement</li>
                     <li><strong>November:</strong> Submitted application</li>
                     <li><strong>February:</strong> Received acceptance letter!</li>
                 </ul>
                 
                 <h2>Scholarship Success</h2>
                 <p>I applied for the ASEAN Undergraduate Scholarship and was thrilled to receive full funding! The scholarship covers my tuition and provides a living allowance of SGD 5,800 per year.</p>
                 
                 <h2>Tips for Future Applicants</h2>
                 <div class="success-box">
                     <ul>
                         <li>Start early - give yourself at least 6 months</li>
                         <li>Be authentic in your essays - tell YOUR story</li>
                         <li>Apply for every scholarship you're eligible for</li>
                         <li>Connect with current students on LinkedIn</li>
                         <li>Practice for interviews - prepare answers for common questions</li>
                     </ul>
                 </div>
                 
                 <h2>Life at NUS</h2>
                 <p>NUS has exceeded all my expectations. The professors are world-class, the facilities are amazing, and I've made friends from all over the world. The best part is the entrepreneurial ecosystem - I'm already working on a startup with friends from the engineering faculty!</p>'''),
                
                # Article 7 - Korean Language Guide
                (7, 'korean-language-guide-international-students', 'Korean Language Guide for International Students', 'Korea', 1, 'Khary', 'Feb 10, 2026', '5 min read',
                 '''<h2>Essential Korean Phrases for Daily Life</h2>
                 <table>
                     <tr><th>English</th><th>Korean</th><th>Pronunciation</th></tr>
                     <tr><td>Hello</td><td>안녕하세요</td><td>An-nyeong-ha-se-yo</td></tr>
                     <tr><td>Thank you</td><td>감사합니다</td><td>Gam-sa-ham-ni-da</td></tr>
                     <tr><td>I'm sorry</td><td>죄송합니다</td><td>Jwe-song-ham-ni-da</td></tr>
                     <tr><td>Yes</td><td>네</td><td>Ne</td></tr>
                     <tr><td>No</td><td>아니요</td><td>A-ni-yo</td></tr>
                     <tr><td>How much?</td><td>얼마예요?</td><td>Eol-ma-ye-yo?</td></tr>
                     <tr><td>Delicious</td><td>맛있어요</td><td>Ma-si-sseo-yo</td></tr>
                 </table>
                 
                 <h2>TOPIK Exam Guide</h2>
                 <p>The Test of Proficiency in Korean (TOPIK) has 6 levels:</p>
                 <ul>
                     <li><strong>TOPIK I (Level 1-2):</strong> Basic conversation, 800-1,500 words</li>
                     <li><strong>TOPIK II (Level 3-4):</strong> Daily life and study, 3,000 words</li>
                     <li><strong>TOPIK II (Level 5-6):</strong> Professional fluency, 5,000+ words</li>
                 </ul>
                 
                 <h2>Best Apps for Learning Korean</h2>
                 <ul>
                     <li><strong>Talk To Me In Korean:</strong> Excellent free lessons</li>
                     <li><strong>Duolingo:</strong> Good for vocabulary building</li>
                     <li><strong>Papago:</strong> Best translation app for Korean</li>
                     <li><strong>HelloTalk:</strong> Language exchange with natives</li>
                 </ul>
                 
                 <h2>Tips from Students</h2>
                 <p>1. Watch K-dramas with Korean subtitles</p>
                 <p>2. Listen to K-pop and look up lyrics</p>
                 <p>3. Practice with language exchange partners</p>
                 <p>4. Learn Hangul (Korean alphabet) first - it only takes a few hours!</p>'''),
                
                # Article 8 - Japanese University Guide
                (8, 'japanese-university-entrance-exams-explained', 'Japanese University Entrance Exams Explained', 'Japan', 1, 'Khary', 'Feb 5, 2026', '8 min read',
                 '''<h2>Understanding EJU (Examination for Japanese University Admission)</h2>
                 <p>The EJU is required for most international students applying to Japanese universities. It's held twice a year (June and November) in Japan and 14 other countries.</p>
                 
                 <h3>EJU Subjects:</h3>
                 <ul>
                     <li><strong>Japanese as a Foreign Language:</strong> 125 min, 450 points</li>
                     <li><strong>Science (Physics, Chemistry, Biology):</strong> 80 min, 200 points</li>
                     <li><strong>Mathematics:</strong> 80 min, 200 points</li>
                     <li><strong>Japan and the World:</strong> 80 min, 200 points</li>
                 </ul>
                 
                 <h2>JLPT (Japanese-Language Proficiency Test)</h2>
                 <p>The JLPT measures Japanese language ability and has 5 levels:</p>
                 <ul>
                     <li><strong>N5:</strong> Basic understanding (80 hrs study)</li>
                     <li><strong>N4:</strong> Everyday conversation (300 hrs)</li>
                     <li><strong>N3:</strong> Limited daily Japanese (450 hrs)</li>
                     <li><strong>N2:</strong> Understanding of general Japanese (600 hrs)</li>
                     <li><strong>N1:</strong> Understanding of complex Japanese (900+ hrs)</li>
                 </ul>
                 
                 <h2>Top Universities and Their Requirements</h2>
                 <table>
                     <tr><th>University</th><th>EJU Score</th><th>JLPT</th><th>English</th></tr>
                     <tr><td>University of Tokyo</td><td>680+</td><td>N1</td><td>TOEFL 90+</td></tr>
                     <tr><td>Kyoto University</td><td>650+</td><td>N1</td><td>TOEFL 85+</td></tr>
                     <tr><td>Osaka University</td><td>620+</td><td>N2</td><td>TOEFL 80+</td></tr>
                     <tr><td>Tohoku University</td><td>600+</td><td>N2</td><td>TOEFL 75+</td></tr>
                     <tr><td>Waseda University</td><td>580+</td><td>N2</td><td>IELTS 6.0</td></tr>
                 </table>
                 
                 <h2>Application Timeline</h2>
                 <ul>
                     <li><strong>April-June:</strong> Take EJU</li>
                     <li><strong>July-August:</strong> Submit applications</li>
                     <li><strong>September-October:</strong> University exams/interviews</li>
                     <li><strong>November-December:</strong> Results</li>
                     <li><strong>April:</strong> Enrollment</li>
                 </ul>'''),
                
                # Article 9 - SINGA Scholarship Guide
                (9, 'singapore-singa-scholarship-complete-guide', 'Singapore\'s SINGA Scholarship: Complete Guide', 'Singapore', 1, 'Khary', 'Jan 30, 2026', '7 min read',
                 '''<h2>What is SINGA?</h2>
                 <p>The Singapore International Graduate Award (SINGA) is a prestigious PhD scholarship offered jointly by:</p>
                 <ul>
                     <li>Nanyang Technological University (NTU)</li>
                     <li>National University of Singapore (NUS)</li>
                     <li>Singapore University of Technology and Design (SUTD)</li>
                     <li>Singapore Institute of Technology (SIT)</li>
                     <li>Singapore Management University (SMU)</li>
                 </ul>
                 
                 <h2>Scholarship Benefits</h2>
                 <div class="success-box">
                     <ul>
                         <li><strong>Full tuition fees</strong> for 4 years</li>
                         <li><strong>Monthly stipend:</strong> SGD 2,200 (increases to SGD 2,700 after passing qualifying exam)</li>
                         <li><strong>One-time airfare grant:</strong> SGD 1,500</li>
                         <li><strong>Settling-in allowance:</strong> SGD 1,000</li>
                         <li><strong>Conference travel allowance:</strong> SGD 4,000 total</li>
                     </ul>
                 </div>
                 
                 <h2>Eligibility Requirements</h2>
                 <ul>
                     <li>Open to all international graduates</li>
                     <li>Excellent academic record (Bachelor's degree with 2nd Upper Honors or equivalent)</li>
                     <li>Strong research potential</li>
                     <li>Good English proficiency (IELTS/TOEFL if previous degree wasn't in English)</li>
                     <li>GRE scores recommended for some programs</li>
                 </ul>
                 
                 <h2>Research Areas</h2>
                 <p>SINGA supports PhD research in:</p>
                 <ul>
                     <li>Biomedical Sciences</li>
                     <li>Computing & Information Sciences</li>
                     <li>Engineering & Technology</li>
                     <li>Physical Sciences</li>
                     <li>Materials Science</li>
                 </ul>
                 
                 <h2>Application Deadlines</h2>
                 <ul>
                     <li><strong>June intake:</strong> Apply by December 1</li>
                     <li><strong>January intake:</strong> Apply by June 1</li>
                 </ul>
                 
                 <h2>Application Process</h2>
                 <ol>
                     <li>Choose research project from participating labs</li>
                     <li>Prepare documents (CV, academic transcripts, recommendation letters)</li>
                     <li>Submit online application</li>
                     <li>Shortlisted candidates interviewed (via video call)</li>
                     <li>Results announced 3-4 months after deadline</li>
                 </ol>
                 
                 <h2>Tips from Successful Applicants</h2>
                 <p>"I contacted potential supervisors before applying. When they knew me and my research interests, it made a huge difference!" - Dr. Wei Chen, NTU Alumni</p>
                 <p>"My research proposal was key - I spent 2 months refining it with feedback from my undergraduate thesis advisor." - Dr. Priya Kumar, NUS Alumni</p>'''),
                
                # Continue with more articles... (I'll add 21 more)
                # Article 10
                (10, 'chinese-government-scholarship-guide', 'Chinese Government Scholarship (CSC): Complete Guide 2026', 'Scholarships', 1, 'Khary', 'Jan 25, 2026', '9 min read',
                 '''<h2>What is the CSC Scholarship?</h2>
                 <p>The Chinese Government Scholarship (CSC) is the most comprehensive scholarship for international students wishing to study in China. Funded by the Chinese Ministry of Education, it covers over 280 Chinese universities.</p>
                 
                 <h2>Types of CSC Scholarships</h2>
                 <ul>
                     <li><strong>Type A:</strong> Bilateral Program - through your home country's embassy</li>
                     <li><strong>Type B:</strong> Chinese University Program - direct application to universities</li>
                     <li><strong>Great Wall Program:</strong> For UNESCO member countries</li>
                     <li><strong>EU Program:</strong> For EU students</li>
                     <li><strong>AUN Program:</strong> For ASEAN University Network members</li>
                 </ul>
                 
                 <h2>Benefits</h2>
                 <ul>
                     <li>Full tuition waiver</li>
                     <li>Free on-campus accommodation</li>
                     <li>Monthly stipend: 
                         <ul>
                             <li>Bachelor's: CNY 2,500</li>
                             <li>Master's: CNY 3,000</li>
                             <li>PhD: CNY 3,500</li>
                         </ul>
                     </li>
                     <li>Comprehensive medical insurance</li>
                 </ul>
                 
                 <h2>Eligibility</h2>
                 <ul>
                     <li><strong>Bachelor's:</strong> High school diploma, age under 25</li>
                     <li><strong>Master's:</strong> Bachelor's degree, age under 35</li>
                     <li><strong>PhD:</strong> Master's degree, age under 40</li>
                     <li>HSK 3+ for Chinese-taught programs</li>
                     <li>IELTS 6.0+ for English-taught programs</li>
                 </ul>
                 
                 <h2>Required Documents</h2>
                 <ul>
                     <li>CSC Application Form</li>
                     <li>University Application Form</li>
                     <li>Highest diploma (notarized copy)</li>
                     <li>Academic transcripts</li>
                     <li>Study plan or research proposal</li>
                     <li>2 recommendation letters</li>
                     <li>Passport copy</li>
                     <li>Physical examination form</li>
                     <li>Language proficiency certificate</li>
                 </ul>'''),
                
                # Article 11
                (11, 'top-engineering-universities-asia', 'Top 10 Engineering Universities in Asia 2026', 'Engineering', 1, 'Khary', 'Jan 20, 2026', '10 min read',
                 '''<h2>1. Tsinghua University (China)</h2>
                 <p><strong>World Rank:</strong> #16, <strong>Engineering Rank:</strong> #1 in Asia</p>
                 <p>Known as the "MIT of China," Tsinghua excels in computer science, electrical engineering, and mechanical engineering.</p>
                 
                 <h2>2. National University of Singapore (Singapore)</h2>
                 <p><strong>World Rank:</strong> #8, <strong>Engineering Rank:</strong> #2 in Asia</p>
                 <p>NUS Engineering offers 14 programs and has strong industry connections with companies like Google, Facebook, and local tech giants.</p>
                 
                 <h2>3. Nanyang Technological University (Singapore)</h2>
                 <p><strong>World Rank:</strong> #12, <strong>Engineering Rank:</strong> #3 in Asia</p>
                 <p>NTU's College of Engineering is the largest engineering college in the world with over 10,000 students.</p>
                 
                 <h2>4. Peking University (China)</h2>
                 <p><strong>World Rank:</strong> #17, <strong>Engineering Rank:</strong> #4 in Asia</p>
                 <p>Strong in computer science, software engineering, and information technology.</p>
                 
                 <h2>5. University of Tokyo (Japan)</h2>
                 <p><strong>World Rank:</strong> #23, <strong>Engineering Rank:</strong> #5 in Asia</p>
                 <p>Japan's top university for engineering, with 7 engineering departments and 22 research centers.</p>
                 
                 <h2>6. KAIST (Korea)</h2>
                 <p><strong>World Rank:</strong> #41, <strong>Engineering Rank:</strong> #6 in Asia</p>
                 <p>Known as the "MIT of Asia," KAIST focuses on research and innovation in engineering and technology.</p>
                 
                 <h2>7. Shanghai Jiao Tong University (China)</h2>
                 <p><strong>World Rank:</strong> #46, <strong>Engineering Rank:</strong> #7 in Asia</p>
                 <p>Excellence in naval architecture, mechanical engineering, and robotics.</p>
                 
                 <h2>8. Zhejiang University (China)</h2>
                 <p><strong>World Rank:</strong> #42, <strong>Engineering Rank:</strong> #8 in Asia</p>
                 <p>Strong in computer science, software engineering, and agricultural engineering.</p>
                 
                 <h2>9. Kyoto University (Japan)</h2>
                 <p><strong>World Rank:</strong> #36, <strong>Engineering Rank:</strong> #9 in Asia</p>
                 <p>Known for research in electronics, materials science, and civil engineering.</p>
                 
                 <h2>10. Seoul National University (Korea)</h2>
                 <p><strong>World Rank:</strong> #29, <strong>Engineering Rank:</strong> #10 in Asia</p>
                 <p>Comprehensive engineering programs with strong industry partnerships with Samsung, LG, and Hyundai.</p>'''),
                
                # Article 12
                (12, 'mbbs-in-china-guide', 'MBBS in China: Complete Guide for International Students', 'Medicine', 1, 'Khary', 'Jan 15, 2026', '11 min read',
                 '''<h2>Why Study MBBS in China?</h2>
                 <ul>
                     <li>Quality education at affordable cost</li>
                     <li>WHO and MCI recognized universities</li>
                     <li>Modern facilities and teaching hospitals</li>
                     <li>International learning environment</li>
                     <li>Growing healthcare sector</li>
                 </ul>
                 
                 <h2>Top Medical Universities in China</h2>
                 <table>
                     <tr><th>University</th><th>Location</th><th>Tuition/Year</th><th>MCI Approved</th></tr>
                     <tr><td>Peking University Health Science Center</td><td>Beijing</td><td>¥45,000</td><td>Yes</td></tr>
                     <tr><td>Fudan University Shanghai Medical College</td><td>Shanghai</td><td>¥42,000</td><td>Yes</td></tr>
                     <tr><td>Shanghai Jiao Tong University School of Medicine</td><td>Shanghai</td><td>¥44,000</td><td>Yes</td></tr>
                     <tr><td>Sichuan University West China Medical Center</td><td>Chengdu</td><td>¥38,000</td><td>Yes</td></tr>
                     <tr><td>Sun Yat-sen University Medical School</td><td>Guangzhou</td><td>¥40,000</td><td>Yes</td></tr>
                     <tr><td>Wuhan University Medical School</td><td>Wuhan</td><td>¥35,000</td><td>Yes</td></tr>
                 </table>
                 
                 <h2>Admission Requirements</h2>
                 <ul>
                     <li>High school diploma with Physics, Chemistry, Biology (minimum 70%)</li>
                     <li>Age 17-25 years</li>
                     <li>NEET qualification (for Indian students)</li>
                     <li>IELTS 6.0 or TOEFL 80+ (for English programs)</li>
                     <li>HSK 4 (for Chinese programs)</li>
                 </ul>
                 
                 <h2>Program Duration</h2>
                 <ul>
                     <li><strong>MBBS:</strong> 6 years (including 1 year internship)</li>
                     <li><strong>Medium of instruction:</strong> English or Chinese</li>
                 </ul>
                 
                 <h2>Cost Breakdown</h2>
                 <ul>
                     <li><strong>Tuition:</strong> ¥35,000-50,000/year</li>
                     <li><strong>Accommodation:</strong> ¥6,000-12,000/year</li>
                     <li><strong>Living expenses:</strong> ¥18,000-24,000/year</li>
                     <li><strong>Total:</strong> ¥60,000-85,000/year ($8,500-12,000 USD)</li>
                 </ul>
                 
                 <h2>Application Timeline</h2>
                 <ul>
                     <li><strong>March-June:</strong> University applications</li>
                     <li><strong>July-August:</strong> Admission letters issued</li>
                     <li><strong>August-September:</strong> Visa application</li>
                     <li><strong>September:</strong> Classes begin</li>
                 </ul>'''),
                
                # Article 14 - Singapore Universities (FIXED)
(14, 'top-universities-singapore', 'Top Universities in Singapore: Complete Guide 2026', 'Singapore', 1, 'Khary', 'March 13, 2026', '8 min read',
 '''<h2>Why Study in Singapore?</h2>
 <p>Singapore is Asia\'s education hub, with two universities consistently ranked among the world\'s top 20. Known for excellence in research, innovation, and global connections.</p>
 
 <h2>1. National University of Singapore (NUS)</h2>
 <p><strong>Ranking:</strong> #1 in Singapore, #8 World</p>
 <p><strong>Location:</strong> Singapore</p>
 <p><strong>Popular Programs:</strong> Computer Science, Engineering, Business, Law, Medicine</p>
 <p><strong>Tuition:</strong> SGD 30,000-40,000/year</p>
 
 <h2>2. Nanyang Technological University (NTU)</h2>
 <p><strong>Ranking:</strong> #2 in Singapore, #12 World</p>
 <p><strong>Location:</strong> Singapore</p>
 <p><strong>Popular Programs:</strong> Engineering, Computer Science, Business, Design</p>
 
 <h2>3. Singapore Management University (SMU)</h2>
 <p><strong>Ranking:</strong> #3 in Singapore, #87 World</p>
 <p><strong>Location:</strong> Singapore</p>
 <p><strong>Popular Programs:</strong> Business, Accountancy, Law, Economics</p>'''),

# Article 15 - Singapore Scholarships (FIXED)
(15, 'singapore-scholarships-complete-guide', 'Singapore Scholarships: Complete Guide to SINGA, ASEAN, and More', 'Scholarships', 1, 'Khary', 'March 14, 2026', '9 min read',
 '''<h2>Top Scholarships in Singapore</h2>
 
 <h2>1. Singapore International Graduate Award (SINGA)</h2>
 <p><strong>Coverage:</strong> Full tuition + SGD 2,000/month stipend + airfare</p>
 <p><strong>Deadline:</strong> June 1 & December 1</p>
 
 <h2>2. ASEAN Undergraduate Scholarship</h2>
 <p><strong>Coverage:</strong> Full tuition + living allowance</p>
 <p><strong>For:</strong> Students from ASEAN countries</p>
 
 <h2>3. NUS Merit Scholarship</h2>
 <p><strong>Coverage:</strong> Full tuition + SGD 5,800 living allowance</p>
 
 <h2>4. NTU Nanyang Scholarship</h2>
 <p><strong>Coverage:</strong> Full tuition + SGD 5,000 living allowance</p>'''),

# Article 16 - Japan Universities (FIXED)
(16, 'top-universities-japan', 'Top Universities in Japan: Complete Guide for International Students', 'Japan', 1, 'Khary', 'March 15, 2026', '10 min read',
 '''<h2>Why Study in Japan?</h2>
 <p>Japan combines cutting-edge technology with rich cultural heritage. Home to 13 Nobel laureates and world-class research facilities.</p>
 
 <h2>1. University of Tokyo (Todai)</h2>
 <p><strong>Ranking:</strong> #1 in Japan, #23 World</p>
 <p><strong>Location:</strong> Tokyo</p>
 <p><strong>Popular Programs:</strong> Engineering, Law, Economics, Medicine, Sciences</p>
 <p><strong>Tuition:</strong> ¥535,800/year</p>
 
 <h2>2. Kyoto University</h2>
 <p><strong>Ranking:</strong> #2 in Japan, #36 World</p>
 <p><strong>Location:</strong> Kyoto</p>
 <p><strong>Popular Programs:</strong> Science, Engineering, Law, Medicine</p>
 
 <h2>3. Osaka University</h2>
 <p><strong>Ranking:</strong> #3 in Japan, #55 World</p>
 <p><strong>Location:</strong> Osaka</p>
 <p><strong>Popular Programs:</strong> Engineering, Science, Medicine, Economics</p>'''),

# Article 17 - Korea Universities (FIXED)
(17, 'top-universities-korea', 'Top Universities in South Korea: Complete Guide for International Students', 'Korea', 1, 'Khary', 'March 16, 2026', '10 min read',
 '''<h2>Why Study in South Korea?</h2>
 <p>South Korea has emerged as a global leader in education, technology, and innovation. With world-class universities, cutting-edge research facilities, and the vibrant Korean Wave culture, Korea attracts over 200,000 international students annually.</p>
 
 <h2>1. Seoul National University (SNU)</h2>
 <p><strong>Ranking:</strong> #1 in Korea, #29 World</p>
 <p><strong>Location:</strong> Seoul</p>
 <p><strong>Popular Programs:</strong> Engineering, Business, Medicine, Law, Sciences</p>
 <p><strong>Tuition:</strong> KRW 5,000,000-7,000,000/year</p>
 
 <h2>2. KAIST</h2>
 <p><strong>Ranking:</strong> #2 in Korea, #41 World</p>
 <p><strong>Location:</strong> Daejeon</p>
 <p><strong>Popular Programs:</strong> Electrical Engineering, Computer Science, Mechanical Engineering</p>
 
 <h2>3. Yonsei University</h2>
 <p><strong>Ranking:</strong> #3 in Korea, #73 World</p>
 <p><strong>Location:</strong> Seoul</p>
 <p><strong>Popular Programs:</strong> Business, Medicine, Engineering, Economics</p>'''),

# Article 18 - Korea University Rankings Part 2 (FIXED)
(18, 'top-korean-universities-part2', 'More Top Universities in Korea: Complete Guide', 'Korea', 1, 'Khary', 'March 17, 2026', '8 min read',
 '''<h2>More Top Universities in South Korea</h2>
 
 <h2>4. Korea University</h2>
 <p><strong>Ranking:</strong> #4 in Korea, #74 World</p>
 <p><strong>Location:</strong> Seoul</p>
 <p><strong>Popular Programs:</strong> Law, Political Science, Business, Engineering</p>
 
 <h2>5. POSTECH</h2>
 <p><strong>Ranking:</strong> #5 in Korea, #81 World</p>
 <p><strong>Location:</strong> Pohang</p>
 <p><strong>Popular Programs:</strong> Material Science, Computer Science, Mechanical Engineering</p>
 
 <h2>6. Sungkyunkwan University (SKKU)</h2>
 <p><strong>Ranking:</strong> #6 in Korea, #97 World</p>
 <p><strong>Location:</strong> Seoul</p>
 <p><strong>Popular Programs:</strong> Business, Engineering, Medicine, Law</p>
 
 <h2>7. Hanyang University</h2>
 <p><strong>Ranking:</strong> #7 in Korea, #104 World</p>
 <p><strong>Location:</strong> Seoul</p>
 <p><strong>Popular Programs:</strong> Engineering, Architecture, Business</p>'''),

                (14, 'top-universities-singapore', 'Top Universities in Singapore: Complete Guide 2026', 'Singapore', 1, 'Khary', 'March 13, 2026', '8 min read', '<h2>Why Study in Singapore?</h2> <p>Singapore is Asia\'s education hub, with two universities consistently ranked among the world\'s top 20. Known for excellence in research, innovation, and global connections.</p> <h2>1. National University of Singapore (NUS)</h2> <p><strong>Ranking:</strong> #1 in Singapore, #8 World</p> <p><strong>Location:</strong> Singapore</p> <p><strong>Popular Programs:</strong> Computer Science, Engineering, Business, Law, Medicine</p> <p><strong>Tuition:</strong> SGD 30,000-40,000/year</p> <h2>2. Nanyang Technological University (NTU)</h2> <p><strong>Ranking:</strong> #2 in Singapore, #12 World</p> <p><strong>Location:</strong> Singapore</p> <p><strong>Popular Programs:</strong> Engineering, Computer Science, Business, Design</p> <h2>3. Singapore Management University (SMU)</h2> <p><strong>Ranking:</strong> #3 in Singapore, #87 World</p> <p><strong>Location:</strong> Singapore</p> <p><strong>Popular Programs:</strong> Business, Accountancy, Law, Economics</p>'),
    
                  

                 ]
            
            for post in posts:
                c.execute('''INSERT INTO blog_posts 
                           (id, slug, title, category, author_id, author_name, date, read_time, content)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', post)
            
            conn.commit()
            print("✅ 30 blog posts initialized")
        
        conn.close()
    except Exception as e:
        print(f"❌ Error initializing blog posts: {e}") 
 
# ==================== AUTHOR PROFILES ====================
@app.route('/author/<int:author_id>')
@login_required
def author_profile(author_id):
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    
    # Get author info
    c.execute("SELECT * FROM authors WHERE id = ?", (author_id,))
    author = c.fetchone()
    
    if not author:
        # Default author if not found
        author = {
            'name': 'Khary',
            'bio': 'Study abroad expert with 10+ years of experience helping students get into top Asian universities. Khary has personally guided 1000+ students to their dream schools.',
            'role': 'Founder & CEO',
            'avatar': '/static/khary-profile.jpg',
            'articles_count': 45,
            'followers': 1250,
            'joined_date': '2024'
        }
    
    # Get author's articles
    c.execute("SELECT id, title, category, date, read_time, views, likes FROM blog_posts WHERE author_id = ? ORDER BY date DESC", (author_id,))
    articles = c.fetchall()
    
    conn.close()
    
    return render_template('author.html', author=author, articles=articles)

@app.route('/api/follow-author', methods=['POST'])
@login_required
def follow_author():
    data = request.json
    author_id = data.get('author_id')
    user_id = session['user_id']
    
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    
    # Check if already following
    c.execute("SELECT * FROM author_followers WHERE user_id = ? AND author_id = ?", (user_id, author_id))
    existing = c.fetchone()
    
    if existing:
        # Unfollow
        c.execute("DELETE FROM author_followers WHERE user_id = ? AND author_id = ?", (user_id, author_id))
        c.execute("UPDATE authors SET followers = followers - 1 WHERE id = ?", (author_id,))
        action = 'unfollowed'
    else:
        # Follow
        c.execute("INSERT INTO author_followers (user_id, author_id) VALUES (?, ?)", (user_id, author_id))
        c.execute("UPDATE authors SET followers = followers + 1 WHERE id = ?", (author_id,))
        action = 'followed'
    
    conn.commit()
    
    # Get new follower count
    c.execute("SELECT followers FROM authors WHERE id = ?", (author_id,))
    followers = c.fetchone()[0]
    conn.close()
    
    return jsonify({'success': True, 'action': action, 'followers': followers})               
        
# ==================== BLOG SEARCH ====================
@app.route('/blog/search')
@login_required
def blog_search():
    query = request.args.get('q', '')
    category = request.args.get('category', 'all')
    
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    
    sql = "SELECT id, title, category, date, excerpt, views, likes FROM blog_posts WHERE published = 1"
    params = []
    
    if query:
        sql += " AND (title LIKE ? OR content LIKE ? OR excerpt LIKE ?)"
        search_term = f'%{query}%'
        params.extend([search_term, search_term, search_term])
    
    if category != 'all':
        sql += " AND category = ?"
        params.append(category)
    
    sql += " ORDER BY date DESC"
    
    c.execute(sql, params)
    results = c.fetchall()
    conn.close()
    
    return render_template('search_results.html', results=results, query=query, category=category)

@app.route('/api/blog/posts')

def get_blog_posts():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, title, category, date, read_time, content FROM blog_posts ORDER BY id")
    posts = c.fetchall()
    conn.close()
    
    result = []
    for p in posts:
        # Clean excerpt from HTML
        import re
        clean_text = re.sub(r'<[^>]+>', '', p[5][:200]) if p[5] else ''
        excerpt = clean_text[:150] + '...' if clean_text else ''
        
        result.append({
            'id': p[0],
            'title': p[1],
            'category': p[2],
            'date': p[3],
            'read_time': p[4],
            'excerpt': excerpt
        })
    
    return jsonify(result)


# ==================== FILE UPLOAD CONFIGURATION ====================
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database
init_db()

# ==================== COMPLETE UNIVERSITY DATA - 75 UNIVERSITIES ====================

# ==================== CHINA - 30 UNIVERSITIES ====================
china_universities = [
    {
        "id": 101,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Tsinghua University",
        "ranking": "#1 in China",
        "world_ranking": "16th",
        "location": "Beijing",
        "established": "1911",
        "students": "50,000+",
        "international": "12%",
        "description": "China's premier university for engineering and computer science. Known as the 'MIT of China'. Consistently ranked as China's best university with world-class research facilities and Nobel laureate faculty members.",
        "programs": {
            "undergraduate": ["Computer Science", "Electrical Engineering", "Economics", "International Relations", "Law", "Architecture", "Automation", "Business Administration"],
            "graduate": ["AI & Robotics", "Business Analytics", "Environmental Engineering", "Global Governance", "Data Science", "MBA", "Financial Engineering"],
            "phd": ["PhD in Computer Science", "PhD in Economics", "PhD in Engineering", "PhD in Physics", "PhD in Architecture", "PhD in Business"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma (85%+)", "HSK Level 4", "IELTS 6.5 (min 6.0)", "SAT 1400+/ACT 30+", "3 Recommendation Letters", "Personal Statement"],
            "graduate": ["Bachelor's Degree (3.5/4.0 GPA)", "HSK Level 5", "IELTS 7.0 (min 6.5)", "GRE 320+/GMAT 700+", "Research Proposal", "2-3 Years Work Experience"],
            "phd": ["Master's Degree", "HSK Level 6", "IELTS 7.5", "Research Publications", "Interview", "Detailed Research Plan"]
        },
        "fees": {
            "undergraduate": "26,000 - 40,000 RMB/year ($3,600 - $5,500 USD)",
            "graduate": "30,000 - 45,000 RMB/year ($4,100 - $6,200 USD)",
            "phd": "32,000 - 48,000 RMB/year ($4,400 - $6,600 USD)"
        },
        "scholarships": [
            {
                "name": "Chinese Government Scholarship (CSC)",
                "coverage": "Full tuition + accommodation + monthly stipend (3,000 RMB)",
                "deadline": "January-March",
                "eligibility": "All international students"
            },
            {
                "name": "Tsinghua University Scholarship",
                "coverage": "50-100% tuition reduction",
                "deadline": "Same as application",
                "eligibility": "Top 10% applicants"
            },
            {
                "name": "Beijing Government Scholarship",
                "coverage": "20,000 - 40,000 RMB/year",
                "deadline": "March-April",
                "eligibility": "Students with excellent academic records"
            },
            {
                "name": "Confucius Institute Scholarship",
                "coverage": "Full tuition + accommodation",
                "deadline": "May-June",
                "eligibility": "Chinese language students"
            }
        ],
        "deadlines": {"fall": "March 15", "spring": "October 30"},
        "accepted_students": "500+ international students yearly",
        "acceptance_rate": "10-15%",
        "language": "Chinese/English",
        "website": "www.tsinghua.edu.cn",
        "image": "🎓",
        "ranking_world": "16th"
    },
    {
        "id": 102,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Peking University",
        "ranking": "#2 in China",
        "world_ranking": "17th",
        "location": "Beijing",
        "established": "1898",
        "students": "45,000+",
        "international": "15%",
        "description": "Leading university in humanities, social sciences and medicine. Known as the 'Harvard of China'. Produced numerous Chinese leaders and has the best medical school in China.",
        "programs": {
            "undergraduate": ["Medicine", "Law", "Chinese Literature", "Economics", "International Business", "Philosophy", "History", "Political Science"],
            "graduate": ["MBA", "Public Health", "International Law", "Chinese Philosophy", "Global Studies", "Public Policy", "Medical Research"],
            "phd": ["PhD in Medicine", "PhD in Law", "PhD in Economics", "PhD in Philosophy", "PhD in History", "PhD in Chinese Literature"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma (85%+)", "HSK Level 5", "IELTS 7.0 (min 6.5)", "SAT 1450+/ACT 32+", "Personal Statement", "Interview"],
            "graduate": ["Bachelor's Degree (3.5/4.0 GPA)", "HSK Level 5", "IELTS 7.0", "GRE 315+/GMAT 680+", "Work Experience", "Research Proposal"],
            "phd": ["Master's Degree", "HSK Level 6", "IELTS 7.5", "Publications", "Research Plan", "Interview"]
        },
        "fees": {
            "undergraduate": "24,000 - 38,000 RMB/year ($3,300 - $5,200 USD)",
            "graduate": "28,000 - 42,000 RMB/year ($3,800 - $5,800 USD)",
            "phd": "30,000 - 45,000 RMB/year ($4,100 - $6,200 USD)"
        },
        "scholarships": [
            {
                "name": "Peking University Scholarship",
                "coverage": "Full tuition + stipend",
                "deadline": "March",
                "eligibility": "Outstanding international students"
            },
            {
                "name": "Beijing Government Scholarship",
                "coverage": "20,000 - 40,000 RMB/year",
                "deadline": "April",
                "eligibility": "All international students"
            },
            {
                "name": "Confucius Institute Scholarship",
                "coverage": "Full tuition",
                "deadline": "May",
                "eligibility": "Chinese language majors"
            },
            {
                "name": "New Students Scholarship",
                "coverage": "50% tuition first year",
                "deadline": "Automatic consideration",
                "eligibility": "Top 15% admitted students"
            }
        ],
        "deadlines": {"fall": "March 31", "spring": "November 15"},
        "accepted_students": "450+ international students yearly",
        "acceptance_rate": "12-18%",
        "language": "Chinese/English",
        "website": "www.pku.edu.cn",
        "image": "🏛️"
    },
    {
        "id": 103,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Fudan University",
        "ranking": "#3 in China",
        "world_ranking": "34th",
        "location": "Shanghai",
        "established": "1905",
        "students": "40,000+",
        "international": "14%",
        "description": "Top university in Shanghai, strong in business and medicine. Located in China's financial capital with excellent industry connections and internship opportunities.",
        "programs": {
            "undergraduate": ["Business", "Medicine", "Journalism", "Economics", "Pharmacy", "International Relations", "Law"],
            "graduate": ["MBA", "International Business", "Public Policy", "Biomedical Research", "Finance", "Data Science"],
            "phd": ["PhD in Management", "PhD in Medicine", "PhD in Economics", "PhD in Pharmacy"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "HSK Level 4", "IELTS 6.5", "SAT/ACT", "Essays"],
            "graduate": ["Bachelor's Degree", "HSK Level 5", "IELTS 6.5", "GMAT/GRE", "Work Experience"],
            "phd": ["Master's Degree", "HSK Level 6", "IELTS 7.0", "Research Papers"]
        },
        "fees": {
            "undergraduate": "22,000 - 36,000 RMB/year ($3,000 - $5,000 USD)",
            "graduate": "26,000 - 40,000 RMB/year ($3,600 - $5,500 USD)",
            "phd": "28,000 - 42,000 RMB/year ($3,800 - $5,800 USD)"
        },
        "scholarships": [
            {"name": "Shanghai Government Scholarship", "coverage": "Full tuition", "deadline": "April"},
            {"name": "Fudan University Scholarship", "coverage": "50-100% tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"},
            {"name": "Excellence Scholarship", "coverage": "10,000-30,000 RMB", "deadline": "September"}
        ],
        "deadlines": {"fall": "April 15", "spring": "November 30"},
        "accepted_students": "400+",
        "acceptance_rate": "15-20%",
        "image": "🏙️"
    },
    {
        "id": 104,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Shanghai Jiao Tong University",
        "ranking": "#4 in China",
        "world_ranking": "46th",
        "location": "Shanghai",
        "established": "1896",
        "students": "42,000+",
        "international": "13%",
        "description": "Excellence in engineering, technology and business. Strong industry connections with companies like Tesla, General Motors, and Chinese tech giants.",
        "programs": {
            "undergraduate": ["Mechanical Engineering", "Naval Architecture", "Business", "Computer Science", "Data Science", "Electrical Engineering"],
            "graduate": ["Data Science", "Robotics", "Finance", "Supply Chain", "AI Engineering", "MBA"],
            "phd": ["PhD in Engineering", "PhD in Management", "PhD in Computer Science"]
        },
        "fees": {
            "undergraduate": "24,000 - 38,000 RMB/year",
            "graduate": "28,000 - 42,000 RMB/year",
            "phd": "30,000 - 45,000 RMB/year"
        },
        "scholarships": [
            {"name": "SJTU Scholarship", "coverage": "Full tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"},
            {"name": "Shanghai Government Scholarship", "coverage": "20,000-40,000 RMB", "deadline": "April"}
        ],
        "deadlines": {"fall": "March 31", "spring": "October 31"},
        "accepted_students": "380+",
        "image": "⚙️"
    },
    {
        "id": 105,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Zhejiang University",
        "ranking": "#5 in China",
        "world_ranking": "42nd",
        "location": "Hangzhou",
        "established": "1897",
        "students": "48,000+",
        "international": "12%",
        "description": "Comprehensive university with strong engineering and agriculture. Located in beautiful Hangzhou, home to Alibaba and many tech companies.",
        "programs": {
            "undergraduate": ["Agricultural Science", "Computer Science", "Chemical Engineering", "Economics", "Food Science", "Software Engineering"],
            "graduate": ["Food Science", "AI", "Environmental Science", "MBA", "Biotechnology"],
            "phd": ["PhD in Agriculture", "PhD in Engineering", "PhD in Computer Science"]
        },
        "fees": {
            "undergraduate": "22,000 - 35,000 RMB/year",
            "graduate": "26,000 - 38,000 RMB/year",
            "phd": "28,000 - 40,000 RMB/year"
        },
        "scholarships": [
            {"name": "ZJU Presidential Scholarship", "coverage": "100% tuition + stipend", "deadline": "April"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"},
            {"name": "Zhejiang Government Scholarship", "coverage": "20,000-30,000 RMB", "deadline": "May"}
        ],
        "deadlines": {"fall": "April 15", "spring": "November 15"},
        "accepted_students": "350+",
        "image": "🌾"
    },
    {
        "id": 106,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "University of Science and Technology of China",
        "ranking": "#6 in China",
        "world_ranking": "93rd",
        "location": "Hefei",
        "established": "1958",
        "students": "35,000+",
        "international": "8%",
        "description": "Leading research university in science and technology. Known for physics, quantum research, and producing Nobel laureates.",
        "programs": {
            "undergraduate": ["Physics", "Chemistry", "Mathematics", "Computer Science", "Quantum Technology", "Material Science"],
            "graduate": ["Quantum Physics", "Material Science", "Biotechnology", "Data Science", "Nanotechnology"],
            "phd": ["PhD in Physics", "PhD in Chemistry", "PhD in Computer Science"]
        },
        "fees": {
            "undergraduate": "20,000 - 32,000 RMB/year",
            "graduate": "24,000 - 36,000 RMB/year",
            "phd": "26,000 - 38,000 RMB/year"
        },
        "scholarships": [
            {"name": "CAS-TWAS Scholarship", "coverage": "Full package", "deadline": "February"},
            {"name": "USTC Scholarship", "coverage": "50-100% tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "January"}
        ],
        "deadlines": {"fall": "March 15", "spring": "October 30"},
        "accepted_students": "200+",
        "image": "🔬"
    },
    {
        "id": 107,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Nanjing University",
        "ranking": "#7 in China",
        "world_ranking": "95th",
        "location": "Nanjing",
        "established": "1902",
        "students": "38,000+",
        "international": "11%",
        "description": "Historic university strong in humanities and sciences. One of China's most beautiful campuses with rich cultural heritage.",
        "programs": {
            "undergraduate": ["Chinese Language", "History", "Geology", "Economics", "Environmental Science", "Astronomy"],
            "graduate": ["Chinese Studies", "Environmental Science", "International Relations", "MBA"],
            "phd": ["PhD in History", "PhD in Geology", "PhD in Literature"]
        },
        "fees": {
            "undergraduate": "20,000 - 34,000 RMB/year",
            "graduate": "24,000 - 38,000 RMB/year",
            "phd": "26,000 - 40,000 RMB/year"
        },
        "scholarships": [
            {"name": "Jiangsu Provincial Scholarship", "coverage": "30,000-50,000 RMB", "deadline": "April"},
            {"name": "NJU Scholarship", "coverage": "50% tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 15"},
        "accepted_students": "250+",
        "image": "📚"
    },
    {
        "id": 108,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Wuhan University",
        "ranking": "#8 in China",
        "world_ranking": "157th",
        "location": "Wuhan",
        "established": "1893",
        "students": "45,000+",
        "international": "10%",
        "description": "Beautiful campus, strong in law and economics. Famous for cherry blossoms and comprehensive programs.",
        "programs": {
            "undergraduate": ["Law", "Economics", "Surveying", "Computer Science", "Remote Sensing", "Hydrology"],
            "graduate": ["International Law", "Finance", "Remote Sensing", "MBA", "Environmental Engineering"],
            "phd": ["PhD in Law", "PhD in Economics", "PhD in Engineering"]
        },
        "fees": {
            "undergraduate": "20,000 - 33,000 RMB/year",
            "graduate": "24,000 - 37,000 RMB/year",
            "phd": "26,000 - 39,000 RMB/year"
        },
        "scholarships": [
            {"name": "Hubei Provincial Scholarship", "coverage": "20,000-40,000 RMB", "deadline": "April"},
            {"name": "WHU Scholarship", "coverage": "50-100% tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"}
        ],
        "deadlines": {"fall": "April 15", "spring": "November 30"},
        "accepted_students": "280+",
        "image": "🌸"
    },
    {
        "id": 109,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Harbin Institute of Technology",
        "ranking": "#9 in China",
        "world_ranking": "260th",
        "location": "Harbin",
        "established": "1920",
        "students": "40,000+",
        "international": "9%",
        "description": "Top engineering university, strong in aerospace and robotics. Key contributor to China's space program.",
        "programs": {
            "undergraduate": ["Aerospace Engineering", "Mechanical Engineering", "Robotics", "Material Science", "Control Systems"],
            "graduate": ["Space Technology", "Control Systems", "Advanced Materials", "Energy Engineering"],
            "phd": ["PhD in Aerospace", "PhD in Mechanical Engineering", "PhD in Robotics"]
        },
        "fees": {
            "undergraduate": "18,000 - 30,000 RMB/year",
            "graduate": "22,000 - 34,000 RMB/year",
            "phd": "24,000 - 36,000 RMB/year"
        },
        "scholarships": [
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"},
            {"name": "HIT Scholarship", "coverage": "50-100% tuition", "deadline": "March"},
            {"name": "Heilongjiang Scholarship", "coverage": "20,000 RMB", "deadline": "May"}
        ],
        "deadlines": {"fall": "March 31", "spring": "October 31"},
        "accepted_students": "220+",
        "image": "🚀"
    },
    {
        "id": 110,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Xi'an Jiaotong University",
        "ranking": "#10 in China",
        "world_ranking": "290th",
        "location": "Xi'an",
        "established": "1896",
        "students": "38,000+",
        "international": "8%",
        "description": "Leading university in management and engineering. Located in historic capital with rich cultural experiences.",
        "programs": {
            "undergraduate": ["Electrical Engineering", "Management", "Energy", "Computer Science", "Biomedical Engineering"],
            "graduate": ["Power Systems", "MBA", "Renewable Energy", "Big Data", "Energy Engineering"],
            "phd": ["PhD in Engineering", "PhD in Management", "PhD in Energy"]
        },
        "fees": {
            "undergraduate": "18,000 - 32,000 RMB/year",
            "graduate": "22,000 - 36,000 RMB/year",
            "phd": "24,000 - 38,000 RMB/year"
        },
        "scholarships": [
            {"name": "Shaanxi Provincial Scholarship", "coverage": "20,000 RMB", "deadline": "April"},
            {"name": "XJTU Scholarship", "coverage": "50% tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"}
        ],
        "deadlines": {"fall": "April 15", "spring": "November 15"},
        "accepted_students": "200+",
        "image": "🏯"
    },
    {
        "id": 111,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Sun Yat-sen University",
        "ranking": "#11 in China",
        "world_ranking": "159th",
        "location": "Guangzhou",
        "established": "1924",
        "students": "42,000+",
        "international": "12%",
        "description": "Comprehensive university in Southern China. Strong in medicine, business, and marine sciences with tropical climate.",
        "programs": {
            "undergraduate": ["Medicine", "Business", "Marine Science", "Computer Science", "Pharmacy", "Dentistry"],
            "graduate": ["Clinical Medicine", "International Business", "Marine Biology", "Data Science", "Public Health"],
            "phd": ["PhD in Medicine", "PhD in Marine Science", "PhD in Business"]
        },
        "fees": {
            "undergraduate": "22,000 - 36,000 RMB/year",
            "graduate": "26,000 - 40,000 RMB/year",
            "phd": "28,000 - 42,000 RMB/year"
        },
        "scholarships": [
            {"name": "Guangdong Provincial Scholarship", "coverage": "20,000-40,000 RMB", "deadline": "April"},
            {"name": "SYSU Scholarship", "coverage": "50-100% tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 30"},
        "accepted_students": "320+",
        "image": "🌊"
    },
    {
        "id": 112,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Beijing Normal University",
        "ranking": "#12 in China",
        "world_ranking": "251st",
        "location": "Beijing",
        "established": "1902",
        "students": "35,000+",
        "international": "13%",
        "description": "Top teacher training and education research. Strong in psychology, education, and Chinese language teaching.",
        "programs": {
            "undergraduate": ["Education", "Psychology", "Chinese Language", "History", "Geography", "Environmental Science"],
            "graduate": ["Educational Leadership", "Child Psychology", "Teaching Chinese", "Curriculum Development", "Applied Psychology"],
            "phd": ["PhD in Education", "PhD in Psychology", "PhD in Chinese Studies"]
        },
        "fees": {
            "undergraduate": "20,000 - 34,000 RMB/year",
            "graduate": "24,000 - 38,000 RMB/year",
            "phd": "26,000 - 40,000 RMB/year"
        },
        "scholarships": [
            {"name": "Confucius Institute Scholarship", "coverage": "Full tuition", "deadline": "May"},
            {"name": "BNU Scholarship", "coverage": "50-100% tuition", "deadline": "March"},
            {"name": "Beijing Government Scholarship", "coverage": "20,000 RMB", "deadline": "April"}
        ],
        "deadlines": {"fall": "March 31", "spring": "October 31"},
        "accepted_students": "250+",
        "image": "📖"
    },
    {
        "id": 113,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Tianjin University",
        "ranking": "#13 in China",
        "world_ranking": "334th",
        "location": "Tianjin",
        "established": "1895",
        "students": "37,000+",
        "international": "9%",
        "description": "China's first modern university, strong in engineering and architecture. Close to Beijing with lower cost of living.",
        "programs": {
            "undergraduate": ["Chemical Engineering", "Architecture", "Civil Engineering", "Management", "Environmental Engineering"],
            "graduate": ["Chemical Technology", "Urban Planning", "Structural Engineering", "MBA", "Project Management"],
            "phd": ["PhD in Chemical Engineering", "PhD in Architecture", "PhD in Civil Engineering"]
        },
        "fees": {
            "undergraduate": "18,000 - 32,000 RMB/year",
            "graduate": "22,000 - 36,000 RMB/year",
            "phd": "24,000 - 38,000 RMB/year"
        },
        "scholarships": [
            {"name": "Tianjin Government Scholarship", "coverage": "20,000 RMB", "deadline": "April"},
            {"name": "TJU Scholarship", "coverage": "50% tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"}
        ],
        "deadlines": {"fall": "April 15", "spring": "November 15"},
        "accepted_students": "180+",
        "image": "🏗️"
    },
    {
        "id": 114,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Sichuan University",
        "ranking": "#14 in China",
        "world_ranking": "355th",
        "location": "Chengdu",
        "established": "1896",
        "students": "40,000+",
        "international": "10%",
        "description": "Leading university in Western China, strong in medicine and dentistry. Famous for pandas and Sichuan cuisine.",
        "programs": {
            "undergraduate": ["Stomatology", "Pharmacy", "Chinese Medicine", "Material Science", "Dentistry", "Biomedical Engineering"],
            "graduate": ["Dentistry", "Pharmaceutical Sciences", "Traditional Medicine", "Biomaterials", "Public Health"],
            "phd": ["PhD in Stomatology", "PhD in Pharmacy", "PhD in Chinese Medicine"]
        },
        "fees": {
            "undergraduate": "18,000 - 34,000 RMB/year",
            "graduate": "22,000 - 38,000 RMB/year",
            "phd": "24,000 - 40,000 RMB/year"
        },
        "scholarships": [
            {"name": "Sichuan Provincial Scholarship", "coverage": "20,000 RMB", "deadline": "April"},
            {"name": "SCU Scholarship", "coverage": "50% tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 30"},
        "accepted_students": "220+",
        "image": "🏔️"
    },
    {
        "id": 115,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Shandong University",
        "ranking": "#15 in China",
        "world_ranking": "403rd",
        "location": "Jinan/Qingdao",
        "established": "1901",
        "students": "43,000+",
        "international": "11%",
        "description": "Comprehensive university with strong humanities and marine sciences. Has campuses in both Jinan and coastal Qingdao.",
        "programs": {
            "undergraduate": ["Chinese Culture", "Marine Biology", "Mathematics", "Economics", "Korean Studies", "Oceanography"],
            "graduate": ["Chinese Philosophy", "Marine Science", "Financial Mathematics", "International Trade", "Marine Engineering"],
            "phd": ["PhD in Literature", "PhD in Marine Science", "PhD in Mathematics"]
        },
        "fees": {
            "undergraduate": "18,000 - 32,000 RMB/year",
            "graduate": "22,000 - 36,000 RMB/year",
            "phd": "24,000 - 38,000 RMB/year"
        },
        "scholarships": [
            {"name": "Shandong Government Scholarship", "coverage": "20,000 RMB", "deadline": "April"},
            {"name": "SDU Scholarship", "coverage": "50% tuition", "deadline": "March"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"}
        ],
        "deadlines": {"fall": "April 15", "spring": "November 15"},
        "accepted_students": "250+",
        "image": "🌊"
    }
]

# ==================== CHINA - ADDITIONAL 15 UNIVERSITIES (16-30) ====================
china_universities_extra = [
    {
        "id": 116,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Tongji University",
        "ranking": "#16 in China",
        "world_ranking": "211th",
        "location": "Shanghai",
        "established": "1907",
        "students": "36,000+",
        "international": "11%",
        "description": "Leading university in engineering, architecture, and urban planning. Famous for German-style education and strong industry partnerships.",
        "programs": {
            "undergraduate": ["Architecture", "Civil Engineering", "Urban Planning", "Design", "Automotive Engineering"],
            "graduate": ["Architecture", "Transportation Engineering", "Environmental Engineering", "MBA"],
            "phd": ["PhD in Architecture", "PhD in Civil Engineering", "PhD in Design"]
        },
        "fees": {
            "undergraduate": "20,000 - 35,000 RMB/year",
            "graduate": "24,000 - 38,000 RMB/year",
            "phd": "26,000 - 40,000 RMB/year"
        },
        "scholarships": [
            {"name": "Shanghai Government Scholarship", "coverage": "20,000-40,000 RMB", "deadline": "April"},
            {"name": "Tongji University Scholarship", "coverage": "50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 15"},
        "accepted_students": "300+",
        "image": "🏛️"
    },
    {
        "id": 117,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Beihang University (BUAA)",
        "ranking": "#17 in China",
        "world_ranking": "251st",
        "location": "Beijing",
        "established": "1952",
        "students": "30,000+",
        "international": "8%",
        "description": "Top university for aerospace engineering and technology. Key contributor to China's space program and satellite development.",
        "programs": {
            "undergraduate": ["Aerospace Engineering", "Computer Science", "Mechanical Engineering", "Automation"],
            "graduate": ["Space Technology", "Aviation Engineering", "Robotics", "Materials Science"],
            "phd": ["PhD in Aerospace", "PhD in Computer Science", "PhD in Engineering"]
        },
        "fees": {
            "undergraduate": "19,000 - 33,000 RMB/year",
            "graduate": "23,000 - 37,000 RMB/year",
            "phd": "25,000 - 39,000 RMB/year"
        },
        "scholarships": [
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"},
            {"name": "BUAA Scholarship", "coverage": "50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "March 31", "spring": "October 31"},
        "accepted_students": "200+",
        "image": "🚀"
    },
    {
        "id": 118,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "East China Normal University",
        "ranking": "#18 in China",
        "world_ranking": "301st",
        "location": "Shanghai",
        "established": "1951",
        "students": "32,000+",
        "international": "14%",
        "description": "Leading normal university, strong in education, humanities, and teacher training. Known for its beautiful campus and research output.",
        "programs": {
            "undergraduate": ["Education", "Chinese Language", "Psychology", "History", "Geography"],
            "graduate": ["Educational Leadership", "Teaching Chinese", "Applied Psychology", "MBA"],
            "phd": ["PhD in Education", "PhD in Psychology", "PhD in Chinese Literature"]
        },
        "fees": {
            "undergraduate": "18,000 - 32,000 RMB/year",
            "graduate": "22,000 - 36,000 RMB/year",
            "phd": "24,000 - 38,000 RMB/year"
        },
        "scholarships": [
            {"name": "Confucius Institute Scholarship", "coverage": "Full tuition", "deadline": "May"},
            {"name": "ECNU Scholarship", "coverage": "50% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 15"},
        "accepted_students": "350+",
        "image": "📚"
    },
    {
        "id": 119,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "South China University of Technology",
        "ranking": "#19 in China",
        "world_ranking": "341st",
        "location": "Guangzhou",
        "established": "1952",
        "students": "40,000+",
        "international": "9%",
        "description": "Leading university in engineering and technology in Southern China. Strong industry connections with Pearl River Delta companies.",
        "programs": {
            "undergraduate": ["Chemical Engineering", "Food Science", "Light Industry", "Materials", "Computer Science"],
            "graduate": ["Food Technology", "Chemical Engineering", "Materials Science", "MBA"],
            "phd": ["PhD in Chemical Engineering", "PhD in Food Science", "PhD in Materials"]
        },
        "fees": {
            "undergraduate": "19,000 - 34,000 RMB/year",
            "graduate": "23,000 - 38,000 RMB/year",
            "phd": "25,000 - 40,000 RMB/year"
        },
        "scholarships": [
            {"name": "Guangdong Government Scholarship", "coverage": "20,000-30,000 RMB", "deadline": "April"},
            {"name": "SCUT Scholarship", "coverage": "50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "April 15", "spring": "November 30"},
        "accepted_students": "180+",
        "image": "🔧"
    },
    {
        "id": 120,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "University of Electronic Science and Technology of China",
        "ranking": "#20 in China",
        "world_ranking": "371st",
        "location": "Chengdu",
        "established": "1956",
        "students": "33,000+",
        "international": "7%",
        "description": "Top university for electronics, communication, and computer science. Key research center for information technology in Western China.",
        "programs": {
            "undergraduate": ["Electronic Engineering", "Communication", "Computer Science", "Software Engineering"],
            "graduate": ["Communication Systems", "Signal Processing", "AI", "Cybersecurity"],
            "phd": ["PhD in Electronics", "PhD in Communication", "PhD in Computer Science"]
        },
        "fees": {
            "undergraduate": "18,000 - 32,000 RMB/year",
            "graduate": "22,000 - 36,000 RMB/year",
            "phd": "24,000 - 38,000 RMB/year"
        },
        "scholarships": [
            {"name": "Sichuan Government Scholarship", "coverage": "20,000 RMB", "deadline": "April"},
            {"name": "UESTC Scholarship", "coverage": "50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 15"},
        "accepted_students": "150+",
        "image": "💻"
    },
    {
        "id": 121,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Dalian University of Technology",
        "ranking": "#21 in China",
        "world_ranking": "401st",
        "location": "Dalian",
        "established": "1949",
        "students": "35,000+",
        "international": "8%",
        "description": "Key university in Liaoning province, strong in engineering and technology. Coastal location with strong marine engineering programs.",
        "programs": {
            "undergraduate": ["Mechanical Engineering", "Chemical Engineering", "Civil Engineering", "Naval Architecture"],
            "graduate": ["Engineering Mechanics", "Chemical Technology", "Port & Coastal Engineering"],
            "phd": ["PhD in Mechanical Engineering", "PhD in Chemical Engineering"]
        },
        "fees": {
            "undergraduate": "17,000 - 31,000 RMB/year",
            "graduate": "21,000 - 35,000 RMB/year",
            "phd": "23,000 - 37,000 RMB/year"
        },
        "scholarships": [
            {"name": "Liaoning Government Scholarship", "coverage": "20,000 RMB", "deadline": "May"},
            {"name": "DUT Scholarship", "coverage": "50% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "May 15", "spring": "December 15"},
        "accepted_students": "120+",
        "image": "⚓"
    },
    {
        "id": 122,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Northwestern Polytechnical University",
        "ranking": "#22 in China",
        "world_ranking": "431st",
        "location": "Xi'an",
        "established": "1938",
        "students": "32,000+",
        "international": "6%",
        "description": "Leading university in aeronautics, astronautics, and marine engineering. Critical role in China's defense and aerospace industry.",
        "programs": {
            "undergraduate": ["Aeronautical Engineering", "Astronautics", "Marine Engineering", "Materials"],
            "graduate": ["Flight Vehicle Design", "Propulsion", "Control Systems", "Aerospace Materials"],
            "phd": ["PhD in Aerospace", "PhD in Marine Engineering", "PhD in Materials"]
        },
        "fees": {
            "undergraduate": "17,000 - 31,000 RMB/year",
            "graduate": "21,000 - 35,000 RMB/year",
            "phd": "23,000 - 37,000 RMB/year"
        },
        "scholarships": [
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"},
            {"name": "NPU Scholarship", "coverage": "50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "March 31", "spring": "October 31"},
        "accepted_students": "100+",
        "image": "✈️"
    },
    {
        "id": 123,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "China Agricultural University",
        "ranking": "#23 in China",
        "world_ranking": "451st",
        "location": "Beijing",
        "established": "1905",
        "students": "30,000+",
        "international": "7%",
        "description": "Top university for agriculture, food science, and biotechnology. Leading research in crop science and agricultural innovation.",
        "programs": {
            "undergraduate": ["Agriculture", "Food Science", "Biotechnology", "Veterinary Medicine", "Environmental Science"],
            "graduate": ["Crop Science", "Food Technology", "Animal Science", "Plant Protection"],
            "phd": ["PhD in Agriculture", "PhD in Food Science", "PhD in Biotechnology"]
        },
        "fees": {
            "undergraduate": "16,000 - 30,000 RMB/year",
            "graduate": "20,000 - 34,000 RMB/year",
            "phd": "22,000 - 36,000 RMB/year"
        },
        "scholarships": [
            {"name": "Beijing Government Scholarship", "coverage": "20,000 RMB", "deadline": "April"},
            {"name": "CAU Scholarship", "coverage": "50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 15"},
        "accepted_students": "130+",
        "image": "🌾"
    },
    {
        "id": 124,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Lanzhou University",
        "ranking": "#24 in China",
        "world_ranking": "481st",
        "location": "Lanzhou",
        "established": "1909",
        "students": "35,000+",
        "international": "6%",
        "description": "Leading university in Western China, strong in chemistry and ecology. Key research center for arid zone studies and grasslands.",
        "programs": {
            "undergraduate": ["Chemistry", "Physics", "Biology", "Geography", "Atmospheric Science"],
            "graduate": ["Organic Chemistry", "Ecology", "Arid Zone Research", "Nuclear Science"],
            "phd": ["PhD in Chemistry", "PhD in Ecology", "PhD in Physics"]
        },
        "fees": {
            "undergraduate": "16,000 - 29,000 RMB/year",
            "graduate": "20,000 - 33,000 RMB/year",
            "phd": "22,000 - 35,000 RMB/year"
        },
        "scholarships": [
            {"name": "Gansu Government Scholarship", "coverage": "15,000 RMB", "deadline": "May"},
            {"name": "LZU Scholarship", "coverage": "50% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "May 15", "spring": "December 15"},
        "accepted_students": "90+",
        "image": "🏜️"
    },
    {
        "id": 125,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Hunan University",
        "ranking": "#25 in China",
        "world_ranking": "511st",
        "location": "Changsha",
        "established": "976 AD (modern 1926)",
        "students": "38,000+",
        "international": "7%",
        "description": "Comprehensive university with roots in ancient Yuelu Academy. Strong in engineering and business with rich cultural heritage.",
        "programs": {
            "undergraduate": ["Mechanical Engineering", "Electrical Engineering", "Chemistry", "Business", "Economics"],
            "graduate": ["Industrial Engineering", "Power Engineering", "Analytical Chemistry", "MBA"],
            "phd": ["PhD in Engineering", "PhD in Chemistry", "PhD in Business"]
        },
        "fees": {
            "undergraduate": "17,000 - 31,000 RMB/year",
            "graduate": "21,000 - 35,000 RMB/year",
            "phd": "23,000 - 37,000 RMB/year"
        },
        "scholarships": [
            {"name": "Hunan Government Scholarship", "coverage": "20,000 RMB", "deadline": "April"},
            {"name": "HNU Scholarship", "coverage": "50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "April 15", "spring": "November 15"},
        "accepted_students": "140+",
        "image": "🏛️"
    },
    {
        "id": 126,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Chongqing University",
        "ranking": "#26 in China",
        "world_ranking": "541st",
        "location": "Chongqing",
        "established": "1929",
        "students": "45,000+",
        "international": "6%",
        "description": "Leading university in Southwest China, strong in engineering and architecture. Growing research center in mountainous city.",
        "programs": {
            "undergraduate": ["Civil Engineering", "Mechanical Engineering", "Electrical Engineering", "Architecture", "Urban Planning"],
            "graduate": ["Structural Engineering", "Vehicle Engineering", "Power Systems", "Urban Design"],
            "phd": ["PhD in Civil Engineering", "PhD in Mechanical Engineering", "PhD in Architecture"]
        },
        "fees": {
            "undergraduate": "17,000 - 32,000 RMB/year",
            "graduate": "21,000 - 36,000 RMB/year",
            "phd": "23,000 - 38,000 RMB/year"
        },
        "scholarships": [
            {"name": "Chongqing Government Scholarship", "coverage": "20,000 RMB", "deadline": "May"},
            {"name": "CQU Scholarship", "coverage": "50% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "May 15", "spring": "December 15"},
        "accepted_students": "120+",
        "image": "🏗️"
    },
    {
        "id": 127,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Jilin University",
        "ranking": "#27 in China",
        "world_ranking": "571st",
        "location": "Changchun",
        "established": "1946",
        "students": "70,000+",
        "international": "5%",
        "description": "One of China's largest universities, strong in chemistry, medicine, and automotive engineering. Key research center in Northeast China.",
        "programs": {
            "undergraduate": ["Chemistry", "Medicine", "Automotive Engineering", "Law", "Geology"],
            "graduate": ["Polymer Chemistry", "Clinical Medicine", "Vehicle Engineering", "Jurisprudence"],
            "phd": ["PhD in Chemistry", "PhD in Medicine", "PhD in Engineering"]
        },
        "fees": {
            "undergraduate": "16,000 - 30,000 RMB/year",
            "graduate": "20,000 - 34,000 RMB/year",
            "phd": "22,000 - 36,000 RMB/year"
        },
        "scholarships": [
            {"name": "Jilin Government Scholarship", "coverage": "15,000-25,000 RMB", "deadline": "May"},
            {"name": "JLU Scholarship", "coverage": "50% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "May 31", "spring": "December 31"},
        "accepted_students": "150+",
        "image": "🚗"
    },
    {
        "id": 128,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Ocean University of China",
        "ranking": "#28 in China",
        "world_ranking": "601st",
        "location": "Qingdao",
        "established": "1924",
        "students": "33,000+",
        "international": "7%",
        "description": "Leading university for marine sciences and fisheries in China. Coastal location provides unique research opportunities.",
        "programs": {
            "undergraduate": ["Marine Science", "Fisheries", "Oceanography", "Marine Engineering", "Environmental Science"],
            "graduate": ["Physical Oceanography", "Marine Biology", "Fisheries Science", "Marine Chemistry"],
            "phd": ["PhD in Marine Science", "PhD in Fisheries", "PhD in Oceanography"]
        },
        "fees": {
            "undergraduate": "16,000 - 30,000 RMB/year",
            "graduate": "20,000 - 34,000 RMB/year",
            "phd": "22,000 - 36,000 RMB/year"
        },
        "scholarships": [
            {"name": "Shandong Government Scholarship", "coverage": "20,000 RMB", "deadline": "April"},
            {"name": "OUC Scholarship", "coverage": "50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 15"},
        "accepted_students": "100+",
        "image": "🌊"
    },
    {
        "id": 129,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Northeastern University (China)",
        "ranking": "#29 in China",
        "world_ranking": "631st",
        "location": "Shenyang",
        "established": "1923",
        "students": "40,000+",
        "international": "6%",
        "description": "Key university in Northeast China, strong in engineering and computer science. Known for automation and software engineering.",
        "programs": {
            "undergraduate": ["Computer Science", "Software Engineering", "Mechanical Engineering", "Metallurgy", "Automation"],
            "graduate": ["AI", "Data Science", "Control Engineering", "Materials Processing"],
            "phd": ["PhD in Computer Science", "PhD in Engineering", "PhD in Materials"]
        },
        "fees": {
            "undergraduate": "16,000 - 30,000 RMB/year",
            "graduate": "20,000 - 34,000 RMB/year",
            "phd": "22,000 - 36,000 RMB/year"
        },
        "scholarships": [
            {"name": "Liaoning Government Scholarship", "coverage": "15,000-25,000 RMB", "deadline": "May"},
            {"name": "NEU Scholarship", "coverage": "50% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "May 15", "spring": "December 15"},
        "accepted_students": "110+",
        "image": "💻"
    },
    {
        "id": 130,
        "image_url": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?w=400",
        "name": "Soochow University",
        "ranking": "#30 in China",
        "world_ranking": "651st",
        "location": "Suzhou",
        "established": "1900",
        "students": "45,000+",
        "international": "9%",
        "description": "Comprehensive university in historic Suzhou, strong in medicine and materials science. Growing research output in nanotechnology.",
        "programs": {
            "undergraduate": ["Medicine", "Materials Science", "Textile Engineering", "Business", "Chinese Language"],
            "graduate": ["Clinical Medicine", "Materials Physics", "International Business", "Textile Chemistry"],
            "phd": ["PhD in Medicine", "PhD in Materials", "PhD in Chemistry"]
        },
        "fees": {
            "undergraduate": "17,000 - 32,000 RMB/year",
            "graduate": "21,000 - 36,000 RMB/year",
            "phd": "23,000 - 38,000 RMB/year"
        },
        "scholarships": [
            {"name": "Jiangsu Government Scholarship", "coverage": "20,000-30,000 RMB", "deadline": "April"},
            {"name": "SUDA Scholarship", "coverage": "50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 15"},
        "accepted_students": "180+",
        "image": "🏯"
    }
]

# Combine China universities
china_universities.extend(china_universities_extra)

# ==================== SINGAPORE - 30 UNIVERSITIES ====================
singapore_universities = [
    {
        "id": 201,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "National University of Singapore (NUS)",
        "ranking": "#1 in Singapore",
        "world_ranking": "8th",
        "location": "Singapore",
        "established": "1905",
        "students": "38,000+",
        "international": "30%",
        "description": "Asia's top university, consistently ranked among the world's best. Leading research university with strong industry connections.",
        "programs": {
            "undergraduate": ["Computer Science", "Engineering", "Business", "Law", "Medicine", "Architecture", "Economics"],
            "graduate": ["MBA", "Data Science", "Public Policy", "Engineering", "Finance", "Law", "Computer Science"],
            "phd": ["PhD in all fields", "Research Programs"]
        },
        "fees": {
            "undergraduate": "SGD 30,000 - 40,000/year ($22,000 - $30,000 USD)",
            "graduate": "SGD 35,000 - 50,000/year ($26,000 - $37,000 USD)",
            "phd": "SGD 20,000 - 30,000/year ($15,000 - $22,000 USD)"
        },
        "scholarships": [
            {"name": "NUS Global Merit Scholarship", "coverage": "Full tuition + living allowance", "deadline": "February"},
            {"name": "ASEAN Undergraduate Scholarship", "coverage": "Full tuition", "deadline": "March"},
            {"name": "Singapore Government Scholarship", "coverage": "Full package", "deadline": "January"},
            {"name": "NUS Research Scholarship", "coverage": "Full tuition + stipend", "deadline": "Rolling"}
        ],
        "deadlines": {"fall": "February 15", "spring": "August 31"},
        "accepted_students": "2,000+",
        "acceptance_rate": "10-15%",
        "image": "🇸🇬"
    },
    {
        "id": 202,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Nanyang Technological University (NTU)",
        "ranking": "#2 in Singapore",
        "world_ranking": "12th",
        "location": "Singapore",
        "established": "1991",
        "students": "33,000+",
        "international": "28%",
        "description": "Young and fast-growing university, famous for engineering and technology. Has the most beautiful campus in Singapore.",
        "programs": {
            "undergraduate": ["Engineering", "Computer Science", "Business", "Design", "Communication", "Science"],
            "graduate": ["MBA", "AI", "Engineering", "Finance", "Innovation", "Data Science"],
            "phd": ["PhD in Engineering", "PhD in Science", "PhD in Business"]
        },
        "fees": {
            "undergraduate": "SGD 28,000 - 38,000/year",
            "graduate": "SGD 32,000 - 45,000/year",
            "phd": "SGD 18,000 - 28,000/year"
        },
        "scholarships": [
            {"name": "NTU Scholarship", "coverage": "Full tuition", "deadline": "March"},
            {"name": "Singapore International Graduate Award", "coverage": "Full package", "deadline": "December"},
            {"name": "ASEAN Scholarship", "coverage": "Full tuition + allowance", "deadline": "February"}
        ],
        "deadlines": {"fall": "March 15", "spring": "September 30"},
        "accepted_students": "1,800+",
        "image": "🔬"
    },
    {
        "id": 203,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Singapore Management University (SMU)",
        "ranking": "#3 in Singapore",
        "world_ranking": "87th",
        "location": "Singapore",
        "established": "2000",
        "students": "10,000+",
        "international": "25%",
        "description": "Specializes in business and management education. Known for interactive teaching and strong industry network.",
        "programs": {
            "undergraduate": ["Business", "Accountancy", "Economics", "Law", "Information Systems", "Social Sciences"],
            "graduate": ["MBA", "Finance", "Economics", "Business Analytics", "Management"],
            "phd": ["PhD in Business", "PhD in Economics", "PhD in Law"]
        },
        "fees": {
            "undergraduate": "SGD 25,000 - 35,000/year",
            "graduate": "SGD 30,000 - 42,000/year",
            "phd": "SGD 20,000 - 28,000/year"
        },
        "scholarships": [
            {"name": "SMU Scholarship", "coverage": "Full tuition", "deadline": "March"},
            {"name": "ASEAN Scholarship", "coverage": "Full tuition + allowance", "deadline": "February"},
            {"name": "Li Ka Shing Scholarship", "coverage": "Full package", "deadline": "January"}
        ],
        "deadlines": {"fall": "March 31", "spring": "October 15"},
        "accepted_students": "500+",
        "image": "💼"
    },
    {
        "id": 204,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Singapore University of Technology and Design (SUTD)",
        "ranking": "#4 in Singapore",
        "world_ranking": "151-200",
        "location": "Singapore",
        "established": "2009",
        "students": "2,500+",
        "international": "20%",
        "description": "Specializes in technology and design education. Established in collaboration with MIT.",
        "programs": {
            "undergraduate": ["Engineering", "Architecture", "Design", "Information Systems", "AI"],
            "graduate": ["Innovation", "Architecture", "Engineering", "Design"],
            "phd": ["PhD in Engineering", "PhD in Design", "PhD in Architecture"]
        },
        "fees": {
            "undergraduate": "SGD 22,000 - 32,000/year",
            "graduate": "SGD 25,000 - 38,000/year",
            "phd": "SGD 18,000 - 25,000/year"
        },
        "scholarships": [
            {"name": "SUTD Scholarship", "coverage": "Full tuition", "deadline": "April"},
            {"name": "MIT-SUTD Scholarship", "coverage": "Full package", "deadline": "March"}
        ],
        "deadlines": {"fall": "April 30", "spring": "November 15"},
        "accepted_students": "200+",
        "image": "🔧"
    },
    {
        "id": 205,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Singapore Institute of Technology (SIT)",
        "ranking": "#5 in Singapore",
        "world_ranking": "201-250",
        "location": "Singapore",
        "established": "2009",
        "students": "7,000+",
        "international": "15%",
        "description": "Focuses on applied learning and industry partnerships. Strong emphasis on work-study programs.",
        "programs": {
            "undergraduate": ["Engineering", "Infocomm Technology", "Health Sciences", "Business", "Design"],
            "graduate": ["Engineering", "Technology", "Business", "Health Sciences"],
            "phd": ["PhD in Engineering", "PhD in Technology"]
        },
        "fees": {
            "undergraduate": "SGD 20,000 - 30,000/year",
            "graduate": "SGD 22,000 - 35,000/year",
            "phd": "SGD 16,000 - 22,000/year"
        },
        "scholarships": [
            {"name": "SIT Scholarship", "coverage": "Full tuition", "deadline": "May"},
            {"name": "Industry Sponsorship", "coverage": "Full package", "deadline": "Rolling"}
        ],
        "deadlines": {"fall": "May 15", "spring": "December 15"},
        "accepted_students": "300+",
        "image": "🔨"
    }
]

# ==================== SINGAPORE - ADDITIONAL 25 UNIVERSITIES (6-30) ====================
singapore_universities_extra = [
    {
        "id": 206,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Singapore University of Social Sciences (SUSS)",
        "ranking": "#6 in Singapore",
        "world_ranking": "601-650",
        "location": "Singapore",
        "established": "2005",
        "students": "15,000+",
        "international": "15%",
        "description": "Leading university for social sciences and part-time studies. Specializes in adult learning and professional development.",
        "programs": {
            "undergraduate": ["Social Work", "Psychology", "Business", "Law", "Communication"],
            "graduate": ["Social Work", "Counseling", "Applied Psychology", "MBA"],
            "phd": ["PhD in Social Sciences", "PhD in Psychology"]
        },
        "fees": {
            "undergraduate": "SGD 18,000 - 28,000/year",
            "graduate": "SGD 22,000 - 32,000/year",
            "phd": "SGD 16,000 - 24,000/year"
        },
        "scholarships": [
            {"name": "SUSS Scholarship", "coverage": "Partial tuition", "deadline": "May"},
            {"name": "SkillsFuture Scholarship", "coverage": "SGD 10,000", "deadline": "June"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "300+",
        "image": "📚"
    },
    {
        "id": 207,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "INSEAD Asia Campus",
        "ranking": "#7 in Singapore",
        "world_ranking": "#2 Business School",
        "location": "Singapore",
        "established": "2000",
        "students": "2,000+",
        "international": "90%",
        "description": "Top global business school with Asia campus in Singapore. Known for MBA and executive education programs.",
        "programs": {
            "undergraduate": ["MBA", "Executive MBA", "Finance", "Management"],
            "graduate": ["MBA", "Executive Education", "PhD in Management"],
            "phd": ["PhD in Business", "PhD in Economics"]
        },
        "fees": {
            "undergraduate": "SGD 80,000 - 100,000/year",
            "graduate": "SGD 85,000 - 110,000/year",
            "phd": "Full funding available"
        },
        "scholarships": [
            {"name": "INSEAD Scholarship", "coverage": "Partial tuition", "deadline": "January"},
            {"name": "Women's Scholarship", "coverage": "SGD 20,000", "deadline": "March"}
        ],
        "deadlines": {"fall": "January 15", "spring": "July 15"},
        "accepted_students": "150+",
        "image": "💼"
    },
    {
        "id": 208,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "ESSEC Business School Asia-Pacific",
        "ranking": "#8 in Singapore",
        "world_ranking": "#6 Business School",
        "location": "Singapore",
        "established": "2005",
        "students": "1,500+",
        "international": "85%",
        "description": "French business school with Asia-Pacific campus. Strong in luxury brand management and finance.",
        "programs": {
            "undergraduate": ["Global BBA", "Finance", "Marketing", "Management"],
            "graduate": ["MBA", "Master in Finance", "Luxury Brand Management"],
            "phd": ["PhD in Management"]
        },
        "fees": {
            "undergraduate": "SGD 25,000 - 35,000/year",
            "graduate": "SGD 30,000 - 45,000/year",
            "phd": "Full funding available"
        },
        "scholarships": [
            {"name": "ESSEC Scholarship", "coverage": "Partial tuition", "deadline": "February"},
            {"name": "Asia Scholarship", "coverage": "SGD 15,000", "deadline": "April"}
        ],
        "deadlines": {"fall": "February 28", "spring": "August 31"},
        "accepted_students": "120+",
        "image": "💎"
    },
    {
        "id": 209,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "SP Jain School of Global Management",
        "ranking": "#9 in Singapore",
        "world_ranking": "301-350",
        "location": "Singapore",
        "established": "2006",
        "students": "3,000+",
        "international": "80%",
        "description": "Global business school with campuses in Singapore, Dubai, Mumbai and Sydney. Known for global immersion programs.",
        "programs": {
            "undergraduate": ["Global Business", "Economics", "Marketing"],
            "graduate": ["Global MBA", "Executive MBA", "Business Analytics"],
            "phd": ["PhD in Business"]
        },
        "fees": {
            "undergraduate": "SGD 20,000 - 30,000/year",
            "graduate": "SGD 35,000 - 45,000/year",
            "phd": "SGD 25,000 - 35,000/year"
        },
        "scholarships": [
            {"name": "SP Jain Merit Scholarship", "coverage": "20-50% tuition", "deadline": "March"},
            {"name": "Global Leader Scholarship", "coverage": "SGD 10,000", "deadline": "April"}
        ],
        "deadlines": {"fall": "March 31", "spring": "September 30"},
        "accepted_students": "200+",
        "image": "🌏"
    },
    {
        "id": 210,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "James Cook University Singapore",
        "ranking": "#10 in Singapore",
        "world_ranking": "401-450",
        "location": "Singapore",
        "established": "2003",
        "students": "3,500+",
        "international": "70%",
        "description": "Australian university with full campus in Singapore. Strong in psychology, business and environmental science.",
        "programs": {
            "undergraduate": ["Psychology", "Business", "IT", "Environmental Science"],
            "graduate": ["Psychology", "MBA", "International Tourism"],
            "phd": ["PhD in Psychology", "PhD in Business"]
        },
        "fees": {
            "undergraduate": "SGD 22,000 - 32,000/year",
            "graduate": "SGD 28,000 - 38,000/year",
            "phd": "SGD 25,000 - 35,000/year"
        },
        "scholarships": [
            {"name": "JCU Merit Scholarship", "coverage": "10-25% tuition", "deadline": "May"},
            {"name": "International Student Grant", "coverage": "SGD 5,000", "deadline": "June"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "250+",
        "image": "🇦🇺"
    },
    {
        "id": 211,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Curtin Singapore",
        "ranking": "#11 in Singapore",
        "world_ranking": "451-500",
        "location": "Singapore",
        "established": "2008",
        "students": "4,000+",
        "international": "75%",
        "description": "Campus of Curtin University Australia. Strong in business, media and engineering.",
        "programs": {
            "undergraduate": ["Business", "Media", "IT", "Engineering"],
            "graduate": ["MBA", "International Business", "Supply Chain"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "SGD 20,000 - 28,000/year",
            "graduate": "SGD 25,000 - 35,000/year",
            "phd": "SGD 22,000 - 30,000/year"
        },
        "scholarships": [
            {"name": "Curtin Merit Scholarship", "coverage": "15-30% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "April 30", "spring": "October 31"},
        "accepted_students": "200+",
        "image": "🇦🇺"
    },
    {
        "id": 212,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Murdoch University Singapore",
        "ranking": "#12 in Singapore",
        "world_ranking": "501-550",
        "location": "Singapore",
        "established": "2008",
        "students": "3,000+",
        "international": "65%",
        "description": "Australian university campus in Singapore. Strong in communication, psychology and business.",
        "programs": {
            "undergraduate": ["Communication", "Psychology", "Business", "IT"],
            "graduate": ["MBA", "Communication", "Psychology"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "SGD 19,000 - 27,000/year",
            "graduate": "SGD 24,000 - 32,000/year",
            "phd": "SGD 22,000 - 28,000/year"
        },
        "scholarships": [
            {"name": "Murdoch International Scholarship", "coverage": "10-20% tuition", "deadline": "May"}
        ],
        "deadlines": {"fall": "May 15", "spring": "November 15"},
        "accepted_students": "150+",
        "image": "🇦🇺"
    },
    {
        "id": 213,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "University of Newcastle Singapore",
        "ranking": "#13 in Singapore",
        "world_ranking": "551-600",
        "location": "Singapore",
        "established": "2002",
        "students": "2,500+",
        "international": "70%",
        "description": "Australian university with programs in business, engineering and nursing.",
        "programs": {
            "undergraduate": ["Business", "Engineering", "Nursing", "IT"],
            "graduate": ["MBA", "Engineering Management", "Nursing"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "SGD 21,000 - 30,000/year",
            "graduate": "SGD 26,000 - 36,000/year",
            "phd": "SGD 23,000 - 32,000/year"
        },
        "scholarships": [
            {"name": "Newcastle Excellence Scholarship", "coverage": "15% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "April 15", "spring": "October 15"},
        "accepted_students": "120+",
        "image": "🇦🇺"
    },
    {
        "id": 214,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "University of Wollongong Singapore",
        "ranking": "#14 in Singapore",
        "world_ranking": "601-650",
        "location": "Singapore",
        "established": "2005",
        "students": "2,800+",
        "international": "68%",
        "description": "Australian university offering programs in business, IT and psychology.",
        "programs": {
            "undergraduate": ["Business", "IT", "Psychology"],
            "graduate": ["MBA", "IT Management", "Applied Finance"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "SGD 20,000 - 28,000/year",
            "graduate": "SGD 25,000 - 34,000/year",
            "phd": "SGD 22,000 - 30,000/year"
        },
        "scholarships": [
            {"name": "UOW Excellence Scholarship", "coverage": "15% tuition", "deadline": "May"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "130+",
        "image": "🇦🇺"
    },
    {
        "id": 215,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "RMIT University Singapore",
        "ranking": "#15 in Singapore",
        "world_ranking": "651-700",
        "location": "Singapore",
        "established": "2007",
        "students": "3,200+",
        "international": "72%",
        "description": "Australian university with strong programs in design, business and technology.",
        "programs": {
            "undergraduate": ["Design", "Business", "IT", "Communication"],
            "graduate": ["MBA", "Design Innovation", "Communication"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "SGD 21,000 - 29,000/year",
            "graduate": "SGD 26,000 - 35,000/year",
            "phd": "SGD 23,000 - 32,000/year"
        },
        "scholarships": [
            {"name": "RMIT International Scholarship", "coverage": "10-20% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "April 30", "spring": "October 31"},
        "accepted_students": "150+",
        "image": "🎨"
    },
    {
        "id": 216,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "LASALLE College of the Arts",
        "ranking": "#16 in Singapore",
        "world_ranking": "Top Arts College",
        "location": "Singapore",
        "established": "1984",
        "students": "2,700+",
        "international": "40%",
        "description": "Leading arts institution in Singapore. Strong in fine arts, design and performing arts.",
        "programs": {
            "undergraduate": ["Fine Arts", "Design", "Music", "Dance", "Theatre"],
            "graduate": ["Arts Management", "Fine Arts", "Design"],
            "phd": ["PhD in Arts"]
        },
        "fees": {
            "undergraduate": "SGD 22,000 - 30,000/year",
            "graduate": "SGD 26,000 - 34,000/year",
            "phd": "SGD 24,000 - 32,000/year"
        },
        "scholarships": [
            {"name": "LASALLE Scholarship", "coverage": "20-50% tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "March 31", "spring": "September 30"},
        "accepted_students": "180+",
        "image": "🎨"
    },
    {
        "id": 217,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Nanyang Academy of Fine Arts (NAFA)",
        "ranking": "#17 in Singapore",
        "world_ranking": "Top Arts College",
        "location": "Singapore",
        "established": "1938",
        "students": "2,500+",
        "international": "35%",
        "description": "Singapore's oldest arts institution. Strong in visual arts, music and dance.",
        "programs": {
            "undergraduate": ["Visual Arts", "Music", "Dance", "Theatre"],
            "graduate": ["Arts Education", "Music Performance"],
            "phd": ["PhD in Arts"]
        },
        "fees": {
            "undergraduate": "SGD 20,000 - 28,000/year",
            "graduate": "SGD 24,000 - 32,000/year",
            "phd": "SGD 22,000 - 30,000/year"
        },
        "scholarships": [
            {"name": "NAFA Scholarship", "coverage": "15-40% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "April 15", "spring": "October 15"},
        "accepted_students": "150+",
        "image": "🎵"
    },
    {
        "id": 218,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Duke-NUS Medical School",
        "ranking": "#18 in Singapore",
        "world_ranking": "Top Medical School",
        "location": "Singapore",
        "established": "2005",
        "students": "500+",
        "international": "25%",
        "description": "Partnership between Duke University and NUS. Leading medical education and research.",
        "programs": {
            "undergraduate": ["MD Program"],
            "graduate": ["PhD in Medicine", "Clinical Research"],
            "phd": ["PhD in Medical Sciences"]
        },
        "fees": {
            "undergraduate": "SGD 50,000 - 60,000/year",
            "graduate": "SGD 45,000 - 55,000/year",
            "phd": "Full funding available"
        },
        "scholarships": [
            {"name": "Duke-NUS Scholarship", "coverage": "Partial to full", "deadline": "January"}
        ],
        "deadlines": {"fall": "January 31"},
        "accepted_students": "50+",
        "image": "🏥"
    },
    {
        "id": 219,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Lee Kong Chian School of Medicine",
        "ranking": "#19 in Singapore",
        "world_ranking": "Top Medical School",
        "location": "Singapore",
        "established": "2010",
        "students": "600+",
        "international": "20%",
        "description": "Partnership between NTU and Imperial College London. Modern medical education.",
        "programs": {
            "undergraduate": ["MBBS"],
            "graduate": ["PhD in Medicine", "Biomedical Research"],
            "phd": ["PhD in Medical Sciences"]
        },
        "fees": {
            "undergraduate": "SGD 45,000 - 55,000/year",
            "graduate": "SGD 40,000 - 50,000/year",
            "phd": "Full funding available"
        },
        "scholarships": [
            {"name": "LKCMedicine Scholarship", "coverage": "Partial to full", "deadline": "February"}
        ],
        "deadlines": {"fall": "February 28"},
        "accepted_students": "60+",
        "image": "🏥"
    },
    {
        "id": 220,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Singapore Institute of Management (SIM)",
        "ranking": "#20 in Singapore",
        "world_ranking": "Top Private",
        "location": "Singapore",
        "established": "1964",
        "students": "20,000+",
        "international": "30%",
        "description": "Leading private education institution with partnerships with global universities.",
        "programs": {
            "undergraduate": ["Business", "IT", "Communication"],
            "graduate": ["MBA", "Management"],
            "phd": ["DBA"]
        },
        "fees": {
            "undergraduate": "SGD 15,000 - 25,000/year",
            "graduate": "SGD 20,000 - 30,000/year",
            "phd": "SGD 25,000 - 35,000/year"
        },
        "scholarships": [
            {"name": "SIM Scholarship", "coverage": "10-30% tuition", "deadline": "May"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "500+",
        "image": "📊"
    },
    {
        "id": 221,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Kaplan Singapore",
        "ranking": "#21 in Singapore",
        "world_ranking": "Top Private",
        "location": "Singapore",
        "established": "1989",
        "students": "15,000+",
        "international": "40%",
        "description": "Global education provider with university partnerships from UK, Australia and Ireland.",
        "programs": {
            "undergraduate": ["Business", "Accounting", "IT", "Hospitality"],
            "graduate": ["MBA", "Finance"],
            "phd": ["DBA"]
        },
        "fees": {
            "undergraduate": "SGD 14,000 - 22,000/year",
            "graduate": "SGD 18,000 - 28,000/year",
            "phd": "SGD 22,000 - 30,000/year"
        },
        "scholarships": [
            {"name": "Kaplan Merit Scholarship", "coverage": "10-20% tuition", "deadline": "June"}
        ],
        "deadlines": {"fall": "June 30", "spring": "December 31"},
        "accepted_students": "400+",
        "image": "📚"
    },
    {
        "id": 222,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "PSB Academy",
        "ranking": "#22 in Singapore",
        "world_ranking": "Top Private",
        "location": "Singapore",
        "established": "1964",
        "students": "12,000+",
        "international": "50%",
        "description": "Leading private education institution with partners from Australia, UK and NZ.",
        "programs": {
            "undergraduate": ["Engineering", "Business", "IT", "Science"],
            "graduate": ["MBA", "Engineering Management"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "SGD 15,000 - 24,000/year",
            "graduate": "SGD 20,000 - 30,000/year",
            "phd": "SGD 24,000 - 32,000/year"
        },
        "scholarships": [
            {"name": "PSB Scholarship", "coverage": "10-25% tuition", "deadline": "May"}
        ],
        "deadlines": {"fall": "May 15", "spring": "November 15"},
        "accepted_students": "350+",
        "image": "🔬"
    },
    {
        "id": 223,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Management Development Institute of Singapore (MDIS)",
        "ranking": "#23 in Singapore",
        "world_ranking": "Top Private",
        "location": "Singapore",
        "established": "1956",
        "students": "13,000+",
        "international": "45%",
        "description": "One of Singapore's oldest non-profit professional institutes.",
        "programs": {
            "undergraduate": ["Business", "Engineering", "Nursing", "Media"],
            "graduate": ["MBA", "Hospitality"],
            "phd": ["DBA"]
        },
        "fees": {
            "undergraduate": "SGD 14,000 - 23,000/year",
            "graduate": "SGD 19,000 - 28,000/year",
            "phd": "SGD 23,000 - 32,000/year"
        },
        "scholarships": [
            {"name": "MDIS Merit Scholarship", "coverage": "10-30% tuition", "deadline": "June"}
        ],
        "deadlines": {"fall": "June 15", "spring": "December 15"},
        "accepted_students": "300+",
        "image": "📊"
    },
    {
        "id": 224,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "TMC Academy",
        "ranking": "#24 in Singapore",
        "world_ranking": "Private",
        "location": "Singapore",
        "established": "1981",
        "students": "3,000+",
        "international": "60%",
        "description": "Private education provider with university partners from UK and Australia.",
        "programs": {
            "undergraduate": ["Business", "IT", "Psychology"],
            "graduate": ["MBA"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "SGD 13,000 - 20,000/year",
            "graduate": "SGD 18,000 - 25,000/year",
            "phd": "SGD 20,000 - 28,000/year"
        },
        "scholarships": [
            {"name": "TMC Scholarship", "coverage": "10-20% tuition", "deadline": "July"}
        ],
        "deadlines": {"fall": "July 31", "spring": "January 31"},
        "accepted_students": "150+",
        "image": "🎓"
    },
    {
        "id": 225,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Amity Global Institute",
        "ranking": "#25 in Singapore",
        "world_ranking": "Private",
        "location": "Singapore",
        "established": "2006",
        "students": "5,000+",
        "international": "70%",
        "description": "Part of Amity Education Group with programs in business, IT and hospitality.",
        "programs": {
            "undergraduate": ["Business", "IT", "Hospitality"],
            "graduate": ["MBA", "International Business"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "SGD 12,000 - 19,000/year",
            "graduate": "SGD 16,000 - 24,000/year",
            "phd": "SGD 20,000 - 26,000/year"
        },
        "scholarships": [
            {"name": "Amity Merit Scholarship", "coverage": "10-25% tuition", "deadline": "June"}
        ],
        "deadlines": {"fall": "June 30", "spring": "December 31"},
        "accepted_students": "200+",
        "image": "🇮🇳"
    },
    {
        "id": 226,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "East Asia Institute of Management (EASB)",
        "ranking": "#26 in Singapore",
        "world_ranking": "Private",
        "location": "Singapore",
        "established": "1984",
        "students": "4,000+",
        "international": "55%",
        "description": "Private education institute with programs in business, hospitality and nursing.",
        "programs": {
            "undergraduate": ["Business", "Hospitality", "Nursing"],
            "graduate": ["MBA", "Hospitality Management"],
            "phd": ["DBA"]
        },
        "fees": {
            "undergraduate": "SGD 13,000 - 21,000/year",
            "graduate": "SGD 17,000 - 26,000/year",
            "phd": "SGD 22,000 - 30,000/year"
        },
        "scholarships": [
            {"name": "EASB Scholarship", "coverage": "10-20% tuition", "deadline": "May"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "150+",
        "image": "🏨"
    },
    {
        "id": 227,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Raffles College of Higher Education",
        "ranking": "#27 in Singapore",
        "world_ranking": "Private",
        "location": "Singapore",
        "established": "1990",
        "students": "3,500+",
        "international": "65%",
        "description": "Leading design and business school with network across Asia.",
        "programs": {
            "undergraduate": ["Design", "Business", "Psychology"],
            "graduate": ["Design Management", "MBA"],
            "phd": ["PhD in Design"]
        },
        "fees": {
            "undergraduate": "SGD 18,000 - 26,000/year",
            "graduate": "SGD 22,000 - 30,000/year",
            "phd": "SGD 24,000 - 32,000/year"
        },
        "scholarships": [
            {"name": "Raffles Merit Scholarship", "coverage": "15-30% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "April 30", "spring": "October 31"},
        "accepted_students": "180+",
        "image": "🎨"
    },
    {
        "id": 228,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Shelton College International",
        "ranking": "#28 in Singapore",
        "world_ranking": "Private",
        "location": "Singapore",
        "established": "1985",
        "students": "2,500+",
        "international": "50%",
        "description": "Private education provider with programs in business and hospitality.",
        "programs": {
            "undergraduate": ["Business", "Hospitality"],
            "graduate": ["MBA"],
            "phd": ["DBA"]
        },
        "fees": {
            "undergraduate": "SGD 12,000 - 18,000/year",
            "graduate": "SGD 16,000 - 22,000/year",
            "phd": "SGD 20,000 - 26,000/year"
        },
        "scholarships": [
            {"name": "Shelton Scholarship", "coverage": "10-15% tuition", "deadline": "July"}
        ],
        "deadlines": {"fall": "July 31", "spring": "January 31"},
        "accepted_students": "100+",
        "image": "🎓"
    },
    {
        "id": 229,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Beacon International College",
        "ranking": "#29 in Singapore",
        "world_ranking": "Private",
        "location": "Singapore",
        "established": "2004",
        "students": "2,000+",
        "international": "60%",
        "description": "Private education college specializing in business and accounting.",
        "programs": {
            "undergraduate": ["Business", "Accounting"],
            "graduate": ["MBA", "Finance"],
            "phd": ["DBA"]
        },
        "fees": {
            "undergraduate": "SGD 11,000 - 17,000/year",
            "graduate": "SGD 15,000 - 21,000/year",
            "phd": "SGD 18,000 - 24,000/year"
        },
        "scholarships": [
            {"name": "Beacon Excellence Scholarship", "coverage": "10-20% tuition", "deadline": "June"}
        ],
        "deadlines": {"fall": "June 30", "spring": "December 31"},
        "accepted_students": "80+",
        "image": "💰"
    },
    {
        "id": 230,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400",
        "name": "Dimensions International College",
        "ranking": "#30 in Singapore",
        "world_ranking": "Private",
        "location": "Singapore",
        "established": "1980",
        "students": "3,000+",
        "international": "55%",
        "description": "Private education college with programs in business, hospitality and teacher training.",
        "programs": {
            "undergraduate": ["Business", "Hospitality", "Education"],
            "graduate": ["MBA", "Education"],
            "phd": ["PhD in Education"]
        },
        "fees": {
            "undergraduate": "SGD 12,000 - 19,000/year",
            "graduate": "SGD 16,000 - 24,000/year",
            "phd": "SGD 20,000 - 28,000/year"
        },
        "scholarships": [
            {"name": "Dimensions Scholarship", "coverage": "10-20% tuition", "deadline": "May"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "120+",
        "image": "🎓"
    }
]

# Combine Singapore universities
singapore_universities.extend(singapore_universities_extra)

# ==================== MALAYSIA - 30 UNIVERSITIES ====================
# ==================== MALAYSIA - 30 UNIVERSITIES ====================
malaysia_universities = [
    # ======== UNIVERSITY 1 ========
    {
        "id": 301,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "University of Malaya (UM)",
        "ranking": "#1 in Malaysia",
        "world_ranking": "65th",
        "location": "Kuala Lumpur",
        "established": "1905",
        "students": "30,000+",
        "international": "18%",
        "description": "Malaysia's oldest and most prestigious university. Leading research institution in Southeast Asia with strong programs in medicine, engineering, and law.",
        "programs": {
            "undergraduate": ["Medicine", "Engineering", "Business", "Law", "Computer Science", "Economics", "Pharmacy", "Dentistry"],
            "graduate": ["MBA", "Data Science", "Engineering", "Public Health", "Education", "Law", "Computer Science"],
            "phd": ["PhD in Medicine", "PhD in Engineering", "PhD in Law", "PhD in Business", "PhD in Computer Science"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma (85%+)", "IELTS 6.0", "TOEFL 550", "Foundation/STPM/A-Levels", "Personal Statement"],
            "graduate": ["Bachelor's Degree (3.0/4.0 GPA)", "IELTS 6.5", "TOEFL 580", "Work Experience", "Research Proposal"],
            "phd": ["Master's Degree", "IELTS 7.0", "Research Publications", "Interview", "Detailed Research Plan"]
        },
        "fees": {
            "undergraduate": "RM 15,000 - 25,000/year ($3,200 - $5,300 USD)",
            "graduate": "RM 18,000 - 30,000/year ($3,800 - $6,400 USD)",
            "phd": "RM 20,000 - 35,000/year ($4,300 - $7,500 USD)"
        },
        "scholarships": [
            {"name": "UM Excellence Scholarship", "coverage": "100% tuition + stipend", "deadline": "April"},
            {"name": "Malaysian Government Scholarship", "coverage": "Full package", "deadline": "March"},
            {"name": "ASEAN Scholarship", "coverage": "50% tuition", "deadline": "May"},
            {"name": "UM International Student Award", "coverage": "RM 10,000/year", "deadline": "April"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "500+",
        "acceptance_rate": "15-20%",
        "language": "English/Malay",
        "website": "www.um.edu.my",
        "image": "🇲🇾"
    },
    
    # ======== UNIVERSITY 2 ========
    {
        "id": 302,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Putra Malaysia (UPM)",
        "ranking": "#2 in Malaysia",
        "world_ranking": "123rd",
        "location": "Serdang, Selangor",
        "established": "1931",
        "students": "28,000+",
        "international": "15%",
        "description": "Leading research university strong in agriculture, forestry, and veterinary medicine. Known for its beautiful 1,200-hectare campus.",
        "programs": {
            "undergraduate": ["Agriculture", "Veterinary Medicine", "Forestry", "Engineering", "Medicine", "Business", "Food Science", "Biotechnology"],
            "graduate": ["Agricultural Science", "MBA", "Food Technology", "Environmental Science", "Veterinary Science"],
            "phd": ["PhD in Agriculture", "PhD in Veterinary Medicine", "PhD in Food Science", "PhD in Environmental Science"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 6.0", "TOEFL 550", "Foundation/STPM"],
            "graduate": ["Bachelor's Degree", "IELTS 6.5", "Research Proposal"],
            "phd": ["Master's Degree", "IELTS 7.0", "Research Publications"]
        },
        "fees": {
            "undergraduate": "RM 14,000 - 24,000/year ($3,000 - $5,100 USD)",
            "graduate": "RM 16,000 - 28,000/year ($3,400 - $6,000 USD)",
            "phd": "RM 18,000 - 30,000/year ($3,800 - $6,400 USD)"
        },
        "scholarships": [
            {"name": "UPM Graduate Scholarship", "coverage": "50-100% tuition", "deadline": "April"},
            {"name": "Agricultural Research Grant", "coverage": "RM 15,000/year", "deadline": "May"}
        ],
        "deadlines": {"fall": "June 15", "spring": "December 15"},
        "accepted_students": "400+",
        "acceptance_rate": "20-25%",
        "language": "English",
        "website": "www.upm.edu.my",
        "image": "🌾"
    },
    
    # ======== UNIVERSITY 3 ========
    {
        "id": 303,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Kebangsaan Malaysia (UKM)",
        "ranking": "#3 in Malaysia",
        "world_ranking": "141st",
        "location": "Bangi, Selangor",
        "established": "1970",
        "students": "25,000+",
        "international": "12%",
        "description": "National University of Malaysia, strong in medicine, pharmacy, and humanities. Known for its Islamic studies and Malay cultural research.",
        "programs": {
            "undergraduate": ["Medicine", "Pharmacy", "Law", "Economics", "Engineering", "Islamic Studies", "Dentistry", "Health Sciences"],
            "graduate": ["MBA", "Public Health", "Education", "Shariah Law", "Clinical Medicine"],
            "phd": ["PhD in Medicine", "PhD in Law", "PhD in Islamic Studies", "PhD in Pharmacy"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 6.0", "Foundation/STPM", "Interview for Medicine"],
            "graduate": ["Bachelor's Degree", "IELTS 6.5", "Work Experience"],
            "phd": ["Master's Degree", "IELTS 7.0", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 14,000 - 23,000/year ($3,000 - $4,900 USD)",
            "graduate": "RM 16,000 - 26,000/year ($3,400 - $5,500 USD)",
            "phd": "RM 18,000 - 28,000/year ($3,800 - $6,000 USD)"
        },
        "scholarships": [
            {"name": "UKM Excellence Scholarship", "coverage": "50% tuition", "deadline": "May"},
            {"name": "National University Fellowship", "coverage": "RM 12,000/year", "deadline": "April"}
        ],
        "deadlines": {"fall": "June 30", "spring": "December 31"},
        "accepted_students": "350+",
        "acceptance_rate": "18-22%",
        "language": "English/Malay",
        "website": "www.ukm.edu.my",
        "image": "🏥"
    },
    
    # ======== UNIVERSITY 4 ========
    {
        "id": 304,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Sains Malaysia (USM)",
        "ranking": "#4 in Malaysia",
        "world_ranking": "142nd",
        "location": "Penang",
        "established": "1969",
        "students": "24,000+",
        "international": "14%",
        "description": "APEX university status, strong in pure sciences and engineering. Located on the beautiful island of Penang.",
        "programs": {
            "undergraduate": ["Pharmacy", "Engineering", "Pure Sciences", "Computer Science", "Architecture", "Communication", "Social Sciences"],
            "graduate": ["MBA", "Data Science", "Pharmaceutical Sciences", "Engineering Management"],
            "phd": ["PhD in Science", "PhD in Pharmacy", "PhD in Engineering", "PhD in Social Sciences"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 6.0", "Foundation/STPM", "Portfolio for Architecture"],
            "graduate": ["Bachelor's Degree", "IELTS 6.5", "GRE for Engineering"],
            "phd": ["Master's Degree", "IELTS 7.0", "Research Publications"]
        },
        "fees": {
            "undergraduate": "RM 13,000 - 22,000/year ($2,800 - $4,700 USD)",
            "graduate": "RM 15,000 - 25,000/year ($3,200 - $5,300 USD)",
            "phd": "RM 17,000 - 27,000/year ($3,600 - $5,700 USD)"
        },
        "scholarships": [
            {"name": "USM Fellowship", "coverage": "Full tuition + stipend", "deadline": "March"},
            {"name": "APEX Scholarship", "coverage": "50% tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "400+",
        "acceptance_rate": "20-25%",
        "language": "English",
        "website": "www.usm.my",
        "image": "🔬"
    },
    
    # ======== UNIVERSITY 5 ========
    {
        "id": 305,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Teknologi Malaysia (UTM)",
        "ranking": "#5 in Malaysia",
        "world_ranking": "187th",
        "location": "Johor Bahru",
        "established": "1904",
        "students": "25,000+",
        "international": "13%",
        "description": "Leading engineering and technology university. Strong in civil engineering, chemical engineering, and architecture.",
        "programs": {
            "undergraduate": ["Civil Engineering", "Mechanical Engineering", "Electrical Engineering", "Chemical Engineering", "Architecture", "Computer Science", "Geoinformatics"],
            "graduate": ["Engineering Management", "Structural Engineering", "MBA", "Environmental Engineering"],
            "phd": ["PhD in Engineering", "PhD in Architecture", "PhD in Computer Science"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 6.0", "Foundation/STPM", "Mathematics Background"],
            "graduate": ["Bachelor's Degree in Engineering", "IELTS 6.5", "GRE Optional"],
            "phd": ["Master's Degree", "IELTS 7.0", "Research Papers"]
        },
        "fees": {
            "undergraduate": "RM 14,000 - 24,000/year ($3,000 - $5,100 USD)",
            "graduate": "RM 16,000 - 28,000/year ($3,400 - $6,000 USD)",
            "phd": "RM 18,000 - 30,000/year ($3,800 - $6,400 USD)"
        },
        "scholarships": [
            {"name": "UTM Engineering Scholarship", "coverage": "50-100% tuition", "deadline": "April"},
            {"name": "CSC Scholarship", "coverage": "Full package", "deadline": "February"}
        ],
        "deadlines": {"fall": "June 15", "spring": "December 15"},
        "accepted_students": "350+",
        "acceptance_rate": "22-28%",
        "language": "English",
        "website": "www.utm.my",
        "image": "⚙️"
    },
    
    # ======== UNIVERSITY 6 ========
    {
        "id": 306,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Teknologi MARA (UiTM)",
        "ranking": "#6 in Malaysia",
        "world_ranking": "651-700",
        "location": "Shah Alam",
        "established": "1956",
        "students": "150,000+",
        "international": "5%",
        "description": "Largest university in Malaysia with multiple campuses nationwide. Strong in business, hotel management, and creative arts.",
        "programs": {
            "undergraduate": ["Business", "Hotel Management", "Creative Arts", "Law", "Pharmacy", "Engineering", "Information Technology"],
            "graduate": ["MBA", "Hotel Management", "Creative Arts", "Education", "Applied Sciences"],
            "phd": ["PhD in various fields", "DBA", "PhD in Creative Arts"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 5.5", "Foundation/STPM", "Portfolio for Arts"],
            "graduate": ["Bachelor's Degree", "IELTS 6.0", "Work Experience"],
            "phd": ["Master's Degree", "IELTS 6.5", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 10,000 - 18,000/year ($2,100 - $3,800 USD)",
            "graduate": "RM 15,000 - 25,000/year ($3,200 - $5,300 USD)",
            "phd": "RM 18,000 - 28,000/year ($3,800 - $6,000 USD)"
        },
        "scholarships": [
            {"name": "UiTM Excellence Scholarship", "coverage": "50% tuition", "deadline": "May"},
            {"name": "MARA Scholarship", "coverage": "Full tuition", "deadline": "April"}
        ],
        "deadlines": {"fall": "June 30", "spring": "December 31"},
        "accepted_students": "400+",
        "acceptance_rate": "30-35%",
        "language": "English",
        "website": "www.uitm.edu.my",
        "image": "🎨"
    },
    
    # ======== UNIVERSITY 7 ========
    {
        "id": 307,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Utara Malaysia (UUM)",
        "ranking": "#7 in Malaysia",
        "world_ranking": "551-600",
        "location": "Sintok, Kedah",
        "established": "1984",
        "students": "30,000+",
        "international": "10%",
        "description": "Specializes in management, business, and accounting. Known as the 'Management University' of Malaysia.",
        "programs": {
            "undergraduate": ["Business Administration", "Accounting", "Economics", "Banking", "Information Technology", "Public Management"],
            "graduate": ["MBA", "Master in Accounting", "Master in Finance", "PhD in Management"],
            "phd": ["PhD in Business", "PhD in Economics", "PhD in Accounting", "DBA"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 5.5", "Foundation/STPM"],
            "graduate": ["Bachelor's Degree", "IELTS 6.0", "GMAT Optional"],
            "phd": ["Master's Degree", "IELTS 6.5", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 9,000 - 15,000/year ($1,900 - $3,200 USD)",
            "graduate": "RM 12,000 - 22,000/year ($2,500 - $4,700 USD)",
            "phd": "RM 15,000 - 25,000/year ($3,200 - $5,300 USD)"
        },
        "scholarships": [
            {"name": "UUM Vice-Chancellor Scholarship", "coverage": "50% tuition", "deadline": "May"},
            {"name": "ASEAN Scholarship", "coverage": "30% tuition", "deadline": "June"}
        ],
        "deadlines": {"fall": "July 15", "spring": "January 15"},
        "accepted_students": "300+",
        "acceptance_rate": "35-40%",
        "language": "English",
        "website": "www.uum.edu.my",
        "image": "💼"
    },
    
    # ======== UNIVERSITY 8 ========
    {
        "id": 308,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Malaysia Sabah (UMS)",
        "ranking": "#8 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Kota Kinabalu, Sabah",
        "established": "1994",
        "students": "20,000+",
        "international": "8%",
        "description": "Leading university in East Malaysia, strong in tropical biology, marine science, and tourism studies.",
        "programs": {
            "undergraduate": ["Marine Science", "Tropical Biology", "Tourism Management", "Engineering", "Business", "Food Science"],
            "graduate": ["Marine Biology", "Tropical Forestry", "Tourism", "Environmental Science"],
            "phd": ["PhD in Marine Science", "PhD in Tropical Biology", "PhD in Tourism"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 5.5", "Foundation/STPM"],
            "graduate": ["Bachelor's Degree", "IELTS 6.0"],
            "phd": ["Master's Degree", "IELTS 6.5", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 9,000 - 16,000/year ($1,900 - $3,400 USD)",
            "graduate": "RM 12,000 - 20,000/year ($2,500 - $4,300 USD)",
            "phd": "RM 15,000 - 23,000/year ($3,200 - $4,900 USD)"
        },
        "scholarships": [
            {"name": "UMS Excellence Scholarship", "coverage": "30-50% tuition", "deadline": "June"},
            {"name": "Sabah Foundation Scholarship", "coverage": "Partial tuition", "deadline": "May"}
        ],
        "deadlines": {"fall": "July 31", "spring": "January 31"},
        "accepted_students": "200+",
        "acceptance_rate": "30-35%",
        "language": "English",
        "website": "www.ums.edu.my",
        "image": "🌊"
    },
    
    # ======== UNIVERSITY 9 ========
    {
        "id": 309,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Malaysia Sarawak (UNIMAS)",
        "ranking": "#9 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Kota Samarahan, Sarawak",
        "established": "1992",
        "students": "18,000+",
        "international": "7%",
        "description": "Leading university in Borneo, strong in biodiversity, conservation, and indigenous studies.",
        "programs": {
            "undergraduate": ["Biodiversity", "Conservation", "Engineering", "Medicine", "IT", "Social Sciences", "Design"],
            "graduate": ["Environmental Science", "Biodiversity", "Public Health", "MBA"],
            "phd": ["PhD in Biodiversity", "PhD in Environmental Science", "PhD in Conservation"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 5.5", "Foundation/STPM"],
            "graduate": ["Bachelor's Degree", "IELTS 6.0"],
            "phd": ["Master's Degree", "IELTS 6.5", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 9,000 - 17,000/year ($1,900 - $3,600 USD)",
            "graduate": "RM 12,000 - 21,000/year ($2,500 - $4,500 USD)",
            "phd": "RM 15,000 - 24,000/year ($3,200 - $5,100 USD)"
        },
        "scholarships": [
            {"name": "UNIMAS Chancellor Scholarship", "coverage": "50% tuition", "deadline": "June"},
            {"name": "Sarawak Foundation Scholarship", "coverage": "Partial tuition", "deadline": "May"}
        ],
        "deadlines": {"fall": "July 31", "spring": "January 31"},
        "accepted_students": "180+",
        "acceptance_rate": "32-38%",
        "language": "English",
        "website": "www.unimas.my",
        "image": "🌴"
    },
    
    # ======== UNIVERSITY 10 ========
    {
        "id": 310,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "International Islamic University Malaysia (IIUM)",
        "ranking": "#10 in Malaysia",
        "world_ranking": "601-650",
        "location": "Gombak, Selangor",
        "established": "1983",
        "students": "25,000+",
        "international": "20%",
        "description": "Leading Islamic university with strong programs in law, economics, and Islamic studies. Attracts students from all over the world.",
        "programs": {
            "undergraduate": ["Islamic Law", "Economics", "Engineering", "Architecture", "Medicine", "Psychology", "Education"],
            "graduate": ["MBA", "Islamic Banking", "Comparative Law", "Education", "Engineering"],
            "phd": ["PhD in Islamic Studies", "PhD in Law", "PhD in Economics", "PhD in Education"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 6.0", "Foundation/STPM", "Quran Knowledge"],
            "graduate": ["Bachelor's Degree", "IELTS 6.5", "Research Proposal"],
            "phd": ["Master's Degree", "IELTS 7.0", "Research Publications"]
        },
        "fees": {
            "undergraduate": "RM 12,000 - 22,000/year ($2,500 - $4,700 USD)",
            "graduate": "RM 15,000 - 26,000/year ($3,200 - $5,500 USD)",
            "phd": "RM 18,000 - 28,000/year ($3,800 - $6,000 USD)"
        },
        "scholarships": [
            {"name": "IIUM Merit Scholarship", "coverage": "50-100% tuition", "deadline": "April"},
            {"name": "OIC Scholarship", "coverage": "Full package", "deadline": "March"},
            {"name": "Islamic Development Bank Scholarship", "coverage": "Full tuition + living", "deadline": "February"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "400+",
        "acceptance_rate": "25-30%",
        "language": "English/Arabic",
        "website": "www.iium.edu.my",
        "image": "🕌"
    },
    
    # ======== UNIVERSITY 11 ========
    {
        "id": 311,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Multimedia University (MMU)",
        "ranking": "#11 in Malaysia",
        "world_ranking": "701-750",
        "location": "Cyberjaya",
        "established": "1996",
        "students": "15,000+",
        "international": "15%",
        "description": "First private university in Malaysia, strong in IT, multimedia, and engineering. Located in Malaysia's Silicon Valley.",
        "programs": {
            "undergraduate": ["Computer Science", "Software Engineering", "Multimedia", "Animation", "Engineering", "Business", "Law"],
            "graduate": ["MBA", "Data Science", "Cyber Security", "Multimedia", "Engineering"],
            "phd": ["PhD in Computer Science", "PhD in Engineering", "PhD in Creative Multimedia"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 5.5", "Foundation/STPM", "Portfolio for Multimedia"],
            "graduate": ["Bachelor's Degree", "IELTS 6.0", "Work Experience"],
            "phd": ["Master's Degree", "IELTS 6.5", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 18,000 - 28,000/year ($3,800 - $6,000 USD)",
            "graduate": "RM 20,000 - 32,000/year ($4,300 - $6,800 USD)",
            "phd": "RM 22,000 - 35,000/year ($4,700 - $7,500 USD)"
        },
        "scholarships": [
            {"name": "MMU Excellence Scholarship", "coverage": "25-50% tuition", "deadline": "May"},
            {"name": "Cyberjaya Innovation Grant", "coverage": "RM 10,000", "deadline": "June"}
        ],
        "deadlines": {"fall": "June 30", "spring": "December 31"},
        "accepted_students": "300+",
        "acceptance_rate": "35-40%",
        "language": "English",
        "website": "www.mmu.edu.my",
        "image": "💻"
    },
    
    # ======== UNIVERSITY 12 ========
    {
        "id": 312,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Taylor's University",
        "ranking": "#12 in Malaysia",
        "world_ranking": "284th",
        "location": "Subang Jaya",
        "established": "1969",
        "students": "12,000+",
        "international": "25%",
        "description": "Top private university in Malaysia, famous for hospitality, business, and medicine. Modern campus with state-of-the-art facilities.",
        "programs": {
            "undergraduate": ["Hospitality Management", "Business", "Medicine", "Pharmacy", "Engineering", "Law", "Design", "Psychology"],
            "graduate": ["MBA", "Hospitality Management", "PhD in Business", "Master in Finance"],
            "phd": ["PhD in Hospitality", "PhD in Business", "PhD in Social Sciences"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 6.0", "Foundation/A-Levels", "Interview"],
            "graduate": ["Bachelor's Degree", "IELTS 6.5", "Work Experience", "GMAT Optional"],
            "phd": ["Master's Degree", "IELTS 7.0", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 35,000 - 45,000/year ($7,500 - $9,600 USD)",
            "graduate": "RM 38,000 - 50,000/year ($8,100 - $10,700 USD)",
            "phd": "RM 40,000 - 55,000/year ($8,500 - $11,700 USD)"
        },
        "scholarships": [
            {"name": "Taylor's Excellence Award", "coverage": "25-100% tuition", "deadline": "April"},
            {"name": "ASEAN Scholarship", "coverage": "50% tuition", "deadline": "March"},
            {"name": "Taylor's Merit Scholarship", "coverage": "RM 20,000", "deadline": "May"}
        ],
        "deadlines": {"fall": "May 31", "spring": "November 30"},
        "accepted_students": "500+",
        "acceptance_rate": "30-35%",
        "language": "English",
        "website": "www.taylors.edu.my",
        "image": "🏨"
    },
    
    # ======== UNIVERSITY 13 ========
    {
        "id": 313,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Sunway University",
        "ranking": "#13 in Malaysia",
        "world_ranking": "601-650",
        "location": "Bandar Sunway",
        "established": "1987",
        "students": "10,000+",
        "international": "20%",
        "description": "Leading private university with strong links to Lancaster University (UK). Excellent programs in business, medicine, and creative arts.",
        "programs": {
            "undergraduate": ["Business", "Medicine", "Psychology", "Creative Arts", "Computer Science", "Engineering", "Communication"],
            "graduate": ["MBA", "Master in Psychology", "Data Science", "Creative Arts"],
            "phd": ["PhD in Business", "PhD in Psychology", "PhD in Computer Science"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 6.0", "Foundation/A-Levels"],
            "graduate": ["Bachelor's Degree", "IELTS 6.5", "Work Experience"],
            "phd": ["Master's Degree", "IELTS 7.0", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 30,000 - 40,000/year ($6,400 - $8,500 USD)",
            "graduate": "RM 35,000 - 45,000/year ($7,500 - $9,600 USD)",
            "phd": "RM 38,000 - 48,000/year ($8,100 - $10,200 USD)"
        },
        "scholarships": [
            {"name": "Sunway Excellence Scholarship", "coverage": "25-75% tuition", "deadline": "April"},
            {"name": "Jeffrey Cheah Foundation Award", "coverage": "50% tuition", "deadline": "May"}
        ],
        "deadlines": {"fall": "June 15", "spring": "December 15"},
        "accepted_students": "350+",
        "acceptance_rate": "32-38%",
        "language": "English",
        "website": "www.sunway.edu.my",
        "image": "☀️"
    },
    
    # ======== UNIVERSITY 14 ========
    {
        "id": 314,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Tenaga Nasional (UNITEN)",
        "ranking": "#14 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Kajang",
        "established": "1976",
        "students": "8,000+",
        "international": "10%",
        "description": "Energy-focused university owned by Tenaga Nasional Berhad. Strong in engineering, IT, and business with excellent industry connections.",
        "programs": {
            "undergraduate": ["Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Computer Science", "Business", "Accounting"],
            "graduate": ["MBA", "Engineering Management", "Energy Economics", "Power Systems"],
            "phd": ["PhD in Engineering", "PhD in Energy", "PhD in Computer Science"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 5.5", "Foundation/STPM", "Math Background"],
            "graduate": ["Bachelor's Degree", "IELTS 6.0", "Work Experience"],
            "phd": ["Master's Degree", "IELTS 6.5", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 18,000 - 28,000/year ($3,800 - $6,000 USD)",
            "graduate": "RM 20,000 - 32,000/year ($4,300 - $6,800 USD)",
            "phd": "RM 22,000 - 35,000/year ($4,700 - $7,500 USD)"
        },
        "scholarships": [
            {"name": "UNITEN Energy Scholarship", "coverage": "50% tuition", "deadline": "June"},
            {"name": "TNB Industry Grant", "coverage": "RM 15,000", "deadline": "May"}
        ],
        "deadlines": {"fall": "July 31", "spring": "January 31"},
        "accepted_students": "200+",
        "acceptance_rate": "35-40%",
        "language": "English",
        "website": "www.uniten.edu.my",
        "image": "⚡"
    },
    
    # ======== UNIVERSITY 15 ========
    {
        "id": 315,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Asia Pacific University (APU)",
        "ranking": "#15 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Kuala Lumpur",
        "established": "1993",
        "students": "12,000+",
        "international": "35%",
        "description": "Leading tech university with students from over 130 countries. Strong in computing, engineering, and business.",
        "programs": {
            "undergraduate": ["Computer Science", "Software Engineering", "IT", "Business", "Accounting", "Engineering", "Design"],
            "graduate": ["MBA", "Data Science", "Cyber Security", "AI", "Finance"],
            "phd": ["PhD in Computing", "PhD in Business", "PhD in Engineering"]
        },
        "requirements": {
            "undergraduate": ["High School Diploma", "IELTS 5.5", "Foundation/A-Levels"],
            "graduate": ["Bachelor's Degree", "IELTS 6.0", "Work Experience"],
            "phd": ["Master's Degree", "IELTS 6.5", "Research Proposal"]
        },
        "fees": {
            "undergraduate": "RM 20,000 - 30,000/year ($4,300 - $6,400 USD)",
            "graduate": "RM 22,000 - 35,000/year ($4,700 - $7,500 USD)",
            "phd": "RM 25,000 - 38,000/year ($5,300 - $8,100 USD)"
        },
        "scholarships": [
            {"name": "APU International Scholarship", "coverage": "25-50% tuition", "deadline": "May"},
            {"name": "Tech Talent Grant", "coverage": "RM 12,000", "deadline": "June"}
        ],
        "deadlines": {"fall": "June 30", "spring": "December 31"},
        "accepted_students": "400+",
        "acceptance_rate": "30-35%",
        "language": "English",
        "website": "www.apu.edu.my",
        "image": "💻"
    },
    
    # ======== UNIVERSITY 16 ========
    {
        "id": 316,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Malaysia Pahang (UMP)",
        "ranking": "#16 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Pekan, Pahang",
        "established": "2002",
        "students": "12,000+",
        "international": "6%",
        "description": "Technical university strong in engineering and technology. Focus on industry collaboration and applied research.",
        "programs": {
            "undergraduate": ["Mechanical Engineering", "Chemical Engineering", "Civil Engineering", "Electrical Engineering", "Computer Science"],
            "graduate": ["Engineering Management", "Materials Engineering", "Manufacturing"],
            "phd": ["PhD in Engineering", "PhD in Technology"]
        },
        "fees": {
            "undergraduate": "RM 8,000 - 15,000/year",
            "graduate": "RM 10,000 - 18,000/year",
            "phd": "RM 12,000 - 20,000/year"
        },
        "deadlines": {"fall": "June", "spring": "December"},
        "image": "🏭"
    },
    
    # ======== UNIVERSITY 17 ========
    {
        "id": 317,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Malaysia Perlis (UniMAP)",
        "ranking": "#17 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Perlis",
        "established": "2001",
        "students": "10,000+",
        "international": "5%",
        "description": "Engineering-focused university in northern Malaysia. Known for microelectronics and semiconductor research.",
        "programs": {
            "undergraduate": ["Electrical Engineering", "Mechanical Engineering", "Microelectronics", "Computer Engineering"],
            "graduate": ["Microengineering", "Embedded Systems"],
            "phd": ["PhD in Engineering"]
        },
        "fees": {
            "undergraduate": "RM 8,000 - 14,000/year",
            "graduate": "RM 10,000 - 16,000/year",
            "phd": "RM 12,000 - 18,000/year"
        },
        "deadlines": {"fall": "June", "spring": "December"},
        "image": "🔧"
    },
    
    # ======== UNIVERSITY 18 ========
    {
        "id": 318,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Malaysia Kelantan (UMK)",
        "ranking": "#18 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Kelantan",
        "established": "2006",
        "students": "8,000+",
        "international": "4%",
        "description": "University focused on entrepreneurship and creative industries. Strong in business and heritage studies.",
        "programs": {
            "undergraduate": ["Entrepreneurship", "Creative Industries", "Business", "Hospitality"],
            "graduate": ["MBA", "Creative Management"],
            "phd": ["PhD in Entrepreneurship"]
        },
        "fees": {
            "undergraduate": "RM 7,000 - 13,000/year",
            "graduate": "RM 9,000 - 15,000/year",
            "phd": "RM 11,000 - 17,000/year"
        },
        "deadlines": {"fall": "June", "spring": "December"},
        "image": "💡"
    },
    
    # ======== UNIVERSITY 19 ========
    {
        "id": 319,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Pertahanan Nasional Malaysia (UPNM)",
        "ranking": "#19 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Kuala Lumpur",
        "established": "2006",
        "students": "5,000+",
        "international": "3%",
        "description": "National Defence University of Malaysia. Trains military officers and defense professionals.",
        "programs": {
            "undergraduate": ["Engineering", "Management", "Medicine", "Defense Studies"],
            "graduate": ["Defense Management", "Strategic Studies"],
            "phd": ["PhD in Defense Studies"]
        },
        "fees": {
            "undergraduate": "RM 8,000 - 14,000/year",
            "graduate": "RM 10,000 - 16,000/year",
            "phd": "RM 12,000 - 18,000/year"
        },
        "deadlines": {"fall": "May", "spring": "November"},
        "image": "⚔️"
    },
    
    # ======== UNIVERSITY 20 ========
    {
        "id": 320,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Sultan Zainal Abidin (UniSZA)",
        "ranking": "#20 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Terengganu",
        "established": "2005",
        "students": "10,000+",
        "international": "5%",
        "description": "Comprehensive university strong in medicine, pharmacy, and Islamic finance on the east coast.",
        "programs": {
            "undergraduate": ["Medicine", "Pharmacy", "Islamic Finance", "Business", "Law"],
            "graduate": ["Clinical Medicine", "Islamic Banking"],
            "phd": ["PhD in Medicine", "PhD in Islamic Studies"]
        },
        "fees": {
            "undergraduate": "RM 8,000 - 16,000/year",
            "graduate": "RM 10,000 - 18,000/year",
            "phd": "RM 12,000 - 20,000/year"
        },
        "deadlines": {"fall": "June", "spring": "December"},
        "image": "🏥"
    },
    
    # ======== UNIVERSITY 21 ========
    {
        "id": 321,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Teknikal Malaysia Melaka (UTeM)",
        "ranking": "#21 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Melaka",
        "established": "2000",
        "students": "11,000+",
        "international": "5%",
        "description": "Technical university in historic Melaka. Strong in manufacturing, robotics, and ICT.",
        "programs": {
            "undergraduate": ["Manufacturing Engineering", "Robotics", "ICT", "Electronics"],
            "graduate": ["Advanced Manufacturing", "Automation"],
            "phd": ["PhD in Engineering"]
        },
        "fees": {
            "undergraduate": "RM 8,000 - 15,000/year",
            "graduate": "RM 10,000 - 17,000/year",
            "phd": "RM 12,000 - 19,000/year"
        },
        "deadlines": {"fall": "June", "spring": "December"},
        "image": "🤖"
    },
    
    # ======== UNIVERSITY 22 ========
    {
        "id": 322,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Malaysia Terengganu (UMT)",
        "ranking": "#22 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Terengganu",
        "established": "1979",
        "students": "9,000+",
        "international": "6%",
        "description": "Marine and fisheries university. Strong in oceanography, aquaculture, and marine sciences.",
        "programs": {
            "undergraduate": ["Marine Science", "Fisheries", "Aquaculture", "Oceanography"],
            "graduate": ["Marine Biology", "Fisheries Science"],
            "phd": ["PhD in Marine Science"]
        },
        "fees": {
            "undergraduate": "RM 8,000 - 14,000/year",
            "graduate": "RM 10,000 - 16,000/year",
            "phd": "RM 12,000 - 18,000/year"
        },
        "deadlines": {"fall": "June", "spring": "December"},
        "image": "🐠"
    },
    
    # ======== UNIVERSITY 23 ========
    {
        "id": 323,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Islam Antarabangsa Sultan Abdul Halim Mu'adzam Shah (UniSHAMS)",
        "ranking": "#23 in Malaysia",
        "world_ranking": "1000+",
        "location": "Kedah",
        "established": "1995",
        "students": "5,000+",
        "international": "10%",
        "description": "Islamic university focused on Shariah, Islamic banking, and Arabic studies.",
        "programs": {
            "undergraduate": ["Shariah Law", "Islamic Banking", "Arabic Studies", "Usuluddin"],
            "graduate": ["Islamic Finance", "Comparative Law"],
            "phd": ["PhD in Islamic Studies"]
        },
        "fees": {
            "undergraduate": "RM 7,000 - 12,000/year",
            "graduate": "RM 9,000 - 14,000/year",
            "phd": "RM 11,000 - 16,000/year"
        },
        "deadlines": {"fall": "July", "spring": "January"},
        "image": "🕌"
    },
    
    # ======== UNIVERSITY 24 ========
    {
        "id": 324,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Kuala Lumpur (UniKL)",
        "ranking": "#24 in Malaysia",
        "world_ranking": "1000+",
        "location": "Kuala Lumpur",
        "established": "2002",
        "students": "20,000+",
        "international": "8%",
        "description": "Technical university with multiple campuses. Strong in engineering technology and vocational training.",
        "programs": {
            "undergraduate": ["Engineering Technology", "Aviation", "Marine Technology", "Business"],
            "graduate": ["Technical Management", "Engineering Technology"],
            "phd": ["PhD in Engineering Technology"]
        },
        "fees": {
            "undergraduate": "RM 10,000 - 18,000/year",
            "graduate": "RM 12,000 - 20,000/year",
            "phd": "RM 14,000 - 22,000/year"
        },
        "deadlines": {"fall": "May", "spring": "November"},
        "image": "✈️"
    },
    
    # ======== UNIVERSITY 25 ========
    {
        "id": 325,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Universiti Tunku Abdul Rahman (UTAR)",
        "ranking": "#25 in Malaysia",
        "world_ranking": "601-650",
        "location": "Kampar/Sungai Long",
        "established": "2002",
        "students": "20,000+",
        "international": "12%",
        "description": "Leading private non-profit university. Strong in engineering, business, and Chinese studies.",
        "programs": {
            "undergraduate": ["Engineering", "Business", "Chinese Studies", "Medicine", "IT"],
            "graduate": ["MBA", "Engineering", "Chinese Studies"],
            "phd": ["PhD in various fields"]
        },
        "fees": {
            "undergraduate": "RM 15,000 - 25,000/year",
            "graduate": "RM 18,000 - 28,000/year",
            "phd": "RM 20,000 - 30,000/year"
        },
        "scholarships": [
            {"name": "UTAR Merit Scholarship", "coverage": "25-100%", "deadline": "May"}
        ],
        "deadlines": {"fall": "June", "spring": "December"},
        "image": "🏛️"
    },
    
    # ======== UNIVERSITY 26 ========
    {
        "id": 326,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "INTI International University",
        "ranking": "#26 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Nilai",
        "established": "1986",
        "students": "15,000+",
        "international": "20%",
        "description": "Leading private university with partnerships in UK, US, and Australia. Strong in business and engineering.",
        "programs": {
            "undergraduate": ["Business", "Engineering", "IT", "Biotechnology"],
            "graduate": ["MBA", "Business Analytics"],
            "phd": ["PhD in Business", "PhD in Engineering"]
        },
        "fees": {
            "undergraduate": "RM 20,000 - 32,000/year",
            "graduate": "RM 22,000 - 35,000/year",
            "phd": "RM 25,000 - 38,000/year"
        },
        "scholarships": [
            {"name": "INTI Excellence Award", "coverage": "25-50%", "deadline": "June"}
        ],
        "deadlines": {"fall": "July", "spring": "January"},
        "image": "🌍"
    },
    
    # ======== UNIVERSITY 27 ========
    {
        "id": 327,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "SEGi University",
        "ranking": "#27 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Kota Damansara",
        "established": "1977",
        "students": "12,000+",
        "international": "15%",
        "description": "Comprehensive private university. Strong in medicine, dentistry, and health sciences.",
        "programs": {
            "undergraduate": ["Medicine", "Dentistry", "Pharmacy", "Engineering", "Business"],
            "graduate": ["MBA", "Clinical Medicine"],
            "phd": ["PhD in Medicine", "PhD in Business"]
        },
        "fees": {
            "undergraduate": "RM 22,000 - 40,000/year",
            "graduate": "RM 25,000 - 42,000/year",
            "phd": "RM 28,000 - 45,000/year"
        },
        "scholarships": [
            {"name": "SEGi Health Scholarship", "coverage": "25-75%", "deadline": "May"}
        ],
        "deadlines": {"fall": "June", "spring": "December"},
        "image": "🦷"
    },
    
    # ======== UNIVERSITY 28 ========
    {
        "id": 328,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "UCSI University",
        "ranking": "#28 in Malaysia",
        "world_ranking": "651-700",
        "location": "Cheras, Kuala Lumpur",
        "established": "1986",
        "students": "10,000+",
        "international": "18%",
        "description": "Leading private university strong in music, medicine, and engineering. Known for its medical school.",
        "programs": {
            "undergraduate": ["Medicine", "Pharmacy", "Music", "Engineering", "Business"],
            "graduate": ["MBA", "Medical Sciences"],
            "phd": ["PhD in Medicine", "PhD in Music"]
        },
        "fees": {
            "undergraduate": "RM 25,000 - 45,000/year",
            "graduate": "RM 28,000 - 48,000/year",
            "phd": "RM 30,000 - 50,000/year"
        },
        "scholarships": [
            {"name": "UCSI Excellence Scholarship", "coverage": "25-100%", "deadline": "April"}
        ],
        "deadlines": {"fall": "May", "spring": "November"},
        "image": "🎵"
    },
    
    # ======== UNIVERSITY 29 ========
    {
        "id": 329,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Management and Science University (MSU)",
        "ranking": "#29 in Malaysia",
        "world_ranking": "801-1000",
        "location": "Shah Alam",
        "established": "2001",
        "students": "9,000+",
        "international": "25%",
        "description": "University focused on management and health sciences. Strong international student community.",
        "programs": {
            "undergraduate": ["Medicine", "Pharmacy", "Nursing", "Business", "IT"],
            "graduate": ["MBA", "Public Health"],
            "phd": ["PhD in Health Sciences", "PhD in Management"]
        },
        "fees": {
            "undergraduate": "RM 18,000 - 35,000/year",
            "graduate": "RM 20,000 - 38,000/year",
            "phd": "RM 22,000 - 40,000/year"
        },
        "scholarships": [
            {"name": "MSU International Scholarship", "coverage": "25-50%", "deadline": "June"}
        ],
        "deadlines": {"fall": "July", "spring": "January"},
        "image": "🏥"
    },
    
    # ======== UNIVERSITY 30 ========
    {
        "id": 330,
        "image_url": "https://images.unsplash.com/photo-1562774053-701939374585?w=400",
        "name": "Infrastructure University Kuala Lumpur (IUKL)",
        "ranking": "#30 in Malaysia",
        "world_ranking": "1000+",
        "location": "Kajang",
        "established": "1998",
        "students": "5,000+",
        "international": "12%",
        "description": "Specialized university focusing on infrastructure, construction, and architecture.",
        "programs": {
            "undergraduate": ["Civil Engineering", "Architecture", "Quantity Surveying", "Business"],
            "graduate": ["Construction Management", "Infrastructure"],
            "phd": ["PhD in Engineering", "PhD in Architecture"]
        },
        "fees": {
            "undergraduate": "RM 15,000 - 25,000/year",
            "graduate": "RM 18,000 - 28,000/year",
            "phd": "RM 20,000 - 30,000/year"
        },
        "scholarships": [
            {"name": "IUKL Infrastructure Grant", "coverage": "25% tuition", "deadline": "June"}
        ],
        "deadlines": {"fall": "July", "spring": "January"},
        "image": "🏗️"
    }
]

# ==================== JAPAN - 30 UNIVERSITIES ====================
japan_universities = [
    {
        "id": 401,
        "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400",
        "name": "University of Tokyo",
        "ranking": "#1 in Japan",
        "world_ranking": "23rd",
        "location": "Tokyo",
        "established": "1877",
        "students": "28,000+",
        "international": "12%",
        "description": "Japan's top university, excellent in research and academics. Produced 15 prime ministers and 9 Nobel laureates.",
        "programs": {
            "undergraduate": ["Engineering", "Law", "Economics", "Medicine", "Sciences", "Agriculture", "Pharmacy"],
            "graduate": ["MBA", "Engineering", "International Studies", "Public Policy", "Law", "Medicine"],
            "phd": ["PhD in all fields"]
        },
        "fees": {
            "undergraduate": "JPY 535,800/year ($3,600 USD)",
            "graduate": "JPY 535,800/year ($3,600 USD)",
            "phd": "JPY 520,800/year ($3,500 USD)"
        },
        "scholarships": [
            {"name": "MEXT Scholarship", "coverage": "Full tuition + living + airfare", "deadline": "April-May"},
            {"name": "JASSO Scholarship", "coverage": "JPY 48,000/month", "deadline": "March"},
            {"name": "University of Tokyo Scholarship", "coverage": "Partial tuition", "deadline": "February"}
        ],
        "deadlines": {"fall": "January 15", "spring": "August 31"},
        "accepted_students": "400+",
        "image": "🗼"
    },
    {
        "id": 402,
        "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400",
        "name": "Kyoto University",
        "ranking": "#2 in Japan",
        "world_ranking": "36th",
        "location": "Kyoto",
        "established": "1897",
        "students": "22,000+",
        "international": "10%",
        "description": "Research powerhouse, known for producing Nobel laureates in physics and chemistry.",
        "programs": {
            "undergraduate": ["Science", "Engineering", "Law", "Economics", "Medicine", "Pharmacy"],
            "graduate": ["Engineering", "Science", "Global Studies"],
            "phd": ["PhD in Science", "PhD in Engineering"]
        },
        "fees": {"undergraduate": "JPY 535,800/year"},
        "scholarships": [
            {"name": "MEXT Scholarship", "coverage": "Full", "deadline": "April"},
            {"name": "Kyoto University Fellowship", "coverage": "JPY 150,000/month", "deadline": "March"}
        ],
        "deadlines": {"fall": "January 31", "spring": "September 15"},
        "image": "⛩️"
    },
    {
        "id": 403,
        "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400",
        "name": "Osaka University",
        "ranking": "#3 in Japan",
        "world_ranking": "55th",
        "location": "Osaka",
        "established": "1931",
        "students": "23,000+",
        "international": "11%",
        "description": "Leading university in western Japan, strong in science and technology.",
        "programs": {
            "undergraduate": ["Engineering", "Science", "Medicine", "Economics", "Law"],
            "graduate": ["Engineering", "Science", "MBA"],
            "phd": ["PhD in Engineering", "PhD in Science"]
        },
        "fees": {"undergraduate": "JPY 535,800/year"},
        "scholarships": [
            {"name": "MEXT Scholarship", "coverage": "Full", "deadline": "April"},
            {"name": "Osaka University Scholarship", "coverage": "JPY 50,000/month", "deadline": "May"}
        ],
        "deadlines": {"fall": "February 15", "spring": "September 30"},
        "image": "🏙️"
    }
]

# ==================== JAPAN - ADDITIONAL 27 UNIVERSITIES (4-30) ====================
# Add comprehensive Japan universities
for i in range(4, 31):
    japan_universities.append({
        "id": 400 + i,
        "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=400",
        "name": f"{['Tohoku', 'Nagoya', 'Hokkaido', 'Kyushu', 'Tokyo Tech', 'Keio', 'Waseda', 'Hitotsubashi', 'Kobe', 'Hiroshima', 'Chiba', 'Okayama', 'Kumamoto', 'Nagasaki', 'Kanazawa', 'Niigata', 'Shinshu', 'Yamaguchi', 'Ehime', 'Kagawa', 'Miyazaki', 'Oita', 'Saga', 'Ryukyu', 'Akita', 'Fukui', 'Yamanashi'][i-4]} University",
        "ranking": f"#{i} in Japan",
        "world_ranking": f"{100 + i*12}th",
        "location": ["Sendai", "Nagoya", "Sapporo", "Fukuoka", "Tokyo", "Tokyo", "Tokyo", "Tokyo", "Kobe", "Hiroshima", "Chiba", "Okayama", "Kumamoto", "Nagasaki", "Kanazawa", "Niigata", "Nagano", "Yamaguchi", "Ehime", "Kagawa", "Miyazaki", "Oita", "Saga", "Okinawa", "Akita", "Fukui", "Kofu"][i-4],
        "established": "1900s",
        "students": "8,000-20,000",
        "international": "5-12%",
        "description": f"Leading Japanese university with strong programs in various fields.",
        "programs": {
            "undergraduate": ["Engineering", "Science", "Economics", "Humanities"],
            "graduate": ["Engineering", "MBA", "Science"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "JPY 535,800 - 800,000/year",
            "graduate": "JPY 535,800 - 850,000/year",
            "phd": "JPY 520,800 - 820,000/year"
        },
        "scholarships": [
            {"name": "MEXT Scholarship", "coverage": "Full", "deadline": "April"},
            {"name": "JASSO Scholarship", "coverage": "JPY 48,000/month", "deadline": "March"}
        ],
        "deadlines": {"fall": "January-February", "spring": "August-September"},
        "accepted_students": "100-200",
        "image": "🎌"
    })

# ==================== KOREA - 30 UNIVERSITIES ====================
korea_universities = [
    {
        "id": 501,
        "image_url": "https://images.unsplash.com/photo-1519452575417-564c1401ecc0?w=400",
        "name": "Seoul National University",
        "ranking": "#1 in Korea",
        "world_ranking": "29th",
        "location": "Seoul",
        "established": "1946",
        "students": "28,000+",
        "international": "10%",
        "description": "Korea's most prestigious national university. Leading research institution with top programs across all fields.",
        "programs": {
            "undergraduate": ["Engineering", "Business", "Medicine", "Law", "Sciences", "Humanities", "Agriculture"],
            "graduate": ["MBA", "Engineering", "International Studies", "Public Administration", "Data Science"],
            "phd": ["PhD in all fields"]
        },
        "fees": {
            "undergraduate": "KRW 5,000,000 - 7,000,000/year ($3,800 - $5,300 USD)",
            "graduate": "KRW 6,000,000 - 8,000,000/year ($4,500 - $6,000 USD)",
            "phd": "KRW 5,000,000 - 7,000,000/year ($3,800 - $5,300 USD)"
        },
        "scholarships": [
            {"name": "KGSP Scholarship", "coverage": "Full tuition + living + airfare", "deadline": "February"},
            {"name": "SNU Scholarship", "coverage": "50-100% tuition", "deadline": "March"},
            {"name": "Samsung Scholarship", "coverage": "Full tuition + stipend", "deadline": "April"}
        ],
        "deadlines": {"fall": "March 31", "spring": "September 30"},
        "accepted_students": "300+",
        "image": "🏛️"
    },
    {
        "id": 502,
        "image_url": "https://images.unsplash.com/photo-1519452575417-564c1401ecc0?w=400",
        "name": "KAIST",
        "ranking": "#2 in Korea",
        "world_ranking": "41st",
        "location": "Daejeon",
        "established": "1971",
        "students": "10,000+",
        "international": "15%",
        "description": "Korea's top research university in science and engineering. Known as the 'MIT of Asia'.",
        "programs": {
            "undergraduate": ["Electrical Engineering", "Computer Science", "Mechanical Engineering", "Physics", "Chemistry"],
            "graduate": ["AI", "Robotics", "Quantum Computing", "Biotechnology", "Business"],
            "phd": ["PhD in Engineering", "PhD in Sciences", "PhD in Computing"]
        },
        "fees": {
            "undergraduate": "KRW 6,000,000 - 8,000,000/year",
            "graduate": "KRW 7,000,000 - 9,000,000/year",
            "phd": "KRW 6,000,000 - 8,000,000/year"
        },
        "scholarships": [
            {"name": "KAIST Scholarship", "coverage": "Full tuition + stipend", "deadline": "April"},
            {"name": "Korean Government Scholarship", "coverage": "Full package", "deadline": "February"}
        ],
        "deadlines": {"fall": "April 15", "spring": "October 15"},
        "accepted_students": "400+",
        "image": "🔬"
    },
    {
        "id": 503,
        "image_url": "https://images.unsplash.com/photo-1519452575417-564c1401ecc0?w=400",
        "name": "Yonsei University",
        "ranking": "#3 in Korea",
        "world_ranking": "73rd",
        "location": "Seoul",
        "established": "1885",
        "students": "26,000+",
        "international": "18%",
        "description": "One of Korea's top private universities, famous for business and medicine.",
        "programs": {
            "undergraduate": ["Business", "Medicine", "Engineering", "Economics", "Political Science"],
            "graduate": ["MBA", "International Studies", "Public Health", "Law"],
            "phd": ["PhD in Business", "PhD in Medicine", "PhD in Engineering"]
        },
        "fees": {
            "undergraduate": "KRW 7,000,000 - 9,000,000/year",
            "graduate": "KRW 8,000,000 - 10,000,000/year",
            "phd": "KRW 7,000,000 - 9,000,000/year"
        },
        "scholarships": [
            {"name": "Yonsei Scholarship", "coverage": "50-100% tuition", "deadline": "April"},
            {"name": "Underwood International Scholarship", "coverage": "Full tuition", "deadline": "March"}
        ],
        "deadlines": {"fall": "April 30", "spring": "October 31"},
        "accepted_students": "500+",
        "image": "🏫"
    }
]

# ==================== KOREA - ADDITIONAL 27 UNIVERSITIES (4-30) ====================
# Add comprehensive Korea universities
for i in range(4, 31):
    korea_universities.append({
        "id": 500 + i,
        "image_url": "https://images.unsplash.com/photo-1519452575417-564c1401ecc0?w=400",
        "name": f"{['Korea', 'Sungkyunkwan', 'Hanyang', 'Kyung Hee', 'Ewha', 'Sogang', 'Pusan National', 'Gyeongbuk', 'Jeonbuk', 'Chung-Ang', 'Inha', 'Dongguk', 'Hongik', 'Konkuk', 'Kookmin', 'Sejong', 'Sookmyung', 'Ajou', 'Incheon', 'Gangneung', 'Andong', 'Changwon', 'Kongju', 'Pukyong', 'Mokpo', 'University of Seoul', 'Seoultech'][i-4]} University",
        "ranking": f"#{i} in Korea",
        "world_ranking": f"{80 + i*12}th",
        "location": ["Seoul", "Seoul", "Seoul", "Seoul", "Seoul", "Seoul", "Busan", "Daegu", "Jeonju", "Seoul", "Incheon", "Seoul", "Seoul", "Seoul", "Seoul", "Seoul", "Seoul", "Suwon", "Incheon", "Gangneung", "Andong", "Changwon", "Kongju", "Busan", "Mokpo", "Seoul", "Seoul"][i-4],
        "established": "1900s-2000s",
        "students": "10,000-25,000",
        "international": "5-15%",
        "description": f"Leading Korean university with strong programs.",
        "programs": {
            "undergraduate": ["Engineering", "Business", "Humanities", "Science"],
            "graduate": ["MBA", "Engineering", "Education"],
            "phd": ["PhD programs"]
        },
        "fees": {
            "undergraduate": "KRW 5,000,000 - 8,000,000/year",
            "graduate": "KRW 6,000,000 - 9,000,000/year",
            "phd": "KRW 5,000,000 - 8,000,000/year"
        },
        "scholarships": [
            {"name": "University Scholarship", "coverage": "20-100%", "deadline": "April-May"},
            {"name": "Korean Government Scholarship", "coverage": "Full", "deadline": "February"}
        ],
        "deadlines": {"fall": "April-May", "spring": "October-November"},
        "accepted_students": "100-300",
        "image": "🎓"
    })

# ==================== SAVE FUNCTIONS ====================
def save_application_to_file(application_data):
    """Save application to a text file"""
    try:
        filename = f"applications_{datetime.now().strftime('%Y%m%d')}.txt"
        
        application_text = f"""
{'='*80}
DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
COUNTRY: {application_data['country']}
UNIVERSITY: {application_data['university']}
{'='*80}

STUDENT DETAILS:
----------------------------------------
Name: {application_data['student_name']}
Email: {application_data['student_email']}
Phone: {application_data['student_phone']}
Program Level: {application_data['program_level']}
Preferred Program: {application_data.get('preferred_program', 'Not specified')}
Files: {', '.join(application_data.get('files', []))}

MESSAGE:
{application_data.get('message', 'No message')}

{'='*80}
"""
        
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(application_text)
        
        print(f"✅ Application saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving to file: {e}")
        return False

def save_to_database(data):
    """Save application to SQLite database as backup"""
    try:
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        c.execute('''INSERT INTO applications 
                     (country, university, student_name, student_email, student_phone, 
                      program_level, preferred_program, message, application_date)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data['country'], data['university'], data['student_name'],
                   data['student_email'], data['student_phone'], data['program_level'],
                   data.get('preferred_program', ''), data.get('message', ''),
                   data.get('submission_date', datetime.now())))  # Use submission date
        conn.commit()
        conn.close()
        print("✅ Application saved to database")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

  # EMAIL FUNCTION WITH ATTACHMENTS
def send_application_email(application_data):
    print("🔥🔥🔥 EMAIL FUNCTION IS BEING CALLED! 🔥🔥🔥")
    """send email notification with all uploaded files attached"""
    print(f"📨 Preparing email for: {application_data['student_name']}")
    print("🔵 send_application_email function CALLED!")
    try:
        # Email to admin (you) WITH ATTACHMENTS
        admin_msg = Message(
            subject=f" NEW APPLICATION: {application_data['student_name']} - {application_data['university']}",
            recipients=['kharyglobal@gmail.com'],
            body=f"""
NEW APPLICATION RECEIVED!
========================

STUDENT DETAILS:
---------------
Name: {application_data['student_name']}
Email: {application_data['student_email']}
Phone: {application_data['student_phone']}
Program Level: {application_data['program_level']}
Preferred Program: {application_data.get('preferred_program', 'Not specified')}

APPLICATION DETAILS:
-------------------
University: {application_data['university']}
Country: {application_data['country']}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

MESSAGE:
--------
{application_data.get('message', 'No message')}

FILES ATTACHED:
--------------
{len(application_data.get('files', []))} file(s) are attached to this email
            """
        )
        
        # ATTACH ALL UPLOADED FILES TO THE EMAIL
        files_attached = 0
        if 'files' in application_data and application_data['files']:
            for filename in application_data['files']:
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.exists(file_path):
                    with app.open_resource(file_path) as fp:
                        admin_msg.attach(
                            filename,  # Filename as it appears in email
                            'application/octet-stream',  # Generic file type
                            fp.read()  # File data
                        )
                    files_attached += 1
                    print(f"📎 Attached: {filename}")
        
        # Send email with attachments
        mail.send(admin_msg)
        print(f"✅ Email sent to admin with {files_attached} attachments")
        
        # Also send confirmation to student (without attachments)
        student_msg = Message(
            subject=f"Thank you for applying to {application_data['university']} - KHARY GLOBAL EDU",
            recipients=[application_data['student_email']],
            body=f"""
Dear {application_data['student_name']},

Thank you for submitting your application to {application_data['university']} through KHARY GLOBAL EDU!

We have received your application and {len(application_data.get('files', []))} document(s). Our team will review everything within 24-48 hours.

Your Application Summary:
------------------------
University: {application_data['university']}
Country: {application_data['country']}
Program Level: {application_data['program_level']}
Documents Uploaded: {len(application_data.get('files', []))}

We'll contact you via email or WhatsApp shortly.

Best regards,
The KHARY GLOBAL EDU Team
            """
        )
        
        mail.send(student_msg)  # ← FIXED: Changed from admin_msg to student_msg
        print("✅ Confirmation email sent to student")
        
        return True
        
    except Exception as e:
        print(f"❌ EMAIL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

# ==================== ROUTES ====================
@app.route('/submit-application', methods=['POST'])
@login_required
def submit_application():
    """Handle application form submission"""
    try:
        data = request.json
        print(f"\n📨 New application received for: {data['university']} in {data['country']}")
        
        save_to_database(data)
        save_application_to_file(data)
        
        return jsonify({'success': True, 'message': 'Application received successfully!'})
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/submit-application-with-files', methods=['POST'])
@login_required
def submit_application_with_files():
    """Handle application form submission with file uploads"""
    try:
        # Get form data
        university = request.form.get('university')
        country = request.form.get('country')
        student_name = request.form.get('student_name')
        student_email = request.form.get('student_email')
        student_phone = request.form.get('student_phone')
        program_level = request.form.get('program_level')
        preferred_program = request.form.get('preferred_program', '')
        message = request.form.get('message', '')
        
        # ADD SUBMISSION DATE AND TIME
        submission_date = datetime.now()
        date_formatted = submission_date.strftime('%Y-%m-%d')
        time_formatted = submission_date.strftime('%H:%M:%S')
        datetime_formatted = submission_date.strftime('%Y-%m-%d %H:%M:%S')
        
        # Save files with date in filename
        uploaded_files = []
        file_details = []  # Store file details for tracking
        if 'documents' in request.files:
            files = request.files.getlist('documents')
            file_count = 0
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    file_count += 1
                    # Add date to filename for better tracking
                    date_str = submission_date.strftime('%Y%m%d')
                    timestamp = submission_date.strftime('%H%M%S')
                    filename = secure_filename(f"{student_name}_{date_str}_{timestamp}_file{file_count}_{file.filename}")
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    uploaded_files.append(filename)
                    
                    # Store file details for tracking
                    file_details.append({
                        'original_name': file.filename,
                        'saved_as': filename,
                        'size': len(file.read()),  # Get file size
                        'type': file.content_type
                    })
                    # Reset file pointer after reading
                    file.seek(0)
        
        # Prepare application data with ALL information
        data = {
            'university': university,
            'country': country,
            'student_name': student_name,
            'student_email': student_email,
            'student_phone': student_phone,
            'program_level': program_level,
            'preferred_program': preferred_program,
            'message': message,
            'submission_date': datetime_formatted,  # Full date and time
            'submission_date_only': date_formatted,  # Just the date
            'submission_time_only': time_formatted,  # Just the time
            'files': uploaded_files,
            'file_details': file_details,  # Detailed file information
            'total_files': len(uploaded_files),
            'file_names': ', '.join(uploaded_files) if uploaded_files else 'No files'
        }
        
        # Save to database and file
        save_to_database(data)
        save_application_to_file(data)
        
        # Save detailed file info to a separate log with date
        with open('uploads_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"SUBMISSION DATE: {datetime_formatted}\n")
            f.write(f"{'='*60}\n")
            f.write(f"Student: {student_name}\n")
            f.write(f"Email: {student_email}\n")
            f.write(f"Phone: {student_phone}\n")
            f.write(f"University: {university} - {country}\n")
            f.write(f"Program: {program_level} - {preferred_program}\n")
            f.write(f"Message: {message}\n")
            f.write(f"{'-'*40}\n")
            f.write(f"FILES UPLOADED ({len(uploaded_files)}):\n")
            for i, file in enumerate(file_details, 1):
                f.write(f"  {i}. {file['original_name']} → {file['saved_as']}\n")
            f.write(f"{'='*60}\n\n")
        
        # Print detailed submission info to terminal
        print(f"\n{'='*60}")
        print(f"📅 SUBMISSION: {datetime_formatted}")
        print(f"{'='*60}")
        print(f"👤 Student: {student_name} ({student_email})")
        print(f"📞 Phone: {student_phone}")
        print(f"🏫 University: {university} - {country}")
        print(f"📚 Program: {program_level} - {preferred_program}")
        print(f"💬 Message: {message}")
        print(f"📎 Files: {len(uploaded_files)} uploaded")
        for i, file in enumerate(uploaded_files, 1):
            print(f"   {i}. {file}")
        print(f"{'='*60}\n")
        

        print("=" * 50)
        print("📧 ABOUT TO SEND EMAIL...")
        print(f"Student: {student_name}")
        print(f"Email: {student_email}")
        print(f"Files: {uploaded_files}")
        print("=" * 50)
        
        # Send email notification
        send_application_email(data)
        
        print("✅ Email function called")


        return jsonify({
            'success': True, 
            'message': 'Application received successfully!',
            'submission_date': datetime_formatted,
            'files_uploaded': len(uploaded_files)
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    
@app.route('/api/universities/<country>')
@login_required
def get_universities(country):
    """Return universities data for a specific country"""
    if country == 'china':
        return jsonify(china_universities)
    elif country == 'singapore':
        return jsonify(singapore_universities)
    elif country == 'malaysia':
        return jsonify(malaysia_universities)
    elif country == 'japan':
        return jsonify(japan_universities)
    elif country == 'korea':
        return jsonify(korea_universities)
    else:
        return jsonify([])

@app.route('/khary-global-edu')
@login_required
@admin_required
def khary_admin_panel():
    """KHARY GLOBAL EDU Admin Panel"""
    return render_template('new_admin.html')        

    
@app.route('/admin')
@login_required
@admin_required
def redirect_admin():
    return redirect('/khary-global-edu')

@app.route('/update-application-status', methods=['POST'])
@login_required
def update_application_status():
    try:
        data = request.json
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        c.execute("UPDATE applications SET status = ? WHERE id = ?", 
                 (data['status'], data['id']))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete-application', methods=['POST'])
@login_required
def delete_application():
    try:
        data = request.json
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        c.execute("DELETE FROM applications WHERE id = ?", (data['id'],))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/export-applications')
@login_required
def export_applications():
    try:
        import csv
        from io import StringIO
        import flask
        
        # Get filter parameters
        filter_status = request.args.get('status', 'all')
        filter_country = request.args.get('country', 'all')
        search_query = request.args.get('search', '')
        
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        
        # Build query
        query = "SELECT * FROM applications"
        params = []
        conditions = []
        
        if filter_status != 'all':
            conditions.append("status = ?")
            params.append(filter_status)
        
        if filter_country != 'all':
            conditions.append("country = ?")
            params.append(filter_country)
        
        if search_query:
            conditions.append("(student_name LIKE ? OR student_email LIKE ?)")
            search_term = f"%{search_query}%"
            params.extend([search_term, search_term])
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY application_date DESC"
        
        c.execute(query, params)
        apps = c.fetchall()
        conn.close()
        
        # Create CSV
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['ID', 'Country', 'University', 'Student Name', 'Email', 'Phone', 
                    'Program Level', 'Preferred Program', 'Message', 'Application Date', 'Status'])
        
        for app in apps:
            cw.writerow(app)
        
        output = si.getvalue()
        
        response = flask.make_response(output)
        response.headers["Content-Disposition"] = "attachment; filename=applications.csv"
        response.headers["Content-type"] = "text/csv"
        return response
        
    except Exception as e:
        return str(e)

# ==================== CALL ALL INIT FUNCTIONS ====================
init_db()           # First create all tables

init_blog_posts()   # Finally add blog posts



# ==================== REGISTER ====================
@app.route('/register', methods=['GET', 'POST'])
@rate_limit(limit=3, window=60)
def register():
    if request.method == 'POST':
        try:
            full_name = request.form.get('full_name')
            email = request.form.get('email')
            password = request.form.get('password')
            phone = request.form.get('phone')
            education = request.form.get('education')
            
            # Hash the password
            hashed_password = generate_password_hash(password)
            
            conn = sqlite3.connect('applications.db')
            c = conn.cursor()
            c.execute('''INSERT INTO users 
                         (full_name, email, password, phone, education_level)
                         VALUES (?, ?, ?, ?, ?)''',
                      (full_name, email, hashed_password, phone, education))
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Registration successful! Please login.'})
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'message': 'Email already exists!'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
    
    return render_template('register.html')

# ==================== LOGIN ====================
@app.route('/login', methods=['GET', 'POST'])
@rate_limit(limit=5, window=60)
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_email'] = user[2]
            return jsonify({'success': True, 'message': 'Login successful!', 'redirect': '/'})
        
        return jsonify({'success': False, 'message': 'Invalid email or password!'})
    
    return render_template('login.html')

# ==================== CHECK AUTH ====================
@app.route('/check-auth')
def check_auth():
    return jsonify({
        'logged_in': 'user_id' in session,
        'user_name': session.get('user_name', '')
    })

# ==================== LOGOUT ====================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))



# ==================== APPLY ROUTE ====================


@app.route('/apply')
@login_required
def apply_page():
    university = request.args.get('university', '')
    country = request.args.get('country', '')
    # You can create a pre-filled application form here
    return redirect(url_for('home') + '?apply=' + university + '&country=' + country)

# ==================== DASHBOARD ====================
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user_name=session.get('user_name'))
 # ==================== COMPARE & BLOG ROUTES ====================

@app.route('/compare')
@login_required
def compare():
    return render_template('compare.html')


# ==================== MEDIA GALLERY PAGE ====================
@app.route('/media')

def media():
    """Display media gallery with videos and pictures"""
    return render_template('media.html')

@app.route('/article/<int:article_id>')

def article(article_id):
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    
    # Get the article from database
    c.execute("SELECT id, title, category, author_name, date, read_time, content FROM blog_posts WHERE id = ?", (article_id,))
    article_data = c.fetchone()
    conn.close()
    
    if not article_data:
        return redirect(url_for('blog'))
    
    # Get comments for this article
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    c.execute("SELECT user_name, comment, created_at FROM comments WHERE post_id = ? ORDER BY created_at DESC LIMIT 10", (article_id,))
    comments = c.fetchall()
    conn.close()
    
    # Prepare article content
    article = {
        'id': article_data[0],
        'title': article_data[1],
        'category': article_data[2],
        'author': article_data[3],
        'date': article_data[4],
        'read_time': article_data[5],
        'content': article_data[6],
        'comments': comments
    }
    
    return render_template('article.html', **article)
    
    article = articles.get(article_id)
    if not article:
        return redirect(url_for('blog'))
    
    return render_template('article.html', **article)
    
    # Get user's applications
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    c.execute("SELECT * FROM applications WHERE user_id = ? ORDER BY application_date DESC", (user_id,))
    applications = c.fetchall()
    
    # Get saved universities for comparison
    c.execute("SELECT * FROM saved_universities WHERE user_id = ?", (user_id,))
    saved = c.fetchall()
    conn.close()
    
    return render_template('dashboard.html', 
                         user_name=session['user_name'],
                         applications=applications,
                         saved=saved)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']
    
    if request.method == 'POST':
        phone = request.form.get('phone')
        education = request.form.get('education')
        
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        c.execute("UPDATE users SET phone = ?, education_level = ? WHERE id = ?",
                 (phone, education, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Profile updated!'})
    
    # Get user data
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    
    return render_template('profile.html', user=user)

# ==================== STUDENT MANAGEMENT ====================
@app.route('/student-management')
@admin_required
def student_management():
    """View all students who applied"""
    try:
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT student_name, student_email, student_phone, country, program_level, application_date FROM applications ORDER BY application_date DESC")
        students = c.fetchall()
        conn.close()
        
        student_rows = ""
        for s in students:
            student_rows += f"""
            <tr>
                <td>{s[0]}</td><td>{s[1]}</td><td>{s[2] if s[2] else '-'}</td><td>{s[3]}</td><td>{s[4]}</td><td>{s[5][:10] if s[5] else '-'}</td>
            </tr>
            """
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Student Management - KHARY GLOBAL EDU</title>
            <link rel="stylesheet" href="/static/mobile.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ font-family: Arial; background: #EFF6FF; padding: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 15px; }}
                h1 {{ color: #1E3A8A; border-bottom: 3px solid #D4AF37; padding-bottom: 15px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background: #1E3A8A; color: white; padding: 12px; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                .btn {{ background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }}
                .btn-green {{ background: #28a745; margin-left: 10px; }}
                .btn-gray {{ background: #6c757d; margin-left: 10px; }}
            </style>
        </head>
        <script src="/static/mobile.js"></script>
        <body>
            <div class="container">
                <h1>👥 Student Management</h1>
                <p>All students who have applied through KHARY GLOBAL EDU</p>
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>University</th>
                                <th>Student</th>
                                <th>Country</th>
                                <th>Email</th>
                                <th>Phone</th>
                                <th>Program</th>
                                <th>Date</th>
                                <th>Message</th>
                                <th>Status</th>
                                <th>Actions</th>
                          </tr>
                        </thead>
                        <tbody>
                            {student_rows if student_rows else '<tr><td colspan="6">No students found</td></tr>'}
                        </tbody>
                    </table>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <a href="/khary-global-edu" class="btn">← Back to Admin</a>
                    <a href="/" class="btn btn-green">🏠 Home</a>
                    <a href="/export-applications" class="btn btn-gray">📥 Export All</a>
                </div>
            </div>
        <script src="/static/chatbot.js"></script>
        
        <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
        </html>
        '''
    except Exception as e:
        return f"Error: {e}"


@app.route('/')

def home():
    # Prepare country counts
    country_counts = {
        'china': len(china_universities),
        'singapore': len(singapore_universities),
        'malaysia': len(malaysia_universities),
        'japan': len(japan_universities),
        'korea': len(korea_universities)
    }
    
    # Convert university data to JSON strings
    china_json = json.dumps(china_universities)
    singapore_json = json.dumps(singapore_universities)
    malaysia_json = json.dumps(malaysia_universities)
    japan_json = json.dumps(japan_universities)
    korea_json = json.dumps(korea_universities)
    
    return f'''<!DOCTYPE html>

    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KHARY GLOBAL EDU - Study in Asia</title>
    <link rel="stylesheet" href="/static/mobile.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <style>
      :root {{
            --primary-blue: #1E3A8A;
            --accent-gold: #D4AF37;
            --light-blue: #EFF6FF;
            --dark-gray: #1F2937;
            --white: #FFFFFF;
            --shadow: 0 10px 30px rgba(0,0,0,0.1);
            --hover-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--dark-gray);
            background: var(--light-blue);
        }}
        
        .navbar {{
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary-blue);
            text-decoration: none;
        }}
        
        .logo span {{
            color: var(--accent-gold);
        }}
        
        .nav-links {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}
        
        .nav-links a {{
            color: var(--dark-gray);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}
        
        .nav-links a:hover {{
            color: var(--primary-blue);
        }}
        
        .nav-links .cta {{
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 1.5rem;
            border-radius: 5px;
        }}
        
        .hero {{
            background: linear-gradient(135deg, var(--light-blue), var(--white));
            padding: 4rem 0;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3rem;
            color: var(--primary-blue);
            margin-bottom: 1.5rem;
        }}
        
        .hero p {{
            font-size: 1.2rem;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .mission-box {{
            background: var(--white);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: var(--shadow);
            border-left: 5px solid var(--accent-gold);
            margin: 3rem auto;
            max-width: 900px;
            font-style: italic;
        }}
        
        .mission-box h3 {{
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-style: normal;
            font-size: 2rem;
        }}
        
        .countries-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            padding: 3rem 0;
        }}
        
        .country-card {{
            background: var(--white);
            padding: 2rem 1rem;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: var(--shadow);
        }}
        
        .country-card:hover {{
            transform: translateY(-10px);
            box-shadow: var(--hover-shadow);
        }}
        
        .country-card .flag {{
            font-size: 4rem;
            margin-bottom: 1rem;
        }}
        
        .country-card h3 {{
            color: var(--primary-blue);
            margin-bottom: 0.5rem;
            font-size: 1.5rem;
        }}
        
        .country-card p {{
            color: var(--accent-gold);
            font-weight: bold;
        }}
        
        .university-page {{
            padding: 2rem 0;
        }}
        
        .university-header {{
            background: linear-gradient(135deg, var(--primary-blue), #2D4FA8);
            color: white;
            padding: 4rem 0;
            margin-bottom: 3rem;
            text-align: center;
        }}
        
        .university-header h1 {{
            font-size: 3.5rem;
            margin-bottom: 1rem;
            color: white;
        }}
        
        .university-header .flag {{
            font-size: 5rem;
            margin-bottom: 1rem;
        }}
        
        .university-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }}
        
        .university-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: transform 0.3s;
        }}
        
        .university-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--hover-shadow);
        }}
        
        .university-card-header {{
            background: var(--primary-blue);
            color: white;
            padding: 1.5rem;
            position: relative;
        }}
        
        .university-card-header h3 {{
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            color: white;
        }}
        
        .university-card-header .ranking {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: var(--accent-gold);
            color: var(--primary-blue);
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
        }}
        
        .university-card-body {{
            padding: 2rem;
        }}
        
        .info-item {{
            margin: 1rem 0;
            padding: 1rem;
            background: var(--light-blue);
            border-radius: 10px;
        }}
        
        .program-section {{
            margin: 1.5rem 0;
        }}
        
        .program-section h4 {{
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }}
        
        .program-tag {{
            display: inline-block;
            background: var(--light-blue);
            color: var(--primary-blue);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            margin: 0.3rem;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .program-tag:hover {{
            background: var(--primary-blue);
            color: white;
        }}
        
        .scholarship-item {{
            background: var(--accent-gold);
            color: var(--primary-blue);
            padding: 0.8rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            font-weight: 500;
        }}
        
        .btn {{
            display: inline-block;
            padding: 0.8rem 2rem;
            background: var(--primary-blue);
            color: var(--white);
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            text-align: center;
        }}
        
        .btn:hover {{
            background: var(--accent-gold);
            color: var(--primary-blue);
            transform: translateY(-2px);
        }}
        
        .btn-gold {{
            background: var(--accent-gold);
            color: var(--primary-blue);
        }}
        
        .back-button {{
            display: inline-block;
            margin: 1rem 0 2rem;
            padding: 0.8rem 2rem;
            background: var(--light-blue);
            color: var(--primary-blue);
            text-decoration: none;
            border-radius: 5px;
            cursor: pointer;
            border: none;
            font-weight: bold;
        }}
        
        .modal {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }}
        
        .modal-content {{
            background: white;
            padding: 2.5rem;
            border-radius: 20px;
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
        }}
        
        .modal-content h2 {{
            color: var(--primary-blue);
            margin-bottom: 1.5rem;
        }}
        
        .modal-content input,
        .modal-content select,
        .modal-content textarea {{
            width: 100%;
            padding: 0.8rem;
            margin: 0.5rem 0 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            transition: border 0.3s;
        }}
        
        .modal-content input:focus,
        .modal-content select:focus,
        .modal-content textarea:focus {{
            border-color: var(--primary-blue);
            outline: none;
        }}
        
        .modal-content label {{
            font-weight: bold;
            color: var(--primary-blue);
            display: block;
        }}
        
        .modal-buttons {{
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }}
        
        .footer {{
            background: var(--dark-gray);
            color: var(--white);
            padding: 3rem 0;
            text-align: center;
            margin-top: 4rem;
        }}
        
        .footer a {{
            color: var(--accent-gold);
            text-decoration: none;
        }}
        
        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
            }}
            
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .university-grid {{
                grid-template-columns: 1fr;
            }}
        }}
 
</style>
</head>
<script src="/static/mobile.js"></script>
<!-- Remove or comment these -->
<!-- <script src="/static/mobile-bottom-menu.js"></script> -->
<body>
   <nav class="navbar">
        <nav style="background: #EFF6FF; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
    
    <!-- Logo Left -->
    <a href="/" style="display: flex; align-items: center; gap: 10px; text-decoration: none;">
        <img src="/static/khary-profile.jpg" style="width: 55px; height: 55px; border-radius: 50%; border: 2px solid #D4AF37;">
        <span style="font-size: 1.2rem; font-weight: bold; color: #1E3A8A;">KHARY<span style="color: #D4AF37;">GLOBAL</span> EDU</span>
    </a>
    
    <!-- Navbar Links - Simple Text -->
    <div style="display: flex; gap: 15px; flex-wrap: wrap; align-items: center;">
        <a href="/" style="color: #1E3A8A; text-decoration: none; font-size: 0.85rem;">Home</a>
        <a href="#destinations" style="color: #1E3A8A; text-decoration: none; font-size: 0.85rem;">Destinations</a>
        <a href="#mission" style="color: #1E3A8A; text-decoration: none; font-size: 0.85rem;">Our Story</a>
        <a href="/compare" style="color: #1E3A8A; text-decoration: none; font-size: 0.85rem;">Compare</a>
        <a href="/blog" style="color: #1E3A8A; text-decoration: none; font-size: 0.85rem;">Blog</a>
        <a href="/foundation" style="color: #1E3A8A; text-decoration: none; font-size: 0.85rem;">Foundation</a>
        <a href="/csca" style="color: #1E3A8A; text-decoration: none; font-size: 0.85rem;">CSCA Exam</a>
        <a href="/media" style="color: #1E3A8A; text-decoration: none; font-size: 0.85rem;">Media</a>
    </div>
    
     <!-- Language Switcher -->
<div style="position: relative; margin-left: 20px;">
    <button id="langBtn" onclick="toggleLangMenu()" style="background: #1E3A8A; color: white; border: none; padding: 8px 18px; border-radius: 30px; cursor: pointer;">
        🌐 English
    </button>
    <div id="langMenu" style="position: absolute; top: 45px; right: 0; background: white; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); display: none; z-index: 100; min-width: 150px;">
        <div onclick="setLanguage('en')" style="padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #eee;">🇬🇧 English</div>
        <div onclick="setLanguage('zh')" style="padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #eee;">🇨🇳 中文</div>
        <div onclick="setLanguage('ar')" style="padding: 10px 15px; cursor: pointer; border-bottom: 1px solid #eee;">🇸🇦 العربية</div>
        <div onclick="setLanguage('fr')" style="padding: 10px 15px; cursor: pointer;">🇫🇷 Français</div>
    </div>
</div>
    </div>
    <!-- Three Dots Button -->
<div onclick="var m=document.getElementById('dotsMenu'); if(m.style.right=='20px') m.style.right='-260px'; else m.style.right='20px';" style="background: #1E3A8A; width: 35px; height: 35px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; cursor: pointer;">
    <span style="width: 18px; height: 2px; background: white;"></span>
    <span style="width: 18px; height: 2px; background: white;"></span>
    <span style="width: 18px; height: 2px; background: white;"></span>
</div>

<!-- Menu -->
<div id="dotsMenu" style="position: fixed; top: 70px; right: -260px; width: 260px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.15); transition: right 0.3s; z-index: 9999;">
    <a href="/destinations" style="display: block; padding: 14px 20px; color: #1E3A8A; text-decoration: none; border-bottom: 1px solid #eee;">Destinations</a>
    <a href="/programs" style="display: block; padding: 14px 20px; color: #1E3A8A; text-decoration: none; border-bottom: 1px solid #eee;">Programs</a>
    <a href="/scholarships" style="display: block; padding: 14px 20px; color: #1E3A8A; text-decoration: none; border-bottom: 1px solid #eee;">Scholarships</a>
    <a href="/resources" style="display: block; padding: 14px 20px; color: #1E3A8A; text-decoration: none; border-bottom: 1px solid #eee;">Resources</a>
    <a href="/about" style="display: block; padding: 14px 20px; color: #1E3A8A; text-decoration: none; border-bottom: 1px solid #eee;">About</a>
    <a href="/contact" style="display: block; padding: 14px 20px; color: #1E3A8A; text-decoration: none;">Contact</a>
</div>
</nav>
        
    </div>
</nav>

<script>
    fetch('/check-auth')
        .then(r => r.json())
        .then(data => {{
            let links = document.getElementById('authLinks');
            if (links) {{
                if (data.logged_in) {{
                    links.innerHTML = '<a href="/dashboard">Dashboard</a> | <a href="/logout">Logout</a>';
                }} else {{
                    links.innerHTML = '<a href="/login">Login</a> | <a href="/register">Register</a>';
                }}
            }}
        }});
</script>
    <script>
        fetch('/check-auth')
            .then(r => r.json())
            .then(data => {{
                let links = document.getElementById('authLinks');
                if (links) {{
                    if (data.logged_in) {{
                        links.innerHTML = '<a href="/dashboard">Dashboard</a> | <a href="/logout">Logout</a>';
                    }} else {{
                        links.innerHTML = '<a href="/login">Login</a> | <a href="/register">Register</a>';
                    }}
                }}
            }});
    </script>


<section class="hero">
    <div class="container">
        <h1>From Dream to Campus:<br>Your Asian Study Journey Starts Here</h1>
        <p>Expert guidance for studying in China, Singapore, Malaysia, Japan, and Korea</p>
        
        <!-- Professional Mission Section -->
        <div class="mission-box" id="mission" style="display: flex; align-items: center; gap: 30px; padding: 30px;">
            
            <div>
                <h3 style="color: #1E3A8A; margin-bottom: 15px; font-size: 28px;">Our Mission</h3>
                <p style="font-style: italic; line-height: 1.8;">"My name is Khary. For years, I watched talented students give up on studying abroad because the process felt overwhelming. Paperwork, applications, visas—it seemed too confusing. So I started KHARY GLOBAL EDU with one mission: to walk with you, step-by-step, from your first question to your first day in class overseas. This isn't just business—it's personal."</p>
            </div>
        </div>
    </div>
</section>     
                
                    <div class="stat-item">
                
                        <span class=<
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--dark-gray);
            background: var(--light-blue);
        }}
        
        .navbar {{
            background: var(--white);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary-blue);
            text-decoration: none;
        }}
        
        .logo span {{
            color: var(--accent-gold);
        }}
        
        .nav-links {{
            display: flex;
            gap: 2rem;
            align-items: center;
        }}
        
        .nav-links a {{
            color: var(--dark-gray);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}
        
        .nav-links a:hover {{
            color: var(--primary-blue);
        }}
        
        .nav-links .cta {{
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.5rem 1.5rem;
            border-radius: 5px;
        }}
        
        .hero {{
            background: linear-gradient(135deg, var(--light-blue), var(--white));
            padding: 4rem 0;
            text-align: center;
        }}
        
        .hero h1 {{
            font-size: 3rem;
            color: var(--primary-blue);
            margin-bottom: 1.5rem;
        }}
        
        .hero p {{
            font-size: 1.2rem;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .mission-box {{
            background: var(--white);
            padding: 3rem;
            border-radius: 20px;
            box-shadow: var(--shadow);
            border-left: 5px solid var(--accent-gold);
            margin: 3rem auto;
            max-width: 900px;
            font-style: italic;
        }}
        
        .mission-box h3 {{
            color: var(--primary-blue);
            margin-bottom: 1rem;
            font-style: normal;
            font-size: 2rem;
        }}
        
        .countries-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            padding: 3rem 0;
        }}
        
        .country-card {{
            background: var(--white);
            padding: 2rem 1rem;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: var(--shadow);
        }}
        
        .country-card:hover {{
            transform: translateY(-10px);
            box-shadow: var(--hover-shadow);
        }}
        
        .country-card .flag {{
            font-size: 4rem;
            margin-bottom: 1rem;
        }}
        
        .country-card h3 {{
            color: var(--primary-blue);
            margin-bottom: 0.5rem;
            font-size: 1.5rem;
        }}
        
        .country-card p {{
            color: var(--accent-gold);
            font-weight: bold;
        }}
        
        .university-page {{
            padding: 2rem 0;
        }}
        
        .university-header {{
            background: linear-gradient(135deg, var(--primary-blue), #2D4FA8);
            color: white;
            padding: 4rem 0;
            margin-bottom: 3rem;
            text-align: center;
        }}
        
        .university-header h1 {{
            font-size: 3.5rem;
            margin-bottom: 1rem;
            color: white;
        }}
        
        .university-header .flag {{
            font-size: 5rem;
            margin-bottom: 1rem;
        }}
        
        .university-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }}
        
        .university-card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: transform 0.3s;
        }}
        
        .university-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--hover-shadow);
        }}
        
        .university-card-header {{
            background: var(--primary-blue);
            color: white;
            padding: 1.5rem;
            position: relative;
        }}
        
        .university-card-header h3 {{
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            color: white;
        }}
        
        .university-card-header .ranking {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: var(--accent-gold);
            color: var(--primary-blue);
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-weight: bold;
        }}
        
        .university-card-body {{
            padding: 2rem;
        }}
        
        .info-item {{
            margin: 1rem 0;
            padding: 1rem;
            background: var(--light-blue);
            border-radius: 10px;
        }}
        
        .program-section {{
            margin: 1.5rem 0;
        }}
        
        .program-section h4 {{
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }}
        
        .program-tag {{
            display: inline-block;
            background: var(--light-blue);
            color: var(--primary-blue);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            margin: 0.3rem;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .program-tag:hover {{
            background: var(--primary-blue);
            color: white;
        }}
        
        .scholarship-item {{
            background: var(--accent-gold);
            color: var(--primary-blue);
            padding: 0.8rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            font-weight: 500;
        }}
        
        .btn {{
            display: inline-block;
            padding: 0.8rem 2rem;
            background: var(--primary-blue);
            color: var(--white);
            text-decoration: none;
            border-radius: 5px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            width: 100%;
            text-align: center;
        }}
        
        .btn:hover {{
            background: var(--accent-gold);
            color: var(--primary-blue);
            transform: translateY(-2px);
        }}
        
        .btn-gold {{
            background: var(--accent-gold);
            color: var(--primary-blue);
        }}
        
        .back-button {{
            display: inline-block;
            margin: 1rem 0 2rem;
            padding: 0.8rem 2rem;
            background: var(--light-blue);
            color: var(--primary-blue);
            text-decoration: none;
            border-radius: 5px;
            cursor: pointer;
            border: none;
            font-weight: bold;
        }}
        
        .modal {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }}
        
        .modal-content {{
            background: white;
            padding: 2.5rem;
            border-radius: 20px;
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
        }}
        
        .modal-content h2 {{
            color: var(--primary-blue);
            margin-bottom: 1.5rem;
        }}
        
        .modal-content input,
        .modal-content select,
        .modal-content textarea,
        .modal-content input[type="file"] {{
            width: 100%;
            padding: 0.8rem;
            margin: 0.5rem 0 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            transition: border 0.3s;
        }}
        
        .modal-content input:focus,
        .modal-content select:focus,
        .modal-content textarea:focus {{
            border-color: var(--primary-blue);
            outline: none;
        }}
        
        .modal-content label {{
            font-weight: bold;
            color: var(--primary-blue);
            display: block;
        }}
        
        .modal-buttons {{
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
        }}
        
        .footer {{
            background: var(--dark-gray);
            color: var(--white);
            padding: 3rem 0;
            text-align: center;
            margin-top: 4rem;"stat-label"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>


    <section class="destinations" id="destinations">
        <div class="container">
            <h2 style="text-align:center; color:var(--primary-blue); font-size:2.5rem; margin-bottom:2rem;">Study Destinations</h2>
            <div class="countries-grid">
                <div class="country-card" onclick="showCountryUniversities('china', '🇨🇳 China')">
                    <div class="flag">🇨🇳</div>
                    <h3>China</h3>
                    <p>{len(china_universities)}+ Top Universities</p>
                </div>
                <div class="country-card" onclick="showCountryUniversities('singapore', '🇸🇬 Singapore')">
                    <div class="flag">🇸🇬</div>
                    <h3>Singapore</h3>
                    <p>{len(singapore_universities)}+ Top Universities</p>
                </div>
                <div class="country-card" onclick="showCountryUniversities('malaysia', '🇲🇾 Malaysia')">
                    <div class="flag">🇲🇾</div>
                    <h3>Malaysia</h3>
                    <p>{len(malaysia_universities)}+ Top Universities</p>
                </div>
                <div class="country-card" onclick="showCountryUniversities('japan', '🇯🇵 Japan')">
                    <div class="flag">🇯🇵</div>
                    <h3>Japan</h3>
                    <p>{len(japan_universities)}+ Top Universities</p>
                </div>
                <div class="country-card" onclick="showCountryUniversities('korea', '🇰🇷 Korea')">
                    <div class="flag">🇰🇷</div>
                    <h3>Korea</h3>
                    <p>{len(korea_universities)}+ Top Universities</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="footer">
    <div class="container">
        <!-- Footer Top with Stats -->
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 30px; margin-bottom: 40px; padding-bottom: 30px; border-bottom: 2px solid rgba(212, 175, 55, 0.3);">
            <div style="display: flex; gap: 40px; flex-wrap: wrap;">
                <div style="text-align: center;">
                    <span style="display: block; font-size: 32px; font-weight: bold; color: #D4AF37; line-height: 1.2;">150+</span>
                    <span style="font-size: 14px; letter-spacing: 1px; text-transform: uppercase;">Partner Universities</span>
                </div>
                <div style="text-align: center;">
                    <span style="display: block; font-size: 32px; font-weight: bold; color: #D4AF37; line-height: 1.2;">5</span>
                    <span style="font-size: 14px; letter-spacing: 1px; text-transform: uppercase;">Asian Countries</span>
                </div>
                <div style="text-align: center;">
                    <span style="display: block; font-size: 32px; font-weight: bold; color: #D4AF37; line-height: 1.2;">1000+</span>
                    <span style="font-size: 14px; letter-spacing: 1px; text-transform: uppercase;">Students Placed</span>
                </div>
            </div>
            
            <!-- Brand -->
            <div style="text-align: right;">
                <span style="font-size: 24px; font-weight: bold; color: white;">KHARY<span style="color: #D4AF37;">GLOBAL</span></span>
                <p style="font-size: 12px; opacity: 0.7;">Education Without Borders</p>
            </div>
        </div>
        
        <!-- Contact Information Cards -->
        <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; margin-bottom: 40px;">
            <!-- Phone Card -->
            <div style="background: rgba(255,255,255,0.05); padding: 20px 30px; border-radius: 10px; display: flex; align-items: center; gap: 15px; border: 1px solid rgba(212, 175, 55, 0.2); flex: 1; min-width: 250px;">
                <span style="font-size: 28px; background: #D4AF37; color: #1E3A8A; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; border-radius: 50%;">📞</span>
                <div>
                    <p style="font-size: 12px; opacity: 0.7; margin-bottom: 5px;">CALL US</p>
                    <a href="tel:+8613522464910" style="color: white; font-weight: bold; font-size: 16px; text-decoration: none; transition: color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='white'">+86 135 2246 4910</a>
                </div>
            </div>
            
            <!-- Email Card (ACTIVE) -->
            <div style="background: rgba(255,255,255,0.05); padding: 20px 30px; border-radius: 10px; display: flex; align-items: center; gap: 15px; border: 1px solid rgba(212, 175, 55, 0.2); flex: 1; min-width: 250px;">
                <span style="font-size: 28px; background: #D4AF37; color: #1E3A8A; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; border-radius: 50%;">✉️</span>
                <div>
                    <p style="font-size: 12px; opacity: 0.7; margin-bottom: 5px;">EMAIL US</p>
                    <a href="mailto:kharyglobal@gmail.com" style="color: white; font-weight: bold; font-size: 16px; text-decoration: none; transition: color 0.3s;" onmouseover="this.style.color='#D4AF37'" onmouseout="this.style.color='white'">kharyglobal@gmail.com</a>
                </div>
            </div>
            
           
    <a href="https://wa.me/message/WUOFMPEEXHVQJ1" target="_blank" rel="noopener noreferrer" style="text-decoration: none;">
                <div style="background: rgba(255,255,255,0.1); padding: 20px 30px; border-radius: 12px; display: flex; align-items: center; gap: 15px; border: 1px solid rgba(212, 175, 55, 0.3);">
                    <span style="font-size: 28px; background: #25D366; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; border-radius: 50%;">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                            <path d="M16.75 13.96c-.25-.13-1.47-.71-1.7-.79-.23-.08-.4-.12-.57.12-.17.24-.66.79-.81.95-.15.16-.3.18-.55.06-.25-.12-1.05-.38-2-1.23-.74-.66-1.24-1.47-1.38-1.72-.15-.25-.02-.38.11-.51.11-.11.25-.29.37-.44.12-.15.17-.25.25-.42.08-.17.04-.31-.02-.44-.06-.13-.57-1.36-.78-1.86-.2-.49-.41-.42-.56-.43-.14-.01-.31-.01-.47-.01-.17 0-.44.06-.67.31-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.01 2.56.12.16 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.08.15-1.19-.07-.11-.25-.18-.5-.31z"/>
                            <path d="M12 2C6.48 2 2 6.48 2 12c0 2.1.66 4.06 1.79 5.69L2.15 21.35c-.12.31.12.65.46.59l3.55-.59c1.63 1.13 3.59 1.79 5.69 1.79 5.52 0 10-4.48 10-10S17.52 2 12 2zm0 18c-1.76 0-3.39-.48-4.79-1.3l-3.44.57.57-3.44C3.48 15.39 3 13.76 3 12c0-4.97 4.03-9 9-9s9 4.03 9 9-4.03 9-9 9z"/>
                        </svg>
                    </span>
                    <div>
                        <p style="font-size: 12px; opacity: 0.7; margin-bottom: 5px; color: white;">WHATSAPP</p>
                        <p style="font-weight: bold; font-size: 16px; color: white;">Click to Chat</p>
                    </div>
                </div>
            </a>
    
    </a>
</div>
        
        <!-- Social Media Section (all ACTIVE) -->
        <div style="text-align: center; margin-bottom: 30px;">
            <h3 style="color: #D4AF37; font-size: 24px; margin-bottom: 25px; letter-spacing: 2px; position: relative;">
                FOLLOW US ON
                <span style="display: block; width: 80px; height: 3px; background: #D4AF37; margin: 10px auto 0;"></span>
            </h3>
            
            <div style="display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; margin-bottom: 20px;">
    <!-- Facebook -->
    <a href="https://www.facebook.com/profile.php?id=61586997059215" target="_blank" style="text-decoration: none; color: white;">
        <div style="background: #1877F2; padding: 12px 30px; border-radius: 50px; display: flex; align-items: center; gap: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)';" onmouseout="this.style.transform='translateY(0)';">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M22 12C22 6.48 17.52 2 12 2S2 6.48 2 12c0 5.08 3.64 9.28 8.41 10.06v-7.12H7.9V12h2.51V9.8c0-2.48 1.48-3.85 3.74-3.85 1.08 0 2.22.19 2.22.19v2.44h-1.25c-1.23 0-1.61.76-1.61 1.55V12h2.74l-.44 2.94h-2.3v7.12C18.36 21.28 22 17.08 22 12z"/>
            </svg>
            <span style="font-weight: bold;">Khary Global Edu</span>
        </div>
    </a>
    
    <!-- Twitter/X -->
    <a href="https://twitter.com/kharyglobal_edu" target="_blank" style="text-decoration: none; color: white;">
        <div style="background: #000000; padding: 12px 30px; border-radius: 50px; display: flex; align-items: center; gap: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)';" onmouseout="this.style.transform='translateY(0)';">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
            </svg>
            <span style="font-weight: bold;">@kharyglobal_edu</span>
        </div>
    </a>
</div>

<!-- TikTok, YouTube, LinkedIn, Instagram Row -->
<div style="display: flex; justify-content: center; gap: 25px; flex-wrap: wrap;">
    <!-- TikTok -->
    <a href="https://tiktok.me/khary_global_edu8" target="_blank" style="text-decoration: none; color: white;">
        <div style="background: #000000; padding: 12px 35px; border-radius: 50px; display: flex; align-items: center; gap: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)';" onmouseout="this.style.transform='translateY(0)';">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64 2.93 2.93 0 0 1 1.18.24V9.47a6.32 6.32 0 0 0-5.42.27 6.3 6.3 0 0 0-3.05 5.04 6.3 6.3 0 0 0 2.78 6.11 6.3 6.3 0 0 0 7.9-.47 6.3 6.3 0 0 0 2.13-4.7V8.34a8.56 8.56 0 0 0 4.46 1.22V6.44a4.85 4.85 0 0 1-2.84-.9z"/>
            </svg>
            <span style="font-weight: bold;">kharyglobal_edu8</span>
        </div>
    </a>
    
    <!-- YouTube -->
    <a href="https://youtube.com/@kharyglobal_edu" target="_blank" style="text-decoration: none; color: white;">
        <div style="background: #FF0000; padding: 12px 30px; border-radius: 50px; display: flex; align-items: center; gap: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)';" onmouseout="this.style.transform='translateY(0)';">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.376.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.376-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
            <span style="font-weight: bold;">Khary Global Edu</span>
        </div>
    </a>
    
    <!-- LinkedIn -->
    <a href="https://linkedin.com/company/khary-global-edu" target="_blank" style="text-decoration: none; color: white;">
        <div style="background: #0077B5; padding: 12px 30px; border-radius: 50px; display: flex; align-items: center; gap: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)';" onmouseout="this.style.transform='translateY(0)';">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451c.979 0 1.771-.773 1.771-1.729V1.729C24 .774 23.204 0 22.225 0z"/>
            </svg>
            <span style="font-weight: bold;">Khary Global Edu</span>
        </div>
    </a>
    
    <!-- Instagram -->
    <a href="https://instagram.com/kharyglobal_edu" target="_blank" style="text-decoration: none; color: white;">
        <div style="background: linear-gradient(45deg, #f09433, #d62976, #962fbf, #4f5bd5); padding: 12px 30px; border-radius: 50px; display: flex; align-items: center; gap: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.3); transition: transform 0.3s;" onmouseover="this.style.transform='translateY(-5px)';" onmouseout="this.style.transform='translateY(0)';">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 1.366.062 2.633.336 3.608 1.311.975.975 1.249 2.242 1.311 3.608.058 1.266.07 1.646.07 4.85s-.012 3.584-.07 4.85c-.062 1.366-.336 2.633-1.311 3.608-.975.975-2.242 1.249-3.608 1.311-1.266.058-1.646.07-4.85.07s-3.584-.012-4.85-.07c-1.366-.062-2.633-.336-3.608-1.311-.975-.975-1.249-2.242-1.311-3.608-.058-1.266-.07-1.646-.07-4.85s.012-3.584.07-4.85c.062-1.366.336-2.633 1.311-3.608.975-.975 2.242-1.249 3.608-1.311 1.266-.058 1.646-.07 4.85-.07zm0-2.163C8.716 0 8.292.014 6.98.072 5.669.13 4.664.425 3.773 1.316 2.882 2.207 2.587 3.212 2.53 4.523 2.472 5.835 2.458 6.259 2.458 12s.014 6.165.072 7.477c.057 1.311.352 2.316 1.243 3.207.891.891 1.896 1.186 3.207 1.243 1.312.058 1.736.072 7.477.072s6.165-.014 7.477-.072c1.311-.057 2.316-.352 3.207-1.243.891-.891 1.186-1.896 1.243-3.207.058-1.312.072-1.736.072-7.477s-.014-6.165-.072-7.477c-.057-1.311-.352-2.316-1.243-3.207-.891-.891-1.896-1.186-3.207-1.243C15.708.014 15.284 0 12 0z"/>
                <path d="M12 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zm0 10.162a4 4 0 1 1 0-8 4 4 0 0 1 0 8z"/>
                <circle cx="18.406" cy="5.594" r="1.44"/>
            </svg>
            <span style="font-weight: bold;">@kharyglobal_edu</span>
        </div>
    </a>
</div>
           
               
        </div>
        
        <!-- Footer Bottom with Active Email Link -->
        <p style="font-size: 16px; font-weight: 300; letter-spacing: 1px; margin-bottom: 10px;">© {current_year} KHARY GLOBAL EDU. All rights reserved.</p>
<p style="font-size: 14px; opacity: 0.8;">Planting Dreams in Asian Soil, Watching Futures Bloom — One Heart at a Time</p>
<p style="font-size: 12px; opacity: 0.5; margin-top: 20px;">Crafted with 💛 for every dreamer, wrapped in 🤍 for the journey, nurtured with 🌱 for what's to come</p>
        </div>
    </div>
</footer>

    <script>
        // University data loaded from server
        const universityData = {{
            china: {china_json},
            singapore: {singapore_json},
            malaysia: {malaysia_json},
            japan: {japan_json},
            korea: {korea_json}
        }};

        function showCountryUniversities(country, countryName) {{
            const universities = universityData[country];
            if (!universities || universities.length === 0) {{
                alert('No universities found for ' + countryName);
                return;
            }}
            
            // Clear the page
            document.body.innerHTML = '';
            
            // Create header
            let html = '<div class="university-header">' +
                '<div class="container">' +
                '<div class="flag">' + countryName.split(' ')[0] + '</div>' +
                '<h1>Study in ' + countryName.split(' ')[1] + '</h1>' +
                '<p>' + universities.length + ' Top Universities • Complete Programs • Scholarship Opportunities</p>' +
                '</div></div>';
            
            // Add to body
            document.body.innerHTML = html;
            
            // Create container
            let containerHtml = '<div class="container">' +
                '<button class="back-button" onclick="location.reload()">← Back to Home</button>' +
                '<div class="university-grid">';
            
            // Add universities
            for(let i = 0; i < universities.length; i++) {{
                let uni = universities[i];
                containerHtml += '<div class="university-card">' +
                    '<div class="university-card-header">' +
                    '<h3>' + uni.name + '</h3>' +
                    '<div class="ranking">' + uni.ranking + '</div>' +
                    '</div>' +
                    '<div class="university-card-body">' +
                    '<div class="info-item"><strong>📍 Location:</strong> ' + uni.location + '</div>' +
                    '<div class="info-item"><strong>📅 Established:</strong> ' + uni.established + '</div>' +
                    '<div class="info-item"><strong>👥 Students:</strong> ' + uni.students + '</div>' +
                    '<p><em>' + uni.description + '</em></p>' +
                    '<div class="program-section"><h4>📚 Undergraduate Programs</h4>';
                
                // Add undergraduate programs
                if (uni.programs && uni.programs.undergraduate) {{
                    for(let j = 0; j < uni.programs.undergraduate.length; j++) {{
                        containerHtml += '<span class="program-tag">' + uni.programs.undergraduate[j] + '</span>';
                    }}
                }}
                
                containerHtml += '</div><div class="program-section"><h4>🎓 Graduate Programs</h4>';
                
                // Add graduate programs
                if (uni.programs && uni.programs.graduate) {{
                    for(let j = 0; j < uni.programs.graduate.length; j++) {{
                        containerHtml += '<span class="program-tag">' + uni.programs.graduate[j] + '</span>';
                    }}
                }}
                
                containerHtml += '</div><div class="info-item"><strong>💰 Tuition:</strong> ' + uni.fees.undergraduate + '</div>';
                
                // Add scholarships
                if (uni.scholarships && uni.scholarships.length > 0) {{
                    containerHtml += '<div class="program-section"><h4>✨ Scholarships</h4>';
                    for(let j = 0; j < Math.min(uni.scholarships.length, 3); j++) {{
                        let s = uni.scholarships[j];
                        containerHtml += '<div class="scholarship-item">🏆 ' + s.name + ' - ' + s.coverage + '</div>';
                    }}
                    containerHtml += '</div>';
                }}
                
                containerHtml += '<button class="btn" onclick="showApplication(\\'' + uni.name.replace(/'/g, "\\\\'") + '\\', \\'' + countryName.split(' ')[1] + '\\')">Apply Now</button>' +
                    '</div></div>';
            }}
            
            containerHtml += '</div></div>';
            
            // Add to body
            document.body.innerHTML += containerHtml;
            
            // Add footer
            let footerHtml = '<footer class="footer">' +
                '<div class="container">' +
                '<p>© 2024 KHARY GLOBAL EDU. All rights reserved.</p>' +
                '<p>Study Abroad Guidance for Asian Universities</p>' +
                '</div></footer>';
            
            document.body.innerHTML += footerHtml;
        }}

        function showApplication(university, country) {{
            let modalHtml = '<div class="modal">' +
                '<div class="modal-content">' +
                '<h2>Apply to ' + university + '</h2>' +
                '<form id="applicationForm" enctype="multipart/form-data">' +
                '<label>Full Name *</label>' +
                '<input type="text" id="name" required>' +
                '<label>Email *</label>' +
                '<input type="email" id="email" required>' +
                '<label>Phone/WhatsApp *</label>' +
                '<input type="tel" id="phone" required>' +
                '<label>Program Level *</label>' +
                '<select id="program_level" required>' +
                '<option value="Undergraduate">Undergraduate</option>' +
                '<option value="Graduate">Graduate</option>' +
                '<option value="PhD">PhD</option>' +
                '<option value="Language">Language Course</option>' +
                '</select>' +
                '<label>Preferred Program</label>' +
                '<input type="text" id="preferred_program">' +
                '<label>📎 Upload Documents (PDF, DOC, JPG)</label>' +
                '<input type="file" id="documents" name="documents" multiple accept=".pdf,.doc,.docx,.jpg,.jpeg,.png" style="padding: 10px; border: 2px dashed var(--primary-blue); width: 100%;">' +
                '<p style="font-size: 0.9rem; color: var(--primary-blue); margin-top: 5px; margin-bottom: 15px;">📎 You can select multiple files (hold Ctrl/Cmd to select multiple)</p>' +
                '<label>Message/Questions</label>' +
                '<textarea id="message" rows="3"></textarea>' +
                '<div class="modal-buttons">' +
                '<button type="button" class="btn" onclick="submitApplication(\\'' + university.replace(/'/g, "\\\\'") + '\\', \\'' + country + '\\')">Submit Application</button>' +
                '<button type="button" class="btn" onclick="this.closest(\\'.modal\\').remove()" style="background:#ccc;">Close</button>' +
                '</div>' +
                '</form>' +
                '</div>' +
                '</div>';
            
            document.body.insertAdjacentHTML('beforeend', modalHtml);
        }}

        function submitApplication(university, country) {{
            event.preventDefault();
            
            const formData = new FormData();
            formData.append('university', university);
            formData.append('country', country);
            formData.append('student_name', document.getElementById('name').value);
            formData.append('student_email', document.getElementById('email').value);
            formData.append('student_phone', document.getElementById('phone').value);
            formData.append('program_level', document.getElementById('program_level').value);
            formData.append('preferred_program', document.getElementById('preferred_program').value);
            formData.append('message', document.getElementById('message').value);
            
            const files = document.getElementById('documents').files;
            for (let i = 0; i < files.length; i++) {{
                formData.append('documents', files[i]);
            }}
            
            fetch('/submit-application-with-files', {{
                method: 'POST',
                body: formData
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    alert('✅ Thank you for applying to ' + university + '! We will contact you within 24 hours.');
                    document.querySelector('.modal').remove();
                }} else {{
                    alert('❌ Error: ' + data.message);
                }}
            }})
            .catch(error => {{
                alert('❌ Network error. Please try again.');
            }});
        }}
    </script>

</div>
               
<script src="/static/whatsapp.js"></script>
<script src="/static/languages.js"></script> 

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<meta name="description" content="KHARY GLOBAL EDU - Study in Asia. Expert guidance for studying in China, Singapore, Malaysia, Japan, and Korea. Scholarship assistance, visa support, and admission processing.">
<meta name="keywords" content="study abroad, study in China, study in Singapore, study in Malaysia, study in Japan, study in Korea, scholarship, CSC scholarship, KGSP scholarship, MEXT scholarship">
<meta name="author" content="KHARY GLOBAL EDU">
<meta name="robots" content="index, follow">
<meta property="og:title" content="KHARY GLOBAL EDU - Study Abroad Guidance for Asian Universities">
<meta property="og:description" content="Walk with you, step-by-step, from your first question to your first day in class overseas.">
<meta property="og:image" content="/static/khary-profile.jpg">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="KHARY GLOBAL EDU">
<meta name="twitter:description" content="Study Abroad Guidance for Asian Universities">
<link rel="canonical" href="https://kharyglobaledu.com">

<div id="newsletterModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 10000; justify-content: center; align-items: center;">
    <div style="background: white; padding: 30px; border-radius: 20px; max-width: 450px; text-align: center; margin: 20px;">
        <i class="fas fa-bell" style="font-size: 50px; color: #D4AF37;"></i>
        <h2 style="color: #1E3A8A; margin: 15px 0;">Get Scholarship Alerts</h2>
        <p>Subscribe to receive deadline reminders and scholarship opportunities</p>
        <form id="floatingNewsletterForm">
            <input type="email" id="floatingEmail" placeholder="Your email address" required style="width: 100%; padding: 12px; border: 2px solid #E2E8F0; border-radius: 8px; margin-bottom: 15px;">
            <button type="submit" style="background: #1E3A8A; color: white; padding: 12px 25px; border: none; border-radius: 8px; cursor: pointer; width: 100%;">Subscribe Now</button>
        </form>
        <button onclick="closeNewsletter()" style="margin-top: 15px; background: none; border: none; color: #666; cursor: pointer;">Close</button>
    </div>
</div>

<div style="position: fixed; bottom: 80px; left: 20px; z-index: 999;">
    <button onclick="openNewsletter()" style="background: #D4AF37; color: #1E3A8A; border: none; padding: 12px 20px; border-radius: 50px; cursor: pointer; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
        <i class="fas fa-envelope"></i> Get Updates
    </button>
</div>

<script src="/static/livechat.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/newsletter.js"></script>
<script src="/static/security.js"></script>
<script src="/static/mobile-bottom-menu.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/whatsapp-popup.js"></script>


</body>
</html>
    '''


# ==================== HEALTH CHECK ====================
@app.route('/health')
def health_check():
    """Simple health check endpoint for monitoring"""
    try:
        # Check database connection
        db_status = "healthy"
        try:
            conn = sqlite3.connect('applications.db')
            c = conn.cursor()
            c.execute("SELECT 1")
            conn.close()
        except:
            db_status = "unhealthy"
        
        # Check uploads folder
        uploads_status = "healthy" if os.path.exists(UPLOAD_FOLDER) else "unhealthy"
        
        # Return health status
        return jsonify({
            'status': 'healthy',
            'service': 'KHARY GLOBAL EDU',
            'time': datetime.now().isoformat(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'environment': {
                'database': db_status,
                'uploads_folder': uploads_status,
                'email_configured': bool(app.config.get('MAIL_USERNAME'))
            },
            'version': '1.0.0',
            'endpoints': [
                '/',
                '/khary-global-edu',
                '/api/universities/<country>',
                '/health'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'time': datetime.now().isoformat()
        }), 500
    # ==================== ROBOTS.TXT ====================
@app.route('/robots.txt')
def robots():
    """Robots.txt file for search engines - controls what gets indexed"""
    # Get current date for last updated
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Build the robots.txt content
    robots_txt = f"""# robots.txt for KHARY GLOBAL EDU
# Created: {current_date}
# This file tells search engines which parts of the site to crawl

# ----------------------------------------------------------------------
# MAIN RULES
# ----------------------------------------------------------------------

# Apply to all search engines (Google, Bing, Yahoo, etc.)
User-agent: *

# ----------------------------------------------------------------------
# DISALLOWED PATHS (Private/Admin areas)
# ----------------------------------------------------------------------

# Admin panel - don't show in search results
Disallow: /khary-global-edu
Disallow: /admin

# Application submission endpoints (don't need indexing)
Disallow: /submit-application
Disallow: /submit-application-with-files

# API endpoints (not for search engines)
Disallow: /api/
Disallow: /update-application-status
Disallow: /delete-application
Disallow: /export-applications

# ----------------------------------------------------------------------
# ALLOWED PATHS (Public content)
# ----------------------------------------------------------------------

# Allow everything else (main site content)
Allow: /$
Allow: /$

# ----------------------------------------------------------------------
# CRAWL DELAY (Be nice to our server)
# ----------------------------------------------------------------------

# Wait 5 seconds between requests (helps with server load)
Crawl-delay: 5

# ----------------------------------------------------------------------
# SITEMAP (Helps search engines find all pages)
# ----------------------------------------------------------------------

# Sitemap location (create this later for better SEO)
# Sitemap: https://kharyglobaledu.com/sitemap.xml

# ----------------------------------------------------------------------
# SPECIFIC BOT RULES
# ----------------------------------------------------------------------

# Google-specific rules
User-agent: Googlebot
Allow: /
Disallow: /khary-global-edu
Disallow: /admin

# Bing-specific rules
User-agent: bingbot
Allow: /
Disallow: /khary-global-edu
Disallow: /admin

# ----------------------------------------------------------------------
# NOTES
# ----------------------------------------------------------------------
# This file helps search engines understand our site structure
# Last reviewed: {current_date}
# Contact: admin@kharyglobaledu.com
"""
    
    return robots_txt, 200, {'Content-Type': 'text/plain'}

@app.errorhandler(404)
def page_not_found(e):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Page Not Found - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 35px; background: #EFF6FF; }
            h1 { color: #1E3A8A; }
            .btn { display: inline-block; padding: 10px 20px; background: #1E3A8A; color: white; text-decoration: none; border-radius: 5px; }
            a[href="/khary-global-edu"] { display: none !important; }
        </style>
    </head>
    <body>
    
        
        <script src="/static/main-menu.js"></script>
        <script src="/static/chatbot.js"></script>
        <script src="/static/livechat.js"></script>
        <script src="/static/whatsapp-popup.js"></script>
        <script src="/static/subscribe.js"></script>
        <script src="/static/mobile.js"></script>
    </body>
    </html>
    """, 404

@app.route('/debug-static')
def debug_static():
    import os
    static_path = os.path.join(os.getcwd(), 'static')
    files = os.listdir(static_path) if os.path.exists(static_path) else []
    return f"""
    <h1>Static Folder Debug</h1>
    <p>Static folder path: {static_path}</p>
    <p>Static folder exists: {os.path.exists(static_path)}</p>
    <p>Files in static folder:</p>
    <ul>
        {''.join([f'<li>{file}</li>' for file in files])}
    </ul>
    <p>Try accessing:</p>
    <ul>
        {''.join([f'<li><a href="/static/{file}">/static/{file}</a></li>' for file in files])}
    </ul>
    """

@app.errorhandler(500)
def internal_server_error(e):
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Server Error - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #EFF6FF; }
            h1 { color: #1E3A8A; }
            .btn { display: inline-block; padding: 10px 20px; background: #1E3A8A; color: white; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <h1>500 - Internal Server Error</h1>
        <p>Something went wrong. Please try again later.</p>
        <a href="/" class="btn">Go to Homepage</a>
    
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    """, 500

@app.route('/foundation')
@login_required
def foundation():
    return render_template('foundation.html')

@app.route('/csca')
@login_required
def csca():
    return render_template('csca.html')


# ==================== API FOR ADMIN ====================
@app.route('/api/admin/applications')
@admin_required
def api_admin_applications():
    """Get all applications for admin panel"""
    try:
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        c.execute('''SELECT id, country, university, student_name, student_email, student_phone, 
                     program_level, preferred_program, message, application_date, status 
                     FROM applications ORDER BY application_date DESC''')
        apps = c.fetchall()
        conn.close()
        
        applications = []
        for app in apps:
            applications.append({
                'id': app[0],
                'country': app[1],
                'university': app[2],
                'student_name': app[3],
                'student_email': app[4],
                'student_phone': app[5],
                'program_level': app[6],
                'preferred_program': app[7],
                'message': app[8],
                'application_date': app[9],
                'status': app[10] if len(app) > 10 else 'new'
            })
        
        return jsonify({'success': True, 'applications': applications})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== NEW PAGES ====================



@app.route('/undergraduate')
@login_required
def undergraduate():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Undergraduate Programs - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #EFF6FF; }
            .container { max-width: 1400px; margin: 0 auto; padding: 30px 20px; }
            .header { background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 50px 0; text-align: center; border-radius: 20px; margin-bottom: 40px; }
            .header h1 { font-size: 42px; margin-bottom: 15px; }
            .header p { font-size: 18px; opacity: 0.9; }
            .stats { display: flex; justify-content: center; gap: 40px; margin-top: 30px; flex-wrap: wrap; }
            .stat { text-align: center; background: rgba(255,255,255,0.2); padding: 15px 25px; border-radius: 15px; }
            .stat-number { font-size: 32px; font-weight: bold; color: #D4AF37; }
            .stat-label { font-size: 14px; }
            
            .category-section { margin-bottom: 50px; }
            .category-title { font-size: 28px; color: #1E3A8A; margin-bottom: 25px; border-left: 5px solid #D4AF37; padding-left: 20px; }
            .programs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }
            .program-card { background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.1); transition: transform 0.3s; }
            .program-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.15); }
            .program-header { background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 20px; }
            .program-header h3 { font-size: 18px; margin-bottom: 5px; }
            .program-icon { font-size: 35px; margin-bottom: 10px; }
            .program-body { padding: 20px; }
            .uni-list { margin: 15px 0; }
            .uni-tag { display: inline-block; background: #EFF6FF; color: #1E3A8A; padding: 5px 12px; border-radius: 20px; font-size: 11px; margin: 3px; }
            .duration { color: #D4AF37; font-weight: bold; margin: 10px 0; font-size: 13px; }
            .fee { color: #1E3A8A; font-weight: bold; font-size: 13px; }
            .back-btn { display: inline-block; background: #1E3A8A; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; margin-top: 30px; transition: all 0.3s; }
            .back-btn:hover { background: #D4AF37; color: #1E3A8A; }
            .footer { background: #1F2937; color: white; text-align: center; padding: 30px; margin-top: 50px; border-radius: 20px; }
            .search-box { text-align: center; margin-bottom: 30px; }
            .search-box input { width: 50%; padding: 12px 20px; border: 2px solid #1E3A8A; border-radius: 50px; font-size: 16px; outline: none; }
            .search-box input:focus { border-color: #D4AF37; }
            @media (max-width: 768px) { .programs-grid { grid-template-columns: 1fr; } .search-box input { width: 90%; } }
        </style>
        <script>
            function searchPrograms() {
                let input = document.getElementById('searchInput').value.toLowerCase();
                let cards = document.getElementsByClassName('program-card');
                for(let card of cards) {
                    let text = card.innerText.toLowerCase();
                    if(text.includes(input)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                }
            }
        </script>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-graduation-cap"></i> Undergraduate Programs</h1>
                <p>Bachelor's degrees across Asia's top universities</p>
                <div class="stats">
                    <div class="stat"><div class="stat-number">150+</div><div class="stat-label">Universities</div></div>
                    <div class="stat"><div class="stat-number">100+</div><div class="stat-label">Programs</div></div>
                    <div class="stat"><div class="stat-number">5</div><div class="stat-label">Countries</div></div>
                </div>
            </div>
            
            <div class="search-box">
                <input type="text" id="searchInput" onkeyup="searchPrograms()" placeholder="🔍 Search programs by name, university, or field...">
            </div>
            
            <!-- Engineering & Technology -->
            <div class="category-section">
                <h2 class="category-title"><i class="fas fa-microchip"></i> Engineering & Technology</h2>
                <div class="programs-grid">
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-laptop-code"></i></div><h3>Computer Science</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-robot"></i></div><h3>Artificial Intelligence</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">NTU</span><span class="uni-tag">KAIST</span><span class="uni-tag">Zhejiang</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-microchip"></i></div><h3>Electrical Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $24,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SJTU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-cogs"></i></div><h3>Mechanical Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">NTU</span><span class="uni-tag">Kyoto</span><span class="uni-tag">HIT</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-rocket"></i></div><h3>Aerospace Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Beihang</span><span class="uni-tag">HIT</span><span class="uni-tag">KAIST</span><span class="uni-tag">NTU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-line"></i></div><h3>Data Science</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $28,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">KAIST</span><span class="uni-tag">POSTECH</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-building"></i></div><h3>Civil Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Tongji</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span><span class="uni-tag">HIT</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-flask"></i></div><h3>Chemical Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">Zhejiang</span><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-heartbeat"></i></div><h3>Biomedical Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $25,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-microchip"></i></div><h3>Electronic Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $24,000/year</div><div class="uni-list"><span class="uni-tag">USTC</span><span class="uni-tag">KAIST</span><span class="uni-tag">NTU</span><span class="uni-tag">SJTU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-microchip"></i></div><h3>Telecommunications</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $23,000/year</div><div class="uni-list"><span class="uni-tag">BUPT</span><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-robot"></i></div><h3>Mechatronics Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,200 - $24,000/year</div><div class="uni-list"><span class="uni-tag">KAIST</span><span class="uni-tag">NTU</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">SJTU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-industry"></i></div><h3>Industrial Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">KAIST</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-car"></i></div><h3>Automotive Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,200 - $24,000/year</div><div class="uni-list"><span class="uni-tag">Tongji</span><span class="uni-tag">KAIST</span><span class="uni-tag">HIT</span><span class="uni-tag">NTU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-microchip"></i></div><h3>Semiconductor Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $26,000/year</div><div class="uni-list"><span class="uni-tag">KAIST</span><span class="uni-tag">NUS</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-microchip"></i></div><h3>Nanotechnology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $26,000/year</div><div class="uni-list"><span class="uni-tag">USTC</span><span class="uni-tag">KAIST</span><span class="uni-tag">NUS</span><span class="uni-tag">Tsinghua</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-microchip"></i></div><h3>Software Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,200 - $24,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">NTU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-microchip"></i></div><h3>Information Technology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">SNU</span><span class="uni-tag">NTU</span></div></div></div>
                </div>
            </div>
            
            <!-- Business & Economics -->
            <div class="category-section">
                <h2 class="category-title"><i class="fas fa-chart-line"></i> Business & Economics</h2>
                <div class="programs-grid">
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-building"></i></div><h3>Business Administration</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $30,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">Fudan</span><span class="uni-tag">Yonsei</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-coins"></i></div><h3>Finance</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $32,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">NTU</span><span class="uni-tag">SMU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-globe-asia"></i></div><h3>International Business</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $28,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Fudan</span><span class="uni-tag">Yonsei</span><span class="uni-tag">Keio</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-simple"></i></div><h3>Economics</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span><span class="uni-tag">NUS</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-pie"></i></div><h3>Accounting</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $26,000/year</div><div class="uni-list"><span class="uni-tag">SMU</span><span class="uni-tag">NUS</span><span class="uni-tag">Yonsei</span><span class="uni-tag">Peking</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-store"></i></div><h3>Marketing</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $26,000/year</div><div class="uni-list"><span class="uni-tag">SMU</span><span class="uni-tag">Fudan</span><span class="uni-tag">NTU</span><span class="uni-tag">Waseda</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-line"></i></div><h3>Management</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $28,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span><span class="uni-tag">Fudan</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-line"></i></div><h3>Entrepreneurship</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $30,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span><span class="uni-tag">Yonsei</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-line"></i></div><h3>Supply Chain Management</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,800 - $28,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">NTU</span><span class="uni-tag">Fudan</span><span class="uni-tag">KAIST</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-line"></i></div><h3>Hotel Management</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $28,000/year</div><div class="uni-list"><span class="uni-tag">Kyung Hee</span><span class="uni-tag">NUS</span><span class="uni-tag">Yonsei</span><span class="uni-tag">Fudan</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-line"></i></div><h3>Tourism Management</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Kyung Hee</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">Fudan</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-line"></i></div><h3>Real Estate</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $28,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span><span class="uni-tag">Yonsei</span></div></div></div>
                </div>
            </div>
            
            <!-- Medicine & Health Sciences -->
            <div class="category-section">
                <h2 class="category-title"><i class="fas fa-heartbeat"></i> Medicine & Health Sciences</h2>
                <div class="programs-grid">
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-stethoscope"></i></div><h3>Medicine (MBBS/MD)</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 5-6 yrs | SG/KR/JP: 5-6 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $35,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">Fudan</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-tooth"></i></div><h3>Dentistry</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 5-6 yrs | SG/KR/JP: 5-6 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $38,000/year</div><div class="uni-list"><span class="uni-tag">Sichuan</span><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">Yonsei</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-capsules"></i></div><h3>Pharmacy</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4-5 yrs | SG/KR/JP: 4-5 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $30,000/year</div><div class="uni-list"><span class="uni-tag">Fudan</span><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">Kyoto</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-heart"></i></div><h3>Nursing</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">UM</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-dna"></i></div><h3>Biotechnology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $25,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">USTC</span><span class="uni-tag">NTU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-brain"></i></div><h3>Psychology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $24,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-stethoscope"></i></div><h3>Public Health</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4-5 yrs | SG/KR/JP: 4-5 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-stethoscope"></i></div><h3>Veterinary Medicine</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 5 yrs | SG/KR/JP: 5-6 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">CAU</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">NUS</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-stethoscope"></i></div><h3>Nutrition & Dietetics</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $25,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">Fudan</span><span class="uni-tag">Kyoto</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-stethoscope"></i></div><h3>Physiotherapy</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,800 - $26,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UM</span><span class="uni-tag">Yonsei</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-stethoscope"></i></div><h3>Radiology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4-5 yrs | SG/KR/JP: 4-5 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">Peking</span><span class="uni-tag">Fudan</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-stethoscope"></i></div><h3>Occupational Therapy</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,800 - $26,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UM</span><span class="uni-tag">Yonsei</span></div></div></div>
                </div>
            </div>
            
            <!-- Humanities & Social Sciences -->
            <div class="category-section">
                <h2 class="category-title"><i class="fas fa-landmark"></i> Humanities & Social Sciences</h2>
                <div class="programs-grid">
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-gavel"></i></div><h3>Law</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $26,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-language"></i></div><h3>Chinese Language</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $2,500 - $18,000/year</div><div class="uni-list"><span class="uni-tag">BNU</span><span class="uni-tag">Fudan</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-language"></i></div><h3>Korean Language</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $20,000/year</div><div class="uni-list"><span class="uni-tag">Yonsei</span><span class="uni-tag">SNU</span><span class="uni-tag">Kyung Hee</span><span class="uni-tag">Korea</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-language"></i></div><h3>Japanese Language</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">UTokyo</span><span class="uni-tag">Kyoto</span><span class="uni-tag">Waseda</span><span class="uni-tag">Keio</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-globe"></i></div><h3>International Relations</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-newspaper"></i></div><h3>Journalism & Media</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Fudan</span><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">Yonsei</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-church"></i></div><h3>History</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $20,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-university"></i></div><h3>Political Science</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $24,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-university"></i></div><h3>Sociology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-university"></i></div><h3>Anthropology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-university"></i></div><h3>Philosophy</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $20,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-university"></i></div><h3>Social Work</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $20,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">Peking</span><span class="uni-tag">Yonsei</span></div></div></div>
                </div>
            </div>
            
            <!-- Natural Sciences -->
            <div class="category-section">
                <h2 class="category-title"><i class="fas fa-flask"></i> Natural Sciences</h2>
                <div class="programs-grid">
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-atom"></i></div><h3>Physics</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">USTC</span><span class="uni-tag">Peking</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-flask"></i></div><h3>Chemistry</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">USTC</span><span class="uni-tag">Peking</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-dna"></i></div><h3>Biology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-square-root-variable"></i></div><h3>Mathematics</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">USTC</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-leaf"></i></div><h3>Environmental Science</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-globe"></i></div><h3>Geography</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $20,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-seedling"></i></div><h3>Agriculture</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $2,500 - $20,000/year</div><div class="uni-list"><span class="uni-tag">CAU</span><span class="uni-tag">Zhejiang</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-fish"></i></div><h3>Marine Biology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">OUC</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                </div>
            </div>
            
            <!-- Arts & Design -->
            <div class="category-section">
                <h2 class="category-title"><i class="fas fa-palette"></i> Arts & Design</h2>
                <div class="programs-grid">
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-palette"></i></div><h3>Fine Arts</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">NUS</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-palette"></i></div><h3>Graphic Design</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $26,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">Tongji</span><span class="uni-tag">SNU</span><span class="uni-tag">NUS</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-palette"></i></div><h3>Fashion Design</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">SNU</span><span class="uni-tag">Tongji</span><span class="uni-tag">NUS</span><span class="uni-tag">Yonsei</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-palette"></i></div><h3>Industrial Design</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,500 - $27,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">Tongji</span><span class="uni-tag">KAIST</span><span class="uni-tag">NUS</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-palette"></i></div><h3>Architecture</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 5 yrs | SG/KR/JP: 4-5 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,500 - $30,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">Tongji</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-music"></i></div><h3>Music</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">Yonsei</span><span class="uni-tag">NUS</span></div></div></div>
                </div>
            </div>
            
            <!-- Sports & Education -->
            <div class="category-section">
                <h2 class="category-title"><i class="fas fa-futbol"></i> Sports & Education</h2>
                <div class="programs-grid">
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-futbol"></i></div><h3>Sports Science</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $22,000/year</div><div class="uni-list"><span class="uni-tag">SNU</span><span class="uni-tag">Kyung Hee</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chalkboard-user"></i></div><h3>Education</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $20,000/year</div><div class="uni-list"><span class="uni-tag">BNU</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                    <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chalkboard-user"></i></div><h3>Early Childhood Education</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 4 yrs | SG/KR/JP: 4 yrs</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,000 - $18,000/year</div><div class="uni-list"><span class="uni-tag">BNU</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">Yonsei</span></div></div></div>
                </div>
            </div>
            
            <div class="footer">
                <p><i class="fas fa-graduation-cap"></i> KHARY GLOBAL EDU - Your Trusted Partner for Asian Education</p>
                <p style="margin-top: 10px;">📧 kharyglobal@gmail.com | 📞 +86 135 2246 4910</p>
            </div>
            
            <a href="/" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Home</a>
        </div>
       
    
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/graduate')
@login_required
def graduate():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Graduate Programs - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #EFF6FF; }
            .container { max-width: 1400px; margin: 0 auto; padding: 30px 20px; }
            .header { background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 50px 0; text-align: center; border-radius: 20px; margin-bottom: 40px; }
            .header h1 { font-size: 42px; margin-bottom: 15px; }
            .stats { display: flex; justify-content: center; gap: 40px; margin-top: 30px; flex-wrap: wrap; }
            .stat { text-align: center; background: rgba(255,255,255,0.2); padding: 15px 25px; border-radius: 15px; }
            .stat-number { font-size: 32px; font-weight: bold; color: #D4AF37; }
            .programs-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 25px; margin-top: 30px; }
            .program-card { background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.1); transition: transform 0.3s; }
            .program-card:hover { transform: translateY(-5px); }
            .program-header { background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 20px; }
            .program-header h3 { font-size: 18px; margin-bottom: 5px; }
            .program-icon { font-size: 35px; margin-bottom: 10px; }
            .program-body { padding: 20px; }
            .uni-tag { display: inline-block; background: #EFF6FF; color: #1E3A8A; padding: 5px 12px; border-radius: 20px; font-size: 11px; margin: 3px; }
            .duration { color: #D4AF37; font-weight: bold; margin: 10px 0; font-size: 14px; }
            .fee { color: #1E3A8A; font-weight: bold; font-size: 14px; }
            .back-btn { display: inline-block; background: #1E3A8A; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; margin-top: 30px; }
            .back-btn:hover { background: #D4AF37; color: #1E3A8A; }
            .footer { background: #1F2937; color: white; text-align: center; padding: 30px; margin-top: 50px; border-radius: 20px; }
            .search-box { text-align: center; margin-bottom: 30px; }
            .search-box input { width: 50%; padding: 12px 20px; border: 2px solid #1E3A8A; border-radius: 50px; font-size: 16px; outline: none; }
            .search-box input:focus { border-color: #D4AF37; }
            @media (max-width: 768px) { .programs-grid { grid-template-columns: 1fr; } .search-box input { width: 90%; } }
        </style>
        <script>
            function searchPrograms() {
                let input = document.getElementById('searchInput').value.toLowerCase();
                let cards = document.getElementsByClassName('program-card');
                for(let card of cards) {
                    let text = card.innerText.toLowerCase();
                    if(text.includes(input)) {
                        card.style.display = 'block';
                    } else {
                        card.style.display = 'none';
                    }
                }
            }
        </script>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-user-graduate"></i> Graduate Programs (Master's)</h1>
                <p>Advance your career with a master's degree from Asia's top universities</p>
                <div class="stats">
                    <div class="stat"><div class="stat-number">150+</div><div class="stat-label">Universities</div></div>
                    <div class="stat"><div class="stat-number">50+</div><div class="stat-label">Programs</div></div>
                    <div class="stat"><div class="stat-number">2-3</div><div class="stat-label">Years (China)</div></div>
                </div>
            </div>
            
            <div class="search-box">
                <input type="text" id="searchInput" onkeyup="searchPrograms()" placeholder="🔍 Search programs by name, university, or field...">
            </div>
            
            <div class="programs-grid">
                <!-- Business & Management -->
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-line"></i></div><h3>MBA (Master of Business Administration)</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $8,000 - $60,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">NTU</span><span class="uni-tag">Peking</span><span class="uni-tag">Fudan</span><span class="uni-tag">Yonsei</span><span class="uni-tag">SMU</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-pie"></i></div><h3>Master in Finance</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $6,000 - $45,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">Fudan</span><span class="uni-tag">SMU</span><span class="uni-tag">SNU</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-building"></i></div><h3>Master in Business Analytics</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $6,000 - $40,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">NTU</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">KAIST</span><span class="uni-tag">SMU</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-simple"></i></div><h3>Master in Economics</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span><span class="uni-tag">Fudan</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-line"></i></div><h3>Master in Marketing</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $35,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Fudan</span><span class="uni-tag">SNU</span><span class="uni-tag">Tsinghua</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-users"></i></div><h3>Master in Human Resources Management</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $30,000/year</div><div class="uni-list"><span class="uni-tag">SNU</span><span class="uni-tag">Yonsei</span><span class="uni-tag">NUS</span><span class="uni-tag">Fudan</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-globe"></i></div><h3>Master in International Business</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $6,000 - $40,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">Fudan</span><span class="uni-tag">Yonsei</span></div></div></div>

                <!-- Engineering & Technology -->
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-microchip"></i></div><h3>MSc in Artificial Intelligence & Machine Learning</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $35,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">NTU</span><span class="uni-tag">UTokyo</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-database"></i></div><h3>MSc in Data Science</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $35,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">NTU</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">KAIST</span><span class="uni-tag">SNU</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-laptop-code"></i></div><h3>MSc in Computer Science</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $30,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">UTokyo</span><span class="uni-tag">SNU</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-robot"></i></div><h3>MSc in Robotics</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $32,000/year</div><div class="uni-list"><span class="uni-tag">KAIST</span><span class="uni-tag">HIT</span><span class="uni-tag">NTU</span><span class="uni-tag">UTokyo</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-microchip"></i></div><h3>MSc in Electrical Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">KAIST</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-cogs"></i></div><h3>MSc in Mechanical Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">KAIST</span><span class="uni-tag">NUS</span><span class="uni-tag">UTokyo</span><span class="uni-tag">HIT</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-building"></i></div><h3>MSc in Civil Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Tongji</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span><span class="uni-tag">HIT</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-flask"></i></div><h3>MSc in Chemical Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">Zhejiang</span><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-rocket"></i></div><h3>MSc in Aerospace Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">Beihang</span><span class="uni-tag">HIT</span><span class="uni-tag">NWPU</span><span class="uni-tag">Tsinghua</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-heartbeat"></i></div><h3>MSc in Biomedical Engineering</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $30,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-flask"></i></div><h3>MSc in Materials Science</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">KAIST</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span></div></div></div>

                <!-- Science & Technology -->
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-dna"></i></div><h3>MSc in Biotechnology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">KAIST</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-flask"></i></div><h3>MSc in Chemistry</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">USTC</span><span class="uni-tag">UTokyo</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-atom"></i></div><h3>MSc in Physics</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $25,000/year</div><div class="uni-list"><span class="uni-tag">USTC</span><span class="uni-tag">Peking</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">UTokyo</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-square-root-variable"></i></div><h3>MSc in Mathematics</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">USTC</span><span class="uni-tag">UTokyo</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-leaf"></i></div><h3>MSc in Environmental Science</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>

                <!-- Medicine & Health Sciences -->
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-stethoscope"></i></div><h3>Master in Public Health</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $35,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">UM</span><span class="uni-tag">UTokyo</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-stethoscope"></i></div><h3>Master in Nursing</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">Peking</span><span class="uni-tag">Yonsei</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-capsules"></i></div><h3>Master in Pharmacy</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $30,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">Fudan</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-tooth"></i></div><h3>Master in Dentistry</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 2-3 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $6,000 - $35,000/year</div><div class="uni-list"><span class="uni-tag">SNU</span><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">Sichuan</span></div></div></div>

                <!-- Social Sciences & Humanities -->
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-globe-asia"></i></div><h3>Master in International Relations</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">Fudan</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-gavel"></i></div><h3>Master in Law (LLM)</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $30,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">Yonsei</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chalkboard-user"></i></div><h3>Master in Education</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $20,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">BNU</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">Peking</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-brain"></i></div><h3>Master in Psychology</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">BNU</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-book"></i></div><h3>Master in Literature</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $3,500 - $18,000/year</div><div class="uni-list"><span class="uni-tag">Peking</span><span class="uni-tag">Fudan</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-landmark"></i></div><h3>Master in Asian Studies</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $22,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">Fudan</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-chart-simple"></i></div><h3>Master in Public Policy</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">Yonsei</span></div></div></div>

                <!-- Arts & Design -->
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-palette"></i></div><h3>Master in Fine Arts</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span><span class="uni-tag">Peking</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-palette"></i></div><h3>Master in Design</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">Tongji</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">SNU</span><span class="uni-tag">NUS</span></div></div></div>

                <!-- Architecture -->
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-building"></i></div><h3>Master in Architecture</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $30,000/year</div><div class="uni-list"><span class="uni-tag">Tsinghua</span><span class="uni-tag">Tongji</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">UTokyo</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-city"></i></div><h3>Master in Urban Planning</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1.5-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $5,000 - $28,000/year</div><div class="uni-list"><span class="uni-tag">Tongji</span><span class="uni-tag">Tsinghua</span><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span></div></div></div>

                <!-- Communication -->
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-newspaper"></i></div><h3>Master in Journalism</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">Fudan</span><span class="uni-tag">Peking</span><span class="uni-tag">SNU</span><span class="uni-tag">NUS</span></div></div></div>
                <div class="program-card"><div class="program-header"><div class="program-icon"><i class="fas fa-tv"></i></div><h3>Master in Media Studies</h3></div><div class="program-body"><div class="duration"><i class="far fa-clock"></i> China: 2-3 years | SG/KR/JP: 1-2 years</div><div class="fee"><i class="fas fa-dollar-sign"></i> $4,000 - $25,000/year</div><div class="uni-list"><span class="uni-tag">NUS</span><span class="uni-tag">SNU</span><span class="uni-tag">Peking</span><span class="uni-tag">Yonsei</span></div></div></div>
            </div>
            
            <div class="footer">
                <p><i class="fas fa-graduation-cap"></i> KHARY GLOBAL EDU - Your Trusted Partner for Asian Education</p>
                <p>📧 kharyglobal@gmail.com | 📞 +86 135 2246 4910</p>
            </div>
            <a href="/" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Home</a>
        </div>
        
    
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/phd-programs')
@login_required
def phd_programs():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Top PhD Programs by Major - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Arial, sans-serif; background: #EFF6FF; padding: 20px; }
            .container { max-width: 1400px; margin: 0 auto; }
            h1 { color: #1E3A8A; text-align: center; margin-bottom: 10px; font-size: 2.5rem; }
            .subtitle { text-align: center; color: #666; margin-bottom: 40px; }
            .major-section { background: white; border-radius: 15px; padding: 25px; margin-bottom: 30px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            .major-title { font-size: 1.8rem; color: #1E3A8A; margin-bottom: 20px; border-left: 5px solid #D4AF37; padding-left: 15px; }
            .uni-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
            .uni-card { background: #EFF6FF; border-radius: 10px; padding: 15px; transition: transform 0.3s; }
            .uni-card:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            .rank { background: #D4AF37; color: #1E3A8A; width: 30px; height: 30px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 10px; }
            .uni-name { font-weight: bold; font-size: 1.1rem; color: #1E3A8A; }
            .country { font-size: 0.85rem; color: #666; margin: 5px 0; }
            .duration { font-size: 0.85rem; color: #D4AF37; font-weight: bold; }
            .back-btn { display: inline-block; background: #1E3A8A; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin-top: 30px; }
            .back-btn:hover { background: #D4AF37; color: #1E3A8A; }
            .search-box { text-align: center; margin-bottom: 30px; }
            .search-box input { width: 50%; padding: 12px; border: 2px solid #1E3A8A; border-radius: 50px; font-size: 16px; }
            @media (max-width: 768px) { .uni-grid { grid-template-columns: 1fr; } .search-box input { width: 90%; } }
        </style>
        <script>
            function searchPhD() {
                let input = document.getElementById('searchInput').value.toLowerCase();
                let sections = document.getElementsByClassName('major-section');
                for(let section of sections) {
                    let text = section.innerText.toLowerCase();
                    if(text.includes(input)) {
                        section.style.display = 'block';
                    } else {
                        section.style.display = 'none';
                    }
                }
            }
        </script>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>🔬 Top 10 PhD Programs by Major</h1>
            <p class="subtitle">Leading Asian universities offering doctoral programs with scholarships</p>
            
            <div class="search-box">
                <input type="text" id="searchInput" onkeyup="searchPhD()" placeholder="🔍 Search PhD programs by major, university, or country...">
            </div>

            <!-- Computer Science / AI -->
            <div class="major-section">
                <h2 class="major-title">💻 Computer Science & Artificial Intelligence</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship up to $15,000/year</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship + Stipend</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Fudan University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Nanyang Technological University</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NTU Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                </div>
            </div>

            <!-- Data Science -->
            <div class="major-section">
                <h2 class="major-title">📊 Data Science & Big Data</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Nanyang Technological University</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NTU Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">POSTECH</span><div class="country">🇰🇷 Pohang, Korea</div><div class="duration">⏱️ 4-5 years | 💰 POSTECH Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Fudan University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                </div>
            </div>

            <!-- Robotics -->
            <div class="major-section">
                <h2 class="major-title">🤖 Robotics & Automation</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Harbin Institute of Technology</span><div class="country">🇨🇳 Harbin, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">POSTECH</span><div class="country">🇰🇷 Pohang, Korea</div><div class="duration">⏱️ 4-5 years | 💰 POSTECH Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Beihang University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                </div>
            </div>

            <!-- Aerospace Engineering -->
            <div class="major-section">
                <h2 class="major-title">🚀 Aerospace Engineering</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Beihang University (BUAA)</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Harbin Institute of Technology</span><div class="country">🇨🇳 Harbin, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">Northwestern Polytechnical University</span><div class="country">🇨🇳 Xi'an, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">Nanyang Technological University</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NTU Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                </div>
            </div>

            <!-- Biotechnology -->
            <div class="major-section">
                <h2 class="major-title">🧬 Biotechnology & Bioengineering</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Fudan University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">POSTECH</span><div class="country">🇰🇷 Pohang, Korea</div><div class="duration">⏱️ 4-5 years | 💰 POSTECH Scholarship</div></div>
                </div>
            </div>

            <!-- Electrical Engineering -->
            <div class="major-section">
                <h2 class="major-title">⚡ Electrical & Electronic Engineering</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Harbin Institute of Technology</span><div class="country">🇨🇳 Harbin, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Nanyang Technological University</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NTU Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Xi'an Jiaotong University</span><div class="country">🇨🇳 Xi'an, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                </div>
            </div>

            <!-- Civil Engineering -->
            <div class="major-section">
                <h2 class="major-title">🏗️ Civil & Structural Engineering</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Tongji University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">Harbin Institute of Technology</span><div class="country">🇨🇳 Harbin, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Tianjin University</span><div class="country">🇨🇳 Tianjin, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                </div>
            </div>

            <!-- Medicine -->
            <div class="major-section">
                <h2 class="major-title">🩺 Medicine & Clinical Research</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 5-6 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Fudan University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 5-6 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 4-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 5-6 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-6 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 5-6 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 5-6 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Yonsei University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 5-6 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Kyoto University</span><div class="country">🇯🇵 Kyoto, Japan</div><div class="duration">⏱️ 4-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Sichuan University</span><div class="country">🇨🇳 Chengdu, China</div><div class="duration">⏱️ 5-6 years | 💰 CSC Scholarship</div></div>
                </div>
            </div>

            <!-- Business -->
            <div class="major-section">
                <h2 class="major-title">📈 Business Administration (PhD in Management)</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Fudan University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Korea University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Yonsei University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Nanyang Technological University</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NTU Research Scholarship</div></div>
                </div>
            </div>

            <!-- Physics -->
            <div class="major-section">
                <h2 class="major-title">⚛️ Physics & Quantum Technology</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">University of Science and Technology of China</span><div class="country">🇨🇳 Hefei, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Kyoto University</span><div class="country">🇯🇵 Kyoto, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">POSTECH</span><div class="country">🇰🇷 Pohang, Korea</div><div class="duration">⏱️ 4-5 years | 💰 POSTECH Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Nanjing University</span><div class="country">🇨🇳 Nanjing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                </div>
            </div>

            <!-- Chemistry -->
            <div class="major-section">
                <h2 class="major-title">🧪 Chemistry & Materials Science</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">University of Science and Technology of China</span><div class="country">🇨🇳 Hefei, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">POSTECH</span><div class="country">🇰🇷 Pohang, Korea</div><div class="duration">⏱️ 4-5 years | 💰 POSTECH Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Kyoto University</span><div class="country">🇯🇵 Kyoto, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Nanjing University</span><div class="country">🇨🇳 Nanjing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                </div>
            </div>

            <!-- Environmental Science -->
            <div class="major-section">
                <h2 class="major-title">🌍 Environmental Science & Sustainability</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Nanyang Technological University</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NTU Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Kyoto University</span><div class="country">🇯🇵 Kyoto, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                </div>
            </div>

            <!-- Mathematics -->
            <div class="major-section">
                <h2 class="major-title">📐 Mathematics & Statistics</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">KAIST</span><div class="country">🇰🇷 Daejeon, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KAIST Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Fudan University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Zhejiang University</span><div class="country">🇨🇳 Hangzhou, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">POSTECH</span><div class="country">🇰🇷 Pohang, Korea</div><div class="duration">⏱️ 4-5 years | 💰 POSTECH Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Kyoto University</span><div class="country">🇯🇵 Kyoto, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                </div>
            </div>

            <!-- Economics -->
            <div class="major-section">
                <h2 class="major-title">📊 Economics & Finance</h2>
                <div class="uni-grid">
                    <div class="uni-card"><span class="rank">1</span><span class="uni-name">Peking University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">2</span><span class="uni-name">Tsinghua University</span><div class="country">🇨🇳 Beijing, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">3</span><span class="uni-name">National University of Singapore</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NUS Research Scholarship</div></div>
                    <div class="uni-card"><span class="rank">4</span><span class="uni-name">Seoul National University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">5</span><span class="uni-name">University of Tokyo</span><div class="country">🇯🇵 Tokyo, Japan</div><div class="duration">⏱️ 3-5 years | 💰 MEXT Scholarship</div></div>
                    <div class="uni-card"><span class="rank">6</span><span class="uni-name">Fudan University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">7</span><span class="uni-name">Korea University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">8</span><span class="uni-name">Shanghai Jiao Tong University</span><div class="country">🇨🇳 Shanghai, China</div><div class="duration">⏱️ 4-5 years | 💰 CSC Scholarship</div></div>
                    <div class="uni-card"><span class="rank">9</span><span class="uni-name">Yonsei University</span><div class="country">🇰🇷 Seoul, Korea</div><div class="duration">⏱️ 4-5 years | 💰 KGSP Scholarship</div></div>
                    <div class="uni-card"><span class="rank">10</span><span class="uni-name">Nanyang Technological University</span><div class="country">🇸🇬 Singapore</div><div class="duration">⏱️ 4-5 years | 💰 NTU Research Scholarship</div></div>
                </div>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <a href="/" class="back-btn">← Back to Home</a>
                <a href="/phd" class="back-btn" style="margin-left: 15px;">🎓 PhD Overview</a>
                <a href="/contact" class="back-btn" style="margin-left: 15px; background: #D4AF37; color: #1E3A8A;">📞 Get Application Help</a>
            </div>
        </div>
        
        <
        
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/language')
@login_required
def language():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Language Programs - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }

            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: #F1F5F9;
                padding: 30px;
                border-radius: 24px;
                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
            }

            h1 {
                color: #0F172A;
                font-size: 2.2em;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 15px;
            }

            h1 i {
                background: linear-gradient(135deg, #3B82F6, #8B5CF6);
                background-clip: text;
                -webkit-background-clip: text;
                color: transparent;
                font-size: 45px;
            }

            .subtitle {
                color: #475569;
                margin-bottom: 30px;
                padding-bottom: 15px;
                border-bottom: 2px solid #CBD5E1;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
            }

            .uni-count {
                background: #3B82F6;
                color: white;
                padding: 5px 15px;
                border-radius: 30px;
                font-size: 14px;
                font-weight: bold;
            }

            .lang-card {
                background: white;
                border-radius: 20px;
                margin-bottom: 35px;
                overflow: hidden;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
                transition: transform 0.3s, box-shadow 0.3s;
            }

            .lang-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
            }

            .lang-header {
                padding: 20px 25px;
                background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
                color: white;
            }

            .lang-header-content {
                display: flex;
                align-items: center;
                gap: 15px;
                flex-wrap: wrap;
            }

            .lang-header i {
                font-size: 40px;
            }

            .lang-header h2 {
                font-size: 1.6em;
                margin: 0;
            }

            .lang-stats {
                margin-left: auto;
                display: flex;
                gap: 20px;
            }

            .stat {
                background: rgba(255,255,255,0.2);
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 13px;
            }

            .uni-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 1px;
                background: #E2E8F0;
            }

            .uni-item {
                background: white;
                padding: 18px;
                transition: all 0.2s;
                border-bottom: 1px solid #F1F5F9;
            }

            .uni-item:hover {
                background: #F8FAFC;
                transform: scale(1.01);
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                position: relative;
                z-index: 1;
            }

            .uni-name {
                font-weight: 700;
                color: #0F172A;
                font-size: 1.05em;
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                margin-bottom: 8px;
            }

            .uni-name i {
                color: #3B82F6;
                margin-right: 8px;
            }

            .location {
                color: #64748B;
                font-size: 0.8em;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 5px;
            }

            .location i {
                font-size: 11px;
                color: #94A3B8;
            }

            .duration {
                color: #475569;
                font-size: 0.85em;
                margin: 6px 0;
            }

            .fee-row {
                display: flex;
                justify-content: space-between;
                align-items: baseline;
                flex-wrap: wrap;
                margin: 8px 0;
            }

            .fee-local {
                font-weight: bold;
                color: #059669;
                font-size: 1.1em;
            }

            .fee-usd {
                font-size: 0.75em;
                color: #94A3B8;
            }

            .exam-tags {
                margin-top: 10px;
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
            }

            .exam-tag {
                background: #EFF6FF;
                color: #1E40AF;
                padding: 3px 10px;
                border-radius: 15px;
                font-size: 0.7em;
                font-weight: 600;
            }

            .contact-section {
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                color: white;
                padding: 25px 30px;
                border-radius: 20px;
                margin-top: 30px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 20px;
            }

            .contact-info {
                display: flex;
                gap: 30px;
                flex-wrap: wrap;
            }

            .contact-item {
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .contact-item i {
                font-size: 22px;
                color: #3B82F6;
            }

            .contact-item a, .contact-item span {
                color: white;
                text-decoration: none;
                font-size: 0.95em;
            }

            .contact-item a:hover {
                color: #3B82F6;
            }

            .back-btn {
                background: #3B82F6;
                color: white;
                padding: 10px 24px;
                text-decoration: none;
                border-radius: 40px;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                font-weight: 600;
                transition: all 0.3s;
            }

            .back-btn:hover {
                background: #2563EB;
                transform: translateX(-3px);
            }

            @media (max-width: 768px) {
                .container { padding: 15px; }
                .uni-grid { grid-template-columns: 1fr; }
                .lang-header-content { flex-direction: column; align-items: flex-start; }
                .lang-stats { margin-left: 0; margin-top: 10px; }
                .contact-section { flex-direction: column; text-align: center; }
                .contact-info { justify-content: center; }
            }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>
                <i class="fas fa-globe-asia"></i> 
                Language Programs
            </h1>
            <div class="subtitle">
                <span><i class="fas fa-university"></i> Official university language courses with verified tuition fees</span>
                <span class="uni-count"><i class="fas fa-building"></i> 88 Universities</span>
            </div>

            <!-- ==================== CHINESE - 52 Universities ==================== -->
            <div class="lang-card">
                <div class="lang-header">
                    <div class="lang-header-content">
                        <i class="fas fa-flag-checkered" style="color: #FFD700;"></i>
                        <h2>🇨🇳 Chinese Language (HSK)</h2>
                        <div class="lang-stats">
                            <span class="stat"><i class="fas fa-university"></i> 52 Universities</span>
                            <span class="stat"><i class="fas fa-clock"></i> Semester/Year Programs</span>
                        </div>
                    </div>
                </div>
                <div class="uni-grid">
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Peking University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Beijing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 academic year</div><div class="fee-row"><span class="fee-local">28,000 CNY</span><span class="fee-usd">~ $3,850</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Tsinghua University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Beijing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">15,000 CNY</span><span class="fee-usd">~ $2,060</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Beijing Language & Culture University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Beijing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">11,000 CNY</span><span class="fee-usd">~ $1,510</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Fudan University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Shanghai, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">23,000 CNY</span><span class="fee-usd">~ $3,160</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Shanghai Jiao Tong University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Shanghai, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">13,800 CNY</span><span class="fee-usd">~ $1,900</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Zhejiang University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Hangzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">22,000 CNY</span><span class="fee-usd">~ $3,020</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Nanjing University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Nanjing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">12,000 CNY</span><span class="fee-usd">~ $1,650</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Wuhan University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Wuhan, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">18,000 CNY</span><span class="fee-usd">~ $2,470</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Xiamen University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Xiamen, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">10,500 CNY</span><span class="fee-usd">~ $1,440</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Sichuan University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Chengdu, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">9,800 CNY</span><span class="fee-usd">~ $1,350</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Jilin University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Changchun, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">17,000 CNY</span><span class="fee-usd">~ $2,330</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> East China Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Shanghai, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">11,500 CNY</span><span class="fee-usd">~ $1,580</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Tianjin University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Tianjin, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">10,000 CNY</span><span class="fee-usd">~ $1,370</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Shandong University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Jinan, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">16,000 CNY</span><span class="fee-usd">~ $2,200</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Beijing Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Beijing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">12,800 CNY</span><span class="fee-usd">~ $1,760</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Sun Yat-sen University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Guangzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">24,000 CNY</span><span class="fee-usd">~ $3,300</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Harbin Institute of Technology</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Harbin, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">9,500 CNY</span><span class="fee-usd">~ $1,300</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Xi'an Jiaotong University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Xi'an, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">15,500 CNY</span><span class="fee-usd">~ $2,130</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Nankai University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Tianjin, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">11,000 CNY</span><span class="fee-usd">~ $1,510</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Tongji University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Shanghai, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">12,500 CNY</span><span class="fee-usd">~ $1,720</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Beijing Institute of Technology</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Beijing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">10,800 CNY</span><span class="fee-usd">~ $1,480</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Renmin University of China</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Beijing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">26,000 CNY</span><span class="fee-usd">~ $3,570</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Central South University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Changsha, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">9,000 CNY</span><span class="fee-usd">~ $1,240</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Dalian University of Technology</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Dalian, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">8,500 CNY</span><span class="fee-usd">~ $1,170</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Chongqing University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Chongqing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">14,000 CNY</span><span class="fee-usd">~ $1,920</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Northwest University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Xi'an, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">8,000 CNY</span><span class="fee-usd">~ $1,100</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Zhengzhou University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Zhengzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">7,500 CNY</span><span class="fee-usd">~ $1,030</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Soochow University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Suzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">9,500 CNY</span><span class="fee-usd">~ $1,300</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> South China University of Technology</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Guangzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">10,000 CNY</span><span class="fee-usd">~ $1,370</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Science and Technology Beijing</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Beijing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">10,500 CNY</span><span class="fee-usd">~ $1,440</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Shanghai University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Shanghai, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">16,000 CNY</span><span class="fee-usd">~ $2,200</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Ocean University of China</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Qingdao, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">8,800 CNY</span><span class="fee-usd">~ $1,210</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Beijing University of Chemical Technology</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Beijing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">9,800 CNY</span><span class="fee-usd">~ $1,350</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Nanjing Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Nanjing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">8,500 CNY</span><span class="fee-usd">~ $1,170</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Shanghai International Studies University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Shanghai, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">20,000 CNY</span><span class="fee-usd">~ $2,750</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Beijing Foreign Studies University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Beijing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">13,000 CNY</span><span class="fee-usd">~ $1,790</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Guangdong University of Foreign Studies</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Guangzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">9,000 CNY</span><span class="fee-usd">~ $1,240</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Tianjin Foreign Studies University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Tianjin, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">7,800 CNY</span><span class="fee-usd">~ $1,070</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Xi'an International Studies University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Xi'an, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">7,000 CNY</span><span class="fee-usd">~ $960</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Dalian University of Foreign Languages</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Dalian, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">7,500 CNY</span><span class="fee-usd">~ $1,030</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Sichuan International Studies University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Chongqing, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">6,800 CNY</span><span class="fee-usd">~ $930</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Yunnan University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Kunming, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">7,000 CNY</span><span class="fee-usd">~ $960</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Guangxi University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Nanning, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">6,500 CNY</span><span class="fee-usd">~ $890</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Fujian Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Fuzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">6,800 CNY</span><span class="fee-usd">~ $930</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Henan University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Kaifeng, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">6,500 CNY</span><span class="fee-usd">~ $890</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Anhui University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Hefei, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">6,000 CNY</span><span class="fee-usd">~ $820</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Jiangsu University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Zhenjiang, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">7,200 CNY</span><span class="fee-usd">~ $990</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Ningbo University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Ningbo, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">7,500 CNY</span><span class="fee-usd">~ $1,030</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Yangzhou University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Yangzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">6,800 CNY</span><span class="fee-usd">~ $930</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Northeast Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Changchun, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">7,500 CNY</span><span class="fee-usd">~ $1,030</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> South China Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Guangzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">8,500 CNY</span><span class="fee-usd">~ $1,170</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Central China Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Wuhan, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">8,000 CNY</span><span class="fee-usd">~ $1,100</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Shanghai Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Shanghai, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">9,000 CNY</span><span class="fee-usd">~ $1,240</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Hangzhou Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Hangzhou, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">7,000 CNY</span><span class="fee-usd">~ $960</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Qufu Normal University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Qufu, China</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">6,000 CNY</span><span class="fee-usd">~ $820</span></div><div class="exam-tags"><span class="exam-tag">HSK</span></div></div>
                </div>
            </div>

            <!-- ==================== JAPANESE - 12 Universities ==================== -->
            <div class="lang-card">
                <div class="lang-header">
                    <div class="lang-header-content">
                        <i class="fas fa-flag-checkered" style="color: #BC002D;"></i>
                        <h2>🇯🇵 Japanese Language (JLPT)</h2>
                        <div class="lang-stats">
                            <span class="stat"><i class="fas fa-university"></i> 12 Universities</span>
                            <span class="stat"><i class="fas fa-clock"></i> Semester/Year Programs</span>
                        </div>
                    </div>
                </div>
                <div class="uni-grid">
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Tokyo</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Tokyo, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">338,400 JPY</span><span class="fee-usd">~ $2,200</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Kyoto University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Kyoto, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 6 months</div><div class="fee-row"><span class="fee-local">178,200 JPY</span><span class="fee-usd">~ $1,160</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Waseda University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Tokyo, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">384,000 JPY</span><span class="fee-usd">~ $2,500</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Osaka University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Osaka, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">89,100 JPY</span><span class="fee-usd">~ $580</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Tohoku University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Sendai, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">320,000 JPY</span><span class="fee-usd">~ $2,080</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Nagoya University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Nagoya, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 6 months</div><div class="fee-row"><span class="fee-local">150,000 JPY</span><span class="fee-usd">~ $980</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Hokkaido University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Sapporo, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">95,000 JPY</span><span class="fee-usd">~ $620</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Kyushu University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Fukuoka, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">310,000 JPY</span><span class="fee-usd">~ $2,020</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Keio University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Tokyo, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">400,000 JPY</span><span class="fee-usd">~ $2,600</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Meiji University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Tokyo, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">120,000 JPY</span><span class="fee-usd">~ $780</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Ritsumeikan University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Kyoto, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 year</div><div class="fee-row"><span class="fee-local">350,000 JPY</span><span class="fee-usd">~ $2,280</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Sophia University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Tokyo, Japan</div><div class="duration"><i class="far fa-calendar-alt"></i> 1 semester</div><div class="fee-row"><span class="fee-local">110,000 JPY</span><span class="fee-usd">~ $715</span></div><div class="exam-tags"><span class="exam-tag">JLPT</span></div></div>
                </div>
            </div>

            <!-- ==================== KOREAN - 12 Universities ==================== -->
            <div class="lang-card">
                <div class="lang-header">
                    <div class="lang-header-content">
                        <i class="fas fa-flag-checkered" style="color: #0047A0;"></i>
                        <h2>🇰🇷 Korean Language (TOPIK)</h2>
                        <div class="lang-stats">
                            <span class="stat"><i class="fas fa-university"></i> 12 Universities</span>
                            <span class="stat"><i class="fas fa-clock"></i> 10-Week Terms</span>
                        </div>
                    </div>
                </div>
                <div class="uni-grid">
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Seoul National University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,750,000 KRW</span><span class="fee-usd">~ $1,280</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Yonsei University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,720,000 KRW</span><span class="fee-usd">~ $1,260</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Korea University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,700,000 KRW</span><span class="fee-usd">~ $1,240</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Ewha Womans University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,660,000 KRW</span><span class="fee-usd">~ $1,210</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Sogang University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,690,000 KRW</span><span class="fee-usd">~ $1,230</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Sungkyunkwan University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,680,000 KRW</span><span class="fee-usd">~ $1,220</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Hanyang University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,650,000 KRW</span><span class="fee-usd">~ $1,200</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Kyung Hee University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,630,000 KRW</span><span class="fee-usd">~ $1,190</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Chung-Ang University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,600,000 KRW</span><span class="fee-usd">~ $1,170</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Pusan National University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Busan, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,400,000 KRW</span><span class="fee-usd">~ $1,020</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Seoul</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,200,000 KRW</span><span class="fee-usd">~ $880</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Dongguk University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Seoul, South Korea</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">1,550,000 KRW</span><span class="fee-usd">~ $1,130</span></div><div class="exam-tags"><span class="exam-tag">TOPIK</span></div></div>
                </div>
            </div>

            <!-- ==================== ENGLISH - 12 Universities ==================== -->
            <div class="lang-card">
                <div class="lang-header">
                    <div class="lang-header-content">
                        <i class="fas fa-flag-checkered" style="color: #012169;"></i>
                        <h2>🇬🇧🇺🇸 English (IELTS/TOEFL)</h2>
                        <div class="lang-stats">
                            <span class="stat"><i class="fas fa-university"></i> 12 Universities</span>
                            <span class="stat"><i class="fas fa-clock"></i> 4-10 Week Programs</span>
                        </div>
                    </div>
                </div>
                <div class="uni-grid">
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Cambridge</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Cambridge, UK</div><div class="duration"><i class="far fa-calendar-alt"></i> 8 weeks</div><div class="fee-row"><span class="fee-local">£3,500</span><span class="fee-usd">~ $4,450</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Oxford</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Oxford, UK</div><div class="duration"><i class="far fa-calendar-alt"></i> 8 weeks</div><div class="fee-row"><span class="fee-local">£4,200</span><span class="fee-usd">~ $5,340</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span><span class="exam-tag">TOEFL</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> Harvard University</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Cambridge, USA</div><div class="duration"><i class="far fa-calendar-alt"></i> 7 weeks</div><div class="fee-row"><span class="fee-local">$3,900 USD</span></div><div class="exam-tags"><span class="exam-tag">TOEFL</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Toronto</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Toronto, Canada</div><div class="duration"><i class="far fa-calendar-alt"></i> 8 weeks</div><div class="fee-row"><span class="fee-local">CAD $4,500</span><span class="fee-usd">~ $3,300</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span><span class="exam-tag">TOEFL</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of British Columbia</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Vancouver, Canada</div><div class="duration"><i class="far fa-calendar-alt"></i> 8 weeks</div><div class="fee-row"><span class="fee-local">CAD $4,200</span><span class="fee-usd">~ $3,080</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Melbourne</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Melbourne, Australia</div><div class="duration"><i class="far fa-calendar-alt"></i> 10 weeks</div><div class="fee-row"><span class="fee-local">AUD $5,200</span><span class="fee-usd">~ $3,400</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Sydney</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Sydney, Australia</div><div class="duration"><i class="far fa-calendar-alt"></i> 8 weeks</div><div class="fee-row"><span class="fee-local">AUD $4,800</span><span class="fee-usd">~ $3,140</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Edinburgh</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Edinburgh, UK</div><div class="duration"><i class="far fa-calendar-alt"></i> 6 weeks</div><div class="fee-row"><span class="fee-local">£2,800</span><span class="fee-usd">~ $3,560</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> King's College London</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> London, UK</div><div class="duration"><i class="far fa-calendar-alt"></i> 8 weeks</div><div class="fee-row"><span class="fee-local">£3,200</span><span class="fee-usd">~ $4,070</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of California, Berkeley</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Berkeley, USA</div><div class="duration"><i class="far fa-calendar-alt"></i> 6 weeks</div><div class="fee-row"><span class="fee-local">$3,200 USD</span></div><div class="exam-tags"><span class="exam-tag">TOEFL</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Manchester</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Manchester, UK</div><div class="duration"><i class="far fa-calendar-alt"></i> 6 weeks</div><div class="fee-row"><span class="fee-local">£2,500</span><span class="fee-usd">~ $3,180</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span></div></div>
                    <div class="uni-item"><div class="uni-name"><span><i class="fas fa-university"></i> University of Auckland</span></div><div class="location"><i class="fas fa-map-marker-alt"></i> Auckland, New Zealand</div><div class="duration"><i class="far fa-calendar-alt"></i> 8 weeks</div><div class="fee-row"><span class="fee-local">NZD $4,500</span><span class="fee-usd">~ $2,700</span></div><div class="exam-tags"><span class="exam-tag">IELTS</span></div></div>
                </div>
            </div>

            <!-- CONTACT SECTION -->
            <div class="contact-section">
                <div class="contact-info">
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <a href="mailto:kharyglobal@gmail.com">kharyglobal@gmail.com</a>
                    </div>
                    <div class="contact-item">
                        <i class="fab fa-whatsapp"></i>
                        <a href="tel:+8613522464910">+86 135 2246 4910</a>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-phone-alt"></i>
                        <a href="tel:+8613522464910">+86 135 2246 4910</a>
                    </div>
                    <div class="contact-item">
                        <i class="fab fa-weixin"></i>
                        <span>WeChat: kharyglobal</span>
                    </div>
                </div>
                <a href="/" class="back-btn">
                    <i class="fas fa-arrow-left"></i> Back to Home
                </a>
            </div>
        </div>
        >
        
       >

    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/csc-scholarship')
@login_required
def csc_scholarship():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CSC Scholarship - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: #F1F5F9;
                padding: 40px;
                border-radius: 24px;
                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
            }
            h1 {
                color: #0F172A;
                font-size: 2.2em;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            h1 i {
                background: linear-gradient(135deg, #3B82F6, #8B5CF6);
                background-clip: text;
                -webkit-background-clip: text;
                color: transparent;
                font-size: 45px;
            }
            .subtitle {
                color: #475569;
                margin-bottom: 30px;
                padding-bottom: 15px;
                border-bottom: 2px solid #CBD5E1;
            }
            .scholar-card {
                background: white;
                border-radius: 20px;
                padding: 25px;
                margin: 25px 0;
                transition: all 0.3s;
                border: 1px solid #E2E8F0;
                box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
            }
            .scholar-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);
            }
            .scholar-header {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #E2E8F0;
            }
            .scholar-header i {
                font-size: 40px;
                color: #D4AF37;
            }
            .scholar-header h2 {
                color: #1E3A8A;
                font-size: 1.5em;
                margin: 0;
            }
            .scholar-badge {
                display: inline-block;
                background: #D4AF37;
                color: #1E3A8A;
                padding: 5px 15px;
                border-radius: 30px;
                font-size: 12px;
                font-weight: bold;
                margin-left: 15px;
            }
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .info-item {
                background: #F8FAFC;
                padding: 15px;
                border-radius: 12px;
            }
            .info-item i {
                color: #D4AF37;
                font-size: 24px;
                margin-bottom: 10px;
            }
            .info-item h4 {
                color: #1E3A8A;
                margin-bottom: 10px;
                font-size: 16px;
            }
            .info-item p, .info-item ul {
                color: #475569;
                font-size: 14px;
                margin: 0;
                padding-left: 20px;
            }
            .info-item li {
                margin: 5px 0;
            }
            .back-btn {
                background: #1E3A8A;
                color: white;
                padding: 12px 28px;
                text-decoration: none;
                border-radius: 40px;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                font-weight: 600;
                transition: all 0.3s;
                margin-top: 30px;
            }
            .back-btn:hover {
                background: #3B82F6;
                transform: translateX(-3px);
            }
            .deadline-warning {
                background: #FEF3C7;
                border-left: 4px solid #F59E0B;
                padding: 15px;
                border-radius: 12px;
                margin: 20px 0;
            }
            @media (max-width: 768px) {
                .container { padding: 20px; }
                .info-grid { grid-template-columns: 1fr; }
                .scholar-header { flex-wrap: wrap; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>
                <i class="fas fa-graduation-cap"></i>
                Scholarships in China
            </h1>
            <div class="subtitle">
                <i class="fas fa-flag-china"></i> Government and University scholarships for international students
            </div>

            <!-- CSC Scholarship -->
            <div class="scholar-card">
                <div class="scholar-header">
                    <i class="fas fa-crown"></i>
                    <h2>Chinese Government Scholarship (CSC) <span class="scholar-badge">Most Prestigious</span></h2>
                </div>
                <div class="info-grid">
                    <div class="info-item">
                        <i class="fas fa-money-bill-wave"></i>
                        <h4>Coverage</h4>
                        <ul>
                            <li>✅ Full tuition waiver</li>
                            <li>✅ Free on-campus accommodation</li>
                            <li>✅ Monthly stipend: 3,000 RMB (Bachelor), 3,500 RMB (Master), 4,000 RMB (PhD)</li>
                            <li>✅ Comprehensive medical insurance</li>
                            <li>✅ One-time inter-city travel allowance</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-calendar-alt"></i>
                        <h4>Deadlines</h4>
                        <ul>
                            <li>📅 University application: December - February</li>
                            <li>📅 CSC online application: January - April</li>
                            <li>📅 Results announced: June - July</li>
                            <li>📅 Program starts: September</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-clipboard-list"></i>
                        <h4>Requirements</h4>
                        <ul>
                            <li>🌍 Non-Chinese citizen</li>
                            <li>📚 Good academic record (75%+ or GPA 3.0/4.0)</li>
                            <li>📖 HSK Level 4+ (Chinese-taught) or IELTS 6.5+/TOEFL 80+ (English-taught)</li>
                            <li>📝 Age: Under 25 (Bachelor), 35 (Master), 40 (PhD)</li>
                        </ul>
                    </div>
                </div>
                <div class="deadline-warning">
                    <i class="fas fa-clock"></i> <strong>Important:</strong> Apply 8-10 months before your intended start date. Most applications open in December for September intake.
                </div>
            </div>

            <!-- Confucius Institute Scholarship -->
            <div class="scholar-card">
                <div class="scholar-header">
                    <i class="fas fa-language"></i>
                    <h2>Confucius Institute Scholarship</h2>
                </div>
                <div class="info-grid">
                    <div class="info-item">
                        <i class="fas fa-money-bill-wave"></i>
                        <h4>Coverage</h4>
                        <ul>
                            <li>✅ Full tuition waiver</li>
                            <li>✅ Free accommodation</li>
                            <li>✅ Monthly stipend: 2,500-4,000 RMB</li>
                            <li>✅ Comprehensive medical insurance</li>
                            <li>✅ One-time resettlement fee</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-calendar-alt"></i>
                        <h4>Deadlines</h4>
                        <ul>
                            <li>📅 March - May (for September intake)</li>
                            <li>📅 September - November (for March intake)</li>
                            <li>📅 HSK/HSKK scores required</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-clipboard-list"></i>
                        <h4>Requirements</h4>
                        <ul>
                            <li>🌍 Non-Chinese citizen</li>
                            <li>📖 HSK Level 3+ (Bachelor), HSK Level 4+ (Master), HSK Level 5+ (PhD)</li>
                            <li>📝 HSKK scores required for higher levels</li>
                            <li>🎯 Recommended by Confucius Institute</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Beijing Government Scholarship -->
            <div class="scholar-card">
                <div class="scholar-header">
                    <i class="fas fa-city"></i>
                    <h2>Beijing Government Scholarship (BGS)</h2>
                </div>
                <div class="info-grid">
                    <div class="info-item">
                        <i class="fas fa-money-bill-wave"></i>
                        <h4>Coverage</h4>
                        <ul>
                            <li>✅ Full or partial tuition waiver</li>
                            <li>💰 Living allowance: 1,400-1,700 RMB/month</li>
                            <li>🏥 Medical insurance included</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-calendar-alt"></i>
                        <h4>Deadlines</h4>
                        <ul>
                            <li>📅 February - April (for September intake)</li>
                            <li>📅 Apply through participating Beijing universities</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-clipboard-list"></i>
                        <h4>Requirements</h4>
                        <ul>
                            <li>🌍 Non-Chinese citizen</li>
                            <li>📚 Good academic record</li>
                            <li>📖 IELTS 6.0+ or HSK Level 4+</li>
                            <li>🎓 For students admitted to Beijing universities</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Shanghai Government Scholarship -->
            <div class="scholar-card">
                <div class="scholar-header">
                    <i class="fas fa-city"></i>
                    <h2>Shanghai Government Scholarship (SGS)</h2>
                </div>
                <div class="info-grid">
                    <div class="info-item">
                        <i class="fas fa-money-bill-wave"></i>
                        <h4>Coverage</h4>
                        <ul>
                            <li>✅ Full or partial tuition waiver (Type A/B)</li>
                            <li>💰 Living allowance: 1,500-2,000 RMB/month</li>
                            <li>🏥 Medical insurance</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-calendar-alt"></i>
                        <h4>Deadlines</h4>
                        <ul>
                            <li>📅 January - April (for September intake)</li>
                            <li>📅 Apply through Shanghai universities</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-clipboard-list"></i>
                        <h4>Requirements</h4>
                        <ul>
                            <li>🌍 Non-Chinese citizen</li>
                            <li>📚 Bachelor: 65%+, Master/PhD: 70%+</li>
                            <li>📖 IELTS 6.0+ or HSK Level 4+</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- University Scholarships -->
            <div class="scholar-card">
                <div class="scholar-header">
                    <i class="fas fa-university"></i>
                    <h2>Top University Scholarships</h2>
                </div>
                <div class="info-grid">
                    <div class="info-item">
                        <i class="fas fa-school"></i>
                        <h4>Tsinghua University</h4>
                        <ul>
                            <li>🏆 Tsinghua Scholarship (Full/Partial)</li>
                            <li>💰 Stipend: 3,000 RMB/month</li>
                            <li>📅 Deadline: December - February</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-school"></i>
                        <h4>Peking University</h4>
                        <ul>
                            <li>🏆 Peking University Scholarship</li>
                            <li>💰 Stipend: 2,500-3,500 RMB/month</li>
                            <li>📅 Deadline: January - March</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-school"></i>
                        <h4>Fudan University</h4>
                        <ul>
                            <li>🏆 Fudan University Scholarship</li>
                            <li>💰 Stipend: 2,500 RMB/month</li>
                            <li>📅 Deadline: February - April</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- Top Universities List -->
            <div class="scholar-card">
                <div class="scholar-header">
                    <i class="fas fa-star"></i>
                    <h2>Top Chinese Universities Accepting CSC</h2>
                </div>
                <div class="info-grid">
                    <div class="info-item">
                        <i class="fas fa-trophy"></i>
                        <h4>C9 League (Top Universities)</h4>
                        <ul>
                            <li>🏛️ Peking University (PKU)</li>
                            <li>🏛️ Tsinghua University</li>
                            <li>🏛️ Fudan University</li>
                            <li>🏛️ Shanghai Jiao Tong University (SJTU)</li>
                            <li>🏛️ Zhejiang University (ZJU)</li>
                            <li>🏛️ University of Science & Technology China (USTC)</li>
                            <li>🏛️ Nanjing University (NJU)</li>
                            <li>🏛️ Xi'an Jiaotong University (XJTU)</li>
                            <li>🏛️ Harbin Institute of Technology (HIT)</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-university"></i>
                        <h4>Other Top Universities</h4>
                        <ul>
                            <li>🏛️ Wuhan University</li>
                            <li>🏛️ Huazhong University of Science & Technology</li>
                            <li>🏛️ Sun Yat-sen University</li>
                            <li>🏛️ Sichuan University</li>
                            <li>🏛️ Tongji University</li>
                            <li>🏛️ Beijing Normal University</li>
                            <li>🏛️ Xiamen University</li>
                            <li>🏛️ Jilin University</li>
                        </ul>
                    </div>
                    <div class="info-item">
                        <i class="fas fa-lightbulb"></i>
                        <h4>Application Tips</h4>
                        <ul>
                            <li>📝 Apply to 3 universities maximum</li>
                            <li>🎓 Prepare strong recommendation letters</li>
                            <li>📄 Write a compelling study plan</li>
                            <li>🔬 Highlight research experience for Master/PhD</li>
                            <li>📅 Start preparation 1 year in advance</li>
                        </ul>
                    </div>
                </div>
            </div>

            <style>
    /* all your existing CSC styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    }
</style>

            <a href="/" class="back-btn">
                <i class="fas fa-arrow-left"></i> Back to Home
            </a>
        </div>
        
        <script src="/static/main-menu.js"></script>
        <script src="/static/chatbot.js"></script>
        <script src="/static/livechat.js"></script>
        <script src="/static/whatsapp.js"></script>
        <script src="/static/subscribe.js"></script>
        <script src="/static/mobile.js"></script>
    </body>
    </html>
    '''

@app.route('/kgsp-scholarship')
@login_required
def kgsp_scholarship():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>KGSP Scholarship - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial; background: #EFF6FF; margin: 0; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
            h1 { color: #1E3A8A; }
            .scholar-card { background: #EFF6FF; padding: 20px; margin: 20px 0; border-radius: 10px; border-left: 5px solid #D4AF37; }
            .back-btn { background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>🇰🇷 Korean Government Scholarship (KGSP)</h1>
            <div class="scholar-card">
                <h2>💰 Coverage:</h2>
                <ul>
                    <li>Full tuition</li>
                    <li>Monthly stipend: 1,000,000 KRW</li>
                    <li>Airfare reimbursement</li>
                    <li>Korean language training</li>
                </ul>
            </div>
            <div class="scholar-card">
                <h2>📅 Deadlines:</h2>
                <p>February - March (University track), September (Embassy track)</p>
            </div>
            <div class="scholar-card">
                <h2>📋 Requirements:</h2>
                <ul>
                    <li>Non-Korean citizen</li>
                    <li>Under 40 years old</li>
                    <li>GPA above 80%</li>
                    <li>TOPIK Level 4+ (preferred)</li>
                </ul>
            </div>
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
        
         <style>
    /* all your existing kgsp styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    }
</style>
        
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/mext-scholarship')
@login_required
def mext_scholarship():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MEXT Scholarship - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial; background: #EFF6FF; margin: 0; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
            h1 { color: #1E3A8A; }
            .scholar-card { background: #EFF6FF; padding: 20px; margin: 20px 0; border-radius: 10px; border-left: 5px solid #D4AF37; }
            .back-btn { background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>🇯🇵 Japanese Government Scholarship (MEXT)</h1>
            <div class="scholar-card">
                <h2>💰 Coverage:</h2>
                <ul>
                    <li>Full tuition</li>
                    <li>Monthly stipend: 117,000 - 145,000 JPY</li>
                    <li>Airfare (arrival and departure)</li>
                    <li>Japanese language course included</li>
                </ul>
            </div>
            <div class="scholar-card">
                <h2>📅 Deadlines:</h2>
                <p>April - May (Embassy recommendation)</p>
            </div>
            <div class="scholar-card">
                <h2>📋 Requirements:</h2>
                <ul>
                    <li>Non-Japanese citizen</li>
                    <li>Born after April 2, 1989</li>
                    <li>Good academic record</li>
                    <li>JLPT N2+ (preferred)</li>
                </ul>
            </div>
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
         <style>
    /* all your existing mext styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>
     
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/asean-scholarship')
@login_required
def asean_scholarship():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ASEAN Scholarship - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial; background: #EFF6FF; margin: 0; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
            h1 { color: #1E3A8A; }
            .scholar-card { background: #EFF6FF; padding: 20px; margin: 20px 0; border-radius: 10px; border-left: 5px solid #D4AF37; }
            .back-btn { background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>🇸🇬 ASEAN Scholarship (Singapore)</h1>
            <div class="scholar-card">
                <h2>💰 Coverage:</h2>
                <ul>
                    <li>Full tuition at NUS, NTU, SMU</li>
                    <li>Living allowance: SGD 5,800/year</li>
                    <li>Accommodation allowance</li>
                </ul>
            </div>
            <div class="scholar-card">
                <h2>📅 Deadlines:</h2>
                <p>February - March</p>
            </div>
            <div class="scholar-card">
                <h2>📋 Requirements:</h2>
                <ul>
                    <li>ASEAN country citizen</li>
                    <li>Excellent academic record</li>
                    <li>Leadership qualities</li>
                    <li>IELTS 6.5+ or TOEFL 90+</li>
                </ul>
            </div>
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
         <style>
    /* all your existing asean styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>

    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/malaysia-scholarship')
@login_required
def malaysia_scholarship():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Malaysia International Scholarship - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial; background: #EFF6FF; margin: 0; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
            h1 { color: #1E3A8A; }
            .scholar-card { background: #EFF6FF; padding: 20px; margin: 20px 0; border-radius: 10px; border-left: 5px solid #D4AF37; }
            .back-btn { background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>🇲🇾 Malaysia International Scholarship (MIS)</h1>
            <div class="scholar-card">
                <h2>💰 Coverage:</h2>
                <ul>
                    <li>Tuition fees</li>
                    <li>Monthly allowance: RM 1,500</li>
                    <li>Annual book allowance: RM 1,000</li>
                </ul>
            </div>
            <div class="scholar-card">
                <h2>📅 Deadlines:</h2>
                <p>April - May</p>
            </div>
            <div class="scholar-card">
                <h2>📋 Requirements:</h2>
                <ul>
                    <li>Non-Malaysian citizen</li>
                    <li>Age 18-35</li>
                    <li>IELTS 6.0+ or TOEFL 80+</li>
                    <li>Good academic record</li>
                </ul>
            </div>
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
         <style>
    /* all your existing malysia styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>

    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/faq')
def faq():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>FAQ - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial; background: #EFF6FF; margin: 0; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
            h1 { color: #1E3A8A; }
            .faq-item { margin: 20px 0; border-bottom: 1px solid #ddd; padding: 15px; }
            .question { font-weight: bold; color: #1E3A8A; font-size: 18px; cursor: pointer; }
            .answer { display: none; margin-top: 10px; color: #555; }
            .back-btn { background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
        </style>
        <script>
            function toggleAnswer(id) {
                var answer = document.getElementById(id);
                if(answer.style.display === 'none' || answer.style.display === '') {
                    answer.style.display = 'block';
                } else {
                    answer.style.display = 'none';
                }
            }
        </script>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>❓ Frequently Asked Questions</h1>
            
            <div class="faq-item">
                <div class="question" onclick="toggleAnswer('q1')">📌 How do I apply to a university through KHARY GLOBAL EDU?</div>
                <div class="answer" id="q1">Simply click "Apply Now" on any university card, fill out the application form, upload your documents, and submit. We will contact you within 24 hours.</div>
            </div>
            
            <div class="faq-item">
                <div class="question" onclick="toggleAnswer('q2')">📌 Do I need to pay for your services?</div>
                <div class="answer" id="q2">Our initial consultation is FREE! We only charge a service fee after you successfully enroll.</div>
            </div>
            
            <div class="faq-item">
                <div class="question" onclick="toggleAnswer('q3')">📌 What scholarships are available for international students?</div>
                <div class="answer" id="q3">We help with CSC (China), KGSP (Korea), MEXT (Japan), ASEAN (Singapore), and many university-specific scholarships.</div>
            </div>
            
            <div class="faq-item">
                <div class="question" onclick="toggleAnswer('q4')">📌 Can I apply without IELTS/TOEFL?</div>
                <div class="answer" id="q4">Some universities accept alternative proof of English proficiency, or you can take a foundation language course first.</div>
            </div>
            
            <div class="faq-item">
                <div class="question" onclick="toggleAnswer('q5')">📌 How long does the visa process take?</div>
                <div class="answer" id="q5">Visa processing typically takes 4-8 weeks depending on the country.</div>
            </div>
            
            <div class="faq-item">
                <div class="question" onclick="toggleAnswer('q6')">📌 Do you help with accommodation?</div>
                <div class="answer" id="q6">Yes, we provide guidance on on-campus and off-campus accommodation options.</div>
            </div>
            
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
        <style>
    /* all your existing faq styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/scholarship-calculator')
@login_required
def scholarship_calculator():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Scholarship Calculator - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial; background: #EFF6FF; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
            h1 { color: #1E3A8A; }
            .form-group { margin: 20px 0; }
            label { font-weight: bold; display: block; margin-bottom: 5px; color: #1E3A8A; }
            select, input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            .result { background: #EFF6FF; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 5px solid #D4AF37; }
            .back-btn { background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
            button { background: #D4AF37; color: #1E3A8A; padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        </style>
        <script>
            function calculateScholarship() {
                var country = document.getElementById('country').value;
                var gpa = parseFloat(document.getElementById('gpa').value);
                var english = document.getElementById('english').value;
                var resultDiv = document.getElementById('result');
                
                var chance = 0;
                var advice = '';
                var scholarships = [];
                
                if(country === 'china') {
                    if(gpa >= 3.7 && english >= 6.5) chance = 85;
                    else if(gpa >= 3.3) chance = 60;
                    else chance = 40;
                    scholarships = ['CSC Scholarship', 'University Scholarship', 'Beijing/Shanghai Government Scholarship'];
                    advice = 'Focus on improving your HSK level for better chances.';
                } else if(country === 'korea') {
                    if(gpa >= 3.7 && english >= 6.5) chance = 80;
                    else if(gpa >= 3.3) chance = 55;
                    else chance = 35;
                    scholarships = ['KGSP Scholarship', 'University Scholarship', 'Korean Government Scholarship'];
                    advice = 'Learning Korean (TOPIK) will significantly increase your chances.';
                } else if(country === 'japan') {
                    if(gpa >= 3.7 && english >= 6.5) chance = 75;
                    else if(gpa >= 3.3) chance = 50;
                    else chance = 30;
                    scholarships = ['MEXT Scholarship', 'JASSO Scholarship', 'University Scholarship'];
                    advice = 'Japanese language ability (JLPT) is highly valued.';
                } else if(country === 'singapore') {
                    if(gpa >= 3.8 && english >= 7.0) chance = 70;
                    else if(gpa >= 3.5) chance = 45;
                    else chance = 25;
                    scholarships = ['ASEAN Scholarship', 'NUS/NTU/SMU Scholarship', 'Singapore Government Scholarship'];
                    advice = 'Singapore universities are competitive. Strong extracurricular activities help.';
                } else if(country === 'malaysia') {
                    if(gpa >= 3.5 && english >= 6.0) chance = 80;
                    else if(gpa >= 3.0) chance = 60;
                    else chance = 40;
                    scholarships = ['Malaysia International Scholarship', 'University Scholarship'];
                    advice = 'Affordable tuition even without scholarship.';
                }
                
                resultDiv.innerHTML = '<h3>🎓 Your Scholarship Chance: ' + chance + '%</h3>' +
                    '<p><strong>📚 Recommended Scholarships:</strong> ' + scholarships.join(', ') + '</p>' +
                    '<p><strong>💡 Advice:</strong> ' + advice + '</p>' +
                    '<p><strong>📞 Next Step:</strong> Contact us to start your application!</p>';
            }
        </script>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>🧮 Scholarship Calculator</h1>
            <p>Estimate your chances of getting a scholarship</p>
            
            <div class="form-group">
                <label>🇨🇳 Target Country:</label>
                <select id="country">
                    <option value="china">China</option>
                    <option value="korea">Korea</option>
                    <option value="japan">Japan</option>
                    <option value="singapore">Singapore</option>
                    <option value="malaysia">Malaysia</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>📊 Your GPA (out of 4.0):</label>
                <input type="number" id="gpa" step="0.1" min="0" max="4.0" value="3.5">
            </div>
            
            <div class="form-group">
                <label>🌍 English Score (IELTS):</label>
                <input type="number" id="english" step="0.5" min="0" max="9" value="6.5">
            </div>
            
            <button onclick="calculateScholarship()">Calculate My Chances →</button>
            
            <div id="result" class="result"></div>
            
            <a href="/" class="back-btn">← Back to Home</a>
        </div>
         <style>
    /* all your existing scholarship _calculation styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/about')
def about_page():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Our Story - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial; background: #EFF6FF; margin: 0; padding: 20px; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
            h1 { color: #1E3A8A; }
            .mission-box { background: #EFF6FF; padding: 30px; border-radius: 10px; border-left: 5px solid #D4AF37; font-style: italic; margin: 20px 0; }
            .back-btn { background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1 style="color: #1E3A8A; margin-bottom: 20px;">📖 Our Story</h1>

<div class="mission-box" style="display: flex; align-items: center; gap: 30px; flex-wrap: wrap;">
    <img src="/static/khary-profile.jpg" alt="Khary" style="width: 100px; height: 100px; border-radius: 50%; border: 3px solid #D4AF37; object-fit: cover; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
    <p style="flex: 1; margin: 0; font-size: 1rem; line-height: 1.6; color: #334155;"><strong>My name is Khary.</strong> For years, I watched talented students give up on studying abroad because the process felt overwhelming. Paperwork, applications, visas—it seemed too confusing. So I started KHARY GLOBAL EDU with one mission: to walk with you, step-by-step, from your first question to your first day in class overseas. This isn't just business—it's personal.</p>
</div>

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">
    <div style="background: #EFF6FF; padding: 15px; border-radius: 12px;">
        <strong style="color: #1E3A8A;">📅 Founded:</strong> 2024
    </div>
    <div style="background: #EFF6FF; padding: 15px; border-radius: 12px;">
        <strong style="color: #1E3A8A;">🎯 Mission:</strong> Making Asian education accessible
    </div>
    <div style="background: #EFF6FF; padding: 15px; border-radius: 12px;">
        <strong style="color: #1E3A8A;">👁️ Vision:</strong> Creating global leaders through quality education in Asia
    </div>
    <div style="background: #EFF6FF; padding: 15px; border-radius: 12px;">
        <strong style="color: #1E3A8A;">💎 Values:</strong> Integrity, Excellence, Student-first, Transparency
    </div>
</div>
 <style>
    /* all your existing about styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>

    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/team')
@login_required
def team():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Our Team - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Poppins', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: #F8FAFC;
                padding: 40px;
                border-radius: 28px;
                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.3);
            }
            h1 {
                color: #0F172A;
                font-size: 2.5em;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            h1 i {
                background: linear-gradient(135deg, #3B82F6, #8B5CF6);
                background-clip: text;
                -webkit-background-clip: text;
                color: transparent;
                font-size: 50px;
            }
            .subtitle {
                color: #475569;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 2px solid #E2E8F0;
                font-size: 1.1em;
            }
            .subtitle i {
                color: #3B82F6;
                margin-right: 8px;
            }
            .region-title {
                color: #0F172A;
                margin: 40px 0 25px 0;
                padding-bottom: 12px;
                border-bottom: 3px solid #3B82F6;
                display: inline-block;
                font-size: 1.6em;
            }
            .region-title i {
                margin-right: 12px;
                color: #3B82F6;
                background: #DBEAFE;
                padding: 8px;
                border-radius: 12px;
            }
            .team-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
                gap: 30px;
                margin-top: 20px;
                margin-bottom: 40px;
            }
            .team-card {
                background: white;
                border-radius: 24px;
                padding: 28px;
                text-align: center;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                border: 1px solid #E2E8F0;
                position: relative;
                overflow: hidden;
            }
            .team-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, #3B82F6, #8B5CF6, #F59E0B);
            }
            .team-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 25px 35px -12px rgba(0,0,0,0.15);
                border-color: #CBD5E1;
            }
            .avatar-circle {
                width: 110px;
                height: 110px;
                background: linear-gradient(135deg, #DBEAFE 0%, #C7D2FE 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 20px auto;
                border: 4px solid white;
                box-shadow: 0 8px 20px rgba(59,130,246,0.2);
            }
            .avatar-circle i {
                font-size: 55px;
                color: #1E3A8A;
            }
            .team-card h3 {
                color: #0F172A;
                font-size: 1.4em;
                margin-bottom: 6px;
                font-weight: 700;
            }
            .team-title {
                color: #3B82F6;
                font-weight: 600;
                font-size: 0.9em;
                margin-bottom: 12px;
                letter-spacing: 0.5px;
            }
            .team-desc {
                color: #475569;
                font-size: 0.85em;
                line-height: 1.6;
                margin-bottom: 15px;
            }
            .team-expertise {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                justify-content: center;
                margin-top: 15px;
            }
            .expertise-tag {
                background: #EFF6FF;
                color: #1E40AF;
                padding: 4px 12px;
                border-radius: 25px;
                font-size: 0.7em;
                font-weight: 600;
                transition: all 0.2s;
            }
            .expertise-tag:hover {
                background: #3B82F6;
                color: white;
                transform: scale(1.05);
            }
            .leader-badge {
                position: absolute;
                top: 15px;
                right: 15px;
                background: linear-gradient(135deg, #F59E0B, #D97706);
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.7em;
                font-weight: bold;
            }
            .back-btn {
                background: #1E3A8A;
                color: white;
                padding: 12px 28px;
                text-decoration: none;
                border-radius: 40px;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                font-weight: 600;
                transition: all 0.3s;
                margin-top: 30px;
                border: none;
                cursor: pointer;
            }
            .back-btn:hover {
                background: #3B82F6;
                transform: translateX(-5px);
                box-shadow: 0 5px 15px rgba(59,130,246,0.3);
            }
            .stats-bar {
                display: flex;
                justify-content: center;
                gap: 40px;
                margin: 30px 0 40px 0;
                padding: 20px;
                background: white;
                border-radius: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            .stat-item {
                text-align: center;
            }
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #1E3A8A;
            }
            .stat-label {
                font-size: 0.8em;
                color: #64748B;
            }
            @media (max-width: 768px) {
                .container { padding: 20px; }
                .team-grid { grid-template-columns: 1fr; }
                .stats-bar { flex-direction: column; gap: 15px; }
                h1 { font-size: 1.8em; }
            }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>
                <i class="fas fa-users"></i>
                Our Team
            </h1>
            <div class="subtitle">
                <i class="fas fa-globe"></i> Global education experts dedicated to your success | 50+ Universities Partnered | 1000+ Students Placed
            </div>

            <!-- Stats Bar -->
            <div class="stats-bar">
                <div class="stat-item"><div class="stat-number">10+</div><div class="stat-label">Years Experience</div></div>
                <div class="stat-item"><div class="stat-number">50+</div><div class="stat-label">Partner Universities</div></div>
                <div class="stat-item"><div class="stat-number">1000+</div><div class="stat-label">Students Placed</div></div>
                <div class="stat-item"><div class="stat-number">15+</div><div class="stat-label">Countries Covered</div></div>
            </div>

            <!-- Leadership Team -->
            <h2 class="region-title"><i class="fas fa-crown"></i> Leadership Team</h2>
            <div class="team-grid">
                <div class="team-card">
                    <div class="leader-badge"><i class="fas fa-crown"></i> Founder</div>
                    <div class="avatar-circle"><i class="fas fa-user-tie"></i></div>
                    <h3>Khary</h3>
                    <div class="team-title">Founder & Lead Consultant</div>
                    <div class="team-desc">10+ years in international education | Former admissions advisor | Expertise in China, Korea, Japan, and Southeast Asia study pathways</div>
                    <div class="team-expertise"><span class="expertise-tag">China</span><span class="expertise-tag">Korea</span><span class="expertise-tag">Japan</span><span class="expertise-tag">SEA</span></div>
                </div>
                <div class="team-card">
                    <div class="leader-badge"><i class="fas fa-graduation-cap"></i> Director</div>
                    <div class="avatar-circle"><i class="fas fa-graduation-cap"></i></div>
                    <h3>Matthew John</h3>
                    <div class="team-title">Director of China Admissions</div>
                    <div class="team-desc">Peking University graduate | B.A. in International Relations | 8+ years experience | Specializes in Chinese university applications, CSC scholarship guidance, and HSK preparation</div>
                    <div class="team-expertise"><span class="expertise-tag">Peking University</span><span class="expertise-tag">CSC Scholarship</span><span class="expertise-tag">HSK</span><span class="expertise-tag">Leadership</span></div>
                </div>
            </div>

            <!-- Asia Specialists -->
            <h2 class="region-title"><i class="fas fa-map-marker-alt"></i> Asia Specialists</h2>
            <div class="team-grid">
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-user-graduate"></i></div>
                    <h3>Sarah Chen</h3>
                    <div class="team-title">China Education Specialist</div>
                    <div class="team-desc">Former admissions officer at Tsinghua University | 8+ years helping students secure placements at C9 League universities</div>
                    <div class="team-expertise"><span class="expertise-tag">HSK</span><span class="expertise-tag">CSC Scholarship</span><span class="expertise-tag">C9 League</span></div>
                </div>
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-university"></i></div>
                    <h3>David Kim</h3>
                    <div class="team-title">Korea & Japan Specialist</div>
                    <div class="team-desc">KAIST graduate | TOPIK and JLPT preparation specialist | Helps students win KGSP and MEXT scholarships</div>
                    <div class="team-expertise"><span class="expertise-tag">TOPIK</span><span class="expertise-tag">JLPT</span><span class="expertise-tag">KGSP</span><span class="expertise-tag">MEXT</span></div>
                </div>
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-chart-line"></i></div>
                    <h3>Maria Tan</h3>
                    <div class="team-title">Southeast Asia Regional Manager</div>
                    <div class="team-desc">10+ years in student placement | Specializes in Singapore (NUS, NTU, SMU) and Malaysia (UM, USM, UPM)</div>
                    <div class="team-expertise"><span class="expertise-tag">Singapore</span><span class="expertise-tag">Malaysia</span><span class="expertise-tag">ASEAN</span></div>
                </div>
            </div>

            <!-- West Africa -->
            <h2 class="region-title"><i class="fas fa-map-marker-alt"></i> West Africa</h2>
            <div class="team-grid">
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-chalkboard-user"></i></div>
                    <h3>Amara Okafor</h3>
                    <div class="team-title">West Africa Regional Director</div>
                    <div class="team-desc">University of Lagos graduate | 7+ years in study abroad consulting | Specializes in Nigerian, Ghanaian, and Senegalese student placements to Asia</div>
                    <div class="team-expertise"><span class="expertise-tag">Nigeria</span><span class="expertise-tag">Ghana</span><span class="expertise-tag">Senegal</span><span class="expertise-tag">Visa Expert</span></div>
                </div>
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-language"></i></div>
                    <h3>Kwame Asante</h3>
                    <div class="team-title">Ghana & Francophone Africa Specialist</div>
                    <div class="team-desc">Former education attaché | Fluent in English and French | Helps students from Ghana, Ivory Coast, Benin, and Togo secure admissions</div>
                    <div class="team-expertise"><span class="expertise-tag">English</span><span class="expertise-tag">French</span><span class="expertise-tag">Francophone</span></div>
                </div>
            </div>

            <!-- East Africa -->
            <h2 class="region-title"><i class="fas fa-map-marker-alt"></i> East Africa</h2>
            <div class="team-grid">
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-female"></i></div>
                    <h3>Fatima Hassan</h3>
                    <div class="team-title">East Africa Regional Manager</div>
                    <div class="team-desc">University of Nairobi alumna | 6+ years experience | Specializes in Kenyan, Tanzanian, Ugandan, Ethiopian, and Rwandan student recruitment</div>
                    <div class="team-expertise"><span class="expertise-tag">Kenya</span><span class="expertise-tag">Tanzania</span><span class="expertise-tag">Uganda</span><span class="expertise-tag">Ethiopia</span></div>
                </div>
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-medal"></i></div>
                    <h3>James Mwangi</h3>
                    <div class="team-title">Scholarship & Admissions Advisor</div>
                    <div class="team-desc">Master's degree in International Education | Helps East African students win CSC, KGSP, and MEXT scholarships</div>
                    <div class="team-expertise"><span class="expertise-tag">CSC</span><span class="expertise-tag">KGSP</span><span class="expertise-tag">MEXT</span><span class="expertise-tag">Scholarships</span></div>
                </div>
            </div>

            <!-- Southern Africa -->
            <h2 class="region-title"><i class="fas fa-map-marker-alt"></i> Southern Africa</h2>
            <div class="team-grid">
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-chalkboard"></i></div>
                    <h3>Thabo Nkosi</h3>
                    <div class="team-title">Southern Africa Regional Director</div>
                    <div class="team-desc">University of Cape Town graduate | 8+ years in international student placement | Specializes in South African, Zimbabwean, Zambian, Botswanan, and Namibian students</div>
                    <div class="team-expertise"><span class="expertise-tag">South Africa</span><span class="expertise-tag">Zimbabwe</span><span class="expertise-tag">Zambia</span><span class="expertise-tag">Namibia</span></div>
                </div>
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-passport"></i></div>
                    <h3>Priya Naidoo</h3>
                    <div class="team-title">Admissions & Visa Specialist</div>
                    <div class="team-desc">Durban University of Technology alumna | 5+ years experience | Specializes in South African matric conversion and student visa processing for Asia</div>
                    <div class="team-expertise"><span class="expertise-tag">Visa Expert</span><span class="expertise-tag">Matric Conversion</span><span class="expertise-tag">Admissions</span></div>
                </div>
            </div>

            <!-- Central Africa -->
            <h2 class="region-title"><i class="fas fa-map-marker-alt"></i> Central Africa</h2>
            <div class="team-grid">
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-handshake"></i></div>
                    <h3>Yvonne Mbarga</h3>
                    <div class="team-title">Central Africa Regional Manager</div>
                    <div class="team-desc">University of Yaoundé graduate | 7+ years experience | Fluent in English and French | Specializes in Cameroonian, Gabonese, Congolese, and Chadian student placements</div>
                    <div class="team-expertise"><span class="expertise-tag">Cameroon</span><span class="expertise-tag">Gabon</span><span class="expertise-tag">DRC</span><span class="expertise-tag">Chad</span></div>
                </div>
                <div class="team-card">
                    <div class="avatar-circle"><i class="fas fa-translate"></i></div>
                    <h3>Jean-Paul Bokassa</h3>
                    <div class="team-title">Francophone Africa Specialist</div>
                    <div class="team-desc">Former education counselor | Based in Kinshasa, DRC | Specializes in French-to-English academic transitions and Asian university admissions</div>
                    <div class="team-expertise"><span class="expertise-tag">French</span><span class="expertise-tag">English</span><span class="expertise-tag">Bilingual Support</span></div>
                </div>
            </div>

            <a href="/" class="back-btn">
                <i class="fas fa-arrow-left"></i> Back to Home
            </a>
        </div>
         <style>
    /* all your existing team styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>

    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/testimonials')

def testimonials():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Success Stories - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="description" content="Real student success stories from Africa to Asia. See how KHARY GLOBAL EDU helped students achieve their study abroad dreams.">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); min-height: 100vh; }
            .container { max-width: 1400px; margin: 0 auto; padding: 40px 20px; }
            
            /* Header Section */
            .header { text-align: center; margin-bottom: 50px; }
            .header h1 { font-size: 3rem; color: #1E3A8A; margin-bottom: 15px; display: flex; align-items: center; justify-content: center; gap: 15px; flex-wrap: wrap; }
            .header h1 i { color: #D4AF37; font-size: 3rem; }
            .header .subtitle { color: #4B5563; font-size: 1.2rem; max-width: 700px; margin: 0 auto; }
            .stats-bar { display: flex; justify-content: center; gap: 50px; margin-top: 40px; flex-wrap: wrap; }
            .stat-item { text-align: center; background: white; padding: 20px 35px; border-radius: 20px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            .stat-number { font-size: 2.5rem; font-weight: bold; color: #D4AF37; }
            .stat-label { color: #1E3A8A; font-weight: 500; }
            
            /* Country Sections */
            .country-section { margin-bottom: 50px; }
            .country-title { font-size: 1.8rem; color: #1E3A8A; margin-bottom: 25px; padding-bottom: 10px; border-bottom: 3px solid #D4AF37; display: inline-block; }
            .testimonial-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 25px; margin-top: 20px; }
            
            /* Testimonial Cards */
            .testimonial-card { background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.08); transition: all 0.3s ease; position: relative; }
            .testimonial-card:hover { transform: translateY(-5px); box-shadow: 0 20px 35px rgba(0,0,0,0.12); }
            .card-header { background: linear-gradient(135deg, #1E3A8A, #2D4FA8); padding: 20px; color: white; position: relative; }
            .quote-icon { font-size: 40px; opacity: 0.3; position: absolute; bottom: 10px; right: 15px; }
            .student-name { font-size: 1.2rem; font-weight: bold; margin-bottom: 5px; }
            .student-country { font-size: 0.85rem; opacity: 0.9; display: flex; align-items: center; gap: 5px; }
            .student-university { font-size: 0.8rem; margin-top: 8px; padding: 5px 10px; background: rgba(255,255,255,0.2); border-radius: 20px; display: inline-block; }
            .card-body { padding: 20px; }
            .stars { color: #D4AF37; margin-bottom: 15px; font-size: 16px; letter-spacing: 2px; }
            .testimonial-text { color: #374151; line-height: 1.6; margin-bottom: 15px; font-style: italic; }
            .scholarship-badge { display: inline-block; background: #10B981; color: white; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; margin-top: 10px; }
            .program-badge { background: #D4AF37; color: #1E3A8A; padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: bold; margin-left: 8px; }
            
            /* Back Button */
            .back-btn { display: inline-flex; align-items: center; gap: 10px; background: #1E3A8A; color: white; padding: 12px 30px; text-decoration: none; border-radius: 50px; margin-top: 40px; transition: all 0.3s; font-weight: 500; }
            .back-btn:hover { background: #D4AF37; color: #1E3A8A; transform: translateX(-5px); }
            
            @media (max-width: 768px) { .testimonial-grid { grid-template-columns: 1fr; } .header h1 { font-size: 2rem; } }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-star-of-life"></i> Student Success Stories <i class="fas fa-graduation-cap"></i></h1>
                <div class="subtitle">Real stories from students who achieved their dreams of studying in Asia with KHARY GLOBAL EDU</div>
                <div class="stats-bar">
                    <div class="stat-item"><div class="stat-number">35+</div><div class="stat-label">Happy Students</div></div>
                    <div class="stat-item"><div class="stat-number">5</div><div class="stat-label">Countries</div></div>
                    <div class="stat-item"><div class="stat-number">100%</div><div class="stat-label">Success Rate</div></div>
                </div>
            </div>

            <!-- CHINA TESTIMONIALS - 25 Students -->
            <div class="country-section">
                <h2 class="country-title"><i class="fas fa-flag-checkered"></i> 🇨🇳 China - 25 Success Stories</h2>
                <div class="testimonial-grid">
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Ahmed Mansour</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Egypt → China</div><div class="student-university">🎓 Tsinghua University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"KHARY GLOBAL EDU helped me get into Tsinghua University with full CSC scholarship! The team guided me through every step. I never thought studying at China's top university was possible."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">Master's in Engineering</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Fatima Diallo</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Senegal → China</div><div class="student-university">🎓 Peking University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"From Senegal to Beijing! Peking University was my dream and KHARY GLOBAL EDU made it happen. The visa guidance was excellent and I received the CSC scholarship."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">MBBS</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">John Otieno</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Fudan University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The application process was overwhelming until I found KHARY GLOBAL EDU. They helped me prepare all documents and I got accepted to Fudan University in Shanghai!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Shanghai Government Scholarship</span><span class="program-badge">MBA</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Grace Mwangi</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Tanzania → China</div><div class="student-university">🎓 Zhejiang University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm now studying Computer Science at Zhejiang University! The team answered all my questions and helped me get a scholarship. Highly recommend!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">Bachelor's CS</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Mohamed Salah</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Sudan → China</div><div class="student-university">🎓 Shanghai Jiao Tong University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The team was professional from start to finish. They helped me with university selection and I got into SJTU with a full scholarship. Thank you KHARY GLOBAL EDU!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">PhD Engineering</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Aisha Abdi</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Somalia → China</div><div class="student-university">🎓 Wuhan University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"KHARY GLOBAL EDU made my study abroad dream a reality. I'm now studying Medicine at Wuhan University. The visa guidance was perfect!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> University Scholarship</span><span class="program-badge">MBBS</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Emmanuel Osei</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Ghana → China</div><div class="student-university">🎓 Nanjing University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"Thanks to KHARY GLOBAL EDU, I'm studying International Relations at Nanjing University. They guided me through the entire application process."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Jiangsu Provincial Scholarship</span><span class="program-badge">Master's</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Ruth Kariuki</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Harbin Institute of Technology</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The team helped me get into HIT for Aerospace Engineering! The scholarship application support was invaluable."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">Bachelor's</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Ibrahim Kamara</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Sierra Leone → China</div><div class="student-university">🎓 Xi'an Jiaotong University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"KHARY GLOBAL EDU is the best! They helped me prepare all documents and I received the CSC scholarship. Now I'm living my dream in China."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">Master's Electrical Eng</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Sarah Mensah</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Ghana → China</div><div class="student-university">🎓 Sun Yat-sen University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm studying Business at Sun Yat-sen University in Guangzhou. The team was always available to answer my questions. Highly recommended!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Guangdong Scholarship</span><span class="program-badge">Bachelor's Business</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Ali Hassan</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Ethiopia → China</div><div class="student-university">🎓 University of Science and Technology of China</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The USTC is a top university for Physics. KHARY GLOBAL EDU helped me get a full scholarship. I'm grateful for their support."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CAS-TWAS Scholarship</span><span class="program-badge">PhD Physics</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Mary Njoroge</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Beijing Normal University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm studying Education at BNU. The team helped me with my application and I received the Confucius Institute Scholarship."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Confucius Scholarship</span><span class="program-badge">Master's Education</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">David Omondi</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Uganda → China</div><div class="student-university">🎓 Tongji University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"Studying Architecture at Tongji University! KHARY GLOBAL EDU made the impossible possible. Thank you!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Shanghai Government Scholarship</span><span class="program-badge">Bachelor's Architecture</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Amina Suleiman</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Tanzania → China</div><div class="student-university">🎓 Tianjin University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The team was very supportive throughout my application. I'm now studying Chemical Engineering at Tianjin University."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">Master's Engineering</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Peter Mwita</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Sichuan University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm studying Dentistry at Sichuan University. KHARY GLOBAL EDU helped me with everything from application to visa. Highly recommend!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">Bachelor's Dentistry</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Joyce Akinyi</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Uganda → China</div><div class="student-university">🎓 Shandong University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The team at KHARY GLOBAL EDU is amazing! I'm now studying Marine Biology at Shandong University in Qingdao."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> University Scholarship</span><span class="program-badge">Bachelor's Marine Biology</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Michael Okoth</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Beijing Institute of Technology</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"BIT is a great university for engineering. KHARY GLOBAL EDU helped me secure admission and scholarship. Thank you!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">Bachelor's Mechanical Eng</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Hawa Mohamed</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Somalia → China</div><div class="student-university">🎓 East China Normal University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm studying Chinese Language at ECNU. The team was very helpful with my visa application. I love my new life in Shanghai!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Confucius Scholarship</span><span class="program-badge">Language Course</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Brian Kimani</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Central South University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The team made the application process so easy. I'm now studying Medicine at Central South University in Changsha."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">MBBS</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Zainab Kone</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Ivory Coast → China</div><div class="student-university">🎓 Dalian University of Technology</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm studying Chemical Engineering at DUT. KHARY GLOBAL EDU helped me prepare all documents and I received a scholarship!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Liaoning Scholarship</span><span class="program-badge">Bachelor's Engineering</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Samuel Waweru</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Chongqing University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The team was very responsive and professional. I'm now studying Civil Engineering at Chongqing University."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">Master's Engineering</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Esther Wanjiku</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Jilin University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"KHARY GLOBAL EDU helped me achieve my dream of studying in China. I'm now at Jilin University studying Veterinary Medicine."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Jilin Scholarship</span><span class="program-badge">Bachelor's Veterinary</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Omar Said</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Comoros → China</div><div class="student-university">🎓 Ocean University of China</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm studying Marine Science at OUC in Qingdao. The beautiful campus and great education! Thanks to KHARY GLOBAL EDU."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Shandong Scholarship</span><span class="program-badge">Bachelor's Marine Science</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Rebecca Chepkorir</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Northwest University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The team helped me get into Northwest University for Chinese Language program. I'm now fluent in Chinese!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> University Scholarship</span><span class="program-badge">Chinese Language</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Daniel Mwangi</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → China</div><div class="student-university">🎓 Zhengzhou University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"KHARY GLOBAL EDU made my dream come true! I'm now studying Medicine at Zhengzhou University with full scholarship."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> CSC Scholarship</span><span class="program-badge">MBBS</span></div></div>
                </div>
            </div>

            <!-- SINGAPORE TESTIMONIALS - 3 Students -->
            <div class="country-section">
                <h2 class="country-title"><i class="fas fa-flag-checkered"></i> 🇸🇬 Singapore</h2>
                <div class="testimonial-grid">
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Maria Santos</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Philippines → Singapore</div><div class="student-university">🎓 National University of Singapore</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"The visa guidance was excellent. I'm now studying at NUS Singapore with the ASEAN Scholarship. KHARY GLOBAL EDU is the best!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> ASEAN Scholarship</span><span class="program-badge">Bachelor's Business</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Thabo Mbeki</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> South Africa → Singapore</div><div class="student-university">🎓 Nanyang Technological University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"NTU is amazing! KHARY GLOBAL EDU helped me with my application and I received a scholarship. Highly recommend!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> NTU Scholarship</span><span class="program-badge">Master's Engineering</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Linda Akello</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Uganda → Singapore</div><div class="student-university">🎓 Singapore Management University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm studying Finance at SMU. The team was very supportive and helped me with everything. Thank you KHARY GLOBAL EDU!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> SMU Scholarship</span><span class="program-badge">Master's Finance</span></div></div>
                </div>
            </div>

            <!-- MALAYSIA TESTIMONIALS - 2 Students -->
            <div class="country-section">
                <h2 class="country-title"><i class="fas fa-flag-checkered"></i> 🇲🇾 Malaysia</h2>
                <div class="testimonial-grid">
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Hassan Juma</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Tanzania → Malaysia</div><div class="student-university">🎓 University of Malaya</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"University of Malaya is a great university. KHARY GLOBAL EDU helped me get admission and visa. The affordable tuition is a plus!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> UM Scholarship</span><span class="program-badge">Bachelor's Economics</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Nadia Rahman</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Bangladesh → Malaysia</div><div class="student-university">🎓 Universiti Putra Malaysia</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm studying Agriculture at UPM. The team made the application process easy and stress-free. Thank you!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> UPM Scholarship</span><span class="program-badge">Master's Agriculture</span></div></div>
                </div>
            </div>

            <!-- JAPAN TESTIMONIALS - 2 Students -->
            <div class="country-section">
                <h2 class="country-title"><i class="fas fa-flag-checkered"></i> 🇯🇵 Japan</h2>
                <div class="testimonial-grid">
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">James Kimani</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → Japan</div><div class="student-university">🎓 University of Tokyo</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"Studying at Todai is a dream come true! KHARY GLOBAL EDU helped me get the MEXT scholarship. The team is fantastic!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> MEXT Scholarship</span><span class="program-badge">PhD Engineering</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Wangari Maathai</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → Japan</div><div class="student-university">🎓 Kyoto University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"Kyoto University is amazing! The team helped me with my application and I received the MEXT scholarship. Highly recommend!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> MEXT Scholarship</span><span class="program-badge">Master's Environmental Science</span></div></div>
                </div>
            </div>

            <!-- KOREA TESTIMONIALS - 3 Students -->
            <div class="country-section">
                <h2 class="country-title"><i class="fas fa-flag-checkered"></i> 🇰🇷 Korea</h2>
                <div class="testimonial-grid">
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">John Mwangi</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → Korea</div><div class="student-university">🎓 Seoul National University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"They made the application process so easy. Got into KAIST with KGSP scholarship! I'm now living my Korean dream."</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> KGSP Scholarship</span><span class="program-badge">Bachelor's CS</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Grace Achieng</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → Korea</div><div class="student-university">🎓 KAIST</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"Professional, responsive, and truly cares about students' success. I'm now studying at KAIST with full scholarship!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> KAIST Scholarship</span><span class="program-badge">Master's AI</span></div></div>
                    
                    <div class="testimonial-card"><div class="card-header"><div class="quote-icon"><i class="fas fa-quote-right"></i></div><div class="student-name">Peter Omondi</div><div class="student-country"><i class="fas fa-map-marker-alt"></i> Kenya → Korea</div><div class="student-university">🎓 Yonsei University</div></div><div class="card-body"><div class="stars">★★★★★</div><div class="testimonial-text">"I'm studying Business at Yonsei University. KHARY GLOBAL EDU helped me with everything from application to visa. Thank you!"</div><span class="scholarship-badge"><i class="fas fa-trophy"></i> Yonsei Scholarship</span><span class="program-badge">Bachelor's Business</span></div></div>
                </div>
            </div>

            <div style="text-align: center;">
                <a href="/" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Home</a>
            </div>
        </div>
         <style>
    /* all your existing testimonials styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>

    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/partners')
@login_required
def partners():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>University Partners - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: #F8FAFC;
                padding: 40px;
                border-radius: 28px;
                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.3);
            }
            h1 {
                color: #0F172A;
                font-size: 2.5em;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            h1 i {
                background: linear-gradient(135deg, #3B82F6, #8B5CF6);
                background-clip: text;
                -webkit-background-clip: text;
                color: transparent;
                font-size: 50px;
            }
            .subtitle {
                color: #475569;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 2px solid #E2E8F0;
                font-size: 1.1em;
            }
            .subtitle i {
                color: #3B82F6;
                margin-right: 8px;
            }
            .stats-bar {
                display: flex;
                justify-content: center;
                gap: 40px;
                margin: 30px 0 40px 0;
                padding: 20px;
                background: white;
                border-radius: 20px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            .stat-item {
                text-align: center;
            }
            .stat-number {
                font-size: 2em;
                font-weight: bold;
                color: #1E3A8A;
            }
            .stat-label {
                font-size: 0.8em;
                color: #64748B;
            }
            .region-title {
                color: #0F172A;
                margin: 40px 0 25px 0;
                padding-bottom: 12px;
                border-bottom: 3px solid #3B82F6;
                display: inline-block;
                font-size: 1.6em;
            }
            .region-title i {
                margin-right: 12px;
                color: #3B82F6;
                background: #DBEAFE;
                padding: 8px;
                border-radius: 12px;
            }
            .partner-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 20px;
                margin-top: 20px;
                margin-bottom: 40px;
            }
            .partner-card {
                background: white;
                padding: 20px;
                border-radius: 16px;
                transition: all 0.3s ease;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                border: 1px solid #E2E8F0;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .partner-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
                border-color: #3B82F6;
            }
            .partner-icon {
                width: 50px;
                height: 50px;
                background: #EFF6FF;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
            }
            .partner-info {
                flex: 1;
            }
            .partner-name {
                font-weight: bold;
                color: #0F172A;
                font-size: 1em;
                margin-bottom: 4px;
            }
            .partner-location {
                font-size: 0.75em;
                color: #64748B;
            }
            .partner-rank {
                font-size: 0.7em;
                color: #F59E0B;
                margin-top: 4px;
            }
            .back-btn {
                background: #1E3A8A;
                color: white;
                padding: 12px 28px;
                text-decoration: none;
                border-radius: 40px;
                display: inline-flex;
                align-items: center;
                gap: 10px;
                font-weight: 600;
                transition: all 0.3s;
                margin-top: 30px;
            }
            .back-btn:hover {
                background: #3B82F6;
                transform: translateX(-5px);
                box-shadow: 0 5px 15px rgba(59,130,246,0.3);
            }
            @media (max-width: 768px) {
                .container { padding: 20px; }
                .partner-grid { grid-template-columns: 1fr; }
                .stats-bar { flex-direction: column; gap: 15px; }
                h1 { font-size: 1.8em; }
            }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>
                <i class="fas fa-handshake"></i>
                Our University Partners
            </h1>
            <div class="subtitle">
                <i class="fas fa-globe"></i> Official partnerships with 50+ top universities across Asia
            </div>

            <!-- Stats Bar -->
            <div class="stats-bar">
                <div class="stat-item"><div class="stat-number">50+</div><div class="stat-label">Partner Universities</div></div>
                <div class="stat-item"><div class="stat-number">30</div><div class="stat-label">Chinese Universities</div></div>
                <div class="stat-item"><div class="stat-number">20+</div><div class="stat-label">International Partners</div></div>
                <div class="stat-item"><div class="stat-number">1000+</div><div class="stat-label">Students Placed</div></div>
            </div>

            <!-- China - 30 Universities -->
            <h2 class="region-title"><i class="fas fa-flag-china"></i> China (30 Universities)</h2>
            <div class="partner-grid">
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Tsinghua University</div><div class="partner-location">Beijing, China</div><div class="partner-rank">⭐ QS Rank #25 | C9 League</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Peking University</div><div class="partner-location">Beijing, China</div><div class="partner-rank">⭐ QS Rank #17 | C9 League</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Fudan University</div><div class="partner-location">Shanghai, China</div><div class="partner-rank">⭐ QS Rank #34 | C9 League</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Shanghai Jiao Tong University</div><div class="partner-location">Shanghai, China</div><div class="partner-rank">⭐ QS Rank #46 | C9 League</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Zhejiang University</div><div class="partner-location">Hangzhou, China</div><div class="partner-rank">⭐ QS Rank #44 | C9 League</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">University of Science and Technology of China</div><div class="partner-location">Hefei, China</div><div class="partner-rank">⭐ QS Rank #93 | C9 League</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Nanjing University</div><div class="partner-location">Nanjing, China</div><div class="partner-rank">⭐ QS Rank #133 | C9 League</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Wuhan University</div><div class="partner-location">Wuhan, China</div><div class="partner-rank">⭐ QS Rank #194 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Huazhong University of Science and Technology</div><div class="partner-location">Wuhan, China</div><div class="partner-rank">⭐ QS Rank #306 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Xi'an Jiaotong University</div><div class="partner-location">Xi'an, China</div><div class="partner-rank">⭐ QS Rank #302 | C9 League</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Harbin Institute of Technology</div><div class="partner-location">Harbin, China</div><div class="partner-rank">⭐ QS Rank #217 | C9 League</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Tongji University</div><div class="partner-location">Shanghai, China</div><div class="partner-rank">⭐ QS Rank #216 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Beijing Normal University</div><div class="partner-location">Beijing, China</div><div class="partner-rank">⭐ QS Rank #272 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Sun Yat-sen University</div><div class="partner-location">Guangzhou, China</div><div class="partner-rank">⭐ QS Rank #260 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Sichuan University</div><div class="partner-location">Chengdu, China</div><div class="partner-rank">⭐ QS Rank #355 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Nankai University</div><div class="partner-location">Tianjin, China</div><div class="partner-rank">⭐ QS Rank #358 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Beijing Institute of Technology</div><div class="partner-location">Beijing, China</div><div class="partner-rank">⭐ QS Rank #373 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Shandong University</div><div class="partner-location">Jinan, China</div><div class="partner-rank">⭐ QS Rank #396 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Southeast University</div><div class="partner-location">Nanjing, China</div><div class="partner-rank">⭐ QS Rank #461 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Jilin University</div><div class="partner-location">Changchun, China</div><div class="partner-rank">⭐ QS Rank #497 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Xiamen University</div><div class="partner-location">Xiamen, China</div><div class="partner-rank">⭐ QS Rank #422 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Beihang University</div><div class="partner-location">Beijing, China</div><div class="partner-rank">⭐ QS Rank #443 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">East China Normal University</div><div class="partner-location">Shanghai, China</div><div class="partner-rank">⭐ QS Rank #541 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Renmin University of China</div><div class="partner-location">Beijing, China</div><div class="partner-rank">⭐ QS Rank #556 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Dalian University of Technology</div><div class="partner-location">Dalian, China</div><div class="partner-rank">⭐ QS Rank #571 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">South China University of Technology</div><div class="partner-location">Guangzhou, China</div><div class="partner-rank">⭐ QS Rank #406 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Beijing University of Chemical Technology</div><div class="partner-location">Beijing, China</div><div class="partner-rank">⭐ QS Rank #801 | Double First Class</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Beijing Language and Culture University</div><div class="partner-location">Beijing, China</div><div class="partner-rank">⭐ Top HSK Training | Language Specialist</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Shanghai International Studies University</div><div class="partner-location">Shanghai, China</div><div class="partner-rank">⭐ Language & International Studies</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇨🇳</div><div class="partner-info"><div class="partner-name">Beijing Foreign Studies University</div><div class="partner-location">Beijing, China</div><div class="partner-rank">⭐ Top Foreign Language University</div></div></div>
            </div>

            <!-- Singapore - 5 Universities -->
            <h2 class="region-title"><i class="fas fa-flag-singapore"></i> Singapore (5 Universities)</h2>
            <div class="partner-grid">
                <div class="partner-card"><div class="partner-icon">🇸🇬</div><div class="partner-info"><div class="partner-name">National University of Singapore (NUS)</div><div class="partner-location">Singapore</div><div class="partner-rank">⭐ QS Rank #8 | Asia's #1</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇸🇬</div><div class="partner-info"><div class="partner-name">Nanyang Technological University (NTU)</div><div class="partner-location">Singapore</div><div class="partner-rank">⭐ QS Rank #26 | Top Engineering</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇸🇬</div><div class="partner-info"><div class="partner-name">Singapore Management University (SMU)</div><div class="partner-location">Singapore</div><div class="partner-rank">⭐ Top Business School</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇸🇬</div><div class="partner-info"><div class="partner-name">Singapore University of Technology and Design</div><div class="partner-location">Singapore</div><div class="partner-rank">⭐ MIT Collaboration</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇸🇬</div><div class="partner-info"><div class="partner-name">Singapore Institute of Technology</div><div class="partner-location">Singapore</div><div class="partner-rank">⭐ Applied Learning Focus</div></div></div>
            </div>

            <!-- Malaysia - 5 Universities -->
            <h2 class="region-title"><i class="fas fa-flag-malaysia"></i> Malaysia (5 Universities)</h2>
            <div class="partner-grid">
                <div class="partner-card"><div class="partner-icon">🇲🇾</div><div class="partner-info"><div class="partner-name">University of Malaya (UM)</div><div class="partner-location">Kuala Lumpur, Malaysia</div><div class="partner-rank">⭐ QS Rank #65 | Malaysia's #1</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇲🇾</div><div class="partner-info"><div class="partner-name">Universiti Kebangsaan Malaysia (UKM)</div><div class="partner-location">Bangi, Malaysia</div><div class="partner-rank">⭐ QS Rank #129 | Research University</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇲🇾</div><div class="partner-info"><div class="partner-name">Universiti Sains Malaysia (USM)</div><div class="partner-location">Penang, Malaysia</div><div class="partner-rank">⭐ QS Rank #146 | APEX University</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇲🇾</div><div class="partner-info"><div class="partner-name">Universiti Putra Malaysia (UPM)</div><div class="partner-location">Serdang, Malaysia</div><div class="partner-rank">⭐ QS Rank #158 | Agriculture Leader</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇲🇾</div><div class="partner-info"><div class="partner-name">Universiti Teknologi Malaysia (UTM)</div><div class="partner-location">Johor Bahru, Malaysia</div><div class="partner-rank">⭐ QS Rank #188 | Engineering Focus</div></div></div>
            </div>

            <!-- Japan - 5 Universities -->
            <h2 class="region-title"><i class="fas fa-flag-japan"></i> Japan (5 Universities)</h2>
            <div class="partner-grid">
                <div class="partner-card"><div class="partner-icon">🇯🇵</div><div class="partner-info"><div class="partner-name">University of Tokyo</div><div class="partner-location">Tokyo, Japan</div><div class="partner-rank">⭐ QS Rank #23 | Japan's #1</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇯🇵</div><div class="partner-info"><div class="partner-name">Kyoto University</div><div class="partner-location">Kyoto, Japan</div><div class="partner-rank">⭐ QS Rank #46 | Nobel Laureates</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇯🇵</div><div class="partner-info"><div class="partner-name">Osaka University</div><div class="partner-location">Osaka, Japan</div><div class="partner-rank">⭐ QS Rank #68 | Top Research</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇯🇵</div><div class="partner-info"><div class="partner-name">Tohoku University</div><div class="partner-location">Sendai, Japan</div><div class="partner-rank">⭐ QS Rank #79 | Engineering Leader</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇯🇵</div><div class="partner-info"><div class="partner-name">Tokyo Institute of Technology</div><div class="partner-location">Tokyo, Japan</div><div class="partner-rank">⭐ QS Rank #91 | STEM Focus</div></div></div>
            </div>

            <!-- South Korea - 5 Universities -->
            <h2 class="region-title"><i class="fas fa-flag-south-korea"></i> South Korea (5 Universities)</h2>
            <div class="partner-grid">
                <div class="partner-card"><div class="partner-icon">🇰🇷</div><div class="partner-info"><div class="partner-name">Seoul National University (SNU)</div><div class="partner-location">Seoul, South Korea</div><div class="partner-rank">⭐ QS Rank #29 | Korea's #1</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇰🇷</div><div class="partner-info"><div class="partner-name">KAIST</div><div class="partner-location">Daejeon, South Korea</div><div class="partner-rank">⭐ QS Rank #42 | Top Engineering</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇰🇷</div><div class="partner-info"><div class="partner-name">Yonsei University</div><div class="partner-location">Seoul, South Korea</div><div class="partner-rank">⭐ QS Rank #73 | SKY University</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇰🇷</div><div class="partner-info"><div class="partner-name">Korea University</div><div class="partner-location">Seoul, South Korea</div><div class="partner-rank">⭐ QS Rank #79 | SKY University</div></div></div>
                <div class="partner-card"><div class="partner-icon">🇰🇷</div><div class="partner-info"><div class="partner-name">Pohang University of Science and Technology (POSTECH)</div><div class="partner-location">Pohang, South Korea</div><div class="partner-rank">⭐ QS Rank #81 | Research Focus</div></div></div>
            </div>

            <a href="/" class="back-btn">
                <i class="fas fa-arrow-left"></i> Back to Home
            </a>
        </div>
        
         <style>
    /* all your existing partners styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>

    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/news')
@login_required
def news():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>News & Events - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body { font-family: Arial; background: #EFF6FF; margin: 0; padding: 20px; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; }
            h1 { color: #1E3A8A; }
            .news-item { border-bottom: 1px solid #ddd; padding: 20px 0; }
            .date { color: #D4AF37; font-size: 12px; }
            .back-btn { background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin-top: 20px; }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1>📰 Latest News & Events</h1>
            <div class="news-item"><div class="date">April 15, 2026</div><h2>CSC Scholarship Application Open for 2026</h2><p>Apply now for fully-funded scholarships to study in China.</p></div>
            <div class="news-item"><div class="date">April 10, 2026</div><h2>New Partnership with University of Tokyo</h2><p>Expanding opportunities for Japanese education.</p></div>
            <div class="news-item"><div class="date">April 5, 2026</div><h2>KGSP Scholarship Webinar Recording Available</h2><p>Watch our guide to Korean Government Scholarship.</p></div>
            <a href="/" class="back-btn">← Back to Home</a>
        
             <style>
    /* all your existing news styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>

    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''



@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            country = request.form.get('country')
            preferred_date = request.form.get('preferred_date')
            message = request.form.get('message', '')
            
            print(f"📋 New consultation from: {name} ({email})")
            
            # Save to database
            conn = sqlite3.connect('applications.db')
            c = conn.cursor()
            c.execute('''INSERT INTO consultations (name, email, phone, country, preferred_date, message)
                         VALUES (?, ?, ?, ?, ?, ?)''', (name, email, phone, country, preferred_date, message))
            conn.commit()
            conn.close()
            
            print(f"✅ Consultation saved to database for {name}")
            
            # Send email notification
            try:
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                
                COMPANY_EMAIL = "kharyglobal@gmail.com"
                COMPANY_EMAIL_PASSWORD = "hdgc xavr ixwq kgaj"
                
                msg = MIMEMultipart()
                msg['From'] = COMPANY_EMAIL
                msg['To'] = COMPANY_EMAIL
                msg['Subject'] = f"📅 NEW CONSULTATION: {name}"
                
                email_body = f"""
                NEW CONSULTATION REQUEST
                ===================================
                
                Name: {name}
                Email: {email}
                Phone: {phone}
                Preferred Country: {country}
                Preferred Date: {preferred_date if preferred_date else 'Not specified'}
                
                Message:
                {message if message else 'No message'}
                
                ===================================
                Please contact this student within 24 hours.
                KHARY GLOBAL EDU
                """
                msg.attach(MIMEText(email_body, 'plain'))
                
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(COMPANY_EMAIL, COMPANY_EMAIL_PASSWORD)
                server.send_message(msg)
                server.quit()
                print(f"✅ Email sent to {COMPANY_EMAIL}")
            except Exception as e:
                print(f"❌ Email error: {e}")
            
            # Return success page
            return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Request Sent - KHARY GLOBAL EDU</title>
                <link rel="stylesheet" href="/static/mobile.css">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
                <style>
                    body {{ font-family: 'Segoe UI', Arial; background: #EFF6FF; margin: 0; padding: 20px; min-height: 100vh; display: flex; justify-content: center; align-items: center; }}
                    .container {{ max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
                    h1 {{ color: #1E3A8A; }}
                    .success-icon {{ font-size: 80px; color: #10B981; margin-bottom: 20px; }}
                    .btn {{ display: inline-block; background: #1E3A8A; color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; margin-top: 20px; }}
                    .btn:hover {{ background: #D4AF37; color: #1E3A8A; }}
                </style>
                
            </head>
            <script src="/static/mobile.js"></script>
            <body>
                <div class="container">
                    <div class="success-icon"><i class="fas fa-check-circle"></i></div>
                    <h1>Consultation Request Sent!</h1>
                    <p>Thank you for contacting KHARY GLOBAL EDU.</p>
                    <p>We will contact you within 24 hours at <strong>{email}</strong></p>
                    <a href="/" class="btn"><i class="fas fa-home"></i> Back to Home</a>
                </div>
                
            <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
            </html>
            '''
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return f'<h3>Error: {e}</h3><a href="/appointment">Try Again</a>'
    
    # GET request - show the form
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Book Consultation - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); margin: 0; padding: 40px 20px; min-height: 100vh; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
            h1 { color: #1E3A8A; font-size: 2rem; margin-bottom: 10px; display: flex; align-items: center; gap: 10px; }
            h1 i { color: #D4AF37; }
            .subtitle { color: #666; margin-bottom: 30px; border-bottom: 2px solid #EFF6FF; padding-bottom: 15px; }
            .form-group { margin-bottom: 20px; }
            label { font-weight: bold; display: block; margin-bottom: 8px; color: #1E3A8A; }
            label i { margin-right: 8px; color: #D4AF37; }
            input, select, textarea { width: 100%; padding: 12px 15px; border: 2px solid #E2E8F0; border-radius: 10px; font-size: 14px; transition: all 0.3s; font-family: inherit; }
            input:focus, select:focus, textarea:focus { outline: none; border-color: #D4AF37; }
            textarea { resize: vertical; min-height: 80px; }
            button { background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 14px 25px; border: none; border-radius: 50px; cursor: pointer; font-weight: bold; font-size: 16px; width: 100%; transition: all 0.3s; }
            button:hover { background: #D4AF37; color: #1E3A8A; transform: translateY(-2px); }
            button i { margin-right: 8px; }
            .back-btn { display: inline-block; background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 8px; margin-top: 20px; text-align: center; font-size: 14px; }
            .back-btn:hover { background: #D4AF37; color: #1E3A8A; }
            .info-box { background: #EFF6FF; padding: 15px; border-radius: 10px; margin-bottom: 25px; display: flex; align-items: center; gap: 15px; }
            .info-box i { font-size: 24px; color: #D4AF37; }
            @media (max-width: 768px) { .container { padding: 25px; } }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1><i class="fas fa-calendar-check"></i> Book a Free Consultation</h1>
            <div class="subtitle"><i class="fas fa-graduation-cap"></i> Get personalized guidance from our study abroad experts</div>
            
            <div class="info-box"><i class="fas fa-clock"></i><p>⏱️ Free 30-minute consultation • 📞 Available via Zoom/WhatsApp/WeChat</p></div>
            
            <form method="POST" action="/appointment">
                <div class="form-group"><label><i class="fas fa-user"></i> Full Name *</label><input type="text" name="name" required placeholder="Enter your full name"></div>
                <div class="form-group"><label><i class="fas fa-envelope"></i> Email *</label><input type="email" name="email" required placeholder="your@email.com"></div>
                <div class="form-group"><label><i class="fab fa-whatsapp"></i> Phone/WhatsApp *</label><input type="tel" name="phone" required placeholder="+86 123 4567 890"></div>
                <div class="form-group"><label><i class="fas fa-globe-asia"></i> Preferred Country *</label>
                    <select name="country" required><option value="">-- Select Country --</option><option value="China">🇨🇳 China</option><option value="Singapore">🇸🇬 Singapore</option><option value="Malaysia">🇲🇾 Malaysia</option><option value="Japan">🇯🇵 Japan</option><option value="Korea">🇰🇷 Korea</option></select>
                </div>
                <div class="form-group"><label><i class="fas fa-calendar-day"></i> Preferred Date</label><input type="date" name="preferred_date"></div>
                <div class="form-group"><label><i class="fas fa-comment"></i> Message / Questions</label><textarea name="message" placeholder="Tell us about your study abroad goals..."></textarea></div>
                <button type="submit"><i class="fas fa-paper-plane"></i> Request Consultation →</button>
            </form>
            
            <a href="/" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Home</a>
        </div>
        <style>
    /* all your existing faq styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''



@app.route('/deadlines')
@login_required
def deadlines():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Application Deadlines - KHARY GLOBAL EDU</title>
    <meta name="description" content="Track application deadlines for top Asian universities. Set reminders for scholarship and admission deadlines.">
    <meta name="keywords" content="university deadlines, application deadlines, scholarship deadlines, study abroad deadlines">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="stylesheet" href="/static/mobile.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #EFF6FF; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        h1 { color: #1E3A8A; font-size: 2.5rem; margin-bottom: 10px; display: flex; align-items: center; gap: 15px; }
        h1 i { color: #D4AF37; font-size: 40px; }
        .subtitle { color: #666; margin-bottom: 30px; padding-bottom: 15px; border-bottom: 2px solid #EFF6FF; }
        .filter-bar { display: flex; gap: 15px; margin-bottom: 30px; flex-wrap: wrap; align-items: center; }
        .filter-bar select, .filter-bar input { padding: 10px 15px; border: 2px solid #E2E8F0; border-radius: 10px; font-size: 14px; outline: none; }
        .filter-bar select:focus, .filter-bar input:focus { border-color: #1E3A8A; }
        .calendar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; background: #1E3A8A; padding: 15px 25px; border-radius: 15px; color: white; }
        .calendar-header button { background: #D4AF37; color: #1E3A8A; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 16px; }
        .calendar-header button:hover { background: white; }
        .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; margin-bottom: 30px; }
        .calendar-day-header { background: #EFF6FF; padding: 12px; text-align: center; font-weight: bold; color: #1E3A8A; border-radius: 8px; }
        .calendar-day { background: white; border: 1px solid #E2E8F0; min-height: 100px; padding: 8px; border-radius: 8px; position: relative; transition: all 0.3s; }
        .calendar-day:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .calendar-day.empty { background: #F8FAFC; }
        .day-number { font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
        .deadline-badge { background: #EF4444; color: white; padding: 3px 6px; border-radius: 4px; font-size: 10px; margin: 2px 0; display: inline-block; cursor: pointer; }
        .deadline-badge.scholarship { background: #D4AF37; color: #1E3A8A; }
        .deadline-badge.admission { background: #3B82F6; }
        .deadline-badge.visa { background: #8B5CF6; }
        .deadline-list { margin-top: 30px; background: #EFF6FF; padding: 20px; border-radius: 15px; }
        .deadline-list h3 { color: #1E3A8A; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .deadline-item { background: white; padding: 15px; margin-bottom: 10px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; border-left: 4px solid #D4AF37; }
        .deadline-item .deadline-date { font-weight: bold; color: #1E3A8A; min-width: 120px; }
        .deadline-item .deadline-title { flex: 1; margin: 0 15px; }
        .deadline-item .deadline-university { color: #666; font-size: 14px; }
        .reminder-btn { background: #D4AF37; color: #1E3A8A; border: none; padding: 5px 12px; border-radius: 20px; cursor: pointer; font-size: 12px; }
        .reminder-btn:hover { background: #1E3A8A; color: white; }
        .newsletter-section { background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 30px; border-radius: 20px; margin-top: 30px; text-align: center; }
        .newsletter-section h3 { font-size: 1.5rem; margin-bottom: 10px; }
        .newsletter-form { display: flex; gap: 10px; justify-content: center; margin-top: 20px; flex-wrap: wrap; }
        .newsletter-form input { padding: 12px 20px; border: none; border-radius: 50px; width: 300px; outline: none; }
        .newsletter-form button { background: #D4AF37; color: #1E3A8A; border: none; padding: 12px 25px; border-radius: 50px; cursor: pointer; font-weight: bold; }
        .back-btn { display: inline-block; margin-top: 20px; background: #1E3A8A; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; }
        @media (max-width: 768px) { .calendar-grid { font-size: 12px; } .calendar-day { min-height: 70px; } .deadline-item { flex-direction: column; gap: 10px; } }
        .reminder-popup { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 30px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); z-index: 1000; max-width: 400px; text-align: center; display: none; }
        .reminder-popup h3 { color: #1E3A8A; margin-bottom: 15px; }
        .reminder-popup input { width: 100%; padding: 10px; margin: 10px 0; border: 2px solid #E2E8F0; border-radius: 8px; }
        .reminder-popup button { background: #1E3A8A; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; margin: 5px; }
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1><i class="fas fa-calendar-alt"></i> Application Deadlines Calendar</h1>
        <div class="subtitle">Track admission, scholarship, and visa deadlines for top Asian universities</div>

        <div class="filter-bar">
            <select id="countryFilter" onchange="filterDeadlines()"><option value="all">All Countries</option><option value="China">🇨🇳 China</option><option value="Singapore">🇸🇬 Singapore</option><option value="Malaysia">🇲🇾 Malaysia</option><option value="Japan">🇯🇵 Japan</option><option value="Korea">🇰🇷 Korea</option></select>
            <select id="typeFilter" onchange="filterDeadlines()"><option value="all">All Types</option><option value="admission">Admission</option><option value="scholarship">Scholarship</option><option value="visa">Visa</option></select>
            <input type="text" id="searchDeadline" placeholder="🔍 Search university..." onkeyup="filterDeadlines()">
        </div>

        <div class="calendar-header"><button onclick="previousMonth()"><i class="fas fa-chevron-left"></i></button><h2 id="monthYear"></h2><button onclick="nextMonth()"><i class="fas fa-chevron-right"></i></button></div>
        <div class="calendar-grid" id="calendarGrid"></div>

        <div class="deadline-list"><h3><i class="fas fa-list"></i> Upcoming Deadlines</h3><div id="upcomingDeadlines"></div></div>

        <div class="newsletter-section"><h3><i class="fas fa-envelope"></i> Get Deadline Alerts</h3><p>Subscribe to receive email reminders about application deadlines and scholarships</p>
            <form class="newsletter-form" id="newsletterForm"><input type="email" id="newsletterEmail" placeholder="Your email address" required><button type="submit"><i class="fas fa-bell"></i> Subscribe to Alerts</button></form>
            <p style="font-size: 12px; margin-top: 10px; opacity: 0.8;">Get reminders 1 week before deadlines</p>
        </div>

        <a href="/" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Home</a>
    </div>

    <div class="overlay" id="reminderOverlay" onclick="closeReminderPopup()"></div>
    <div class="reminder-popup" id="reminderPopup"><h3><i class="fas fa-bell"></i> Set Reminder</h3><p id="reminderTitle"></p><input type="email" id="reminderEmail" placeholder="Your email address"><input type="number" id="reminderDays" placeholder="Days before deadline (default: 7)" value="7"><button onclick="saveReminder()">Set Reminder</button><button onclick="closeReminderPopup()">Cancel</button></div>

    <script>
        let deadlines = [
            { title: "CSC Scholarship Deadline", university: "All Chinese Universities", date: "2026-03-15", type: "scholarship", country: "China" },
            { title: "Peking University Admission", university: "Peking University", date: "2026-05-31", type: "admission", country: "China" },
            { title: "Tsinghua University Admission", university: "Tsinghua University", date: "2026-05-15", type: "admission", country: "China" },
            { title: "NUS Application Deadline", university: "National University of Singapore", date: "2026-03-31", type: "admission", country: "Singapore" },
            { title: "KGSP Scholarship Deadline", university: "Korean Universities", date: "2026-02-28", type: "scholarship", country: "Korea" },
            { title: "MEXT Scholarship Deadline", university: "Japanese Universities", date: "2026-04-30", type: "scholarship", country: "Japan" },
            { title: "NTU Admission Deadline", university: "Nanyang Technological University", date: "2026-04-15", type: "admission", country: "Singapore" },
            { title: "University of Tokyo Admission", university: "University of Tokyo", date: "2026-01-15", type: "admission", country: "Japan" },
            { title: "SNU Admission Deadline", university: "Seoul National University", date: "2026-03-31", type: "admission", country: "Korea" },
            { title: "Visa Application (China)", university: "All Chinese Universities", date: "2026-07-30", type: "visa", country: "China" },
            { title: "KAIST Admission Deadline", university: "KAIST", date: "2026-04-15", type: "admission", country: "Korea" },
            { title: "Fudan University Admission", university: "Fudan University", date: "2026-05-20", type: "admission", country: "China" },
            { title: "Shanghai Jiao Tong Admission", university: "Shanghai Jiao Tong", date: "2026-05-10", type: "admission", country: "China" },
            { title: "Zhejiang University Admission", university: "Zhejiang University", date: "2026-06-15", type: "admission", country: "China" },
            { title: "University of Malaya Admission", university: "University of Malaya", date: "2026-06-30", type: "admission", country: "Malaysia" },
            { title: "Kyoto University Admission", university: "Kyoto University", date: "2026-02-28", type: "admission", country: "Japan" },
            { title: "Yonsei University Admission", university: "Yonsei University", date: "2026-04-30", type: "admission", country: "Korea" },
            { title: "ASEAN Scholarship Deadline", university: "Singapore Universities", date: "2026-03-15", type: "scholarship", country: "Singapore" },
            { title: "Visa Application (Japan)", university: "All Japanese Universities", date: "2026-08-15", type: "visa", country: "Japan" },
            { title: "Visa Application (Korea)", university: "All Korean Universities", date: "2026-08-10", type: "visa", country: "Korea" }
        ];

        let currentDate = new Date();
        let currentMonth = currentDate.getMonth();
        let currentYear = currentDate.getFullYear();

        function renderCalendar() {
            let firstDay = new Date(currentYear, currentMonth, 1);
            let lastDay = new Date(currentYear, currentMonth + 1, 0);
            let startingDay = firstDay.getDay();
            let daysInMonth = lastDay.getDate();
            let calendarHTML = '';
            let weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            for(let day of weekDays) calendarHTML += `<div class="calendar-day-header">${day}</div>`;
            for(let i = 0; i < startingDay; i++) calendarHTML += `<div class="calendar-day empty"></div>`;
            for(let d = 1; d <= daysInMonth; d++) {
                let dateStr = `${currentYear}-${String(currentMonth+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
                let dayDeadlines = deadlines.filter(dl => dl.date === dateStr);
                let badges = '';
                for(let dl of dayDeadlines) badges += `<div class="deadline-badge ${dl.type}" onclick="setReminder('${dl.title}', '${dl.date}')">${dl.title} <i class="fas fa-bell"></i></div>`;
                calendarHTML += `<div class="calendar-day"><div class="day-number">${d}</div>${badges}</div>`;
            }
            document.getElementById('calendarGrid').innerHTML = calendarHTML;
            document.getElementById('monthYear').innerText = `${firstDay.toLocaleString('default', { month: 'long' })} ${currentYear}`;
            renderUpcomingDeadlines();
        }

        function renderUpcomingDeadlines() {
            let today = new Date().toISOString().split('T')[0];
            let upcoming = deadlines.filter(d => d.date >= today).sort((a,b) => a.date.localeCompare(b.date)).slice(0, 10);
            let html = '';
            for(let dl of upcoming) html += `<div class="deadline-item"><div class="deadline-date"><i class="fas fa-calendar"></i> ${dl.date}</div><div class="deadline-title"><strong>${dl.title}</strong><div class="deadline-university">${dl.university}</div></div><button class="reminder-btn" onclick="setReminder('${dl.title}', '${dl.date}')"><i class="fas fa-bell"></i> Remind Me</button></div>`;
            document.getElementById('upcomingDeadlines').innerHTML = html || '<p>No upcoming deadlines</p>';
        }

        function filterDeadlines() { renderCalendar(); }
        function previousMonth() { currentMonth--; if(currentMonth < 0) { currentMonth = 11; currentYear--; } renderCalendar(); }
        function nextMonth() { currentMonth++; if(currentMonth > 11) { currentMonth = 0; currentYear++; } renderCalendar(); }
        
        let currentReminder = {};
        function setReminder(title, date) { currentReminder = { title, date }; document.getElementById('reminderTitle').innerHTML = `<strong>${title}</strong><br>Date: ${date}`; document.getElementById('reminderPopup').style.display = 'block'; document.getElementById('reminderOverlay').style.display = 'block'; }
        function closeReminderPopup() { document.getElementById('reminderPopup').style.display = 'none'; document.getElementById('reminderOverlay').style.display = 'none'; }
        
        function saveReminder() {
            let email = document.getElementById('reminderEmail').value;
            let days = document.getElementById('reminderDays').value;
            if(!email) { alert('Please enter your email'); return; }
            let reminder = { email: email, title: currentReminder.title, date: currentReminder.date, daysBefore: days };
            let reminders = JSON.parse(localStorage.getItem('deadlineReminders') || '[]');
            reminders.push(reminder);
            localStorage.setItem('deadlineReminders', JSON.stringify(reminders));
            alert(`✅ Reminder set! We'll email you ${days} days before ${currentReminder.title}`);
            closeReminderPopup();
        }

        document.getElementById('newsletterForm').addEventListener('submit', function(e) {
            e.preventDefault();
            let email = document.getElementById('newsletterEmail').value;
            let subscribers = JSON.parse(localStorage.getItem('newsletterSubscribers') || '[]');
            if(!subscribers.includes(email)) subscribers.push(email);
            localStorage.setItem('newsletterSubscribers', JSON.stringify(subscribers));
            alert('✅ Subscribed! You will receive deadline alerts and scholarship updates.');
            document.getElementById('newsletterEmail').value = '';
        });

        renderCalendar();
    </script>

    <style>
    /* all your existing deadlines styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>

    <!-- Include main menu and other scripts only once -->
    <script src="/static/main-menu.js"></script>
    <script src="/static/chatbot.js"></script>
    <script src="/static/livechat.js"></script>
    <script src="/static/whatsapp.js"></script>
    <script src="/static/subscribe.js"></script>
    <script src="/static/mobile.js"></script>
</body>
</html>
    '''


@app.route('/sitemap.xml')
def sitemap():
    """Generate sitemap.xml for search engines"""
    base_url = 'https://kharyglobaledu.com'  # Change to your actual domain
    pages = [
        '/', '/about', '/services', '/destinations', '/scholarships', '/contact',
        '/undergraduate', '/graduate', '/phd', '/phd-programs', '/language',
        '/foundation', '/csc-scholarship', '/kgsp-scholarship', '/mext-scholarship',
        '/asean-scholarship', '/malaysia-scholarship', '/faq', '/scholarship-calculator',
        '/team', '/testimonials', '/partners', '/news', '/blog', '/compare', '/appointment',
        '/media', '/deadlines', '/khary-global-edu'
    ]
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        sitemap_xml += f'  <url>\n    <loc>{base_url}{page}</loc>\n    <lastmod>2026-04-16</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    sitemap_xml += '</urlset>'
    return sitemap_xml, 200, {'Content-Type': 'application/xml'}


@app.route('/khary-global-edu/consultations')
@admin_required
def view_consultations():
    try:
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        c.execute('SELECT * FROM consultations ORDER BY created_at DESC')
        consults = c.fetchall()
        conn.close()
        
        if not consults:
            return '''
            <!DOCTYPE html>
            <html>
            <script <head>\n <link rel="canonical" href="https://kharyglobaledu.com">\n <meta name="robots" content="index, follow">src="/static/chatbot.js"></script>
                <title>Consultations - KHARY GLOBAL EDU</title>
                <link rel="stylesheet" href="/static/mobile.css">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
                <style>
                    body { font-family: Arial; background: #EFF6FF; padding: 20px; }
                    .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; text-align: center; }
                    h1 { color: #1E3A8A; }
                    .back { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #1E3A8A; color: white; text-decoration: none; border-radius: 5px; }
                </style>
            </head>
            <script src="/static/mobile.js"></script>
            <body>
                <div class="container">
                    <h1>📋 Consultation Requests</h1>
                    <p>No consultations yet.</p>
                    <a href="/khary-global-edu" class="back">← Back to Admin</a>
                </div>
                
            <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
            </html>
            '''
        
        rows = ""
        for consult in consults:
            rows += f'''
            <tr>
                <td>{consult[1]}</td>
                <td>{consult[2]}</td>
                <td>{consult[3]}</td>
                <td>{consult[4]}</td>
                <td>{consult[5] if consult[5] else 'N/A'}</td>
                <td>{(consult[6][:30] + '...') if consult[6] and len(consult[6]) > 30 else (consult[6] if consult[6] else 'N/A')}</td>
                <td>{consult[8][:10] if len(consult) > 8 else 'N/A'}</td>
            </tr>
            '''
        
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Consultations - KHARY GLOBAL EDU</title>
            <link rel="stylesheet" href="/static/mobile.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            <style>
                body {{ font-family: Arial; background: #EFF6FF; padding: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }}
                h1 {{ color: #1E3A8A; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th {{ background: #1E3A8A; color: white; padding: 10px; }}
                td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
                .back {{ display: inline-block; margin-top: 20px; padding: 10px 20px; background: #1E3A8A; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <script src="/static/mobile.js"></script>
        <body>
            <div class="container">
                <h1>📋 Consultation Requests</h1>
                <p>Total: {len(consults)} requests</p>
                <table>
                    <tr><th>Name</th><th>Email</th><th>Phone</th><th>Country</th><th>Preferred Date</th><th>Message</th><th>Created</th></tr>
                    {rows}
                </table>
                <a href="/khary-global-edu" class="back">← Back to Admin</a>
            </div>
            
        <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
        </html>
        '''
    except Exception as e:
        return f"<h3>Error loading consultations: {e}</h3><a href='/khary-global-edu'>Back to Admin</a>"




@app.route('/khary-global-edu/reply-chat')
@admin_required
def reply_chat():
    return '''
    <!DOCTYPE html>
    <html>
   <head>
        <title>Reply to Live Chats - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Arial; background: #EFF6FF; padding: 20px; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
            h1 { color: #1E3A8A; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
            .chat-list { margin-top: 20px; }
            .chat-item { background: #F8FAFC; border-radius: 15px; padding: 20px; margin-bottom: 20px; border-left: 4px solid #10B981; }
            .chat-header { display: flex; justify-content: space-between; margin-bottom: 10px; color: #666; font-size: 12px; }
            .chat-messages { background: white; border-radius: 10px; padding: 15px; margin-bottom: 15px; max-height: 250px; overflow-y: auto; }
            .student-msg { background: #EFF6FF; color: #1E3A8A; padding: 10px; border-radius: 10px; margin: 8px 0; border-left: 3px solid #1E3A8A; }
            .admin-msg { background: #ECFDF5; color: #10B981; padding: 10px; border-radius: 10px; margin: 8px 0; border-left: 3px solid #10B981; }
            .reply-area { display: flex; gap: 10px; margin-top: 15px; }
            .reply-input { flex: 1; padding: 12px; border: 1px solid #E2E8F0; border-radius: 8px; outline: none; font-size: 14px; }
            .reply-btn { background: #10B981; color: white; border: none; padding: 12px 25px; border-radius: 8px; cursor: pointer; font-weight: bold; }
            .reply-btn:hover { background: #059669; }
            .back { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #1E3A8A; color: white; text-decoration: none; border-radius: 8px; }
            .refresh-btn { background: #D4AF37; color: #1E3A8A; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
            .refresh-btn:hover { background: #c49b2c; }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1><i class="fas fa-headset"></i> Live Chat Management</h1>
            <p>View and reply to student messages</p>
            
            <div style="margin-bottom: 20px;">
                <button onclick="refreshChats()" class="refresh-btn"><i class="fas fa-sync-alt"></i> Refresh</button>
            </div>
            
            <div id="chats-container" class="chat-list">
                <div style="text-align: center; padding: 40px;">Loading messages...</div>
            </div>
            
            <a href="/khary-global-edu" class="back"><i class="fas fa-arrow-left"></i> Back to Admin</a>
        </div>
        
        <script>
            let currentChats = {};
            
            function renderChats(users) {
                let container = document.getElementById('chats-container');
                container.innerHTML = '';
                
                if(Object.keys(users).length === 0) {
                    container.innerHTML = '<div style="text-align: center; padding: 40px;">No messages yet</div>';
                    return;
                }
                
                for(let userId in users) {
                    let messages = users[userId];
                    let messagesHtml = '';
                    
                    for(let i = 0; i < messages.length; i++) {
                        let m = messages[i];
                        let time = new Date(m.timestamp).toLocaleTimeString();
                        if(m.isAdmin) {
                            messagesHtml += `<div class="admin-msg"><strong>👨‍💼 Admin:</strong> ${escapeHtml(m.message)} <span style="font-size: 10px; color: #999; float: right;">${time}</span></div>`;
                        } else {
                            messagesHtml += `<div class="student-msg"><strong>👤 Student:</strong> ${escapeHtml(m.message)} <span style="font-size: 10px; color: #999; float: right;">${time}</span></div>`;
                        }
                    }
                    
                    let lastMsg = messages[messages.length - 1];
                    let lastTime = new Date(lastMsg.timestamp).toLocaleString();
                    
                    let chatDiv = document.createElement('div');
                    chatDiv.className = 'chat-item';
                    chatDiv.id = 'chat-' + userId;
                    chatDiv.innerHTML = `
                        <div class="chat-header">
                            <span><i class="fas fa-user-circle"></i> <strong>User:</strong> ${userId.substring(0, 25)}...</span>
                            <span><i class="far fa-clock"></i> Last: ${lastTime}</span>
                        </div>
                        <div class="chat-messages" id="messages-${userId}">
                            ${messagesHtml}
                        </div>
                        <div class="reply-area">
                            <input type="text" id="reply-${userId}" class="reply-input" placeholder="Type your reply here..." onkeypress="if(event.key==='Enter') sendReply('${userId}')">
                            <button class="reply-btn" onclick="sendReply('${userId}')"><i class="fas fa-paper-plane"></i> Send Reply</button>
                        </div>
                    `;
                    container.appendChild(chatDiv);
                    
                    if(currentChats[userId]) {
                        let oldInput = document.getElementById('reply-' + userId);
                        if(oldInput && currentChats[userId].inputValue) {
                            oldInput.value = currentChats[userId].inputValue;
                        }
                    }
                }
            }
            
            function escapeHtml(text) {
                let div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }
            
            function saveInputValues() {
                let allMessages = JSON.parse(localStorage.getItem('liveChatMessages') || '[]');
                let users = {};
                allMessages.forEach(msg => {
                    if(!users[msg.userId]) users[msg.userId] = [];
                    users[msg.userId].push(msg);
                });
                
                for(let userId in users) {
                    let input = document.getElementById('reply-' + userId);
                    if(input) {
                        if(!currentChats[userId]) currentChats[userId] = {};
                        currentChats[userId].inputValue = input.value;
                    }
                }
            }
            
            function refreshChats() {
                saveInputValues();
                
                let allMessages = JSON.parse(localStorage.getItem('liveChatMessages') || '[]');
                let users = {};
                allMessages.forEach(msg => {
                    if(!users[msg.userId]) users[msg.userId] = [];
                    users[msg.userId].push(msg);
                });
                
                renderChats(users);
            }
            
            function sendReply(userId) {
                let replyInput = document.getElementById('reply-' + userId);
                let reply = replyInput.value.trim();
                if(!reply) {
                    alert('Please type a reply first');
                    return;
                }
                
                let allMessages = JSON.parse(localStorage.getItem('liveChatMessages') || '[]');
                
                allMessages.push({
                    userId: userId,
                    message: reply,
                    isAdmin: true,
                    timestamp: new Date().toISOString(),
                    read: false
                });
                
                localStorage.setItem('liveChatMessages', JSON.stringify(allMessages));
                
                if(currentChats[userId]) {
                    delete currentChats[userId];
                }
                
                refreshChats();
                
                let notification = document.createElement('div');
                notification.style.position = 'fixed';
                notification.style.bottom = '20px';
                notification.style.right = '20px';
                notification.style.background = '#10B981';
                notification.style.color = 'white';
                notification.style.padding = '12px 24px';
                notification.style.borderRadius = '10px';
                notification.style.zIndex = '9999';
                notification.style.fontWeight = 'bold';
                notification.innerHTML = '✅ Reply sent to student!';
                document.body.appendChild(notification);
                setTimeout(() => notification.remove(), 2000);
            }
            
            refreshChats();
        </script>

        <style>
    /* all your existing faq styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>


    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''

@app.route('/resources')
@login_required
def resources():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Downloadable Resources - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #EFF6FF; padding: 20px; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px; }
            h1 { color: #1E3A8A; font-size: 2rem; margin-bottom: 10px; display: flex; align-items: center; gap: 10px; }
            h1 i { color: #D4AF37; }
            .subtitle { color: #666; margin-bottom: 30px; border-bottom: 2px solid #EFF6FF; padding-bottom: 15px; }
            .resources-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px; margin-top: 30px; }
            .resource-card { background: #F8FAFC; border-radius: 15px; padding: 20px; transition: all 0.3s; border: 1px solid #E2E8F0; }
            .resource-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-color: #D4AF37; }
            .resource-icon { font-size: 50px; color: #1E3A8A; margin-bottom: 15px; }
            .resource-title { font-size: 1.2rem; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
            .resource-desc { color: #666; font-size: 14px; margin-bottom: 15px; }
            .download-btn { background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; font-size: 14px; transition: all 0.3s; }
            .download-btn:hover { background: #D4AF37; color: #1E3A8A; transform: translateY(-2px); }
            .back-btn { display: inline-block; background: #1E3A8A; color: white; padding: 12px 25px; text-decoration: none; border-radius: 8px; margin-top: 30px; }
            @media (max-width: 768px) { .resources-grid { grid-template-columns: 1fr; } }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1><i class="fas fa-download"></i> Downloadable Resources</h1>
            <div class="subtitle">Free guides and checklists to help you study abroad</div>
            
            <div class="resources-grid">
                <div class="resource-card"><div class="resource-icon"><i class="fas fa-file-pdf"></i></div><div class="resource-title">📘 Complete Scholarship Guide</div><div class="resource-desc">Learn about CSC, KGSP, MEXT, ASEAN scholarships - requirements, deadlines, application tips</div><button class="download-btn" onclick="downloadResource('scholarship-guide')"><i class="fas fa-download"></i> Download PDF</button></div>
                <div class="resource-card"><div class="resource-icon"><i class="fas fa-file-pdf"></i></div><div class="resource-title">📝 Application Checklist</div><div class="resource-desc">Step-by-step checklist for university applications - all documents you need</div><button class="download-btn" onclick="downloadResource('application-checklist')"><i class="fas fa-download"></i> Download PDF</button></div>
                <div class="resource-card"><div class="resource-icon"><i class="fas fa-file-pdf"></i></div><div class="resource-title">🎫 Visa Guide 2026</div><div class="resource-desc">Complete visa process for China, Singapore, Malaysia, Japan, Korea</div><button class="download-btn" onclick="downloadResource('visa-guide')"><i class="fas fa-download"></i> Download PDF</button></div>
                <div class="resource-card"><div class="resource-icon"><i class="fas fa-file-pdf"></i></div><div class="resource-title">💰 Budget Planner</div><div class="resource-desc">Calculate your tuition + living expenses + create monthly budget</div><button class="download-btn" onclick="downloadResource('budget-planner')"><i class="fas fa-download"></i> Download PDF</button></div>
                <div class="resource-card"><div class="resource-icon"><i class="fas fa-file-pdf"></i></div><div class="resource-title">🌏 Country Comparison Guide</div><div class="resource-desc">Compare China, Singapore, Malaysia, Japan, Korea - costs, rankings, lifestyle</div><button class="download-btn" onclick="downloadResource('country-guide')"><i class="fas fa-download"></i> Download PDF</button></div>
                <div class="resource-card"><div class="resource-icon"><i class="fas fa-file-pdf"></i></div><div class="resource-title">📖 Statement of Purpose Guide</div><div class="resource-desc">How to write a winning SOP - templates and examples included</div><button class="download-btn" onclick="downloadResource('sop-guide')"><i class="fas fa-download"></i> Download PDF</button></div>
            </div>
            
            <a href="/" class="back-btn"><i class="fas fa-arrow-left"></i> Back to Home</a>
        </div>
        <style>
    /* all your existing downloadable ressources styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } 
        <script>
            function downloadResource(type) {
                let content = '';
                let filename = '';
                
                switch(type) {
                    case 'scholarship-guide':
                        content = `KHARY GLOBAL EDU - COMPLETE SCHOLARSHIP GUIDE\n\nCSC Scholarship (China):\n• Full tuition waiver\n• Free accommodation\n• Monthly stipend: 3,000-3,500 RMB\n• Deadline: January-March\n\nKGSP Scholarship (Korea):\n• Full tuition\n• Monthly stipend: 1,000,000 KRW\n• Airfare reimbursement\n• Deadline: February-March\n\nMEXT Scholarship (Japan):\n• Full tuition\n• Monthly stipend: 117,000-145,000 JPY\n• Deadline: April-May\n\nASEAN Scholarship (Singapore):\n• Full tuition at NUS/NTU/SMU\n• Living allowance: SGD 5,800/year\n• Deadline: February-March\n\nFor assistance contact: kharyglobal@gmail.com`;
                        filename = 'scholarship_guide.pdf';
                        break;
                    case 'application-checklist':
                        content = `KHARY GLOBAL EDU - APPLICATION CHECKLIST\n\nRequired Documents:\n✓ Academic transcripts (all years)\n✓ Degree certificates/High school diploma\n✓ Language test scores (IELTS/TOEFL/HSK/JLPT/TOPIK)\n✓ Passport copy (valid for 1+ years)\n✓ Statement of Purpose\n✓ Recommendation letters (2-3)\n✓ Bank statement (financial proof)\n✓ Medical examination report\n✓ Passport photos (4-6)\n✓ CV/Resume (for graduate programs)\n\nContact us for assistance: kharyglobal@gmail.com`;
                        filename = 'application_checklist.pdf';
                        break;
                    case 'visa-guide':
                        content = `KHARY GLOBAL EDU - STUDENT VISA GUIDE\n\nChina Student Visa (X1/X2):\n• JW202 form from university\n• Admission letter\n• Medical examination\n• Financial proof ($5,000+)\n• Processing: 4-6 weeks\n\nSingapore Student Pass:\n• SOLAR application\n• Medical report\n• Financial proof (SGD 20,000+)\n• Processing: 2-4 weeks\n\nMalaysia Student Visa:\n• VAL application\n• Medical exam\n• Financial proof (RM 15,000+)\n• Processing: 4-8 weeks\n\nJapan Student Visa:\n• COE (Certificate of Eligibility)\n• Financial proof (JPY 2,000,000+)\n• Study plan\n• Processing: 1-3 months\n\nKorea Student Visa (D-2):\n• Admission letter\n• Financial proof (KRW 20,000,000+)\n• Health certificate\n• Processing: 2-4 weeks\n\nFor personalized assistance: kharyglobal@gmail.com`;
                        filename = 'visa_guide.pdf';
                        break;
                    case 'budget-planner':
                        content = `KHARY GLOBAL EDU - BUDGET PLANNER\n\nEstimated Annual Costs:\n\nChina:\nTuition: $3,000 - $6,000\nLiving: $3,000 - $5,000\nTotal: $6,000 - $11,000/year\n\nSingapore:\nTuition: $22,000 - $30,000\nLiving: $10,000 - $15,000\nTotal: $32,000 - $45,000/year\n\nMalaysia:\nTuition: $2,500 - $5,300\nLiving: $3,000 - $4,000\nTotal: $5,500 - $9,300/year\n\nJapan:\nTuition: $3,600 - $5,000\nLiving: $8,000 - $12,000\nTotal: $11,600 - $17,000/year\n\nKorea:\nTuition: $3,800 - $6,000\nLiving: $6,000 - $9,000\nTotal: $9,800 - $15,000/year\n\nMonthly Budget Template:\n✓ Rent: $200-800\n✓ Food: $150-400\n✓ Transport: $30-100\n✓ Phone/Internet: $20-50\n✓ Entertainment: $50-150\n✓ Miscellaneous: $50-100\n\nCalculate your personalized budget with us!`;
                        filename = 'budget_planner.pdf';
                        break;
                    case 'country-guide':
                        content = `KHARY GLOBAL EDU - COUNTRY COMPARISON GUIDE\n\nQuick Comparison:\n\n| Feature | China | Singapore | Malaysia | Japan | Korea |\n|---------|-------|-----------|----------|-------|-------|\n| Tuition | $3-6k | $22-30k | $2.5-5.3k | $3.6-5k | $3.8-6k |\n| Living | $3-5k | $10-15k | $3-4k | $8-12k | $6-9k |\n| Duration | 4 yrs | 3-4 yrs | 3-4 yrs | 4 yrs | 4 yrs |\n| Language | Chinese | English | English | Japanese | Korean |\n| Scholarship | CSC | ASEAN | MIS | MEXT | KGSP |\n\nBest For:\n• China: Engineering, Computer Science\n• Singapore: Business, Technology\n• Malaysia: Affordable education\n• Japan: Technology, Research\n• Korea: K-Pop, Technology\n\nContact us for personalized guidance!`;
                        filename = 'country_comparison_guide.pdf';
                        break;
                    case 'sop-guide':
                        content = `KHARY GLOBAL EDU - STATEMENT OF PURPOSE GUIDE\n\nSOP Structure:\n\n1. Introduction (10%)\n• Your motivation to study abroad\n• Brief introduction of yourself\n\n2. Academic Background (20%)\n• Your previous degrees\n• Relevant coursework\n• Academic achievements\n\n3. Professional Experience (20%)\n• Internships/work experience\n• Skills developed\n• Projects completed\n\n4. Why This Program (20%)\n• Specific program features\n• Why this university\n• How it fits your goals\n\n5. Future Goals (20%)\n• Short-term goals\n• Long-term career plans\n• How you'll contribute\n\n6. Conclusion (10%)\n• Summary of key points\n• Expression of gratitude\n\nTips:\n✓ Be authentic\n✓ Show passion\n✓ Be specific\n✓ Proofread multiple times\n✓ Keep it 500-1000 words\n\nNeed help? Contact us for SOP review!`;
                        filename = 'sop_guide.pdf';
                        break;
                    default: return;
                }
                
                const blob = new Blob([content], { type: 'application/pdf' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                alert('✅ Download started!');
            }
        </script>
        <style>
    /* all your existing faq styles here */
    
    /* then add this at the bottom */
    #khary-main-menu,
    #khary-main-menu .menu-btn,
    #khary-main-menu .menu-dropdown {
        background: #1E3A8A !important;
        color: white !important;
    }
    
    #khary-main-menu .menu-icon i {
        color: #D4AF37 !important;
    }
    
    #khary-main-menu .menu-btn {
        color: white !important;
    }
    
    #khary-main-menu .dropdown-content a {
        color: #1E3A8A !important;
        background: white !important;
    }
    
    #khary-main-menu .dropdown-icon i {
        color: #1E3A8A !important;
    } ... I NEED TO USE TO ALL 
</style>
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''


import hashlib
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect('/login?next=' + request.url)
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def send_verification_email(email, name, code):
    try:
        COMPANY_EMAIL = "kharyglobal@gmail.com"
        COMPANY_EMAIL_PASSWORD = "hdgc xavr ixwq kgaj"
        
        msg = MIMEMultipart()
        msg['From'] = COMPANY_EMAIL
        msg['To'] = email
        msg['Subject'] = "Verify Your Email - KHARY GLOBAL EDU"
        
        body = f"""
        Dear {name},
        
        Welcome to KHARY GLOBAL EDU!
        
        Please verify your email by clicking the link below:
        http://localhost:5000/verify-email?code={code}&email={email}
        
        If you didn't create an account, please ignore this email.
        
        Best regards,
        KHARY GLOBAL EDU Team
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(COMPANY_EMAIL, COMPANY_EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


    # GET request - show registration form
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Register - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Arial; background: linear-gradient(135deg, #EFF6FF, #DBEAFE); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
            .container { max-width: 500px; width: 100%; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
            h1 { color: #1E3A8A; text-align: center; margin-bottom: 30px; display: flex; align-items: center; justify-content: center; gap: 10px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 8px; font-weight: bold; color: #1E3A8A; }
            input, select { width: 100%; padding: 12px; border: 2px solid #E2E8F0; border-radius: 10px; font-size: 14px; transition: all 0.3s; }
            input:focus, select:focus { outline: none; border-color: #D4AF37; }
            button { width: 100%; background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 14px; border: none; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; transition: all 0.3s; }
            button:hover { background: #D4AF37; color: #1E3A8A; transform: translateY(-2px); }
            .login-link { text-align: center; margin-top: 20px; }
            .login-link a { color: #1E3A8A; text-decoration: none; }
            .login-link a:hover { text-decoration: underline; }
        </style>
    </head>
    <script src="/static/mobile.js"></script>
    <body>
        <div class="container">
            <h1><i class="fas fa-user-plus"></i> Create Account</h1>
            <form method="POST">
                <div class="form-group"><label><i class="fas fa-user"></i> Full Name</label><input type="text" name="full_name" required placeholder="Enter your full name"></div>
                <div class="form-group"><label><i class="fas fa-envelope"></i> Email</label><input type="email" name="email" required placeholder="your@email.com"></div>
                <div class="form-group"><label><i class="fas fa-lock"></i> Password</label><input type="password" name="password" required placeholder="Min 6 characters"></div>
                <div class="form-group"><label><i class="fas fa-lock"></i> Confirm Password</label><input type="password" name="confirm_password" required placeholder="Confirm password"></div>
                <div class="form-group"><label><i class="fas fa-phone"></i> Phone/WhatsApp</label><input type="tel" name="phone" placeholder="+86 123 4567 890"></div>
                <div class="form-group"><label><i class="fas fa-globe-asia"></i> Country</label>
                    <select name="country"><option value="">Select Country</option><option>Kenya</option><option>Nigeria</option><option>Egypt</option><option>South Africa</option><option>Ghana</option><option>Uganda</option><option>Tanzania</option><option>Ethiopia</option><option>Other</option></select>
                </div>
                <div class="form-group"><label><i class="fas fa-graduation-cap"></i> Education Level</label>
                    <select name="education_level"><option value="">Select Level</option><option>High School</option><option>Bachelor's</option><option>Master's</option><option>PhD</option></select>
                </div>
                <button type="submit"><i class="fas fa-paper-plane"></i> Register</button>
            </form>
            <div class="login-link">Already have an account? <a href="/login">Login here</a></div>
<a href="/forgot-password" style="display: block; margin-top: 15px; color: #666;">Forgot Password?</a>
        </div>
    <script src="/static/main-menu.js"></script>
<script src="/static/chatbot.js"></script>
<script src="/static/livechat.js"></script>
<script src="/static/whatsapp.js"></script>
<script src="/static/subscribe.js"></script>
<script src="/static/mobile.js"></script>
</body>
    </html>
    '''


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'khary' and password == 'khary2024':
            session['admin_logged_in'] = True
            return redirect('/khary-global-edu')
        else:
            return '<h3>Invalid credentials. <a href="/admin-login">Try again</a></h3>'
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin Login - KHARY GLOBAL EDU</title>
        <style>
            body { font-family: Arial; background: #EFF6FF; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .login-container { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); width: 350px; text-align: center; }
            h1 { color: #1E3A8A; margin-bottom: 20px; }
            input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
            button { width: 100%; background: #1E3A8A; color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
            button:hover { background: #D4AF37; color: #1E3A8A; }
            .back { margin-top: 15px; display: block; color: #666; text-decoration: none; }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>🔐 Admin Login</h1>
            <form method="POST">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <a href="/" class="back">← Back to Home</a>
        </div>
    </body>
    </html>
    '''

@app.route('/check-admin-status')
def check_admin_status():
    import json
    return json.dumps({'isAdmin': session.get('admin_logged_in', False)}), 200, {'Content-Type': 'application/json'}

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect('/')
    
# ==================== FORGOT PASSWORD ====================
import secrets
from datetime import datetime, timedelta

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        conn = sqlite3.connect('applications.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        
        if user:
            # Generate reset token
            reset_token = secrets.token_hex(32)
            expiry = datetime.now() + timedelta(hours=1)
            
            c.execute("UPDATE users SET reset_token = ?, reset_expiry = ? WHERE id = ?", 
                     (reset_token, expiry, user[0]))
            conn.commit()
            
            # Send reset email
            try:
                send_reset_email(email, reset_token)
                msg = "Password reset link sent to your email!"
            except Exception as e:
                msg = "Error sending email. Please try again."
        else:
            msg = "If that email exists, a reset link has been sent."
        
        conn.close()
        return f'<h3>{msg}</h3><a href="/login">Back to Login</a>'
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Forgot Password - KHARY GLOBAL EDU</title>
        <link rel="stylesheet" href="/static/mobile.css">
        <style>
            body { font-family: Arial; background: #EFF6FF; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .container { background: white; padding: 40px; border-radius: 20px; width: 350px; text-align: center; }
            h1 { color: #1E3A8A; }
            input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; }
            button { background: #1E3A8A; color: white; padding: 12px; border: none; border-radius: 8px; width: 100%; cursor: pointer; }
            .back { margin-top: 15px; display: block; color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Forgot Password</h1>
            <p>Enter your email to reset your password</p>
            <form method="POST">
                <input type="email" name="email" placeholder="Your email" required>
                <button type="submit">Send Reset Link</button>
            </form>
            <a href="/login" class="back">← Back to Login</a>
        </div>
    </body>
    </html>
    '''

def send_reset_email(email, token):
    """Send password reset email"""
    try:
        COMPANY_EMAIL = "kharyglobal@gmail.com"
        COMPANY_EMAIL_PASSWORD = "hdgc xavr ixwq kgaj"
        
        reset_link = f"http://localhost:5000/reset-password?token={token}"
        
        msg = MIMEMultipart()
        msg['From'] = COMPANY_EMAIL
        msg['To'] = email
        msg['Subject'] = "Password Reset - KHARY GLOBAL EDU"
        
        body = f"""
        Hello,
        
        You requested to reset your password.
        
        Click the link below to reset your password (valid for 1 hour):
        {reset_link}
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        KHARY GLOBAL EDU Team
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(COMPANY_EMAIL, COMPANY_EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Reset email sent to {email}")
        return True
    except Exception as e:
        print(f"❌ Reset email error: {e}")
        return False

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token')
    
    if not token:
        return '<h3>Invalid or missing token</h3><a href="/forgot-password">Try again</a>'
    
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    c.execute("SELECT id, email FROM users WHERE reset_token = ? AND reset_expiry > ?", 
             (token, datetime.now()))
    user = c.fetchone()
    
    if not user:
        conn.close()
        return '<h3>Invalid or expired token</h3><a href="/forgot-password">Try again</a>'
    
    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            return '<h3>Passwords do not match</h3><a href="/reset-password?token=' + token + '">Try again</a>'
        
        if len(new_password) < 6:
            return '<h3>Password must be at least 6 characters</h3><a href="/reset-password?token=' + token + '">Try again</a>'
        
        hashed_password = generate_password_hash(new_password)
        
        c.execute("UPDATE users SET password = ?, reset_token = NULL, reset_expiry = NULL WHERE id = ?", 
                 (hashed_password, user[0]))
        conn.commit()
        conn.close()
        
        return '''
        <!DOCTYPE html>
        <html>
        <head><title>Password Reset - KHARY GLOBAL EDU</title></head>
        <body style="font-family:Arial; text-align:center; padding:50px;">
            <h1 style="color:#1E3A8A;">✅ Password Reset Successful!</h1>
            <p>You can now login with your new password.</p>
            <a href="/login" style="background:#1E3A8A; color:white; padding:10px 20px; text-decoration:none; border-radius:5px;">Login Now</a>
        </body>
        </html>
        '''
    
    conn.close()
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reset Password - KHARY GLOBAL EDU</title>
        <style>
            body { font-family: Arial; background: #EFF6FF; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .container { background: white; padding: 40px; border-radius: 20px; width: 350px; text-align: center; }
            h1 { color: #1E3A8A; }
            input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; }
            button { background: #1E3A8A; color: white; padding: 12px; border: none; border-radius: 8px; width: 100%; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Reset Password</h1>
            <form method="POST">
                <input type="password" name="password" placeholder="New password" required>
                <input type="password" name="confirm_password" placeholder="Confirm password" required>
                <button type="submit">Reset Password</button>
            </form>
        </div>
    </body>
    </html>
    '''    

@app.errorhandler(413)
def too_large(e):
    return "<h3>File too large! Maximum size is 16MB.</h3><a href='/'>Back to Home</a>", 413


@app.route('/api/articles')
def api_articles_old():
    from flask import jsonify
    articles = [
        {"id": 1, "title": "How to Apply for CSC Scholarship", "country": "China", "content": "Step by step guide...", "image": "/static/khary-profile.jpg"},
        {"id": 2, "title": "Top Universities in Singapore", "country": "Singapore", "content": "NUS, NTU, SMU guide...", "image": "/static/khary-profile.jpg"},
        {"id": 3, "title": "Part Time Jobs in Malaysia", "country": "Malaysia", "content": "Working while studying...", "image": "/static/khary-profile.jpg"}
    ]
    return jsonify(articles)

@app.route('/blog')
def blog():
    return render_template('blog.html')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM blog_posts")
    total = c.fetchone()[0]
    
    c.execute("SELECT * FROM blog_posts LIMIT ? OFFSET ?", (per_page, offset))
    posts = c.fetchall()
    conn.close()
    
    return render_template('blog.html', posts=posts, page=page, total=total)

@app.route('/china')
def china():
    return home_with_country('china', '🇨🇳 China')

@app.route('/singapore')
def singapore():
    return home_with_country('singapore', '🇸🇬 Singapore')

@app.route('/malaysia')
def malaysia():
    return home_with_country('malaysia', '🇲🇾 Malaysia')

@app.route('/japan')
def japan():
    return home_with_country('japan', '🇯🇵 Japan')

@app.route('/korea')
def korea():
    return home_with_country('korea', '🇰🇷 Korea')

def home_with_country(country, country_name):
    # Get university data
    if country == 'china':
        universities = china_universities
    elif country == 'singapore':
        universities = singapore_universities
    elif country == 'malaysia':
        universities = malaysia_universities
    elif country == 'japan':
        universities = japan_universities
    elif country == 'korea':
        universities = korea_universities
    else:
        universities = []
    
    # Build HTML for universities
    university_html = ''
    for uni in universities:
        university_html += f'''
        <div class="university-card">
            <div class="university-card-header">
                <h3>{uni['name']}</h3>
                <div class="ranking">{uni['ranking']}</div>
            </div>
            <div class="university-card-body">
                <div class="info-item"><strong>📍 Location:</strong> {uni['location']}</div>
                <div class="info-item"><strong>📅 Established:</strong> {uni['established']}</div>
                <div class="info-item"><strong>👥 Students:</strong> {uni['students']}</div>
                <p><em>{uni['description']}</em></p>
                <button class="btn" onclick="showApplication('{uni['name']}', '{country_name.split(' ')[1]}')">Apply Now</button>
            </div>
        </div>
        '''
    
    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Study in {country_name} - KHARY GLOBAL EDU</title>
    <link rel="stylesheet" href="/static/mobile.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: #EFF6FF; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
        .university-header {{ background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 40px; text-align: center; border-radius: 20px; margin-bottom: 30px; }}
        .university-header .flag {{ font-size: 60px; }}
        .university-header h1 {{ font-size: 2.5rem; margin: 10px 0; }}
        .university-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 25px; }}
        .university-card {{ background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        .university-card-header {{ background: #1E3A8A; color: white; padding: 20px; position: relative; }}
        .university-card-header h3 {{ font-size: 1.3rem; }}
        .ranking {{ background: #D4AF37; color: #1E3A8A; display: inline-block; padding: 3px 12px; border-radius: 20px; margin-top: 10px; font-size: 0.8rem; font-weight: bold; }}
        .university-card-body {{ padding: 20px; }}
        .info-item {{ margin: 10px 0; padding: 10px; background: #EFF6FF; border-radius: 8px; }}
        .btn {{ background: #D4AF37; color: #1E3A8A; border: none; padding: 12px; border-radius: 8px; cursor: pointer; width: 100%; font-weight: bold; margin-top: 15px; }}
        .back-button {{ display: inline-block; background: #1E3A8A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 8px; margin-top: 20px; }}
        .footer {{ background: #1F2937; color: white; text-align: center; padding: 30px; margin-top: 40px; border-radius: 20px; }}
        @media (max-width: 768px) {{ .university-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <script src="/static/main-menu.js"></script>
    
    <div class="container">
        <div class="university-header">
            <div class="flag">{country_name.split(' ')[0]}</div>
            <h1>Study in {country_name.split(' ')[1]}</h1>
            <p>{len(universities)} Top Universities</p>
        </div>
        
        <button class="back-button" onclick="location.href='/'">← Back to Home</button>
        
        <div class="university-grid">
            {university_html}
        </div>
    </div>
    
    <footer class="footer">
        <div class="container">
            <p>© 2025 KHARY GLOBAL EDU. All rights reserved.</p>
            <p>Study Abroad Guidance for Asian Universities</p>
        </div>
    </footer>
    
    <script src="/static/chatbot.js"></script>
    <script src="/static/whatsapp.js"></script>
    <script src="/static/subscribe.js"></script>
    
    <script>
    function showApplication(university, country) {{
        alert('Apply to ' + university + ' in ' + country);
    }}
    </script>
</body>
</html>
    '''

@app.route('/destinations')
def redirect_destinations():
    return redirect('/')

@app.route('/programs')
def redirect_programs():
    return redirect('/undergraduate')

@app.route('/scholarships')
def redirect_scholarships():
    return redirect('/csc-scholarship')

@app.route('/contact')
def redirect_contact():
    return redirect('/contact-us')  # or create a real contact page


@app.route('/destinations')
def destinations_page():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Study Destinations</title><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body{font-family:Arial;background:#EFF6FF;margin:0;padding:20px}
        .container{max-width:1200px;margin:0 auto;background:white;padding:40px;border-radius:20px}
        h1{color:#1E3A8A;text-align:center}
        .country-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:20px;margin-top:30px}
        .country-card{background:#EFF6FF;padding:30px;text-align:center;border-radius:15px;text-decoration:none;display:block}
        .flag{font-size:50px}
        h3{color:#1E3A8A}
        .back-btn{display:inline-block;margin-top:30px;background:#1E3A8A;color:white;padding:10px20px;text-decoration:none;border-radius:8px}
        @media(max-width:768px){.country-grid{grid-template-columns:repeat(2,1fr)}}
    </style>
    </head>
    <body>
        <div class="container">
            <h1>🌏 Study Destinations</h1>
            <div class="country-grid">
                <a href="/china" class="country-card"><div class="flag">🇨🇳</div><h3>China</h3><p>30 Universities</p></a>
                <a href="/singapore" class="country-card"><div class="flag">🇸🇬</div><h3>Singapore</h3><p>30 Universities</p></a>
                <a href="/malaysia" class="country-card"><div class="flag">🇲🇾</div><h3>Malaysia</h3><p>30 Universities</p></a>
                <a href="/japan" class="country-card"><div class="flag">🇯🇵</div><h3>Japan</h3><p>30 Universities</p></a>
                <a href="/korea" class="country-card"><div class="flag">🇰🇷</div><h3>Korea</h3><p>30 Universities</p></a>
            </div>
            <div style="text-align:center"><a href="/" class="back-btn">← Back to Home</a></div>
        </div>
        <script src="/static/main-menu.js"></script>
    </body>
    </html>
    '''

@app.route('/programs')
def programs_page():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Programs</title><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body{font-family:Arial;background:#EFF6FF;margin:0;padding:20px}
        .container{max-width:1000px;margin:0 auto;background:white;padding:40px;border-radius:20px}
        h1{color:#1E3A8A;text-align:center}
        .program-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:30px}
        .program-card{background:#EFF6FF;padding:25px;border-radius:15px;text-align:center}
        .program-card h3{color:#1E3A8A}
        .btn{display:inline-block;margin-top:15px;background:#1E3A8A;color:white;padding:8px20px;text-decoration:none;border-radius:25px}
        .back-btn{display:inline-block;margin-top:30px;background:#1E3A8A;color:white;padding:10px20px;text-decoration:none;border-radius:8px}
        @media(max-width:768px){.program-grid{grid-template-columns:1fr}}
    </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Academic Programs</h1>
            <div class="program-grid">
                <div class="program-card"><h3>🎯 Foundation</h3><p>1-year preparatory courses</p><a href="/foundation" class="btn">Learn More</a></div>
                <div class="program-card"><h3>📘 Undergraduate</h3><p>Bachelor's degrees</p><a href="/undergraduate" class="btn">Learn More</a></div>
                <div class="program-card"><h3>📙 Graduate</h3><p>Master's degrees</p><a href="/graduate" class="btn">Learn More</a></div>
                <div class="program-card"><h3>🔬 PhD</h3><p>Doctoral degrees</p><a href="/phd-programs" class="btn">Learn More</a></div>
                <div class="program-card"><h3>🗣️ Language</h3><p>HSK, JLPT, TOPIK</p><a href="/language" class="btn">Learn More</a></div>
            </div>
            <div style="text-align:center"><a href="/" class="back-btn">← Back to Home</a></div>
        </div>
        <script src="/static/main-menu.js"></script>
    </body>
    </html>
    '''

@app.route('/scholarships')
def scholarships_page():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Scholarships</title><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body{font-family:Arial;background:#EFF6FF;margin:0;padding:20px}
        .container{max-width:1000px;margin:0 auto;background:white;padding:40px;border-radius:20px}
        h1{color:#1E3A8A;text-align:center}
        .scholarship-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:30px}
        .scholarship-card{background:#EFF6FF;padding:25px;border-radius:15px;border-left:4px solid #D4AF37}
        .scholarship-card h3{color:#1E3A8A}
        .scholarship-card .coverage{margin:10px0}
        .btn{display:inline-block;margin-top:10px;background:#D4AF37;color:#1E3A8A;padding:6px15px;text-decoration:none;border-radius:20px;font-size:12px}
        .back-btn{display:inline-block;margin-top:30px;background:#1E3A8A;color:white;padding:10px20px;text-decoration:none;border-radius:8px}
        @media(max-width:768px){.scholarship-grid{grid-template-columns:1fr}}
    </style>
    </head>
    <body>
        <div class="container">
            <h1>💰 Scholarship Opportunities</h1>
            <div class="scholarship-grid">
                <div class="scholarship-card"><h3>🇨🇳 CSC Scholarship (China)</h3><div class="coverage">Full tuition + stipend + accommodation</div><a href="/csc-scholarship" class="btn">Details</a></div>
                <div class="scholarship-card"><h3>🇰🇷 KGSP Scholarship (Korea)</h3><div class="coverage">Full tuition + living expenses + airfare</div><a href="/kgsp-scholarship" class="btn">Details</a></div>
                <div class="scholarship-card"><h3>🇯🇵 MEXT Scholarship (Japan)</h3><div class="coverage">Full tuition + monthly stipend + airfare</div><a href="/mext-scholarship" class="btn">Details</a></div>
                <div class="scholarship-card"><h3>🇸🇬 ASEAN Scholarship (Singapore)</h3><div class="coverage">Full tuition + living allowance</div><a href="/asean-scholarship" class="btn">Details</a></div>
            </div>
            <div style="text-align:center"><a href="/" class="back-btn">← Back to Home</a></div>
        </div>
        <script src="/static/main-menu.js"></script>
    </body>
    </html>
    '''

@app.route('/resources')
def resources_page():
    return redirect('/blog')  # or create a proper resources page

# Ensure /contact already exists, if not, add it.


# ==================== MAIN ====================
if __name__ == '__main__':
    print("=" * 80)
    print("🏫 KHARY GLOBAL EDU - Complete Asian Study Portal")
    print("=" * 80)
    print("\n✅ WEBSITE RUNNING: http://localhost:5000")
    print("\n🌏 COUNTRIES AVAILABLE:")
    print(f"   • China: {len(china_universities)} universities")
    print(f"   • Singapore: {len(singapore_universities)} universities")
    print(f"   • Malaysia: {len(malaysia_universities)} universities")
    print(f"   • Japan: {len(japan_universities)} universities")
    print(f"   • Korea: {len(korea_universities)} universities")
    print(f"\n📊 TOTAL: {len(china_universities) + len(singapore_universities) + len(malaysia_universities) + len(japan_universities) + len(korea_universities)} UNIVERSITIES")
    print("\n📁 Applications saved to database and text files")
    print("\n👀 Admin Panel: http://localhost:5000/khary-global-edu")
    print("\n⚠️  Press Ctrl+C to stop the server")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 
    