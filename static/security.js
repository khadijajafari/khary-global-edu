// static/security.js - Client-side security

// Input validation before form submit
function validateForm(formId) {
    let form = document.getElementById(formId);
    if(!form) return true;
    
    let inputs = form.querySelectorAll('input, textarea');
    let isValid = true;
    
    inputs.forEach(input => {
        if(input.value) {
            // Remove dangerous characters
            let dangerous = ['<script>', '</script>', 'javascript:', 'onclick', 'onerror'];
            for(let d of dangerous) {
                if(input.value.toLowerCase().includes(d)) {
                    alert('Invalid characters detected');
                    input.value = '';
                    isValid = false;
                }
            }
            // Limit length
            if(input.value.length > 500) {
                alert('Input too long (max 500 characters)');
                input.value = input.value.substring(0, 500);
                isValid = false;
            }
        }
    });
    
    return isValid;
}

// Rate limit for actions
let actionCount = {};
function checkRateLimit(action, limit=5, seconds=60) {
    let now = Date.now();
    if(!actionCount[action]) actionCount[action] = [];
    actionCount[action] = actionCount[action].filter(t => now - t < seconds * 1000);
    if(actionCount[action].length >= limit) {
        alert(`Too many attempts. Please wait ${seconds} seconds.`);
        return false;
    }
    actionCount[action].push(now);
    return true;
}

// Password strength checker
function checkPasswordStrength(password) {
    let strength = 0;
    if(password.length >= 8) strength++;
    if(password.match(/[A-Z]/)) strength++;
    if(password.match(/[a-z]/)) strength++;
    if(password.match(/[0-9]/)) strength++;
    if(password.match(/[^A-Za-z0-9]/)) strength++;
    
    if(strength <= 2) return { color: '#EF4444', text: 'Weak' };
    if(strength <= 4) return { color: '#F59E0B', text: 'Medium' };
    return { color: '#10B981', text: 'Strong' };
}

// Add to password field
document.addEventListener('DOMContentLoaded', function() {
    let passwordField = document.getElementById('password');
    if(passwordField) {
        passwordField.addEventListener('input', function() {
            let result = checkPasswordStrength(this.value);
            let indicator = document.getElementById('password-strength');
            if(!indicator) {
                indicator = document.createElement('div');
                indicator.id = 'password-strength';
                indicator.style.marginTop = '5px';
                indicator.style.fontSize = '12px';
                this.parentNode.appendChild(indicator);
            }
            indicator.style.color = result.color;
            indicator.innerHTML = 'Strength: ' + result.text;
        });
    }
});

// Block suspicious keys
document.addEventListener('keydown', function(e) {
    // Block F12, Ctrl+U, Ctrl+S, Ctrl+Shift+I
    if(e.key === 'F12' || (e.ctrlKey && e.key === 'u') || (e.ctrlKey && e.key === 's') || (e.ctrlKey && e.shiftKey && e.key === 'I')) {
        e.preventDefault();
        return false;
    }
});

// Disable right click (optional)
document.addEventListener('contextmenu', function(e) {
    // Uncomment to disable right click
    // e.preventDefault();
});