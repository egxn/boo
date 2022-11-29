import sounddevice as sd
import soundfile as sf
import time

def get_timestamp():
    return str(int(time.time()))

def list_microphones():
    print(sd.query_devices())

def set_microphone():
    sd.default.device = 'REDRAGON Live Camera'

def record_audio(fs=44100, channels=2, duration=10, filename=""):
  try:
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    return filename
  except Exception as e:
    print(e)
    return None