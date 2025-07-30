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
        const botRawResponse = data.response; // Get the raw bot response

        // --- CALL formatBotReply HERE ---
        const formattedBotResponse = formatBotReply(botRawResponse);

        displayMessage("Bot", formattedBotResponse, "bot-message");

        chatHistoryIds = data.chat_history_ids;

        // Trigger TTS
        speak(data.response);

    } catch (error) {
        displayMessage("Error", error.message, "bot-message");
    }
}


function formatBotReply(rawText) {
    if (!rawText || typeof rawText !== 'string') {
        return '';
    }

    let formattedText = rawText;

    // 1. Handle Code Blocks (must be done before other formatting to prevent issues)
    // Matches ```language\ncode\n``` or ```\ncode\n```
    formattedText = formattedText.replace(/```(\w*)\n([\s\S]+?)\n```/g, (match, lang, code) => {
        // Basic escaping for HTML entities within the code block
        const escapedCode = code.replace(/&/g, '&amp;')
                               .replace(/</g, '&lt;')
                               .replace(/>/g, '&gt;');
        // You could add syntax highlighting libraries here based on `lang`
        return `<pre><code${lang ? ` class="language-${lang}"` : ''}>${escapedCode}</code></pre>`;
    });

    // 2. Handle Paragraphs and Lists (split by lines to process more easily)
    const lines = formattedText.split('\n');
    let htmlOutput = [];
    let inList = false;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();

        // Check for empty lines to create new paragraphs
        if (line === '') {
            if (inList) {
                htmlOutput.push('</ul>');
                inList = false;
            }
            // Add a paragraph break, but avoid multiple empty paragraphs if there are consecutive empty lines
            if (htmlOutput.length > 0 && !htmlOutput[htmlOutput.length - 1].endsWith('</p>')) {
                 htmlOutput.push('<p></p>'); // Add an empty paragraph for spacing
            }
            continue;
        }

        // Check for List Items
        if (line.startsWith('* ') || line.startsWith('- ')) {
            if (!inList) {
                htmlOutput.push('<ul>');
                inList = true;
            }
            // Remove the bullet point and trim again
            let listItemContent = line.substring(2).trim();
            htmlOutput.push(`<li>${listItemContent}</li>`);
        } else {
            // If we were in a list, close it
            if (inList) {
                htmlOutput.push('</ul>');
                inList = false;
            }
            // Treat as a regular paragraph line (will be wrapped in <p> later if not a direct HTML element)
            htmlOutput.push(line);
        }
    }

    // Close any open list at the end
    if (inList) {
        htmlOutput.push('</ul>');
    }

    // Join lines and then apply inline formatting and final paragraph wrapping
    let finalContent = htmlOutput.join('\n');

    // 3. Handle Inline Code
    formattedText = finalContent.replace(/`([^`]+)`/g, '<code>$1</code>');

    // 4. Handle Bold (stronger emphasis)
    formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // 5. Handle Italics (lighter emphasis)
    // This regex ensures it doesn't match if it's already part of a **bold** match
    formattedText = formattedText.replace(/(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)/g, '<em>$1</em>'); // Matches *text* not preceded/followed by *
    formattedText = formattedText.replace(/_([^_]+)_/g, '<em>$1</em>'); // Matches _text_

    // 6. Wrap remaining plain text lines in paragraphs
    // This is a bit tricky after list processing. A common approach is to
    // split by newlines again and wrap anything that isn't already HTML.
    // For simplicity, let's assume if it's not starting with an HTML tag it's a paragraph.
    const finalLines = formattedText.split('\n');
    let outputWithParagraphs = [];
    let currentParagraph = [];

    for (const line of finalLines) {
        const trimmedLine = line.trim();
        // Check if the line looks like an HTML tag, or if it's empty (already handled for new paragraphs)
        if (trimmedLine === '' || trimmedLine.startsWith('<') || trimmedLine.startsWith('</')) {
            if (currentParagraph.length > 0) {
                outputWithParagraphs.push(`<p>${currentParagraph.join(' ')}</p>`);
                currentParagraph = [];
            }
            outputWithParagraphs.push(line); // Add the HTML tag or empty line directly
        } else {
            currentParagraph.push(line); // Collect lines for the current paragraph
        }
    }
    // Add any remaining paragraph content
    if (currentParagraph.length > 0) {
        outputWithParagraphs.push(`<p>${currentParagraph.join(' ')}</p>`);
    }


    return outputWithParagraphs.join('\n').trim();
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