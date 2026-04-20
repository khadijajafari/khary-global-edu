// SEO Tags - Add to every page
(function() {
    // Add meta description
    if(!document.querySelector('meta[name="description"]')) {
        const meta = document.createElement('meta');
        meta.name = 'description';
        meta.content = 'KHARY GLOBAL EDU - Study abroad guidance for Asian universities. Scholarships, visa support, admission help for China, Singapore, Malaysia, Japan, Korea.';
        document.head.appendChild(meta);
    }
    
    // Add meta keywords
    if(!document.querySelector('meta[name="keywords"]')) {
        const meta = document.createElement('meta');
        meta.name = 'keywords';
        meta.content = 'study abroad, study in China, study in Singapore, study in Malaysia, study in Japan, study in Korea, CSC scholarship, KGSP scholarship, MEXT scholarship, study in Asia';
        document.head.appendChild(meta);
    }
    
    // Add meta author
    if(!document.querySelector('meta[name="author"]')) {
        const meta = document.createElement('meta');
        meta.name = 'author';
        meta.content = 'KHARY GLOBAL EDU';
        document.head.appendChild(meta);
    }
    
    // Add Open Graph tags (for social media sharing)
    if(!document.querySelector('meta[property="og:title"]')) {
        const ogTitle = document.createElement('meta');
        ogTitle.setAttribute('property', 'og:title');
        ogTitle.content = 'KHARY GLOBAL EDU - Study in Asia';
        document.head.appendChild(ogTitle);
        
        const ogDesc = document.createElement('meta');
        ogDesc.setAttribute('property', 'og:description');
        ogDesc.content = 'Your trusted partner for studying in China, Singapore, Malaysia, Japan, and Korea.';
        document.head.appendChild(ogDesc);
        
        const ogImage = document.createElement('meta');
        ogImage.setAttribute('property', 'og:image');
        ogImage.content = '/static/khary-profile.jpg';
        document.head.appendChild(ogImage);
    }
})();