const chatBox = document.getElementById('chatBox');
const form = document.getElementById('chatForm');
const inputField = document.getElementById('userInput');

const bot1 = "";  
const bot2 = "";


// Display a message in the chat box
function displayMessage(sender, text, className) {
    chatBox.innerHTML += `<div class="message ${className}"><strong>${sender}:</strong> ${text}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send the message to the backend and get a response
/*
async function sendUserMessage(message, history) {
    
    const response = await fetch(`/starting_message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, chat_history_ids: history })
    });

    if (!response.ok) throw new Error("Server error");

    return await response.json();
} */

// Helper function to check bots and run conversation
async function startConversation(userInput) {
    try {
        // Step 1: Check if bots are initialized
        const botStatusResponse = await fetch("/check_bots");
        if (!botStatusResponse.ok) throw new Error("Failed to check bot status");
        
        const botStatus = await botStatusResponse.json();
        const { bot1_exists, bot2_exists } = botStatus;

        if (!bot1_exists || !bot2_exists) {
            console.error("Bots not initialized.");
            alert("Bots are not initialized. Please click 'Initialize Bots' first.");
            return;
        }

        // Step 2: Start bot conversation
        const result = await botConversation(userInput);
        console.log("Bot conversation result:", result);
        /*  
        Object { conversation: (5) […] }
        ​
        conversation: Array(5) [ {…}, {…}, {…}, … ]
        ​​
        0: Object { message: "hello how are you?", sender: "user" }
        ​​
        1: Object { message: "I am well. How are you?", sender: "Dumb_Bot" }
        ​​
        2: Object { message: "Pretty good. How about you?", sender: "Dumb_Bot" }
        ​​
        3: Object { message: "Not bad.How about you?", sender: "Dumb_Bot" }
        ​​
        4: Object { message: "I don't know. I don't think I'll be able to talk about it", sender: "Dumb_Bot" }
        ​​
        length: 5*/

        // Example: Display messages
        displayConversation(result.conversation);

    } catch (error) {
        console.error("Error in startConversation:", error);
    }
}

// Process the bot's input and update the chat
async function processBotMessage(userInput) {
    displayMessage("You", userInput, "user-message");

    try {
        const data = await startConverstation(userInput);
        const botRawResponse = data.response; // Get the raw bot response

        // --- CALL formatBotReply HERE ---
        const formattedBotResponse = formatBotReply(botRawResponse);

        displayMessage("Bot", formattedBotResponse, "bot-message");

        //chatHistoryIds = data.chat_history_ids;

        // Trigger TTS
        //speak(data.response);

    } catch (error) {
        displayMessage("Error", error.message, "bot-message");
    }
}

/*
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
}*/

// set up bots in the backend
async function setupBots() {
    const response = await fetch(`/setup_bot_convo`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bot1, bot2 })
    });

    if (!response.ok) throw new Error("Server error");

    return await response.json();
}

// Start bot conversation from user input
async function botConversation(userInput) {
    const response = await fetch(`/run_conversation`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userInput }) // key should match what backend expects
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Server error");
    }

    return await response.json(); // returns { conversation: [...] }
}


// Check if bots already exist
async function checkBots() {
    const response = await fetch("/check_bots");
    if (!response.ok) throw new Error("Error checking bot status");

    const result = await response.json();
    return result; // { bot1_exists: true/false, bot2_exists: true/false }
}


/* */
// Handle form submission
function handleFormSubmit(event) {
    event.preventDefault();

    const userInput = inputField.value.trim();
    if (!userInput) return;

    inputField.value = "";
    startConversation(userInput);
    //botConversation(userInput);
}

function displayConversation(convoArray) {
    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML = ""; // Clear previous messages

    convoArray.forEach((entry) => {
        const p = document.createElement("p");
        p.textContent = `${entry.sender}: ${entry.message}`;
        chatBox.appendChild(p);
    });
}


/* 
document.addEventListener("DOMContentLoaded", () => {
    const botInitButton = document.getElementById("botInitButton");
    if (botInitButton) {
        botInitButton.addEventListener("click", async () => {
            try {
                //alert("Button clicked!");
                const result = await setupBots();
                console.log("Bots initialized:", result);
            } catch (error) {
                console.error("Failed to set up bots:", error);
            }
        });
    }
});

*/

// On page load, check if bots exist
document.addEventListener("DOMContentLoaded", async () => {
    const botInitButton = document.getElementById("botInitButton");

    try {
        const botStatus = await checkBots();
        console.log("Bot existence check:", botStatus);

        if (botStatus.bot1_exists && botStatus.bot2_exists) {
            console.log("Bots are already initialized.");
        } else {
            if (botInitButton) {
                botInitButton.addEventListener("click", async () => {
                    try {
                        const result = await setupBots();
                        console.log("Bots initialized:", result);
                    } catch (error) {
                        console.error("Failed to set up bots:", error);
                    }
                });
            }
        }
    } catch (error) {
        console.error("Error during bot status check:", error);
    }
});

form.addEventListener("submit", handleFormSubmit);