import os
import uvicorn
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from typing import Union
from pydantic import BaseModel
from redis import Redis
from rq import Queue

from tts_coqui import list_models, tts
from stt_whisper import stt
from wsockets import ConnectionManager

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
app.mount("/audios", StaticFiles(directory="files_tts"), name="audios")
manager = ConnectionManager()

@app.get("/api/healthcheck")
async def root():
    return {"message": "OK"}

@app.post("/api/stt")
async def speech_to_text(file: UploadFile = File(...)):
    with open('files_stt/' + file.filename, 'wb') as audio:
        content = await file.read()
        audio.write(content)
        audio.close()
    try:
        queue.enqueue(stt_task, file.filename, on_failure=error_queue)
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
    queue.enqueue(tss_task, args=(textToSpeech.text, textToSpeech.user), on_failure=error_queue)
    return {"message": "OK"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_text_update(client_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)

async def tss_task(text, user):
    client_id, filename = await tts(text, user)
    await manager.send_text_update(client_id, filename)

async def stt_task(filename):
    stt(filename)

def error_queue(job, connection, type, value, traceback):
    print('error', value)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000)
