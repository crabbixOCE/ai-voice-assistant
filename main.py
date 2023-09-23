from listener import listener
from s2t import transcribe_audio
from response import generate_response
import os
import elevenlabs as el
from apiKey import api_key
el.set_api_key(api_key)
myvoice = [v for v in el.voices() if v.name=="alexmk2" ][0]
listener = listener(talking_threshold=10)

def main():
    while True:
        fname = next(listener)
        if fname == "nothing recorded":
            continue
        audio = transcribe_audio(fname)
        os.remove(fname)
        if audio:
            print(audio)
            audio_stream = el.generate(
                                    text=generate_response(audio),
                                    stream=True,
                                    voice=myvoice,   
                                    )
            el.stream(audio_stream)
main()