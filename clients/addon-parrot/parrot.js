const API_DOMAIN = 'localhost:5000'
const API = `http://${API_DOMAIN}/api`
const WS = `ws://${API_DOMAIN}/ws`
const USER_ID = '8419'

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

const ws = new WebSocket(`${WS}/${USER_ID}`)
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

const ps = document.querySelectorAll('p')
ps.forEach((p) => {
  const btn = document.createElement('button')
  btn.innerText = '🦜'
  btn.style.float = 'right'
  btn.addEventListener('click', async () => {
    if (p.innerText !== '') {
      const { id } = await textToSpeech(p.innerText.replace('🦜', ''))
      p.setAttribute('data-ttsid', id)
    }
  })
  p.appendChild(btn)
})
