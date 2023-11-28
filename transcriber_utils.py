import assemblyai as aai
import os

aai.settings.api_key = os.environ.get('assemblyai_key', '')
transcriber = aai.Transcriber()


def audio_to_text(audio_saved):
    config = aai.TranscriptionConfig(language_code=aai.LanguageCode.pt)
    transcript = transcriber.transcribe(f"./uploads/{audio_saved['filename']}", config)
    return transcript.text
