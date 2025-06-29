import whisper

class Whisper_Bot:
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)

    def transcribe_audio(self, audio_path: str, language_code: str = None, fp16: bool = True) -> str:
        result = self.model.transcribe(audio_path, language=language_code, fp16=fp16)
        return result.get("text", "")
