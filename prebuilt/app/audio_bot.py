import whisper

class Whisper_Bot:
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)
        self.language_code = None

    def transcribe_audio(self, audio_path: str, fp16:bool) -> str:
        result = self.model.transcribe(audio_path, language=self.language_code, fp16=True)
        return result.get("text", "")
    
    def set_language(self, language_code:str): 
        print("Language code being set: ", language_code)
        self.language_code = language_code
