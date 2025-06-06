function speakText(text) {
    if (!text) return;

    const utterance = new SpeechSynthesisUtterance(text);

    // Optional: Change rate
    // utterance.rate = 1.0;

    utterance.voice = VoiceSelector.getSelectedVoice();
    speechSynthesis.speak(utterance);
}