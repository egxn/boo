from utils import set_microphone, record_audio, get_timestamp
from stt import stt
from tts import tts

import whisper

def main():
    set_microphone()
    model = os.getenv("WHISPER_MODEL_NAME")
    while True:
        print("Press Enter to start recording")
        print("Press Ctrl+C to stop recording")
        try:
            input()
            filename = get_timestamp()
            audio_file = record_audio(duration=30, filename=filename + ".user.wav")
            text = stt(model, audio_file)
            print(text)
            tts(text, filename + ".coqui.wav")
        except KeyboardInterrupt:
            print("Exiting")
            break

if __name__ == "__main__":
    main()