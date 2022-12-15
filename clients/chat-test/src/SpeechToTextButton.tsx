import useRecorder from './useRecorder';
import './SpeechToTextButton.css';

const SpeechToTextButton = ({ stt }: { stt: () => void }) => {
  const [audioURL, isRecording, startRecording, stopRecording, deleteAudio] = useRecorder();

  return (
    <div className='speech-to-text'>
      {audioURL && ( 
        <>
          <button
            className='btn'
            onClick={deleteAudio}>
          🗑
          </button>
          <div className='bar'>
            {<audio controls src={audioURL} />}
          </div>
          <button
            className='btn'
            onClick={stt}>
          🔮
          </button>
        </>
      )}
      {!audioURL && (
        <button
          className={`btn record-button ${isRecording ? 'recording' : ''}`}
          onClick={isRecording ? stopRecording : startRecording}>
          🎙
        </button>
      )}
    </div>
  );
};

export default SpeechToTextButton;
