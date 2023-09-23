import pyaudio
import wave
import datetime
import audioop
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def listener(talking_threshold=300):
    while True:
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        print("* recording")
        frames = []
        silence = 0
        talking = 0
        while True:
            data = stream.read(CHUNK)
            if audioop.rms(data,2)<300:
                silence += 1
                if silence > 70:
                    break
            else:
                talking += 1
                silence = 0
            frames.append(data)
        print("* done recording")
        if talking < talking_threshold:
            yield "nothing recorded"
        else:
            stream.stop_stream()
            stream.close()
            p.terminate()
            fname = f"stream{datetime.datetime.now().strftime('%H%Mm%S')}.wav"
            wf = wave.open(fname, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            yield(fname)