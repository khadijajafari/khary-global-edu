// Newsletter functionality
function openNewsletter() {
    var modal = document.getElementById('newsletterModal');
    if(modal) modal.style.display = 'flex';
}
function closeNewsletter() {
    var modal = document.getElementById('newsletterModal');
    if(modal) modal.style.display = 'none';
}
document.addEventListener('DOMContentLoaded', function() {
    if(!document.getElementById('newsletterModal')) {
        var modalDiv = document.createElement('div');
        modalDiv.id = 'newsletterModal';
        modalDiv.style.cssText = 'display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:10000; justify-content:center; align-items:center;';
        modalDiv.innerHTML = '<div style="background:white; padding:30px; border-radius:20px; max-width:450px; text-align:center; margin:20px;"><i class="fas fa-bell" style="font-size:50px; color:#D4AF37;"></i><h2 style="color:#1E3A8A; margin:15px 0;">Get Scholarship Alerts</h2><p>Subscribe to receive deadline reminders and scholarship opportunities</p><form id="floatingNewsletterForm"><input type="email" id="floatingEmail" placeholder="Your email address" required><button type="submit">Subscribe Now</button></form><button onclick="closeNewsletter()">Close</button></div>';
        document.body.appendChild(modalDiv);
    }
    var form = document.getElementById('floatingNewsletterForm');
    if(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            var email = document.getElementById('floatingEmail').value;
            if(email) {
                var subscribers = JSON.parse(localStorage.getItem('newsletterSubscribers') || '[]');
                if(!subscribers.includes(email)) subscribers.push(email);
                localStorage.setItem('newsletterSubscribers', JSON.stringify(subscribers));
                alert('Subscribed! You will receive updates.');
                closeNewsletter();
                document.getElementById('floatingEmail').value = '';
            }
        });
    }
});