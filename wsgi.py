import sys
import os

# Add your project path
project_home = '/home/kharyglobaledu/khary-global-edu'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'

# Import your Flask app
from app import app as application