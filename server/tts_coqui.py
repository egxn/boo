import asyncio
import time
from dotenv import load_dotenv
from os import getenv

load_dotenv()

args = {
  "list_models": "--list_models",
  "list_speaker_idxs": "--list_speaker_idxs",
  "model_name": "--model_name",
  "out_path": "--out_path",
  "use_cuda": "--use_cuda",
  "speaker_idx": "--speaker_idx",
  "text": "--text",
}

def get_default_model():
    return getenv("COQUI_TTS_MODEL_NAME")

def get_default_speaker_id():
    return 0

async def list_models():
    """List all available models
    
    Returns:
        ([tts_models], [vocoder_models])
    """
    proc = await asyncio.create_subprocess_exec('tts', 
        args['list_models'],
        args['use_cuda'], "true",
        
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if (stderr):
        print(f'[{stderr.decode()}]')
        return None
    else:
        output = stdout.decode('UTF-8').split('\n')
        models = map(lambda line: line.strip().split(' '), output)
        models = filter(lambda model: len(model) == 2, models)
        models = list(map(lambda model: model[1], models))
        tts_models = filter(lambda model: model.startswith(
            'tts_models'), models.copy())
        vocoders = filter(lambda model: model.startswith(
            'vocoder_models'), models.copy())
        return (list(tts_models), list(vocoders))

async def list_speakers_id(model=None):
    """List all available speakers id
    
    Args:
        model (str): model to use
    Returns:
        [speakers_id]
    """
    model = get_default_model() if model is None else model
    proc = await asyncio.create_subprocess_exec('tts',
        args['model_name'], model,
        args['list_speaker_idxs'],
        args['use_cuda'], "true",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if (stderr):
        print(f'[{stderr.decode()}]')
        return None
    else:
        output = stdout.decode('UTF-8').split('\n')
        return list(output)

async def tts(text: str, prefix="", model=None, speaker_id=None):
    """Text to speech
    Args:
        text (str): text to convert to speech
        prefix (str, optional): output filename. Defaults timestamp.
        model (str): model to use
        speaker_id (str, optional): speaker id. Defaults to None.
    Returns:
        filename (str): output filename
    """
    filename = prefix + str(int(time.time())) + '.coqui.wav'
    model = get_default_model() if model is None else model
    speaker_id = get_default_speaker_id() if speaker_id is None else speaker_id
    proc = await asyncio.create_subprocess_exec('tts', 
        args['text'], text,
        args['model_name'], model,
        args['out_path'], './files/' + filename,
        args['use_cuda'], "true",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    if (stderr):
        print(f'[{stderr.decode()}]')
        return None
    else:
        print(f'[{stdout.decode()}]')
        print(filename)
        return filename

async def main():
    await tts('Hello cats of the world')
