import os
import requests

def tts_coqui(text, filename):
    server = os.getenv("COQUI_TTS_SERVER_URL")
    url = server + "/api/tts?text=" + text
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return filename
    else:
        return None