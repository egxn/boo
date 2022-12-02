import requests

api_url = 'http://localhost:5000/api'

def test_stt():
  url_stt = api_url + '/stt/1312'
  file = {'file': open('audio.test.wav', 'rb')}
  resp = requests.post(url=url_stt, files=file)
  print(resp.json())

def test_tts():
  url_tts = api_url + '/tts'
  data = {'text': 'Hello world', 'user': '1312'}
  resp = requests.post(url=url_tts, json=data)
  print(resp.json())

def main():
  test_stt()
  test_tts()

if __name__ == '__main__':
  main()
