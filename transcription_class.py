
import time
import whisper
import os
from pyannote.audio import Pipeline, Inference
import streamlit as st
from outputmanager_class import OutputManager
from fileoperation_class import FileOperation  

class Transcription:

   # Here the variable "AUTH_TOKEN_VOCATIO" should contain the token that 
   # you have recieved for the diarization model from hugging face (as "..." 
   # which is a long string with letters and numbers) or it is loaded as 
   # envronmental variables in "windows" by using "os.getenv("...")" command.
    AUTH_TOKEN_VOCATIO = os.getenv("AUTH_TOKEN_VOCATIO")
    WHIS_MODEL = "medium"

    @st.cache_resource
    def load_models():

        start_time_pipeline = time.perf_counter()
        vad_pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection", use_auth_token = Transcription.AUTH_TOKEN_VOCATIO)
        embedding_model = Inference("pyannote/embedding", use_auth_token = Transcription.AUTH_TOKEN_VOCATIO)
        diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token = Transcription.AUTH_TOKEN_VOCATIO)
        end_time_pipeline = time.perf_counter()
        print(f"Loading the diarization models took {end_time_pipeline - start_time_pipeline:.2f} s.\n")

        start_time_whisper = time.perf_counter()
        model = whisper.load_model(Transcription.WHIS_MODEL)
        end_time_whisper = time.perf_counter()
        print(f"Loading the Whisper model took {end_time_whisper - start_time_whisper:.2f} s.\n")

        # The "FileOperation" class is used to safely create
        # new folders without risking to overwrite existing folders.
        # Minimal information should be written by this filehandling.
        fileoperation = FileOperation()
        fileoperation.setIsVerbose(False)

        # Create the empty folders: "temp", "video" and "audio" if
        # they do not exist. This should only be done once, when the 
        # program starts.
        fileoperation.create_folder_if_not_exists("temp")
        fileoperation.create_folder_if_not_exists("video")
        fileoperation.create_folder_if_not_exists("audio")

        return vad_pipeline, embedding_model, diarization_pipeline, model

    def __init__(self, st):

        if not Transcription.AUTH_TOKEN_VOCATIO:
           print("Authorization token from hugging face not found! Please set your AUTH_TOKEN_VOCATIO environment variable.")

        self.st = st

        self.vad_pipeline, self.embedding_model, self.diarization_pipeline, self.model = Transcription.load_models()
        self.output_manager = OutputManager(self.st)

    def transcribe_audio(self, file_path, progress_bar = None):

        start_time_transcription = time.perf_counter()
        result = self.model.transcribe(file_path)
        end_time_transcription = time.perf_counter()
        print(f"Transcription took {end_time_transcription - start_time_transcription:.2f} s.\n")
        if progress_bar:
            progress_bar.progress(50)
        return result

    def diarize_audio(self, file_path, progress_bar = None):

        start_time_vad = time.perf_counter()
        vad = self.vad_pipeline(file_path)
        end_time_vad = time.perf_counter()
        print(f"VAD took {end_time_vad - start_time_vad:.2f} s.\n")
        
        start_time_diarization = time.perf_counter()
        diarization = self.diarization_pipeline(file_path)
        end_time_diarization = time.perf_counter()
        print(f"Diarization took {end_time_diarization - start_time_diarization:.2f} s.\n")
        if progress_bar:
            progress_bar.progress(100)
        return diarization

    def align_transcription_with_diarization(self, transcription_result, diarization_result):

        segments = transcription_result["segments"]
        speaker_transcriptions = {}
        full_conversation = []

        for segment in segments:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]

            matched = False
            for turn, _, spk in diarization_result.itertracks(yield_label=True):
                if turn.start <= start < turn.end or turn.start < end <= turn.end:
                    if spk not in speaker_transcriptions:
                        speaker_transcriptions[spk] = []
                    speaker_transcriptions[spk].append(text)
                    full_conversation.append((start, spk, text))
                    matched = True
                    break

            if not matched:
                full_conversation.append((start, "UNKNOWN", text))

        full_conversation.sort()  # Sort by start time

        return {"full_conversation": full_conversation, "speaker_transcriptions": speaker_transcriptions}
   
    def calculate_speaker_talk_time(self, diarization_result):

        def convert_speaker_label_to_int(speaker_label):
            return int(speaker_label.split('_')[1])

        def convert_int_to_speaker_label(number):
            return f"SPEAKER_{number:02}"

        nr_speakers = 0
        sp_tot_time_vect = []

        for turn, _, spk in diarization_result.itertracks(yield_label=True):
            speaker_int = convert_speaker_label_to_int(spk)
            nr_speakers = max(nr_speakers, speaker_int + 1)
            if len(sp_tot_time_vect) <= speaker_int:
                sp_tot_time_vect.extend([0] * (speaker_int + 1 - len(sp_tot_time_vect)))
            sp_tot_time_vect[speaker_int] += (turn.end - turn.start)

        speaker_times = {}
        for j in range(nr_speakers):
            speaker_label = convert_int_to_speaker_label(j)
            speaker_times[speaker_label] = round(sp_tot_time_vect[j], 2)

        return speaker_times


    def write_full_conversation_on_screen(self, full_conversation):

        self.output_manager.write_full_conversation(full_conversation)

    def write_talk_times_on_screen(self, speaker_times, use_blank_rows):

        self.output_manager.write_talk_times(speaker_times, use_blank_rows)

    def format_full_conversation(self, full_conversation):

        return self.output_manager.format_full_conversation(full_conversation)
    