import numpy as np
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import os
import json
from playsound import playsound
import requests
import sys
from fuzzywuzzy import process


"""Voice Command Service [VCS]"""

#This is the code for voice commands! 


#TODO: Transcribe only words instead of phrases.
#TODO: Better Integration w/ front-end emotion screen (Usr feedback).



class SpeechRecognitionService:
    def __init__(self):
        model_path = "./Services/HeliosVoice/model"
        print(f"[INF|VCS] Looking for model in: {os.path.abspath(model_path)}")
        if not os.path.exists(model_path):
            print(f"[CRIT.ERR|VCS] Model path does not exist: {os.path.abspath(model_path)}")
            exit(1)
        
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.commands = {
            "bark": self.bark,
            "search": self.search,
            "how are you": self.respond_status,
            "take a photo": self.photo
        }
        self.active = False 
        self.activation_word = "helios"

    def match_activation_word(self, recognized_text, threshold=75):
        #match activation word with a threshold
        best_match, score = process.extractOne(recognized_text, [self.activation_word])
        print(f"[INF|VCS] Checking activation word: Heard '{recognized_text}', Matched '{best_match}' with score {score}%")
        if score >= threshold:
            return True, score
        return False, score  #always returns a tuple

    def match_command(self, recognized_text, threshold=75):
        #find the best match w/ a threshold
        best_match, score = process.extractOne(recognized_text, self.commands.keys())
        print(f"[INF|VCS] Checking command: Heard '{recognized_text}', Best match '{best_match}' with score {score}%")
        if score >= threshold:
            return best_match
        return None

    def bark(self):
        print("[INF|VCS] Barking.")
        playsound('./Services/HeliosVoice/bark.ogg')
        self.send_command_update("bark")

    def search(self):
        print("[INF|VCS] Searching.")
        self.send_command_update("search")

    def respond_status(self):
        print("[INF|VCS] I am good, thank you for asking.")
        self.send_command_update("how are you")

    def photo(self):
        print("[INF|VCS] Photo taken!")
        self.send_command_update("take a photo")

    def send_command_update(self, command):
        print(f"[INFO|SR] Command executed: {command}, sending data.")
        response = requests.post('http://localhost:5000/command_executed', json={'command': command})
        print(f"[INFO|SR] Server response: {response.text}")

    def listen_and_transcribe(self):
        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            data = indata.astype(np.int16).tobytes()
            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                command = result.get('text', '').lower().strip()
                if command:
                    print(f"[INF|VCS] Heard: {command}")
                    if not self.active:
                        matched, score = self.match_activation_word(command)  #unpack values here
                        if matched:
                            self.active = True
                            print(f"[INF|VCS] Activation word recognized with score {score}%. Ready for command.")
                    else:
                        matched_command = self.match_command(command)
                        if matched_command:
                            self.commands[matched_command]()
                            self.active = False  #reset to wait for another activation

        # Open the microphone stream
        with sd.InputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=callback):
            print("[INF|VCS] Listening, say 'Helios' to activate!")
            while True:
                pass

if __name__ == "__main__":
    service = SpeechRecognitionService()
    service.listen_and_transcribe()
