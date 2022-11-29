from os import getenv

def get_default_model():
  return getenv("WHISPER_MODEL_NAME")

def stt(audio_file, model=None):
  model = get_default_model() if model is None else model
  if audio_file is not None:
    result = model.transcribe(audio_file)
    return result["text"]
  return None
