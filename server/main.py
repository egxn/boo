import os
import uvicorn
from fastapi import Body, FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis import Redis
from rq import Queue

from tasks import stt_task, tss_task, error_queue
from tts_coqui import list_models
from wsockets import ConnectionManager

class User(BaseModel):
    user: str

class Text(User):
    text: str

redis_conn = Redis()
queue = Queue(connection=redis_conn)
manager = ConnectionManager()
app = FastAPI()

origins = [
    "http://localhost:5000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/audios", StaticFiles(directory="files_tts"), name="audios")


@app.get("/api/healthcheck")
async def root():
    return {"message": "OK"}

@app.post("/api/stt/{user}")
async def speech_to_text(user:str, file: UploadFile = File(...)):
    filename = 'files_stt/' + file.filename
    print(filename)
    with open(filename, 'wb') as audio:
        content = await file.read()
        audio.write(content)
        audio.close()
    try:
        queue.enqueue(stt_task, filename, user, on_failure=error_queue)
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

@app.post("/api/hook")
async def send_message(text: Text):
    await manager.send_text_update(text.user, text.text)
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000)
