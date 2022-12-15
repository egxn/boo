import { FormEvent, useState } from 'react';
import './TextToSpeechForm.css';

const TextToSpeechForm = ({ tts }: { 
  tts: (text: string ) => Promise<void> 
}) => {
  const [text, setText] = useState<string>('');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!text) {
      return;
    }

    await tts(text);
    setText('');
  }

  const handleChange = (event: FormEvent<HTMLInputElement>) => {
    setText(event.currentTarget.value);
  }

  return (
    <form className="message-form" onSubmit={handleSubmit}>
      <input className="message-input" name="message" onChange={handleChange} value={text} type="text" />
      <button className="send-button" type="submit">🔮</button>
    </form>
  )
}

export default TextToSpeechForm;