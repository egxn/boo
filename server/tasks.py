from requests import post
from integrations.llm_llama import llm
from integrations.tts_coqui import tts, xtts
from integrations.stt_whisper import stt

URL_HOOK = 'http://localhost:5000/api/hook'
API_DOMAIN = 'localhost:5000'

async def llm_task(prompt, n, user, id):
    output = await llm(prompt=prompt, n=n)

    data = {
        'id': id ,
        'user': user,
        'output': output,
        'prompt': prompt,
        'content_type': 'llm'
    }
    post(URL_HOOK, json=data)

async def tts_task(text, user, id):
    client_id, filename = await tts(text, user)
    data = {
        'id': id ,
        'user': client_id,
        'url': 'http://' + API_DOMAIN + '/audios/' + filename,
        'text': text,
        'content_type': 'tts'
    }
    post(URL_HOOK, json=data)

async def xtts_task(text, user, id):
    client_id, filename = await xtts(text, user)
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