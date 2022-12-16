import { useEffect, useState } from 'react';

const useRecorder = (): [string, boolean, () => void, () => void, () => void] => {
  const [audioURL, setAudioURL] = useState<string>('');
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [recorder, setRecorder] = useState<MediaRecorder| null>(null);

  useEffect(() => {
    if (recorder === null) {
      if (isRecording) {
        requestRecorder().then(setRecorder, console.error);
      }
      return;
    }

    if (isRecording) {
      recorder.start();
    } else {
      recorder.stop();
    }

    const handleData = (event: BlobEvent) => {
      setAudioURL(URL.createObjectURL(event.data));
    };

    recorder.addEventListener("dataavailable", handleData);
    return () => recorder.removeEventListener("dataavailable", handleData);
  }, [recorder, isRecording]);

  const startRecording = () => {
    setIsRecording(true);
  };

  const stopRecording = () => {
    setIsRecording(false);
  };

  const deleteAudio = () => {
    setAudioURL('');
  }

  return [audioURL, isRecording, startRecording, stopRecording, deleteAudio];
};

async function requestRecorder() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  return new MediaRecorder(stream);
}

export default useRecorder;
