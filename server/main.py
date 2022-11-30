import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from typing import Union
from pydantic import BaseModel
from redis import Redis
from rq import Queue

from queue_callbacks import success_tts, error_tts, success_stt, error_stt
from tts_coqui import list_models, tts
from stt_whisper import stt


class User(BaseModel):
    authorization_token: str
    user: str


class Prompt(User):
    prompt: str


class Speech(User, UploadFile):
    speech: str


class Text(User):
    text: str


class TextToText(User):
    lang_source: Union[str, None]
    lang_target: Union[str, None]
    text: str


redis_conn = Redis()
queue = Queue(connection=redis_conn)

app = FastAPI()
app.mount("/audios", StaticFiles(directory="files_tss"), name="audios")

@app.get("/api/healtcheck")
async def root():
    return {"message": "OK"}

@app.post("/api/stt")
async def speech_to_text(file: UploadFile = File(...)):
    with open('files_stt/' + file.filename, 'wb') as audio:
        content = await file.read()
        audio.write(content)
        audio.close()
    try:
        queue.enqueue(stt, file.filename, on_success=success_stt, on_failure=error_stt)
        return {"message": "OK"}
    except Exception as e:
        os.remove(file.filename)
        return {"error": str(e)}

@app.get("/api/tts")
async def tts_models():
    tts_models, vocoders_models = await list_models()
    return {"models": tts_models, "vocoders": vocoders_models}

@app.post("/api/tts")
async def text_to_speech(textToSpeech: Text):
    queue.enqueue(tts, args=(textToSpeech.text, textToSpeech.user), on_success=success_tts, on_failure=error_tts)
    return {"message": "OK"}

@app.post("api/analyze/")
async def analyze(text: Text):
    pass

@app.post("api/complete/")
async def complete(text: Text):
    pass

@app.post("api/prompt/")
async def prompt(prompt: Prompt):
    pass

@app.post("api/summarize/")
async def summarize(text: Text):
    pass

@app.post("api/translate/")
async def translate(translate: TextToText):
    pass

@app.post("api/diff/")
async def diff(textA: Text, textB: Text):
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000)
