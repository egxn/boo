import { useEffect, useState } from "react";

type Message = {
  id?: number;
  content?: string;
  type: string;
  text: string;
};

const useWsMessages = (): [Message[], (msgs: Message[]) => void] => {
  const API_DOMAIN = 'localhost:5000';
  const WS = `ws://${API_DOMAIN}/ws`;
  const AUDIOS_URL = `http://${API_DOMAIN}/audios`;

  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    const ws = new WebSocket(`${WS}/1312`);
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      const msgs = messages.map((message) => message.id === msg.id 
        ? { ...message, content: `${AUDIOS_URL}/${msg.content}` } 
        : message
      );

      setMessages(msgs);
    };

    ws.onerror = (error) => {
      console.error(error);
    };
  }, [messages]);


  return [messages, setMessages];
};

export default useWsMessages;