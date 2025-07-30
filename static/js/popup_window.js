// ===== POPUP ANIMATION CONTROLLER =====

class PopupController {
  constructor() {
    this.activePopups = new Set();
    this.animationDuration = 300; // milliseconds
    this.init();
  }

  init() {
    // Create backdrop element
    this.createBackdrop();
    
    // Add global click listener to close popups when clicking outside
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.popup-element') && !e.target.closest('.popup-trigger')) {
        this.hideAllPopups();
      }
    });

    // Add escape key listener
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.hideAllPopups();
      }
    });
  }

  createBackdrop() {
    this.backdrop = document.createElement('div');
    this.backdrop.className = 'popup-backdrop';
    this.backdrop.addEventListener('click', () => this.hideAllPopups());
    document.body.appendChild(this.backdrop);
  }

  // Method 1: Simple toggle
  togglePopup(elementId, animationType = 'scale') {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.classList.add('popup-element');
    
    if (element.classList.contains('show')) {
      this.hidePopup(elementId, animationType);
    } else {
      this.showPopup(elementId, animationType);
    }
  }

  // Method 2: Show popup
  showPopup(elementId, animationType = 'scale') {
    const element = document.getElementById(elementId);
    if (!element) return;

    // Add popup classes
    element.classList.add('popup-element', `popup-${animationType}`);
    
    // Show backdrop if not already shown
    if (this.activePopups.size === 0) {
      this.backdrop.classList.add('show');
    }
    
    // Add to active popups
    this.activePopups.add(elementId);
    
    // Trigger animation
    requestAnimationFrame(() => {
      element.classList.add('show');
      element.classList.remove('hide');
    });

    // Emit custom event
    element.dispatchEvent(new CustomEvent('popup:show', { 
      detail: { elementId, animationType } 
    }));
  }

  // Method 3: Hide popup
  hidePopup(elementId, animationType = 'scale') {
    const element = document.getElementById(elementId);
    if (!element) return;

    // For elastic animation, use hide class
    if (animationType === 'elastic') {
      element.classList.add('hide');
      element.classList.remove('show');
    } else {
      element.classList.remove('show');
    }

    // Remove from active popups
    this.activePopups.delete(elementId);
    
    // Hide backdrop if no more popups
    if (this.activePopups.size === 0) {
      this.backdrop.classList.remove('show');
    }

    // Clean up after animation
    setTimeout(() => {
      if (!element.classList.contains('show')) {
        element.classList.remove(`popup-${animationType}`, 'hide');
      }
    }, this.animationDuration + 100);

    // Emit custom event
    element.dispatchEvent(new CustomEvent('popup:hide', { 
      detail: { elementId, animationType } 
    }));
  }

  // Method 4: Hide all popups
  hideAllPopups() {
    this.activePopups.forEach(elementId => {
      const element = document.getElementById(elementId);
      if (element) {
        const animationType = this.getAnimationType(element);
        this.hidePopup(elementId, animationType);
      }
    });
  }

  // Method 5: Show popup with delay
  showPopupDelayed(elementId, delay = 0, animationType = 'scale') {
    setTimeout(() => {
      this.showPopup(elementId, animationType);
    }, delay);
  }

  // Method 6: Auto-hide popup after duration
  showPopupTimed(elementId, duration = 3000, animationType = 'scale') {
    this.showPopup(elementId, animationType);
    setTimeout(() => {
      this.hidePopup(elementId, animationType);
    }, duration);
  }

  // Helper method to detect animation type from element classes
  getAnimationType(element) {
    const classes = ['scale', 'slide-scale', 'bounce', 'blur', 'flip', 'elastic'];
    for (const type of classes) {
      if (element.classList.contains(`popup-${type}`)) {
        return type;
      }
    }
    return 'scale'; // default
  }

  // Method 7: Sequential popup showing (staggered)
  showPopupsSequential(elementIds, interval = 200, animationType = 'scale') {
    elementIds.forEach((elementId, index) => {
      this.showPopupDelayed(elementId, index * interval, animationType);
    });
  }
}

// Initialize popup controller
const popupController = new PopupController();

// ===== EASY-TO-USE FUNCTIONS =====

