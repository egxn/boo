import React from 'react';
import AudioRecorder from './AudioRecorder';
import './Chat.css';

type Message = {
  type: string;
  content: string;
} | {
  type: string;
  content: string;
};

const Chat = () => {
  const API_DOMAIN = 'localhost:5000';
  const WS = `ws://${API_DOMAIN}/ws`;
  const API = `http://${API_DOMAIN}/api`;
  const AUDIOS_URL = `http://${API_DOMAIN}/audios`;
  const [messages, setMessages] = React.useState<Message[]>([]);

  React.useEffect(() => {
    const ws = new WebSocket(`${WS}/1312`);
    ws.onmessage = (event) => {
      const message = { type: 'audio', content: event.data as string};
      setMessages([...messages, message]);
    };

    ws.onerror = (error) => {
      console.error(error);
    };
  }, []);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const message = (event.target as HTMLFormElement).message.value;
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

    setMessages([...messages, { type: 'text', content: message }]);
  };

  return (
    <div className="chat">
      <ul className="messages">
        {messages.map((message, index) => (
          message.type === 'text' ? (
            <li key={index} className="text-message">
              {message.content}
            </li>
          ) : (
              <li key={index} className="audio-message">
                <audio src={`${AUDIOS_URL}/${message.content}`} controls />
              </li>
          )
        ))}
      </ul>

      <form onSubmit={handleSubmit} className="message-form">
        <input type="text" name="message" className="message-input"/>
        <button type="submit" className="send-button">Send</button>
        <AudioRecorder />
      </form>
    </div>
  );
};

export default Chat;