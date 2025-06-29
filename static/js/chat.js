let chatHistoryIds = null;

// Change to Flask port number
const PORT_NUM = '5000';
const SERVER_URL = `${window.location.protocol}//${window.location.hostname}:${PORT_NUM}`;

const chatBox = document.getElementById('chatBox');
const form = document.getElementById('chatForm');
const inputField = document.getElementById('userInput');
const micButton = document.getElementById("micButton");

// Display a message in the chat box
function displayMessage(sender, text, className) {
    chatBox.innerHTML += `<div class="message ${className}"><strong>${sender}:</strong> ${text}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send the message to the backend and get a response
async function sendMessageToAPI(message, history) {
    // Use http://xxx.x.x.xx:PORT/chat or http://xxx.x.x.xx:PORT/chat-stream
    // need to concat str ex: fetch(serverUrl + '/chat', { ... });
    // or us `` not: '' . Then {} not ()
    const response = await fetch(`${SERVER_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, chat_history_ids: history })
    });

    if (!response.ok) throw new Error("Server error");

    return await response.json();
}

// Speak text using browser TTS (defined in tts.js)
function speak(text) {
    speakText(text);  // Delegates to tts.js
}

// Process the user's input and update the chat
async function processUserMessage(userInput) {
    displayMessage("You", userInput, "user-message");

    try {
        const data = await sendMessageToAPI(userInput, chatHistoryIds);
        displayMessage("Bot", data.response, "bot-message");

        chatHistoryIds = data.chat_history_ids;

        // Trigger TTS
        speak(data.response);

    } catch (error) {
        displayMessage("Error", error.message, "bot-message");
    }
}

/* */
// Handle form submission
function handleFormSubmit(event) {
    event.preventDefault();

    const userInput = inputField.value.trim();
    if (!userInput) return;

    inputField.value = "";
    processUserMessage(userInput);
}

// Attach event listener
form.addEventListener('submit', handleFormSubmit);

// ---------------- Audio Processing ----------------
/*
async function startVoiceInput() {
    // Request microphone access
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const audioChunks = [];

    mediaRecorder.ondataavailable = event => audioChunks.push(event.data);

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append("audio", audioBlob, "speech.wav");

        try {
            const response = await fetch("/api/audio", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            const userText = data.transcription;
            const botResponse = data.response;

            displayMessage("You (voice)", userText, "user-message");
            displayMessage("Bot", botResponse, "bot-message");
            speak(botResponse); // trigger TTS
        } catch (err) {
            displayMessage("Error", err.message, "bot-message");
        }
    };

    mediaRecorder.start();

    setTimeout(() => {
        mediaRecorder.stop();
    }, 5000); // record for 5 seconds
}
*/
let mediaRecorder;
let audioChunks = [];

async function startRecording() {
    // Request microphone access
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append("audio", audioBlob, "speech.wav");

        try {
            const response = await fetch("/api/audio", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            const userText = data.transcription || "(no transcription)";
            const botResponse = data.response || "(no response)";

            displayMessage("You (voice)", userText, "user-message");
            displayMessage("Bot", botResponse, "bot-message");
            speak(botResponse); // trigger TTS
        } catch (err) {
            displayMessage("Error", err.message, "bot-message");
        }
    };

    mediaRecorder.start();
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== "inactive") {
        mediaRecorder.stop();
    }
}

// Attach event listeners to micButton


micButton.addEventListener("mousedown", () => {
    startRecording();
});

micButton.addEventListener("mouseup", () => {
    stopRecording();
});

// For touch devices
micButton.addEventListener("touchstart", (e) => {
    e.preventDefault(); // Prevent mouse event emulation
    startRecording();
});

micButton.addEventListener("touchend", (e) => {
    e.preventDefault();
    stopRecording();
});



document.getElementById("micButton").addEventListener("click", startVoiceInput);