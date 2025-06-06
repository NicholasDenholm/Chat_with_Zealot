from app import create_app

app = create_app('microsoft/DialoGPT-medium')

def run_prebuilt():
        
    # input as argument, the model name, find options below
    '''
    DialoGPT-(smallmedium/large): A model fine-tuned for conversational purposes.
    GPT-2: More general-purpose text generation.
    BART: Another good option for conversational tasks.
    T5: A versatile transformer model that can also be used for dialogues.
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    #run_prebuilt()    