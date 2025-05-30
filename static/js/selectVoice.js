// `selectedVoice` must be accessible globally
let selectedVoice = null;

// Load and list available voices
function loadVoices(callback) {
    let voices = speechSynthesis.getVoices();

    if (voices.length) {
        callback(voices);
    } else {
        speechSynthesis.onvoiceschanged = () => {
            voices = speechSynthesis.getVoices();
            callback(voices);
        };
    }
}

// Populate the <select> dropdown with available voices
function populateVoiceDropdown(voices) {
    const voiceSelect = document.getElementById('voiceSelect');
    voiceSelect.innerHTML = '';

    voices.forEach((voice, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `${voice.name} (${voice.lang})`;
        voiceSelect.appendChild(option);
    });

    // Set default voice
    selectedVoice = voices[0];

    // Change voice on selection
    voiceSelect.addEventListener('change', () => {
        const selectedIndex = voiceSelect.value;
        selectedVoice = voices[selectedIndex];
    });
}

// Initialize voice selection
function initVoiceSelection() {
    loadVoices((voices) => {
        populateVoiceDropdown(voices);
    });
}

// Automatically run on page load
document.addEventListener("DOMContentLoaded", initVoiceSelection);
