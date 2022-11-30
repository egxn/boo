def success_tts(job, connection, result):
    print('TTS succes', result)


def error_tts(job, connection, type, value, traceback):
    print('TTS error', value)


def success_stt(job, connection, result):
    print('STT succes', result)


def error_stt(job, connection, type, value, traceback):
    print('STT error', value)
