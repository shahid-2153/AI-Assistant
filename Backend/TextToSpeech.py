import pygame
import random
import asyncio
import edge_tts
import os 
import time
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")
async def TextToAudioFile(text) -> str:
    file_path = rf"Data\speech_{int(time.time()*1000)}.mp3"

    communicate = edge_tts.Communicate(
        text,
        AssistantVoice,
        pitch='+5Hz',
        rate='+13%'
    )
    await communicate.save(file_path)
    return file_path


def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            audio_file = asyncio.run(TextToAudioFile(Text))
            
            pygame.mixer.quit()
            pygame.mixer.init()

            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if func() == False: 
                    break
                pygame.time.Clock().tick(10) 
            return True
        
        except Exception as e:
            print (f"Error in TTS: {e}")        
          
        finally:
            try:
                func(False)
                pygame.mixer.music.stop() 
                pygame.mixer.quit() 

            except Exception as e: 
                print(f"Error in finally block: {e}")
            if os.path.exists(audio_file):
                os.remove(audio_file)

def TextToSpeech (Text, func=lambda r=None: True):
    Data = str(Text).split(".")
    
    TTS(Text, func)

if __name__ == "__main__":
    while True:
        TextToSpeech(input("You:"))