// ./static/js/page_switcher.js

function switchPage(page) {
    // Update active states
    document.querySelectorAll('.switch-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    
    // Update indicator position
    document.querySelector('.switcher-toggle').setAttribute('data-active', page);
    
    // Handle navigation
    if (page === 'home') {
        window.location.href = '/';
    } else if (page === 'bot-selector') {
        window.location.href = '/bot-menu';
    } else if (page === 'talk-to-bot') {
        window.location.href = '/talk-to-bot';
    }
}

// Initialize the switcher based on current page
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    let activePage = 'home';
    
    if (currentPath.includes('bot-menu') || currentPath.includes('bot-selector')) {
        activePage = 'bot-selector';
    }

    if (currentPath.includes('talk-to-bot')) {
        activePage = 'talk-to-bot';
    }
    
    // Set initial active state
    document.querySelectorAll('.switch-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelector(`[data-page="${activePage}"]`).classList.add('active');
    document.querySelector('.switcher-toggle').setAttribute('data-active', activePage);
});