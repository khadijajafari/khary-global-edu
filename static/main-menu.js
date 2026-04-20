// Universal Main Menu for KHARY GLOBAL EDU - FIXED: Top-level buttons are links
(function() {
    const menuHTML = `
    <div id="khary-main-menu" style="background: #1E3A8A; color: white; position: sticky; top: 0; z-index: 10000; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <div class="container" style="max-width: 1400px; margin: 0 auto; padding: 0 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                
                <!-- Logo Left -->
                <a href="/" style="display: flex; align-items: center; text-decoration: none; padding: 10px 0;">
                    <img src="/static/khary-profile.jpg" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 10px; border: 2px solid #D4AF37;">
                    <span style="color: white; font-weight: bold; font-size: 16px;">KHARY<span style="color: #D4AF37;">GLOBAL EDU</span></span>
                </a>
                
                <!-- Desktop Menu -->
                <div class="desktop-menu" style="display: flex; flex-wrap: wrap; gap: 5px;">
                    
                    <!-- DESTINATIONS - Button is a link, dropdown also has links -->
                    <div class="menu-dropdown" style="position: relative; display: inline-block;">
                        <a href="/destinations" class="menu-btn" style="background: transparent; border: none; color: white; padding: 12px 12px; font-size: 14px; cursor: pointer; font-weight: 500; text-decoration: none; display: inline-block;">
                            🌏 Destinations ▼
                        </a>
                        <div class="dropdown-content" style="display: none; position: absolute; background: white; min-width: 200px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-radius: 8px; z-index: 10001; top: 100%; left: 0;">
                            <a href="/china">🇨🇳 China</a>
                            <a href="/singapore">🇸🇬 Singapore</a>
                            <a href="/malaysia">🇲🇾 Malaysia</a>
                            <a href="/japan">🇯🇵 Japan</a>
                            <a href="/korea">🇰🇷 Korea</a>
                        </div>
                    </div>
                    
                    <!-- PROGRAMS -->
                    <div class="menu-dropdown" style="position: relative; display: inline-block;">
                        <a href="/programs" class="menu-btn" style="background: transparent; border: none; color: white; padding: 12px 12px; font-size: 14px; cursor: pointer; font-weight: 500; text-decoration: none; display: inline-block;">
                            🎓 Programs ▼
                        </a>
                        <div class="dropdown-content" style="display: none; position: absolute; background: white; min-width: 200px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-radius: 8px; z-index: 10001; top: 100%; left: 0;">
                            <a href="/foundation">🎯 Foundation Programs</a>
                            <a href="/undergraduate">📘 Undergraduate Programs</a>
                            <a href="/graduate">📙 Graduate Programs</a>
                            <a href="/phd-programs">🔬 PhD Programs</a>
                            <a href="/language">🗣️ Language Courses</a>
                        </div>
                    </div>
                    
                    <!-- SCHOLARSHIPS -->
                    <div class="menu-dropdown" style="position: relative; display: inline-block;">
                        <a href="/scholarships" class="menu-btn" style="background: transparent; border: none; color: white; padding: 12px 12px; font-size: 14px; cursor: pointer; font-weight: 500; text-decoration: none; display: inline-block;">
                            💰 Scholarships ▼
                        </a>
                        <div class="dropdown-content" style="display: none; position: absolute; background: white; min-width: 220px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-radius: 8px; z-index: 10001; top: 100%; left: 0;">
                            <a href="/csc-scholarship">🇨🇳 CSC Scholarship (China)</a>
                            <a href="/kgsp-scholarship">🇰🇷 KGSP Scholarship (Korea)</a>
                            <a href="/mext-scholarship">🇯🇵 MEXT Scholarship (Japan)</a>
                            <a href="/asean-scholarship">🇸🇬 ASEAN Scholarship (Singapore)</a>
                            <a href="/malaysia-scholarship">🇲🇾 Malaysia Scholarship</a>
                        </div>
                    </div>
                    
                    <!-- RESOURCES -->
                    <div class="menu-dropdown" style="position: relative; display: inline-block;">
                        <a href="/resources" class="menu-btn" style="background: transparent; border: none; color: white; padding: 12px 12px; font-size: 14px; cursor: pointer; font-weight: 500; text-decoration: none; display: inline-block;">
                            📚 Resources ▼
                        </a>
                        <div class="dropdown-content" style="display: none; position: absolute; background: white; min-width: 200px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-radius: 8px; z-index: 10001; top: 100%; left: 0;">
                            <a href="/blog">📝 Blog & Tips</a>
                            <a href="/media">📸 Media Gallery</a>
                            <a href="/compare">⚖️ Compare Universities</a>
                            <a href="/scholarship-calculator">🧮 Scholarship Calculator</a>
                            <a href="/faq">❓ FAQ</a>
                            <a href="/deadlines">📅 Application Deadlines</a>
                        </div>
                    </div>
                    
                    <!-- ABOUT -->
                    <div class="menu-dropdown" style="position: relative; display: inline-block;">
                        <a href="/about" class="menu-btn" style="background: transparent; border: none; color: white; padding: 12px 12px; font-size: 14px; cursor: pointer; font-weight: 500; text-decoration: none; display: inline-block;">
                            ℹ️ About ▼
                        </a>
                        <div class="dropdown-content" style="display: none; position: absolute; background: white; min-width: 200px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-radius: 8px; z-index: 10001; top: 100%; left: 0;">
                            <a href="/about">📖 Our Story</a>
                            <a href="/team">👥 Our Team</a>
                            <a href="/testimonials">⭐ Student Testimonials</a>
                            <a href="/partners">🤝 University Partners</a>
                            <a href="/news">📰 News & Events</a>
                        </div>
                    </div>
                    
                    <!-- CONTACT -->
                    <div class="menu-dropdown" style="position: relative; display: inline-block;">
                        <a href="/contact" class="menu-btn" style="background: transparent; border: none; color: white; padding: 12px 12px; font-size: 14px; cursor: pointer; font-weight: 500; text-decoration: none; display: inline-block;">
                            📞 Contact ▼
                        </a>
                        <div class="dropdown-content" style="display: none; position: absolute; background: white; min-width: 220px; box-shadow: 0 8px 16px rgba(0,0,0,0.2); border-radius: 8px; z-index: 10001; top: 100%; left: 0;">
                            <a href="/contact">📧 Contact Form</a>
                            <a href="mailto:kharyglobal@gmail.com">✉️ Email: kharyglobal@gmail.com</a>
                            <a href="https://wa.me/8613522464910" target="_blank">💬 WhatsApp: +86 135 2246 4910</a>
                            <a href="/appointment">📅 Book Free Consultation</a>
                        </div>
                    </div>
                    
                </div>
                
                <!-- Mobile Hamburger Button -->
                <div class="mobile-menu-icon" style="display: none; cursor: pointer; padding: 10px;">
                    <i class="fas fa-bars" style="font-size: 24px; color: white;"></i>
                </div>
            </div>
        </div>
        
        <!-- Mobile Side Menu (unchanged) -->
        <div class="mobile-side-menu" style="display: none; position: fixed; top: 0; right: -280px; width: 280px; height: 100%; background: white; z-index: 10001; transition: right 0.3s; padding: 60px 20px; box-shadow: -2px 0 10px rgba(0,0,0,0.1);">
            <div class="close-menu" style="position: absolute; top: 15px; right: 15px; font-size: 24px; cursor: pointer; color: #1E3A8A;">✕</div>
            <a href="/">🏠 Home</a>
            <a href="/china">🇨🇳 China</a>
            <a href="/singapore">🇸🇬 Singapore</a>
            <a href="/malaysia">🇲🇾 Malaysia</a>
            <a href="/japan">🇯🇵 Japan</a>
            <a href="/korea">🇰🇷 Korea</a>
            <a href="/foundation">🎓 Foundation</a>
            <a href="/undergraduate">📘 Undergraduate</a>
            <a href="/graduate">📙 Graduate</a>
            <a href="/phd-programs">🔬 PhD</a>
            <a href="/language">🗣️ Language</a>
            <a href="/csc-scholarship">💰 CSC Scholarship</a>
            <a href="/kgsp-scholarship">💰 KGSP Scholarship</a>
            <a href="/mext-scholarship">💰 MEXT Scholarship</a>
            <a href="/media">📸 Media</a>
            <a href="/blog">📝 Blog</a>
            <a href="/contact">📞 Contact</a>
            <a href="/appointment">📅 Book Consultation</a>
        </div>
        <div class="mobile-overlay" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 10000;"></div>
    </div>
    
    <style>
        .menu-dropdown:hover .dropdown-content {
            display: block !important;
        }
        .menu-dropdown:hover .menu-btn {
            background: rgba(255,255,255,0.15);
            border-radius: 8px;
        }
        .dropdown-content a {
            display: block;
            padding: 12px 16px;
            color: #1E3A8A;
            text-decoration: none;
            border-bottom: 1px solid #eee;
            font-size: 14px;
        }
        .dropdown-content a:hover {
            background: #EFF6FF;
        }
        
        @media (max-width: 768px) {
            .desktop-menu {
                display: none !important;
            }
            .mobile-menu-icon {
                display: flex !important;
            }
            .mobile-side-menu {
                display: block !important;
            }
            .mobile-side-menu a {
                display: block;
                padding: 12px 0;
                color: #1E3A8A;
                text-decoration: none;
                border-bottom: 1px solid #eee;
            }
        }
        
        @media (min-width: 769px) {
            .mobile-side-menu, .mobile-overlay {
                display: none !important;
            }
        }
    </style>
    `;
    
    document.body.insertAdjacentHTML('afterbegin', menuHTML);
    
    // Mobile menu toggle
    var menuIcon = document.querySelector('.mobile-menu-icon');
    var sideMenu = document.querySelector('.mobile-side-menu');
    var overlay = document.querySelector('.mobile-overlay');
    var closeBtn = document.querySelector('.close-menu');
    
    if(menuIcon) {
        menuIcon.onclick = function() {
            sideMenu.style.right = '0px';
            if(overlay) overlay.style.display = 'block';
        };
    }
    
    function closeMobileMenu() {
        sideMenu.style.right = '-280px';
        if(overlay) overlay.style.display = 'none';
    }
    
    if(closeBtn) closeBtn.onclick = closeMobileMenu;
    if(overlay) overlay.onclick = closeMobileMenu;
})();