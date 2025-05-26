## Backend Features

# Prebuilt
[x] Add text to speech to prebuilt
[x] add tts library to requirements_P.txt

# Ollama
[] Add text to speech to Ollama
[] add tts library to requirements_O.txt

# Training
[] training method: save model during training 
--> at periodic times say every 20 min 
--> at every epoch etc.

[] training model: stop model when error doesnt improve
--> when error rate stops changing, save and stop the model.



---------------------------------------------------------------
## Frontend Features

# Web

[] Improve look of the website
--> Make a proper header?
--> Make a chat link? 
--> change how the text is displayed on the screen

[] Change look of text
--> display the text as blocks ie: chatgpt style?
    *what other styles could we try*

[] improve history function
--> change how the history is brought up when typing into the text box.

# Interactivity

[] Add a check-able button to the screen

[] create toggle button so you can hear the bots reply through the website

[] Add speech to text option?



---------------------------------------------------------------
## Bugs

[x] prebuilt stops replying after some time
--> after ~3 messages remove older memory so it doesnt get stuck

[] **Write test methods** for testing/ollama/prebuilt


[] fix/text retraining option in ./training/main.py



---------------------------------------------------------------
## Refactor / Cleanup

[x] Refactor prebuilt into reusable functions  

[x] Refactor ollama into reusable functions

- Split the traing, ollama and prebuilt files into their own folders
[x] training
[] ollama
[] prebuilt

- Clean up training
[] remove unused and repeated methods/functions
[] 


