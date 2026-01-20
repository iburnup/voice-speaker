from piper import PiperVoice
from pyaudio import PyAudio


class PiperJenny():

    def __init__(self):

        #model = "./en_GB-jenny_dioco-medium"
        #model, config = find_voice(model, "./")

        self.voice = PiperVoice.load("./en_GB-jenny_dioco-medium.onnx")

        try:
            self.p = PyAudio()
        except:
            pass


    def say(self, text_data):

        stream = self.p.open(format = 8,  
            channels = 1,  
            rate = 22050,  
            output = True)

        for audio_chunk in self.voice.synthesize(text_data):
            # Process each chunk
            sample_rate = audio_chunk.sample_rate
            audio_bytes = audio_chunk.audio_int16_bytes
            stream.write(audio_bytes)

        stream.stop_stream()  
        stream.close()

    def stop(self):
        self.p.terminate()
