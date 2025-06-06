let chatHistoryIds = null;

// Change to Flask port number
const PORT_NUM = '5000';
const SERVER_URL = `${window.location.protocol}//${window.location.hostname}:${PORT_NUM}`;

const chatBox = document.getElementById('chatBox');
const form = document.getElementById('chatForm');
const inputField = document.getElementById('userInput');

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
