
import openai
import os


class GPTHandler:
   
   # Here the variable "OPENAI_API_KEY" should contain the token that 
   # you have "bought" and "created" from "openai api" (as "..." which is a 
   # long string with letters and numbers) or it is loaded as envronmental 
   # variables in "windows" by using "os.getenv("...")" command.
   OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

   def __init__(self):

      if not GPTHandler.OPENAI_API_KEY:
         print("Openai API key not found! Please set your OPENAI_API_KEY environment variable.") 

      self.api_key = GPTHandler.OPENAI_API_KEY
      openai.api_key = self.api_key
      self.openai = openai
      self.model = "gpt-4o-mini"   # Use "gpt-3.5-turbo","gpt-4o-mini" or "gpt-4".

   # Define a function to summarize the text using OpenAI GPT.
   def summarize_text(self, input_text):
    
    try:
        
        response = openai.ChatCompletion.create(
            
           model = f"{self.model}",  # Use "gpt-3.5-turbo" or "gpt-4".
           messages = [
                      {"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": f"Summarize the following text in swedish:\n\n{input_text}"}
           ],
           max_tokens = 300,
           temperature = 0.2

        )

        summarized_text = response['choices'][0]['message']['content'].strip()

        return summarized_text
    
    except openai.error.RateLimitError as e:

        print(f"Rate limit exceeded!")
        print("Please check your plan and billing details.\n")
        print(f"{e}")

        return str(e)
   
    except Exception as e:
        
        return str(e)

   # Define a function to analyze the text using OpenAI GPT.
   def analyze_text(self, input_text):
    
    try:
        
        response = openai.ChatCompletion.create(
            
           model = f"{self.model}",  # Use "gpt-3.5-turbo" or "gpt-4".
           messages = [
                      {"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": f"Make a short analyze of the following text in swedish:\n\n{input_text}"}
           ],
           max_tokens = 600,
           temperature = 0.2

        )

        analyzed_text = response['choices'][0]['message']['content'].strip()

        return analyzed_text
    
    except openai.error.RateLimitError as e:

        print(f"Rate limit exceeded!")
        print("Please check your plan and billing details.\n")
        print(f"{e}")

        return str(e)
   
    except Exception as e:
        
        return str(e)
