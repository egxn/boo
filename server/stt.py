def stt_whisper(model, audio_file):
  if audio_file is not None:
    result = model.transcribe(audio_file)
    return result["text"]
  return None
