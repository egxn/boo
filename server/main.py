import os
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from typing import Union
from pydantic import BaseModel

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


app = FastAPI()
app.mount("/audios", StaticFiles(directory="files"), name="audios")

@app.get("/api/healtcheck")
async def root():
    return {"message": "OK"}

@app.post("/api/stt")
async def speech_to_text(file: UploadFile = File(...)):
    with open(file.filename, 'wb') as audio:
        content = await file.read()
        audio.write(content)
        audio.close()
    try:
        text = stt(file.filename)
        os.remove(file.filename)
        return {"text": text}
    except Exception as e:
        os.remove(file.filename)
        return {"error": str(e)}

@app.get("/api/tts")
async def tts_models():
    tts_models, vocoders_models = await list_models()
    return {"models": tts_models, "vocoders": vocoders_models}

@app.post("/api/tts")
async def text_to_speech(textToSpeech: Text):
    filename = await tts(textToSpeech.text, textToSpeech.user)
    return {"filename": filename}

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

@app.get("/audios")
def audios():
    out = []
    for filename in os.listdir("files"):
        out.append({
            "name": filename.split(".")[0],
            "path": "/files/" + filename
        })
    return out

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000)
