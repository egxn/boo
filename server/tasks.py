from requests import post
from tts_coqui import tts
from stt_whisper import stt

url_hook = 'http://localhost:5000/api/hook'

async def tss_task(text, user):
    client_id, filename = await tts(text, user)
    data = {'text': filename, 'user': client_id }
    post(url_hook, json=data)


async def stt_task(filename, user):
    text = stt(filename)
    data = {'text': text, 'user': user }
    post(url_hook, json=data)

def error_queue(job, connection, type, value, traceback):
    print('error', value)