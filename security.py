# security.py - Server-side security functions
import re
import time
from functools import wraps
from flask import request, jsonify

# Rate limiting storage
RATE_LIMIT = {}

def check_rate_limit(ip, action, limit=5, window=60):
    key = f"{ip}:{action}"
    now = time.time()
    if key not in RATE_LIMIT:
        RATE_LIMIT[key] = []
    RATE_LIMIT[key] = [t for t in RATE_LIMIT[key] if now - t < window]
    if len(RATE_LIMIT[key]) >= limit:
        return False
    RATE_LIMIT[key].append(now)
    return True

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain an uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain a lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain a number"
    return True, "OK"

def validate_email(email):
    if not email or '@' not in email or '.' not in email:
        return False
    if len(email) > 100:
        return False
    return True

def sanitize_input(text, max_length=500):
    if not text:
        return ''
    import html
    dangerous = ['<script>', '</script>', 'javascript:', 'onclick', 'onerror', 'onload']
    for d in dangerous:
        if d.lower() in text.lower():
            return ''
    return html.escape(text.strip())[:max_length]

def rate_limit(limit=5, window=60):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            ip = request.remote_addr
            action = request.endpoint
            if not check_rate_limit(ip, action, limit, window):
                return jsonify({'error': 'Too many requests. Try again later.'}), 429
            return f(*args, **kwargs)
        return decorated
    return decorator


def rate_limit(limit=5, window=60):
    def decorator(f):
        from functools import wraps
        from flask import request, jsonify
        import time
        
        RATE_LIMIT_STORE = {}
        
        @wraps(f)
        def decorated(*args, **kwargs):
            ip = request.remote_addr
            key = f"{ip}:{request.endpoint}"
            now = time.time()
            
            if key not in RATE_LIMIT_STORE:
                RATE_LIMIT_STORE[key] = []
            
            RATE_LIMIT_STORE[key] = [t for t in RATE_LIMIT_STORE[key] if now - t < window]
            
            if len(RATE_LIMIT_STORE[key]) >= limit:
                return jsonify({'error': 'Too many requests. Try again later.'}), 429
            
            RATE_LIMIT_STORE[key].append(now)
            return f(*args, **kwargs)
        return decorated
    return decorator
