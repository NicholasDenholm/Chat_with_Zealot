const VoiceSelector = (() => {
  let voices = [];
  let selectedVoice = null;
  const STORAGE_KEY = 'selectedVoiceName';
  const voiceSelect = document.getElementById('voiceSelect');

  const loadVoices = (callback) => {
    voices = speechSynthesis.getVoices();
    if (voices.length) {
      callback(voices);
    } else {
      speechSynthesis.onvoiceschanged = () => {
        voices = speechSynthesis.getVoices();
        callback(voices);
      };
    }
  };

  const populateVoiceDropdown = (voicesList) => {
    voiceSelect.innerHTML = '';

    voicesList.forEach((voice, idx) => {
      const option = document.createElement('option');
      option.value = idx;
      option.textContent = `${voice.name} (${voice.lang})`;
      voiceSelect.appendChild(option);
    });

    // Try loading saved voice from localStorage
    const savedVoiceName = localStorage.getItem(STORAGE_KEY);
    const defaultIndex = voicesList.findIndex(v => v.name === savedVoiceName);
    selectedVoice = voicesList[defaultIndex >= 0 ? defaultIndex : 0];
    voiceSelect.value = voicesList.indexOf(selectedVoice);

    voiceSelect.addEventListener('change', () => {
      selectedVoice = voices[voiceSelect.value];
      localStorage.setItem(STORAGE_KEY, selectedVoice.name); // Save on change
    });
  };

  const init = () => {
    if (!voiceSelect) {
      console.error("Voice select element not found");
      return;
    }
    loadVoices(populateVoiceDropdown);
  };

  const getSelectedVoice = () => selectedVoice;

  return {
    init,
    getSelectedVoice,
  };
})();

document.addEventListener('DOMContentLoaded', () => {
  VoiceSelector.init();
});
