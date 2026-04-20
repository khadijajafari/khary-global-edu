// Mobile Bottom Navigation Menu - Appears only on phones
(function() {
    function addMobileBottomMenu() {
        // Check if screen width is mobile
        if(window.innerWidth > 768) return;
        
        // Check if menu already exists
        if(document.getElementById('mobile-bottom-menu')) return;
        
        // Create bottom menu HTML
        const menuHTML = `
        <div id="mobile-bottom-menu" style="position: fixed; bottom: 0; left: 0; right: 0; background: white; box-shadow: 0 -2px 15px rgba(0,0,0,0.1); z-index: 99999; padding: 8px 12px; border-top: 1px solid #E2E8F0;">
            <div style="display: flex; justify-content: space-around; align-items: center; max-width: 500px; margin: 0 auto;">
                <a href="/" style="display: flex; flex-direction: column; align-items: center; text-decoration: none; color: #1E3A8A; gap: 4px;">
                    <i class="fas fa-home" style="font-size: 22px;"></i>
                    <span style="font-size: 10px;">Home</span>
                </a>
                <div onclick="document.getElementById('destinations')?.scrollIntoView({behavior: 'smooth'})" style="display: flex; flex-direction: column; align-items: center; text-decoration: none; color: #1E3A8A; gap: 4px; cursor: pointer;">
                    <i class="fas fa-globe-asia" style="font-size: 22px;"></i>
                    <span style="font-size: 10px;">Countries</span>
                </div>
                <div onclick="showCountryUniversities('china', '🇨🇳 China')" style="display: flex; flex-direction: column; align-items: center; text-decoration: none; color: #1E3A8A; gap: 4px; cursor: pointer;">
                    <i class="fas fa-graduation-cap" style="font-size: 22px;"></i>
                    <span style="font-size: 10px;">Universities</span>
                </div>
                <a href="/media" style="display: flex; flex-direction: column; align-items: center; text-decoration: none; color: #1E3A8A; gap: 4px;">
                    <i class="fas fa-photo-video" style="font-size: 22px;"></i>
                    <span style="font-size: 10px;">Media</span>
                </a>
                <a href="/contact" style="display: flex; flex-direction: column; align-items: center; text-decoration: none; color: #1E3A8A; gap: 4px;">
                    <i class="fas fa-headset" style="font-size: 22px;"></i>
                    <span style="font-size: 10px;">Support</span>
                </a>
            </div>
        </div>
        
        <style>
            @media (max-width: 768px) {
                body {
                    padding-bottom: 65px !important;
                }
                .footer {
                    margin-bottom: 0 !important;
                }
                #mobile-bottom-menu {
                    display: flex !important;
                }
            }
            @media (min-width: 769px) {
                #mobile-bottom-menu {
                    display: none !important;
                }
            }
        </style>
        `;
        
        document.body.insertAdjacentHTML('beforeend', menuHTML);
    }
    
    // Add when page loads
    if(document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', addMobileBottomMenu);
    } else {
        addMobileBottomMenu();
    }
    
    // Handle resize (show/hide based on screen size)
    window.addEventListener('resize', function() {
        const menu = document.getElementById('mobile-bottom-menu');
        if(window.innerWidth <= 768) {
            if(!menu) addMobileBottomMenu();
        } else {
            if(menu) menu.remove();
            // Remove body padding when desktop
            document.body.style.paddingBottom = '';
        }
    });
})();