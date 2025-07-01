import os
import sys
from chat_app.app import create_app

backend = 'llamacpp'
model_name = 'llama3.2'


if backend == 'huggingface':
    app = create_app('huggingface','microsoft/DialoGPT-medium')
    print("Made app ...\n")
elif backend == 'llamacpp':
    # TODO seperate logic of app and model init to enable hotswapping of models.
    app = create_app('llamacpp', 'llama3.2')
    print("Made llama app... \n")
else: 
    print("Backend not supported.")
    sys.exit(1)

if __name__ == "__main__":
    mode = os.getenv("MODE", "flask")  # Choose mode via ENV VAR

    if mode == "flask":
        app.run(host='0.0.0.0', port=5000, debug=True)
    elif mode == "prebuilt":
        #run_prebuilt()
        print("prebuilt selected")
    else:
        print(f"Unknown mode: {mode}. Use MODE=flask or MODE=prebuilt")
