from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from dotenv import dotenv_values
import os
import mtranslate as mt
import time

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")
if not InputLanguage:
    print("Error: InputLanguage is not set in the .env file.")
    exit()

data_dir = os.path.join(os.getcwd(), "Data")
os.makedirs(data_dir, exist_ok=True)

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            if (recognition) {
                recognition.stop();
            }
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

HtmlCode = HtmlCode.replace("recognition.lang = '';", f"recognition.lang = '{InputLanguage}';")

html_path = os.path.join(data_dir, "Voice.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")

chrome_options.add_argument("--headless=chrome")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--disable-logging")  
chrome_options.add_argument("--log-level=3")  


# 🔹 SET CHROMEDRIVER PATH (MATCHES CHROME 143)
service = Service(r"C:\WebDriver\chromedriver.exe")


driver = webdriver.Chrome(service=service, options=chrome_options)

temp_dir_path = os.path.join(os.getcwd(), "Frontend", "Files")
os.makedirs(temp_dir_path, exist_ok=True)

def SetAssistantStatus(Status):
    status_path = os.path.join(temp_dir_path, "Status.data")
    with open(status_path, "w", encoding="utf-8") as file:
        file.write(Status)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition():
    driver.get("file:///" + html_path.replace("\\", "/"))  
    driver.find_element(By.ID, "start").click()
    
    last_text = ""
    while True:
        try:
            time.sleep(0.5) 
            Text = driver.find_element(By.ID, "output").text.strip()
            if Text and Text != last_text:  
                driver.find_element(By.ID, "end").click()
                if InputLanguage and (InputLanguage.lower() == "en" or "en" in InputLanguage.lower()):
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            pass

if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)
