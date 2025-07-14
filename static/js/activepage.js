// Add active class based on current page
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const homeBtn = document.getElementById('homeBtn');
    const botBtn = document.getElementById('botBtn');
    
    // Remove active class from all buttons
    homeBtn.classList.remove('active');
    botBtn.classList.remove('active');
    
    // Add active class to current page button
    if (currentPath === '/' || currentPath === '/home') {
        homeBtn.classList.add('active');
    } else if (currentPath === '/bot-menu') {   
        botBtn.classList.add('active');
    }
});