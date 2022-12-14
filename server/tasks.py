from requests import post
from tts_coqui import tts
from stt_whisper import stt

url_hook = 'http://localhost:5000/api/hook'

async def tss_task(text, user):
    client_id, filename = await tts(text, user)
    data = {'content': filename, 'user': client_id, 'content_type': 'url' }
    post(url_hook, json=data)


async def stt_task(filename, user):
    text = stt(filename)
    data = {'content': text, 'user': user, 'content_type': 'text' }
    post(url_hook, json=data)

def error_queue(job, connection, type, value, traceback):
    print('error', value)