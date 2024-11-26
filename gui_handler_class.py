
import streamlit as st
import os
from main_handler_class import MainHandler
from email_handler_class import EmailHandler


class GUIHandler:

   # Here the "email adress" ("SMTP_EMAIL_USER") and "password" 
   # ("SMTP_EMAIL_PASSWORD") is used (as for instance 
   # "kalle@gmail.com" and "password1") from where you send your emails 
   # or it is loaded as envronmental variables in "windows" by using
   # "os.getenv("...")" command.
   SMTP_EMAIL_USER = os.getenv("SMTP_EMAIL_USER")
   SMTP_EMAIL_PASSWORD = os.getenv("SMTP_EMAIL_PASSWORD")

   def __init__(self, st, email_handler = None):

      if not GUIHandler.SMTP_EMAIL_USER:
         print("Email address not found! Please set your SMTP_EMAIL_USER environment variable.")

      if not GUIHandler.SMTP_EMAIL_PASSWORD:
         print("Email password not found! Please set your SMTP_EMAIL_PASSWORD environment variable.")

      self.st = st

      self.main_handler = MainHandler(self.st)

      self.email_handler = email_handler or EmailHandler(
         smtp_server = "smtp.gmail.com",
         smtp_port = 587,
         smtp_user = GUIHandler.SMTP_EMAIL_USER,
         smtp_password = GUIHandler.SMTP_EMAIL_PASSWORD
      )

   def initialize_session_state(self):

      self.main_handler.initialize_session_state()

   def reset_session_state(self):
      
      self.main_handler.reset_session_state()
      
   def display_title_and_description(self):

      self.st.title("Vocatio AI")
      self.st.write("Welcome to the Audio Transcription and Diarization App. You can transcribe audio from a file or a YouTube URL.")

   def handle_user_options(self):

      option = st.radio("Choose an option:", ("Transcribe from File", 
                        "Transcribe from YouTube URL"),
                        on_change = self.reset_session_state  # Reset the state when the user changes options.
      )

      if option == "Transcribe from File":

         self.handle_file_upload()

      elif option == "Transcribe from YouTube URL":

         self.handle_youtube_url()

   def handle_file_upload(self):

      uploaded_file = self.st.file_uploader("Choose an audio file:", type=["wav", "mp4"], on_change = self.main_handler.reset_session_state)

      if uploaded_file and not self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:

         self.main_handler.handle_file_upload(uploaded_file)

   def handle_youtube_url(self):

      youtube_url = self.st.text_input("Enter YouTube URL", on_change = self.main_handler.reset_session_state)

      if youtube_url and not self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:

         self.main_handler.handle_youtube_url(youtube_url)

   def display_results(self):

      if self.main_handler.TRANSCRIPTION_RESULT in self.st.session_state and self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:

         full_conversation = self.st.session_state[self.main_handler.TRANSCRIPTION_RESULT].get("full_conversation", [])
         formatted_conversation = [(entry[0], entry[1], entry[2]) for entry in full_conversation]
         self.main_handler.output_manager.write_full_conversation(formatted_conversation)
         # self.main_handler.output_manager.write_talk_times(self.st.session_state[self.main_handler.DIARIZATION_RESULT], use_blank_rows = True)

         if self.st.download_button("Download Transcription", self.main_handler.output_manager.format_full_conversation(formatted_conversation), file_name = "transcription.txt"):

            self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED] = True

   def display_summary_button(self):
      
      if self.main_handler.TRANSCRIPTION_RESULT in self.st.session_state and self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:
         
         if self.st.button("Summarize"):

            if self.main_handler.getIsSummaryAlreadyPressed() == False:
               
               if self.isSummaryAvailable() == False:

                  self.summarize_transcription()

                  print(f"Summarize is pressed and gets new results.")              

               self.main_handler.setIsSummaryAlreadyPressed(True)

   def summarize_transcription(self):

      if self.main_handler.TRANSCRIPTION_RESULT in self.st.session_state and self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:

         summary = self.main_handler.gpt_handler.summarize_text(self.st.session_state[self.main_handler.TRANSCRIPTION_RESULT])
         self.main_handler.setSummary(summary)
         self.main_handler.save_summary_to_transcriptions(summary)

      else:

         self.st.write("No transcription result available to summarize.")

   def display_existing_summary(self):
      
      if self.main_handler.TRANSCRIPTION_RESULT in self.st.session_state and self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:
      
         if len(self.main_handler.getSummary()) > 0:

            self.st.write("Summary:")
            self.st.write(self.main_handler.getSummary())

   def display_analyze_button(self):
      
      if self.main_handler.TRANSCRIPTION_RESULT in self.st.session_state and self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:
         
         if self.st.button("Analyze"):

            if self.main_handler.getIsAnalyzeAlreadyPressed() == False:

               if self.isAnalyzeAvailable() == False:
               
                  self.analyze_transcription()

                  print(f"Analyze is pressed and gets new results.")

               self.main_handler.setIsAnalyzeAlreadyPressed(True)

   def analyze_transcription(self):

      if self.main_handler.TRANSCRIPTION_RESULT in self.st.session_state and self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:

         analyze = self.main_handler.gpt_handler.analyze_text(self.st.session_state[self.main_handler.TRANSCRIPTION_RESULT])
         self.main_handler.setAnalyze(analyze)
         self.main_handler.save_analyze_to_transcriptions(analyze)

      else:

         self.st.write("No transcription result available to analyze the text.")

   def display_existing_analyze(self):
      
      if self.main_handler.TRANSCRIPTION_RESULT in self.st.session_state and self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:
      
         if len(self.main_handler.getAnalyze()) > 0:

            self.st.write("Analyze:")
            self.st.write(self.main_handler.getAnalyze())

   def isSummaryAvailable(self):

      bOK = False

      index = self.main_handler.getSelectedTranscription()

      if index < 0:

         return bOK

      selected_transcription = self.st.session_state.completed_transcriptions[index]

      if len(selected_transcription['summary']) < 1:

         return bOK
      
      bOK = True

      return bOK
   
   def isAnalyzeAvailable(self):

      bOK = False

      index = self.main_handler.getSelectedTranscription()

      if index < 0:

         return bOK

      selected_transcription = self.st.session_state.completed_transcriptions[index]

      if len(selected_transcription['analyze']) < 1:

         return bOK
      
      bOK = True

      return bOK

   # Define a callback function to be triggered after deletion.
   def delete_and_update(self):
        
      selected_transcription = self.st.session_state["transcription_selectbox"]

      # Perform the deletion.
      self.delete_selected_transcription(selected_transcription)

      # Force the selectbox to update by resetting the selected value.
      if len(self.st.session_state.completed_transcriptions) > 0:
            
         # Reset the selectbox to the first item after deletion.
         self.st.session_state.transcription_selectbox = 0

      else:
            
         # If no transcriptions left, clear the selectbox.
         del self.st.session_state.transcription_selectbox

   def display_saved_transcriptions(self):

      if 'completed_transcriptions' in self.st.session_state and self.st.session_state.completed_transcriptions:

         # Ensure transcriptions are displayed if they exist
         if len(self.st.session_state.completed_transcriptions) > 0:

            selected_transcription = self.st.selectbox(
                  "Select a previous transcription:",
                  options = range(len(self.st.session_state.completed_transcriptions)),
                  format_func = lambda x: self.st.session_state.completed_transcriptions[x]['base_name'],
                  key = "transcription_selectbox"  # Add a key to persist the selectbox.
            )

            if self.st.button("Load Transcription"):

               self.load_selected_transcription(selected_transcription)

            if self.st.button("Delete Transcription", on_click = self.delete_and_update):

               # The deletion and UI update is handled via callback function.
               pass

   def load_selected_transcription(self, selected_transcription):

      self.reset_session_state()
      transcription_data = self.st.session_state.completed_transcriptions[selected_transcription]
      self.st.session_state[self.main_handler.TRANSCRIPTION_RESULT] = transcription_data['aligned_results']
      self.st.session_state[self.main_handler.DIARIZATION_RESULT] = transcription_data['speaker_times']
      self.main_handler.setSummary(transcription_data['summary'])
      self.main_handler.setAnalyze(transcription_data['analyze'])
      self.st.session_state.completed_transcriptions[selected_transcription] = transcription_data
      self.main_handler.setSelectedTranscription(selected_transcription)
      self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED] = True
      self.st.success("Transcription loaded successfully.")

   def delete_selected_transcription(self, selected_transcription):

      bOK = False

      transcriptions = self.st.session_state.completed_transcriptions
      n_max = len(transcriptions)

      if selected_transcription > n_max or selected_transcription < 0:

         return bOK
      
      bOK = True

      # Remove the selected transcription.
      del transcriptions[selected_transcription]
      self.st.session_state.completed_transcriptions = transcriptions  # Update the session state.

      # Save the new transcription list.
      self.main_handler.file_handler.save_transcriptions(self.st.session_state.completed_transcriptions)

      self.st.success("Transcription is deleted successfully.")
      print(f"Transcription with index ({selected_transcription}) is deleted successfully.")

      # Clear the current selection and reset index. 
      index = -1
      self.main_handler.setSelectedTranscription(index)

      return bOK 

   def send_email_with_transcription(self):

      email = self.st.text_input("Enter your email address:")

      if self.st.button("Send Email"):

         if email and self.main_handler.TRANSCRIPTION_RESULT in self.st.session_state and self.st.session_state[self.main_handler.TRANSCRIPTION_COMPLETED]:

            transcription = self.main_handler.output_manager.format_full_conversation(self.st.session_state[self.main_handler.TRANSCRIPTION_RESULT].get("full_conversation", []))
            summary = self.main_handler.getSummary()

            if len(summary) < 1:
                    
                    self.st.error("No available summary.")

                    return
                
            email_body = f"Transcription:\n\n{transcription}\n\nSummary:\n\n{summary}"

            if self.email_handler.send_email(email, "Your Transcription and Summary", email_body):

               self.st.success("Email sent successfully.")

            else:

               self.st.error("Failed to send email.")

         else:

            self.st.error("No transcription result available or email address is empty.")

   def run(self):

      self.initialize_session_state()
      self.display_title_and_description()
      self.handle_user_options()
      self.display_saved_transcriptions()
      self.display_results()
      self.display_summary_button()
      self.display_analyze_button()
      self.send_email_with_transcription()
      self.display_existing_summary()
      self.display_existing_analyze()
