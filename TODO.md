## Backend Features

# Prebuilt
[x] Add text to speech to prebuilt
[x] add tts library to requirements_P.txt

# Ollama
[] Add text to speech to Ollama
[] add tts library to requirements_O.txt
[] create lobotomy function that clears personality
[] create function that updates personality

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

[x] Add speech to text option?
--> see: https://ollama.com/dimavz/whisper-tiny

[x] Get one model to talk to the other
[] be able to change dumb models memory cutoff
[] test other dumb models

[] Get one model to talk to another that is loaded onto a non local device


---------------------------------------------------------------
## Security

[] Check that input from text box is cleaned

[] verify what port is best to place website on.
--> 5000 is for testing
--> 8000 is better?

[] training methods may need to be refactored greatly to limit attack surface

---------------------------------------------------------------
## Bugs

[x] prebuilt stops replying after some time
--> after ~3 messages remove older memory so it doesnt get stuck

[] **Write test methods** for training/ollama/prebuilt

[] Prebuilt Test methods
--> make init so that tests can be a python module  [x] 
--> chat bot  4/11
--> routes   2/2
--> run      4/1

[] Ollama test methods

[] training test methods


[] fix/text retraining option in ./training/main.py



---------------------------------------------------------------
## Refactor / Cleanup
x
[x] Refactor prebuilt into reusable functions  

[x] Refactor ollama into reusable functions

- Split the traing, ollama and prebuilt files into their own folders
[x] training
[] ollama
[x] prebuilt

- Clean up training
[] remove unused and repeated methods/functions
[] 


