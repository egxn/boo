import AudioRecorder from './SpeechToTextButton';
import TextToSpeechForm from './TextToSpeechForm';
import { textToSpeech } from './services';
import useWsMessages from './useWsMessages';
import './Chat.css';

type Message = {
  id?: number;
  content?: string;
  type: string;
  text: string;
};

const Message = ({ message }: { message: Message }) => {
  return (
    <>
      <li className="text-message">
        {message.text}
      </li>
      { message.content && (
        <li className="audio-message">
          <audio src={message.content} controls />
        </li>
      )}
    </>
  );
}

const Chat = () => {
  const [messages, setMessages] = useWsMessages();

  const tts = async (text: string) => {
    const data = await textToSpeech(text);
    setMessages([...messages, { id: data.id, type: 'text', text: text }]);
  }

  return (
    <div className="chat">
      <ul className="messages">
        {messages.map((message, index) => <Message key={index} message={message} />)}
      </ul>
      <AudioRecorder stt={()=>{}}/>
      <TextToSpeechForm tts={tts} />
    </div>
  );
};

export default Chat;