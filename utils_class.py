import os
import streamlit as st
import ffmpeg
import yt_dlp

class Utils:

   def __init__(self, st_screen):
       
      self.st_screen = st_screen
      self.file_path = ""

   def convert_mp4_to_wav(self, mp4_file_path):

      # Convert an MP4 file to a WAV file.

      temp_dir = "temp"

      if not os.path.exists(temp_dir):

         os.makedirs(temp_dir)

      wav_file_path = os.path.join(temp_dir, os.path.splitext(os.path.basename(mp4_file_path))[0] + ".wav")

      # Check if the file exists
      if os.path.exists(wav_file_path):
         
         # Remove the file
         os.remove(wav_file_path)
         print(f"{wav_file_path} has been deleted.")

      else:
         
         print(f"{wav_file_path} does not exist.")

      ffmpeg.input(mp4_file_path).output(wav_file_path).run()
 
      return wav_file_path

   def save_uploaded_file(self, uploaded_file):

      file_path = os.path.join("temp", uploaded_file.name)

      with open(file_path, "wb") as f:

         f.write(uploaded_file.getbuffer())

      self.file_path = file_path

      return file_path

   # New path_hook function
   def path_hook(self, d):

      if d['status'] == 'finished':

         print("Download completed ...")
         file_path = d['filename']

         self.file_path = file_path

   # Updated download_youtube_audio function
   def download_youtube_audio(self, url):

      try:

         ydl_opts = {
                    'format': 'bestaudio/best',  # Get the best audio-only format
                    'outtmpl': './temp/%(title)s',  # output path
                    'progress_hooks': [self.path_hook],
                    'postprocessors': [{
                       'key': 'FFmpegExtractAudio',
                       'preferredcodec': 'wav',  # Convert to .wav format
                    }],
         }

         self.st_screen.write("Downloading audio from YouTube ...")

         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            
            ydl.download([url])

         self.st_screen.write("Download completed ...")
         print(self.file_path)

         return self.file_path + '.wav'
    
      except Exception as e:

         self.st_screen.error(f"Failed to download YouTube audio: {e}")    

         return None