// Show language selector
function showLanguageSelector(animationType = 'bounce') {
  popupController.showPopup('languageSelector', animationType);
}

// Hide language selector
function hideLanguageSelector(animationType = 'bounce') {
  popupController.hidePopup('languageSelector', animationType);
}

// Toggle language selector
function toggleLanguageSelector(animationType = 'bounce') {
  popupController.togglePopup('languageSelector', animationType);
}

// Show voice selector
function showVoiceSelector(animationType = 'slide-scale') {
  popupController.showPopup('voiceSelector', animationType);
}

// Hide voice selector
function hideVoiceSelector(animationType = 'slide-scale') {
  popupController.hidePopup('voiceSelector', animationType);
}

// Toggle voice selector
function toggleVoiceSelector(animationType = 'slide-scale') {
  popupController.togglePopup('voiceSelector', animationType);
}

// ===== TRIGGER BUTTON SETUP =====
function createPopupTriggers() {
  // Create language selector trigger
  const langTrigger = document.createElement('button');
  langTrigger.className = 'popup-trigger';
  langTrigger.innerHTML = '🌐';
  langTrigger.title = 'Language Settings';
  langTrigger.style.bottom = '90px';
  langTrigger.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleLanguageSelector('bounce');
  });
  document.body.appendChild(langTrigger);

  // Create voice selector trigger
  const voiceTrigger = document.createElement('button');
  voiceTrigger.className = 'popup-trigger';
  voiceTrigger.innerHTML = '🔊';
  voiceTrigger.title = 'Voice Settings';
  voiceTrigger.style.bottom = '20px';
  voiceTrigger.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleVoiceSelector('slide-scale');
  });
  document.body.appendChild(voiceTrigger);
}

// ===== AUTO-INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
  // Auto-setup if elements exist
  const languageBox = document.querySelector('.language-select-box');
  const voiceBox = document.querySelector('.voice-select-box');

  if (languageBox && !languageBox.id) {
    languageBox.id = 'languageSelector';
  }

  if (voiceBox && !voiceBox.id) {
    voiceBox.id = 'voiceSelector';
  }

  // Create trigger buttons
  // createPopupTriggers(); // Uncomment if you want automatic trigger buttons
});

// ===== EVENT LISTENERS FOR CUSTOM EVENTS =====
document.addEventListener('popup:show', (e) => {
  console.log(`Popup shown: ${e.detail.elementId} with ${e.detail.animationType} animation`);
});

document.addEventListener('popup:hide', (e) => {
  console.log(`Popup hidden: ${e.detail.elementId} with ${e.detail.animationType} animation`);
});

// ===== EXAMPLE USAGE FUNCTIONS =====

// Example: Show popup on hover
function setupHoverTrigger(triggerId, popupId, animationType = 'scale') {
  const trigger = document.getElementById(triggerId);
  const popup = document.getElementById(popupId);
  
  if (trigger && popup) {
    let hoverTimeout;
    
    trigger.addEventListener('mouseenter', () => {
      clearTimeout(hoverTimeout);
      popupController.showPopup(popupId, animationType);
    });
    
    trigger.addEventListener('mouseleave', () => {
      hoverTimeout = setTimeout(() => {
        popupController.hidePopup(popupId, animationType);
      }, 500); // 500ms delay before hiding
    });
    
    popup.addEventListener('mouseenter', () => {
      clearTimeout(hoverTimeout);
    });
    
    popup.addEventListener('mouseleave', () => {
      popupController.hidePopup(popupId, animationType);
    });
  }
}

// Example: Show popup on long press (mobile)
function setupLongPressTrigger(triggerId, popupId, animationType = 'scale') {
  const trigger = document.getElementById(triggerId);
  
  if (trigger) {
    let pressTimeout;
    
    trigger.addEventListener('touchstart', (e) => {
      pressTimeout = setTimeout(() => {
        popupController.showPopup(popupId, animationType);
        // Haptic feedback if available
        if (navigator.vibrate) {
          navigator.vibrate(50);
        }
      }, 500); // 500ms long press
    });
    
    trigger.addEventListener('touchend', () => {
      clearTimeout(pressTimeout);
    });
  }
}