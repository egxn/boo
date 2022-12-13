# 🐯 Boo

Boo wraps tts and sst on a simple REST API to make it easy to use them in desktop apps.

# Requirements

- [Coqui](https://github.com/coqui-ai/TTS) for TTS.
- [Whisper](https://github.com/openai/whisper) for STT
- [Redis](https://redis.io/) for queueing.
- [FastAPI](https://fastapi.tiangolo.com/) for the Rest API and websockets.

Additional requirements are listed in the `requirements.txt` file.

# Server Development

> cd server
> redis-server
> rq worker --with-scheduler
> python main.py


 
