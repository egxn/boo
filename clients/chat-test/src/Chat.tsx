import React from 'react';
import AudioRecorder from './SpeechToTextButton';
import './Chat.css';
import TextToSpeechForm from './TextToSpeechForm';

type Message = {
  id: number;
  type: string;
  content: string;
} | {
  id: number;
  type: string;
  content: string;
};

const Message = ({ message }: { message: Message }) => {
  if (message.type === 'text') {
    return (
      <li className="text-message">
        {message.content}
      </li>
    );
  } else if (message.type === 'audio') {
    return (
      <li className="audio-message">
        <audio src={message.content} controls />
      </li>
    );
  }

  return null;
}

const Chat = () => {
  const API_DOMAIN = 'localhost:5000';
  const WS = `ws://${API_DOMAIN}/ws`;
  const API = `http://${API_DOMAIN}/api`;
  const AUDIOS_URL = `http://${API_DOMAIN}/audios`;
  const [messages, setMessages] = React.useState<Message[]>([]);

  React.useEffect(() => {
    const ws = new WebSocket(`${WS}/1312`);
    ws.onmessage = (event) => {
      const [contentType = '', content = ''] = event.data.split(':::')
      const message = { id: messages.length ,content: content.trim(), type: contentType.trim() };
      setMessages([...messages, message]);
    };

    ws.onerror = (error) => {
      console.error(error);
    };
  }, []);

  const textToSpeech = async (message: string) => {
    setMessages([...messages, { content: message, id: messages.length , type: 'text' }]);

    try {
      const response = await fetch(`${API}/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify({ user: '1312', text: message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status} ${response.statusText}`);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="chat">
      <ul className="messages">
        {messages.map((message, index) => <Message key={index} message={message} />)}
      </ul>
      <AudioRecorder stt={()=>{}}/>
      <TextToSpeechForm tts={textToSpeech} />
    </div>
  );
};

export default Chat;