import whisper
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def get_default_model():
  return getenv("WHISPER_MODEL_NAME")

def stt(audio_file, model_name=None):
  model_name = get_default_model() if model_name is None else model_name
  model = whisper.load_model(model_name)
  if audio_file is not None:
      print("Processing audio file: %s" % audio_file)
      result = model.transcribe(audio_file)
      print(result["text"])
      return result["text"]
  return None
