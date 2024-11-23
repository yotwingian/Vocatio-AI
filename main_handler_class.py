
import os
import streamlit as st
from transcription_class import Transcription
from utils_class import Utils
from gpthandler_class import GPTHandler
from outputmanager_class import OutputManager
from file_handler_class import FileHandler


class MainHandler:


   TRANSCRIPTION_RESULT = 'transcription_result'
   DIARIZATION_RESULT = 'diarization_result'
   TRANSCRIPTION_COMPLETED = 'transcription_completed'


   def __init__(self, st, utils = None, file_handler = None, transcription = None, output_manager = None):

      self.st = st

      self.utils = utils or Utils(st)
      self.file_handler = file_handler or FileHandler()
      self.transcription = transcription or Transcription(st)
      self.gpt_handler = GPTHandler()
      self.output_manager = output_manager or OutputManager(st)

      self.summary = ""
      self.analyze = ""

      self.isSummaryAlreadyPressed = False
      self.isAnalyzeAlreadyPressed = False

      self.selectedTranscription = -1

      self.initialize_session_state()

   def initialize_session_state(self):

      self.st.session_state.setdefault('transcription', self.transcription)
      self.st.session_state.setdefault('gpt_handler', self.gpt_handler)
      self.st.session_state.setdefault('output_manager', self.output_manager)
      self.st.session_state.setdefault(self.TRANSCRIPTION_COMPLETED, False)
      self.st.session_state.setdefault('completed_transcriptions', self.file_handler.load_transcriptions())

      if 'summary' not in self.st.session_state:
         self.st.session_state.summary = ""

      if 'analyze' not in self.st.session_state:
         self.st.session_state.analyze = ""

      if 'isSummaryAlreadyPressed' not in self.st.session_state:
         self.st.session_state.isSummaryAlreadyPressed = False

      if 'isAnalyzeAlreadyPressed' not in self.st.session_state:
         self.st.session_state.isAnalyzeAlreadyPressed = False

      if 'selectedTranscription' not in self.st.session_state:
         self.st.session_state.selectedTranscription = -1

   def reset_session_state(self):

      self.st.session_state.pop(self.TRANSCRIPTION_RESULT, None)
      self.st.session_state.pop(self.DIARIZATION_RESULT, None)
      self.st.session_state[self.TRANSCRIPTION_COMPLETED] = False

      self.st.session_state.summary = ""
      self.st.session_state.analyze = ""

      self.st.session_state.isSummaryAlreadyPressed = False
      self.st.session_state.isAnalyzeAlreadyPressed = False

      self.st.session_state.selectedTranscription = -1

   def getSelectedTranscription(self):

      return self.st.session_state["selectedTranscription"]
    
   def setSelectedTranscription(self, selectedTranscription):

      self.st.session_state["selectedTranscription"] = selectedTranscription

   def getSummary(self):

      return self.st.session_state["summary"]
    
   def getAnalyze(self):

      return self.st.session_state["analyze"]

   def setSummary(self, summary):

      self.st.session_state["summary"] = summary

   def setAnalyze(self, analyze):

      self.st.session_state["analyze"] = analyze

   def getIsSummaryAlreadyPressed(self):

      return self.st.session_state["isSummaryAlreadyPressed"]
    
   def getIsAnalyzeAlreadyPressed(self):

      return self.st.session_state["isAnalyzeAlreadyPressed"]

   def setIsSummaryAlreadyPressed(self, isSummaryAlreadyPressed):

      self.st.session_state["isSummaryAlreadyPressed"] = isSummaryAlreadyPressed

   def setIsAnalyzeAlreadyPressed(self, isAnalyzeAlreadyPressed):

      self.st.session_state["isAnalyzeAlreadyPressed"] = isAnalyzeAlreadyPressed

   def process_file(self, file_path):

      try:

         aligned_results, speaker_times = self.process_transcription_and_diarization(file_path)
         self.update_session_state(file_path, aligned_results, speaker_times)
         self.st.success("File processed successfully.")

      except Exception as e:

         self.st.error(f"Error processing file: {e}")

   def save_summary_to_transcriptions(self, summary):

      index = self.getSelectedTranscription()

      print(index)
      # print(summary)

      if index < 0:

         return

      if len(summary) < 1:

         return

      new_transcription = self.st.session_state.completed_transcriptions[index]
      new_transcription['summary'] = summary
      self.st.session_state.completed_transcriptions[index] = new_transcription
      self.file_handler.save_transcriptions(self.st.session_state.completed_transcriptions)

   def save_analyze_to_transcriptions(self, analyze):

      index = self.getSelectedTranscription()

      print(index)
      # print(analyze)

      if index < 0:

         return

      if len(analyze) < 1:

         return

      new_transcription = self.st.session_state.completed_transcriptions[index]
      new_transcription['analyze'] = analyze
      self.st.session_state.completed_transcriptions[index] = new_transcription
      self.file_handler.save_transcriptions(self.st.session_state.completed_transcriptions)

   def update_session_state(self, file_path, aligned_results, speaker_times):

      self.st.session_state[self.TRANSCRIPTION_RESULT] = aligned_results
      self.st.session_state[self.DIARIZATION_RESULT] = speaker_times
      self.st.session_state[self.TRANSCRIPTION_COMPLETED] = True

      file_name = os.path.basename(file_path)
      base_name = os.path.splitext(file_name)[0]
      summary = self.getSummary()
      analyze = self.getAnalyze()

      new_transcription = {
         'base_name': base_name,
         'file_name': file_name,
         'file_path': file_path,
         'aligned_results': aligned_results,
         'speaker_times': speaker_times,
         'summary': summary,
         'analyze': analyze
      }

      # Check if transcription with the same file_name already exists.
      updated = False

      for i, transcription in enumerate(self.st.session_state.completed_transcriptions):
           
         if transcription['file_name'] == file_name:

            # Overwrite the existing transcription.
            self.st.session_state.completed_transcriptions[i] = new_transcription
            updated = True

            self.setSelectedTranscription(i)

            print(f"Index: {i}.")

            break

      # If no existing transcription is found, append a new one.
      if not updated:

         index = len(self.st.session_state.completed_transcriptions)
         
         self.st.session_state.completed_transcriptions.append(new_transcription)

         self.setSelectedTranscription(index)

         print(f"Index 2: {index}.")

      self.file_handler.save_transcriptions(self.st.session_state.completed_transcriptions)

   def handle_file_upload(self, uploaded_file):

      try:

         file_path = self.utils.save_uploaded_file(uploaded_file)

         if uploaded_file.type == "video/mp4":

            file_path = self.utils.convert_mp4_to_wav(file_path)

         self.process_file(file_path)

      except Exception as e:

         self.st.error(f"Error processing file: {e}")

   def handle_youtube_url(self, youtube_url):

      try:

         file_path = self.utils.download_youtube_audio(youtube_url)

         if file_path and file_path.endswith(".mp4"):

            file_path = self.utils.convert_mp4_to_wav(file_path)

         self.process_file(file_path)

      except Exception as e:

         self.st.error(f"Error processing YouTube URL: {e}")

   def process_transcription_and_diarization(self, file_path):

      transcription_result = self.transcription.transcribe_audio(file_path)
      diarization_result = self.transcription.diarize_audio(file_path)
      aligned_results = self.transcription.align_transcription_with_diarization(transcription_result, diarization_result)
      speaker_times = self.transcription.calculate_speaker_talk_time(diarization_result)

      return aligned_results, speaker_times
    