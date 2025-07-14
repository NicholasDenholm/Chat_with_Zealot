// ./static/js/page_switcher.js

// Define page order for directional animation
const pageOrder = ['talk-to-bot', 'bot-selector', 'home'];
let currentPageIndex = 0;

function getCurrentPage() {
    const currentPath = window.location.pathname;
    let activePage = '';
    
    if (currentPath.includes('bot-menu') || currentPath.includes('bot-selector')) {
        activePage = 'bot-selector';
    } else if (currentPath.includes('talk-to-bot')) {
        activePage = 'talk-to-bot';
    } else {
        activePage = 'home';
    }
    
    return activePage;
}

function getPageIndex(page) {
    return pageOrder.indexOf(page);
}

function switchPage(page) {
    const currentPage = getCurrentPage();
    const currentIndex = getPageIndex(currentPage);
    const newIndex = getPageIndex(page);
    
    // Determine direction
    const direction = newIndex > currentIndex ? 'right' : 'left';
    
    // Update active states
    document.querySelectorAll('.switch-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    
    // Update indicator position with direction class
    const switcherToggle = document.querySelector('.switcher-toggle');
    
    // Remove previous direction classes
    switcherToggle.classList.remove('slide-left', 'slide-right');
    
    // Add direction class for smoother animation
    switcherToggle.classList.add(`slide-${direction}`);
    
    // Update indicator position
    switcherToggle.setAttribute('data-active', page);
    
    // Remove direction class after animation completes
    setTimeout(() => {
        switcherToggle.classList.remove('slide-left', 'slide-right');
    }, 500);
    
    // Update current page index
    currentPageIndex = newIndex;
    
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
    const activePage = getCurrentPage();
    currentPageIndex = getPageIndex(activePage);
    
    // Set initial active state
    document.querySelectorAll('.switch-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const activeButton = document.querySelector(`[data-page="${activePage}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
    
    const switcherToggle = document.querySelector('.switcher-toggle');
    if (switcherToggle) {
        switcherToggle.setAttribute('data-active', activePage);
    }
});