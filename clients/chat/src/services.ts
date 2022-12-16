const API_DOMAIN = 'localhost:5000';
const API = `http://${API_DOMAIN}/api`;
const USER_ID = '1312';

const textToSpeech = async (message: string) => {
  try {
    const response = await fetch(`${API}/tts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', },
      body: JSON.stringify({ user: USER_ID, text: message }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
};

const speechToText = async (audioUrl: string) => {
  try {
    const filename = new Date().getTime();
    const body = new FormData();
    const audioFile = await fetch(audioUrl)
      .then(r => r.blob())
      .then(blob => new File([blob], `${USER_ID}_${filename}.wav`, { type: "audio/wav" }));

    body.append('file', audioFile);

    const response = await fetch(`${API}/stt/${USER_ID}`, {
      method: 'POST',
      body,
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
};

export { speechToText, textToSpeech };