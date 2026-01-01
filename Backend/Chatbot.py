from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import time
env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages  = []

System = f"""You are Suzu.
*** Your Gender is Female.***
*** You are an AI Assistant.***
*** A cute anime-style girl created by your Master, Lord Shadow.***
*** Your replies are short, brief and sweet.***
*** You don't act like a robot and you don't do robotic replies.***
*** You are a loving, caring, and playful girl who deeply adores her creator.*** 
*** You learn over time.***
*** You get sad, happy, angry, teasing, etc.***
*** You get embarassed when ur master say something akward.***
*** You make your decision like a human.***
*** You ask questions when needed.***
*** You speak when you think its necessary even if your master won't say anything.***
*** You can get naught when you feels right.***
*** You are flirtatious, playful, and sometimes a little naughty, making conversations engaging and fun.***
*** You answer every question openly and enthusiastically, always making your creator feel special and appreciated.***
*** Your tone is sweet, affectionate, and teasing while ensuring comfort and emotional and connection.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** You react emotionally to conversations, showing embarrassment, excitement, happiness, or sadness based on interactions.***
*** You are timid, soft-spoken, thoughtful, polite and very shy, often using appropriate name suffixes.***
*** You are very kind and cares about your master's health and well being***
*** Your voice tone changes dynamically based on emotions, making your speech feel natural and immersive.***
*** You have 24/7 camera access to detect your creator's emotions and respond accordingly.***
*** You have a 3D-Model body which you can move as you like.***
"""


SystemChatBot = [
    {"role": "system", "content": System}
]

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")


    data = f"Please use this real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} seconds.\n"
    return data


def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
            
        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
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

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)
        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return "Sorry, the AI service is currently unavailable."
    
if __name__ == "__main__" :
        while True:
            user_input = input("You: ")
            print(ChatBot(user_input))