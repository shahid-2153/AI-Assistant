try:
    # When run from Main.py (project root)
    from Backend.TextToSpeech import TextToSpeech
except ModuleNotFoundError:
    # When run directly (VS Code ▶ on this file)
    from TextToSpeech import TextToSpeech
from AppOpener import close, open as appopen 
from webbrowser import open as webopen 
from pywhatkit import search, playonyt  
from dotenv import dotenv_values  
from bs4 import BeautifulSoup  
from rich import print  
from groq import Groq
import threading
import webbrowser  
import subprocess
import requests  
import keyboard 
import asyncio  
import os 

SILENT_MODE = False 



async def speak(text: str):
    await asyncio.to_thread(TextToSpeech, text)

env_vars = dotenv_values('.env')
GroqAPIKey = env_vars.get('GroqAPIKey')  

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", 
           "IZ6rdc", "OSurRd LTKOO", "vLZv6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", 
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask."
]

messages = []

SystemChatBot = [{'role': 'system', 'content': f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

def GoogleSearch(Topic):
    search(Topic) 
    return True  

def Content(Topic):
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'  
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) 

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  
            messages=SystemChatBot + messages,  
            max_tokens=2048,  
            temperature=0.7, 
            top_p=1, 
            stream=True, 
            stop=None 
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content: 
                Answer += chunk.choices[0].delta.content 

        Answer = Answer.replace("</s>", "") 
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data/{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI) 
        file.close()

    OpenNotepad(rf"Data/{Topic.lower().replace(' ', '')}.txt")  
    return True 

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}" 
    webbrowser.open(Url4Search)  
    return True 

def PlayYouTube(query):
    playonyt(query)
    return True  


def build_response(commands: list[str]) -> str:
    opened = []
    closed = []
    played = []

    for cmd in commands:
        if cmd.startswith("open "):
            opened.append(cmd.replace("open ", ""))
        elif cmd.startswith("close "):
            closed.append(cmd.replace("close ", ""))
        elif cmd.startswith("play "):
            played.append(cmd.replace("play ", ""))

    responses = []

    if opened:
        responses.append("opening " + ", ".join(opened))
    if closed:
        responses.append("closing " + ", ".join(closed))
    if played:
        responses.append("playing " + ", ".join(played))

    if responses:
        return "I am " + " and ".join(responses) + "."
    
    return ""


def OpenApp(app, sess=requests.session()):
    try:
        # Try opening local app
        appopen(app, match_closest=True, output=True, throw_error=True)

        # 🔊 Speak success
        return True

    except Exception as e:
        print(f"App not found locally: {app}")
        print(e)

        # 🔊 Speak fallback
        

        # 🔍 Open Google search
        url = f"https://www.{app}.com"
        webbrowser.open(url)
        
        # 🔊 Speak fallback
        
        return True

def CloseApp(app):
    if "chrome" in app:
        pass  
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  
            return True
        except:
            return False 

def System(command):
    def mute():
        keyboard.press_and_release("volume mute") 

    def unmute():
        keyboard.press_and_release("volume mute") 

    def volume_up():
        keyboard.press_and_release("volume up")
    def volume_down():
        keyboard.press_and_release("volume down")  
        
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()

    return True  

async def TranslateAndExecute(commands: list[str]):

    funcs = []  

    for command in commands:
        
        if command.startswith("open "):  

            if "open it" in command:  
                pass

            if "open file" == command: 
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open ")) 
                funcs.append(fun)

        elif command.startswith("general "):  
            pass

        elif command.startswith("realtime "):  
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close ")) 
            funcs.append(fun)

        elif command.startswith("play "): 
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))  
            funcs.append(fun)
            
        elif command.startswith("content "):  
            fun = asyncio.to_thread(Content, command.removeprefix("content ")) 
            funcs.append(fun)

        elif command.startswith("google search "):  
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))  
            funcs.append(fun)

        elif command.startswith("youtube search "):  
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))  
            funcs.append(fun)

        elif command.startswith("system "): 
            fun = asyncio.to_thread(System, command.removeprefix("system "))  
            funcs.append(fun)
        else:
            print(f"No Function Found. For {command}")  

    results = await asyncio.gather(*funcs)  

    for result in results:  
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    open_apps = [c.replace("open ", "") for c in commands if c.startswith("open ")]

    # 🔊 Speak ONLY ONCE
    if len(open_apps) == 1:
        await speak(f"Opening {open_apps[0]}")
    elif len(open_apps) > 1:
       await speak("Opening " + ", ".join(open_apps))

    # 🚀 Execute commands silently
    async for _ in TranslateAndExecute(commands):
        pass

    return True
if __name__ == "__main__":
    asyncio.run(Automation(["open facebook", "open instagram", "open notepad", "open netflix"]))