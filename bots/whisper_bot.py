import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile
import os
import keyboard 

class Whisper_Bot:
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)
        self.language_code = None

    def transcribe_audio(self, audio_path: str, fp16:bool) -> str:
        result = self.model.transcribe(audio_path, language=self.language_code, fp16=fp16)
        return result.get("text", "")
    
    def set_language(self, language_code:str): 
        self.language_code = language_code

# --------------- Language Setup --------------- #

def pick_language() -> str:
    language_options = {
        "1": ("English", "en"),
        "2": ("Spanish", "es"),
        "3": ("French", "fr"),
        "4": ("German", "de"),
        "5": ("Italian", "it"),
        "6": ("Portuguese", "pt"),
        "7": ("Russian", "ru"),
        "8": ("Chinese (Simplified)", "zh"),
        "9": ("Japanese", "ja"),
        "10": ("Korean", "ko"),
        "11": ("Hindi", "hi"),
        "12": ("Arabic", "ar"),
        "13": ("Turkish", "tr"),
        "14": ("Dutch", "nl"),
        "15": ("Vietnamese", "vi"),
        "16": ("Auto-detect", None)
    }

    print("\nSelect language for transcription:")
    for key, (lang, _) in language_options.items():
        print(f"{key}. {lang}")

    while True:
        choice = input("Enter the number of your language choice: ").strip()
        if choice in language_options:
            selected = language_options[choice]
            print(f"Selected: {selected[0]}")
            return selected[1]  # ISO code or None
        else:
            print("Invalid selection. Please try again.")


# --------------- Recording and Transcribing --------------- #

def record_while_key_held(fs=16000):
    
    recording = []
    is_recording = False
    try:
        while True:
            if keyboard.is_pressed('esc'):
                print("\nExiting.")
                break

            if keyboard.is_pressed('space'):
                if not is_recording:
                    #print("Recording started...")
                    is_recording = True
                    recording = []

                chunk = sd.rec(int(3 * fs), samplerate=fs, channels=1, dtype='int16') # Record a small chunk (e.g., 0.1 sec)
                sd.wait()
                recording.append(chunk.flatten())

            else:
                if is_recording:
                    #print("Recording stopped. Transcribing...")
                    is_recording = False
                    if recording:
                        audio_data = np.concatenate(recording)
                        #print(f"Captured audio max amplitude: {np.max(np.abs(audio_data))}") # For debugging
                        return audio_data  # Return the captured audio 
                    
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        return None

def speak_to_bot(bot, fs:int, language_code:str):
    
    print("\n--- Hold down SPACE to record. Release to stop and transcribe. Press ESC to exit. ---\n")
    while True:
        audio_data = record_while_key_held(fs=fs)
        if audio_data is None:
            break

        audio_data = audio_data.astype(np.float32) / 32768.0    # Normalize and convert to float32

        fd, temp_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)

        try:
            scipy.io.wavfile.write(temp_path, fs, audio_data)
            transcription = bot.transcribe_audio(temp_path, language_code, True)
            print("You said:", transcription)
        finally:
            os.unlink(temp_path)


# --------------- Main --------------- #
def main():
    
    bot = Whisper_Bot(model_name="medium")
    fs = 16000  # Sample rate
    language_code = pick_language() # ISO code
    bot.set_language(language_code)
    
    speak_to_bot(bot, fs, language_code)
    

if __name__ == "__main__":
    main()
