from requests import post
from tts_coqui import tts
from tts_coqui_py import tts as tts_py
from stt_whisper import stt


URL_HOOK = 'http://localhost:5000/api/hook'
API_DOMAIN = 'localhost:5000'

async def tts_task(text, user, id):
    # client_id, filename = await tts(text, user)
    client_id, filename = await tts_py(text, user)
    data = {
        'id': id ,
        'user': client_id,
        'url': 'http://' + API_DOMAIN + '/audios/' + filename,
        'text': text,
        'content_type': 'tts'
    }
    post(URL_HOOK, json=data)


async def stt_task(filename, user, id):
    text = stt(filename)
    data = {
        'id': id,
        'user': user,
        'url': filename,
        'text': text,
        'content_type': 'stt'
    }
    post(URL_HOOK, json=data)

def error_queue(job, connection, type, value, traceback):
    print('error', value)