# Vocatio AI

## Description

The program can create a transcription from an audio (.mp4) or video file (.wav). It also performs speaker diarization of the conversation. This is particularly useful for recording meetings in Teams. Additionally, it can provide a summary or analysis of the conversation. The conversation, along with the summary and analysis, can be stored in the program, and old stored conversations can also be deleted. It is a Streamlit application.

## Features

- Transcribe audio from files (wav, mp4) or YouTube URLs.

- Perform speaker diarization to identify and separate different     speakers in the audio.

- Display full conversation transcripts.

- Summarize and analyze transcriptions using OpenAI GPT.

- Save, load, and delete transcriptions.

- Send transcriptions and summaries via email.

## Installation

Python version required: 3.10

Libraries in requirements.txt:
ffmpeg
whisper
pyannote.audio
streamlit
openai==0.28.0
yt_dlp

You can install these packages by running the following command in your terminal:

pip install -r requirements.txt

## Keys

- The OpenAI API key (OPENAI_API_KEY) needs to be bought and it is recommended to set this key in the environmental variables.

- The diarization key (AUTH_TOKEN_VOCATIO) from Hugging Face needs to be set and it is recommended to set this key in the environmental variables.

- The email address (SMTP_EMAIL_USER) needs to be set and it is recommended to set this key in the environmental variables.

- The email password (SMTP_EMAIL_PASSWORD) needs to be set and it is recommended to set this key in the environmental variables.

- You can set a environmental key like this in windows in your project folder: setx OPENAI_API_KEY ".....key_value......"


## Running the Program

streamlit run app.py
