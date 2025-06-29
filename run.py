import os
from chat_app.app import create_app


# You can pass any supported model name here
app = create_app('huggingface','microsoft/DialoGPT-medium')
print("Made app ...\n")

def run_prebuilt():
    print("Here in run Prebuilt!!!! \n\n")
    

if __name__ == "__main__":
    mode = os.getenv("MODE", "flask")  # Choose mode via ENV VAR

    if mode == "flask":
        app.run(host='0.0.0.0', port=5000, debug=True)
    elif mode == "prebuilt":
        run_prebuilt()
    else:
        print(f"Unknown mode: {mode}. Use MODE=flask or MODE=prebuilt")