// WhatsApp Popup - Small & Compact
(function() {
    const popupHTML = `
    <div id="whatsapp-popup-container" style="position: fixed; top: 50%; right: 15px; transform: translateY(-50%); z-index: 99999;">
        <!-- WhatsApp Button - SMALLER -->
        <div id="whatsapp-main-btn" style="background: #25D366; width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 3px 10px rgba(0,0,0,0.15); transition: all 0.3s;">
            <i class="fab fa-whatsapp" style="font-size: 24px; color: white;"></i>
        </div>
        
        <!-- Popup Window - SMALLER, opens to LEFT -->
        <div id="whatsapp-popup-window" style="display: none; position: absolute; top: 50%; right: 55px; transform: translateY(-50%); width: 260px; background: white; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.2); overflow: hidden;">
            
            <!-- Header - COMPACT -->
            <div style="background: #075E54; padding: 10px 12px; color: white; display: flex; align-items: center; gap: 8px;">
                <img src="/static/khary-profile.jpg" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid #D4AF37;">
                <div style="flex: 1;">
                    <h4 style="margin: 0; font-size: 13px;">KHARY GLOBAL EDU</h4>
                    <p style="margin: 0; font-size: 10px; opacity: 0.9;">Online · Quick reply</p>
                </div>
                <button id="close-whatsapp-popup" style="background: none; border: none; color: white; font-size: 16px; cursor: pointer;">✕</button>
            </div>
            
            <!-- Body - COMPACT -->
            <div style="padding: 12px;">
                <!-- QR Code - SMALLER -->
                <div style="text-align: center; margin-bottom: 10px;">
                    <div id="whatsapp-qr" style="display: flex; justify-content: center;"></div>
                    <p style="font-size: 10px; color: #666; margin-top: 5px;">Scan with phone</p>
                </div>
                
                <!-- Phone Number - COMPACT -->
                <div style="background: #f5f5f5; border-radius: 8px; padding: 8px 10px; display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #075E54; font-size: 12px;">+86 135 2246 4910</span>
                    <button id="copy-phone-btn" style="background: #25D366; border: none; padding: 4px 10px; border-radius: 15px; color: white; cursor: pointer; font-size: 10px;">Copy</button>
                </div>
                
                <!-- Start Chat Button - COMPACT -->
                <a href="https://wa.me/8613522464910?text=Hello%20KHARY%20GLOBAL%20EDU%2C%20I%20have%20a%20question%20about%20studying%20in%20Asia" 
                   target="_blank" 
                   style="display: block; background: #25D366; color: white; text-align: center; padding: 8px; border-radius: 25px; text-decoration: none; font-weight: bold; font-size: 12px;">
                    <i class="fab fa-whatsapp"></i> Chat Now
                </a>
            </div>
        </div>
    </div>
    
    <style>
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        #whatsapp-main-btn:hover {
            transform: scale(1.05);
        }
    </style>
    `;
    
    document.body.insertAdjacentHTML('beforeend', popupHTML);
    
    const mainBtn = document.getElementById('whatsapp-main-btn');
    const popupWindow = document.getElementById('whatsapp-popup-window');
    const closeBtn = document.getElementById('close-whatsapp-popup');
    const copyBtn = document.getElementById('copy-phone-btn');
    
    mainBtn.onclick = function() {
        if(popupWindow.style.display === 'none' || popupWindow.style.display === '') {
            popupWindow.style.display = 'block';
            generateQRCode();
        } else {
            popupWindow.style.display = 'none';
        }
    };
    
    closeBtn.onclick = function() {
        popupWindow.style.display = 'none';
    };
    
    document.addEventListener('click', function(event) {
        if(!mainBtn.contains(event.target) && !popupWindow.contains(event.target)) {
            popupWindow.style.display = 'none';
        }
    });
    
    copyBtn.onclick = function() {
        navigator.clipboard.writeText("+86 135 2246 4910").then(function() {
            showToast('✅ Copied!');
        });
    };
    
    function showToast(msg) {
        const toast = document.createElement('div');
        toast.textContent = msg;
        toast.style.cssText = 'position: fixed; bottom: 20px; right: 20px; background: #333; color: white; padding: 6px 12px; border-radius: 15px; font-size: 11px; z-index: 100000;';
        document.body.appendChild(toast);
        setTimeout(function() { toast.remove(); }, 1500);
    }
    
    function generateQRCode() {
        const qrContainer = document.getElementById('whatsapp-qr');
        if(qrContainer && typeof QRCode !== 'undefined') {
            qrContainer.innerHTML = '';
            new QRCode(qrContainer, {
                text: "https://wa.me/8613522464910",
                width: 80,
                height: 80
            });
        }
    }
    
    if(typeof QRCode === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js';
        document.head.appendChild(script);
    }
})();