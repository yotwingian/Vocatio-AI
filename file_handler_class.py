
import json

class FileHandler:

    def __init__(self, file_path = 'transcriptions.json'):

        self.file_path = file_path

    def save_transcriptions(self, transcriptions):

        with open(self.file_path, 'w') as f:

            json.dump(transcriptions, f)

    def load_transcriptions(self):

        try:

            with open(self.file_path, 'r') as f:

                return json.load(f)
            
        except FileNotFoundError:

            return []
        