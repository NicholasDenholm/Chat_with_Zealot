let selectedBot = null;
let currentBot = null;

// Initialize the menu
async function initMenu() {
    await getCurrentBotPlusType();
    setupEventListeners();
}

// Get current bot info
async function getCurrentBot() {
    try {
        const response = await fetch('/api/bot/current');
        const data = await response.json();
        
        if (data.backend && data.model) {
            currentBot = { backend: data.backend, model: data.model };
            document.getElementById('currentBotName').textContent = 
                `${data.backend} (${data.model})`;
            
            // Mark current bot as active
            updateActiveBot(data.backend, data.model);
        } else {
            document.getElementById('currentBotName').textContent = 'None';
        }
    } catch (error) {
        console.error('Error getting current bot:', error);
        document.getElementById('currentBotName').textContent = 'Error loading';
    }
}

async function getCurrentBotPlusType() {
    try {
        const response = await fetch('/api/bot/current');
        const data = await response.json();
        
        if (data.backend && data.model && data.botType) {
            currentBot = { backend: data.backend, model: data.model, bot_type: data.botType };
            document.getElementById('currentBotName').textContent = 
                `${data.backend} (${data.model}) (${data.botType})`;
            
            // Mark current bot as active
            updateActiveBot(data.backend, data.model, data.botType);
        } else {
            document.getElementById('currentBotName').textContent = 'None';
        }
    } catch (error) {
        console.error('Error getting current bot:', error);
        document.getElementById('currentBotName').textContent = 'Error loading';
    }
}


// Update active bot display
function updateActiveBot(backend, model, botType) {
    document.querySelectorAll('.bot-option').forEach(option => {
        option.classList.remove('active');
        if (option.dataset.backend === backend && option.dataset.model === model && option.dataset.botType === botType) {
            option.classList.add('active');
        }
    });
}

// Setup event listeners
function setupEventListeners() {
    document.querySelectorAll('.bot-option').forEach(option => {
        option.addEventListener('click', function() {
            // Remove active class from all options
            document.querySelectorAll('.bot-option').forEach(opt => {
                opt.classList.remove('active');
            });
            
            // Add active class to clicked option
            this.classList.add('active');
            
            // Store selection
            selectedBot = {
                backend: this.dataset.backend,
                model: this.dataset.model,
                botType: this.dataset.botType
            };
            
            // Update button text
            document.getElementById('swapButton').textContent = 
                `Switch to ${this.dataset.backend}`;
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

async function switchToPersonalityMenu(page_choice) {
    
    const personality_pages = ["/personality-menu-assistant", "personality-menu-zealot", "personality-menu-coder"];
    // Validate page_choice
    if (page_choice < 0 || page_choice >= personality_pages.length) {
        showStatus('Invalid personality choice', 'error');
        return;
    }
    let choice = personality_pages[page_choice]

    // How to put into fetch the choice?
    try {
        const response = await fetch(choice);
        if (response.ok) {
            // This will redirect to the personality menu page
            window.location.href = choice;
        } else {
            showStatus(`Failed to load personality menu: ${response.status}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}


// Function to determine and switch to the appropriate personality menu
async function switchToCorrespondingPersonalityMenu(bot) {
    // Map bot configurations to personality menu indices
    const botToPersonalityMap = {
        'llamacpp-llama3.2-smart_bot': 0,      // assistant
        'llamacpp-llama3.2-zealot_bot': 1,     // zealot
        'llamacpp-codellama:7b-smart_bot': 2       // coder
    };
    
    // Create a key from bot properties
    const botKey = `${bot.backend}-${bot.model}-${bot.botType}`;
    
    // Check if this bot configuration should trigger a personality menu switch
    if (botToPersonalityMap.hasOwnProperty(botKey)) {
        const personalityIndex = botToPersonalityMap[botKey];
        await switchToPersonalityMenu(personalityIndex);
    }
    // If no mapping exists, don't switch personality menus
}


// Swap bot function
async function swapBot() {
    if (!selectedBot) {
        showStatus('Please select a bot first', 'error');
        return;
    }

    const button = document.getElementById('swapButton');
    const originalText = button.textContent;
    
    // Show loading state
    button.innerHTML = '<span class="loading"></span>Switching...';
    button.disabled = true;
    
    try {
        const response = await fetch('/api/bot/swap', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                backend: selectedBot.backend,
                model: selectedBot.model,
                botType: selectedBot.botType
            })
        });

        const data = await response.json();

        if (data.success) {
            showStatus(`Successfully switched to ${selectedBot.backend} (${selectedBot.model})`, 'success');
            currentBot = selectedBot;
            document.getElementById('currentBotName').textContent = 
                `${selectedBot.backend} (${selectedBot.model} ${selectedBot.botType})`;

            // Switch to corresponding personality page
            await switchToCorrespondingPersonalityMenu(selectedBot);

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