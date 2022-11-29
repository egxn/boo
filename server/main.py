import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typing import Union
from pydantic import BaseModel

from tts_coqui import tts
from stt_whisper import stt


class User(BaseModel):
    authorization_token: str
    user: str


class Prompt(User, BaseModel):
    prompt: str


class SpeechToText(User, BaseModel):
    speech: str


class Text(User, BaseModel):
    text: str


class TextToText(User, BaseModel):
    lang_source: Union[str, None]
    lang_target: Union[str, None]
    text: str


app = FastAPI()
app.mount("/audios", StaticFiles(directory="files"), name="audios")

@app.get("/api/healtcheck")
async def root():
    return {"message": "OK"}

@app.post("api/stt/")
def speech_to_text(speechToText: SpeechToText):
    stt(speechToText.audio_file)

@app.post("/api/tts")
async def text_to_speech(textToSpeech: Text):
    print(textToSpeech.text)
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
