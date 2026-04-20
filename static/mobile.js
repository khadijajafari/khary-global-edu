document.addEventListener('DOMContentLoaded', function() {
    var dots = document.querySelector('.navbar .three-dots');
    var panel = document.getElementById('sidePanel');
    var overlay = document.getElementById('panelOverlay');
    if (!dots || !panel || !overlay) return;
    dots.onclick = function() {
        panel.classList.toggle('open');
        overlay.classList.toggle('show');
        document.body.style.overflow = panel.classList.contains('open') ? 'hidden' : '';
    };
    overlay.onclick = function() {
        panel.classList.remove('open');
        overlay.classList.remove('show');
        document.body.style.overflow = '';
    };
});