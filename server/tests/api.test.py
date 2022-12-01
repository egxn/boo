import requests

api_url = "http://localhost:5000/api"

url_stt = api_url + '/stt'
file = {'file': open('audio.test.wav', 'rb')}
resp = requests.post(url=url_stt, files=file)
print(resp.json())

url_tts = api_url + '/tts'
data = {'text': 'Hello world', 'user': 1312, 'authorization_token': 'token'}
resp = requests.post(url=url_tts, json=data)
print(resp.json())


