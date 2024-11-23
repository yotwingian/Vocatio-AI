
import os
import shutil


class FileOperation:

   def __init__(self):
        
      # Print out more information in the results.
      self.isVerbose = True

   # Chooses if a lot of information should be
   # printed to the screen by the boolean "bIsVerbose". 
   def setIsVerbose(self, bIsVerbose):

      self.isVerbose = bIsVerbose

   # Checks if a lot of information should be printed
   # by the obtained boolean.
   def getIsVerbose(self):

      return self.isVerbose

   def remove_folder_with_files(self, folder_path):
    
      bOK = False

      if os.path.exists(folder_path):
         
         try:
                
            shutil.rmtree(folder_path)  # Recursively delete the folder and its contents.
            if self.isVerbose == True:
               print(f"Folder '{folder_path}' and its contents have been removed.")

         except OSError as e:
                
            print(f"Error: Failed to remove folder '{folder_path}': {e.strerror}.")

      else:

         if self.isVerbose == True:
            print(f"Folder '{folder_path}' does not exist.")

      return bOK

   def move_file(self, source_path, destination_folder):
       
      bOK = False

      try:
                
         # Ensure destination folder exists.
         if not os.path.exists(destination_folder):
      
            os.makedirs(destination_folder)
    
         shutil.move(source_path, destination_folder)
         if self.isVerbose == True:
            print(f"File moved to {destination_folder}.")
         bOK = True

      except (OSError, shutil.Error) as e:
         
         print(f"Error: Failed to move file: {e.strerror}.")

      return bOK

   def copy_file(self, source_path, destination_folder):
     
      bOK = False

      try:
                    
         # Ensure destination folder exists.
         if not os.path.exists(destination_folder):
        
            os.makedirs(destination_folder)
    
         shutil.copy(source_path, destination_folder)  # Use shutil.copy2() for preserving metadata.
         if self.isVerbose == True:
            print(f"File copied to {destination_folder}.")
         bOK = True

      except (OSError, shutil.Error) as e:
         
         print(f"Error: Failed to copy file: {e.strerror}.")

      return bOK

   def remove_file(self, file_path):
      
      bOK = False
    
      if os.path.exists(file_path):
                        
         try:
                  
            os.remove(file_path)
            if self.isVerbose == True:
               print(f"File {file_path} has been deleted.")
            bOK = True

         except OSError as e:
                
            print(f"Error: Failed to delete file '{file_path}': {e.strerror}.")

      else:

         if self.isVerbose == True:
            print(f"File {file_path} does not exist.")

      return bOK

   def remove_folder_if_empty(self, folder_path):
      
      bOK = False

      # Check if the folder exists and is a directory.
      if os.path.isdir(folder_path):
         
         # List the contents of the folder.
         if not os.listdir(folder_path):  # If the list is empty, the folder is empty.
            
            try:
                
               os.rmdir(folder_path)
               if self.isVerbose == True:
                  print(f"Folder '{folder_path}' has been deleted.")
               bOK = True

            except OSError as e:
                
               print(f"Error: {folder_path} could not be deleted: {e.strerror}.")

         else:

            if self.isVerbose == True:
               print(f"Folder '{folder_path}' is not empty.")

      else:
   
         if self.isVerbose == True:
            print(f"Folder '{folder_path}' does not exist or is not a directory.")

      return bOK

   def create_folder_if_not_exists(self, folder_path):
    
      bOK = False

      # Check if the folder already exists.
      if not os.path.exists(folder_path):
         
         try:
            
            # Create the folder (and intermediate directories if needed).
            os.makedirs(folder_path)
            if self.isVerbose == True:
               print(f"Folder '{folder_path}' created successfully.")
            bOK = True

         except OSError as e:
            
            print(f"Error: Unable to create folder '{folder_path}': {e.strerror}.")

      else:

         if self.isVerbose == True:
            print(f"Folder '{folder_path}' already exists.")

      return bOK
