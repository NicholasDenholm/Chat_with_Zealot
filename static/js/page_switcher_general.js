// Generalized Page Switcher ./static/js/page_switcher.js

// Store the page configuration globally
let pageConfig = {};

function initPageSwitcher(config) {
    pageConfig = config;
    
    // Set initial active state based on current page
    const currentPath = window.location.pathname;
    let activePage = findActivePageByPath(currentPath);
    
    if (activePage) {
        setActiveState(activePage);
    }
}

function findActivePageByPath(currentPath) {
    // Find the active page based on current URL path
    for (const [key, page] of Object.entries(pageConfig)) {
        if (page.paths) {
            // Check if current path matches any of the page's paths
            if (page.paths.some(path => currentPath.includes(path))) {
                return key;
            }
        } else if (page.path && currentPath.includes(page.path)) {
            return key;
        }
    }
    
    // Return the first page as default if no match found
    const firstPageKey = Object.keys(pageConfig)[0];
    return firstPageKey || null;
}

function switchPage(pageKey) {
    const page = pageConfig[pageKey];
    if (!page) {
        console.warn(`Page '${pageKey}' not found in configuration`);
        return;
    }
    
    // Update active states
    setActiveState(pageKey);
    
    // Handle navigation
    if (page.url) {
        window.location.href = page.url;
    } else {
        console.warn(`No URL configured for page '${pageKey}'`);
    }
}

function setActiveState(pageKey) {
    // Update button active states
    document.querySelectorAll('.switch-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const activeBtn = document.querySelector(`[data-page="${pageKey}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
    
    // Update indicator position
    const toggleElement = document.querySelector('.switcher-toggle');
    if (toggleElement) {
        toggleElement.setAttribute('data-active', pageKey);
        updateIndicatorPosition(pageKey);
    }
}

function updateIndicatorPosition(pageKey) {
    const toggleElement = document.querySelector('.switcher-toggle');
    const activeBtn = document.querySelector(`[data-page="${pageKey}"]`);
    const indicator = document.querySelector('.switch-indicator');
    
    if (toggleElement && activeBtn && indicator) {
        const btnRect = activeBtn.getBoundingClientRect();
        const toggleRect = toggleElement.getBoundingClientRect();
        
        const btnWidth = activeBtn.offsetWidth;
        const btnOffset = activeBtn.offsetLeft;
        
        // Set CSS custom properties for smooth animation
        toggleElement.style.setProperty('--btn-width', `${btnWidth}px`);
        toggleElement.style.setProperty('--btn-offset', `${btnOffset}px`);
        
        // Update indicator directly
        indicator.style.width = `${btnWidth}px`;
        indicator.style.transform = `translateX(${btnOffset}px)`;
    }
}

// Auto-initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const switcherElement = document.querySelector('.page-switcher');
    
    if (switcherElement) {
        // Get configuration from data attributes
        const configData = switcherElement.getAttribute('data-config');
        
        if (configData) {
            try {
                const config = JSON.parse(configData);
                initPageSwitcher(config);
            } catch (e) {
                console.error('Error parsing page switcher configuration:', e);
            }
        } else {
            // Fallback: try to auto-detect based on current page
            autoDetectAndInitialize();
        }
    }
});

function autoDetectAndInitialize() {
    // Fallback configurations for common page patterns
    const currentPath = window.location.pathname;
    let config = {};
    
    // Chat/Bot selector pages
    if (currentPath.includes('talk-to-bot') || currentPath.includes('bot-menu')) {
        config = {
            'home': {
                url: '/',
                paths: ['', 'Home']
            },
            'bot-selector': {
                url: '/bot-menu',
                paths: ['bot-menu', 'bot-selector']
            }
        };
    }
    
    if (Object.keys(config).length > 0) {
        initPageSwitcher(config);
    }
}