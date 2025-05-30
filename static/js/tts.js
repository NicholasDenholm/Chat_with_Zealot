function speakText(text) {
    if (!text) return;

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US'; // or 'en-GB', etc.

    // Optional: Change voice or rate
    // utterance.voice = speechSynthesis.getVoices()[0];
    // utterance.rate = 1.0;

    speechSynthesis.speak(utterance);
}