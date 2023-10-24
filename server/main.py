import os
import uvicorn
from fastapi import Body, FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis import Redis
from rq import Queue
from rq.registry import FinishedJobRegistry, StartedJobRegistry
from wsockets import ConnectionManager

from integrations.tts_coqui import list_models
from tasks import llm_task, stt_task, tts_task, xtts_task, error_queue
from utils import create_id, calculate_wer

class User(BaseModel):
    user: str

class Text(User):
    text: str

class LlmPayload(Text):
    n: int

class WerPayload(BaseModel):
    reference: str
    hypothesis: str

class HookPayload(User):
    id: str
    url: str
    text: str
    content_type: str
    
redis_conn = Redis()
queue = Queue(connection=redis_conn)
queue.empty()
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

@app.post("/api/stt/{user}", status_code=201)
async def speech_to_text(user:str, file: UploadFile = File(...)):
    filename = 'files_stt/' + file.filename
    with open(filename, 'wb') as audio:
        content = await file.read()
        audio.write(content)
        audio.close()
    try:
        id = create_id()
        queue.enqueue(stt_task, args=(filename, user, id), on_failure=error_queue)
        return {"message": "OK", "id": id}
    except Exception as e:
        os.remove(file.filename)
        return {"error": str(e)}

@app.post("/api/wer/")
async def score(payload: WerPayload):
    try:
        return {"score": calculate_wer(payload.reference, payload.hypothesis)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/tts")
async def text_to_speech_models():
    tts_models = await list_models()
    return {"models": tts_models }

@app.post("/api/tts", status_code=201)
async def text_to_speech(textToSpeech: Text):
    id = create_id()
    queue.enqueue(tts_task, args=(textToSpeech.text, textToSpeech.user, id), on_failure=error_queue)
    return {"message": "OK", "id": id}

@app.post("/api/xtts", status_code=201)
async def text_to_speech_x(textToSpeech: Text):
    id = create_id()
    job = queue.enqueue(xtts_task, args=(textToSpeech.text, textToSpeech.user, id), on_failure=error_queue)
    return {"message": "OK", "id": id}

@app.post("/api/llm", status_code=201)
async def long_language_model(textToText: LlmPayload):
    id = create_id()
    print(textToText.text)
    queue.enqueue(llm_task, args=(textToText.text, textToText.n,
                  textToText.user, id), on_failure=error_queue, job_timeout=1000)
    return {"message": "OK", "id": id}

@app.post("/api/hook")
async def send_message(payload: HookPayload):
    await manager.send_text_update(payload.id, payload.user, payload.url, payload.text, payload.content_type)
    return {"message": "OK", "id": payload.id}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_text_update(client_id, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id, queue)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000)
