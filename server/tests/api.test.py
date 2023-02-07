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

def test_wer():
  print('test_wer')
  url_wer = api_url + '/wer/'
  data = {'reference': 'Hello world', 'hypothesis': 'Hello world'}
  resp = requests.get(url=url_wer, json=data)
  print(resp.json().get('score') == 0.0)

def main():
  test_stt()
  test_tts()
  test_wer()

if __name__ == '__main__':
  main()
