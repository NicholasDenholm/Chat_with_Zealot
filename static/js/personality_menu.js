let selectedBot = null;
let currentBot = null;

// Initialize the menu
async function initMenu() {
    await getCurrentBot();
    setupEventListeners();
}

// Get current bot info
async function getCurrentBot() {
    try {
        const response = await fetch('/api/bot/current');
        const data = await response.json();
        
        if (data.backend && data.personality) {
            currentBot = { backend: data.backend, personality: data.personality };
            document.getElementById('currentPersonalityName').textContent = 
                `${data.backend} (${data.personality})`;
            
            // Mark current bot as active
            updateActiveBot(data.backend, data.personality);
        } else {
            document.getElementById('currentPersonalityName').textContent = 'None';
        }
    } catch (error) {
        console.error('Error getting current bot:', error);
        document.getElementById('currentPersonalityName').textContent = 'Error loading';
    }
}

// Update active bot display
function updateActiveBot(backend, personality) {
    document.querySelectorAll('.personality-option').forEach(option => {
        option.classList.remove('active');
        if (option.dataset.backend === backend && option.dataset.personality === personality) {
            option.classList.add('active');
        }
    });
}

// Setup event listeners
function setupEventListeners() {
    document.querySelectorAll('.personality-option').forEach(option => {
        option.addEventListener('click', function() {
            // Remove active class from all options
            document.querySelectorAll('.personality-option').forEach(opt => {
                opt.classList.remove('active');
            });
            
            // Add active class to clicked option
            this.classList.add('active');
            
            // Store selection
            selectedBot = {
                backend: this.dataset.backend,
                personality: this.dataset.personality
            };
            
            // Update button text
            document.getElementById('swapButton').textContent = 
                `Switch to ${this.dataset.personality}`;
        });
    });
}

async function switchToChatPage() {
    try {
        const response = await fetch('/talk-to-bot');
        if (response.ok) {
            // This will redirect to the personality menu page
            window.location.href = '/talk-to-bot';
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Swap bot function
async function swapPersonality() {
    if (!selectedBot) {
        showStatus('Please select a personality first', 'error');
        return;
    }

    const button = document.getElementById('swapButton');
    const originalText = button.textContent;
    
    // Show loading state
    button.innerHTML = '<span class="loading"></span>Switching...';
    button.disabled = true;
    
    try {
        const response = await fetch('/api/bot/personality_change', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                backend: selectedBot.backend,
                personality: selectedBot.personality
            })
        });

        const data = await response.json();

        if (data.success) {
            showStatus(`Successfully switched to ${selectedBot.backend} (${selectedBot.personality})`, 'success');
            currentBot = selectedBot;
            document.getElementById('currentPersonalityName').textContent = 
                `${selectedBot.backend} (${selectedBot.personality})`;
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Network error: ${error.message}`, 'error');
    } finally {
        // Reset button
        button.textContent = originalText;
        button.disabled = false;
    }
}

// Show status message
function showStatus(message, type) {
    const statusElement = document.getElementById('statusMessage');
    statusElement.textContent = message;
    statusElement.className = `status-message status-${type}`;
    statusElement.style.display = 'block';
   
    /*
    // Auto-hide after 7 seconds, then redirect
    setTimeout(async () => {
        statusElement.style.display = 'none';
        try {
            await switchToChatPage();
        } catch (error) {
            console.error('Error switching to chat page:', error);
        }
    }, 3000);
    */
    // if successful then swap to main chat page
    if (type === 'success') {
        setTimeout(() => {
            statusElement.style.display = 'none';    
            switchToChatPage();
        }, 2000);
    } else {
        // Auto-hide error message after 5 seconds
        setTimeout(() => {
            statusElement.style.display = 'none';
        }, 5000);
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initMenu);