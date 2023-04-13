# 🐯 Boo

Boo is a local REST API to use ML models in local desktop apps.

# Models

You need install each tool following the instructions in the model's repository.

- 🐸 [Coqui](https://github.com/coqui-ai/TTS) for text to speech
- 🦙 [Llama](https://github.com/ggerganov/llama.cpp) for large language models
- 👁️‍🗨️ [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) for OCR (in progress)
- 👄 [Whisper](https://github.com/openai/whisper) for speech to text

# How it works

- ⚡ [FastAPI](https://fastapi.tiangolo.com/) for the REST API and websockets.
- 🟥 [Redis](https://redis.io/) for queueing.

Additional requirements are listed in the `requirements.txt` file.

# Server Development

./run.sh

# How to use it in your app

1. Create a new websocket connection to `ws://localhost:5000/ws/{client_id}`
2. Consume the API (using the same the client_id).
3. The tasks are queued using the REST API and the outcome will be sent using the websocket.

# Example clients list

### Web addon for chapGPT

Adds a button to the right of the `<p>` tags with the p selected to generate audio from the selected text and a button on the bottom input to transcribe audio to text.

### Web addon Parrot

Adds a parrot button at the right of to the `<p>` tags  with the p selected to generate audio from the selected text.

