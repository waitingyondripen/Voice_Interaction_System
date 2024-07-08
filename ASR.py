import wave
from websockets.sync.client import connect
import json
import time

class ASR:
    def __init__(self):
        self.asr_url = "ws://localhost:10095"
        self.hearing_voice_path = "./wav_file/hear.wav"

    def asr(self):
        wf = wave.open(self.hearing_voice_path, 'rb')
        hearing_bytes = wf.readframes(wf.getnframes())
        with connect(self.asr_url) as websocket:
            # send wav data
            websocket.send(hearing_bytes)
            # send args
            websocket.send(json.dumps({"mode": "offline", "is_speaking": False, "chunk_interval":10, "wav_name":"h5", "chunk_size":[5,10,5]}))
            # recv result
            message = websocket.recv()
            message = json.loads(message)
        time.sleep(1)
        
        return message["text"]

asr = ASR()