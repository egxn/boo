# 🐯 Boo

Boo wraps tts and sst on a simple REST API to make it easy to use them in desktop apps.

# Requirements

- [Coqui](https://github.com/coqui-ai/TTS) for TTS.
- [Whisper](https://github.com/openai/whisper) for STT
- [Redis](https://redis.io/) for queueing.
- [FastAPI](https://fastapi.tiangolo.com/) for the Rest API and websockets.

Additional requirements are listed in the `requirements.txt` file.

# Server Development

./run.sh

# Client use

1. Create a new websocket connection to `ws://localhost:5000/ws/{client_id}`
2. Consume the API (using the same the client_id).
3. The tasks queued using the REST API and the outcome will be sent using the websocket.

# Example clients list

### Web addon for chapGPT

Adds a button to the right of the `<p>` tags with the p selected to generate audio from the selected text and a button on the bottom input to transcribe audio to text.

### Web addon Parrot

Adds a parrot button at the right of to the `<p>` tags  with the p selected to generate audio from the selected text.

### Template

A template to use as a starting point for your own client.
