import requests

url = 'http://127.0.0.1:5000/api/stt'
file = {'file': open('audio.test.wav', 'rb')}
resp = requests.post(url=url, files=file)
print(resp.json())
