// Subscription System - No app.py changes needed
(function() {
    // Create subscription popup
    function showSubscribePopup() {
        let popup = document.getElementById('subscribe-popup');
        if(popup) return;
        
        const popupHTML = `
        <div id="subscribe-popup" style="position: fixed; top: 15%; left: 50%; transform: translateX(-50%); background: white; padding: 25px; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); z-index: 100000; width: 90%; max-width: 380px; text-align: center; font-family: 'Segoe UI', Arial; max-height: 80vh; overflow-y: auto;">
            <div style="position: absolute; top: 10px; right: 15px; cursor: pointer; font-size: 24px;" onclick="closeSubscribePopup()">✕</div>
            <i class="fas fa-envelope" style="font-size: 50px; color: #D4AF37;"></i>
            <h2 style="color: #1E3A8A; margin: 15px 0; font-size: 1.3rem;">Get Scholarship Alerts!</h2>
            <p style="color: #666; margin-bottom: 20px; font-size: 0.9rem;">Subscribe to receive updates about scholarships, deadlines, and new universities</p>
            <form id="subscribe-form" onsubmit="saveSubscriber(event)">
                <input type="text" id="sub-name" placeholder="Your Name" required style="width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px;">
                <input type="email" id="sub-email" placeholder="Your Email" required style="width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px;">
                <select id="sub-country" style="width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px;">
                    <option value="">Interested Country</option>
                    <option value="China">🇨🇳 China</option>
                    <option value="Singapore">🇸🇬 Singapore</option>
                    <option value="Malaysia">🇲🇾 Malaysia</option>
                    <option value="Japan">🇯🇵 Japan</option>
                    <option value="Korea">🇰🇷 Korea</option>
                </select>
                <button type="submit" style="width: 100%; background: linear-gradient(135deg, #1E3A8A, #2D4FA8); color: white; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; margin-top: 10px;">Subscribe Now →</button>
            </form>
            <p style="font-size: 11px; color: #999; margin-top: 15px;">We respect your privacy. No spam, unsubscribe anytime.</p>
        </div>
        <div id="popup-overlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 99999;" onclick="closeSubscribePopup()"></div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', popupHTML);
    }
    
    window.closeSubscribePopup = function() {
        let popup = document.getElementById('subscribe-popup');
        let overlay = document.getElementById('popup-overlay');
        if(popup) popup.remove();
        if(overlay) overlay.remove();
    }
    
    window.saveSubscriber = function(event) {
        event.preventDefault();
        
        let name = document.getElementById('sub-name').value;
        let email = document.getElementById('sub-email').value;
        let country = document.getElementById('sub-country').value;
        
        let subscribers = JSON.parse(localStorage.getItem('subscribers') || '[]');
        
        if(subscribers.find(s => s.email === email)) {
            alert('You are already subscribed!');
            closeSubscribePopup();
            return;
        }
        
        subscribers.push({
            name: name,
            email: email,
            country: country,
            date: new Date().toISOString()
        });
        
        localStorage.setItem('subscribers', JSON.stringify(subscribers));
        
        alert(`✅ Thank you ${name}! You have been subscribed.`);
        closeSubscribePopup();
        
        let adminNotifications = JSON.parse(localStorage.getItem('adminNotifications') || '[]');
        adminNotifications.push({
            type: 'new_subscriber',
            name: name,
            email: email,
            country: country,
            timestamp: new Date().toISOString(),
            read: false
        });
        localStorage.setItem('adminNotifications', JSON.stringify(adminNotifications));
    }
    
    // Show popup after 5 seconds
    setTimeout(() => {
        let lastShown = localStorage.getItem('popupLastShown');
        let now = Date.now();
        if(!lastShown || (now - parseInt(lastShown)) > 30 * 24 * 60 * 60 * 1000) {
            showSubscribePopup();
            localStorage.setItem('popupLastShown', now.toString());
        }
    }, 5000);
    
    // Floating subscribe button - position at bottom center
    const floatBtn = document.createElement('div');
    floatBtn.innerHTML = '<i class="fas fa-bell" style="font-size: 18px;"></i> <span style="font-size: 12px;">Subscribe</span>';
    floatBtn.style.cssText = 'position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #D4AF37; color: #1E3A8A; padding: 10px 20px; border-radius: 50px; display: flex; align-items: center; gap: 8px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.2); z-index: 9998; font-weight: bold; font-size: 14px;';
    floatBtn.onclick = showSubscribePopup;
    document.body.appendChild(floatBtn);
})();


// In subscribe.js, make sure the popup has:
style.position = 'fixed';
style.top = '50%';
style.left = '50%';
style.transform = 'translate(-50%, -50%)';