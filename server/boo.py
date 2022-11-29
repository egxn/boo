import asyncio
from jiwer import wer
from utils import set_microphone, record_audio, get_timestamp
from stt_whisper import stt
from tts_coqui import tts

async def main():
    set_microphone()
    while True:
        print("Press Enter to start recording")
        print("Press Ctrl+C to stop recording")
        try:
            input()
            filename = get_timestamp()
            audio_file = record_audio(duration=30, filename=filename + ".user.wav")
            text = stt(audio_file)
            await tts(text, filename + ".coqui.wav")
            coqui_text = stt(filename + ".coqui.wav")
            jiwer_score = wer(text, coqui_text)
            print(f"Jiwer score: {jiwer_score}")
        except KeyboardInterrupt:
            print("Exiting")
            break

asyncio.run(main())
