from fastapi import FastAPI
from types import Prompt, SpeechToText, Text, TextToText

app = FastAPI()

@app.get("/api/healtcheck")
async def root():
    return {"message": "OK"}

@app.post("api/stt/")
async def speech_to_text(speechToText: SpeechToText):
    pass

@app.post("/api/tts")
def text_to_speech(textToSpeech: Text):
    pass

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

