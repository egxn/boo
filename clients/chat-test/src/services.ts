const API_DOMAIN = 'localhost:5000';
const API = `http://${API_DOMAIN}/api`;

const textToSpeech = async (message: string) => {
  try {
    const response = await fetch(`${API}/tts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', },
      body: JSON.stringify({ user: '1312', text: message }),
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


export { textToSpeech };