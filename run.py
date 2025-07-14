import os
import sys
from chat_app.app import create_app, init_bot

backend = 'llamacpp'
model_name = 'llama3.2'

# Create app without bot initialization
app = create_app()
print("Made app...\n")

# Initialize bot based on backend
if backend == 'huggingface':
    init_bot(app, 'huggingface', 'microsoft/DialoGPT-medium')
    print("Initialized Hugging Face bot...\n")
elif backend == 'llamacpp':
    init_bot(app, 'llamacpp', 'llama3.2')
    print("Initialized LlamaCPP bot...\n")
else:
    print("Backend not supported.")
    sys.exit(1)

if __name__ == "__main__":
    mode = os.getenv("MODE", "flask")  # Choose mode via ENV VAR

    if mode == "flask":
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print(f"Unknown mode: {mode}. Use MODE=flask or MODE=prebuilt")
