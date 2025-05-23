# Chat_with_Zealot
**WarhammerBot Chatbot**

This is a multi approach conversational AI chatbot built around local llms such as **DialoGPT** and **llama** that interact with a Flask web service. Additionally there is a framework to train your own textbased models from pdf -> text files. 

The prebuilt bots can hold conversations with users and generate personilzed responses based on the input. They can store and maintain conversation history to ensure context is carried over between exchanges.

## Features
- **Interactive Chatbot**: Use the chatbot to ask questions and have ongoing conversations.
- **Personality Customization**: change how the llama model responds user input and adapt length and tone of resposnes using `length`, `style`, `emotionality`
- **Diverse Responses**: The DiabloGPT model framework is able to produce diverse and coherent responses based on tunable parameters such as `temperature`, `top_k`, and `top_p`
- **Persistent Chat History**: The bot remembers previous conversations within the session.
- **GPU Support**: The model automatically uses GPU if available to speed up the response generation.

---

## Setup

1. **Clone the repository (if applicable)**:
    ```bash
    git clone https://github.com/NicholasDenholm/Chat_with_Zealot
    cd warhammerbot
    ```

2. Set up a virtual enviroment
    
    ```
    python -m venv venv
    source venv/bin/activate  # For macOS/Linux
    .\venv\Scripts\activate  # For Windows
    ```

---

## Install Dependencies

Before downloading dependencies, choose which features you would like use. This will determine which requirement package you should install.

## Ollama

Install Ollama: https://ollama.com/download
   Download a model that works for your system, ex: llama3.2

Open a new terminal window and run the command:
   ```ollama run <Your_model>```

Install ollama requirements:
    ```pip install -r ./setup/requirements_O.txt```

Modify this line in ollama_main.py
    ```model = OllamaLLM(model="<Your_models_name>")```

## Prebuilt

install prebuilt requirements:
    ```pip install -r ./setup/requirements_P.txt```

Optionally if you have a NVIDA GPU: install cuda to use GPU acceleration.
    Full guide here: https://medium.com/@jorgefmp.mle/gpu-accelerated-deep-learning-with-pytorch-on-windows-519898e4c283

## Training

Install training requirements:
    ```pip install -r ./setup/requirements_T.txt```

Look in the training folder for relavant python files.

---

If you want **all 3 options** follow these steps:

1. Install required packages

    ```pip install -r ./setup/requirements.txt```

2. Install Ollama

    ```https://ollama.com/download```

3. Download a model that works for your system, see Ollama section above.

Modify this line in ollama_main.py
    ```model = OllamaLLM(model="<Your_models_name>")```

---

You should now be able to run your choosen functionality in the terminal. If you want it to be displayed in the browser you do the following:

### **Modify `app.py` for your model**

Ensure that the **`app.py`** file is configured correctly. The app will automatically choose to run on a GPU if available or fallback to CPU if needed.

This is done on the following line:
```python
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
```

### 3. **Starting the sever** 

    ```python app.py```