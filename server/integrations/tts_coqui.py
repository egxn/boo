import time

from dotenv import load_dotenv
from os import getenv
from TTS.api import TTS

load_dotenv()


def get_default_language():
    return getenv("COQUI_TTS_LANGUAGE")

def get_use_cuda():
    return getenv("USE_CUDA") == '1'

async def list_models():
    return TTS.list_models()

async def list_speakers(model=None):
    if model is None:
        model = getenv("COQUI_TTS_MODEL_NAME")
    tts = TTS(model)
    return tts.speakers


async def tts(text: str, prefix="", model=None, speaker_id=None):
    """Text to speech
    Args:
        text (str): text to convert to speech
        prefix (str, optional): output filename. Defaults timestamp.
        model (str): model to use
    Returns:
        filename (str): output filename
    """
    filename = prefix + "_" + str(int(time.time())) + '.coqui.wav'
    model_name = getenv("COQUI_TTS_MODEL_NAME") if model is None else model
    tts = TTS(model_name=model_name, progress_bar=False, gpu=get_use_cuda())
    tts.tts_to_file(text=text, file_path='files_tts/' + filename)
    return (prefix, filename)

async def xtts(text: str, prefix=""):
    filename = prefix + "_" + str(int(time.time())) + '.coqui.wav'
    speaker_wav = "tts_coqui_teacher.wav"
    device = "cuda" if get_use_cuda() else "cpu"
    print(f"Using device: {device}")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v1").to(device)
    tts.tts_to_file(text=text, speaker_wav=speaker_wav, language="en", file_path='files_tts/' + filename)
    return (prefix, filename)


async def main():
    print(await tts("This is a test", "test"))
