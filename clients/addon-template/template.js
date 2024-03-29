const API_DOMAIN = 'localhost:5000'
const API = `http://${API_DOMAIN}/api`
const WS = `ws://${API_DOMAIN}/ws`
const USER_ID = '1312'

const textToSpeech = async (message) => {
  try {
    const response = await fetch(`${API}/tts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', },
      body: JSON.stringify({ user: USER_ID, text: message }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status} ${response.statusText}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error(error)
  }
}

const speechToText = async (audioUrl) => {
  try {
    const filename = new Date().getTime()
    const body = new FormData()
    const audioFile = await fetch(audioUrl)
      .then(r => r.blob())
      .then(blob => new File([blob], `${USER_ID}_${filename}.wav`, { type: "audio/wav" }))

    body.append('file', audioFile)

    const response = await fetch(`${API}/stt/${USER_ID}`, {
      method: 'POST',
      body,
    })

    const data = await response.json()
    return data
  } catch (error) {
    console.error(error)
  }
}

async function requestRecorder() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  const recorder = new MediaRecorder(stream)
  const chunks = []

  recorder.ondataavailable = (event) => {
    chunks.push(event.data)
  }

  recorder.onstop = async () => {
    const blob = new Blob(chunks, { type: "audio/wav" })
    const audioURL = window.URL.createObjectURL(blob)
    await speechToText(audioURL)
  };

  return recorder
}

const ws = new WebSocket(`${WS}/1312`)
ws.onmessage = (event) => {
  const { id, content_type: contentType, text, url } = JSON.parse(event.data)
  if (contentType === 'tts') {
    const el = document.querySelector(`[data-ttsid="${id}"]`)
    if (el) {
      el.style.outline = '1px solid blue'
      const audio = document.createElement('audio')
      audio.style.width = '100%'
      audio.controls = true
      audio.src = url
      el.appendChild(audio)
    }
  } else {
    console.log('unknown message', event.data)
  }
}

ws.onerror = (error) => {
  console.error(error)
}