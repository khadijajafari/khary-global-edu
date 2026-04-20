// static/languages.js - Instant Language Switcher
console.log('🌐 Language system ready');

let currentLang = localStorage.getItem('lang') || 'en';

// All translations
const text = {
    en: {
        home: "Home",
        destinations: "Destinations",
        ourStory: "Our Story",
        compare: "Compare",
        blog: "Blog",
        admin: "Admin",
        heroTitle: "From Dream to Campus:<br>Your Asian Study Journey Starts Here",
        heroSub: "Expert guidance for studying in China, Singapore, Malaysia, Japan, and Korea",
        missionTitle: "Our Mission",
        missionText: "My name is Khary. For years, I watched talented students give up on studying abroad because the process felt overwhelming. Paperwork, applications, visas—it seemed too confusing. So I started KHARY GLOBAL EDU with one mission: to walk with you, step-by-step, from your first question to your first day in class overseas. This isn't just business—it's personal.",
        destTitle: "Study Destinations",
        china: "China",
        singapore: "Singapore",
        malaysia: "Malaysia",
        japan: "Japan",
        korea: "Korea",
        uniLabel: "Top Universities",
        footer1: "© 2026 KHARY GLOBAL EDU. All rights reserved.",
        footer2: "Your Trusted Partner for Asian Education Excellence"
    },
    zh: {
        home: "首页",
        destinations: "留学目的地",
        ourStory: "我们的故事",
        compare: "大学对比",
        blog: "博客",
        admin: "管理后台",
        heroTitle: "从梦想到校园：<br>你的亚洲留学之旅从这里开始",
        heroSub: "为中国、新加坡、马来西亚、日本和韩国留学提供专业指导",
        missionTitle: "我们的使命",
        missionText: "我叫Khary。多年来，我看到许多有才华的学生因为申请过程太繁琐而放弃留学梦想。文件、申请、签证——这一切似乎太复杂了。所以我创办了KHARY GLOBAL EDU，只有一个使命：陪你一步步走过从第一个问题到海外课堂的第一天。这不仅仅是生意——这是个人的承诺。",
        destTitle: "留学目的地",
        china: "中国",
        singapore: "新加坡",
        malaysia: "马来西亚",
        japan: "日本",
        korea: "韩国",
        uniLabel: "顶尖大学",
        footer1: "© 2026 KHARY GLOBAL EDU。保留所有权利。",
        footer2: "您在亚洲教育卓越之路上的可信赖伙伴"
    },
    ar: {
        home: "الرئيسية",
        destinations: "الوجهات",
        ourStory: "قصتنا",
        compare: "مقارنة",
        blog: "المدونة",
        admin: "المشرف",
        heroTitle: "من الحلم إلى الحرم الجامعي:<br>رحلتك للدراسة في آسيا تبدأ هنا",
        heroSub: "إرشادات الخبراء للدراسة في الصين وسنغافورة وماليزيا واليابان وكوريا",
        missionTitle: "مهمتنا",
        missionText: "اسمي خاري. لسنوات، شاهدت الطلاب الموهوبين يتخلون عن الدراسة في الخارج لأن العملية كانت مرهقة. الأوراق والطلبات والتأشيرات - بدا الأمر مربكًا للغاية. لذلك بدأت KHARY GLOBAL EDU بمهمة واحدة: أن أمشي معك خطوة بخطوة، من سؤالك الأول إلى يومك الأول في الفصل الدراسي بالخارج. هذا ليس مجرد عمل - إنه أمر شخصي.",
        destTitle: "وجهات الدراسة",
        china: "الصين",
        singapore: "سنغافورة",
        malaysia: "ماليزيا",
        japan: "اليابان",
        korea: "كوريا",
        uniLabel: "أفضل الجامعات",
        footer1: "© 2026 KHARY GLOBAL EDU. جميع الحقوق محفوظة.",
        footer2: "شريكك الموثوق للتميز التعليمي في آسيا"
    },
    fr: {
        home: "Accueil",
        destinations: "Destinations",
        ourStory: "Notre Histoire",
        compare: "Comparer",
        blog: "Blog",
        admin: "Admin",
        heroTitle: "Du Rêve au Campus:<br>Votre Voyage d'Études en Asie Commence Ici",
        heroSub: "Conseils d'experts pour étudier en Chine, à Singapour, en Malaisie, au Japon et en Corée",
        missionTitle: "Notre Mission",
        missionText: "Je m'appelle Khary. Pendant des années, j'ai vu des étudiants talentueux abandonner l'idée d'étudier à l'étranger car le processus semblait accablant. Paperasse, candidatures, visas—tout semblait trop compliqué. J'ai donc créé KHARY GLOBAL EDU avec une seule mission: vous accompagner pas à pas, de votre première question à votre premier jour de cours à l'étranger. Ce n'est pas qu'une affaire—c'est personnel.",
        destTitle: "Destinations d'Études",
        china: "Chine",
        singapore: "Singapour",
        malaysia: "Malaisie",
        japan: "Japon",
        korea: "Corée",
        uniLabel: "Meilleures Universités",
        footer1: "© 2026 KHARY GLOBAL EDU. Tous droits réservés.",
        footer2: "Votre Partenaire de Confiance pour l'Excellence Éducative en Asie"
    }
};

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('lang', lang);
    
    const t = text[lang];
    
    // Update button text
    const btn = document.getElementById('langBtn');
    if (btn) {
        if (lang === 'en') btn.innerHTML = '🌐 English';
        else if (lang === 'zh') btn.innerHTML = '🌐 中文';
        else if (lang === 'ar') btn.innerHTML = '🌐 العربية';
        else if (lang === 'fr') btn.innerHTML = '🌐 Français';
    }
    
    // Hide menu
    const menu = document.getElementById('langMenu');
    if (menu) menu.style.display = 'none';
    
    // Update text direction for Arabic
    if (lang === 'ar') {
        document.body.style.direction = 'rtl';
        document.body.style.textAlign = 'right';
    } else {
        document.body.style.direction = 'ltr';
        document.body.style.textAlign = 'left';
    }
    
    // Update navbar links
    const homeLink = document.getElementById('homeLink');
    if (homeLink) homeLink.innerText = t.home;
    
    const destLink = document.getElementById('destinationsLink');
    if (destLink) destLink.innerText = t.destinations;
    
    const storyLink = document.getElementById('ourStoryLink');
    if (storyLink) storyLink.innerText = t.ourStory;
    
    const compareLink = document.getElementById('compareLink');
    if (compareLink) compareLink.innerText = t.compare;
    
    const blogLink = document.getElementById('blogLink');
    if (blogLink) blogLink.innerText = t.blog;
    
    const adminLink = document.getElementById('adminLink');
    if (adminLink) adminLink.innerText = t.admin;
    
    // Update hero section
    const heroTitle = document.querySelector('.hero h1');
    if (heroTitle) heroTitle.innerHTML = t.heroTitle;
    
    const heroSub = document.querySelector('.hero p');
    if (heroSub) heroSub.innerText = t.heroSub;
    
    // Update mission section
    const missionTitle = document.querySelector('.mission-box h3');
    if (missionTitle) missionTitle.innerText = t.missionTitle;
    
    const missionText = document.querySelector('.mission-box p');
    if (missionText) missionText.innerText = t.missionText;
    
    // Update destinations title
    const destTitle = document.querySelector('.destinations h2');
    if (destTitle) destTitle.innerText = t.destTitle;
    
    // Update country cards
    const countryCards = document.querySelectorAll('.country-card h3');
    const countries = [t.china, t.singapore, t.malaysia, t.japan, t.korea];
    countryCards.forEach((card, i) => {
        if (card && countries[i]) card.innerText = countries[i];
    });
    
    // Update university count text
    const uniTexts = document.querySelectorAll('.country-card p');
    uniTexts.forEach(p => {
        if (p) p.innerHTML = `30+ ${t.uniLabel}`;
    });
    
    // Update footer
    const footer1 = document.querySelector('.footer p:first-child');
    if (footer1) footer1.innerHTML = t.footer1;
    
    const footer2 = document.querySelector('.footer p:last-child');
    if (footer2 && footer2 !== footer1) footer2.innerText = t.footer2;
    
    console.log('Language changed to:', lang);
}

function toggleLangMenu() {
    const menu = document.getElementById('langMenu');
    if (menu) {
        menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    }
}

// Close menu when clicking outside
document.addEventListener('click', function(e) {
    const menu = document.getElementById('langMenu');
    const btn = document.getElementById('langBtn');
    if (menu && btn && !btn.contains(e.target) && !menu.contains(e.target)) {
        menu.style.display = 'none';
    }
});

// Apply language when page loads
document.addEventListener('DOMContentLoaded', function() {
    setLanguage(currentLang);
});