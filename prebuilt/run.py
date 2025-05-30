from app import create_app

# input as argument, the model name, find options below
app = create_app('microsoft/DialoGPT-medium')
'''
DialoGPT-(smallmedium/large): A model fine-tuned for conversational purposes.
GPT-2: More general-purpose text generation.
BART: Another good option for conversational tasks.
T5: A versatile transformer model that can also be used for dialogues.
'''

if __name__ == "__main__":
    app.run(debug=True)