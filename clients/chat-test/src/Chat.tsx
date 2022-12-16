import SpeechToTextButton from './SpeechToTextButton';
import TextToSpeechForm from './TextToSpeechForm';
import { speechToText, textToSpeech } from './services';
import useWsMessages from './useWsMessages';
import './Chat.css';

type Message = {
  id?: number;
  url?: string;
  text?: string;
  type: string;
};

const Message = ({ message }: { message: Message }) => {
  const Loading = () => (<li className='loading'> 🔮 </li>);

  return (
    <>
      { message.text ? (
        <li className="text-message">
          {message.text}
        </li>
      ): <Loading />}
      { message.url ? (
        <li className="audio-message">
          <audio src={message.url} controls />
        </li>
      ): <Loading />}
    </>
  );
}

const Chat = () => {
  const [messages, setMessages] = useWsMessages();

  const stt = async (content: string) => {
    const data = await speechToText(content);
    setMessages([...messages, { id: data.id, type: 'audio', url: content, text: '' }]);
  }

  const tts = async (text: string) => {
    const data = await textToSpeech(text);
    setMessages([...messages, { id: data.id, type: 'text', text: text }]);
  }

  return (
    <div className="chat">
      <ul className="messages">
        {messages.map((message, index) => <Message key={index} message={message} />)}
      </ul>
      <SpeechToTextButton stt={stt}/>
      <TextToSpeechForm tts={tts} />
    </div>
  );
};

export default Chat;