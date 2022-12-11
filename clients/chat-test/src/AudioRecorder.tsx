import React, { useState } from 'react';

const AudioRecorder: React.FC = () => {
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const chunks: Blob[] = [];
      mediaRecorder.addEventListener('dataavailable', (event: BlobEvent) => {
        chunks.push(event.data);
      });
      mediaRecorder.start();

      setRecording(true);
      setTimeout(() => {
        mediaRecorder.stop();
        setRecording(false);

        const audioBlob = new Blob(chunks, { type: 'audio/webm' });
        setAudioBlob(audioBlob);
      }, 3000);
    } catch (error) {
      console.error('Error accessing the microphone:', error);
    }
  };

  return (
    <div>
      {recording ? (
        <p>Recording audio...</p>
      ) : (
        <button onClick={startRecording}>Start recording</button>
      )}
      {audioBlob ? (
        <audio controls src={URL.createObjectURL(audioBlob)} />
      ) : null}
    </div>
  );
};

export default AudioRecorder;
