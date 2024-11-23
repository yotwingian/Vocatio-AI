
import streamlit as st

class OutputManager:

    def __init__(self, st):

        self.st_screen = st

    def write_full_conversation(self, full_conversation, max_length = 71):

        all_conversation = "Transcription Result:\n\n"
        speaker_before = ""
        
        for start, speaker, text in full_conversation:
            blank_line = " " * (len("SPEAKER_01") + 1)
            add_to_line = f"{blank_line} " if speaker == speaker_before else f"{speaker}: " if speaker != "UNKNOWN" else f"{speaker}:    "
            
            split_part_new = text.strip()
            first = True
            
            while split_part_new:
                split_part_b, split_part_new, _ = self.split_sentence(split_part_new, max_length)
                split_part_b = split_part_b.strip()
                all_conversation += add_to_line + split_part_b + "\n"
                
                if first:
                    add_to_line = f"{blank_line} "
                    first = False
            
            speaker_before = speaker
        
        all_conversation += "\n\n\n"
        self.st_screen.text(all_conversation)

    def write_talk_times(self, speaker_times, use_blank_rows):
        if use_blank_rows:
            self.st_screen.write("")
            self.st_screen.write("")
            self.st_screen.write("")
        
        str_talk_time = "Speaker Talk Times:\n\n\n"
        for speaker, time in speaker_times.items():
            str_talk_time += f"{speaker}: {time} seconds.\n\n"
        
        self.st_screen.text(str_talk_time)

    def split_sentence(self, sentence, max_length):
        if len(sentence) <= max_length:
            return sentence, "", 0
        
        trimmed_sentence = sentence[:max_length]
        last_space_index = trimmed_sentence.rfind(" ")
        
        if last_space_index == -1:
            return sentence, "", 0
        
        part_before = sentence[:last_space_index].strip()
        part_after = sentence[last_space_index + 1:].strip()
        length_part_a = len(part_after)
        
        return part_before, part_after, length_part_a

    def format_full_conversation(self, full_conversation):

        formatted_conversation = ""
        for start, speaker, text in full_conversation:
            formatted_conversation += f"{start:.2f} - {speaker}: {text}\n"
            
        return formatted_conversation
    