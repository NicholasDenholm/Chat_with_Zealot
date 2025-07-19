// Whisper language selector (for backend transcription)
const languageSelect = document.getElementById('languageSelect');
const whisperLanguages = {
  en: "English",
  es: "Spanish",
  fr: "French",
  de: "German",
  it: "Italian",
  zh: "Chinese",
  ja: "Japanese",
  ko: "Korean",
  ru: "Russian"
};

// Populate Whisper language dropdown
Object.entries(whisperLanguages).forEach(([code, name]) => {
  const option = document.createElement('option');
  option.value = code;
  option.textContent = name;
  languageSelect.appendChild(option);
});

// Save Whisper language to Flask
languageSelect.addEventListener('change', () => {
  const selectedLang = languageSelect.value;

  fetch('/set_language', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ language_code: selectedLang })
  }).then(response => {
    if (!response.ok) {
      console.error("Failed to set language.");
    }
  });
});


// Voice selector (speech synthesis)
const voiceSelect = document.getElementById('voiceSelect');
let voices = [];

function populateVoiceDropdown() {
  voices = speechSynthesis.getVoices();
  voiceSelect.innerHTML = '';
  voices.forEach((voice, idx) => {
    const option = document.createElement('option');
    option.value = idx;
    option.textContent = `${voice.name} (${voice.lang})`;
    voiceSelect.appendChild(option);
  });
}

speechSynthesis.onvoiceschanged = populateVoiceDropdown;

// Store selected voice in localStorage
voiceSelect.addEventListener('change', () => {
  const selectedVoice = voices[voiceSelect.value];
  localStorage.setItem('selectedVoice', selectedVoice.name);
});
