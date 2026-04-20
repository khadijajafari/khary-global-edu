// static/whatsapp.js
console.log('WhatsApp script loaded');

function toggleWhatsappPopup() {
    var popup = document.getElementById('whatsappPopup');
    if (popup) {
        if (popup.style.display === 'none' || popup.style.display === '') {
            popup.style.display = 'block';
            generateQRCode();
        } else {
            popup.style.display = 'none';
        }
    }
}

function closeWhatsappPopup() {
    var popup = document.getElementById('whatsappPopup');
    if (popup) {
        popup.style.display = 'none';
    }
}

function copyPhoneNumber() {
    var number = "+86 135 2246 4910";
    navigator.clipboard.writeText(number).then(function() {
        showToast('✅ Number copied!');
    });
}

function showToast(msg) {
    var toast = document.createElement('div');
    toast.textContent = msg;
    toast.style.cssText = 'position:fixed; bottom:100px; right:30px; background:#333; color:white; padding:8px 16px; border-radius:20px; font-size:12px; z-index:10000; animation:fadeOut 1.5s forwards;';
    document.body.appendChild(toast);
    setTimeout(function() { toast.remove(); }, 1500);
}

function generateQRCode() {
    var qrElement = document.getElementById('whatsappQRCode');
    if (qrElement && typeof QRCode !== 'undefined' && qrElement.innerHTML === '') {
        new QRCode(qrElement, {
            text: "https://wa.me/8613522464910?text=Hello%20I%20have%20a%20question%20about%20studying%20in%20Asia",
            width: 100,
            height: 100
        });
    }
}

// Load QR Code library
if (typeof QRCode === 'undefined') {
    var script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js';
    document.head.appendChild(script);
}

// Close popup when clicking outside
document.addEventListener('click', function(event) {
    var popup = document.getElementById('whatsappPopup');
    var btn = document.getElementById('whatsappBtn');
    if (popup && btn && !btn.contains(event.target) && !popup.contains(event.target)) {
        popup.style.display = 'none';
    }
});

// Add animation style
var style = document.createElement('style');
style.textContent = '@keyframes fadeOut { 0% { opacity: 1; } 70% { opacity: 1; } 100% { opacity: 0; visibility: hidden; } }';
document.head.appendChild(style);